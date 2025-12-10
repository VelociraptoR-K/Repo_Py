from logger import logger
import requests
import json
import sys

@logger(handle=sys.stdout)
def get_currencies(currency_codes: list, url:str = "https://www.cbr-xml-daily.ru/daily_json.js")->dict:
    """
    Получает курсы валют с API Центробанка России.

    Args:
        currency_codes (list): Список символьных кодов валют (например, ['USD', 'EUR']).

    Returns:
        dict: Словарь, где ключи - символьные коды валют, а значения - их курсы.

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
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError('Некорректный JSON')

    if "Valute" not in data:
        raise KeyError('Нет ключа “Valute”')

    currencies = {}
    for code in currency_codes:
        if code in data["Valute"]:
            if isinstance(data["Valute"][code]["Value"], (int,float)) == False:
                raise TypeError('Курс валюты имеет неверный тип')
            else:
                currencies[code] = data["Valute"][code]["Value"]
        else:
            raise KeyError(f"Валюта {code} отсутствует в данных")

    return currencies

currency_list = ['USD', 'EUR', 'GBP']
currency_data = get_currencies(currency_list)
if currency_data:
    print(currency_data)