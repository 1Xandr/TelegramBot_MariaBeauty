from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


first_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='😽Реснички', callback_data='service:eyelashes')
        ],
        [
            InlineKeyboardButton(text='👙Депиляция', callback_data="depilation"),
        ],
    ]
)

service_of_first_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👙Бикини 30 евро, 20 мин', callback_data='service:bikini')
        ],
        [
            InlineKeyboardButton(text='🦵Ноги 45 евро, 40 мин', callback_data="service:legs"),
        ],
        [
            InlineKeyboardButton(text='💪Руки 20 евро, 15 мин', callback_data='service:arm')
        ],
        [
            InlineKeyboardButton(text='😌Лицо 10 евро, 10 мин', callback_data="service:face"),
        ],
        [
            InlineKeyboardButton(text='⬅️Назад', callback_data="first:back"),
        ],
    ]
)

choice_month = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📅 Этот месяц 📅', callback_data='month:this_month'),
            InlineKeyboardButton(text='➡️ Следующий месяц ➡️', callback_data="month:next_month"),
        ],
        [
            InlineKeyboardButton(text='⬅️Назад', callback_data="first:back"),
        ],
    ]
)


choice_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='14:00', callback_data='time:14'),
        ],
        [
            InlineKeyboardButton(text='15:00', callback_data="time:15"),
        ],
        [
            InlineKeyboardButton(text='16:00', callback_data="time:16"),
        ],
    ]
)
