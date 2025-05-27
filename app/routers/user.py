from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, WriteRules
from beanie.operators import Pull

from ..dependencies import check_first_name, get_user, get_updated_data, update_data
from ..schemes import ReprProject, UpdateProject, CreateProject, DeleteProject, ReprEducation, CreateEducation, CreateUser, ReprUser, GetUser
from ..db.models import (User, AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags, Course, Lection, Book)


router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/')
async def user_information(user: Annotated[GetUser, Depends(get_user)]):
    return user

@router.post('/create')
async def create_user(user: CreateUser):
    user_create = User(**user.model_dump())
    await user_create.save()
