from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@localhost:"
    f"{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)