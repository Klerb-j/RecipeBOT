#--------------------------------------------------------------------------#
from peewee import PostgresqlDatabase
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
#--------------------------------------------------------------------------#

# Подключение к Датабазе (Supabase)
db = PostgresqlDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)


def init_db(models):
    db.connect(reuse_if_open=True)
    db.create_tables(models)