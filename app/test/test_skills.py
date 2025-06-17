import pytest

from pydantic import HttpUrl
from httpx import AsyncClient


from app.db.models import User, Projects, Skills
from app.test.conftest import USERNAME

@pytest.mark.anyio
async def test_skills_information(async_client: AsyncClient, create_skills: Skills):
    response = await async_client.get('/skills/')
    assert response.status_code == 200
    assert response.json()['workflows'][0] == create_skills.workflows[0].model_dump()
    assert response.json()['instruments'][0] == create_skills.instruments[0].model_dump()

@pytest.mark.anyio
async def test_skills_information_not_exist(async_client: AsyncClient, create_user: User):
    response = await async_client.get('/skills/')
    assert response.status_code == 404
    assert response.json()['detail'] == f"Skill for user {USERNAME} does not exist"


@pytest.mark.parametrize(
        'name',
        ['hello from test'])
@pytest.mark.anyio
async def test_add_instrument(async_client: AsyncClient,
                             create_skills: Skills,
                             name: str):
    response = await async_client.post('/skills/add-instrument',
                                       json={'name': name})
    assert response.status_code == 200
    assert {'name': name} in response.json()

@pytest.mark.parametrize(
        'name',
        ['hello from test'])
@pytest.mark.anyio
async def test_add_instrument_skills_is_none(async_client: AsyncClient,
                                            create_user: User,
                                            name: str):
    response = await async_client.post('/skills/add-instrument',
                                       json={'name': name})
    assert response.status_code == 200
    assert {'name': name} in response.json()


@pytest.mark.anyio
async def test_delete_instrument(async_client: AsyncClient,
                             create_skills: Skills):
    instrument_test = create_skills.instruments[0]
    response = await async_client.delete('/skills/delete-instrument',
                                       params={'name': instrument_test.name})
    skills = await Skills.find_one(Skills.id == create_skills.id)
    instrument_db = skills.instruments
    assert response.status_code == 200
    assert len(instrument_db) == 0


@pytest.mark.parametrize(
        'name',
        ['hello from test'])
@pytest.mark.anyio
async def test_add_workflow(async_client: AsyncClient,
                             create_skills: Skills,
                             name: str):
    response = await async_client.post('/skills/add-workflow',
                                       json={'name': name})
    assert response.status_code == 200
    assert {'name': name} in response.json()

@pytest.mark.parametrize(
        'name',
        ['hello from test'])
@pytest.mark.anyio
async def test_add_workflow_skills_is_none(async_client: AsyncClient,
                                            create_user: User,
                                            name: str):
    response = await async_client.post('/skills/add-workflow',
                                       json={'name': name})
    assert response.status_code == 200
    assert {'name': name} in response.json()


@pytest.mark.anyio
async def test_delete_workflow(async_client: AsyncClient,
                             create_skills: Skills):
    workflow_test = create_skills.workflows[0]
    response = await async_client.delete('/skills/delete-workflow',
                                       params={'name': workflow_test.name})
    skills = await Skills.find_one(Skills.id == create_skills.id)
    workflow_db = skills.workflows
    assert response.status_code == 200
    assert len(workflow_db) == 0