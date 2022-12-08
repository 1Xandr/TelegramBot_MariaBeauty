from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_polling
from days import what_month, choice_day
from callback_button import option_choice, service_of_first_choice, choice_month, first_choice
from config import dp
from google_calendar import total
from sql_file import get_empty_space, update_data

client_description = []  # Which service
client_date = []  # Which date
client_name = []  # Name and phone of user
client_time = []  # Which time

@dp.message_handler(Command('help'))
async def help(message: Message):
    await message.answer('Номера телефона Марии\n👉 <b>+380950988023</b>\n👉 <b>+4915158482594</b>', parse_mode='html')
    await message.answer_contact('380950988023', first_name='Мария', last_name='Гнатюк')


@dp.message_handler(Command('start')) # start bot
async def start(message: Message):
    await message.answer(text='✷✷✷✷✷✷✷✷✷✷✷✷✷✷\n\n● Привет, Здесь вы можете записаться с Пн - Пт\n\n '
                              '● Если возникли проблемы то нажмите сюда 👉 /help\n\n✷✷✷✷✷✷✷✷✷✷✷✷✷✷')
    await message.answer(text='<b>💛 Выберите Действие👇</b>', parse_mode='html', reply_markup=first_choice)


@dp.callback_query_handler(text_contains='entry')  # choice option
async def work_with_entry(call: CallbackQuery):
    await call.message.edit_text(text='<b>🎀 Выберите Опцию👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=option_choice)


@dp.callback_query_handler(text_contains='depilation')  # choice depilation
async def choice_of_depilation(call: CallbackQuery):
    client_description.clear()  # if user restart bot
    client_description.append(call['data'])  # add 'service' to list for google calendar API

    await call.message.edit_text(text='<b>💚 Выбирите Зону👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=service_of_first_choice)


@dp.callback_query_handler(text_contains='service')  # choice month
async def choice_of_month(call: CallbackQuery):
    client_description.pop(-1) if len(client_description) == 2 else None  # if user restart bot
    # if user restart bot and after depilation chose service:eyelashes
    client_description.pop(0) if call['data'] == 'service:eyelashes' and len(client_description) != 0 else None
    client_description.append(call['data'])  # add 'service' to list for google calendar API

    await call.message.edit_text(text='<b>🗓️ Выбирите Месяц👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=choice_month)


@dp.callback_query_handler(text_contains='month')  # choice day
async def choice_of_day(call: CallbackQuery):
    what_month_number = what_month(1 if call['data'] == 'month:next_month' else 0)  # send request to days.py

    client_date.clear()  # if user bot
    client_date.append(what_month_number[1])  # append to list year '2023'| for google calendar API and SQL
    client_date.append(what_month_number[0])  # append to list month '01' | for google calendar API and SQL

    await call.message.edit_text(text='<b>📌 Выбирите День👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=choice_day)


@dp.callback_query_handler(text_contains='day')  # choice time
async def choice_of_time(call: CallbackQuery):
    # append to list day | 'day:25' -> '25' | 'day:3' -> '03' | for google calendar API and SQL
    client_date.append(call['data'][4:] if len(call['data'][4:]) == 2 else f"0{call['data'][4:]}")

    choice_time = InlineKeyboardMarkup()

    # create four button for time here because else there was Exeption
    choice_time.insert(InlineKeyboardButton(text='14:00', callback_data='time:14')) if get_empty_space(client_date)[0] else None
    choice_time.insert(InlineKeyboardButton(text='15:00', callback_data='time:15')) if get_empty_space(client_date)[1] else None
    choice_time.insert(InlineKeyboardButton(text='16:00', callback_data='time:16')) if get_empty_space(client_date)[2] else None
    choice_time.row(InlineKeyboardButton(text='⬅️Назад к выбору дня', callback_data="service:back"))

    await call.message.edit_text(text=f'<b>📍 Вы выбрали <U>{client_date[2]}</U> День\n⏳ Выбирите Время👇</b>', parse_mode='html')
    await call.message.edit_reply_markup(reply_markup=choice_time)


@dp.callback_query_handler(text_contains='time')  # send contact
async def get_contact(call: CallbackQuery):
    client_time.clear()  # if user restart bot
    client_time.append(call['data'][5:])  # append to list '16' | 'time:16' -> 16 | for google calendar API and SQL

    update_data(client_time, client_date)  # send request to SQL

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text="📱 Отправить номер телефона👇", request_contact=True))

    await call.message.delete_reply_markup()
    await call.message.delete()
    await call.message.answer("📲 Отправь свой контакт✅", reply_markup=keyboard)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_user_data(message: Message):
    client_name.clear()  # if user restart bot
    client_name.append(message['contact']['first_name'])  # append to list name | for google calendar API
    client_name.append(message['contact']['phone_number'])  # append to list phone number | for google calendar API

    total(client_name, client_description, client_date, client_time)  # send request for google calendar API
    await message.answer(text='<b>✅ Отлично, я вас записала🤩</b>', parse_mode='html')


@dp.message_handler()  # for message which bot did not understand
async def catch_random_message(message: Message):
    await message.answer('<b>Я вас не поняла🧐\n💜 Для вашего удобства были сделаны кнопки😌</b>', parse_mode='html')


start_polling(dp)
