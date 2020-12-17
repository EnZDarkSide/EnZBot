from typing import Tuple, List
from xml.etree.ElementTree import Element

import requests
from lxml import html
from vbml import Patcher, Pattern

from src.transport.entities.stop import Stop
from src.transport.entities.tram import Tram

base_url = 'https://online.ettu.ru'


class TramParser:

    @staticmethod
    def is_id_valid(stop_id: int) -> bool:
        """Проверяет, если остановка с таким id существует"""

        return requests.get(f'{base_url}/station/{stop_id}').ok

    @staticmethod
    def get_trams(stop_id: int) -> Tuple[Tram]:
        page = requests.get(f'{base_url}/station/{stop_id}')
        tree = html.fromstring(page.text)

        tram_elements = tree.xpath('body/div/div')[:-1]

        # проходится по всем элементам трамвайя — его номер, время прибытия и расстояние до него —,
        # берёт их текст и создаёт объект Tram для каждого из них
        trams = tuple(Tram(*map(lambda el: el.text_content(), tram_element)) for tram_element in tram_elements)

        return trams

    @staticmethod
    def get_stops(first_letter: str) -> List[Stop]:
        """Возвращает объекты Stop по первой букве остановки"""

        tram_stop_els = TramParser._get_stop_elements(first_letter)
        stops = []

        patcher = Patcher()
        pattern = Pattern("<name> (<direction>)")

        for element in tram_stop_els:
            stop_id = int(element.get('href').split('/')[-1])
            stop = patcher.check(element.text, pattern)

            stops.append(Stop(stop_id, stop['name'], stop['direction']))

        return stops

    @staticmethod
    def _get_stop_elements(first_letter: str) -> Tuple[Element]:
        page = requests.get(f'{base_url}/stations/{first_letter.upper()}')
        tree = html.fromstring(page.text)

        # если есть заголовок 'Троллейбусы', то все ссылки,
        # которые сверху этого заголовка, — трамвайные остановки;
        # иначе берутся все ссылки, которые ниже заголовка 'Трамваи'
        tram_stop_els = tree.xpath('//h3[2]/preceding-sibling::a[@href]') \
                        or tree.xpath("//h3[contains(text(), 'Трамваи')][1]/following-sibling::a")

        return tram_stop_els
