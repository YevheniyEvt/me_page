
from .db.models import (AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address)


async def create_about():
    descriptions = 'Привіт. Я Python-розробник початківець. Маю досвід роботи з Django, FastAPI, PostgreSQL Ubuntu, Docker. Люблю приймати нові виклики, вирішувати складні задачі. Наразі весь вільний час приділяю навчанню. Вивчаю python, алгоритми, нові інструменти для покращення своїх навичок програміста.'
    short_description = 'Наразі активно шукаю роботу, хочу долучитись до реальних проєктів та навчатись у досвідчених колег.'
    linkedin_url = 'https://www.linkedin.com/in/yevheniy-yevtushenko-660112319/'
    linkedin_link = Links(
        name='linkedin',
        url=linkedin_url
    )
    github_url = 'https://github.com/YevheniyEvt'
    github_link = Links(
        name='GitHub',
        url=github_url
    )
    address = Address(
        city='Київ',
        country='Україна'
    )
    about = AboutMe(
        first_name='Євгеній',
        second_name='Євтушенко',
        descriptions=descriptions,
        short_description=short_description,
        email = 'genya421@gmail.com',
        address=address,
        links=[linkedin_link, github_link]
    )
    return about

def check_first_name(user_first_name: str | None = None):
    if user_first_name == None:
        user_first_name = 'Євгеній'
    return user_first_name