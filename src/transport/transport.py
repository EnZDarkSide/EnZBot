from typing import List

from .parser import Parser
from .tram import Tram

parser = Parser()


class Transport:
    @staticmethod
    def stop_exists(stop: str) -> bool:
        return stop in parser.get_stops(stop[0].upper())

    @staticmethod
    def get_all_trams(stop_id: int) -> List[Tram]:
        trams = parser.get_trams(stop_id)

        # нужны только трамваи с номерами 14, 25 и 27
        return list(filter(lambda tram: tram.number in (14, 25, 27), trams))
