from datetime import datetime
from calendar import monthrange
import time

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

choice_day = InlineKeyboardMarkup(row_width=7)


def what_month(next_now_month: int):
    choice_day["inline_keyboard"].clear()  # if user restart bot
    current_year = datetime.now().year

    f_month = int(time.strftime('%m')) + next_now_month  # current month + 0 or 1 (if user chose next_month)
    month = 1 if f_month == 13 else f_month  # If now december(12) + 1 -> January(01)
    days_in_month = monthrange(current_year, month)[1]  # on December 31 days| month = 12 , days_in_month = 31
    # if next_month -> range(1, days_in_month + 1) else current day
    current_day = 1 if next_now_month == 1 else int(time.strftime('%d'))

    for day in range(current_day, days_in_month + 1):  # make button in range 1-31 for days
        choice_day.insert(InlineKeyboardButton(text=str(day), callback_data=f'day:{day}'))

    month = f'0{month}' if len(str(month)) == 1 else str(month)  # 1 -> 01 | 12 -> 12
    # make button back
    choice_day.row(InlineKeyboardButton(text='⬅️Назад к выбору месяца', callback_data="service:back"))
    # return number of month ('01') and year('2023')
    return month, str(int(time.strftime('%Y')) + 1) if month == '01' else time.strftime('%Y')  # 12+1, 2022 --> 01, 2023
