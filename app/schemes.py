from beanie import Document, Link
from pydantic import BaseModel, EmailStr, HttpUrl
from .db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags)


class BaseAboutMe(BaseModel):
    first_name:str
    second_name: str
    descriptions: str
    short_description: str
    email: EmailStr


class ReprAboutMe(BaseAboutMe):
    address: Address | None = None
    links: list[Links] | None = None


class CreateAboutMe(BaseAboutMe):
    pass


class UpdateAboutMe(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    descriptions: str | None = None
    short_description: str | None = None
    email: EmailStr | None = None


class BaseProject(BaseModel):
    name: str
    descriptions: str
    instruments: str
    

class ReprProject(BaseProject):
    tags: list[Tags] | None = None
    links: list[Links] | None = None


class CreateProject(BaseProject):
    pass


class UpdateProject(BaseModel):
    name: str | None = None
    descriptions: str | None = None
    instruments: str | None = None


class DeleteProject(BaseModel):
    name: str
