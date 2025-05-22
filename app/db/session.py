""" 
Async SQLAlchemy session and engine setup.

This module sets up:
- The async engine connected to PostgreSQL using asyncpg 
- A session factory to be used with FastAPI 
- The declarative Base class for ORM model declarations

"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.db.config import settings

# ---------------------------------------------------------
# Create the SQLAlchemy Async Engine
# ---------------------------------------------------------
engine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True
)

# ---------------------------------------------------------
# Create an async session factory 
# ---------------------------------------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# ---------------------------------------------------------
# Base class for all ORM models to inherit from
# ---------------------------------------------------------
Base = declarative_base()