from typing import Iterator

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src.other import handlers, messages, branches
from src.other.utils import trams_keyboard, general_keyboard
from src.transport import Transport
from src.transport.entities.stop_type import StopType
from src.transport.entities.tram import Tram

bp = Blueprint()


@bp.on.message(text=[handlers.show_trams, handlers.show_trams_short])
async def show_tram_menu(answer: Message):
    """Создаёт основное меню для травмаев"""
    keyboard = trams_keyboard(user_id=answer.from_id, one_time=True)

    await answer(
        messages.endpoint_choice if Transport.stop_saved(answer.from_id) else messages.no_stop_saved,
        keyboard=keyboard)


    return Branch(branches.trams_menu)


class BaseTramBranchInterface:
    """Реализация правила выхода из ветки"""

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        """Выходит в основное меню"""

        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()


@bp.branch.cls_branch(branches.trams_menu)
class TramsMenuBranch(ClsBranch, BaseTramBranchInterface):
    """Действия для кнопок основного меню трамваев"""

    @rule_disposal(VBMLRule(
        [handlers.show_home_tram_stops, handlers.show_university_tram_stops], lower=True))
    async def show_trams(self, answer: Message):
        """Показывает расписание травмаев"""

        if answer.text == handlers.show_home_tram_stops:
            stop_type = StopType.HOME
        else:
            stop_type = StopType.UNIVERSITY

        trams: Iterator[Tram] = Transport.get_trams(answer.peer_id, stop_type)

        await answer('\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ]) or messages.no_trams, keyboard=trams_keyboard(user_id=answer.from_id, one_time=True))

    @rule_disposal(VBMLRule(handlers.set_tram_stops, lower=True))
    async def start_stops_setup(self, answer: Message):
        """Запускает установление остановок"""

        await answer(messages.getting_home_stop_first_letter)
        return Branch(branches.show_tram_stops, stop_type=StopType.HOME)


@bp.branch.cls_branch(branches.show_tram_stops)
class ShowTramStopsBranch(ClsBranch, BaseTramBranchInterface):
    """Показывает доступные остановки по первой букве

    Получает на вход stop_type — HOME или UNIVERSITY —,
    который передаёт на ветку, которая сохраняет идентификатор остановки.
    """

    async def branch(self, answer: Message, *args):
        """Вызывается, когда пользователь ввёл недопустимый символ или больше одного символа"""

        await answer(messages.no_stops_for_this_char if len(answer.text) == 1 else messages.one_char_only)

    @rule_disposal(VBMLRule(handlers.regex_stop_first_letter, lower=True))
    async def show_stops(self, answer: Message):
        """Показывает остановки по введённой пользователем первой букве"""

        await answer(msg := '\n'.join([
            f'{stop.id}: {stop.title}' for stop in Transport.get_stops(stop_first_letter=answer.text)
        ]) or messages.no_stops_for_this_char)

        if msg != messages.no_stops_for_this_char:
            await answer(messages.stop_choice)
            return Branch(branches.save_tram_stop_id, stop_type=self.context['stop_type'], send=answer)


@bp.branch.cls_branch(branches.save_tram_stop_id)
class SaveTramStopIdBranch(ClsBranch, BaseTramBranchInterface):
    """Сохраняет идентификатор остановки

    Получает на вход stop_type — HOME или UNIVERSITY.
    Если тип — HOME, то после сохранения снова показывает доступные остановки по первому символу,
    если тип — UNIVERSITY — показывает главное меню.
    """

    async def branch(self, answer: Message, *args):
        """Вызывается, когда пользователь ввёл недопустимый идентификатор"""

        await answer(messages.wrong_stop_id)

    @rule_disposal(VBMLRule(handlers.regex_stop_id, lower=True))
    async def save_stop_id(self, answer: Message):
        """Вызывается, когда пользователь вводит число"""

        stop_id: int = int(answer.text)
        stop_type: StopType = self.context['stop_type']

        if not Transport.stop_exists(stop_id):
            await answer(messages.wrong_stop_id)
            return

        Transport.save_tram_stop_id(answer.peer_id, stop_id, stop_type)

        await answer(messages.done)

        if stop_type == StopType.HOME:
            await answer(messages.getting_university_stop_first_letter)
            return Branch(branches.show_tram_stops, stop_type=StopType.UNIVERSITY, send=answer)

        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()
