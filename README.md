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
