from typing import Union, TypeVar

from fastapi import  HTTPException, status

from .db.models import (User, AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags, Course, Lection, Book)


async def create_about_evgeniy():
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


async def get_user(user_first_name: str | None = None):
    if user_first_name == None:
        user_first_name = 'Євгеній'

    user = await User.find_one(User.username == user_first_name,
                         fetch_links=True
                         )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with name {user_first_name} does not exist"
                            )
    return user

T = TypeVar('T', Links, Address, Tags, Course, Lection, Book)

async def get_updated_data(data: list[T], data_name: str)->list[T]:
    updated_data = [value for value in data if value.name != data_name]
    if len(updated_data) == len(data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Data with name {data_name} does not exist"
        )
    else:
        return updated_data
    
async def update_data(data: Union[list[Links], list[Address],
                                  list[Tags], list[Course],
                                  list[Lection], list[Book]],
                new_data: Links | Address | Tags | Course | Lection | Book | None,
                data_name: str | None,
                object_to_save: User | AboutMe | Projects | Education | Skills | Hobbies | None = None,
                ):
    if data_name is None:
        data_name = new_data.name
    data_get = (data_db for data_db in data if data_db.name == data_name)
    try:
        data_db = next(data_get)
    except StopIteration:
        data.append(new_data)
        await object_to_save.save()
    else:
        new_data_items = new_data.model_dump(exclude_none=True).items()
        for key, value in new_data_items:
            setattr(data_db, key, value)
        if object_to_save is None:
            object_to_save = data_db
        await object_to_save.save()