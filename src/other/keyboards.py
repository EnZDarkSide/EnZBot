import json
from typing import Iterator, List, Tuple, Dict, Any

from vkbottle import keyboard_gen

from src.other import handlers, utils
from src.other.utils import schedule_keyboard_obj
from src.transport import Transport


def create_keyboard(*rows, one_time: bool = False, inline: bool = False) -> str:
    """Основная функция для создания клавиатуры
    
    Каждый аргумент — отдельная строка с кнопками в виде листа,
    который содержит в себе словари-кнопки.
    """

    return keyboard_gen(
        [
            [{'text': utils.format_btn(button['text']),
              'color': button['color'] if 'color' in button else 'primary',
              'payload': button['payload'] if 'payload' in button else '',
              'type': button['type'] if 'type' in button else 'text'} for button in row]
            for row in rows
        ],
        one_time=one_time,
        inline=inline
    )


def create_grouped_btns(btns: List[Tuple[str, Dict]], one_time: bool = False,
                        back_btn: bool = False, exit_btn: bool = False) -> str:
    """Создаёт кнопки, группираю по длинне их названий

    Аргументы
    btns — кнопки-картежы: первый элемент — название кнопки, второй — payload в виде словаря
    """

    rows: List[List[Tuple[str, Dict]]] = utils.group_by_length(btns, lambda btn: len(btn[0]))

    grouped_btns = [
        [{'text': btn[0], 'payload': json.dumps(btn[1], ensure_ascii=False)} for btn in btns] for btns in rows
    ]
    extra_btns = list(filter(None.__ne__, [
        {'text': handlers.go_back, 'color': 'secondary'} if back_btn else None,
        {'text': handlers.exit_branch, 'color': 'secondary'} if exit_btn else None,
    ]))

    return create_keyboard(
        *utils.filter_not_empty(*grouped_btns, extra_btns),
        one_time=one_time
    )


def main_menu() -> str:
    return create_keyboard(
        [{'text': handlers.show_schedule}, {'text': handlers.open_portal}],
        [{'text': handlers.show_trams, 'color': 'secondary'}, {'text': handlers.change_group, 'color': 'secondary'}]
    )


def schedule_keyboard() -> str:
    buttons_arr = schedule_keyboard_obj()

    return create_keyboard(*[[{'text': btn['btn_name'],
                               'color': 'positive' if btn['btn_name'] == 'Сегодня' else btn['color']}
                              for btn in split] for split in buttons_arr], [{'text': 'Назад', 'color': 'secondary'}])


def portal_menu() -> str:
    return create_keyboard(
        [{'text': handlers.tasks_schedule}],
        [{'text': handlers.change_data, 'color': 'secondary'}, {'text': handlers.exit_branch, 'color': 'secondary'}]
    )


def trams_menu(user_id: int, one_time: bool = False) -> str:
    saved_stops: Iterator[str] = filter(None.__ne__, Transport.get_saved_stops(user_id))

    direction_btns = [
        {'text': stop_name, 'color': 'positive'} for stop_name in saved_stops
    ]

    action_btns = [
        {'text': handlers.set_tram_stops, 'color': 'negative'},
        {'text': handlers.exit_branch, 'color': 'secondary'}
    ]

    rows = filter(lambda btns: bool(btns), [direction_btns, action_btns])

    return create_keyboard(*rows, one_time=one_time)


def address_menu() -> str:
    return create_keyboard([{'text': handlers.go_back}])


def range_menu(iterable: Iterator[Any]) -> str:
    return create_keyboard(*[[{'text': str(element)}] for element in iterable])
