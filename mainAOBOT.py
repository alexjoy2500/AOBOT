# Машина состояний
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from BOT.TEST.config import TOKEN, TOKEN_OWM # Импорт токенов Бота и Погоды

# Рандом
import random

# Погода
from pyowm import OWM
from pyowm.utils.config import get_default_config

from BOT.AOSHELL import COIN as co, Keyboard as navi
from BOT.AOSHELL.classBOT import PogodaLife

import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='HTML') # TOKEN можно получить у бота BotFather
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Погодный бот
config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM(TOKEN_OWM, config_dict) # Получение Токена Погоды
mgr = owm.weather_manager()

@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await message.answer(
        '☺️<b>Хей... Привет, {0.first_name}!</b> \n\nСпасибо, что используешь моего учебного бота...'.format(
            message.from_user))
    await message.answer(
        'Этот бот пока умеет: '

        '\n\n1. Предсказывать прогноз погоды'
        '\n2. Выдавать рандомное число'
        '\n3. Выдавать курс криптовалют'
        '\n4. Выдавать курс валюты <i>(скоро)</i>'
        '\n5. Отправлять обновления сайта новостей <i>(скоро)</i>'
    )  # <i>(скоро)</i> - делает слово курсиром, <b>(скоро)</b> - делает слово жирным.

    # Отправка Стикера
    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker=r"CAACAgIAAxkBAAEFdj9i61uIxC76WmGQ2SzberOQwqhyJAACuwADMNSdEYqvQODiIDzJKQQ",
                           reply_markup=navi.hello_kb)


@dp.message_handler(commands=['weather'])  # Вызываем при помощи команды /weather
async def PogoLife_1(message: types.Message):
    await message.answer('Введите город:')
    await PogodaLife.weath.set()  # Получаем сообщения от юзера


@dp.message_handler(state=PogodaLife.weath)
async def PogoLife_2(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()  # Собираем все данные введенные юзером

    fok = message.text  # Передал сообщение, чтобы смог определить прогноз погоды

    observation = mgr.weather_at_place(fok)
    w = observation.weather

    celsius = round(w.temperature('celsius')['temp'])
    celsius_max = round(w.temperature('celsius')['temp_max'])
    celsius_min = round(w.temperature('celsius')['temp_min'])

    status = w.detailed_status
    speed = w.wind()['speed']

    rm = f'Город: {fok}\n\n'

    rm += f'Сейчас в городе {celsius}°C\n'
    rm += f'Состояние погоды: {status}\n\n'
    rm += f'Макс. температура {celsius_max}°C\n' \
          f'Мин. температура {celsius_min}°C\n'
    rm += f'Ветер: {speed} м/с \n\n'

    if int(celsius) < 10 and int(celsius) == 0:
        rm += '😪Одевайся потеплее, иначе замерзнишь!'
    elif int(celsius) >= 10 and int(celsius) < 24:
        rm += '😌Уже теплее, оденься немного легче!'
    elif int(celsius) >= 24:
        rm += '🥵Уф.. На улице жарковато, одевайся легко!'
    elif int(celsius) < 0:
        rm += '🥶Охх.. Какая холодрыга... Быстро оделся, а то последние яйца отморозишь!'

    await message.answer(rm)

    await state.finish()  # Заканчиваем машину


@dp.message_handler()
async def get(message: types.Message):
    if message.text == 'Погода':
        await message.answer('Нажмите /weather')

    elif message.text == 'Рандомное число':
        await message.answer(str(random.randint(1, 100)))

    elif message.text == 'Криптовалюта':
        await message.answer('Выберите криптовалюту', reply_markup=navi.crupto_lss)

    else:
        await message.answer('Я ничего не поняль')
        await bot.send_sticker(chat_id=message.from_user.id,
                               sticker=r"CAACAgIAAxkBAAEFeRFi7NowPCM1Bnr1ehZLbAtsDXQjzgAC0QADMNSdEfxR6nTYGt87KQQ")


@dp.callback_query_handler(text_contains = "cc_")
async def crupto(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    callback_data = call.data
    currency = str(callback_data[3:])  # Получаю крипту
    result = co.cg.get_price(ids=currency, vs_currencies='usd') # Обрабатываю
    await bot.send_message(call.from_user.id, f'Криптовалюта <b>{currency}</b>\nСтоимость в настоящий момент {result[currency]["usd"]}$',reply_markup=navi.crupto_lss)


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
