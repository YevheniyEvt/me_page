from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from logging import info

from fastapi import FastAPI, Depends, Request
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie, WriteRules
from beanie.operators import Pull

from ..dependencies import check_first_name
from ..schemes import ReprProject, UpdateProject, CreateProject, DeleteProject
from ..db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags)

router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)


@router.get('/')
async def my_projects(user_first_name: Annotated[str, Depends(check_first_name)])->list[ReprProject]:
    about = await AboutMe.find_one(AboutMe.first_name==user_first_name,
                                   fetch_links=True
                                   )
    if not about:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with name {user_first_name} does not exist"
                            )
    return about.projects

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_project(project: CreateProject,
                        tags: list[Tags],
                        user_first_name: Annotated[str, Depends(check_first_name)]
                         )->ReprProject:
    project_created = Projects(**project.model_dump())
    project_created.tags = tags
    await project_created.save()

    about_db = await AboutMe.find_one(AboutMe.first_name == user_first_name,
                                      fetch_links=True
                                      )
    about_db.projects.append(project_created)
    await about_db.save_changes()
    return project_created


@router.put('/update')
async def update_project(project: UpdateProject)->ReprProject:
    project_db = await Projects.find_one(Projects.name == project.name)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Projects with name {project.name} does not exist"
                            )
    update_data = project.model_dump(exclude_none=True)
    print(update_data)
    for key, value in update_data.items():
        setattr(project_db, key, value)
    await project_db.save_changes()
    return project_db


@router.delete('/delete')
async def delete_project(project: DeleteProject):
    project_db = await Projects.find_one(Projects.name == project.name)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Projects with name {project.name} does not exist"
                            )
    await project_db.delete()


@router.post('/update-link')
async def update_or_add_link(link: Links,
                            project: UpdateProject
                            ) ->list[Links]:
    project_db = await Projects.find_one(Projects.name == project.name)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Projects with name {project.name} does not exist"
                            )
    link_get = (link_db for link_db in project_db.links if link_db.name == link.name)
    try:
        link_db = next(link_get)
        link_db.url = link.url
        await project_db.save_changes()
    except StopIteration:
        project_db.links.append(link)
        await project_db.save()
    return project_db.links


@router.delete('/delete-link/{name}')
async def delete_link(project: UpdateProject, name: str) ->list[Links]:
    project_db = await Projects.find_one(Projects.name == project.name)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Projects with name {project.name} does not exist"
                            )
    updated_links = [link for link in project_db.links if link.name != name]
    if len(updated_links) == len(project_db.links):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"link with name {name} does not exist"
        )
    else:
        project_db.links = updated_links
        await project_db.save_changes()
    return project_db.links
    
@router.post('/update-tag')
async def update_or_add_tag(tag: Tags,
                            project: UpdateProject
                            ) ->list[Tags]:
    project_db = await Projects.find_one(Projects.name == project.name)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Projects with name {project.name} does not exist"
                            )
    tag_get = (tag_db for tag_db in project_db.tags if tag_db.name == tag.name)
    try:
        tag_db = next(tag_get)
        tag_db.description = tag.description
        await project_db.save_changes()
    except StopIteration:
        project_db.links.append(tag)
        await project_db.save()
    return project_db.links


@router.delete('/delete-tag/{name}')
async def delete_tag(project: UpdateProject, name: str) ->list[Tags]:
    project_db = await Projects.find_one(Projects.name == project.name)
    if not project_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Projects with name {project.name} does not exist"
                            )
    updated_tag = [tag for tag in project_db.tags if tag.name != name]
    if len(updated_tag) == len(project_db.tags):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tag with name {name} does not exist"
        )
    else:
        project_db.tags = updated_tag
        await project_db.save_changes()
    return project_db.links