import pytest

from httpx import AsyncClient


from app.db.models import User, Hobbies
from app.test.conftest import USERNAME

@pytest.mark.anyio
async def test_get_hobbies_information(async_client: AsyncClient, create_hobbies: Hobbies):
    response = await async_client.get('/hobbies/')
    assert response.status_code == 200
    assert response.json()['descriptions'] == create_hobbies.descriptions

@pytest.mark.anyio
async def test_get_hobbies_information_not_exist(async_client: AsyncClient, create_user: User):
    response = await async_client.get('/hobbies/')
    assert response.status_code == 404
    assert response.json()['detail'] == f"Hobbies for user {create_user.username} does not exist"

@pytest.mark.parametrize(
        'descriptions',
        ['Hello test'])
@pytest.mark.anyio
async def test_create_hobbies_information(
    async_client: AsyncClient,
    create_user: User,
    descriptions: str):
    response = await async_client.post(
        '/hobbies/create',
        json={'descriptions': descriptions})
    user = await User.find_one(User.username == create_user.username, fetch_links=True)
    hobbies = user.hobbies
    assert response.status_code == 201
    assert hobbies is not None
    assert hobbies.descriptions == descriptions

@pytest.mark.parametrize(
        'descriptions',
        ['Hello test'])
@pytest.mark.anyio
async def test_update_hobbies_information(
    async_client: AsyncClient,
    create_hobbies: Hobbies,
    descriptions: str):
    response = await async_client.put(
        '/hobbies/update',
        json={'descriptions': descriptions})
    user = await User.find_one(User.username == USERNAME, fetch_links=True)
    hobbies = user.hobbies
    assert response.status_code == 200
    assert response.json()['descriptions'] == descriptions
    assert hobbies.descriptions == descriptions

@pytest.mark.parametrize(
        'descriptions',
        ['Hello test'])
@pytest.mark.anyio
async def test_update_hobbies_information_not_exist(
    async_client: AsyncClient,
    create_user: User,
    descriptions: str):
    response = await async_client.put(
        '/hobbies/update',
        json={'descriptions': descriptions})
    assert response.status_code == 404
    assert response.json()['detail'] == f"Hobbies for user {create_user.username} does not exist"

@pytest.mark.anyio
async def test_delete_hobbies_information(async_client: AsyncClient, create_hobbies: Hobbies):
    response = await async_client.delete('/hobbies/delete')
    user = await User.find_one(User.username == USERNAME, fetch_links=True)
    hobbies = user.hobbies
    assert response.status_code == 200
    assert hobbies is None

@pytest.mark.anyio
async def test_delete_hobbies_information_not_exist(async_client: AsyncClient, create_user: User):
    response = await async_client.delete('/hobbies/delete')
    assert response.status_code == 404
    assert response.json()['detail'] == f"Hobbies for user {create_user.username} does not exist"


