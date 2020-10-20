import re
from dataclasses import dataclass
from typing import List, Set

import requests
from lxml import html


@dataclass
class Trolley:
    number: int
    arrival_time: str
    arrival_distance: str


def parse_trolleys_from_url(url: str) -> List[Trolley]:
    page = requests.get(url)
    tree = html.fromstring(page.text)

    trolley_elements = tree.xpath('body/div/div')[:-1]

    # проходится по всем элементам трамвайя — его номер, время прибытия и расстояние до него —,
    # берёт их текст и создаёт объект Trolley для каждого из них
    trolleys = [Trolley(*map(lambda el: el.text_content(), trolley_element)) for trolley_element in trolley_elements]

    return trolleys


def parse_stops(first_letter: str) -> Set[str]:
    url = 'https://online.ettu.ru/stations'

    page = requests.get(f'{url}/{first_letter}')
    tree = html.fromstring(page.text)

    # если есть заголовок 'Троллейбусы', то все ссылки,
    # которые сверху этого заголовка, — трамвайные остановки;
    # иначе берутся все ссылки, которые ниже заголовка 'Трамваи'
    tram_stop_els = tree.xpath('//h3[2]/preceding-sibling::a[@href]') \
                    or tree.xpath('//h3[1]/following-sibling::a')

    # ^((?:\w+ ?)+) \(.*$
    tram_stop_names = set(map(lambda el: re.sub(r'^([^(]+) \(.*$', r'\1', el.text), tram_stop_els))

    return tram_stop_names


class Transport:
    @staticmethod
    def stop_exists(stop: str) -> bool:
        return stop in parse_stops(stop[0].upper())

    @staticmethod
    def get_all_trolleys(dom: str) -> List[Trolley]:
        url = 'https://online.ettu.ru/station/4350'

        trolleys = parse_trolleys_from_url(url)

        # нужны только трамваи с номерами 14, 25 и 27
        return list(filter(lambda trolley: trolley.number in (14, 25, 27), trolleys))
