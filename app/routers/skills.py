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
    try:
        user.skills.model_dump()
        return user.skills
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Skill for user {user.username} does not exist"
        )
    
@router.post('/update-workflow')
async def update_or_add_workflows(user: Annotated[User, Depends(get_user)],
                                workflow: WorkFlow,
                                name: str | None = None,
                                ) ->list[WorkFlow]:
    skills_db = user.skills
    if skills_db is None:
        user.skills = await Skills().create()
        skills_db = user.skills
    print(user.skills.model_dump())
    workflows = skills_db.workflows
    await update_data(data=workflows, new_data=workflow, object_to_save=skills_db, data_name=name)
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

@router.post('/update-instrument')
async def update_or_add_instrument(user: Annotated[User, Depends(get_user)],
                                instrument: Instrument,
                                name: str | None = None,
                                ) ->list[Instrument]:
    skills_db = user.skills
    if skills_db is None:
        user.skills = await Skills().create()
        skills_db = user.skills
    instruments = skills_db.instruments
    await update_data(data=instruments, new_data=instrument, object_to_save=skills_db, data_name=name)
    return skills_db.workflows

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