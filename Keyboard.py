from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


# Keyboard первоначальная, главная
button1 = KeyboardButton('Рандомное число')
button2 = KeyboardButton('Погода')
button3 = KeyboardButton('Криптовалюта')

hello_kb = ReplyKeyboardMarkup(resize_keyboard=True)
hello_kb.add(button1, button2, button3)

# Keyboard криптовалюта - кнопки под текстом
Bitcoin_but = InlineKeyboardButton(text = 'Bitcoin', callback_data = 'cc_bitcoin')
Litecoin_but = InlineKeyboardButton(text = 'Litecoin', callback_data = 'cc_litecoin')
Dogecoin_but = InlineKeyboardButton(text = 'Dogecoin', callback_data = 'cc_dogecoin')

crupto_lss = InlineKeyboardMarkup(row_width=3)
crupto_lss.add(Bitcoin_but, Litecoin_but, Dogecoin_but)