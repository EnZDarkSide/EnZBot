import re
from dataclasses import dataclass
from typing import List, Set

import requests
from lxml import html


@dataclass
class Tram:
    number: int
    arrival_time: str
    arrival_distance: str


def parse_trams_from_url(url: str) -> List[Tram]:
    page = requests.get(url)
    tree = html.fromstring(page.text)

    tram_elements = tree.xpath('body/div/div')[:-1]

    # проходится по всем элементам трамвайя — его номер, время прибытия и расстояние до него —,
    # берёт их текст и создаёт объект Tram для каждого из них
    trams = [Tram(*map(lambda el: el.text_content(), tram_element)) for tram_element in tram_elements]

    return trams


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
    def get_all_trams(dom: str) -> List[Tram]:
        url = 'https://online.ettu.ru/station/4350'

        trams = parse_trams_from_url(url)

        # нужны только трамваи с номерами 14, 25 и 27
        return list(filter(lambda tram: tram.number in (14, 25, 27), trams))
