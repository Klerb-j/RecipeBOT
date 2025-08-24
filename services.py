#--------------------------------------------------------------------------#
import re
import requests
from datetime import datetime
from openai import OpenAI
from config import OPENAI_API_KEY, UNSPLASH_AK
from models import User, SearchHistory
#--------------------------------------------------------------------------#


def save_user_search(telegram_id, username, query):
    # Обращается к Датабазе на основе PosgreSQL (Supabase) для создания Пользователя и его Телеграм ID.
    user, _ = User.get_or_create(
        telegram_id=telegram_id,
        defaults={'name': username}
    )
    # Создает Историю для пользователя вместе с штампом о текущем времени.
    SearchHistory.create(user=user, query=query, timestamp=datetime.now())

def get_user_history(telegram_id):
    # Достает Историю пользователя, если в датабазе есть такой Пользователь
    try:
        user = User.get(User.telegram_id == telegram_id)
        return SearchHistory.select().where(SearchHistory.user == user)
    except User.DoesNotExist:
        return []

def show_history(update, context):
    """
    Показывает Историю.
    Если Пользователь ничего не указал после команды /history, будет использовать значения по умолчанию: порядок - новые, лимит - 5.

    :param update: Телеграм Апдейтер, нужен для взаимодействия с Пользователем
    :param context: Телеграм Контекст, нужен для особых комманд, которые могут принят любые аргументы после самой использования команды.
    :return: Возвращает только если в случае ошибки.
    """

    # Находит ID пользователя
    user_id = update.message.from_user.id

    # Значения по умолчанию
    sort_order = "новые"
    limit = 5

    # Проверяет аргументы после комманды /history
    if context.args:
        if context.args[0].lower() in ["старые", "новые"]:
            sort_order = context.args[0].lower()
        elif context.args[0].isdigit():
            limit = int(context.args[0])
        else:
            update.message.reply_text('<порядок> должен быть существующим (новые/старые)! Проверьте на опечатки!')
            return
        if len(context.args) == 2:
            if context.args[1].isdigit():
                limit = int(context.args[1])
            else:
                update.message.reply_text('<количество> должно быть числом!')
                return
        elif len(context.args) > 2:
            update.message.reply_text('Слишком много Аргументов! Должно быть /search <новые/старые> <количество>.')
            return

    # Ищет историю, чистит её для более приятного вида.
    try:
        # Находит пользователя
        user = User.get(User.telegram_id == user_id)

        # Проверяет на порядок
        order_clause = SearchHistory.timestamp.asc() if sort_order == "старые" else SearchHistory.timestamp.desc()

        # Берёт Историю из Датабазы
        history = (
            SearchHistory
            .select()
            .where(SearchHistory.user == user)
            .order_by(order_clause)
            .limit(limit)
        )

        if not history:
            update.message.reply_text("📭 У вас пока нет истории поиска рецептов.")
            return

        cleaned_history = []
        counter = 1

        # Чистит от цифр для отсчёта, и переписывает их
        for item in history:
            cleaned_query = re.sub(r'^\s*\d+\.\s*', '', item.query, flags=re.MULTILINE)
            formatted_entry = f"{counter}. {cleaned_query} ({item.timestamp.strftime('%d.%m.%Y %H:%M')})"
            cleaned_history.append(formatted_entry)
            counter += 1

        # Соединить в одно сообщение
        history_text = "\n".join(cleaned_history)

        update.message.reply_text(
            f"📝 Ваша история поиска ({sort_order}, {limit} шт.):\n\n{history_text}"
        )

    except User.DoesNotExist:
        update.message.reply_text("📭 У вас пока нет истории поиска рецептов.")

def ai_search(user_input: str):
    # Бёрет ключ из .env файла
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_input,
        store=True,
    )
    # Возвращает ответ от ИИ
    return response.output_text

def image_search(query: str, update):
    # Unsplash Access Key (AK) находится в .env файле.

    per_page = 1
    url = "https://api.unsplash.com/search/photos"
    params = {"query": query,"per_page": per_page, "client_id" : UNSPLASH_AK}

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
    except Exception as exception:
        update.message.reply_text(f'Не удалось загрузить Изображение для блюда! Ошибка: {exception} ')
        return

    data = res.json()
    return data["results"][0]["urls"]["regular"]