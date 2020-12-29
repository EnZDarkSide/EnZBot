import calendar
import datetime
import itertools
import locale
from typing import List, Iterable, Tuple, TypeVar, Callable

import pendulum

from src._date import get_week

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')

T = TypeVar('T')


def group_by_length(elms: Iterable[T], get_length: Callable[[T], int]) -> List[List[T]]:
    """Разделяет элементы по группам из одной, двух или трёх элементов

    Аргументы
    elms — элементы в любом виде, завёрнутые в итерируемый тип
    get_length — функция, принимающая на вход элемент аргумента elms
                 и возвращающая длину элемента, по которой они группируются

    Возвращает список групп; каждая группа — от одной до трёх элементов, в зависимости от длины
    """

    lsts: Tuple[List[T], List[T], List[T]] = [], [], []
    grouped: List[List[T]] = []

    for elm in elms:
        if (length := get_length(elm)) <= 11:
            lsts[0].append(elm)
        elif length <= 18:
            lsts[1].append(elm)
        else:
            lsts[2].append(elm)

    # проходится по всем трём листам
    for i in range(len(lsts)):
        lst = lsts[i]
        # обе перменные нужны для функции zip: https://stackoverflow.com/a/5389547/9645340
        # достать нужное количесвто элементов за раз
        lst_iter = iter(lst)
        # количество кнопок в ряд
        btns_count = 3 - i

        # группирует элементы: короткие — 3 в группу,
        # средние — 2 в группу и длинные — 1 элемент идёт в группу
        grouped.extend([list(elms) for elms in zip(*[lst_iter] * btns_count)])

        # если остаются элементы — например,
        # в листе кортких было 8, берётся два раза по 3, два остаются —
        # добавить их в лист следующих по длине
        if left := len(lst) % btns_count:
            lsts[i + 1].extend(lst[-left:])

    return grouped


def filter_not_empty(*elms: Iterable[T]) -> Iterable[T]:
    return filter(lambda elm: bool(elm), elms)


def button(day_name, start_date, end_date=None, btn_name=None, color='primary'):
    if end_date is None:
        end_date = start_date

    if not btn_name:
        btn_name = day_name

    return {"start_date": start_date.strftime("%d.%m.%Y"), "end_date": end_date.strftime("%d.%m.%Y"),
            "day_name": day_name, "btn_name": btn_name, "color": color}


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
