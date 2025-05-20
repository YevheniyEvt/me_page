import pprint
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from .models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)
from ..settings import config




