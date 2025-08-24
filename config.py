#--------------------------------------------------------------------------#
import os
from dotenv import load_dotenv
#--------------------------------------------------------------------------#


# Скажу честно, идея с .env файлом была не моя, а ChatGPT.

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
UNSPLASH_AK = os.getenv("UNSPLASH_AK")