from fastapi import APIRouter, Depends, status
from typing import Annotated

from fastapi import Depends

from ..dependencies import get_user
from ..schemes import CreateUser, GetUser
from ..db.models import User


router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/')
async def user_information(user: Annotated[GetUser, Depends(get_user)])->User:
    return user

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUser):
    user_create = User(**user.model_dump())
    await user_create.save()
