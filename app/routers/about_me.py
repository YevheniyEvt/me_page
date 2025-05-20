from fastapi import APIRouter

router = APIRouter(
    prefix='/about',
    tags='About me'
)