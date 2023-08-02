from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tokens import bot_token

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import keyboard

from currency_converter import CurrencyConverter

async def on_startup(_):
    print('Бот вышел в онлайн')

convert = CurrencyConverter()
storage = MemoryStorage()
bot = Bot(token=bot_token())
dp = Dispatcher(bot, storage=storage)

amount = 0
class FSMAdmin(StatesGroup):
    summa = State()
    f_curr = State()
    s_curr = State()
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer('Привет, я могу перевести из одной валюты в другую. Например, Eвро / Доллар. Для этого введите команду /convert.')

@dp.message_handler(commands=['convert'])
async def convert_command(message: types.Message):
    await message.answer('введи сумму:')
    await FSMAdmin.summa.set()

@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отмена ввода')

@dp.message_handler(state=FSMAdmin.summa)
async def summa_state(message: types.Message, state: FSMContext):
    global amount
    try:
        amount = int(message.text.strip())
        if amount > 0:
            await message.answer(f'Выбери пару валют', reply_markup=keyboard)
            await state.finish()
        else:
            raise ValueError('Число должно быть больше 0.')
    except ValueError:
        await message.reply('Неверный формат. Введи сумму!')
        await FSMAdmin.summa.set()

@dp.callback_query_handler(Text(equals='другие'))
async def other_callback(call_message: types.CallbackQuery):
    await FSMAdmin.f_curr.set()
    await bot.send_message(call_message.message.chat.id, 'Введи первую валюту:')
    await call_message.answer()

@dp.message_handler(state=FSMAdmin.f_curr)
async def f_curr_state(message: types.Message, state: FSMContext):
    await message.reply('Теперь введи вторую валюту')
    await FSMAdmin.s_curr.set()

@dp.message_handler(state=FSMAdmin.s_curr)
async def s_curr_state(message: types.Message, state: FSMContext):
    await message.reply('Happy end!')
    await state.finish()


@dp.callback_query_handler(lambda x: True)
async def callback(call: types.CallbackQuery):
    value = call.data.split('/')
    await bot.send_message(call.message.chat.id, value)
    await call.answer()

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
