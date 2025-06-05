import pytest
from pydantic import BaseModel, HttpUrl, EmailStr
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.db import models
from app import schemes
from app import dependencies
from app.db.models import User, AboutMe, Projects, Education, Skills, Hobbies
from app.test.conftest import USERNAME


@pytest.mark.anyio
async def test_my_projects(async_client: AsyncClient, create_projects: Projects):
    response = await async_client.get('/projects/')
    project = response.json()[0]
    assert response.status_code == 200
    assert project['name'] == create_projects.name
    assert project['descriptions'] == create_projects.descriptions
    assert project['instruments'] == create_projects.instruments
    assert project['tags'] == []
    assert project['links'] == []


@pytest.mark.anyio
async def test_my_projects_not_exist(async_client: AsyncClient, create_user: User):
    response = await async_client.get('/projects/')
    assert response.status_code == 404
    assert response.json()['detail'] == f"Projects for user {create_user.username} does not exist"


@pytest.mark.parametrize(
        'name, descriptions, instruments, tags_name, tags_description',
        [
            ('created project name', 'created project descriptions',
             'created project instruments', 'created tags name', 'created tags description'),
             ])
@pytest.mark.anyio
async def test_create_project(async_client: AsyncClient,
                           create_user: User,
                           name, descriptions, instruments, tags_name, tags_description):
    response = await async_client.post('/projects/create',
                                       json={'project':{'name': name,
                                                        'descriptions': descriptions,
                                                        'instruments': instruments},
                                            'tags':[{"name": tags_name,
                                                    "description": tags_description}
                                                    ]
                                            })
    tag = response.json()['tags'][0]
    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['descriptions'] == descriptions
    assert response.json()['instruments'] == instruments
    assert tag['name'] == tags_name
    assert tag['description'] == tags_description
    assert response.json()['links'] == []

@pytest.mark.parametrize(
        'name, descriptions, instruments',
        [
            ('updated project name', 'updated project descriptions', 'updated project instruments'),
        ])
@pytest.mark.anyio
async def test_update_project(async_client: AsyncClient,
                                      create_projects: Projects,
                                      name, descriptions, instruments):
    response = await async_client.put(f'/projects/update/{create_projects.name}',
                                       json={'name': name,
                                             'descriptions': descriptions,
                                             'instruments': instruments
                                            })
    project_db = await Projects.find_one(Projects.name == create_projects.name)
    user = await User.find_one(User.username == USERNAME, fetch_links=True)
    user_projects = user.projects
    project = response.json()[0]
    assert response.status_code == 200
    assert project_db is None
    assert any(project for project in user_projects if project.name == name)
    assert project['name'] == name
    assert project['descriptions'] == descriptions
    assert project['instruments'] == instruments
    assert project['tags'] == []
    assert project['links'] == []

@pytest.mark.parametrize(
        'name, descriptions, instruments',
        [
            ('updated project name', 'updated project descriptions', 'updated project instruments'),
        ])
@pytest.mark.anyio
async def test_update_project_not_exist(async_client: AsyncClient,
                                      create_projects: Projects,
                                      name, descriptions, instruments):
    response = await async_client.put(f'/projects/update/{create_projects.name}not_exist',
                                       json={'name': name,
                                             'descriptions': descriptions,
                                             'instruments': instruments
                                            })
    assert response.status_code == 404
    assert response.json()['detail'] == f"Projects for user {USERNAME} does not exist"

@pytest.mark.anyio
async def test_delete_project(async_client: AsyncClient, create_projects: Projects):
    response = await async_client.delete(f'/projects/delete/{create_projects.name}')
    user = await User.find_one(User.username == USERNAME, fetch_links=True)
    user_projects = user.projects
    assert response.status_code == 200
    assert not any(project for project in user_projects if project.name == create_projects.name)

@pytest.mark.anyio
async def test_delete_project_not_exist(async_client: AsyncClient, create_projects: Projects):
    response = await async_client.delete(f'/projects/delete/{create_projects.name}not_exist')
    assert response.status_code == 404
    assert response.json()['detail'] == f"Data with name {create_projects.name}not_exist does not exist"