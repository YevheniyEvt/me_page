from pydantic import BaseModel, HttpUrl, EmailStr

from beanie import Document, Link


class Links(BaseModel):
    name: str
    url: HttpUrl


class Tags(BaseModel):
    name: str
    description: str


class Projects(Document):
    name: str
    descriptions: str
    instruments: str
    tags: list[Tags] | None = None
    links: list[Links] | None = None

    class Settings:
        use_state_management = True


class Address(BaseModel):
    city: str
    country: str


class AboutMe(Document):
    first_name:str
    second_name: str
    descriptions: str
    short_description: str
    email: EmailStr
    address: Address | None = None
    links: list[Links] | None = None
    projects: list[Link[Projects]] | None = None

    class Settings:
        use_state_management = True




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

    class Settings:
        use_state_management = True


class WorkFlow(BaseModel):
    name: str


class Skills(Document):
    workflows: list[WorkFlow]
    instrument: str

    class Settings:
        use_state_management = True


class Hobbies(Document):
    descriptions: str

    class Settings:
        use_state_management = True
