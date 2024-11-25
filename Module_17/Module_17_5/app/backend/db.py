from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_engine('sqlite:///taskmanager.db', echo=True)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
