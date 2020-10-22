from unittest import TestCase

from src.transport import Transport


class TestStopExists(TestCase):
    def test_nonexistent_stop(self):
        self.assertFalse(Transport.stop_exists('Остановка'))

    def test_existent_stop(self):
        self.assertTrue(Transport.stop_exists('Ельцина'))


class TestGetDirections(TestCase):
    def test_stop_has_no_directions(self):
        self.assertListEqual(Transport.get_directions('40 лет ВЛКСМ'), [])

    def test_stop_has_two_directions(self):
        self.assertListEqual(Transport.get_directions('1-й км'), ['на Пионерскую', 'на Техучилище'])

    def test_stop_has_four_directions(self):
        self.assertListEqual(Transport.get_directions('Блюхера'), [
            'на ст.Шарташ',
            'с Мира на Уральский федеральный университет',
            'с Советской на Уральский федеральный университет',
            'на Пионерскую'
        ])
