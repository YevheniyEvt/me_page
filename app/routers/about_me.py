from fastapi import APIRouter, Depends
from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from ..dependencies import set_delete_links
from ..schemes import UpdateAboutMe, DeleteLink
from ..db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)

router = APIRouter(
    prefix='/about',
    tags=['About me']
)


@router.get("/", response_model=AboutMe)
async def about() ->AboutMe:
    # descriptions = 'Привіт. Я Python-розробник початківець. Маю досвід роботи з Django, FastAPI, PostgreSQL Ubuntu, Docker. Люблю приймати нові виклики, вирішувати складні задачі. Наразі весь вільний час приділяю навчанню. Вивчаю python, алгоритми, нові інструменти для покращення своїх навичок програміста.'
    # short_description = 'Наразі активно шукаю роботу, хочу долучитись до реальних проєктів та навчатись у досвідчених колег.'
    # linkedin_url = 'https://www.linkedin.com/in/yevheniy-yevtushenko-660112319/'
    # linkedin_link = Links(
    #     name='linkedin',
    #     url=linkedin_url
    # )
    # github_url = 'https://github.com/YevheniyEvt'
    # github_link = Links(
    #     name='GitHub',
    #     url=github_url
    # )
    # address = Address(
    #     city='Київ',
    #     country='Україна'
    # )
    # about = AboutMe(
    #     first_name='Євгеній',
    #     second_name='Євтушенко',
    #     descriptions=descriptions,
    #     short_description=short_description,
    #     email = 'genya421@gmail.com',
    #     address=address,
    #     links=[linkedin_link, github_link]
    # )
    yevgeniy = await AboutMe.find_one()
    # if not yevgeniy:
    #     await about.create()
    #     yevgeniy = about
    return yevgeniy


@router.put('/update')
async def update_about(about: UpdateAboutMe) ->AboutMe:
    about_db = await AboutMe.find_one()
    for attr in about:
        if attr[1] is not None:
            setattr(about_db, attr[0], attr[1])
    await about_db.save()
    return about_db

@router.put('/update-link')
async def update_about(link: Links) ->list[Links]:
    about_db = await AboutMe.find_one()
    updated = False
    for link_db in about_db.links:
        if link_db.name == link.name:
            link_db.url = link.url
            await about_db.save()
            updated = True
            break
    if not updated:
        about_db.links.append(link)
        await about_db.save()
    return about_db.links

@router.delete('/delete-link/{link_enum}')
async def delete_about(link_enum: DeleteLink) ->list[Links]:
    about_db = await AboutMe.find_one()

    return about_db.links