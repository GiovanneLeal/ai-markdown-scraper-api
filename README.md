# 🕸️ AI Markdown Scraper API

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)
![Selenium](https://img.shields.io/badge/Selenium-Undetected-43B02A.svg)

Uma API REST de extração de dados construída especificamente para alimentar **Agentes de Inteligência Artificial (LLMs) e sistemas RAG**. 

A internet moderna é caótica e cheia de proteções. Esta API resolve dois problemas fundamentais: **1)** contorna sistemas anti-bot complexos (Exceto os da Amazon até o momento...) e **2)** converte o HTML poluído da web em documentos Markdown limpos e estruturados, economizando milhares de tokens no contexto da sua IA.

---

## 🚀 O Problema vs. A Solução

**O Problema:** IAs e LLMs sofrem para ler páginas web diretamente. O HTML cru gasta limite de tokens rapidamente e confunde o modelo com menus, anúncios, scripts e pop-ups de cookies. Além disso, sites bloqueiam bots tradicionais instantaneamente.

**A Solução:** Nossa API usa uma versão indetectável do Chrome rodando em um monitor virtual para simular um humano real. Em seguida, processa a página usando o algoritmo `Readability` (para focar apenas no conteúdo principal) e converte tudo para Markdown puro.

## ✨ Funcionalidades Principais

* 🛡️ **Evasão Anti-Bot:** Utiliza `undetected_chromedriver` e táticas de *eager loading* para simular navegação humana real.
* 🧹 **Limpeza de HTML:** Filtra barras laterais, menus, rodapés e anúncios, extraindo apenas o que é importante no conteúdo.
* 📝 **Saída em Markdown:** Formato perfeito para consumo por modelos de linguagem (OpenAI, Anthropic, Llama, etc).
* ☁️ **Cloud Native & Dockerized:** Configurado com `Xvfb` (Monitor Virtual) para execução *headless* segura em servidores Linux/Nuvem (ex: Fly.io).
* 🔐 **Gatekeeper de Pagamento/Autenticação:** Rota protegida por um validador de cabeçalho (`x-payment-hash`), pronto para monetização Web3, microtransações ou controle de acesso estrito.
* ⚡ **Cache Inteligente:** Memoriza URLs recém-raspadas para responder em milissegundos e poupar recursos do servidor.

---

## 🛠️ Stack Tecnológica

* **Backend:** FastAPI (Python)
* **Scraping Engine:** Selenium + Undetected Chromedriver
* **Processamento de Texto:** `readability-lxml` + `html2text`
* **Infraestrutura:** Docker + Xvfb

---

## ⚙️ Como rodar localmente

### 1. Pré-requisitos
Certifique-se de ter o **Docker** e o **Docker Compose** instalados na sua máquina.

### 2. Instalação
Clone o repositório e acesse a pasta do projeto:
```bash
git clone [https://github.com/GiovanneLeal/ai-markdown-scraper-api.git](https://github.com/GiovanneLeal/ai-markdown-scraper-api.git)
cd ai-markdown-scraper-api
```

### 3. Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com as suas chaves de segurança:
```bash
Snippet de código
WALLET_ADDRESS=sua_carteira_aqui
ADMIN_SECRET=sua_senha_secreta
```
### 4. Construindo e Executando (Docker)
Inicie o container para construir o ambiente com o Chrome invisível:
```bash
docker build -t ai-scraper-api .
docker run -p 8000:8000 --env-file .env ai-scraper-api
```
A API estará disponível em http://localhost:8000. Acesse http://localhost:8000/docs para interagir com o Swagger UI.

### 📡 Como Usar (Endpoint)
```bash
POST /scrape
```
Endpoint principal para raspar uma URL. Requer autenticação no cabeçalho.

### Exemplo de Requisição (cURL):
```bash
curl -X 'POST' \
  'http://localhost:8000/scrape' \
  -H 'accept: application/json' \
  -H 'x-payment-hash: sua_senha_secreta' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://pt.wikipedia.org/wiki/Web_scraping"}'
```
### Exemplo de Resposta:
```bash
JSON
{
  "status": "success",
  "cached": false,
  "data": "# Web scraping\n\nWeb scraping é a extração de dados de sites da web. Isso é feito por meio de um software que simula a navegação humana..."
}
```
---

### ⚠️ Aviso Legal e Ética
Nota Importante: Este projeto tem fins educacionais e de demonstração de arquitetura de software. O Web Scraping deve ser feito com responsabilidade. Sempre verifique o arquivo robots.txt e os Termos de Serviço do site alvo antes de realizar a extração de dados em larga escala.

---
