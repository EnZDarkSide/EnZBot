import re
from typing import Set, Tuple
from xml.etree.ElementTree import Element

import requests
from lxml import html

from src.transport.entities.tram import Tram


class TramParser:
    def __init__(self):
        self.base_url = 'https://online.ettu.ru'

    def get_stop_elements(self, first_letter: str) -> Tuple[Element]:
        page = requests.get(f'{self.base_url}/stations/{first_letter.upper()}')
        tree = html.fromstring(page.text)

        # если есть заголовок 'Троллейбусы', то все ссылки,
        # которые сверху этого заголовка, — трамвайные остановки;
        # иначе берутся все ссылки, которые ниже заголовка 'Трамваи'
        tram_stop_els = tree.xpath('//h3[2]/preceding-sibling::a[@href]') \
                        or tree.xpath("//h3[contains(text(), 'Трамваи')][1]/following-sibling::a")

        return tram_stop_els

    def get_trams(self, stop_id: int) -> Tuple[Tram]:
        page = requests.get(f'{self.base_url}/station/{stop_id}')
        tree = html.fromstring(page.text)

        tram_elements = tree.xpath('body/div/div')[:-1]

        # проходится по всем элементам трамвайя — его номер, время прибытия и расстояние до него —,
        # берёт их текст и создаёт объект Tram для каждого из них
        trams = tuple(Tram(*map(lambda el: el.text_content(), tram_element)) for tram_element in tram_elements)

        return trams

    # возвращает названия остановок с их направлением
    def get_raw_stops(self, first_letter: str) -> Tuple[str]:
        tram_stop_els = self.get_stop_elements(first_letter)
        tram_stops_with_directions = tuple(map(lambda el: str(el.text or ''), tram_stop_els))

        return tram_stops_with_directions

    # возвращает названия остановок
    def get_stops(self, first_letter: str) -> Set[str]:
        tram_stop_els = self.get_raw_stops(first_letter)

        # ^((?:\w+ ?)+) \(.*$
        tram_stop_names = set(map(lambda el: re.sub(r'^([^(]+) \(.*$', r'\1', el.text), tram_stop_els))

        return tram_stop_names

    def get_stops_title_and_id(self, first_letter: str) -> Tuple[Tuple[str, int]]:
        tram_stop_els = self.get_stop_elements(first_letter)

        tram_stops_titles = tuple(map(lambda el: str(el.text or ''), tram_stop_els))
        tram_stops_ids = tuple(map(lambda el: int(el.get('href') or ''), tram_stop_els))

        return tuple(zip(tram_stops_titles, tram_stops_ids))
