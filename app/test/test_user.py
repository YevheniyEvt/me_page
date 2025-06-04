import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from app.db import models
from app import schemes
from app import dependencies
from app.db.models import User, AboutMe, Projects, Education, Skills, Hobbies

@pytest.mark.anyio
async def test_create_user(async_client: AsyncClient):
    response = await async_client.post('/user/create', json={'username': 'Євгеній'})
    user = User.find_one(User.username=='Євгеній')
    assert response.status_code == 201
    assert user is not None


@pytest.mark.anyio
async def test_user_information(async_client: AsyncClient, create_user):
    response = await async_client.get('/user/')
    assert response.status_code == 200
    assert response.json()['username'] == 'Євгеній'
    assert response.json()['about'] == None


{'_id': '683e0034b84ae8db5403e420', 'username': 'Євгеній', 'about': None, 'projects': [], 'education': None, 'skills': None, 'hobbies': None}