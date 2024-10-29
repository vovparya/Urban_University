'''
Домашнее задание по теме "Доработка бота"
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.
Цель: подготовить Telegram-бота для взаимодействия с базой данных.

Задача "Витамины для всех!":
Подготовка:
Подготовьте Telegram-бота из последнего домашнего задания 13 модуля сохранив код с ним в файл module_14_3.py.
Если вы не решали новые задания из предыдущего модуля рекомендуется выполнить их.

Дополните ранее написанный код для Telegram-бота:
Создайте и дополните клавиатуры:
В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
У всех кнопок назначьте callback_data="product_buying"
Создайте хэндлеры и функции к ним:
Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
Функция get_buying_list должна выводить надписи 'Название:
Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза.
После каждой надписи выводите картинки к продуктам. В конце выведите ранее
созданное Inline меню с надписью "Выберите продукт для покупки:".
Callback хэндлер, который реагирует на текст "product_buying" и оборачивает функцию send_confirm_message(call).
Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"
_________________________________________________________________________________________________________________
'''

import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from keyboards import *
import text

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(text.start, reply_markup=start_kb)


@dp.message_handler(text='О нас')
async def price(message):
    await message.answer(text.about, reply_markup=start_kb)


@dp.message_handler(text='Стоимость')
async def info(message):
    await message.answer('Что вас интересует?', reply_markup=catalog_kb)


@dp.callback_query_handler(text='medium')
async def buy_m(call):
    await call.message.answer(text.Mgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='big')
async def buy_l(call):
    await call.message.answer(text.Lgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='mega')
async def buy_xl(call):
    await call.message.answer(text.XLgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text='other')
async def buy_other(call):
    await call.message.answer(text.other, reply_markup=support_kb)
    await call.answer()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        product_description = f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}'
        # Получаем путь к директории со скриптом
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Формируем путь к картинке, предполагая, что она в папке "images"
        photo_path = os.path.join(script_dir, 'images', f'product{i}.png')

        try:
            photo = InputFile(photo_path)
            await message.answer_photo(photo=photo, caption=product_description)
        except FileNotFoundError:
            await message.answer(f'{product_description} (Картинка не найдена)')
    await message.answer('Выберите продукт для покупки:', reply_markup=product_list_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
