# services/ai_service.py
import time

def generate_welcome_message(guest_name, check_in, check_out, motivo_viagem, criancas, historico, holiday_info):
    """Gera a mensagem final no estilo 'Alfred' usando todos os dados coletados (MODO SIMULAÇÃO)."""
    print("!!! MODO DEMONSTRAÇÃO FINAL: Gerando mensagem com dados de feriados públicos !!!")
    
    saudacao = f"Olá {guest_name}, que felicidade ter você de volta!" if historico == "Hóspede Recorrente" else f"Olá {guest_name}! 🌞"
    confirmacao = f"\n\nSeja muito bem-vindo(a) ao Vilarejo do Sol! Confirmamos sua incrível estadia em Rio das Ostras de {check_in} a {check_out}."
    
    corpo = "\n\nComo nosso hotel é all-inclusive, sua única preocupação será relaxar! Traga roupas leves para o dia e um agasalho para as noites."
    if int(criancas) > 0:
        corpo += " O nosso parque aquático e a equipe de recreação estão prontos para fazer a alegria da criançada! 🌊"
    if "Lua de Mel" in motivo_viagem or "Aniversário" in motivo_viagem:
        corpo += " Soubemos que a ocasião é especial e nossos bares já estão preparando drinks comemorativos para vocês! 🍹"

    if holiday_info:
        corpo += f"\n\n{holiday_info}"

    encerramento = "\n\nEstamos finalizando todos os preparativos para que sua experiência seja inesquecível! 🎉"
    assinatura = "\n\nAtenciosamente,\nAlfred."
    
    mensagem_final = saudacao + confirmacao + corpo + encerramento + assinatura
    time.sleep(2)
    return mensagem_final