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

@pytest.mark.parametrize(
        'user_first_name',
        ['Greg'])
@pytest.mark.anyio
async def test_get_about_username_not_exist(async_client: AsyncClient,
                                            create_about: AboutMe,
                                            user_first_name: str):
    response = await async_client.get('/about/', params={'user_first_name': user_first_name})
    assert response.status_code == 404
    assert response.json()['detail'] == f"User with name {user_first_name} does not exist"


@pytest.mark.anyio
async def test_get_about_not_exist(async_client: AsyncClient, create_user):
    response = await async_client.get('/about/')
    assert response.status_code == 404

@pytest.mark.parametrize(
        'first_name, second_name, descriptions, short_description, email',
        [
            (USERNAME, 'create second name', 'create descriptions',
             'create short_description', 'create@example.com')
            ])
@pytest.mark.anyio
async def test_create_about(async_client: AsyncClient,
                            create_user: User,
                            first_name: str, second_name: str, descriptions: str,
                            short_description: str, email: str):
    response = await async_client.post('/about/create',
                                       json={
                                            "first_name": first_name,
                                            "second_name": second_name,
                                            "descriptions": descriptions,
                                            "short_description": short_description,
                                            "email": email
                                            })
    user = await User.find_one(User.username==USERNAME)
    assert response.status_code == 201
    assert user.about is not None


@pytest.mark.parametrize(
        'first_name, second_name, descriptions, short_description, email',
        [
            (USERNAME, 'create second name', 'create descriptions',
             'create short_description', 'create@example.com')
            ])
@pytest.mark.anyio
async def test_create_about_already_created(async_client: AsyncClient,
                                            create_about: AboutMe,
                                            first_name: str, second_name: str, descriptions: str,
                                            short_description: str, email: str):
    response = await async_client.post('/about/create',
                                       json={
                                            "first_name": first_name,
                                            "second_name": second_name,
                                            "descriptions": descriptions,
                                            "short_description": short_description,
                                            "email": email
                                            })
    assert response.status_code == 403

@pytest.mark.parametrize(
        'first_name, second_name, descriptions, short_description, email',
        [
            ('update first name', 'update second name', 'update descriptions',
             'update short_description', 'create@example.com')
            ])
@pytest.mark.anyio
async def test_update_about(async_client: AsyncClient,
                            create_about: AboutMe,
                            first_name: str, second_name: str, descriptions: str,
                            short_description: str, email: str):
    response = await async_client.put('/about/update',
                                       json={
                                            "first_name": first_name,
                                            "second_name": second_name,
                                            "descriptions": descriptions,
                                            "short_description": short_description,
                                            "email": email
                                            })
    user = await User.find_one(User.username == USERNAME)
    about = user.about
    assert response.status_code == 200
    assert response.json()['first_name'] == first_name
    assert response.json()['second_name'] == second_name
    assert response.json()['descriptions'] == descriptions
    assert response.json()['short_description'] == short_description
    assert response.json()['email'] == email
    assert about.first_name == first_name
    assert about.email == email

@pytest.mark.parametrize('first_name, second_name, descriptions, short_description, email',
        [('update first name', 'update second name', 'update descriptions',
             'update short_description', 'create@example.com')
            ])
@pytest.mark.anyio
async def test_update_about_not_exist(async_client: AsyncClient,
                                    create_user: User,
                                    first_name: str, second_name: str, descriptions: str,
                                    short_description: str, email: str):
    response = await async_client.put('/about/update',
                                       json={
                                            "first_name": first_name,
                                            "second_name": second_name,
                                            "descriptions": descriptions,
                                            "short_description": short_description,
                                            "email": email
                                            })
    assert response.status_code == 404
    assert response.json()['detail'] == f'AboutMe for user {USERNAME} does not exist'
    
@pytest.mark.anyio
async def test_delete_about(async_client: AsyncClient, create_about):
    response = await async_client.delete('/about/delete')
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    user = await User.find_one(User.username == USERNAME)
    assert response.status_code == 200
    assert user.about is None
    assert about is None

@pytest.mark.anyio
async def test_delete_about_not_exist(async_client: AsyncClient, create_user: User):
    response = await async_client.delete('/about/delete')
    assert response.status_code == 404
    assert response.json()['detail'] == f'AboutMe for user {USERNAME} does not exist'

@pytest.mark.parametrize('name, url',
        [('update name', 'https://update.com/')])
@pytest.mark.anyio
async def test_update_or_add_link_name_is_None(async_client: AsyncClient,
                                               create_about: AboutMe,
                                               name: str, url: str):
    response = await async_client.post('/about/update-link',
                                 json={
                                     "name": name,
                                     "url": url
                                    })
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert any(link.name == name for link in about.links)
    assert len(about.links) == len(response.json())

@pytest.mark.parametrize('name, url',
        [('linkedin', 'https://update.com/')])
@pytest.mark.anyio
async def test_update_or_add_link_with_name(async_client: AsyncClient,
                                            create_about: AboutMe,
                                            name: str, url: str
                                            ):
    response = await async_client.post('/about/update-link',
                                 json={
                                     "name": name,
                                     "url": url
                                    },
                                    params={'name': name})
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert len(about.links) == len(response.json())
    assert any(link.name == name and link.url == HttpUrl(url) for link in about.links)

@pytest.mark.anyio
async def test_delete_link(async_client: AsyncClient, create_about: AboutMe):   
    response = await async_client.delete('/about/delete-link/linkedin')
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert not any(link.name == 'linkedin' for link in about.links)

@pytest.mark.parametrize('city, country',
        [('update city', 'update country')])
@pytest.mark.anyio
async def test_update_address(async_client: AsyncClient,
                              create_about: AboutMe,
                              city: str, country: str):
    response = await async_client.post('/about/update-address',
                                 json={
                                     "city": city,
                                     "country": country
                                    })
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert about.address.city == city
    assert about.address.country == country

@pytest.mark.parametrize('city, country',
        [('add city', 'add country')])
@pytest.mark.anyio
async def test_add_address(async_client: AsyncClient,
                           create_about: AboutMe,
                           city: str, country: str):
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    about.address = None
    await about.save_changes()
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert about.address is None
    response = await async_client.post('/about/update-address',
                                 json={
                                     "city": city,
                                     "country": country
                                    })
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert about.address.city == city
    assert about.address.country == country

@pytest.mark.anyio
async def test_delete_address(async_client: AsyncClient, create_about):
    response = await async_client.delete('/about/delete-address')
    about = await AboutMe.find_one(AboutMe.first_name == USERNAME)
    assert response.status_code == 200
    assert about.address is None