'''
Домашнее задание по теме "План написания админ панели"
Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

Задача "Продуктовая база":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните ранее написанный код для Telegram-бота:
Создайте файл crud_functions.py и напишите там следующие функции:
initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
title(название продукта) - текст (не пустой)
description(описание) - текст
price(цена) - целое число (не пустой)
get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.

Изменения в Telegram-бот:
В самом начале запускайте ранее написанную функцию get_all_products.
Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов функцию
get_all_products. Полученные записи используйте в выводимой
надписи: "Название: <title> | Описание: <description> | Цена: <price>"
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.

Пример результата выполнения программы:
Добавленные записи в таблицу Product и их отображение в Telegram-bot:

Примечания:
Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)
____________________________________________________________________________________________________________
'''

import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton

from config import *
from keyboards import *
from crud_functions import initiate_db, get_all_products, add_some_products
import text

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализируем базу данных и добавляем продукты один раз
initiate_db()
add_some_products()

# Загружаем продукты из базы данных
products = get_all_products()


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
    global products  # Объявляем products как глобальную переменную
    for product in products:
        product_description = f"Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        photo_path = os.path.join(script_dir, 'images', f'{product[1]}.png')

        try:
            photo = InputFile(photo_path)
            await message.answer_photo(photo=photo, caption=product_description)
        except FileNotFoundError:
            await message.answer(f'{product_description} (Картинка не найдена)')

    # Создаём клавиатуру динамически
    product_list_kb = InlineKeyboardMarkup()
    for product in products:
        product_button = InlineKeyboardButton(text=product[1], callback_data=f'product_buying_{product[0]}')
        product_list_kb.add(product_button)

    await message.answer('Выберите продукт для покупки:', reply_markup=product_list_kb)


@dp.callback_query_handler(lambda call: call.data.startswith('product_buying_'))
async def send_confirm_message(call):
    # Обрабатываем покупку, извлекая product_id из callback_data
    product_id = int(call.data.split('_')[-1])
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
