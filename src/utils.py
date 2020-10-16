from typing import List

from vkbottle import keyboard_gen


def general_menu():
    return create_keyboard([{"text": "Добавить группу"}, {"text": 'Указать адрес'}], [{"text": "Где трамваи?"}])


def trolleys_menu():
    return create_keyboard([{"text": 'Обновить данные'}, {"text": 'Указать адрес'}],
                           [{"text": 'Главное меню', "color": "secondary"}])


def address_menu():
    return create_keyboard([{"text": 'Назад'}])


def create_keyboard(*rows: List[dict]):
    keyboard = keyboard_gen(
        [
            [{"text": button["text"],
              "color": button["color"] if "color" in button else "primary",
              "type": button["type"] if "type" in button else "text"} for button in row]
            for row in rows
        ],
        one_time=True
    )
    return keyboard
