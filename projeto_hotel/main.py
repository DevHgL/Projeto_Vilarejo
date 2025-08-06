# main.py - VERSÃO FINAL E SIMPLIFICADA (APENAS CALENDÁRIO PÚBLICO)
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import datetime
import config

# Imports para a API do Google Calendar
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# --- CONFIGURAÇÃO E AUTENTICAÇÃO ---
SHEETS_SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
CALENDAR_SCOPE = ['https://www.googleapis.com/auth/calendar.readonly']

sheets_creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SHEETS_SCOPE)
sheets_client = gspread.authorize(sheets_creds)
sheet = sheets_client.open(config.GOOGLE_SHEET_NAME).sheet1

calendar_creds = Credentials.from_service_account_file("credentials.json", scopes=CALENDAR_SCOPE)
calendar_service = build('calendar', 'v3', credentials=calendar_creds)


# --- FUNÇÕES DE BUSCA ---

def check_guest_history(guest_name, all_records):
    """Verifica se o nome do hóspede já aparece em registros processados anteriormente."""
    count = 0
    for record in all_records:
        if record.get('Nome do Hóspede') == guest_name and record.get('Status do Envio') == 'Enviado':
            count += 1
    return "Hóspede Recorrente" if count > 0 else "Primeira Visita"

def get_public_holidays(start_date_str, end_date_str):
    """Busca feriados nacionais no calendário público do Google para o período da estadia."""
    try:
        start_datetime = datetime.datetime.strptime(start_date_str, '%d/%m/%Y')
        end_datetime = datetime.datetime.strptime(end_date_str, '%d/%m/%Y')
        
        start_iso = start_datetime.isoformat() + 'Z'
        end_iso = end_datetime.isoformat() + 'Z'

        events_result = calendar_service.events().list(
            calendarId=config.PUBLIC_HOLIDAY_CALENDAR_ID,
            timeMin=start_iso,
            timeMax=end_iso,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        if not events:
            return "" # Retorna vazio se não houver feriados
        
        holiday_names = ", ".join([event['summary'] for event in events])
        return f"Que ótima escolha de datas! Sua visita coincide com o feriado de **{holiday_names}**, a cidade de Rio das Ostras estará ainda mais festiva."

    except Exception as e:
        print(f"Erro ao buscar feriados públicos: {e}")
        return "" # Retorna vazio em caso de erro

# --- FUNÇÕES DE GERAÇÃO DE MENSAGEM E ENVIO ---

def generate_welcome_message(guest_name, check_in, check_out, motivo_viagem, criancas, historico, holiday_info):
    """Gera a mensagem final no estilo 'Alfred' usando todos os dados coletados."""
    print("!!! MODO DEMONSTRAÇÃO FINAL: Gerando mensagem com dados de feriados públicos !!!")
    
    saudacao = f"Olá {guest_name}, que felicidade ter você de volta!" if historico == "Hóspede Recorrente" else f"Olá {guest_name}! 🌞"
    confirmacao = f"\n\nSeja muito bem-vindo(a) ao Vilarejo do Sol! Confirmamos sua incrível estadia em Rio das Ostras de {check_in} a {check_out}."
    
    corpo = "\n\nComo nosso hotel é all-inclusive, sua única preocupação será relaxar! Traga roupas leves para o dia e um agasalho para as noites, que podem ser mais frescas."
    if int(criancas) > 0:
        corpo += " O nosso parque aquático e a equipe de recreação estão prontos para fazer a alegria da criançada! 🌊"

    if "Lua de Mel" in motivo_viagem or "Aniversário" in motivo_viagem:
        corpo += " Soubemos que a ocasião é especial e nossos bares já estão preparando drinks comemorativos para vocês! 🍹"

    # Adiciona a informação do feriado, se houver
    if holiday_info:
        corpo += f"\n\n{holiday_info}"

    encerramento = "\n\nEstamos finalizando todos os preparativos para que sua experiência seja inesquecível! 🎉"
    assinatura = "\n\nAtenciosamente,\nAlfred."
    
    mensagem_final = saudacao + confirmacao + corpo + encerramento + assinatura
    
    time.sleep(2)
    return mensagem_final

def send_telegram_message(message):
    # Sua função de enviar para o Telegram continua aqui...
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        response = requests.get(url, params=params)
        print(f"Mensagem enviada para o Telegram. Status: {response.status_code}")
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")

# --- LÓGICA PRINCIPAL ---
def main():
    print("Iniciando o bot de boas-vindas do hotel (VERSÃO FINAL SIMPLIFICADA)... Pressione CTRL+C para parar.")
    while True:
        try:
            all_records = sheet.get_all_records()
            for i, record in enumerate(all_records):
                row_index = i + 2
                if 'Status do Envio' in record and not record['Status do Envio']:
                    guest = record.get('Nome do Hóspede')
                    checkin = record.get('Data de Check-in')
                    checkout = record.get('Data de Check-out')
                    motivo = record.get('Motivo da Viagem')
                    criancas = record.get('Crianças', 0)
                    
                    print(f"Nova reserva encontrada para: {guest}")
                    
                    historico = check_guest_history(guest, all_records)
                    print(f"-> Histórico: {historico}")
                    
                    feriados = get_public_holidays(checkin, checkout)
                    if feriados:
                        print(f"-> Feriados no Período Encontrados!")
                    
                    welcome_message = generate_welcome_message(guest, checkin, checkout, motivo, criancas, historico, feriados)
                    
                    if welcome_message:
                        send_telegram_message(welcome_message)
                        sheet.update_cell(row_index, 10, "Enviado")
                        print(f"Processo concluído para {guest}.\n")
            
            print("Aguardando novas reservas...")
            time.sleep(60)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            print("Tentando novamente em 60 segundos...")
            time.sleep(60)

if __name__ == "__main__":
    main()