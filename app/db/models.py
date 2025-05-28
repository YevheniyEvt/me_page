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
    tags: list[Tags] | None = []
    links: list[Links] | None = []

    class Settings:
        use_state_management = True


class Address(BaseModel):
    city: str | None = None
    country: str | None = None


class AboutMe(Document):
    first_name:str
    second_name: str
    descriptions: str
    short_description: str
    email: EmailStr
    address: Address | None = None
    links: list[Links] | None = []


    class Settings:
        use_state_management = True


class Course(BaseModel):
    name: str
    descriptions: str


class Lection(BaseModel):
    name: str
    descriptions: str


class Book(BaseModel):
    name: str
    author: str
    
    
class Education(Document):
    descriptions: str
    courses: list[Course] | None = []
    lections: list[Lection] | None = []
    books: list[Book] | None = []

    class Settings:
        use_state_management = True


class WorkFlow(BaseModel):
    name: str

class Instrument(BaseModel):
    name: str

class Skills(Document):
    workflows: list[WorkFlow] | None = []
    instruments: list[Instrument] | None = []

    class Settings:
        use_state_management = True


class Hobbies(Document):
    descriptions: str

    class Settings:
        use_state_management = True


class User(Document):
    username: str
    about: AboutMe | None = None
    projects: list[Link[Projects]] | None = None
    education: Link[Education] | None = None
    skills: Link[Skills] | None = None
    hobbies: Link[Hobbies] | None = None

    class Settings:
        use_state_management = True
