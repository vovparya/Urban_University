from .db import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
