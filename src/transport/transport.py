from typing import Iterator, Union

from src.transport.entities.stop_type import StopType
from .entities.stop import Stop
from .entities.tram import Tram
from .parser import TramParser
from ..database.enitities.Transport import DBTransport

parser = TramParser()


class Transport:

    @staticmethod
    def __check_stop_by_name(stop_name: str) -> bool:
        stop_name = stop_name.lower()
        stop_first_letter = stop_name[0]

        stops_names = map(lambda stop: stop.lower(), Transport.get_stops_names(stop_first_letter))

        return stop_name in stops_names

    @staticmethod
    def __check_stop_by_id(stop_id: int) -> bool:
        return TramParser.is_id_valid(stop_id)

    @staticmethod
    def stop_exists(stop: Union[str, int]) -> bool:
        if isinstance(stop, str):
            return Transport.__check_stop_by_name(stop)
        elif isinstance(stop, int):
            return Transport.__check_stop_by_id(stop)

    @staticmethod
    def get_trams(user_id: int, stop_type: StopType) -> Iterator[Tram]:
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
    def get_stops_names(stop_first_letter: str) -> [str]:
        """Возвращает названия остановок по первой их букве"""

        return list(map(lambda stop: stop.name, Transport.get_stops(stop_first_letter)))

    @staticmethod
    def save_tram_stop_id(user_id: int, tram_stop_id: int, stop_type: StopType):
        if stop_type == StopType.HOME:
            DBTransport.save_home_stop_id(user_id, tram_stop_id)
        else:
            DBTransport.save_university_stop_id(user_id, tram_stop_id)
