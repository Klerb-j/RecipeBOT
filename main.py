from database import init_db
from models import User, SearchHistory
from bot import create_bot

if __name__ == "__main__":
    init_db([User, SearchHistory])
    updater = create_bot()
    print("Бот запущен...")
    updater.start_polling()
    updater.idle()