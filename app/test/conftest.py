import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from ..settings import config
from app.db.models import User, AboutMe, Projects, Education, Skills, Hobbies, Tags, Links
from app.main import get_app
from app.dependencies import create_about_evgeniy

USERNAME = 'Євгеній'

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
    user_create = User(username=USERNAME)
    await user_create.create()
    return user_create

@pytest.fixture(name='create_about')
async def create_about(create_user: User):
    about = await create_about_evgeniy()
    await about.save()
    create_user.about = about
    await create_user.save_changes()
    
@pytest.fixture(name='create_hobbies')
async def create_hobbies(create_user: User):
    hobbies = Hobbies(descriptions='I like to write a code')
    await hobbies.save()
    create_user.hobbies = hobbies
    await create_user.save_changes()
    return hobbies


@pytest.fixture(name='create_projects')
async def create_projects(create_user: User):
    tag = Tags(
        name='created tag name',
        description='created tag descriptions',
    )
    link = Links(
        name='created link name',
        url='https://created.com/',
    )
    project_created = Projects(
        name='created project name',
        descriptions='created project descriptions',
        instruments='created project instruments',
        tags=[tag],
        links=[link]
    )
    await project_created.create()
    create_user.projects.append(project_created)
    await create_user.save_changes()
    return project_created
