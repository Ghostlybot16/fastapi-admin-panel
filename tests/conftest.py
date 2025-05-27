import os
os.environ["TESTING"] = "1"

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import engine, Base, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.deps import get_db


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def async_client():
    """
    Async test client for FastAPI app, with shared DB session override.
    """
    async with AsyncSessionLocal() as session:
        async def override_get_db():
            yield session
            
        app.dependency_overrides[get_db] = override_get_db
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client
        