import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from ..settings import config
from app.db.models import User, AboutMe, Projects, Education, Skills, Hobbies
from app.main import get_app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client  = AsyncIOMotorClient(config.test_database_url)
    app.database = app.mongodb_client.get_default_database()
    await init_beanie(
        database=app.database,
        document_models=[User, AboutMe, Projects, Education, Skills, Hobbies]
        )
    yield
    await app.mongodb_client.drop_database(config.test_database_name)
    app.mongodb_client.close()

@pytest.fixture(name='async_client')
async def client_fixture():
    app = get_app(lifespan=lifespan)
    async with app.router.lifespan_context(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
            ) as async_client:
            yield async_client

@pytest.fixture(name='create_user')
async def create_user():
    user_create = User(username='Євгеній')
    await user_create.save()

        

    