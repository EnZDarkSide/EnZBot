import calendar
import datetime
import itertools
import json
import locale

import pytz
from pytz import timezone
from vkbottle import keyboard_gen

locale.setlocale(locale.LC_ALL, 'ru_RU')

tz = timezone('Asia/Yekaterinburg')
one_day = datetime.timedelta(days=1)


def get_week(_date):
    day_idx = (_date.weekday()) % 7  # turn sunday into 0, monday into 1, etc.
    monday = _date - datetime.timedelta(days=day_idx)
    _date = monday
    for n in range(7):
        yield _date
        _date += one_day


def general_keyboard():
    return create_keyboard([{"text": "Расписание"}, {"text": "Портал"}])


def range_menu(arr):
    return create_keyboard(*[[{"text": str(i)}] for i in arr])


def trams_keyboard():
    return create_keyboard([{"text": 'Обновить данные'}, {"text": 'Указать адрес'}],
                           [{"text": 'Главное меню', "color": "secondary"}])


def button(day_name, start_date, end_date=None, color='primary'):
    if end_date is None:
        end_date = start_date

    return {"start_date": start_date.strftime("%d.%m.%Y"), "end_date": end_date.strftime("%d.%m.%Y"),
            "day_name": day_name, "color": color}


def schedule_keyboard():
    buttons_arr = schedule_keyboard_obj()

    return create_keyboard(*[[{"text": btn['day_name'],
                               "payload": json.dumps(btn),
                               "color": 'positive' if btn['day_name'] == 'Сегодня' else btn['color']}
                              for btn in split] for split in buttons_arr], [{"text": 'Назад', "color": 'secondary'}])


def schedule_keyboard_obj():
    dt = local_dt_now()

    today_index = dt.today().weekday()
    week_dates = list(get_week(dt.now().date()))

    buttons = []

    for d in week_dates:
        buttons.append(button(
            calendar.day_name[d.weekday()].capitalize() if d.weekday() != today_index else 'Сегодня', d, d))

    tomorrow_date = dt.now() + datetime.timedelta(days=1)

    next_week = list(get_week(dt.now().date() + datetime.timedelta(days=7)))

    top_buttons = [
        button('Завтра', tomorrow_date, tomorrow_date),
        button('На нед.', week_dates[0], week_dates[6], 'secondary'),
        button('На след. нед.', next_week[0], next_week[6], 'secondary')
    ]

    buttons_arr = [top_buttons, buttons[3:6], buttons[:3]]
    return buttons_arr


def local_dt_now():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz)


# Список всех кнопок
b_arr = list(itertools.chain(*[[btn['day_name'] for btn in row] for row in schedule_keyboard_obj()]))


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
