from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, WriteRules
from beanie.operators import Pull

from ..dependencies import check_first_name, get_user, get_updated_data, update_data
from ..schemes import ReprProject, UpdateProject, CreateProject, DeleteProject, ReprEducation, CreateEducation
from ..db.models import (User, AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags, Course, Lection, Book)


router = APIRouter(
    prefix='/education',
    tags=['Education']
)

@router.get('/')
async def education_information(user: Annotated[User, Depends(get_user)])->ReprEducation:
    return user.education

@router.post('/create')
async def create_education_information(user: Annotated[User, Depends(get_user)],
                                       education: CreateEducation):
    education_create = await Education(**education.model_dump())
    await education_create.save()
    user.education = education_create
    await user.save_changes()

@router.post('/update-course/{data_name}')
async def update_or_add_courses(user: Annotated[User, Depends(get_user)],
                                course: Course,
                                data_name: str | None = None,
                                ) ->list[Course]:
    education_db = user.education
    courses = education_db.courses
    await update_data(data=courses, new_data=course, object_to_save=education_db, data_name=data_name)
    return education_db.courses

@router.delete('/delete-course/{name}')
async def delete_link(user: Annotated[User, Depends(get_user)],
                      name: str
                      ) ->list[Course]:
    education_db = user.education
    updated_courses = await get_updated_data(data=education_db.courses, name=name)
    education_db.courses = updated_courses
    await education_db.save_changes()
    return education_db.links

@router.post('/update-lection/{data_name}')
async def update_or_add_courses(user: Annotated[User, Depends(get_user)],
                                lection: Lection,
                                data_name: str | None = None,
                                ) ->list[Lection]:
    education_db = user.education
    lections = education_db.lections
    await update_data(data=lections, new_data=lection, object_to_save=education_db, data_name=data_name)
    return education_db.lections

@router.delete('/delete-lection/{data_name}')
async def delete_link(user: Annotated[User, Depends(get_user)],
                      data_name: str
                      ) ->list[Lection]:
    education_db = user.education
    updated_lections = await get_updated_data(data=education_db.lections, data_name=data_name)
    education_db.lections = updated_lections
    await education_db.save_changes()
    return education_db.lections

@router.post('/update-book/{data_name}')
async def update_or_add_courses(user: Annotated[User, Depends(get_user)],
                                book: Book,
                                data_name: str | None = None,
                                ) ->list[Book]:
    education_db = user.education
    books = education_db.books
    await update_data(data=books, new_data=book, object_to_save=education_db, data_name=data_name)
    return education_db.books


@router.delete('/delete-book/{data_name}')
async def delete_link(user: Annotated[User, Depends(get_user)],
                      data_name: str
                      ) ->list[Book]:
    education_db = user.education
    updated_books = await get_updated_data(data=education_db.books, data_name=data_name)
    education_db.books = updated_books
    await education_db.save_changes()
    return education_db.books