'''
Домашнее задание по теме "Методы отправки сообщений".
Цель: написать простейшего телеграм-бота, используя асинхронные функции.

Задача "Он мне ответил!":
Измените функции start и all_messages так, чтобы вместо вывода в консоль строки отправлялись в чате телеграм.
Запустите ваш Telegram-бот и проверьте его на работоспособность.
Пример результата выполнения программы:

Примечания:
Для ответа на сообщение запускайте метод answer асинхронно.
_________________________________________________________________________________________________
'''

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

API_KEY = '***********************************************'
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["Urban", "ff"])
async def urban_message(message: types.Message):
    print(f'Urban message')
    await message.answer('Urban message!')


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler()
async def all_massages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
