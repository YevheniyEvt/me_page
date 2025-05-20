from pydantic import BaseModel, HttpUrl, EmailStr

from beanie import Document

class Links(BaseModel):
    name: str
    url: HttpUrl

class Address(BaseModel):
    city: str
    country: str

class AboutMe(Document):
    first_name:str
    second_name: str
    descriptions: str
    short_description: str
    email: EmailStr
    address: Address
    links: list[Links]


class Tags(BaseModel):
    name: str
    description: str

class Projects(Document):
    name: str
    descriptions: str
    tags: Tags
    instruments: str
    links: list[Links]


class Course(BaseModel):
    name: str
    descriptions: str

class Lection(BaseModel):
    name: str
    descriptions: str

class Book(BaseModel):
    author: str
    book_name: str

class Education(Document):
    descriptions: str
    courses: list[Course]
    lections: list[Lection]
    books: list[Book]


class WorkFlow(BaseModel):
    name: str

class Skills(Document):
    workflows: list[WorkFlow]
    instrument: str


class Hobbies(Document):
    descriptions: str

