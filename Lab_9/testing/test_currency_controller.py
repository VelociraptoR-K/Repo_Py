import unittest
from unittest.mock import MagicMock
from controllers import CurrencyController

class TestCurrencyController(unittest.TestCase):

    def test_list_currencies(self):
        mock_db = MagicMock()
        mock_db._read.return_value = [{"id":1, "char_code":"USD", "value":90}]
        controller = CurrencyController(mock_db)
        result = controller.list_currencies()
        self.assertEqual(result[0]['char_code'], "USD")
        mock_db._read.assert_called_once()

    def test_update_currency(self):
        """Тестирование метода update_currency."""
        # Создаем mock-объект базы данных
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)

        # Тестируемые данные
        test_char_code = "EUR"
        test_value = 105.5
        result = controller.update_currency(test_char_code, test_value)

        self.assertIsNone(result)
        mock_db._update.assert_called_once()
        mock_db._update.assert_called_with({test_char_code: test_value})

    def test_delete_currency(self):
        """Тестирование метода delete_currency."""
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)

        # Тестируемые данные
        test_currency_id = 5

        result = controller.delete_currency(test_currency_id)
        mock_db._delete.assert_called_once()
        mock_db._delete.assert_called_with(test_currency_id)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()