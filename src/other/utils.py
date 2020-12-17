import calendar
import datetime
import itertools
import locale

import pendulum
from vkbottle import keyboard_gen

from src._date import get_week
from src.other import handlers

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


def general_keyboard():
    return create_keyboard([{"text": "Расписание"}, {"text": "Портал"}],
                           [{"text": handlers.show_trams, 'color': 'secondary'},
                            {"text": "Сменить группу", "color": "secondary"}])


def range_menu(arr):
    return create_keyboard(*[[{"text": str(i)}] for i in arr])


def trams_keyboard(home_btn_enabled: bool = True, university_btn_enabled: bool = True, one_time: bool = False) -> str:
    direction_btns = []

    if home_btn_enabled:
        direction_btns.append({"text": handlers.show_home_tram_stops, 'color': 'positive'})

    if university_btn_enabled:
        direction_btns.append({"text": handlers.show_university_tram_stops, 'color': 'positive'})

    action_btns = [
        {"text": handlers.set_tram_stops, "color": "negative"},
        {'text': handlers.exit_branch, 'color': 'secondary'}
    ]

    if direction_btns:
        return create_keyboard(direction_btns, action_btns, one_time=one_time)
    else:
        return create_keyboard(action_btns, one_time=one_time)


def button(day_name, start_date, end_date=None, btn_name=None, color='primary'):
    if end_date is None:
        end_date = start_date

    if not btn_name:
        btn_name = day_name

    return {"start_date": start_date.strftime("%d.%m.%Y"), "end_date": end_date.strftime("%d.%m.%Y"),
            "day_name": day_name, "btn_name": btn_name, "color": color}


def portal_keyboard():
    return create_keyboard([{'text': 'Расписание заданий'}],
                           [{'text': 'Сменить данные', "color": 'secondary'},
                            {'text': 'Выйти', "color": 'secondary'}])


def schedule_keyboard():
    buttons_arr = schedule_keyboard_obj()

    return create_keyboard(*[[{"text": btn['btn_name'],
                               "color": 'positive' if btn['btn_name'] == 'Сегодня' else btn['color']}
                              for btn in split] for split in buttons_arr], [{"text": 'Назад', "color": 'secondary'}])


def schedule_keyboard_obj():
    dt = pendulum.now('Asia/Yekaterinburg')

    print(f'dt = {dt}')

    today_index = dt.weekday()
    week_dates = list(get_week(dt.date()))

    buttons = [
        button(
            calendar.day_name[d.weekday()].capitalize(),
            d, d,
            calendar.day_name[d.weekday()].capitalize() if d.weekday() != today_index else 'Сегодня') for d in
        week_dates]

    tomorrow_date = dt.date() + datetime.timedelta(days=1)

    next_week = list(get_week(dt.date() + datetime.timedelta(days=7)))

    top_buttons = [
        button('Завтра', tomorrow_date, tomorrow_date),
        button('На нед.', week_dates[0], week_dates[6], None, 'secondary'),
        button('На след. нед.', next_week[0], next_week[6], None, 'secondary')
    ]

    buttons_arr = [top_buttons, buttons[3:6], buttons[:3]]
    return buttons_arr


def get_schedule_buttons(add_today=False):
    _list = list(itertools.chain(*[[btn for btn in row] for row in schedule_keyboard_obj()]))
    _dict = {btn['day_name']: btn for btn in _list}

    if add_today:
        today_button = [btn for btn in _list if btn['btn_name'] == 'Сегодня']
        if today_button:
            _dict['Сегодня'] = today_button[0]

    print('/n'.join(_dict))

    return _dict


def address_menu():
    return create_keyboard([{"text": 'Назад'}])


def create_keyboard(*rows, one_time=False):
    keyboard = keyboard_gen(
        [
            [{"text": button["text"],
              "color": button["color"] if "color" in button else "primary",
              "payload": button["payload"] if "payload" in button else "",
              "type": button["type"] if "type" in button else "text"} for button in row]
            for row in rows
        ],
        one_time=one_time
    )
    return keyboard


kb_exit = create_keyboard([{'text': 'Выйти'}])
