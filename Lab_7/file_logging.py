import logging
from logger import logger
from currencies import get_currencies

# Очистка старых обработчиков
logging.root.handlers.clear()

# Полная настройка
file_logger = logging.getLogger("currency")
file_logger.setLevel(logging.DEBUG)

# Удаляем старые обработчики у этого логгера
file_logger.handlers.clear()

# Файловый обработчик
file_handler = logging.FileHandler("currency.log", mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

# Форматтер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик
file_logger.addHandler(file_handler)

# Отключаем распространение
file_logger.propagate = False

@logger(handle=file_logger)
def get_currencies_file(currency_codes: list, url:str="https://www.cbr-xml-daily.ru/daily_json.js")->dict:
    """Версия с файловым логированием"""
    return get_currencies(currency_codes,url)


if __name__ == "__main__":

    try:
        result = get_currencies_file(['USD', 'EUR'])
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")

    with open("currency.log", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
