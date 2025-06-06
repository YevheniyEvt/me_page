import pytest

from httpx import AsyncClient


from app.db.models import User
from app.test.conftest import USERNAME

@pytest.mark.anyio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post('/user/create', json={'username': USERNAME})
    user = User.find_one(User.username==USERNAME)
    assert response.status_code == 201
    assert user is not None


@pytest.mark.anyio
async def test_user_information(async_client: AsyncClient, create_user: User):
    response = await async_client.get('/user/')
    assert response.status_code == 200
    assert response.json()['username'] == USERNAME
    assert response.json()['about'] == None

