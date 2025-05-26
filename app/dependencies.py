from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException, status

from .db.models import (User, AboutMe, Projects, Education, Skills, Hobbies,
                     Links, Address, Tags, Course, Lection, Book)


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

def get_user(user_first_name: str | None = None):
    if user_first_name == None:
        user_first_name = 'Євгеній'
    user = User.find_one(User.about.first_name == user_first_name,
                         fetch_links=True
                         )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with name {user_first_name} does not exist"
                            )
    return user


async def get_updated_data(data: Union[list[Links], list[Address],
                                  list[Tags], list[Course],
                                  list[Lection], list[Book]],
                                  data_name: str
                                  )->Union[list[Links], list[Address],
                                  list[Tags], list[Course],
                                  list[Lection], list[Book]]:
    updated_data = [value for value in data if value.name != data_name]
    if len(updated_data) == len(data):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{data.__name__} with name {data_name} does not exist"
        )
    else:
        return updated_data
    
async def update_data(data: Union[list[Links], list[Address],
                                  list[Tags], list[Course],
                                  list[Lection], list[Book]],
                new_data: Union[Links, Address, Tags, Course, Lection, Book],
                object_to_save: Union[User, AboutMe, Projects, Education, Skills, Hobbies],
                data_name: str,
                ):
    data_get = (data_db for data_db in data if data_db.name == data_name)
    try:
        data_db = next(data_get)
        for key, value in new_data.model_dump(exclude_none=True).items():
            setattr(data_db, key, value)
        await data_db.save_changes()
    except StopIteration:
        data.append(new_data)
        await object_to_save.save_changes()