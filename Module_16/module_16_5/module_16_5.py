'''
Домашнее задание по теме "Шаблонизатор Jinja 2."
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.

Цель: научиться взаимодействовать с шаблонами Jinja 2 и использовать их в запросах.

Задача "Список пользователей в шаблоне":
Подготовка:
Используйте код из предыдущей задачи.
Скачайте заготовленные шаблоны для их дополнения.
Шаблоны оставьте в папке templates у себя в проекте.
Создайте объект Jinja2Templates, указав в качестве папки шаблонов - templates.
Измените и дополните ранее описанные CRUD запросы:
Напишите новый запрос по маршруту '/':
Функция по этому запросу должна принимать аргумент request и возвращать TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и
список users. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
Измените get запрос по маршруту '/user' на '/user/{user_id}':
Функция по этому запросу теперь принимает аргумент request и user_id.
Вместо возврата объекта модели User, теперь возвращается объект TemplateResponse.
TemplateResponse должен подключать ранее заготовленный шаблон 'users.html', а также передавать в него request и
одного из пользователей - user. Ключи в словаре для передачи определите самостоятельно в соответствии с шаблоном.
Создайте несколько пользователей при помощи post запроса со следующими данными:
username - UrbanUser, age - 24
username - UrbanTest, age - 22
username - Capybara, age - 60
В шаблоне 'users.html' заготовлены все необходимые теги и обработка условий, вам остаётся только дополнить
закомментированные строки вашим Jinja 2 кодом (использование полей id, username и age объектов модели User):
1. По маршруту '/' должен отображаться шаблон 'users.html' со списком все ранее созданных объектов:

2. Здесь каждая из записей является ссылкой на описание объекта,
информация о котором отображается по маршруту '/user/{user_id}':
_______________________________________________________________________________________________________________
'''

from typing import List
from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

# Создаем объект Jinja2Templates, указав папку с шаблонами
templates = Jinja2Templates(directory="templates")

# Список пользователей
users: List['User'] = []


# Pydantic-модель пользователя
class User(BaseModel):
    id: int
    username: str
    age: int


# Маршрут для отображения списка пользователей
@app.get('/', response_class=HTMLResponse)
def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


# Маршрут для отображения информации о конкретном пользователе
@app.get('/user/{user_id}', response_class=HTMLResponse)
def read_user(
        request: Request,
        user_id: int = Path(..., title="ID пользователя", ge=1)
):
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": user})
    raise HTTPException(status_code=404, detail="User was not found")


# POST запрос для создания нового пользователя
@app.post('/user/{username}/{age}')
def create_user(
        username: str = Path(..., title='Имя пользователя', min_length=1, max_length=20),
        age: int = Path(..., title='Возраст пользователя', ge=0, le=120)
):
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    user = User(id=new_id, username=username, age=age)
    users.append(user)
    return user


# PUT запрос для обновления существующего пользователя
@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: int = Path(..., title='ID пользователя', ge=1),
        username: str = Path(..., title='Новое имя пользователя', min_length=1, max_length=20),
        age: int = Path(..., title='Новый возраст пользователя', ge=0, le=120)
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


# DELETE запрос для удаления пользователя
@app.delete('/user/{user_id}')
def delete_user(
        user_id: int = Path(..., title='ID пользователя', ge=1)
):
    for index, user in enumerate(users):
        if user.id == user_id:
            return users.pop(index)
    raise HTTPException(status_code=404, detail="User was not found")
