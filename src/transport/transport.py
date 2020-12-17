from typing import Iterator, Union

from src.transport.entities.stop_type import StopType
from .entities.stop import Stop
from .entities.tram import Tram
from .parser import TramParser
from ..database.enitities.Transport import DBTransport

parser = TramParser()


class Transport:
    """API для доступа к расписанию трамваев"""

    @staticmethod
    def stop_exists(stop: Union[str, int]) -> bool:
        """Проверяет существавание остановки по названию или идентификатору"""

        if isinstance(stop, str):
            return Transport._check_stop_by_name(stop)
        elif isinstance(stop, int):
            return Transport._check_stop_by_id(stop)
        else:
            raise TypeError('stop должна быть либо строкой, либо целым числом')

    @staticmethod
    def get_trams(user_id: int, stop_type: StopType) -> Iterator[Tram]:
        """Возвращает список трамваем остановки, идентификатор которой находится в базе пользователя

        Аргументы:
            user_id: int — id из ВК
            stop_type: StopType — два типа: HOME или UNIVERSITY
        """

        if stop_type == StopType.HOME:
            stop_id: int = DBTransport.get_home_stop_id(user_id)
        else:
            stop_id: int = DBTransport.get_university_stop_id(user_id)

        trams = parser.get_trams(stop_id)

        # нужны только трамваи с номерами 14, 25 и 27
        return filter(lambda tram: tram.number in ('14', '25', '27'), trams)

    @staticmethod
    def get_stops(stop_first_letter: str) -> [Stop]:
        """Возвращает остановки по первой букве"""

        return parser.get_stops(stop_first_letter)

    @staticmethod
    def save_tram_stop_id(user_id: int, tram_stop_id: int, stop_type: StopType):
        """Сохраняет идентификатор остановки дома или университета в БД"""

        if stop_type == StopType.HOME:
            DBTransport.save_home_stop_id(user_id, tram_stop_id)
        else:
            DBTransport.save_university_stop_id(user_id, tram_stop_id)

    @staticmethod
    def _check_stop_by_name(stop_name: str) -> bool:
        stop_name = stop_name.lower()
        stop_first_letter = stop_name[0]

        stops_names = map(lambda stop: stop.lower(), Transport._get_stops_names(stop_first_letter))

        return stop_name in stops_names

    @staticmethod
    def _check_stop_by_id(stop_id: int) -> bool:
        return TramParser.is_id_valid(stop_id)

    @staticmethod
    def _get_stops_names(stop_first_letter: str) -> [str]:
        return list(map(lambda stop: stop.name, Transport.get_stops(stop_first_letter)))
