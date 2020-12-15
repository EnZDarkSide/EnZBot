from typing import Tuple
from xml.etree.ElementTree import Element

import requests
from lxml import html
from vbml import Patcher, Pattern

from src.transport.entities.stop import Stop
from src.transport.entities.tram import Tram

base_url = 'https://online.ettu.ru'


class TramParser:

    @staticmethod
    def get_stop_elements(first_letter: str) -> Tuple[Element]:
        page = requests.get(f'{base_url}/stations/{first_letter.upper()}')
        tree = html.fromstring(page.text)

        # если есть заголовок 'Троллейбусы', то все ссылки,
        # которые сверху этого заголовка, — трамвайные остановки;
        # иначе берутся все ссылки, которые ниже заголовка 'Трамваи'
        tram_stop_els = tree.xpath('//h3[2]/preceding-sibling::a[@href]') \
                        or tree.xpath("//h3[contains(text(), 'Трамваи')][1]/following-sibling::a")

        return tram_stop_els

    @staticmethod
    def get_trams(stop_id: int) -> Tuple[Tram]:
        page = requests.get(f'{base_url}/station/{stop_id}')
        tree = html.fromstring(page.text)

        tram_elements = tree.xpath('body/div/div')[:-1]

        # проходится по всем элементам трамвайя — его номер, время прибытия и расстояние до него —,
        # берёт их текст и создаёт объект Tram для каждого из них
        trams = tuple(Tram(*map(lambda el: el.text_content(), tram_element)) for tram_element in tram_elements)

        return trams

    # возвращает названия остановок с их направлением
    @staticmethod
    def get_raw_stops(first_letter: str) -> Tuple[str]:
        tram_stop_els = TramParser.get_stop_elements(first_letter)
        tram_stops_with_directions = tuple(map(lambda el: str(el.text or ''), tram_stop_els))

        return tram_stops_with_directions

    # возвращает названия остановок
    @staticmethod
    def get_stops(first_letter: str) -> [Stop]:
        tram_stop_els = TramParser.get_stop_elements(first_letter)
        result = []

        patcher = Patcher()
        pattern = Pattern("<stop_name> (<stop_direction>)")

        for element in tram_stop_els:
            stop_id = element.get('href').split('/')[-1]
            check = patcher.check(element.text, pattern)
            result.append(Stop(id=stop_id, name=check['stop_name'], direction=check['stop_direction']))

        return result
