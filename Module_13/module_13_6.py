'''
Домашнее задание по теме "Инлайн клавиатуры".
Цель: научится создавать Inline клавиатуры и кнопки на них в Telegram-bot.

Задача "Ещё больше выбора":
Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать' присылалась Inline-клавиатруа.
Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
С текстом 'Рассчитать норму калорий' и callback_data='calories'
С текстом 'Формулы расчёта' и callback_data='formulas'
Создайте новую функцию main_menu(message), которая:
Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'
Создайте новую функцию get_formulas(call), которая:
Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
Будет присылать сообщение с формулой Миффлина-Сан Жеора.
Измените функцию set_age и декоратор для неё:
Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.
По итогу получится следующий алгоритм:
Вводится команда /start
На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий' и 'Формулы расчёта'
По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний по цепочке.
__________________________________________________________________________________________________________
'''

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

API_KEY = '***********************************************'
bot = Bot(token=API_KEY)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Рассчитать'), KeyboardButton('Информация')
)

keyboard_inline = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories'),
    InlineKeyboardButton('Формулы расчёта', callback_data='formulas')
)

keyboard_gender = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton('Мужчина', callback_data='gender_male'),
    InlineKeyboardButton('Женщина', callback_data='gender_female')
)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот, помогающий твоему здоровью. 😊", reply_markup=keyboard_start)


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=keyboard_inline)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call: types.CallbackQuery):
    formula = "**Формула Миффлина-Сан Жеора:**\n" \
              "Для мужчин: (10 x вес в кг) + (6.25 x рост в см) - (5 x возраст в годах) + 5\n" \
              "Для женщин: (10 x вес в кг) + (6.25 x рост в см) - (5 x возраст в годах) - 161"
    await call.message.answer(formula)


@dp.callback_query_handler(text='calories')
async def ask_gender(call: types.CallbackQuery):
    await call.message.answer('Укажите ваш пол:', reply_markup=keyboard_gender)


@dp.callback_query_handler(lambda c: c.data.startswith('gender_'))
async def set_age(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'gender_male':
        gender = 1  # Мужчина
    else:
        gender = 2  # Женщина

    await state.update_data(gender=gender)
    await call.message.answer('Введите ваш возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError
        await state.update_data(age=age)
        await message.answer('Введите ваш рост (в сантиметрах):')
        await UserState.growth.set()
    except ValueError:
        await message.answer('Пожалуйста, введите корректный возраст (число больше нуля).')


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    try:
        growth = int(message.text)
        if growth <= 0:
            raise ValueError
        await state.update_data(growth=growth)
        await message.answer('Введите ваш вес (в килограммах):')
        await UserState.weight.set()
    except ValueError:
        await message.answer('Пожалуйста введите корректный рост (число больше нуля).')


@dp.message_handler(state=UserState.weight)
async def calculate_calories(message: types.Message, state: FSMContext):
    try:
        weight = int(message.text)
        if weight <= 0:
            raise ValueError

        data = await state.get_data()
        age, growth, gender = data['age'], data['growth'], data['gender']

        if gender == 1:  # Мужчина
            calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5
        else:  # Женщина
            calories = (10 * weight) + (6.25 * growth) - (5 * age) - 161

        await message.answer(f'Ваша норма калорий: {round(calories)} ккал')

    except ValueError:
        await message.answer('Пожалуйста, введите корректный вес (число больше нуля).')
    finally:
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
