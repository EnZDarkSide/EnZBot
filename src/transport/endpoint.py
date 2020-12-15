from typing import Iterator

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src.other import handlers, messages, branches
from src.other.utils import trams_keyboard, general_keyboard, StopType
from src.transport import Transport
from src.transport.entities.tram import Tram

bp = Blueprint()


@bp.on.message(text=[handlers.show_trams, handlers.show_trams_short])
async def portal(answer: Message):
    await answer(messages.endpoint_choice, keyboard=trams_keyboard())
    return Branch(branches.trams_menu)


@bp.branch.cls_branch(branches.trams_menu)
class TramsMenuBranch(ClsBranch):

    @rule_disposal(VBMLRule(handlers.show_home_tram_stops, lower=True))
    async def go_to_university(self, answer: Message):
        trams: Iterator[Tram] = Transport.get_trams(answer.id, StopType.HOME)

        message = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ]) or messages.no_trams

        await answer(message, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule(handlers.show_university_tram_stops, lower=True))
    async def go_home(self, answer: Message):
        trams: Iterator[Tram] = Transport.get_trams(answer.id, StopType.UNIVERSITY)

        message = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ]) or messages.no_trams

        await answer(message, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule(handlers.set_tram_stops, lower=True))
    async def select_stop(self, answer: Message):
        await answer(messages.getting_home_stop_first_letter)
        return Branch(branches.first_stop_letter)

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()


@bp.branch.cls_branch(branches.first_stop_letter)
class AddingTramStopBranch(ClsBranch):
    async def branch(self, answer: Message, *args):
        stop_names = [f'{stop.id}. {stop.name} ({stop.direction})'
                      for i, stop in enumerate(Transport.get_stops(answer.text[0]))]

        await answer('\n'.join(stop_names))
        await answer(messages.stop_choice)

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()
