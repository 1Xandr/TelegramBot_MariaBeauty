from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from days import current_day, days_in_month


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
    ]
)

choice_month = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='📅 Этот месяц 📅', callback_data='month:this_month'),
            InlineKeyboardButton(text='➡️ Следующий месяц ➡️', callback_data="month:next_month"),
        ],
    ]
)

choice_day = InlineKeyboardMarkup(row_width=7)

for day in range(current_day, days_in_month + 1):  # make button in range 1-31 for days
    choice_day.insert(InlineKeyboardButton(text=str(day), callback_data=f'day:{day}'))


choice_time = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='14:00', callback_data='time:two'),
        ],
        [
            InlineKeyboardButton(text='15:00', callback_data="time:three"),
        ],
        [
            InlineKeyboardButton(text='16:00', callback_data="time:four"),
        ],
    ]
)
