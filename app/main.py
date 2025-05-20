from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .routers import about_me
from .settings import config
from .db.models import (AboutMe, Projects, Education, Skills, Hobbies,
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
        document_models=[AboutMe, Projects, Education, Skills, Hobbies]
        )
    yield
    app.mongodb_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(about_me.router)


@app.get("/")
async def read_root() ->AboutMe:
    descriptions = 'Привіт. Я Python-розробник початківець. Маю досвід роботи з Django, FastAPI, PostgreSQL Ubuntu, Docker. Люблю приймати нові виклики, вирішувати складні задачі. Наразі весь вільний час приділяю навчанню. Вивчаю python, алгоритми, нові інструменти для покращення своїх навичок програміста.'
    short_description = 'Наразі активно шукаю роботу, хочу долучитись до реальних проєктів та навчатись у досвідчених колег.'
    linkedin_url = 'https://www.linkedin.com/in/yevheniy-yevtushenko-660112319/'
    linkedin_link = Links(
        name='linkedin',
        url=linkedin_url
    )
    github_url = 'https://github.com/YevheniyEvt'
    github_link = Links(
        name='GitHub',
        url=github_url
    )
    address = Address(
        city='Київ',
        country='Україна'
    )
    about = AboutMe(
        first_name='Євгеній',
        second_name='Євтушенко',
        descriptions=descriptions,
        short_description=short_description,
        email = 'genya421@gmail.com',
        address=address,
        links=[linkedin_link, github_link]
    )
    yevgeniy = await AboutMe.find_one(AboutMe.first_name  == "Євгеній")
    if not yevgeniy:
        await about.create()
        yevgeniy = about
    return yevgeniy
