import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, inline_keyboard, InlineKeyboardButton
from aiogram import executor
from aiogram.types import MenuButtonWebApp, WebAppInfo
import requests
from environs import Env
import environs


# Устанавливаем соединение с базой данных SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    tel_id INTEGER
                )''')
conn.commit()



# Инициализируем бота
API_TOKEN = '6962441711:AAEMJrXOVpvI0lr869o8axH2MDd7Fjdo_bs'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


w = 'https://ru.wikipedia.org/wiki/'


admin_id = 669738572

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id != admin_id:
        cursor.execute('SELECT tel_id FROM Users WHERE tel_id = ?', (int(message.from_user.id),))
        results = cursor.fetchall()
        if results == []:
            cursor.execute('INSERT INTO Users (tel_id) VALUES (?)',
                           (int(message.from_user.id),))
            conn.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Узнать про художника", "Узнать про картину"]
        keyboard.add(*buttons)
        await message.answer('Привет, это бот который поможет тебе получить годную инфу!', reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Рассылка рекламы"]
        keyboard.add(*buttons)
        await message.answer('Приветствуем админа', reply_markup=keyboard)


@dp.message_handler(text='Узнать про художника')
async def artist(message: types.Message):
    await message.answer('Пожалуйста, введите фамилию художника, информацию о котором хотите узнать')


@dp.message_handler(text='Узнать про художника')
async def artist(message: types.Message):
    await message.answer('Пожалуйста, введите название картины, информацию о которой хотите узнать')


@dp.message_handler(text='Рассылка рекламы')
async def artist(message: types.Message):
    await message.answer('Пришлите текст рекламы')



@dp.message_handler()
async def artist(message: types.Message):
    if message.from_user.id != admin_id:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Хочу инфу!", web_app=WebAppInfo(url=w+str(message.text))))
        # keyboard.add(types.InlineKeyboardButton(text="Second Button", web_app=WebAppInfo(url="/index1.html")))
        await message.answer('Для получения информации нажмите на кнопку под сообщением', reply_markup=keyboard)
    else:
        cursor.execute('SELECT tel_id FROM Users')
        results = cursor.fetchall()
        for i in results:
            await bot.send_message(i[0], message.text)
        await bot.send_message(admin_id, 'Все ок, реклама готова')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)