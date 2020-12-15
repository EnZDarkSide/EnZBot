from typing import Iterator

from src.other.utils import StopType
from .entities.stop import Stop
from .entities.tram import Tram
from .parser import TramParser
from ..database.enitities.Transport import DBTransport

parser = TramParser()


class Transport:
    # noinspection PyShadowingNames
    @staticmethod
    def stop_exists(stop: str) -> bool:
        stop = stop.lower()
        stop_first_letter = stop[0]

        stops = map(lambda stop: stop.lower(), parser.get_stops(stop_first_letter))

        return stop in stops

    @staticmethod
    def get_trams(user_id: int, stop_type: StopType) -> Iterator[Tram]:
        if stop_type == StopType.HOME:
            stop_id: int = DBTransport.get_home_stop_id(user_id)
        else:
            stop_id: int = DBTransport.get_university_stop_id(user_id)

        trams = parser.get_trams(stop_id)

        # нужны только трамваи с номерами 14, 25 и 27
        return filter(lambda tram: tram.number in (14, 25, 27), trams)

    @staticmethod
    def get_stops(stop_first_letter: str) -> [Stop]:
        """ Возвращает остановки по первой букве """
        return parser.get_stops(stop_first_letter)

    @staticmethod
    def save_tram_stop_id(user_id: int, tram_stop_id: int, stop_type: StopType):
        if stop_type == StopType.HOME:
            DBTransport.save_home_stop_id(user_id, tram_stop_id)
        else:
            DBTransport.save_university_stop_id(user_id, tram_stop_id)
