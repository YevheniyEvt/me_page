from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from ..dependencies import create_about, check_first_name
from ..schemes import UpdateAboutMe, CreateAboutMe, ReprAboutMe
from ..db.models import AboutMe, Links

router = APIRouter(
    prefix='/about',
    tags=['About me']
)


@router.get("/")
async def about(user_first_name: Annotated[str, Depends(check_first_name)])->ReprAboutMe:
    about = await AboutMe.find_one(AboutMe.first_name == user_first_name)
    if not about:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with name {user_first_name} does not exist"
                            )
    return about


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_about(about: CreateAboutMe)->ReprAboutMe:
    if about.first_name == 'Євгеній':
        about_db = create_about()
    else:
        about_db = AboutMe(**about.model_dump())
    await about_db.create()
    return about_db


@router.delete('/delete')
async def delete_about(user_first_name: Annotated[str, Depends(check_first_name)]):
    await AboutMe.find(AboutMe.first_name == user_first_name).delete()
    return {'msg': f'Name {user_first_name} was deleted'}


@router.put('/update')
async def update_about(about: UpdateAboutMe,
                       user_first_name: Annotated[str, Depends(check_first_name)]
                       ) ->ReprAboutMe:
    about_db = await AboutMe.find_one(AboutMe.first_name == user_first_name)
    update_data = about.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(about_db, key, value)
    await about_db.save_changes()
    return about_db


@router.post('/update-link')
async def update_or_add_link(link: Links,
                            user_first_name: Annotated[str, Depends(check_first_name)]
                            ) ->list[Links]:
    about_db = await AboutMe.find_one(AboutMe.first_name == user_first_name)
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
async def delete_link(name: str,
                      user_first_name: Annotated[str, Depends(check_first_name)]
                      ) ->list[Links]:
    about_db = await AboutMe.find_one(AboutMe.first_name == user_first_name)
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