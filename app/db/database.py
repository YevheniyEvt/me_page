from fastapi import FastAPI
from contextlib import asynccontextmanager

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .models import AboutMe, Projects, Education, Skills, Hobbies, User
from ..settings import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client  = AsyncIOMotorClient(config.database_url)
    app.database = app.mongodb_client.get_default_database()
    await init_beanie(
        database=app.database,
        document_models=[User, AboutMe, Projects, Education, Skills, Hobbies]
        )
    yield
    app.mongodb_client.close()


