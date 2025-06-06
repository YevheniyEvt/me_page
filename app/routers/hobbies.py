from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status


from ..dependencies import get_user
from ..db.models import Hobbies, User


router = APIRouter(
    prefix='/hobbies',
    tags=['Hobbies'],
)


@router.get('/', description="Information about hobbies")
async def hobbies_information(user: Annotated[User, Depends(get_user)])->Hobbies:  
    try:
        user.hobbies.model_dump()
        return user.hobbies
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobbies for user {user.username} does not exist"
        )
        
@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_hobbies_information(user: Annotated[User, Depends(get_user)],
                                       hobbies: Hobbies):
    try:
        user.hobbies.model_dump()
        return {'msg': f'Hobbies: {user.hobbies.descriptions} for user {user.username} already exist'}
    except AttributeError:
        hobbies_create = Hobbies(**hobbies.model_dump())
        await hobbies_create.save()
        user.hobbies = hobbies_create
        await user.save_changes()

@router.put('/update')
async def update_hobbies_information(user: Annotated[User, Depends(get_user)],
                                       hobbies: Hobbies)->Hobbies:
    hobbies_db = user.hobbies
    if hobbies_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobbies for user {user.username} does not exist"
        )
    hobbies_db.descriptions = hobbies.descriptions
    await hobbies_db.save_changes()
    return hobbies_db

@router.delete('/delete')
async def delete_hobbies_information(user: Annotated[User, Depends(get_user)]):
    hobbies = user.hobbies
    if hobbies is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hobbies for user {user.username} does not exist"
        )
    await hobbies.delete()
    user.hobbies = None
    await user.save_changes()
