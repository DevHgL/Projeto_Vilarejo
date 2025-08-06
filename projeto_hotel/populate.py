# populate_sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from faker import Faker
import datetime
import random

# --- AUTENTICAÇÃO (continua igual) ---
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# --- CONFIGURAÇÃO ---
SHEET_NAME = "Reservas" 
fake = Faker('pt_BR')

def create_fake_reservations(num_reservations):
    """
    Cria um número especificado de reservas falsas, com dados de perfil detalhados,
    e as insere na planilha.
    """
    print(f"Gerando {num_reservations} reservas fictícias com dados de perfil avançado...")
    
    try:
        sheet = client.open(SHEET_NAME).sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"ERRO: A planilha '{SHEET_NAME}' não foi encontrada ou não foi compartilhada com o e-mail de serviço.")
        return

    # --- Listas de opções para gerar dados mais realistas ---
    motivos_viagem = ["Férias em Família", "Aniversário de Casamento", "Negócios", "Lua de Mel", "Fim de Semana"]
    tipos_quarto = ["Suíte Master com Varanda", "Chalé na Montanha", "Quarto Duplo Luxo", "Bangalô Standard"]
    
    new_rows = []
    today = datetime.date.today()

    for _ in range(num_reservations):
        # --- Geração dos Dados ---
        
        guest_name = fake.name()
        
        check_in_offset = random.randint(1, 90)
        check_in_date = today + datetime.timedelta(days=check_in_offset)
        
        stay_duration = random.randint(2, 10)
        check_out_date = check_in_date + datetime.timedelta(days=stay_duration)
        
        # NOVO: Gerando dados de perfil
        origem = f"{fake.city()}, {fake.state_abbr()}"
        motivo_viagem = random.choice(motivos_viagem)
        tipo_quarto = random.choice(tipos_quarto)
        
        # NOVO: Gerando histórico (80% de chance de ser primeira visita)
        historico = random.choices(['Primeira Visita', 'Hóspede Recorrente'], weights=[80, 20], k=1)[0]
        
        # NOVO: Lógica para adultos e crianças
        adultos = random.randint(1, 2)
        criancas = 0 # Por padrão, zero crianças
        
        if "Família" in motivo_viagem:
            criancas = random.randint(2, 4)
        elif "Lua de Mel" in motivo_viagem or "Aniversário" in motivo_viagem:
            adultos = 2 # Garante 2 adultos para casais
        elif "Negócios" in motivo_viagem:
            adultos = 1 # Garante 1 adulto para negócios

        # --- Montagem da Linha ---
        # A ORDEM AQUI DEVE SER EXATAMENTE A MESMA DAS COLUNAS NA SUA PLANILHA
        row = [
            guest_name,
            check_in_date.strftime('%d/%m/%Y'),
            check_out_date.strftime('%d/%m/%Y'),
            origem,
            motivo_viagem,
            tipo_quarto,
            historico,
            adultos,
            criancas,
            ''  # Coluna 'Status do Envio' fica vazia
        ]
        new_rows.append(row)

    # Insere todas as novas linhas na planilha de uma só vez
    sheet.append_rows(new_rows)
    print(f"SUCESSO: {num_reservations} novas reservas detalhadas foram adicionadas à planilha '{SHEET_NAME}'.")


# --- BLOCO PRINCIPAL PARA EXECUTAR O SCRIPT ---
if __name__ == "__main__":
    NUMERO_DE_RESERVAS_PARA_CRIAR = 3  # Ajuste este número conforme necessário'    
    create_fake_reservations(NUMERO_DE_RESERVAS_PARA_CRIAR)