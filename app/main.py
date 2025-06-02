from fastapi import FastAPI

from .routers import about_me, projects, study, user, skills, hobbies
from app.db.database import lifespan

def get_app(lifespan):
    app = FastAPI(lifespan=lifespan)
    app.include_router(user.router)
    app.include_router(about_me.router)
    app.include_router(projects.router)
    app.include_router(study.router)
    app.include_router(skills.router)
    app.include_router(hobbies.router)
    return app

app = get_app(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {'Hello': 'World'}
