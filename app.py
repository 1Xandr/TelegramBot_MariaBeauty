from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.executor import start_polling
from days import what_month, choice_day
from callback_button import first_choice, service_of_first_choice, choice_month, choice_time
from config import dp


@dp.message_handler(Command('help'))
async def choice(message: Message):
    await message.answer('Номера телефона Марии\n👉 <b>+380950988023</b>'
                                      '\n👉 <b>+4915158482594</b>', parse_mode='html')
    await message.answer_contact('380950988023', first_name='Мария', last_name='Гнатюк')


@dp.message_handler(Command('start')) # start bot
async def choice(message: Message):
    await message.answer(text='● Привет, Здесь вы можете записаться с Пн - Пт\n\n● Если вы сделали '
                              'ошибку при создании записи то напишите или нажмите сюда 👉 /start\n\n'
                              '● Если возникли проблемы то нажмите \nсюда 👉 /help')
    await message.answer(text='Выберите Опцию👇', reply_markup=first_choice)


@dp.callback_query_handler(text_contains='back:first')  # start bot
async def second_start(call: CallbackQuery):
    await call.message.edit_text(text='Выберите Опцию👇',)
    await call.message.edit_reply_markup(reply_markup=first_choice)


@dp.callback_query_handler(text_contains='depilation')  # if choose depilation
async def choice_of_depilation(call: CallbackQuery):
    await call.message.edit_text(text='Выбирите Зону👇')
    await call.message.edit_reply_markup(reply_markup=service_of_first_choice)


@dp.callback_query_handler(text_contains='service')
async def choice_of_month(call: CallbackQuery):
    await call.message.edit_text(text='Выбирите Месяц👇')
    await call.message.edit_reply_markup(reply_markup=choice_month)


@dp.callback_query_handler(text_contains='month')
async def choice_of_day(call: CallbackQuery):
    what_month(1 if call['data'] == 'month:next_month' else 0)  # send request to days.py
    await call.message.edit_text(text='Выбирите День👇')
    await call.message.edit_reply_markup(reply_markup=choice_day)


@dp.callback_query_handler(text_contains='day')
async def choice_of_day(call: CallbackQuery):
    await call.message.edit_text(text='Выбирите Время👇')
    await call.message.edit_reply_markup(reply_markup=choice_time)


@dp.message_handler()
async def random_message(message: Message):
    await message.answer('Я вас не поняла🧐\nДля вашего удобства были сделаны кнопки😌')


start_polling(dp)
