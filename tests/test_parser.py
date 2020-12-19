from unittest import TestCase

from src.transport.entities.stop import Stop
from src.transport.parser import TramParser


class TestGetStops(TestCase):

    def test_no_stops_available(self):
        self.assertListEqual(TramParser.get_stops('2'), [])

    def test_regular_case(self):
        self.assertListEqual(TramParser.get_stops('1'), [
            Stop(1168, '1-й км', 'на Пионерскую'),
            Stop(1169, '1-й км', 'на Техучилище'),
        ])

    def test_stop_has_no_direction(self):
        self.assertListEqual(TramParser.get_stops('4'), [
            Stop(3497, '40 лет ВЛКСМ', None),
            Stop(1170, '40 лет Октября', 'на Диагностический центр'),
            Stop(1171, '40 лет Октября', 'на ст. Машиностроителей')
        ])
