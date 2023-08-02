from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard = InlineKeyboardMarkup(row_width=2)
btn_usd_eur = InlineKeyboardButton(text='USD/EUR', callback_data='USD/EUR')
btn_eur_usd = InlineKeyboardButton(text='EUR/USD', callback_data='EUR/USD')
btn_usd_cny = InlineKeyboardButton(text='USD/CNY', callback_data='USD/CNY')
btn_other = InlineKeyboardButton(text='другие', callback_data='другие')

keyboard.add(btn_usd_eur, btn_eur_usd, btn_usd_cny, btn_other)