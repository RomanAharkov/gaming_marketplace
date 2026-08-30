import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase;

DATABASE_URL = f"postgresql+psycopg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = DeclarativeBase()

def get_db():
    with SessionLocal() as session:
        yield session
