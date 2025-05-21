
from .schemes import UpdateAboutMe, DeleteLink
from .db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)

async def set_delete_links(link_enum):
    about_db = await AboutMe.find_one()
    link_enum = DeleteLink()
    for link in about_db.links:
        setattr(link_enum, link.name, "link.name")
    return link_enum