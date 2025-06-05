from beanie import Document, Link, BeanieObjectId
from pydantic import BaseModel, EmailStr, HttpUrl
from .db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags, Course, Lection, Book)


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
    tags: list[Tags] | list = []
    links: list[Links] | list = []


class CreateProject(BaseProject):
    pass


class UpdateProject(BaseModel):
    name: str | None = None
    descriptions: str | None = None
    instruments: str | None = None


class DeleteProject(BaseModel):
    name: str

class ReprEducation(BaseModel):
    id: BeanieObjectId
    descriptions: str
    courses: list[Course] | None = []
    lections: list[Lection] | None = []
    books: list[Book] | None = []

class CreateEducation(BaseModel):
    descriptions: str


class BaseUser(BaseModel):
    username: str

class CreateUser(BaseUser):
    pass

class ReprUser(BaseUser):
    pass

class GetUser(BaseModel):
    username: str | None = None