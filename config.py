from aiogram import Dispatcher, Bot

# for MySql
host = "127.0.0.1"
user = "root"
password = "root"
db_name = "telegramBotBase"

# for telegramBot
TelegramBotApi = '5976741272:AAFVnAbePUEmCvDK0uG_1RcPbdi15ss6Y04'
bot = Bot(token=TelegramBotApi)
dp = Dispatcher(bot)
