import re
from typing import List, Iterator

from .parser import Parser
from .tram import Tram

parser = Parser()


class Transport:
    # noinspection PyShadowingNames
    @staticmethod
    def stop_exists(stop: str) -> bool:
        stop = stop.lower()
        stops = map(lambda stop: stop.lower(), parser.get_stops(stop[0]))

        return stop in stops

    @staticmethod
    def get_trams(stop_id: int) -> Iterator[Tram]:
        trams = parser.get_trams(stop_id)

        # нужны только трамваи с номерами 14, 25 и 27
        return filter(lambda tram: tram.number in (14, 25, 27), trams)

    @staticmethod
    def get_directions(tram_stop: str) -> List[str]:
        tram_stop = tram_stop.lower()

        directions = []
        for tram_stop_with_direction in parser.get_raw_stops(tram_stop[0]):
            if direction_match := re.match(rf'^{tram_stop} \(([^)]+)\)$', tram_stop_with_direction,
                                           flags=re.IGNORECASE):
                directions.append(direction_match.group(1))

        return directions