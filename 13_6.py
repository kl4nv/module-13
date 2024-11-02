from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

dp = Dispatcher(Bot(token='my_api'), storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)

inkb = InlineKeyboardMarkup()
inbutton1 = InlineKeyboardButton(text='🟰 Рассчитать норму калорий', callback_data='calories')
inbutton2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
inkb.add(inbutton1)
inkb.add(inbutton2)

malekb = InlineKeyboardMarkup()
mbutton = InlineKeyboardButton(text='Мужчина', callback_data='mcalories')
fbutton = InlineKeyboardButton(text='Женщина', callback_data='fcalories')
malekb.add(mbutton)
malekb.add(fbutton)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:',  reply_markup=inkb)

@dp.callback_query_handler(text='formulas')
async def get_gender_menu(call):
    await call.message.answer('Выберите свой пол', reply_markup=malekb)
    await call.answer()

@dp.callback_query_handler(text='mcalories')
async def get_m_folruma(call):
    await call.message.answer('10.0 * вес(кг) + 6.25 * рост(см) - 5.0 * возраст(г) + 5.0')
    await call.answer()

@dp.callback_query_handler(text='fcalories')
async def get_f_folrmula(call):
    await call.message.answer('10.0 * вес(кг) + 6.25 * рост(см) - 5.0 * возраст(г) - 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await call.answer()
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
        calories = 10.0 * data["weight"] + 6.25 * data["growth"] - 5.0 * data["age"] + 5.0
    if data['gender'] == 'Ж':
        calories = 10.0 * data["weight"] + 6.25 * data["growth"] - 5.0 * data['age'] - 161.0
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()

@dp.message_handler(commands=['start'])
async def starter(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler()
async def all_input(message):
    await message.answer('Для рассчета нормы калорий нажмите кнопку: Рассчитать')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)





