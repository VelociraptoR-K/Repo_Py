import unittest
from currencies import get_currencies


class TestGetCurrencies(unittest.TestCase):

    def test_connection_error(self):
        """Тест ConnectionError с заведомо неверным URL"""
        with self.assertRaises(ConnectionError):
            get_currencies(['USD'], url="https://invalid")

    def test_value_error_invalid_json(self):
        """Тест ValueError при некорректном JSON"""
        # Нужен URL, который вернёт не JSON
        with self.assertRaises(ValueError):
            get_currencies(['USD'], url="https://www.google.com")  # Google вернёт HTML

    def test_key_error_no_valute(self):
        """Тест KeyError при отсутствии ключа Valute"""
        # Нужен URL с JSON, но без ключа "Valute"
        # Можно использовать тестовый JSON
        test_url = "https://httpbin.org/json"
        with self.assertRaises(KeyError):
            get_currencies(['USD'], url=test_url)