from unittest import TestCase

from src.transport import Transport


class TestStopExists(TestCase):
    def test_nonexistent_stop(self):
        self.assertFalse(Transport.stop_exists('Остановка'))

    def test_existent_stop(self):
        self.assertTrue(Transport.stop_exists('Ельцина'))
