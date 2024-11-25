'''
Домашнее задание по теме "Использование БД в маршрутизации. 1.2"
Цель: закрепить навык управления записями в БД, используя SQLAlchemy и маршрутизацию FastAPI.

Задача "Маршрутизация заданий":
Необходимо описать логику функций в task.py используя ранее написанные маршруты FastAPI.
Делается практически идентично users.py с некоторыми дополнениями.
Напишите логику работы функций маршрутов аналогично предыдущему заданию:
В модуле task.py:
Функция all_tasks ('/') - идентично all_users.
Функция task_by_id ('/task_id') - идентично user_by_id (тоже по id)
Функция craete_task ('/create'):
Дополнительно принимает модель CreateTask и user_id.
Подставляет в таблицу Task запись значениями указанными в CreateUser и user_id, если пользователь найден.
Т.е. при создании записи Task вам необходимо связать её с конкретным пользователем User.
В конце возвращает словарь {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}
В случае отсутствия пользователя выбрасывает исключение с кодом 404 и описанием "User was not found"
Функция update_task ('/update') - идентично update_user.
Функция delete_task ('/delete') - идентично delete_user.
В модуле user.py:
Создайте новый маршрут get "/user_id/tasks" и функцию tasks_by_user_id. Логика этой функции должна заключатся в
возврате всех Task конкретного User по id.
Дополните функцию delete_user так, чтобы вместе с пользователем удалялись все записи связанные с ним.
Создайте, измените и удалите записи через интерфейс Swagger:
Создайте 4 записи Task для User с id=1 и id=3, по 2 на каждого в соответствии с порядком ниже:
title: FirstTask, SecondTask, ThirdTask, FourthTask
content: Content1, Content2, Content3, Content4
priority: 0, 2, 4, 6
user_id: 1, 1, 3, 3
Должны появится 4 записи следующего вида:

Удалите запись Task с id = 3.
Удалите запись User с id = 1. (должны удалиться записи связанные с этим пользователем)
Выведите все оставшиеся записи Task.
Пример результата выполнения программы:
После всех запросов, все Task в Swagger должны выглядеть так (1 запись удалилась, 2 удалились вместе с пользователем):


В таблице tasks должна остаться одна запись:
______________________________________________________________________________________________________
'''

from fastapi import FastAPI
from app.backend.db import engine
from app.backend.db import Base

from app.routers import user, task

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
async def read_root():
    return {"message": "Welcome to Taskmanager"}


app.include_router(user.router)
app.include_router(task.router)
