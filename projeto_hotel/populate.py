# populate_sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from faker import Faker
import datetime
import random

# --- AUTENTICAÇÃO (a mesma do seu script main.py) ---
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# --- CONFIGURAÇÃO ---
# Nome da planilha que será populada
SHEET_NAME = "Reservas" 
# Inicializa o Faker para gerar dados em Português do Brasil
fake = Faker('pt_BR')

def create_fake_reservations(num_reservations):
    """
    Cria um número especificado de reservas falsas e as insere na planilha.
    """
    print(f"Gerando {num_reservations} reservas fictícias...")
    
    # Abre a planilha
    try:
        sheet = client.open(SHEET_NAME).sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"ERRO: A planilha '{SHEET_NAME}' não foi encontrada ou não foi compartilhada com o e-mail de serviço.")
        return

    new_rows = []
    today = datetime.date.today()

    for _ in range(num_reservations):
        # Gera um nome de hóspede aleatório
        guest_name = fake.name()
        
        # Gera uma data de check-in aleatória nos próximos 90 dias
        check_in_offset = random.randint(1, 90)
        check_in_date = today + datetime.timedelta(days=check_in_offset)
        
        # Gera uma duração de estadia aleatória (entre 1 e 14 noites)
        stay_duration = random.randint(1, 14)
        check_out_date = check_in_date + datetime.timedelta(days=stay_duration)
        
        # Formata a data para o padrão brasileiro e cria a linha
        # A última coluna ('Status do Envio') fica vazia de propósito
        row = [
            guest_name,
            check_in_date.strftime('%d/%m/%Y'),
            check_out_date.strftime('%d/%m/%Y'),
            '' 
        ]
        new_rows.append(row)

    # Insere todas as novas linhas na planilha de uma só vez (muito mais eficiente)
    sheet.append_rows(new_rows)
    print(f"SUCESSO: {num_reservations} novas reservas foram adicionadas à planilha '{SHEET_NAME}'.")


# --- BLOCO PRINCIPAL PARA EXECUTAR O SCRIPT ---
if __name__ == "__main__":
    # Defina aqui quantas reservas você quer criar
    NUMERO_DE_RESERVAS_PARA_CRIAR = 2
    
    create_fake_reservations(NUMERO_DE_RESERVAS_PARA_CRIAR)
