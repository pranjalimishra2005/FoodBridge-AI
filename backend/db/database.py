import ssl
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from sqlalchemy.orm import DeclarativeBase

from backend.core.config import settings


# -----------------------------
# DATABASE BASE MODEL
# -----------------------------
class Base(DeclarativeBase):
    pass


# -----------------------------
# DATABASE ENGINE
# -----------------------------
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"ssl": "require"},
    pool_pre_ping=True,  # <--- CRITICAL FIX: Tests connection before every query
    pool_size=10,        # Keeps a pool of connections ready
    max_overflow=20      # Allows more connections if needed
)

# -----------------------------
# SESSION FACTORY
# -----------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# -----------------------------
# CREATE TABLES
# -----------------------------
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session