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
async def portal(answer: Message):
    await answer(messages.endpoint_choice, keyboard=trams_keyboard(one_time=True))
    return Branch(branches.trams_menu)


@bp.branch.cls_branch(branches.trams_menu)
class TramsMenuBranch(ClsBranch):

    @rule_disposal(VBMLRule(
        [handlers.show_home_tram_stops, handlers.show_university_tram_stops], lower=True))
    async def show_trams(self, answer: Message):
        if answer.text == handlers.show_home_tram_stops:
            stop_type = StopType.HOME
        else:
            stop_type = StopType.UNIVERSITY

        trams: Iterator[Tram] = Transport.get_trams(answer.peer_id, stop_type)

        message = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ]) or messages.no_trams

        await answer(message, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule(handlers.set_tram_stops, lower=True))
    async def select_stop(self, answer: Message):
        await answer(messages.getting_home_stop_first_letter)
        return Branch(branches.set_home_tram_stops)

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()


@bp.branch.cls_branch(branches.set_home_tram_stops)
class SetHomeTramStopsBranch(ClsBranch):

    # вызывается, когда пользователь тупой как пень
    async def branch(self, answer: Message, *args):
        await answer(messages.something_wrong)

    # вызывается, когда пользователь вводит первый символ остановки
    @rule_disposal(VBMLRule(handlers.regex_stop_first_letter, lower=True))
    async def show_stops(self, answer: Message):
        stop_names = [f'{stop.id}. {stop.name} ({stop.direction})'
                      for stop in Transport.get_stops(stop_first_letter=answer.text)]

        await answer('\n'.join(stop_names))
        await answer(messages.stop_choice)

    # вызывается, когда пользователь вводит id остановки
    @rule_disposal(VBMLRule(handlers.regex_stop_id, lower=True))
    async def save_stop_id(self, answer: Message):
        try:
            stop_id = int(answer.text)
        except ValueError:
            await answer(messages.wrong_stop_id)
            return

        if not Transport.stop_exists(stop_id):
            await answer(messages.wrong_stop_id)
            return

        Transport.save_tram_stop_id(answer.peer_id, stop_id, StopType.HOME)

        await answer(messages.done)
        await answer(messages.getting_university_stop_first_letter)

        return Branch(branches.set_university_tram_stops)

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()


@bp.branch.cls_branch(branches.set_university_tram_stops)
class SetUniversityTramStopsBranch(ClsBranch):

    # вызывается, когда пользователь тупой как пень
    async def branch(self, answer: Message, *args):
        await answer(messages.something_wrong)

    # вызывается, когда пользователь вводит первый символ остановки
    @rule_disposal(VBMLRule(handlers.regex_stop_first_letter, lower=True))
    async def show_stops(self, answer: Message):
        stop_names = [f'{stop.id}. {stop.name} ({stop.direction})'
                      for stop in Transport.get_stops(stop_first_letter=answer.text)]

        await answer('\n'.join(stop_names))
        await answer(messages.stop_choice)

    # вызывается, когда пользователь вводит id остановки
    @rule_disposal(VBMLRule(handlers.regex_stop_id, lower=True))
    async def save_stop_id(self, answer: Message):
        try:
            stop_id = int(answer.text)
        except ValueError:
            await answer(messages.wrong_stop_id)
            return

        if not Transport.stop_exists(stop_id):
            await answer(messages.wrong_stop_id)
            return

        Transport.save_tram_stop_id(answer.peer_id, stop_id, StopType.UNIVERSITY)

        await answer(messages.done)

        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()
