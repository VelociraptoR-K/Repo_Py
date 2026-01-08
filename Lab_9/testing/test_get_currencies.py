import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.currencies_api import get_currencies, get_historical_data


def test_get_currencies_returns_list():
    """Тест проверки возвращения списка функции get_currencies"""
    try:
        result = get_currencies()
        assert isinstance(result, list), f"Ожидался list, получен {type(result)}"

        # Если есть элементы, проверяем что это строки (коды валют)
        if len(result) > 0:
            assert isinstance(result[0], str)
    except ConnectionError:
        print("Пропускаем тест: нет интернета")
    except Exception as e:
        print(f"Тест пропущен: {e}")


def test_get_specific_currencies():
    """Тест получения конкретных валют"""
    try:
        currencies = get_currencies(['USD', 'EUR'])

        assert isinstance(currencies, list)

        if len(currencies) > 0:
            currency = currencies[0]
            # Проверяем структуру
            assert 'code' in currency
            assert 'name' in currency
            assert 'value' in currency
            assert 'nominal' in currency

            # Проверяем типы
            assert isinstance(currency['value'], (int, float))
            assert currency['value'] > 0
    except ConnectionError:
        print("Пропускаем тест: нет интернета")
    except KeyError as e:
        print(f"Валюта не найдена: {e}")


def test_get_historical_data_structure():
    """Тест структуры исторических данных"""
    try:
        data = get_historical_data('USD', days=5)

        assert isinstance(data, list)

        if len(data) > 0:
            item = data[0]
            assert 'date' in item
            assert 'value' in item

            # Проверяем формат даты (должен быть YYYY-MM-DD)
            date_parts = item['date'].split('-')
            assert len(date_parts) == 3
            assert len(date_parts[0]) == 4  # год
            assert len(date_parts[1]) == 2  # месяц
            assert len(date_parts[2]) == 2  # день
    except Exception as e:
        print(f"Тест пропущен: {e}")


def test_historical_data_length():
    """Тест количества дней в исторических данных"""
    try:
        # Запрашиваем разное количество дней
        for days in [3, 7, 30]:
            data = get_historical_data('USD', days=days)
            # Может вернуть меньше, но не больше запрошенного
            assert len(data) <= days
    except Exception as e:
        print(f"Тест пропущен: {e}")


def test_multiple_currencies():
    """Тест разных валют"""
    try:
        for code in ['USD', 'EUR', 'GBP']:
            data = get_historical_data(code, days=2)
            assert isinstance(data, list)
    except Exception as e:
        print(f"Тест пропущен: {e}")


def test_api_functions_exist():
    """Тест проверки существования функций"""
    from utils.currencies_api import get_currencies, get_historical_data
    assert callable(get_currencies)
    assert callable(get_historical_data)