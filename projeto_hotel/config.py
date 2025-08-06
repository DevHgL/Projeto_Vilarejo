
# config.py
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- Chaves de API ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- Configurações do Telegram ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Configurações do Google Workspace ---
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME")
PUBLIC_HOLIDAY_CALENDAR_ID = os.getenv("PUBLIC_HOLIDAY_CALENDAR_ID")