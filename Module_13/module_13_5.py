'''
Домашнее задание по теме "Клавиатура кнопок".
Цель: научится создавать клавиатуры и кнопки на них в Telegram-bot.

Задача "Меньше текста, больше кликов":
Необходимо дополнить код предыдущей задачи, чтобы вопросы о параметрах тела
для расчёта калорий выдавались по нажатию кнопки.
Измените massage_handler для функции set_age. Теперь этот хэндлер будет
реагировать на текст 'Рассчитать', а не на 'Calories'.
Создайте клавиатуру ReplyKeyboardMarkup и 2 кнопки KeyboardButton на ней со следующим текстом: 'Рассчитать' и
'Информация'. Сделайте так, чтобы клавиатура подстраивалась под размеры
интерфейса устройства при помощи параметра resize_keyboard.
Используйте ранее созданную клавиатуру в ответе функции start, используя параметр reply_markup.
В итоге при команде /start у вас должна присылаться клавиатура с двумя кнопками. При нажатии на кнопку с надписью
'Рассчитать' срабатывает функция set_age с которой начинается работа машины состояний для age, growth и weight.
____________________________________________________________________________________________________________________
'''

# Раз уже начал с предыдущих заданий, чуть усложнять себе задачу, придется экспериментировать.

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

API_KEY = '***********************************************'
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard_calc = KeyboardButton('Рассчитать')
keyboard_info = KeyboardButton('Информация')
keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True).add(keyboard_calc, keyboard_info)

keyboard_male = KeyboardButton('Мужчина')
keyboard_female = KeyboardButton('Женщина')
keyboard_gender = ReplyKeyboardMarkup(resize_keyboard=True).add(keyboard_male, keyboard_female)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=keyboard_start)


@dp.message_handler(text='Рассчитать')
async def set_gender(message: types.Message):
    await message.answer('Укажи свой пол:', reply_markup=keyboard_gender)


@dp.message_handler(lambda message: message.text in ['Мужчина', 'Женщина'])
async def set_age(message: types.Message, state: FSMContext):
    if message.text == 'Мужчина':
        gender = 1
    else:
        gender = 2

    await state.update_data(gender=gender)
    await message.answer('Введите свой возраст:', reply_markup=types.ReplyKeyboardRemove())
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост (в сантиметрах):')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес (в килограммах):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()

    # Формула Миффлина - Сан Жеора
    if data['gender'] == 1:  # Мужчина
        calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
    else:  # Женщина
        calories = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] - 161

    await message.answer(f'Ваша норма калорий: {int(calories)} ккал')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
