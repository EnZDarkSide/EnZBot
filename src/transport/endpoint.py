from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src.transport import Transport
from src.utils import trams_keyboard, general_keyboard

bp = Blueprint()


@bp.on.message(text=['Где трамваи?', 'Т'])
async def portal(answer: Message):
    await answer('Меню трамваев', keyboard=trams_keyboard())
    return Branch('trams_menu')


@bp.branch.cls_branch("trams_menu")
class PortalBranch(ClsBranch):

    @rule_disposal(VBMLRule("От Умельцев до УрГЭУ", lower=True))
    async def from_dorm_to_usue(self, answer: Message):
        trams = Transport.from_dorm_to_university()

        trams_str = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ])

        await answer(trams_str, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule("От УрГЭУ до Умельцев", lower=True))
    async def from_usue_to_dorm(self, answer: Message):
        trams = Transport.from_university_to_dorm()

        trams_str = '\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ])

        await answer(trams_str, keyboard=trams_keyboard())

    @rule_disposal(VBMLRule("Указать адрес", lower=True))
    async def select_stop(self, answer: Message):
        await answer('Функция скоро будет реализована', keyboard=trams_keyboard())

    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, answer: Message):
        await answer("Возвращаемся", keyboard=general_keyboard())
        return ExitBranch()
