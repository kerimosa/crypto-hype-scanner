# Fichier: scripts/notifier.py (Version Corrigée)
import os
import telegram
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BOT = telegram.Bot(token=TELEGRAM_TOKEN) if TELEGRAM_TOKEN else None

# CHANGEMENT ICI: La fonction est maintenant "async def"
async def send_message(message_text):
    if not BOT:
        print("ERREUR: Bot Telegram non configuré.")
        return
    try:
        # CHANGEMENT ICI: On utilise "await" pour lancer la tâche
        await BOT.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message_text,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi du message: {e}")
