from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from beanie.operators import Pull

from ..dependencies import set_delete_links, create_about
from ..schemes import UpdateAboutMe, DeleteLink, CreateAboutMe
from ..db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)

router = APIRouter(
    prefix='/about',
    tags=['About me']
)


@router.get("/")
async def about(name: str)->AboutMe:
    if name == 'Євгеній':
        about = await AboutMe.find_one(AboutMe.first_name == 'Євгеній')
        if not about:
            about = create_about()
            await about.create()
    else:
        about = await AboutMe.find_one(AboutMe.first_name == name)
        if not about:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"About with name {name} does not exist"
        )
    return about


@router.post('/create')
async def create_about(about: CreateAboutMe)->AboutMe:
    about_db = AboutMe(**about.model_dump())
    await about_db.create()
    return about_db


@router.delete('/delete')
async def delete_about(first_name: str):
    await AboutMe.find(AboutMe.first_name == first_name).delete()
    return {'msg': f'Name {first_name} was deleted'}


@router.put('/update')
async def update_about(about: UpdateAboutMe) ->AboutMe:
    about_db = await AboutMe.find_one()
    for attr in about:
        if attr[1] is not None:
            setattr(about_db, attr[0], attr[1])
    await about_db.save_changes()
    return about_db


@router.post('/update-link')
async def update_or_add_link(link: Links) ->list[Links]:
    about_db = await AboutMe.find_one()
    link_get = (link_db for link_db in about_db.links if link_db.name == link.name)
    try:
        link_db = next(link_get)
        link_db.url = link.url
        await about_db.save_changes()
    except StopIteration:
        about_db.links.append(link)
        await about_db.save()
    return about_db.links


@router.delete('/delete-link/{name}')
async def delete_link(name: str) ->list[Links]:
    about_db = await AboutMe.find_one()
    updated_links = [link for link in about_db.links if link.name != name]
    if len(updated_links) == len(about_db.links):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"link with name {name} does not exist"
        )
    else:
        about_db.links = updated_links
        await about_db.save_changes()
    return about_db.links