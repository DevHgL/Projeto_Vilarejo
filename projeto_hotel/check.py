# check_models.py
import google.generativeai as genai
import config

print("Conectando à API do Google para verificar os modelos disponíveis...")

try:
    # Configura a autenticação com a chave do seu arquivo config.py
    genai.configure(api_key=config.GOOGLE_API_KEY)
except AttributeError:
    print("\nERRO: A variável 'GOOGLE_API_KEY' não foi encontrada no seu arquivo config.py.")
    print("Por favor, verifique se a chave foi adicionada corretamente.")
    exit() # Para o script se a chave não for encontrada

print("\n--- Modelos Disponíveis que Suportam Geração de Texto ---")

try:
    # Pede à API para listar os modelos e verifica quais podem gerar conteúdo
    count = 0
    for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        count += 1
    
    if count == 0:
        print("\nNenhum modelo compatível foi encontrado. Verifique as permissões da sua API Key no Google AI Studio.")
    else:
        print("\n---------------------------------------------------------")
        print("\nINSTRUÇÃO: Copie um dos nomes da lista acima (o mais recente, como 'gemini-1.5-pro-latest' ou similar) e cole no seu arquivo main.py, na linha 'model = genai.GenerativeModel(...)'.")

except Exception as e:
    print(f"\nOcorreu um erro ao tentar listar os modelos: {e}")
    print("Verifique se sua chave de API é válida e se você tem acesso à API do Google AI.")