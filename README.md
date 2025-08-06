# 🏨 Jornada do Hóspede 360° com IA: O Planejador Antecipado

Este repositório contém o protótipo funcional da **Fase 1** do projeto "Jornada do Hóspede 360°". O objetivo desta fase é resolver o problema do "silêncio" pós-reserva, automatizando um primeiro contato acolhedor e hiper-personalizado com o hóspede antes mesmo de sua chegada.

O sistema é orquestrado por um assistente virtual, apelidado de **"Alfred"**, que utiliza dados do hóspede e contexto em tempo real para criar uma experiência de boas-vindas única, que alivia a ansiedade da viagem e fortalece o relacionamento com a marca desde o primeiro momento.

## ✨ Funcionalidades Implementadas

  - **Automação Proativa do Contato Pré-Hospedagem:** O sistema monitora continuamente por novas reservas e inicia o contato de forma autônoma.
  - **Hiper-Personalização Contextual:** As mensagens são geradas com base em múltiplos pontos de dados para criar um texto único para cada hóspede:
      - **Detecção de Recorrência:** Analisa o histórico na base de dados para identificar se é a primeira visita ou se o hóspede é recorrente, adaptando a saudação.
      - **Perfil da Reserva:** Considera o motivo da viagem (ex: Férias em Família, Lua de Mel) e a composição do grupo (número de crianças) para oferecer dicas relevantes.
      - **Consciência de Eventos:** Integra-se com calendários públicos para identificar feriados nacionais durante a estadia do hóspede e mencionar a festividade na mensagem.
  - **Arquitetura Segura e Modular:** As credenciais e chaves de API são gerenciadas de forma segura através de variáveis de ambiente (`.env`) e o código é estruturado em módulos de serviço, seguindo boas práticas de desenvolvimento.
  - **Modo de Demonstração Estável:** O sistema opera com um gerador de mensagens simulado que utiliza toda a lógica de personalização, garantindo uma demonstração ao vivo 100% estável e à prova de falhas de API externas.
  - **Geração de Dados para Testes:** Inclui um script auxiliar (`populate_sheet.py`) que utiliza a biblioteca `Faker` para popular a base de dados com dezenas de reservas fictícias realistas, permitindo testes robustos e demonstrações mais ricas.

## 🚀 Arquitetura e Tecnologias

O protótipo da Fase 1 opera com o seguinte fluxo e tecnologias:

**Fluxo de Dados:** `Google Sheets (Base de Dados)` → `Python Script (Orquestrador)` → `Google Calendar API (Feriados)` → `Lógica de IA Simulada (Cérebro)` → `Telegram API (Canal de Notificação)`

  - **Backend:** Python 3.10+
  - **Base de Dados (Protótipo):** Google Sheets
  - **Serviços Google:**
      - `gspread`: Para manipulação da planilha.
      - `google-api-python-client`: Para integração com a API do Google Calendar.
  - **Notificações:** Telegram Bot API via `requests`.
  - **Segurança:** `python-dotenv` para gerenciamento de segredos.
  - **Utilitários:** `Faker` para geração de dados de teste.

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto.

### 1\. Pré-requisitos

  - Python 3.10 ou superior
  - Uma Conta Google

### 2\. Instalação

1.  **Clone o repositório:**
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

### 3\. Configuração das Credenciais e Ambiente

1.  **Google Cloud:**
      - Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/).
      - Ative as APIs: **"Google Drive API"**, **"Google Sheets API"** e **"Google Calendar API"**.
      - Crie uma **Conta de Serviço**, gere uma chave **JSON** e salve o arquivo como `credentials.json` na raiz do projeto.
2.  **Google Workspace:**
      - Crie uma planilha no **Google Sheets** com os cabeçalhos especificados no `populate_sheet.py`.
      - Compartilhe a planilha com o `client_email` da sua conta de serviço (encontrado no `credentials.json`), dando permissão de **Editor**.
3.  **Crie o arquivo `.env`:**
      - Na raiz do projeto, crie um arquivo chamado `.env`.
      - Copie o conteúdo abaixo e preencha com seus dados.
    <!-- end list -->
    ```dotenv
    # .env - Arquivo de Variáveis de Ambiente

    # --- Configurações do Telegram ---
    TELEGRAM_BOT_TOKEN="SEU_TOKEN_AQUI"
    TELEGRAM_CHAT_ID="SEU_CHAT_ID_AQUI"

    # --- Configurações do Google ---
    GOOGLE_SHEET_NAME="Reservas" # O nome exato da sua planilha
    PUBLIC_HOLIDAY_CALENDAR_ID="pt-br.brazilian#holiday@group.v.calendar.google.com"
    ```

## ▶️ Como Utilizar

**1. Popular a Base de Dados (Opcional):**
Para gerar dados de teste realistas na sua planilha, execute:

```bash
python populate_sheet.py
```

**2. Iniciar o Assistente "Alfred":**
Para iniciar o monitoramento de novas reservas, execute o script principal:

```bash
python main.py
```

O bot começará a verificar a planilha a cada 60 segundos. Para parar, pressione `CTRL+C`.

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
|   |-- ai_service.py       # Módulo que gera as mensagens personalizadas (simuladas)
|   |-- notification_service.py # Módulo que envia as notificações via Telegram
```

## 🗺️ Visão de Futuro (Roadmap)

Este protótipo da Fase 1 estabelece uma base sólida e escalável. A evolução natural do projeto inclui:

  - **Fase 2 (Concierge Interativo):** Implementar um chatbot via **WhatsApp Business API** ou **Telegram** para responder a dúvidas e agendar serviços durante a estadia do hóspede.
  - **Fase 3 (Elo de Fidelidade):** Desenvolver um sistema de análise de dados pós-estadia para enviar ofertas personalizadas e incentivar a fidelização.
  - **Integração com PMS:** Conectar o sistema diretamente com a API de um sistema de gerenciamento hoteleiro para automação completa.

-----