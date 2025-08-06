# main.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import config
import openai

# --- AUTENTICAÇÃO COM GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(config.GOOGLE_SHEET_NAME).sheet1

# --- AUTENTICAÇÃO COM OPENROUTER ---
# Criamos um cliente OpenAI, mas apontamos para o servidor do OpenRouter.
try:
    openrouter_client = openai.OpenAI(
        api_key=config.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        # O OpenRouter recomenda estes cabeçalhos para identificar seu app
        default_headers={
            "HTTP-Referer": "VILAREJO_PROTOTIPO", 
            "X-Title": "Hotel Vilarejo Case",
        },
    )
except AttributeError:
    print("ERRO: A variável 'OPENROUTER_API_KEY' não foi encontrada no arquivo config.py.")
    exit()

# --- FUNÇÕES DO NOSSO PROJETO ---

def generate_welcome_message(guest_name, check_in, check_out):
    """Gera a mensagem personalizada usando a API do OpenRouter."""
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
        # A chamada é idêntica à da OpenAI, mas usando nosso cliente customizado
        response = openrouter_client.chat.completions.create(
            # O nome do modelo que você mencionou (Nous Hermes 2 Mixtral)
            model="mistralai/mixtral-8x7b-instruct",  
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Erro ao chamar a API do OpenRouter: {e}")
        return None

# A função send_telegram_message e a função main continuam exatamente iguais...

def send_telegram_message(message):
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        response = requests.get(url, params=params)
        print(f"Mensagem enviada para o Telegram. Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

def main():
    print("Iniciando o bot de boas-vindas do hotel (usando OpenRouter AI)... Pressione CTRL+C para parar.")
    while True:
        try:
            records = sheet.get_all_records()
            for i, record in enumerate(records):
                row_index = i + 2
                if 'Status do Envio' in record and not record['Status do Envio']:
                    guest = record.get('Nome do Hóspede', 'Hóspede Desconhecido')
                    checkin = record.get('Data de Check-in', 'Data Indefinida')
                    checkout = record.get('Data de Check-out', 'Data Indefinida')
                    
                    print(f"Nova reserva encontrada na linha {row_index} para: {guest}")
                    welcome_message = generate_welcome_message(guest, checkin, checkout)
                    
                    if welcome_message:
                        send_telegram_message(welcome_message)
                        sheet.update_cell(row_index, 4, "Enviado")
                        print(f"Processo concluído para {guest}.")
            
            print("Aguardando novas reservas...")
            time.sleep(60)

        except Exception as e:
            print(f"Ocorreu um erro inesperado no loop principal: {e}")
            print("Tentando novamente em 60 segundos...")
            time.sleep(60)

if __name__ == "__main__":
    main()