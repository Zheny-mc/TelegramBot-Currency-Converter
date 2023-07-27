from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tokens import bot_token


async def on_startup(_):
    print('Бот вышел в онлайн')

bot = Bot(token=bot_token())
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
