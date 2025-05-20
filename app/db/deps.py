from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency which provides a database session. 
    Produces an AsyncSession and ensures that its connection is closed after the request. 
    Used by FastAPI
    """
    
    # `AsyncSessionLocal()` created a new async DB session 
    # `async with` ensures proper closing of the session
    async with AsyncSessionLocal() as session:
        yield session