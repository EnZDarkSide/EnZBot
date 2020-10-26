import datetime
import itertools
import json

from numpy import array_split
from vkbottle import keyboard_gen
from datetime import date
import calendar
import locale

locale.setlocale(locale.LC_ALL, 'ru_RU')


def general_keyboard():
    return create_keyboard([{"text": "Расписание"}, {"text": "Портал"}], [{"text": "Где трамваи?"}])


def range_menu(arr):
    return create_keyboard(*[[{"text": str(i)}] for i in arr])


def trams_keyboard():
    return create_keyboard([{"text": 'Обновить данные'}, {"text": 'Указать адрес'}],
                           [{"text": 'Главное меню', "color": "secondary"}])


def schedule_keyboard():
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(4, -3, -1)]
    today_index = date.today().weekday()

    wd_list = []

    for d in date_list:
        wd_list.append([{"start_date": d.date().strftime("%d.%m.%Y"), "end_date": d.date().strftime("%d.%m.%Y"),
                         "day_name": calendar.day_name[d.weekday()] if d.weekday() != today_index else 'Сегодня'}])

    return create_keyboard(*[[{"text": elem['day_name'],
                               "payload": json.dumps(elem),
                               "color": 'positive' if elem['day_name'] == 'Сегодня' else "primary"}
                              for elem in arr] for arr in wd_list])


def address_menu():
    return create_keyboard([{"text": 'Назад'}])


def create_keyboard(*rows):
    keyboard = keyboard_gen(
        [
            [{"text": button["text"],
              "color": button["color"] if "color" in button else "primary",
              "payload": button["payload"] if "payload" in button else "",
              "type": button["type"] if "type" in button else "text"} for button in row]
            for row in rows
        ],
        one_time=True
    )
    return keyboard
