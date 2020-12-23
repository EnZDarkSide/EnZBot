import calendar
import datetime
import itertools
import locale
from typing import Iterator, List, Dict, Iterable, Any, Callable, Tuple

import pendulum
from vkbottle import keyboard_gen

from src._date import get_week
from src.other import handlers
from src.transport import Transport
from src.transport.entities.stop import Stop

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


def _serialize_by_name_length(stop: Iterable[Stop]) -> Tuple[List[Stop], List[Stop], List[Stop]]:
    """Разделяет элементы по треём категоримя, чтобы вывести по кнопкам"""

    shorts: List[Stop] = []
    mediums: List[Stop] = []
    longs: List[Stop] = []

    for stop in stop:
        if (length := len(stop.name)) <= 11:
            shorts.append(stop)
        elif length <= 18:
            mediums.append(stop)
        else:
            longs.append(stop)

    return shorts, mediums, longs


def general_keyboard() -> str:
    return create_keyboard([{"text": "Расписание"}, {"text": "Портал"}],
                           [{"text": handlers.show_trams, 'color': 'secondary'},
                            {"text": "Сменить группу", "color": "secondary"}])


def range_menu(iterable: Iterator[Any]) -> str:
    return create_keyboard(*[[{"text": str(element)}] for element in iterable])


def trams_keyboard(user_id: int, one_time: bool = False) -> str:
    saved_stops: Iterator[str] = filter(None.__ne__, Transport.get_saved_stops(user_id))

    direction_btns = [
        {'text': stop_name, 'color': 'positive', 'payload': [1, 2]} for stop_name in saved_stops
    ]

    action_btns = [
        {'text': handlers.set_tram_stops, 'color': 'negative'},
        {'text': handlers.exit_branch, 'color': 'secondary'},
        {'text': 'Some text'}
    ]

    rows = filter(lambda btns: bool(btns), [direction_btns, action_btns])

    return create_keyboard(*rows, one_time=one_time)


def stops_keyboard(stops: List[Stop]) -> str:
    # def stops_keyboard(stops: Iterable[Stop]) -> str:
    # получаем три листа: короткие остановки, средние и длинные
    lsts: Tuple[List[Stop], List[Stop], List[Stop]] = _serialize_by_name_length(stops)
    rows: List[List[Dict[str, str]]] = []

    # проходится по всем трём листам
    for i in range(len(lsts)):
        lst = lsts[i]
        # обе перменные нужны для функции zip: https://stackoverflow.com/a/5389547/9645340
        # достать нужное количесвто элементов за раз
        lst_iter = iter(lst)
        # количество кнопок в ряд
        btns_count = 3 - i

        # создаёт кнопки: короткие названия — 3 в ряд,
        # средние — 2 в ряд и длинные — 1 название идёт в ряд
        for stops in zip(*[lst_iter] * btns_count):
            rows.append([{'text': stop.name, 'payload': stop.directions} for stop in stops])

        # если остаются кнопки
        # — например, в листе кортких было 8, берётся два раза по 3, две остаются —
        # добавить их в лист следующих по длине
        if left := len(lst) % btns_count:
            lsts[i + 1].extend(lst[-left:])

    return create_keyboard(*rows, [{'text': handlers.exit_branch, 'color': 'secondary'}])


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


# noinspection PyShadowingNames
def create_keyboard(*rows, one_time: bool = False, inline: bool = False):
    keyboard = keyboard_gen(
        [
            [{"text": button["text"],
              "color": button["color"] if "color" in button else "primary",
              "payload": button["payload"] if "payload" in button else "",
              "type": button["type"] if "type" in button else "text"} for button in row]
            for row in rows
        ],
        one_time=one_time,
        inline=inline
    )
    return keyboard


kb_exit = create_keyboard([{'text': 'Выйти'}])
