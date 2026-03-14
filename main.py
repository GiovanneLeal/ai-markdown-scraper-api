import os
import logging
from dotenv import load_dotenv
from web3 import Web3
from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import html2text
import time
from readability import Document

# = CARREGA O COFRE DE SENHAS (.env)
load_dotenv()

# - CONFIGURAÇÕES FINANCEIRAS
MINHA_CARTEIRA = os.getenv("WALLET_ADDRESS", "0x71C7656EC7ab88b098defB751B7401B5f6d8976F")
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "fsndfn243535nsdk") 

USDC_CONTRACT_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
VALOR_PRECO_USDC = 0.005
VALOR_EXIGIDO_RAW = int(VALOR_PRECO_USDC * (10**6)) 

# Conexão com a rede Base
w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
hashes_utilizados = set()

# - SISTEMA DE CACHE 
# Guarda o resultado de URLs já visitadas para economizar servidor
# Formato: {"url": {"markdown": "texto...", "timestamp": 17000000}}
cache_paginas = {}
TEMPO_CACHE_SEGUNDOS = 3600 # O cache dura 1 hora (3600 segundos)

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="A2A Web Scraper", description="Converts URLs to clean Markdown. Pay per use via USDC on Base.")

class ScrapeRequest(BaseModel):
    url: str

# - AUDITORIA BLOCKCHAIN
def verify_blockchain_transaction(tx_hash: str):
    if tx_hash in hashes_utilizados:
        return False, "Payment hash already used in this session."
    
    try:
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        if receipt['status'] != 1: 
            return False, "Transaction failed on blockchain."
        
        if tx['to'].lower() != USDC_CONTRACT_BASE.lower(): 
            return False, "Payment was not made in USDC."
            
        input_data = tx['input'].hex() if hasattr(tx['input'], 'hex') else str(tx['input'])
        if not input_data.startswith('0xa9059cbb'): 
            return False, "Invalid format. Must be ERC-20 transfer."
            
        endereco_destino = "0x" + input_data[34:74]
        valor_pago_raw = int(input_data[74:], 16)
        
        if endereco_destino.lower() != MINHA_CARTEIRA.lower(): 
            return False, "Payment sent to the wrong wallet."
            
        if valor_pago_raw < VALOR_EXIGIDO_RAW: 
            return False, "Insufficient payment."

        # - BLINDAGEM CONTRA REPLAY ATTACK 
        bloco = w3.eth.get_block(receipt['blockNumber'])
        tempo_transacao = bloco['timestamp']
        tempo_atual = time.time()
        IDADE_MAXIMA_SEGUNDOS = 900 
        idade_transacao = tempo_atual - tempo_transacao
        
        if idade_transacao > IDADE_MAXIMA_SEGUNDOS:
            return False, f"Transaction is too old. Must be within the last 15 minutes. This one is {int(idade_transacao/60)} minutes old."

        return True, "Payment Validated"
        
    except Exception as e: # Se o hash não existir ou a rede falhar
        return False, f"Failed to verify transaction. Reason: {str(e)}"
    
def payment_gatekeeper(x_payment_hash: str = Header(None)): #Impede o acesso sem pagamento e libera o Administrador.
    if not x_payment_hash:
        raise HTTPException(
            status_code=402, 
            detail={
                "error": "Payment Required",
                "message": "Please send a valid USDC transaction hash on the Base network using the 'x-payment-hash' header.",
                "price": f"{VALOR_PRECO_USDC} USDC",
                "wallet": MINHA_CARTEIRA,
                "network": "Base Mainnet"
            }
        )
    
    if x_payment_hash == ADMIN_SECRET: # Atalho do Administrador (Para testes sem pagamentos)

        logger.info("Acesso de Administrador liberado.")
        return True

    is_valid, error_msg = verify_blockchain_transaction(x_payment_hash) # Se enviou um hash, vai na Blockchain conferir
    
    if not is_valid:
        raise HTTPException(status_code=403, detail={"error": "Forbidden", "message": error_msg})
    
    hashes_utilizados.add(x_payment_hash)
    logger.info(f"Pagamento recebido e validado: {x_payment_hash}")
    return True

# - O NOVO MOTOR INDETECTÁVEL
def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = uc.Chrome(options=options) # O uc.Chrome vai achar o Google Chrome Oficial do Docker sozinho
    return driver

# - A RASPAGEM PREMIUM
@app.post("/scrape", dependencies=[Depends(payment_gatekeeper)])
def scrape_url(request: ScrapeRequest):

    # Ajuste da URL
    url_alvo = request.url
    if not url_alvo.startswith("http"):
        url_alvo = "https://" + url_alvo

    # Verificação de Cache
    agora = time.time()
    if url_alvo in cache_paginas:
        dados_salvos = cache_paginas[url_alvo]
        if agora - dados_salvos["timestamp"] < TEMPO_CACHE_SEGUNDOS:
            return {
                "status": "success", 
                "cached": True, 
                "data": dados_salvos["markdown"]
            }

    driver = None
    try:
        # Inicialização do Motor Fantasma na Nuvem
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(30)
        driver.get(url_alvo)

        # Lendo e limpando o HTML
        from readability import Document
        import html2text
        doc = Document(driver.page_source)
        html_limpo = doc.summary()
        
        # Convertendo para Markdown
        converter = html2text.HTML2Text()
        converter.ignore_links = False
        converter.body_width = 0
        markdown_final = converter.handle(html_limpo) 
        
        # Salva no Cache
        cache_paginas[url_alvo] = {
            "markdown": markdown_final, 
            "timestamp": agora
        }
        
        # Retorna o Markdown real!
        return {
            "status": "success", 
            "cached": False, 
            "data": markdown_final
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": "Falha na raspagem", "message": str(e)})
    
    finally: # Fechamento seguro
        if driver:
            try:
                driver.quit()
            except:
                pass

@app.get("/")
def home():
    if __name__ == "__main__":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    return {
        "status": "online", 
        "message": "A2A Web Scraper is running. Use POST /scrape to convert URLs to Markdown.",
        "documentation": "/docs"
    }