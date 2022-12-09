from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from sql_file import get_empty_space

first_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✏️ Записаться', callback_data='entry:make')
        ],
        [
            InlineKeyboardButton(text='📂 Мои записи', callback_data="entry:my"),
            InlineKeyboardButton(text='🗑️ Удалить запись', callback_data="entry:delete"),
        ],
    ]
)

option_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='😽 Реснички', callback_data='service:eyelashes'),
        ],
        [
            InlineKeyboardButton(text='🚺 Депиляция', callback_data="depilation"),
        ],
        [
            InlineKeyboardButton(text='⬅️ Назад к выбору Действия', callback_data="first:back"),
        ],
    ]
)

service_of_first_choice = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='👙 Бикини 30 евро, 20 мин', callback_data='service:bikini')
        ],
        [
            InlineKeyboardButton(text='🦵 Ноги 45 евро, 40 мин', callback_data="service:legs"),
        ],
        [
            InlineKeyboardButton(text='💪 Руки 20 евро, 15 мин', callback_data='service:arm')
        ],
        [
            InlineKeyboardButton(text='😌 Лицо 10 евро, 10 мин', callback_data="service:face"),
        ],
        [
            InlineKeyboardButton(text='⬅️ Назад к выбору Опциии', callback_data="entry:back"),
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
            InlineKeyboardButton(text='⬅️ Назад к выбору Опциии', callback_data="entry:make"),
        ],
    ]
)
back_to_entry = InlineKeyboardMarkup(
    inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Назад к выбору Действия', callback_data="first:back"),
            ]
    ]
)


def show_time(client_date: list):
    choice_time = InlineKeyboardMarkup(row_width=3)
    free_space = get_empty_space(client_date)  # get info from SQL, how many cell in day we have
    for time_but in range(len(free_space)):  # create button time [14:00, 15:00, 16:00 ...]
        choice_time.insert(InlineKeyboardButton(
            text=f'1{time_but + 4}:00', callback_data=f'time:1{time_but + 4}')) if free_space[time_but] else None
    # create button 'back'
    choice_time.row(InlineKeyboardButton(text='⬅️Назад к выбору дня', callback_data="service:back"))

    return choice_time  # return Markup
