from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends


from ..dependencies import create_about, get_user, update_data, get_updated_data
from ..schemes import UpdateAboutMe, CreateAboutMe, ReprAboutMe
from ..db.models import AboutMe, Links, User

router = APIRouter(
    prefix='/about',
    tags=['About me']
)


@router.get("/")
async def about(user: Annotated[User, Depends(get_user)])->ReprAboutMe:
    try:
        user.about.model_dump()
        return user.about
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AboutMe for user {user.username} does not exist"
        )

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_about(user: Annotated[User, Depends(get_user)],
                       about: CreateAboutMe)->ReprAboutMe:
    if about.first_name == 'Євгеній':
        about_db = create_about()
    else:
        about_db = AboutMe(**about.model_dump())
    await about_db.create()
    
    try:
        user.about.model_dump()
        return {'msg': f'AboutMe for user {user.username} already exist'}
    except AttributeError:
        if about.first_name == 'Євгеній':
            about_db = create_about()
        else:
            about_db = AboutMe(**about.model_dump())
        await about_db.save()
        user.about = about_db
        await user.save_changes()
    return user.about

@router.put('/update')
async def update_about(about: UpdateAboutMe,
                       user: Annotated[User, Depends(get_user)],
                       ) ->ReprAboutMe:
    about_db = user.about
    update_data = about.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(about_db, key, value)
    await about_db.save_changes()
    return about_db

@router.delete('/delete')
async def delete_about(user: Annotated[User, Depends(get_user)]):
    try:
        await user.about.delete()
        return {'msg': f'AboutMe for user {user.username} was deleted'}
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AboutMe for user {user.username} does not exist"
        )
    
@router.post('/update-link')
async def update_or_add_link(user: Annotated[User, Depends(get_user)],
                             link: Links,
                             name: str | None = None,
                            ) ->list[Links]:
    about_db = user.about
    links = about_db.links
    await update_data(data=links, new_data=link, object_to_save=about_db, data_name=name)
    return about_db.links

@router.delete('/delete-link/{name}')
async def delete_link(user: Annotated[User, Depends(get_user)],
                      name: str) ->list[Links]:
    about_db = user.about
    updated_links = await get_updated_data(data=about_db.links, data_name=name)
    about_db.links = updated_links
    await about_db.save_changes()
    return about_db.links