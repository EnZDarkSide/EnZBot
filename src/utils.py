from vkbottle.keyboard import Keyboard, Text


def create_main_keyboard():
    keyboard = Keyboard(one_time=True)

    keyboard.add_row()
    keyboard.add_button(Text(label='Добавить группу'), color="primary")

    keyboard.add_row()
    keyboard.add_button(Text(label='Выбрать общежитие'), color="primary")

    return keyboard
