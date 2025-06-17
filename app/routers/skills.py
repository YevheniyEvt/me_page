from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status


from ..dependencies import get_user, get_updated_data, update_data
from ..db.models import Skills, WorkFlow, Instrument, User


router = APIRouter(
    prefix='/skills',
    tags=['Skills'],
)


@router.get('/', description="Information about skills")
async def skills_information(user: Annotated[User, Depends(get_user)])->Skills:
    skill = user.skills
    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill for user {user.username} does not exist"
        )
    else:
        user.skills.model_dump()
        return user.skills
    
@router.post('/add-workflow')
async def add_workflows(user: Annotated[User, Depends(get_user)],
                                workflow: WorkFlow,
                                ) ->list[WorkFlow]:
    skills_db = user.skills
    if skills_db is None:
        user.skills = await Skills().create()
        skills_db = user.skills
    workflows = skills_db.workflows
    workflows.append(workflow)
    await skills_db.save()
    return skills_db.workflows

@router.delete('/delete-workflow')
async def delete_workflow(user: Annotated[User, Depends(get_user)],
                      name: str
                      ) ->list[WorkFlow]:
    skills_db = user.skills
    workflows = skills_db.workflows
    updated_workflow = await get_updated_data(data=workflows, data_name=name)
    skills_db.workflows = updated_workflow
    await skills_db.save_changes()
    return skills_db.workflows

@router.post('/add-instrument')
async def add_instrument(user: Annotated[User, Depends(get_user)],
                                instrument: Instrument,
                                ) ->list[Instrument]:
    skills_db = user.skills
    if skills_db is None:
        user.skills = await Skills().create()
        skills_db = user.skills
    instruments = skills_db.instruments
    instruments.append(instrument)
    await skills_db.save()
    return skills_db.instruments

@router.delete('/delete-instrument')
async def delete_instrument(user: Annotated[User, Depends(get_user)],
                      name: str
                      ) ->list[Instrument]:
    skills_db = user.skills
    instruments = skills_db.instruments
    updated_instrument = await get_updated_data(data=instruments, data_name=name)
    skills_db.instruments = updated_instrument
    await skills_db.save_changes()
    return skills_db.instruments