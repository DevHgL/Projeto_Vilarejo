# main.py
import time
# Importando nossas funções dos módulos de serviço
from services import gcp_service, ai_service, notification_service

def main():
    """Função principal que orquestra o processo."""
    print("Iniciando o bot de boas-vindas do hotel (Versão Modular)... Pressione CTRL+C para parar.")
    while True:
        try:
            all_records = gcp_service.get_all_records()
            for i, record in enumerate(all_records):
                row_index = i + 2
                if record.get('Status do Envio') == '':
                    guest = record.get('Nome do Hóspede')
                    checkin = record.get('Data de Check-in')
                    checkout = record.get('Data de Check-out')
                    motivo = record.get('Motivo da Viagem')
                    criancas = record.get('Crianças', 0)

                    print(f"Nova reserva encontrada para: {guest}")
                    
                    historico = gcp_service.check_guest_history(guest, all_records)
                    print(f"-> Histórico: {historico}")
                    
                    feriados = gcp_service.get_public_holidays(checkin, checkout)
                    if feriados: print(f"-> Feriados no Período Encontrados!")
                    
                    welcome_message = ai_service.generate_welcome_message(
                        guest, checkin, checkout, motivo, criancas, historico, feriados
                    )
                    
                    if welcome_message:
                        notification_service.send_telegram_message(welcome_message)
                        gcp_service.update_sheet_status(row_index, "Enviado")
                        print(f"Processo concluído para {guest}.\n")
            
            print("Aguardando novas reservas...")
            time.sleep(60)

        except Exception as e:
            print(f"Ocorreu um erro inesperado no loop principal: {e}")
            print("Tentando novamente em 60 segundos...")
            time.sleep(60)

if __name__ == "__main__":
    main()