import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import requests
import time
import config  # Importa nossas chaves do arquivo config.py

# --- CONFIGURAÇÃO DAS AUTENTICAÇÕES ---

# Autenticação com Google Sheets usando o arquivo credentials.json
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(config.GOOGLE_SHEET_NAME).sheet1

# Autenticação com OpenAI
openai.api_key = config.OPENAI_API_KEY


# --- FUNÇÕES DO NOSSO PROJETO ---

def generate_welcome_message(guest_name, check_in, check_out):
    """Gera a mensagem personalizada usando a IA da OpenAI."""
    prompt = f"""
    Você é um assistente virtual de um hotel chamado 'Vilarejo do Sol'. Sua comunicação é acolhedora e amigável.
    Crie uma mensagem de pré-hospedagem para o hóspede abaixo para ser enviada no Telegram.

    Dados do Hóspede:
    - Nome: {guest_name}
    - Período da Estadia: de {check_in} a {check_out}

    Instruções para a mensagem:
    1. Comece com uma saudação calorosa e personalizada usando o nome do hóspede.
    2. Mencione o período da estadia.
    3. Dê dicas práticas sobre o que trazer na mala (ex: roupas leves, protetor solar).
    4. Mencione uma atividade fictícia do hotel (ex: luau na sexta-feira).
    5. A mensagem deve ser concisa, ideal para o Telegram, e em português do Brasil.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro ao chamar a API da OpenAI: {e}")
        return None

def send_telegram_message(message):
    """Envia a mensagem de texto para o chat especificado no Telegram."""
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        response = requests.get(url, params=params)
        print(f"Mensagem enviada para o Telegram. Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

# --- LÓGICA PRINCIPAL (LOOP INFINITO) ---

def main():
    print("Iniciando o bot de boas-vindas do hotel... Pressione CTRL+C para parar.")
    while True:
        # Pega todos os registros da planilha
        records = sheet.get_all_records()
        
        # O gspread lê a partir da linha 2, então o índice da linha na planilha é o índice da lista + 2
        for i, record in enumerate(records):
            row_index = i + 2
            # Verifica se a coluna 'Status do Envio' está vazia
            if 'Status do Envio' in record and not record['Status do Envio']:
                guest = record['Nome do Hóspede']
                checkin = record['Data de Check-in']
                checkout = record['Data de Check-out']
                
                print(f"Nova reserva encontrada na linha {row_index} para: {guest}")
                
                # 1. Gerar mensagem com a IA
                welcome_message = generate_welcome_message(guest, checkin, checkout)
                
                if welcome_message:
                    # 2. Enviar mensagem pelo Telegram
                    send_telegram_message(welcome_message)
                    
                    # 3. Atualizar o status na planilha para 'Enviado'
                    sheet.update_cell(row_index, 5, "Enviado") # Assumindo que a coluna 'Status' é a 5ª (E)
                    print(f"Processo concluído para {guest}.")
        
        # Espera 60 segundos antes de verificar a planilha novamente
        print("Aguardando novas reservas...")
        time.sleep(60)

if __name__ == "__main__":
    main()