from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends


from ..dependencies import create_about_evgeniy, get_user, update_data, get_updated_data
from ..schemes import UpdateAboutMe, CreateAboutMe, ReprAboutMe
from ..db.models import AboutMe, Links, User, Address

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
    try:
        user.about.model_dump()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'AboutMe for user {user.username} already exist'
        )

    except AttributeError:
        if about.first_name == 'Євгеній':
            about_db = await create_about_evgeniy()
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
    if about_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'AboutMe for user {user.username} does not exist'
        )
    update_data = about.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(about_db, key, value)
    await about_db.save()
    await user.save_changes()
    return about_db

@router.delete('/delete')
async def delete_about(user: Annotated[User, Depends(get_user)]):

    about = user.about
    if about is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AboutMe for user {user.username} does not exist"
        )
    
    await about.delete()
    user.about = None
    await user.save_changes()
        
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
                      name: str):
    about_db = user.about
    updated_links = await get_updated_data(data=about_db.links, data_name=name)
    about_db.links = updated_links
    await about_db.save()

@router.post('/update-address')
async def update_or_add_address(user: Annotated[User, Depends(get_user)],
                                       address: Address):
    about_db = user.about
    address_db = about_db.address
    try:
        address_db.model_dump()
    except AttributeError:
        address_create = Address(**address.model_dump())
        about_db.address = address_create
        await about_db.save_changes()
    else:
        update_data = address.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(about_db.address, key, value)
        await about_db.save()

@router.delete('/delete-address')
async def delete_address(user: Annotated[User, Depends(get_user)]):
    about_db = user.about
    address = about_db.address
    if address is not None:
        about_db.address = None
        await about_db.save()
        return {'msg': f'Address for user {user.username} was deleted'}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address for user {user.username} does not exist"
        )
    