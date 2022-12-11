from aiogram import Dispatcher, Bot

# for MySql
host = "127.0.0.1"
user = "root"
password = "root"
db_name = "telegramBotBase"

# for telegramBot
TelegramBotApi = '5976741272:AAECCqEfZgDUcSynEjGTEudzeo9KbKYgnfQ'
bot = Bot(token=TelegramBotApi)
dp = Dispatcher(bot)
