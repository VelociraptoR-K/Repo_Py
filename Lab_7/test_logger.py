import unittest
import io
import logging
from logger import logger
from currencies import get_currencies


class TestLoggerDecorator(unittest.TestCase):

    def test_error_logging_with_logging(self):
        """Тест логирования ошибки с logging.Logger"""

        # Создаём логгер с обработчиком в память
        stream = io.StringIO()

        handler = logging.StreamHandler(stream)
        handler.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)

        log = logging.getLogger("test_error")
        log.setLevel(logging.ERROR)
        log.addHandler(handler)

        # Отключаем распространение в корневой логгер
        log.propagate = False

        @logger(handle=log)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")

        with self.assertRaises(ConnectionError):
            wrapped()

        logs = stream.getvalue()
        print(f"DEBUG logs: {repr(logs)}")  # Для отладки

        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)

    def test_successful_execution_logging(self):
        """Тест логирования при успешном выполнении"""

        stream = io.StringIO()
        @logger(handle=stream)
        def test_func(x, y=10):
            return x + y
        result = test_func(5, y=3)

        logs = stream.getvalue()
        # Проверяем сообщение о старте
        self.assertIn("Calling test_func", logs)
        self.assertIn("args=(5,)", logs)
        self.assertIn("kwargs={'y': 3}", logs)
        # Проверяем сообщение об окончании
        self.assertIn("test_func returned 8", logs)
        # Проверяем результат функции
        self.assertEqual(result, 8)

    def test_error_logging(self):
        """Тест логирования при ошибке"""

        stream = io.StringIO()
        @logger(handle=stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")
        with self.assertRaises(ConnectionError):
            wrapped()

        logs = stream.getvalue()
        self.assertIn("ConnectionError", logs)
        self.assertIn("API недоступен", logs)

if __name__ == '__main__':
    unittest.main()