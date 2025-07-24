import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Set default SQLite database URL
    DATABASE_URL = 'sqlite:///trading_bot.db'
    print("⚠️ DATABASE_URL not set, using default SQLite database: trading_bot.db")

logging.basicConfig(level=logging.INFO)
logging.info(f"[DB] Connecting to: {DATABASE_URL}")

connect_args = {}
if DATABASE_URL.startswith("postgresql+asyncpg"):
    connect_args = {"ssl": True}
elif DATABASE_URL.startswith("postgresql+psycopg2"):
    connect_args = {"sslmode": "require"}

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    connect_args=connect_args
)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session