from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase;
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session
