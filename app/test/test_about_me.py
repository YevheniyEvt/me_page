import pytest
from pydantic import BaseModel, HttpUrl, EmailStr
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.db import models
from app import schemes
from app import dependencies
from app.db.models import User, AboutMe, Projects, Education, Skills, Hobbies

USERNAME = 'Євгеній'

@pytest.mark.anyio
async def test_get_about_without_name(async_client: AsyncClient, create_about):
    response = await async_client.get('/about/')
    assert response.status_code == 200
    assert response.json()['first_name'] == USERNAME

@pytest.mark.anyio
async def test_get_about_username_not_exist(async_client: AsyncClient, create_about):
    response = await async_client.get('/about/', params={'user_first_name': 'Greg'})
    assert response.status_code == 404
    assert response.json()['detail'] == "User with name Greg does not exist"


@pytest.mark.anyio
async def test_get_about_not_exist(async_client: AsyncClient, create_user):
    response = await async_client.get('/about/')
    assert response.status_code == 404

@pytest.mark.anyio
async def test_create_about(async_client: AsyncClient, create_user):
    response = await async_client.post('/about/create',
                                       json={
                                            "first_name": USERNAME,
                                            "second_name": "string",
                                            "descriptions": "string",
                                            "short_description": "string",
                                            "email": "user@example.com"
                                            })
    user = await User.find_one(User.username=='Євгеній')
    assert response.status_code == 201
    assert user.about is not None
    assert user.about.first_name == 'Євгеній'

@pytest.mark.anyio
async def test_create_about_already_created(async_client: AsyncClient, create_about):
    response = await async_client.post('/about/create',
                                       json={
                                            "first_name": USERNAME,
                                            "second_name": "string",
                                            "descriptions": "string",
                                            "short_description": "string",
                                            "email": "user@example.com"
                                            })
    assert response.status_code == 403

@pytest.mark.anyio
async def test_update_about(async_client: AsyncClient, create_about):
    response = await async_client.put('/about/update',
                                       json={
                                            "first_name": "Update",
                                            "second_name": "string",
                                            "descriptions": "string",
                                            "short_description": "string",
                                            })
    user = await User.find_one(User.username == 'Євгеній')
    assert response.status_code == 200
    assert response.json()['first_name'] == 'Update'
    assert response.json()['second_name'] == 'string'
    assert response.json()['descriptions'] == 'string'
    assert response.json()['short_description'] == 'string'
    assert response.json()['email'] == 'genya421@gmail.com'
    assert user.about.first_name == 'Update'
    assert user.about.email == 'genya421@gmail.com'

@pytest.mark.anyio
async def test_update_about_not_exist(async_client: AsyncClient, create_user):
    response = await async_client.put('/about/update',
                                       json={
                                            "first_name": "Update",
                                            "second_name": "string",
                                            "descriptions": "string",
                                            "short_description": "string",
                                            })
    assert response.status_code == 404
    assert response.json()['detail'] == 'AboutMe for user Євгеній does not exist'
    
@pytest.mark.anyio
async def test_delete_about(async_client: AsyncClient, create_about):
    response = await async_client.delete('/about/delete')
    about = await AboutMe.find_one(AboutMe.first_name == 'Євгеній')
    user = await User.find_one(User.username == 'Євгеній')
    assert response.status_code == 200
    assert user.about is None
    assert about is None

@pytest.mark.anyio
async def test_delete_about_not_exist(async_client: AsyncClient, create_user):
    response = await async_client.delete('/about/delete')
    assert response.status_code == 404
    assert response.json()['detail'] == f'AboutMe for user {USERNAME} does not exist'

@pytest.mark.anyio
async def test_update_or_add_link_name_is_None(async_client: AsyncClient, create_about):
    response = await async_client.post('/about/update-link',
                                 json={
                                     "name": "test",
                                     "url": "https://example.com/"
                                    })
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert any(link.name == 'test' for link in about.links)
    assert len(about.links) == len(response.json())

@pytest.mark.anyio
async def test_update_or_add_link_with_name(async_client: AsyncClient, create_about):
    response = await async_client.post('/about/update-link',
                                 json={
                                     "name": "linkedin",
                                     "url": "https://example.com/"
                                    },
                                    params={'name': 'linkedin'})
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert len(about.links) == len(response.json())
    assert any(link.name == 'linkedin' and link.url == HttpUrl('https://example.com/') for link in about.links)

@pytest.mark.anyio
async def test_delete_link(async_client: AsyncClient, create_about):   
    response = await async_client.delete('/about/delete-link/linkedin')
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert not any(link.name == 'linkedin' for link in about.links)

@pytest.mark.anyio
async def test_update_address(async_client: AsyncClient, create_about):
    response = await async_client.post('/about/update-address',
                                 json={
                                     "city": "test_city",
                                     "country": "test_country"
                                    })
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert about.address.city == "test_city"
    assert about.address.country == "test_country"

@pytest.mark.anyio
async def test_add_address(async_client: AsyncClient, create_about):
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    about.address = None
    await about.save_changes()
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert about.address is None
    response = await async_client.post('/about/update-address',
                                 json={
                                     "city": "test_city",
                                     "country": "test_country"
                                    })
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert about.address.city == "test_city"
    assert about.address.country == "test_country"

@pytest.mark.anyio
async def test_delete_address(async_client: AsyncClient, create_about):
    response = await async_client.delete('/about/delete-address')
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert about.address is None