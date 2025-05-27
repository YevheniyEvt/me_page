from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status


from ..dependencies import get_user, get_updated_data, update_data
from ..schemes import ReprEducation, CreateEducation
from ..db.models import (User, Education,
                     Course, Lection, Book)


router = APIRouter(
    prefix='/education',
    tags=['Education'],

)

@router.get('/', description="Information about education")
async def education_information(user: Annotated[User, Depends(get_user)])->ReprEducation:  
    try:
        user.education.model_dump()
        return user.education
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Education for user {user.username} does not exist"
        )
        
@router.post('/create')
async def create_education_information(user: Annotated[User, Depends(get_user)],
                                       education: CreateEducation):
    try:
        user.education.model_dump()
        return {'msg': f'Education: {user.education.descriptions} for user {user.username} already exist'}
    except AttributeError:
        education_create = Education(**education.model_dump())
        await education_create.save()
        user.education = education_create
        await user.save_changes()

@router.put('/update')
async def update_education_information(user: Annotated[User, Depends(get_user)],
                                       education: CreateEducation
                                       )->ReprEducation:
    education_db = user.education
    education_db.descriptions = education.descriptions
    await education_db.save_changes()
    return education_db

@router.delete('/delete')
async def delete_education_information(user: Annotated[User, Depends(get_user)]):
    try:
        await user.education.delete()
        return {'msg': f'Education for user {user.username} was deleted'}
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Education for user {user.username} does not exist"
        )
    
@router.post('/update-course')
async def update_or_add_courses(user: Annotated[User, Depends(get_user)],
                                course: Course,
                                name: str | None = None,
                                ) ->list[Course]:
    education_db = user.education
    courses = education_db.courses
    await update_data(data=courses, new_data=course, object_to_save=education_db, data_name=name)
    return education_db.courses

@router.delete('/delete-course')
async def delete_course(user: Annotated[User, Depends(get_user)],
                      name: str
                      ) ->list[Course]:
    education_db = user.education
    updated_courses = await get_updated_data(data=education_db.courses, data_name=name)
    education_db.courses = updated_courses
    await education_db.save_changes()
    return education_db.courses

@router.post('/update-lection')
async def update_or_add_lection(user: Annotated[User, Depends(get_user)],
                                lection: Lection,
                                name: str | None = None,
                                ) ->list[Lection]:
    education_db = user.education
    lections = education_db.lections
    await update_data(data=lections, new_data=lection, object_to_save=education_db, data_name=name)
    return education_db.lections

@router.delete('/delete-lection')
async def delete_lection(user: Annotated[User, Depends(get_user)],
                      name: str
                      ) ->list[Lection]:
    education_db = user.education
    updated_lections = await get_updated_data(data=education_db.lections, data_name=name)
    education_db.lections = updated_lections
    await education_db.save_changes()
    return education_db.lections

@router.post('/update-book')
async def update_or_add_book(user: Annotated[User, Depends(get_user)],
                                book: Book,
                                name: str | None = None,
                                ) ->list[Book]:
    education_db = user.education
    books = education_db.books
    await update_data(data=books, new_data=book, object_to_save=education_db, data_name=name)
    return education_db.books

@router.delete('/delete-book')
async def delete_book(user: Annotated[User, Depends(get_user)],
                      name: str
                      ) ->list[Book]:
    education_db = user.education
    updated_books = await get_updated_data(data=education_db.books, data_name=name)
    education_db.books = updated_books
    await education_db.save_changes()
    return education_db.books