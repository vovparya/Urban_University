'''
Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

Задача "Регистрация покупателей":
Подготовка:
Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.

Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
Эта таблица должна содержать следующие поля:
id - целое число, первичный ключ
username - текст (не пустой)
email - текст (не пустой)
age - целое число (не пустой)
balance - целое число (не пустой)
add_user(username, email, age), которая принимает: имя пользователя, почту и возраст. Данная функция должна добавлять
в таблицу Users вашей БД запись с переданными данными. Баланс у новых пользователей всегда равен 1000. Для добавления
записей в таблице используйте SQL запрос.
is_included(username) принимает имя пользователя и возвращает True, если такой пользователь есть в таблице Users, в
противном случае False. Для получения записей используйте SQL запрос.

Изменения в Telegram-бот:
Кнопки главного меню дополните кнопкой "Регистрация".
Напишите новый класс состояний RegistrationState с следующими объектами
класса State: username, email, age, balance(по умолчанию 1000).
Создайте цепочку изменений состояний RegistrationState.
Фукнции цепочки состояний RegistrationState:
sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода возраста в атрибут RegistrationState.username при помощи метода set.
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и
запрашивать новое состояние для RegistrationState.username.
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в
таблицу Users при помощи ранее написанной crud-функции add_user.
В конце завершать приём состояний при помощи метода finish().
Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода в чате Telegram-бота.
____________________________________________________________________________________________________________
'''

import logging
import os
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from crud_functions import initiate_db, get_all_products, add_some_products, is_included, add_user

from config import *
from keyboards import *
import text

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализируем базу данных и добавляем продукты один раз
initiate_db()
add_some_products()

# Загружаем продукты из базы данных
products = get_all_products()


# Состояния регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


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


# Регистрация пользователя
@dp.message_handler(text='Регистрация')
async def sign_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь с таким именем уже существует. Введите другое имя:")
        return  # Ожидаем новое имя пользователя

    await state.update_data(username=username)
    await message.answer("Введите свой email:")
    await RegistrationState.next()  # Переход к состоянию email


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.next()  # Переход к состоянию age


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = int(message.text)  # Проверка на число
    await state.update_data(age=age)
    user_data = await state.get_data()
    add_user(user_data['username'], user_data['email'], user_data['age'])
    await message.answer(f"Регистрация прошла успешно, {user_data['username']}!")
    await state.finish()  # Завершаем регистрацию


@dp.callback_query_handler(lambda call: call.data.startswith('product_buying_'))
async def send_confirm_message(call):
    # Обрабатываем покупку, извлекая product_id из callback_data
    product_id = int(call.data.split('_')[-1])
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
