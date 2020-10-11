from typing import Tuple, List

from vkbottle import keyboard_gen
from vkbottle.keyboard import Keyboard, Text


def create_keyboard(*rows: List[dict]):
    keyboard = keyboard_gen(
        [
            [{"text": button["text"],
              "color": button["color"] if "color" in button else "primary",
              "type": button["type"] if "type" in button else "text"} for button in row]
            for row in rows
        ]
    )
    return keyboard
