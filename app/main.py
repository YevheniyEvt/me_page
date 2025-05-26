from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .routers import about_me, projects
from .settings import config
from .db.models import (User, AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.mongodb_client  = AsyncIOMotorClient(config.database_url)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    await init_beanie(
        database=app.database,
        document_models=[User, AboutMe, Projects, Education, Skills, Hobbies]
        )
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(about_me.router)
app.include_router(projects.router)

@app.get("/")
async def read_root():
    return {'Hello': 'World'}
