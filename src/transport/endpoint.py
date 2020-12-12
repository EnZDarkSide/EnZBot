from typing import Tuple

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src import messages
from src.transport import Transport, branches
from src.transport.entities.stop import Stop
from src.utils import trams_keyboard, general_keyboard, iterable_to_string

bp = Blueprint()


@bp.on.message(text=['Где трамваи?', 'Т'])
async def portal(answer: Message):
    await answer('Меню трамваев', keyboard=trams_keyboard())
    return Branch(branches.trams_menu)


@bp.branch.cls_branch(branches.trams_menu)
class PortalBranch(ClsBranch):

    @rule_disposal(VBMLRule("От Умельцев до УрГЭУ", lower=True))
    async def from_dorm_to_usue(self, answer: Message):
        trams = Transport.from_dorm_to_university()

        trams_str = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ])

        if not trams_str:
            await answer('Трамваев нет', keyboard=trams_keyboard())

        await answer(trams_str, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule("От УрГЭУ до Умельцев", lower=True))
    async def from_usue_to_dorm(self, answer: Message):
        trams = Transport.from_university_to_dorm()

        trams_str = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ])

        if not trams_str:
            await answer('Трамваев нет', keyboard=trams_keyboard())

        await answer(trams_str, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule("Указать адрес", lower=True))
    async def select_stop(self, answer: Message):
        await answer(messages.getting_home_stop_first_letter)
        return Branch(branches.adding_tram_stop)

    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, answer: Message):
        await answer("Возвращаемся", keyboard=general_keyboard())
        return ExitBranch()


@bp.branch.cls_branch(branches.adding_tram_stop)
class AddingTramStopBranch(ClsBranch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.stops: Tuple[Stop] = tuple()

    # выполняется, когда ответ — первая цифра или буква остановки
    @rule_disposal(VBMLRule(r"^[147А-Я]$", lower=True))
    async def show_tram_stops(self, answer: Message):
        self.stops: Tuple[Stop] = Transport.get_stops(answer.text)
        stop_names: Tuple[str] = tuple(map(lambda stop: str(stop.name), self.stops))

        await answer(iterable_to_string(stop_names))
        await answer(messages.stop_choice)

    # выполняется, когда пользователь написал название остановки
    @rule_disposal(VBMLRule(r"^[0-9а-я ]+"))
    async def add_stop_id_to_db(self, answer: Message):
        stop_name: str = answer.text.lower()

        stops: Tuple[Stop] = tuple(filter(lambda stop: stop.name.lower() == stop_name, self.stops))

        if stops:
            Transport.save_home_tram_stop_id(answer.id, stops[0].id)
            await answer(messages.done)
        else:
            await answer(messages.error)

        return Branch('adding-university-tram-stop')

    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, answer: Message):
        await answer(messages.resp_show_menu, keyboard=general_keyboard())
        return ExitBranch()
