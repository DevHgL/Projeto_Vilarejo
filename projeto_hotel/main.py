# main.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import config  # Importa nossas chaves do arquivo config.py
import google.generativeai as genai # Importa a biblioteca do Google Gemini

# --- CONFIGURAÇÃO DAS AUTENTICAÇÕES ---

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open(config.GOOGLE_SHEET_NAME).sheet1

# Autenticação com Google Gemini
# Pega a chave do nosso arquivo de configuração e configura a biblioteca
try:
    genai.configure(api_key=config.GOOGLE_API_KEY)
except AttributeError:
    print("ERRO: A variável 'GOOGLE_API_KEY' não foi encontrada no arquivo config.py.")
    print("Por favor, adicione sua chave da API do Google Gemini no arquivo de configuração.")
    exit()


# --- FUNÇÕES DO NOSSO PROJETO ---

def generate_welcome_message(guest_name, check_in, check_out):
    """
    Gera a mensagem personalizada usando a API do Google Gemini.
    """
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
        # Inicializa o modelo do Gemini
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Gera o conteúdo
        response = model.generate_content(prompt)
        
        # Retorna o texto da resposta
        return response.text
        
    except Exception as e:
        print(f"Erro ao chamar a API do Google Gemini: {e}")
        return None

def send_telegram_message(message):
    """
    Envia a mensagem de texto para o chat especificado no Telegram.
    """
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
    """
    Função principal que roda o loop para verificar e processar novas reservas.
    """
    print("Iniciando o bot de boas-vindas do hotel... Pressione CTRL+C para parar.")
    while True:
        try:
            # Pega todos os registros da planilha
            records = sheet.get_all_records()
            
            # O gspread lê a partir da linha 2, então o índice da linha na planilha é o índice da lista + 2
            for i, record in enumerate(records):
                row_index = i + 2
                
                # Verifica se a coluna 'Status do Envio' existe e está vazia
                if 'Status do Envio' in record and not record['Status do Envio']:
                    guest = record.get('Nome do Hóspede', 'Hóspede Desconhecido')
                    checkin = record.get('Data de Check-in', 'Data Indefinida')
                    checkout = record.get('Data de Check-out', 'Data Indefinida')
                    
                    print(f"Nova reserva encontrada na linha {row_index} para: {guest}")
                    
                    # 1. Gerar mensagem com a IA
                    welcome_message = generate_welcome_message(guest, checkin, checkout)
                    
                    if welcome_message:
                        # 2. Enviar mensagem pelo Telegram
                        send_telegram_message(welcome_message)
                        
                        # 3. Atualizar o status na planilha para 'Enviado'
                        # Assumindo que a coluna 'Status do Envio' é a 4ª (D)
                        sheet.update_cell(row_index, 4, "Enviado") 
                        print(f"Processo concluído para {guest}.")
            
            # Espera 60 segundos antes de verificar a planilha novamente
            print("Aguardando novas reservas...")
            time.sleep(60)

        except gspread.exceptions.APIError as e:
            print(f"ERRO DE API DO GOOGLE: {e}")
            print("Pode ser um problema de cota ou permissão. Tentando novamente em 60 segundos...")
            time.sleep(60)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            print("Tentando novamente em 60 segundos...")
            time.sleep(60)


if __name__ == "__main__":
    main()