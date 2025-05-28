from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status


from ..dependencies import get_user, update_data, get_updated_data
from ..schemes import ReprProject, UpdateProject, CreateProject
from ..db.models import User, Projects, Links, Tags

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('/')
async def my_projects(user: Annotated[User, Depends(get_user)])->list[ReprProject]:
    if len(user.projects) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projects for user {user.username} does not exist"
        )
    else:
        return user.projects

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_project(project: CreateProject,
                        tags: list[Tags],
                        user: Annotated[User, Depends(get_user)]
                         )->ReprProject:
    project_created = Projects(**project.model_dump())
    project_created.tags = tags
    await project_created.save()

    user.projects.append(project_created)
    await user.save_changes()
    return project_created

@router.put('/update')
async def update_project(user: Annotated[User, Depends(get_user)],
                         project: UpdateProject,
                         name: str | None = None,)->list[ReprProject]:
    if len(user.projects) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projects for user {user.username} does not exist"
        )
    else:
        projects_db = user.projects
        await update_data(data=projects_db, new_data=project, object_to_save=projects_db, data_name=name)
        return projects_db

@router.delete('/delete')
async def delete_project(user: Annotated[User, Depends(get_user)],
                         name: str | None = None)->list[ReprProject]:
    projects_db = user.projects
    updated_projects = await get_updated_data(data=projects_db, data_name=name)
    user.projects = updated_projects
    await user.save_changes()
    return user.projects

@router.post('/update-link')
async def update_or_add_link(user: Annotated[User, Depends(get_user)],
                             link: Links,
                             name_project: str,
                             name_link: str | None = None,
                            ) ->list[Links] | dict:
    projects_db = user.projects
    links = projects_db.links
    await update_data(data=links, new_data=link, object_to_save=projects_db, data_name=name_link)
    return projects_db.links

@router.delete('/delete-link')
async def delete_link(user: Annotated[User, Depends(get_user)],
                      name: str) ->list[Links]:
    projects_db = user.projects
    updated_links = await get_updated_data(data=projects_db.links, data_name=name)
    projects_db.links = updated_links
    await projects_db.save_changes()
    return projects_db.links
    
@router.post('/update-tag')
async def update_or_add_tag(user: Annotated[User, Depends(get_user)],
                            tag: Tags,
                            name_project: str,
                            name_tag: str | None = None,
                            ) ->list[Tags]:
    projects_db = user.projects
    tags = projects_db.tags
    await update_data(data=tags, new_data=tag, object_to_save=projects_db, data_name=name_tag)
    return projects_db.tags

@router.delete('/delete-tag/{name}')
async def delete_tag(user: Annotated[User, Depends(get_user)],
                      name: str) ->list[Tags]:
    projects_db = user.projects
    updated_tags = await get_updated_data(data=projects_db.tags, data_name=name)
    projects_db.tags = updated_tags
    await projects_db.save_changes()
    return projects_db.tags