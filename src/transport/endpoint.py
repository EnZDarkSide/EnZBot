from typing import Tuple, Iterator

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src.other import handlers, messages, branches
from src.other.utils import trams_keyboard, general_keyboard, iterable_to_string, StopType
from src.transport import Transport
from src.transport.entities.stop import Stop
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
        return Branch(branches.adding_tram_stop)

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()


@bp.branch.cls_branch(branches.adding_tram_stop)
class AddingTramStopBranch(ClsBranch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.stop_type: StopType = StopType.HOME
        self.stops: Tuple[Stop] = tuple()

    # выполняется, когда ответ — первая цифра или буква остановки
    @rule_disposal(VBMLRule(handlers.regex_stop_first_letter, lower=True))
    async def show_tram_stops(self, answer: Message):
        self.stops: Tuple[Stop] = Transport.get_stops(answer.text)
        stop_names: Tuple[str] = tuple(map(lambda stop: str(stop.name), self.stops))

        await answer(iterable_to_string(stop_names))
        await answer(messages.stop_choice)

    # выполняется, когда пользователь написал название остановки
    @rule_disposal(VBMLRule(handlers.regex_stop_name))
    async def add_stop_id_to_db(self, answer: Message):
        stop_name: str = answer.text.lower()

        stops: Tuple[Stop] = tuple(filter(lambda stop: stop.name.lower() == stop_name, self.stops))

        if stops:
            Transport.save_tram_stop_id(answer.id, stops[0].id, self.stop_type)

            await answer(messages.done)
            await answer(messages.getting_university_stop_first_letter)

            if self.stop_type == StopType.HOME:
                self.stop_type = StopType.UNIVERSITY
            else:
                return ExitBranch()
        else:
            await answer(messages.error)

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()
