from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Создаём движок для работы с базой данных SQLite
engine = create_engine('sqlite:///taskmanager.db', echo=True)

# Создаём фабрику сессий
SessionLocal = sessionmaker(bind=engine)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass
