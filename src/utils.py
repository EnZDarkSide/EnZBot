from vkbottle.keyboard import Keyboard, Text


def create_keyboard(*buttons):
    keyboard = Keyboard(one_time=True)

    for button in buttons:
        keyboard.add_row()
        keyboard.add_button(Text(label=button), color="primary")

    return keyboard
