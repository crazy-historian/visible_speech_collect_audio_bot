# config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('TG_BOT_TOKEN')
if not API_TOKEN:
    raise ValueError("Переменная окружения TG_BOT_TOKEN не задана")

# Константы
MIN_AGE = 1
MAX_AGE = 120