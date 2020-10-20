from dataclasses import dataclass
from typing import List

from src.parser import Parser

parser = Parser()


@dataclass
class Tram:
    number: int
    arrival_time: str
    arrival_distance: str


class Transport:
    @staticmethod
    def stop_exists(stop: str) -> bool:
        return stop in parser.get_stops(stop[0].upper())

    @staticmethod
    def get_all_trams(stop_id: int) -> List[Tram]:
        trams = parser.get_trams(stop_id)

        # нужны только трамваи с номерами 14, 25 и 27
        return list(filter(lambda tram: tram.number in (14, 25, 27), trams))
