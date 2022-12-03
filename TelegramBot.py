from config import TelegramBotApi
from google_calendar import total
import telebot
from telebot import types

bot = telebot.TeleBot(TelegramBotApi)

client_description = []  # Which service
client_date = []  # Which date
client_name = []  # Name and phone of user
client_time = []  # Which time


# command Help
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Номера телефона Марии\n👉 <b>+380950988023</b>'
                                      '\n👉 <b>+4915158482594</b>',
                     parse_mode='html')
    bot.send_contact(message.chat.id, '380950988023', first_name='Мария', last_name='Гнатюк')


# command Start
@bot.message_handler(commands=['start'])
def start_message(message):
    client_description.clear()  # to clear list if user restart bot
    bot.send_message(message.chat.id, '● Привет, Здесь вы можете записаться с Пн - Пт\n\n● Если вы сделали '
                                      'ошибку при создании записи то напишите или нажмите сюда 👉 /start\n\n'
                                      '● Если возникли проблемы то нажмите \nсюда 👉 /help')
    markup = types.ReplyKeyboardMarkup(row_width=1)
    eyelashes = types.KeyboardButton('😽Реснички')  # first option of service
    depilation = types.KeyboardButton('👙Депиляция')  # second option
    markup.add(eyelashes, depilation)

    bot.send_message(message.chat.id, 'Выбирите услугу👇', reply_markup=markup)  # choose option


@bot.message_handler(content_types=['text'])
def choice_message(message):
    if message.text == '👙Депиляция':  # if choose first option
        client_description.append(message.text[1:])
        markup = types.ReplyKeyboardMarkup(row_width=1)
        # Service of first choose
        bikini = types.KeyboardButton('👙Бикини 30 евро, 20 мин')
        legs = types.KeyboardButton('🦵Ноги 45 евро, 40 мин')
        arms = types.KeyboardButton('💪Руки 20 евро, 15 мин')
        face = types.KeyboardButton('😌Лицо 10 евро, 10 мин')
        markup.add(face, legs, arms, bikini)
        bot.send_message(message.chat.id, 'Выбирите зону👇', reply_markup=markup)  # choose service

    elif message.text[-3::] == 'мин' or message.text == '😽Реснички':  # if choose second option
        if message.text[-3::] == 'мин':  # if message have service of first choose
            client_description.append(message.text[1:])
        else:
            client_description.append('Реснички')
        markup_mounth = types.ReplyKeyboardMarkup()
        for x in range(1, 13):  # cycle 'for' for mouth
            x = types.KeyboardButton(f'🗓{x} Месяц')
            markup_mounth.add(x)
        # choose mouth
        bot.send_message(message.chat.id, 'Выбирите месяц👇 (1 Месяц = Январь)', reply_markup=markup_mounth)

    elif message.text[-5:] == 'Месяц' or message.text == 'Назад ◀':  # if user chose mouth
        client_date.clear()  # to clear list if user restart bot
        if len(message.text[1:-6]) == 1:  # if mouth have only 1 symbol [3 -> 03]
            client_date.append(f'2022-0{message.text[1:-6]}-')
        else:
            client_date.append(f'2022-{message.text[1:-6]}-')  # if not
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for x in range(1, 32):
            x = types.KeyboardButton(str(x))
            markup.add(x)
        bot.send_message(message.chat.id, 'НАПИШИТЕ📝 день. Например 👉 05', reply_markup=markup)  # choose day

    elif len(message.text.strip()) <= 2:  # if user chose day
        client_date.append(f'{(message.text)}')  # for google calendar api
        from sql_file import get_empty_space
        markup = types.ReplyKeyboardMarkup()

        markup.add(types.KeyboardButton('Время на 14:00')) if get_empty_space(client_date)[0] == True else False
        markup.add(types.KeyboardButton('Время на 15:00')) if get_empty_space(client_date)[1] == True else False
        markup.add(types.KeyboardButton('Время на 16:00')) if get_empty_space(client_date)[2] == True else False
        markup.add(types.KeyboardButton('Назад ◀'))

        bot.send_message(message.chat.id, 'Выберите окно которое вам подходит😊', reply_markup=markup)

    elif message.text[:5] == 'Время':  # if yes
        time_chose = message.text[-5:]
        client_time.clear()  # if bot was restarted
        client_time.append(time_chose)
        client_date.append(f'T{time_chose}:00')
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        # create button to share user contact
        button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
        markup.add(button_phone)
        bot.send_message(message.chat.id, 'Предоставсте доступ к номер телефона📲', reply_markup=markup)

    elif message.text[0:3] == 'Нет':  # if no
        bot.send_message(message.chat.id, 'Тогда Напишите другой день😉')  # choose another day
        client_date.pop(-1)
    else:
        bot.send_message(message.chat.id, 'Я вас не поняла, если нужна помощь 👉 /help')


@bot.message_handler(content_types=['contact'])  # if user sent contact
def contact(message):
    from sql_file import update_data
    client_name.clear()  # to clear list if user restart bot
    client_name.append(message.contact.first_name)
    client_name.append(message.contact.last_name)
    client_name.append(message.contact.phone_number)
    bot.send_message(message.chat.id, 'Отлично, я вас записала🤩')  # I wrote you down
    total(client_date, client_description, client_name)  # send request to google calendar api
    update_data(client_time, client_date)  # send request to MySQL


bot.polling(True)

