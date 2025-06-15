# app/database.py
import os
import psycopg2
from psycopg2 import pool

# Читаем переменные окружения
DB_HOSTS = os.getenv("DB_HOSTS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SSLMODE = os.getenv("DB_SSLMODE", "disable")

# Формируем DSN для psycopg2
DSN = (
    f"host={DB_HOSTS} port={DB_PORT} dbname={DB_NAME} "
    f"user={DB_USER} password={DB_PASSWORD} "
    f"sslmode={DB_SSLMODE} target_session_attrs=read-write"
)

# Создаём пул подключений
pg_pool = pool.SimpleConnectionPool(1, 10, dsn=DSN)

def get_db():
    """
    FastAPI dependency: даёт подключение из пула и закрывает после использования.
    """
    conn = pg_pool.getconn()
    try:
        yield conn
    finally:
        pg_pool.putconn(conn)
