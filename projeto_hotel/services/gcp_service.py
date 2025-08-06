# services/gcp_service.py
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import config

# --- CONFIGURAÇÃO E AUTENTICAÇÃO ---
SHEETS_SCOPE = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
CALENDAR_SCOPE = ['https://www.googleapis.com/auth/calendar.readonly']

sheets_creds = gspread.service_account(filename="credentials.json", scopes=SHEETS_SCOPE)
sheet = sheets_creds.open(config.GOOGLE_SHEET_NAME).sheet1

calendar_creds = Credentials.from_service_account_file("credentials.json", scopes=CALENDAR_SCOPE)
calendar_service = build('calendar', 'v3', credentials=calendar_creds)

# --- FUNÇÕES ---
def get_all_records():
    """Busca todos os registros da planilha."""
    return sheet.get_all_records()

def update_sheet_status(row_index, status):
    """Atualiza a célula de status na planilha."""
    # A coluna de Status do Envio é a 10ª (J)
    sheet.update_cell(row_index, 10, status)

def check_guest_history(guest_name, all_records):
    """Verifica se o nome do hóspede já aparece em registros processados."""
    count = 0
    for record in all_records:
        if record.get('Nome do Hóspede') == guest_name and record.get('Status do Envio') == 'Enviado':
            count += 1
    return "Hóspede Recorrente" if count > 0 else "Primeira Visita"

def get_public_holidays(start_date_str, end_date_str):
    """Busca feriados nacionais no calendário público."""
    try:
        start_datetime = datetime.datetime.strptime(start_date_str, '%d/%m/%Y')
        end_datetime = datetime.datetime.strptime(end_date_str, '%d/%m/%Y')
        start_iso, end_iso = start_datetime.isoformat() + 'Z', end_datetime.isoformat() + 'Z'

        events_result = calendar_service.events().list(
            calendarId=config.PUBLIC_HOLIDAY_CALENDAR_ID,
            timeMin=start_iso, timeMax=end_iso, singleEvents=True, orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        if not events: return ""
        
        holiday_names = ", ".join([event['summary'] for event in events])
        return f"Que ótima escolha de datas! Sua visita coincide com o feriado de **{holiday_names}**, a cidade de Rio das Ostras estará ainda mais festiva."
    except Exception as e:
        print(f"Erro ao buscar feriados públicos: {e}")
        return ""