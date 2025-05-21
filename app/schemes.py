from enum import Enum

from pydantic import BaseModel, EmailStr, HttpUrl
from .db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)


class UpdateAboutMe(BaseModel):
    first_name: str | None = None
    second_name: str | None = None
    descriptions: str | None = None
    short_description: str | None = None
    email: EmailStr | None = None

class DeleteLink(str, Enum):
    link = 'link'