from logger import logger
import requests
import json
import sys
from datetime import datetime, timedelta
import random

@logger(handle=sys.stdout)
def get_currencies(currency_codes=None, url: str = "https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes:
            - None: возвращает список всех кодов валют
            - list: возвращает список словарей с полной информацией о валютах

    Returns:
        list: список словарей с полной информацией о валютах

    Raises:
        ConnectionError: API недоступен
        ValueError: Некорректный JSON
        KeyError: Нет ключа "Valute" или валюта отсутствует
        TypeError: Курс валюты имеет неверный тип
    """
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        raise ConnectionError('API недоступен')

    try:
        response.raise_for_status()
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError('Некорректный JSON')

    if "Valute" not in data:
        raise KeyError('Нет ключа "Valute"')

    # Если currency_codes не указан - возвращаем список всех кодов
    if currency_codes is None:
        return list(data["Valute"].keys())

    # Если передан список кодов - возвращаем полную информацию
    currencies_info = []
    for code in currency_codes:
        if code in data["Valute"]:
            currency_data = data["Valute"][code]

            if not isinstance(currency_data["Value"], (int, float)):
                raise TypeError(f'Курс валюты {code} имеет неверный тип')

            currencies_info.append({
                'code': code,
                'num_code': int(currency_data['NumCode']),
                'name': currency_data['Name'],
                'value': currency_data['Value'],
                'nominal': int(currency_data['Nominal'])
            })
        else:
            raise KeyError(f"Валюта {code} отсутствует в данных")

    return currencies_info


def get_historical_data(currency_code: str, days: int = 90) -> list:
    """
    Получает исторические данные о курсе валюты.

    Args:
        currency_code: код валюты (например, 'USD')
        days: количество дней истории (максимум 90)

    Returns:
        list: список словарей с данными [{'date': '2025-12-05', 'value': 93.5}, ...]
    """

    # Для быстрой демонстрации работы прикрепляю версию с тестовыми данными
    # return generate_test_historical_data(currency_code, days)

    # ДОЛГАЯ, НО РАБОЧАЯ ВЕРСИЯ
    try:
        # API для исторических данных
        base_url = "https://www.cbr-xml-daily.ru/"

        # Получаем данные за последние N дней
        historical_data = []

        for i in range(days):
            # Формируем дату (сегодня минус i дней)
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y/%m/%d")

            try:
                # Пробуем получить данные за конкретную дату
                url = f"{base_url}archive/{date_str}/daily_json.js"
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    if currency_code in data['Valute']:
                        historical_data.append({
                            'date': date.strftime("%Y-%m-%d"),
                            'value': data['Valute'][currency_code]['Value']
                        })
            except:
                # Если данных за эту дату нет, пропускаем
                continue

        # Если не получили исторических данных, генерируем тестовые
        if not historical_data:
            return generate_test_historical_data(currency_code, days)

        return historical_data[::-1]  # Возвращаем в хронологическом порядке

    except Exception as e:
        print(f"Ошибка при получении исторических данных: {e}")
        return generate_test_historical_data(currency_code, days)


def generate_test_historical_data(currency_code: str, days: int = 90) -> list:
    """
    Генерирует тестовые исторические данные.

    Args:
        currency_code: код валюты
        days: количество дней

    Returns:
        list: тестовые исторические данные
    """

    base_values = {
        'USD': 90.0,
        'EUR': 98.0,
        'GBP': 115.0,
        'JPY': 0.60,
        'CNY': 12.5,
    }

    base_value = base_values.get(currency_code, 80.0)
    historical_data = []

    for i in range(days):
        date = datetime.now() - timedelta(days=days - i - 1)

        # Генерируем случайное изменение курса (±5%)
        change = random.uniform(-0.05, 0.05)
        value = base_value * (1 + change)

        historical_data.append({
            'date': date.strftime("%Y-%m-%d"),
            'value': round(value, 4)
        })
    return historical_data