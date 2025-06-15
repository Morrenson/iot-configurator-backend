import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Собираем параметры из переменных окружения (или берём значения по-умолчанию)
DB_HOSTS = os.getenv("DB_HOSTS")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SSLMODE = os.getenv("DB_SSLMODE")
DB_TARGET_SESSION_ATTRS = os.getenv("DB_TARGET_SESSION_ATTRS")

# Опционально, если нужен sslrootcert, укажите путь к скачанному Yandex Cloud CA:
# DB_SSLROOTCERT = os.getenv("DB_SSLROOTCERT", "/path/to/yandex-ca.pem")

# Формируем URL для SQLAlchemy (подаём host как список через запятую)
# Если задана переменная окружения DATABASE_URL — она имеет приоритет
default_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOSTS}:{DB_PORT}/{DB_NAME}"
    f"?sslmode={DB_SSLMODE}"
    f"&target_session_attrs={DB_TARGET_SESSION_ATTRS}"
    # f"&sslrootcert={DB_SSLROOTCERT}"  # раскомментируйте, если используете sslrootcert
)
DATABASE_URL = os.getenv("DATABASE_URL", default_url)

# Создаём движок и сессию
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Получает сессию SQLAlchemy для работы с БД.
    Используется как dependency в FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()