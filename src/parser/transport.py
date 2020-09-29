from dataclasses import dataclass

from lxml import html
import requests
from typing import List


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


class Transport:
    @staticmethod
    def get_all_trolleys(dom: str) -> List[Trolley]:
        url = 'https://online.ettu.ru/station/4350'

        trolleys = parse_trolleys_from_url(url)

        # нужны только трамваи с номерами 14, 25 и 27
        return list(filter(lambda trolley: trolley.number in (14, 25, 27), trolleys))
