from google_calendar import total
import telebot
from telebot import types

bot = telebot.TeleBot('5976741272:AAE07_pL6jOB62Xv8tOZh-yO7lHRnnnZknU')

client_description = []  # which service
client_time = []  # which date
client_name = []  # Name and phone of user


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

    elif message.text[-5:] == 'Месяц':  # if user chose mouth
        client_time.clear()  # to clear list if user restart bot
        # if len(message.text[1:-6]) == 1:  # if mouth have only 1 symbol [3 -> 03]
        #     client_time.append(f'2022-0{message.text[1:-6]}-')
        # else:
        #     client_time.append(f'2022-{message.text[1:-6]}-')  # if not
        client_time.append(f'2022-{message.text[1:-6]}-')
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for x in range(1, 32):
            x = types.KeyboardButton(str(x))
            markup.add(x)
        bot.send_message(message.chat.id, 'НАПИШИТЕ📝 день. Например 👉 05', reply_markup=markup)  # choose day

    elif len(message.text.strip()) <= 2:  # if user chose day
        client_time.append(f'{(message.text)}T14:00:00')  # for google calendar api
        markup = types.ReplyKeyboardMarkup()
        yes = types.KeyboardButton('Да мне подходит ✅')
        no = types.KeyboardButton('Нет я хочу выбрать другой день ❎')
        markup.add(yes, no)
        bot.send_message(message.chat.id, 'В этот день есть окно на 14:00, вам подходит🤔?', reply_markup=markup)

    elif message.text[0:2] == 'Да':  # if yes
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        # create button to share user contact
        button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)
        markup.add(button_phone)
        bot.send_message(message.chat.id, 'Предоставсте доступ к номер телефона📲', reply_markup=markup)

    elif message.text[0:3] == 'Нет':  # if no
        bot.send_message(message.chat.id, 'Тогда Напишите другой день😉')  # choose another day
        client_time.pop(-1)
    else:
        bot.send_message(message.chat.id, 'Я вас не поняла, если нужна помощь 👉 /help')


@bot.message_handler(content_types=['contact'])  # if user sent contact
def contact(message):
    client_name.clear()  # to clear list if user restart bot
    client_name.append(message.contact.first_name)
    client_name.append(message.contact.last_name)
    client_name.append(message.contact.phone_number)
    bot.send_message(message.chat.id, 'Отлично, я вас записала🤩')  # I wrote you down
    # total(client_time, client_description, client_name)  # send request to google calendar api
    print(client_name, client_description, client_time)


bot.polling(True)
