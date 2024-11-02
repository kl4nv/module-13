from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

dp = Dispatcher(Bot(token='my_api'), storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=float(message.text))
    await message.answer('Введите свой рост (см)')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=float(message.text))
    await message.answer('Введите свой вес (кг)')
    await UserState.weight.set()

#Дополним функцией для выбора пола, что бы рассчитать точнее калории
@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=float(message.text))
    await message.answer('Введите свой пол (М или Ж)')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_colories(message, state):
    await state.update_data(gender=message.text.upper())
    data = await state.get_data()
    if data['gender'] == 'М':
        colories = 10.0 * data["weight"] + 6.25 * data["growth"] - 5.0 * data["age"] + 5.0
    if data['gender'] == 'Ж':
        colories = 10.0 * data["weight"] + 6.25 * data["growth"] - 5.0 * data['age'] - 161.0
    await message.answer(f'Ваша норма калорий: {colories}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def starter(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler()
async def all_input(message):
    await message.answer('Для рассчета нормы калорий введите или нажмите кнопку: Рассчитать')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





