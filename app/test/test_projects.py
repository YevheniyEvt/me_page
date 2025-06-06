import pytest

from pydantic import HttpUrl
from httpx import AsyncClient


from app.db.models import User, Projects
from app.test.conftest import USERNAME


@pytest.mark.anyio
async def test_my_projects(async_client: AsyncClient, create_projects: Projects):
    response = await async_client.get('/projects/')
    project = response.json()[0]
    assert response.status_code == 200
    assert project['name'] == create_projects.name
    assert project['descriptions'] == create_projects.descriptions
    assert project['instruments'] == create_projects.instruments


@pytest.mark.anyio
async def test_my_projects_not_exist(async_client: AsyncClient, create_user: User):
    response = await async_client.get('/projects/')
    assert response.status_code == 404
    assert response.json()['detail'] == f"Projects for user {create_user.username} does not exist"


@pytest.mark.parametrize(
        'name, descriptions, instruments, tags_name, tags_description',
        [('created project name', 'created project descriptions', 'created project instruments',
          'created tags name', 'created tags description')])
@pytest.mark.anyio
async def test_create_project(
    async_client: AsyncClient,
    create_user: User,
    name: str, descriptions: str, instruments: str, tags_name: str, tags_description: str):
    response = await async_client.post(
        '/projects/create',
        json={
            'project':{'name': name,
                        'descriptions': descriptions,
                        'instruments': instruments},
            'tags':[{"name": tags_name,
                    "description": tags_description}]
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
        [('updated project name', 'updated project descriptions','updated project instruments')])
@pytest.mark.anyio
async def test_update_project(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str, descriptions: str, instruments: str):
    response = await async_client.put(
        f'/projects/update/{create_projects.name}',
        json={
            'name': name,
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


@pytest.mark.parametrize(
        'name, descriptions, instruments',
        [('updated project name', 'updated project descriptions',
          'updated project instruments')])
@pytest.mark.anyio
async def test_update_project_not_exist(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str, descriptions: str, instruments: str):
    response = await async_client.put(
        f'/projects/update/{create_projects.name}not_exist',
        json={
            'name': name,
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


@pytest.mark.parametrize(
        'name, url',
        [('updated link name', 'https://updated.com/')])
@pytest.mark.anyio
async def test_update_or_add_link_without_name(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str, url: str):
    response = await async_client.post(
        f'/projects/update-link/{create_projects.id}',
        json={
            "name": name,
            "url": url
        })
    project = await Projects.find_one(Projects.id == create_projects.id)
    links_db = project.links
    assert response.status_code == 200
    assert any(link.name == name for link in links_db)
    assert len(links_db) == len(response.json())


@pytest.mark.parametrize(
        'name, url',
        [('linkedin', 'https://updated.com/')])
@pytest.mark.anyio
async def test_update_or_add_link_with_name(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str, url: str):
    response = await async_client.post(
        f'/projects/update-link/{create_projects.id}',
        json={
            'name': name,
            "url": url
            },
        params={'name_link': name})
    project = await Projects.find_one(Projects.id == create_projects.id)
    links_db = project.links
    assert response.status_code == 200
    assert len(links_db) == len(response.json())
    assert any(link.name == name and link.url == HttpUrl(url) for link in links_db)


@pytest.mark.parametrize('name',['created link name'])
@pytest.mark.anyio
async def test_delete_link(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str):   
    response = await async_client.delete(
        f'/projects/delete-link/{create_projects.id}',
        params={'name': name})
    project = await Projects.find_one(Projects.id == create_projects.id)
    links_db = project.links
    assert response.status_code == 200
    assert not any(link.name == name for link in links_db)


@pytest.mark.parametrize('name',['link not exist'])
@pytest.mark.anyio
async def test_delete_link_not_exist(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str):   
    response = await async_client.delete(
        f'/projects/delete-link/{create_projects.id}',
        params={'name': name})
    assert response.status_code == 404
    assert response.json()['detail'] == "Data with name link not exist does not exist"


@pytest.mark.parametrize(
        'name, description',
        [('updated tag name', 'updated tag description')])
@pytest.mark.anyio
async def test_update_or_add_tag_without_name(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str, description: str):
    response = await async_client.post(
        f'/projects/update-tag/{create_projects.id}',
        json={
            "name": name,
            "description": description
            })
    project = await Projects.find_one(Projects.id == create_projects.id)
    tags_db = project.tags
    assert response.status_code == 200
    assert any(tag.name == name for tag in tags_db)
    assert len(tags_db) == len(response.json())


@pytest.mark.parametrize(
        'name, description',
        [('updated tag name', 'updated tag description')])
@pytest.mark.anyio
async def test_update_or_add_tag_with_name(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str, description: str):
    response = await async_client.post(
        f'/projects/update-tag/{create_projects.id}',
        json={
            'name': name,
            "description": description
            },
        params={'name_tag': name})
    project = await Projects.find_one(Projects.id == create_projects.id)
    tags_db = project.tags
    assert response.status_code == 200
    assert len(tags_db) == len(response.json())
    assert any(tag.name == name and tag.description == description for tag in tags_db)


@pytest.mark.parametrize('name',['created tag name'])
@pytest.mark.anyio
async def test_delete_tag(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str):
    response = await async_client.delete(
        f'/projects/delete-tag/{create_projects.id}',
        params={'tag_name': name})
    project = await Projects.find_one(Projects.id == create_projects.id)
    tags_db = project.tags
    assert response.status_code == 200
    assert not any(tag.name == name for tag in tags_db)

@pytest.mark.parametrize('name',['tag not exist'])
@pytest.mark.anyio
async def test_delete_tag_not_exist(
    async_client: AsyncClient,
    create_projects: Projects,
    name: str):
    response = await async_client.delete(
        f'/projects/delete-tag/{create_projects.id}',
        params={'tag_name': name})
    assert response.status_code == 404
    assert response.json()['detail'] == "Data with name tag not exist does not exist"
