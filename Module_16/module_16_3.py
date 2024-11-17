'''
Домашнее задание по теме "CRUD Запросы: Get, Post, Put Delete."
Цель: выработать навык работы с CRUD запросами.

Задача "Имитация работы с БД":
Создайте новое приложение FastAPI и сделайте CRUD запросы.
Создайте словарь users = {'1': 'Имя: Example, возраст: 18'}
Реализуйте 4 CRUD запроса:
get запрос по маршруту '/users', который возвращает словарь users.
post запрос по маршруту '/user/{username}/{age}', который добавляет в словарь по максимальному по значению ключом
значение строки "Имя: {username}, возраст: {age}". И возвращает строку "User <user_id> is registered".
put запрос по маршруту '/user/{user_id}/{username}/{age}', который обновляет значение из словаря users под ключом
user_id на строку "Имя: {username}, возраст: {age}". И возвращает строку "The user <user_id> is updated"
delete запрос по маршруту '/user/{user_id}', который удаляет из словаря users по ключу user_id пару.
Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
1. GET '/users'
{
"1": "Имя: Example, возраст: 18"
}
2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24
"User 2 is registered"
3. POST '/user/{username}/{age}' # username - NewUser, age - 22
"User 3 is registered"
4. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28
"User 1 has been updated"
5. DELETE '/user/{user_id}' # user_id - 2
"User 2 has been deleted"
6. GET '/users'
{
"1": "Имя: UrbanProfi, возраст: 28",
"3": "Имя: NewUser, возраст: 22"
}

Примечания:
Не забудьте написать валидацию для каждого запроса, аналогично предыдущему заданию.
_________________________________________________________________________________________________________
'''

from typing import Annotated
from fastapi import FastAPI, Path, HTTPException

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}


@app.get('/users')
def get_users():
    return users


@app.post('/user/{username}/{age}')
def create_user(
        username: Annotated[
            str,
            Path(title='Введите имя пользователя', min_length=5, max_length=20, example='UrbanUser')
        ],
        age: Annotated[
            int,
            Path(title='Введите возраст', ge=18, le=120, example=24)
        ]
):
    # Определяем новый user_id как максимум существующих ключей + 1
    max_id = max(map(int, users.keys()))
    new_user_id = str(max_id + 1)
    # Добавляем нового пользователя в словарь
    users[new_user_id] = f"Имя: {username}, возраст: {age}"
    return f"User {new_user_id} is registered"


@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: Annotated[
            str,
            Path(title='Введите ID пользователя', example='1')
        ],
        username: Annotated[
            str,
            Path(title='Введите имя пользователя', min_length=5, max_length=20, example='UrbanProfi')
        ],
        age: Annotated[
            int,
            Path(title='Введите возраст', ge=18, le=120, example=28)
        ]
):
    if user_id in users:
        users[user_id] = f"Имя: {username}, возраст: {age}"
        return f"The user {user_id} is updated"

    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")


@app.delete('/user/{user_id}')
def delete_user(
        user_id: Annotated[
            str,
            Path(title='Введите ID пользователя', example='2')
        ]
):
    if user_id in users:
        del users[user_id]
        return f"User {user_id} has been deleted"
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
