from unittest import TestCase

from src.transport.parser import TramParser


class TestGetStops(TestCase):
    def setUp(self):
        self.parser = TramParser()

    def test_one_stop_only(self):
        self.assertSetEqual(self.parser.get_stops('Е'), {'Ельцина'})

    def test_stop_name_contains_numbers(self):
        self.assertSetEqual(self.parser.get_stops('1'), {'1-й км'})

    def test_stop_name_with_more_than_one_word(self):
        self.assertSetEqual(self.parser.get_stops('А'),
                            {'Автовокзал', 'Автомагистральная', 'Академия при Президенте России'})

    def test_stop_name_contains_non_letter_characters(self):
        self.assertSetEqual(self.parser.get_stops('Ю'), {'Ювелирная', 'Юго-Западная', 'Южная'})

    def test_stop_on_page_with_no_trolley_header(self):
        self.assertSetEqual(self.parser.get_stops('7'), {'7 Ключей'})

    def test_stop_on_page_with_no_trams_on_it(self):
        self.assertSetEqual(self.parser.get_stops('Я'), set())

    def test_stop_names_with_no_parenthesis(self):
        stop_names = {
            'Ватутина',
            'Верх-Исетский б-р',
            'Верх-Исетский рынок',
            'Вечный Огонь',
            'ВИЗ',
            'Викулова',
            'Войкова',
            'Волгоградская',
            'Ворошиловская',
            'Восточная',
            'Вторчермет'
        }

        self.assertSetEqual(self.parser.get_stops('В'), stop_names)
