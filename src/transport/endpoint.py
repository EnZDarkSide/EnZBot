import json
from typing import Iterator, List, Tuple, Optional, Dict

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src.other import handlers, messages, branches, keyboards
from src.transport import Transport
from src.transport.entities.stop_type import StopType
from src.transport.entities.tram import Tram

bp = Blueprint()


@bp.on.message(text=[handlers.show_trams, handlers.show_trams_short])
async def show_tram_menu(answer: Message):
    """Создаёт основное меню для травмаев"""

    await answer(
        messages.endpoint_choice if Transport.stop_saved(answer.from_id) else messages.no_stop_saved,
        keyboard=keyboards.trams_menu(user_id=answer.from_id, one_time=True)
    )

    return Branch(branches.trams_menu)


class BaseTramBranchInterface:
    """Реализация правила выхода из ветки"""

    @rule_disposal(VBMLRule(handlers.exit_branch, lower=True))
    async def exit_branch(self, answer: Message):
        """Выходит в основное меню"""

        await answer(messages.resp_show_menu, keyboard=keyboards.main_menu())
        return ExitBranch()


@bp.branch.cls_branch(branches.trams_menu)
class TramsMenuBranch(ClsBranch, BaseTramBranchInterface):
    """Действия для кнопок основного меню трамваев"""

    @rule_disposal(VBMLRule(
        [handlers.show_home_tram_stops, handlers.show_university_tram_stops], lower=True))
    async def show_trams(self, answer: Message):
        """Показывает расписание травмаев"""

        stop_type = StopType.HOME if answer.text == handlers.show_home_tram_stops else StopType.UNIVERSITY
        trams: Iterator[Tram] = Transport.get_trams(answer.peer_id, stop_type)

        await answer('\n'.join([
            f'{tram.number}: {tram.arrival_time} [{tram.arrival_distance}]' for tram in trams
        ]) or messages.no_trams, keyboard=keyboards.trams_menu(user_id=answer.from_id, one_time=True))

    @rule_disposal(VBMLRule(handlers.set_tram_stops, lower=True))
    async def start_stops_setup(self, answer: Message):
        """Запускает установление остановок"""

        await answer(messages.getting_home_stop_first_letter)
        return Branch(branches.show_tram_stops, stop_type=StopType.HOME)


@bp.branch.cls_branch(branches.show_tram_stops)
class ShowTramStopsBranch(ClsBranch, BaseTramBranchInterface):
    """Показывает доступные остановки по первой букве

    Получает на вход stop_type — HOME или UNIVERSITY —,
    чтобы передать на ветку, которая сохраняет идентификатор остановки.
    """

    async def branch(self, answer: Message, *args):
        """Вызывается, когда пользователь ввёл недопустимый символ или больше одного символа"""

        await answer(messages.no_stops_for_this_char if len(answer.text) == 1 else messages.one_char_only)

    @rule_disposal(VBMLRule(handlers.regex_stop_first_letter, lower=True))
    async def show_stops(self, answer: Message):
        """Показывает остановки по введённой пользователем первой букве"""

        if not (stops := Transport.get_stops(stop_first_letter=answer.text)):
            await answer(messages.no_stops_for_this_char)
            return

        await answer(
            messages.stop_name_choice,
            keyboard=keyboards.create_grouped_btns([(stop.name, {'directions': stop.directions}) for stop in stops],
                                                   exit_btn=True)
        )

        return Branch(branches.show_tram_directions, stop_type=self.context['stop_type'])


@bp.branch.cls_branch(branches.show_tram_directions)
class ShowTramDirectionsBranch(ClsBranch, BaseTramBranchInterface):
    """"""

    async def branch(self, answer: Message, *args):
        """Показывает направления по выбранной пользователем остановке"""

        if not answer.payload:
            await answer("Выберите остановку из списка кнопок")
            return

        payload: Dict = json.loads(answer.payload)
        # направления остановок с их идентификаторами
        directions: List[Tuple[int, Optional[str]]] = payload['directions']

        if len(directions) == 1:
            stop_id: int = directions[0][0]
            direction_name: Optional[str] = directions[0][1]
            stop_type: StopType = self.context['stop_type']

            stop_title: str = answer.text + (f'({direction_name})' if direction_name else '')
            await answer(f'Вы выбрали {stop_title}')

            Transport.save_tram_stop_id(answer.from_id, stop_id, stop_type)
            await answer(messages.done)

            if self.context['stop_type'] == StopType.HOME:
                await answer(messages.getting_university_stop_first_letter)
                return Branch(branches.show_tram_stops, stop_type=StopType.UNIVERSITY)

            await answer(messages.resp_show_menu, keyboard=keyboards.main_menu())
            return ExitBranch()

        await answer(
            messages.stop_direction_choice,
            keyboard=keyboards.create_grouped_btns(
                [(direction[1] or messages.no_direction, {'stop_id': direction[0]}) for direction in directions],
                one_time=True
            )
        )

        return Branch(branches.save_tram_stop_id, stop_type=self.context['stop_type'])

    @rule_disposal(VBMLRule(handlers.go_back))
    async def go_back(self, answer: Message):
        await answer(messages.getting_home_stop_first_letter)
        return Branch(branches.show_tram_stops, stop_type=self.context['stop_type'])


@bp.branch.cls_branch(branches.save_tram_stop_id)
class SaveTramStopIdBranch(ClsBranch, BaseTramBranchInterface):
    """Сохраняет идентификатор остановки

    Получает на вход stop_type — HOME или UNIVERSITY.
    Если тип — HOME, то после сохранения снова показывает доступные остановки по первому символу,
    если тип — UNIVERSITY — показывает главное меню.
    """

    async def branch(self, answer: Message, *args):
        """Вызывается, когда пользователь выбирает остановку"""

        if not answer.payload:
            await answer("Выберите направление из списка кнопок")
            return

        payload: Dict = json.loads(answer.payload)

        stop_id: int = int(payload['stop_id'])
        stop_type: StopType = self.context['stop_type']

        Transport.save_tram_stop_id(answer.from_id, stop_id, stop_type)
        await answer(messages.done)

        if stop_type == StopType.HOME:
            await answer(messages.getting_university_stop_first_letter)
            return Branch(branches.show_tram_stops, stop_type=StopType.UNIVERSITY)

        await answer(messages.resp_show_menu, keyboard=keyboards.main_menu())
        return ExitBranch()
