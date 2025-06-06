from typing import Annotated
from beanie import BeanieObjectId

from fastapi import APIRouter, Depends, HTTPException, status


from ..dependencies import get_user, update_data, get_updated_data, get_project
from ..schemes import ReprProject, UpdateProject, CreateProject, DeleteTag
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
                        user: Annotated[User, Depends(get_user)])->ReprProject:
    project_created = Projects(**project.model_dump())
    project_created.tags = tags
    await project_created.save()
    user.projects.append(project_created)
    await user.save_changes()
    return project_created

@router.put('/update/{name}')
async def update_project(user: Annotated[User, Depends(get_user)],
                         project: UpdateProject,
                         name: str)->list[ReprProject]:
    user_projects = user.projects
    if not any(project for project in user_projects if project.name == name):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Projects for user {user.username} does not exist"
        )
    else:
        projects_db = user.projects
        await update_data(data=projects_db, new_data=project, data_name=name)
        await user.save_changes()
        return projects_db

@router.delete('/delete/{name}')
async def delete_project(user: Annotated[User, Depends(get_user)],
                         name: str):
    projects_db = user.projects
    updated_projects = await get_updated_data(data=projects_db, data_name=name)
    user.projects = updated_projects
    await user.save_changes()


@router.post('/update-link/{project_id}')
async def update_or_add_link(project: Annotated[Projects, Depends(get_project)],
                             link: Links,
                             name_link: str | None = None) ->list[Links] | dict:
    links = project.links
    await update_data(data=links, new_data=link, object_to_save=project, data_name=name_link)
    return project.links

@router.delete('/delete-link/{project_id}')
async def delete_link(project: Annotated[Projects, Depends(get_project)],
                      name: str) ->list[Links]:
    updated_links = await get_updated_data(data=project.links, data_name=name)
    project.links = updated_links
    await project.save_changes()
    return project.links
    
@router.post('/update-tag/{project_id}')
async def update_or_add_tag(project: Annotated[Projects, Depends(get_project)],
                            tag: Tags,
                            name_tag: str | None = None) ->list[Tags]:
    tags = project.tags
    await update_data(data=tags, new_data=tag, object_to_save=project, data_name=name_tag)
    return project.tags

@router.delete('/delete-tag/{project_id}')
async def delete_tag(project: Annotated[Projects, Depends(get_project)],
                      tag_name: str) ->list[Tags]:
    tags = project.tags
    updated_tags = await get_updated_data(data=tags, data_name=tag_name)
    project.tags = updated_tags
    await project.save_changes()
    return project.tags

