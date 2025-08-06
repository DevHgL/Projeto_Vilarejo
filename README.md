# 🏨 Jornada do Hóspede 360° com IA (Protótipo "Alfred")

## 📜 Descrição

Este projeto é um protótipo funcional de um concierge virtual hoteleiro, apelidado de "Alfred". O sistema automatiza a comunicação pré-hospedagem, enviando mensagens personalizadas e contextuais para os hóspedes, com o objetivo de resolver problemas operacionais, aumentar a receita (RevPAR) e melhorar drasticamente a satisfação do cliente (NPS), gerando fidelização.

O protótipo foi desenvolvido como solução para um case de avaliação técnica, demonstrando a aplicação prática de IA Generativa, integrações de API e boas práticas de desenvolvimento de software em um contexto de negócio real para a indústria hoteleira.

## ✨ Principais Funcionalidades

  - **Automação Proativa:** O sistema monitora novas reservas em tempo real e inicia o contato com o hóspede sem intervenção humana.
  - **Hiper-Personalização:** As mensagens são personalizadas com base em um rico conjunto de dados do hóspede, incluindo:
      - Histórico (primeira visita ou recorrente).
      - Motivo da viagem (família, negócios, lua de mel).
      - Composição da reserva (número de adultos e crianças).
  - **Inteligência Contextual:** O sistema se conecta a calendários externos para obter informações sobre feriados nacionais, tornando as dicas ainda mais relevantes e oportunas.
  - **Detecção de Recorrência:** Analisa o histórico de reservas para identificar hóspedes fiéis e recebê-los com uma saudação especial.
  - **Arquitetura Segura e Modular:** As chaves de API e credenciais são protegidas usando variáveis de ambiente (`.env`), e o código é organizado em módulos de serviço para facilitar a manutenção e futuras atualizações.
  - **Modo de Demonstração Estável:** Possui um modo de simulação que garante uma apresentação à prova de falhas, focada na lógica de negócio e na experiência do usuário.

## 🚀 Arquitetura e Tecnologias Utilizadas

O projeto segue um fluxo de dados claro e utiliza um conjunto de tecnologias modernas e eficientes.

**Fluxo:** `Google Sheets (Gatilho)` → `Python Script (Orquestrador)` → `Google Calendar API (Contexto)` → `IA Generativa (Cérebro)` → `Telegram API (Notificação)`

  - **Backend:** Python 3.12+
  - **Base de Dados (Protótipo):** Google Sheets
  - **Serviços Google:**
      - `gspread` & `oauth2client` para interagir com o Google Sheets.
      - `google-api-python-client` para interagir com o Google Calendar API.
  - **Inteligência Artificial:** O sistema é agnóstico e foi validado com múltiplas APIs (OpenAI, Google Gemini, DeepSeek, OpenRouter), utilizando um modo de simulação para a demonstração final.
  - **Notificações:** Telegram Bot API (via `requests`).
  - **Segurança:** `python-dotenv` para gerenciamento de segredos.
  - **Geração de Dados de Teste:** `Faker` para popular a planilha com dados fictícios realistas.

## ⚙️ Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1\. Pré-requisitos

  - Python 3.10 ou superior
  - Uma Conta Google

### 2\. Instalação

1.  **Clone o repositório (exemplo):**
    ```bash
    git clone https://github.com/seu-usuario/projeto-hotel.git
    cd projeto-hotel
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### 3\. Configuração das APIs e Credenciais

1.  **Google Cloud:** Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/), ative as APIs "Google Drive API", "Google Sheets API" e "Google Calendar API". Crie uma **Conta de Serviço**, gere uma chave **JSON** e salve o arquivo como `credentials.json` na raiz do projeto.
2.  **Google Workspace:**
      - Crie uma planilha no **Google Sheets** com os cabeçalhos especificados no `populate_sheet.py`.
      - Compartilhe a planilha com o `client_email` da sua conta de serviço (encontrado no `credentials.json`), dando permissão de **Editor**.
3.  **Crie o arquivo `.env`:** Renomeie o arquivo `.env.example` (se houver) para `.env` e preencha com suas chaves de API e IDs.
    ```dotenv
    # Exemplo de .env
    TELEGRAM_BOT_TOKEN="SEU_TOKEN_DO_TELEGRAM"
    TELEGRAM_CHAT_ID="SEU_CHAT_ID"
    GOOGLE_SHEET_NAME="Reservas"
    PUBLIC_HOLIDAY_CALENDAR_ID="pt-br.brazilian#holiday@group.v.calendar.google.com"
    ```

## ▶️ Como Usar

O projeto consiste em dois scripts principais:

**1. Popular a Base de Dados (Opcional):**
Para gerar dados de teste realistas na sua planilha, execute:

```bash
python populate_sheet.py
```

**2. Iniciar o Assistente Virtual:**
Para iniciar o monitoramento de novas reservas, execute o script principal:

```bash
python main.py
```

O bot começará a verificar a planilha a cada 60 segundos por novas reservas e a processá-las. Para parar, pressione `CTRL+C`.

## 🗂️ Estrutura do Projeto

```
/projeto_hotel/
|-- .env                    # Arquivo com as chaves e segredos (ignorado pelo Git)
|-- .gitignore              # Arquivos e pastas ignorados pelo Git
|-- credentials.json        # Chave da Conta de Serviço do Google (ignorado pelo Git)
|-- main.py                 # Ponto de entrada da aplicação, orquestra o fluxo
|-- populate_sheet.py       # Script para gerar dados de teste
|-- requirements.txt        # Lista de dependências Python
|-- services/
|   |-- __init__.py
|   |-- gcp_service.py      # Módulo para interagir com Google Sheets e Calendar
|   |-- ai_service.py       # Módulo que gera as mensagens personalizadas
|   |-- notification_service.py # Módulo que envia as notificações via Telegram
```

## 🗺️ Roadmap e Evolução Futura

Este protótipo representa a **Fase 1** de um projeto maior. Os próximos passos incluem:


  - **Fase 2 (Concierge Durante a Hospedagem):** Implementar um chatbot interativo via **Telegram** para responder a perguntas e fazer sugestões proativas (reservas de spa, jantar), aumentando o RevPAR.
  - **Fase 3 (Elo de Fidelidade):** Desenvolver um módulo de análise de dados pós-hospedagem para enviar ofertas personalizadas e incentivar reservas diretas.
  - **Melhorias de Arquitetura:**
      - Migrar de Google Sheets para um banco de dados relacional (ex: PostgreSQL).
      - Integrar diretamente com a API de um **Property Management System (PMS)** hoteleiro.
      - Fazer o deploy do script como um serviço de backend na nuvem (AWS Lambda ou Google Cloud Functions).

-----