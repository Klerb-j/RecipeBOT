#--------------------------------------------------------------------------#
from peewee import Model, CharField, IntegerField, ForeignKeyField, DateTimeField
from datetime import datetime
from database import db
#--------------------------------------------------------------------------#



# Базовая модель для работы с Датабазой (Supabase)
class BaseModel(Model):
    class Meta:
        database = db


# Модель Пользователя в Датабазе, содержит ID и Имя пользователя
class User(BaseModel):
    telegram_id = IntegerField(unique=True)
    name = CharField(null=True)


# Модель Истории пользователя. Содержит Пользователя, его запросы и штамп времени.
class SearchHistory(BaseModel):
    user = ForeignKeyField(User, backref='history')
    query = CharField(max_length=2000)
    timestamp = DateTimeField(default=datetime.now)


