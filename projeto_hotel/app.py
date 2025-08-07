# app.py
from flask import Flask, render_template
from services import gcp_service # Reutilizamos nosso módulo de serviço do Google!
import datetime

# Inicializa a aplicação Flask
app = Flask(__name__)

@app.route('/') # Define a rota principal (ex: seudominio.com/)
def dashboard():
    """
    Esta função é executada quando alguém acessa a página.
    Ela busca os dados e renderiza o dashboard.
    """
    try:
        # Busca todos os registros da planilha usando nossa função já pronta
        all_records = gcp_service.get_all_records()
        
        # --- Lógica para calcular as métricas (KPIs) ---
        total_reservas = len(all_records)
        reservas_processadas = 0
        reservas_na_fila = []

        for record in all_records:
            if record.get('Status do Envio') == 'Enviado':
                reservas_processadas += 1
            else:
                reservas_na_fila.append(record)

        # Prepara os dados para enviar para o HTML
        kpis = {
            "total": total_reservas,
            "processadas": reservas_processadas,
            "fila": len(reservas_na_fila)
        }
        
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # 'render_template' pega o arquivo index.html e injeta as variáveis nele
        return render_template('index.html', kpis=kpis, fila=reservas_na_fila[:5], log=all_records[-5:], timestamp=timestamp)

    except Exception as e:
        # Se der erro (ex: API do Google fora do ar), mostra uma página de erro
        return f"Ocorreu um erro ao carregar o dashboard: {e}"

# Para rodar o servidor localmente
if __name__ == '__main__':
    app.run(debug=True)