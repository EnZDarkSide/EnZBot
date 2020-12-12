import re
from typing import List, Iterator, Tuple

from .entities.tram import Tram
from .entities.stop import Stop
from .parser import TramParser
from ..database.enitities.Transport import DBTransport
from ..utils import StopType

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
    def get_trams(stop_id: int) -> Iterator[Tram]:
        trams = parser.get_trams(stop_id)

        # нужны только трамваи с номерами 14, 25 и 27
        return filter(lambda tram: tram.number in (14, 25, 27), trams)

    @staticmethod
    def get_stops(stop_first_letter: str) -> Tuple[Stop]:
        def stop_name_and_direction(raw_stop):
            stop_match = re.match(rf'^(\d+) \(([^)]+)\)$', tram_stop_with_direction,
                                  flags=re.IGNORECASE)
            if stop_match:
                stop_name = stop_match.group(1)
                stop_direction = stop_match.group(2)

            return tuple(stop_name, stop_direction)

        raw_stops = parser.get_stops_title_and_id(stop_first_letter)

        stop_names, stop_directions = map(stop_name_and_direction, raw_stops)
        stop_ids = map(lambda raw_stop: raw_stop[1], raw_stops)

        stops = tuple(map(lambda stop_tuple: Stop(stop_tuple[0], stop_tuple[1], stop_tuple[2]),
                          zip(stop_ids, stop_names, stop_directions)))

        return stops

    @staticmethod
    def from_dorm_to_university():
        trams = parser.get_trams(4350)
        return trams

    @staticmethod
    def from_university_to_dorm():
        trams = parser.get_trams(3473)
        return list(filter(lambda tram: tram.number in ['14', '25', '27'], trams))

    @staticmethod
    def get_directions(tram_stop: str) -> List[str]:
        tram_stop = tram_stop.lower()

        directions = []
        for tram_stop_with_direction in parser.get_raw_stops(tram_stop[0]):
            direction_match = re.match(rf'^{tram_stop} \(([^)]+)\)$', tram_stop_with_direction,
                                       flags=re.IGNORECASE)
            if direction_match:
                directions.append(direction_match.group(1))

        return directions

    @staticmethod
    def save_tram_stop_id(user_id: int, tram_stop_id: int, stop_type: StopType):
        if stop_type == StopType.HOME:
            DBTransport.save_home_stop_id(user_id, tram_stop_id)
        else:
            DBTransport.save_university_stop_id(user_id, tram_stop_id)
