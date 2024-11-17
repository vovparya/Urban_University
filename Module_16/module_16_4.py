'''
Домашнее задание по теме "Модели данных Pydantic"
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.

Цель: научиться описывать и использовать Pydantic модель.

Задача "Модель пользователя":
Подготовка:
Используйте CRUD запросы из предыдущей задачи.
Создайте пустой список users = []
Создайте класс(модель) User, наследованный от BaseModel, который будет содержать следующие поля:
id - номер пользователя (int)
username - имя пользователя (str)
age - возраст пользователя (int)

Измените и дополните ранее описанные 4 CRUD запроса:
get запрос по маршруту '/users' теперь возвращает список users.
post запрос по маршруту '/user/{username}/{age}', теперь:
Добавляет в список users объект User.
id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
Все остальные параметры объекта User - переданные в функцию username и age соответственно.
В конце возвращает созданного пользователя.
put запрос по маршруту '/user/{user_id}/{username}/{age}' теперь:
Обновляет username и age пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
delete запрос по маршруту '/user/{user_id}', теперь:
Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
Выполните каждый из этих запросов по порядку. Ответы должны совпадать:
1. GET '/users'
[]
2. POST '/user/{username}/{age}' # username - UrbanUser, age - 24

3. POST '/user/{username}/{age}' # username - UrbanTest, age - 36

4. POST '/user/{username}/{age}' # username - Admin, age - 42

5. PUT '/user/{user_id}/{username}/{age}' # user_id - 1, username - UrbanProfi, age - 28

6. DELETE '/user/{user_id}' # user_id - 2

7. GET '/users'

8. DELETE '/user/{user_id}' # user_id - 2
________________________________________________________________________________________
'''

from typing import Annotated
from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Пустой список пользователей
users = []


# Pydantic-модель пользователя
class User(BaseModel):
    id: int  # Номер пользователя
    username: str  # Имя пользователя
    age: int  # Возраст пользователя


# GET запрос для получения списка пользователей
@app.get('/users')
def get_users():
    return users


# POST запрос для создания нового пользователя
@app.post('/user/{username}/{age}')
def create_user(
        username: Annotated[
            str,
            Path(title='Введите имя пользователя', min_length=1, max_length=20)
        ],
        age: Annotated[
            int,
            Path(title='Введите возраст', ge=0, le=120)
        ]
):
    # Генерация нового ID пользователя
    if users:
        new_id = users[-1].id + 1
    else:
        new_id = 1
    # Создание нового пользователя
    user = User(id=new_id, username=username, age=age)
    users.append(user)
    return user


# PUT запрос для обновления существующего пользователя
@app.put('/user/{user_id}/{username}/{age}')
def update_user(
        user_id: Annotated[
            int,
            Path(title='ID пользователя', ge=1)
        ],
        username: Annotated[
            str,
            Path(title='Новое имя пользователя', min_length=1, max_length=20)
        ],
        age: Annotated[
            int,
            Path(title='Новый возраст пользователя', ge=0, le=120)
        ]
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="User was not found")


# DELETE запрос для удаления пользователя
@app.delete('/user/{user_id}')
def delete_user(
        user_id: Annotated[
            int,
            Path(title='ID пользователя', ge=1)
        ]
):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    # Если пользователь не найден, выбрасываем исключение
    raise HTTPException(status_code=404, detail="User was not found")
