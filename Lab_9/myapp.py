from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency, UserCurrency
from controllers import CurrencyRatesCRUD
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utils.currencies_api import get_currencies, get_historical_data
import time
import json

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)


class CurrencyRatesMock():
    """Mock-объект для обратной совместимости."""

    def __init__(self):
        self.__values = []

    @property
    def values(self):
        return self.__values


def load_currencies_from_api():
    """
    Загружает данные о валютах из API Центробанка.

    Returns:
        List[Dict[str, Any]]: список словарей с данными о валютах
    """
    try:
        # Получаем все доступные коды валют
        all_codes = get_currencies()

        # Получаем полную информацию о валютах
        currencies_info = get_currencies(all_codes)

        # Преобразуем в формат для базы данных
        data = []
        for currency in currencies_info:
            data.append({
                "num_code": str(currency['num_code']),
                "char_code": currency['code'],
                "name": currency['name'],
                "value": float(currency['value']),
                "nominal": int(currency['nominal'])
            })

        return data
    except Exception as e:
        print(f"Ошибка при загрузке валют из API: {e}")
        # Возвращаем тестовые данные при ошибке
        return [
            {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
            {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 98.0, "nominal": 1},
            {"num_code": "826", "char_code": "GBP", "name": "Фунт стерлингов", "value": 115.0, "nominal": 1},
        ]


# Создаем mock объект для обратной совместимости
c_r = CurrencyRatesMock()

# Создаем контроллер БД
c_r_controller = CurrencyRatesCRUD(c_r)

# Загружаем реальные данные из API и добавляем в БД
currencies_data = load_currencies_from_api()
if currencies_data:
    c_r_controller._create(currencies_data)
else:
    # Если не удалось загрузить данные, используем тестовые
    c_r_controller._create()

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")
template_author = env.get_template("author.html")
template_404 = env.get_template("404.html")
template_currency_show = env.get_template("currency_show.html")

main_author = Author('Nikolay Bystrov', 'P3124')
main_app = App("CurrenciesListApp", "1.0.0", main_author)

# Общая навигация для всех страниц
main_navigation = [
    {'caption': 'Основная страница', 'href': "/"},
    {'caption': 'Об авторе', 'href': '/author'},
    {'caption': 'Пользователи', 'href': '/users'},
    {'caption': 'Валюты', 'href': '/currencies'},
]

# Кэш для курсов валют
cache = {
    'data': None,
    'last_update': 0,
    'cache_duration': 300,  # 5 минут в секундах
}
data = []


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Парсим URL для маршрутизации
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Маршрутизация
        if path == '/':
            self.handle_home_page()
        elif path == '/users':
            self.handle_users_page()
        elif path == '/user':
            self.handle_user_page(query_params)
        elif path == '/currencies':
            self.handle_currencies_page(query_params)
        elif path == '/author':
            self.handle_author_page()
        elif path == '/currency/delete':
            self.handle_currency_delete(query_params)
        elif path == '/currency/show':
            self.handle_currency_show()
        elif path == '/currency/update':
            self.handle_currency_update(query_params)
        else:
            self.handle_404_error()

    def send_html_response(self, html_content: str, status_code: int = 200):
        """Универсальный метод отправки HTML."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(html_content.encode('utf-8')))

    def handle_home_page(self):
        """Главная страница - рендерим шаблон index.html"""
        html_content = template_index.render(
            myapp="CurrenciesListApp",
            navigation=main_navigation,
            author_name=main_author.name,
            group=main_author.group,
            current_time=time.strftime("%H:%M:%S"),
            currencies=c_r_controller._read()
        )
        self.send_html_response(html_content)

    def handle_users_page(self):
        """Страница пользователей - рендерим шаблон users.html"""
        # Тестовые данные пользователей
        users = [
            User(1, "Иван Смирнов", "ivan@example.com"),
            User(2, "Мария Петрова", "maria@example.com"),
            User(3, "Алексей Сидоров", "alex@example.com"),
        ]
        html_content = template_users.render(
            navigation=main_navigation,
            users=users,
            page_title="Список пользователей"
        )
        self.send_html_response(html_content)

    def handle_user_page(self, query_params):
        """Страница конкретного пользователя с графиком подписок - рендерим шаблон user.html"""
        user_id = query_params.get('id', [None])[0]
        if not user_id:
            html_content = template_user.render(
                navigation=main_navigation,
                error_message="Не указан ID пользователя",
                page_title="Ошибка"
            )
            self.send_html_response(html_content)
        else:
            try:
                user_id_int = int(user_id)
                if user_id_int == 1:
                    user = User(1, "Иван Смирнов", "ivan@example.com")
                    user_subscriptions = [
                        UserCurrency(1, 1, self.get_currency_id_by_code('USD')),
                        UserCurrency(2, 1, self.get_currency_id_by_code('EUR')),
                        UserCurrency(3, 1, self.get_currency_id_by_code('GBP')),
                    ]
                elif user_id_int == 2:
                    user = User(2, "Мария Петрова", "maria@example.com")
                    user_subscriptions = [
                        UserCurrency(4, 2, self.get_currency_id_by_code('USD')),
                        UserCurrency(5, 2, self.get_currency_id_by_code('JPY')),
                    ]
                elif user_id_int == 3:
                    user = User(3, "Алексей Сидоров", "alex@example.com")
                    user_subscriptions = [
                        UserCurrency(6, 3, self.get_currency_id_by_code('EUR')),
                        UserCurrency(7, 3, self.get_currency_id_by_code('CNY')),
                    ]
                else:
                    user = None
                    user_subscriptions = []

                if user:
                    # Получаем все валюты из базы данных
                    currencies_data = c_r_controller._read()
                    currencies = []

                    # Преобразуем данные из БД в объекты Currency
                    for data in currencies_data:
                        try:
                            currency = Currency(
                                id=data['id'],
                                num_code=int(data['num_code']),
                                char_code=data['char_code'],
                                name=data['name'],
                                value=data['value'],
                                nominal=data['nominal']
                            )
                            currencies.append(currency)
                        except ValueError as e:
                            print(f"Ошибка при создании объекта Currency: {e}")
                            continue

                    # Фильтруем валюты, на которые подписан пользователь
                    subscribed_currencies = []
                    for subscription in user_subscriptions:
                        for currency in currencies:
                            if currency.id == subscription.currency_id:
                                # Получаем исторические данные для графика
                                historical_data = get_historical_data(currency.char_code, 90)
                                subscribed_currencies.append({
                                    'currency': currency,
                                    'historical_data': historical_data,
                                    'subscribed_at': time.strftime("%Y-%m-%d",
                                                                   time.localtime(subscription.subscribed_at))
                                })
                                break

                    # Подготавливаем данные для графика
                    chart_data = self.prepare_chart_data(subscribed_currencies)

                    html_content = template_user.render(
                        navigation=main_navigation,
                        user=user,
                        subscribed_currencies=subscribed_currencies,
                        chart_data=json.dumps(chart_data),  # JSON для JavaScript
                        page_title=f"Пользователь #{user.id}"
                    )
                else:
                    html_content = template_user.render(
                        navigation=main_navigation,
                        error_message=f"Пользователь с ID {user_id} не найден",
                        page_title="Ошибка"
                    )

            except ValueError:
                html_content = template_user.render(
                    navigation=main_navigation,
                    error_message="Неверный формат ID пользователя",
                    page_title="Ошибка"
                )
            self.send_html_response(html_content)

    def get_currency_id_by_code(self, currency_code: str) -> int:
        """
        Получает ID валюты по её коду из базы данных.

        Args:
            currency_code: символьный код валюты

        Returns:
            int: ID валюты или 1 по умолчанию если не найдена
        """
        try:
            currency_data = c_r_controller._read(currency_code)
            if currency_data and len(currency_data) > 0:
                return currency_data[0]['id']
        except Exception:
            pass

        # Запасной вариант если не нашли в базе
        currency_map = {
            'USD': 1, 'EUR': 2, 'GBP': 3, 'JPY': 4,
            'CNY': 5, 'CHF': 6, 'CAD': 7, 'AUD': 8
        }
        return currency_map.get(currency_code, 1)

    def prepare_chart_data(self, subscribed_currencies: list):
        """
        Подготавливает данные для графика.

        Args:
            subscribed_currencies: список словарей с валютой и историческими данными

        Returns:
            dict: данные для Chart.js
        """
        if not subscribed_currencies:
            return {'datasets': [], 'labels': []}

        # Используем даты из первой валюты
        first_currency = subscribed_currencies[0]
        labels = [data['date'] for data in first_currency['historical_data']]

        datasets = []
        colors = [
            'rgba(255, 99, 132, 0.8)',  # Красный
            'rgba(54, 162, 235, 0.8)',  # Синий
            'rgba(255, 206, 86, 0.8)',  # Жёлтый
            'rgba(75, 192, 192, 0.8)',  # Зелёный
            'rgba(153, 102, 255, 0.8)',  # Фиолетовый
        ]

        for i, item in enumerate(subscribed_currencies):
            currency = item['currency']
            historical_data = item['historical_data']

            # Извлекаем значения курса
            values = [data['value'] for data in historical_data]

            datasets.append({
                'label': f"{currency.char_code} ({currency.name})",
                'data': values,
                'borderColor': colors[i % len(colors)],
                'backgroundColor': colors[i % len(colors)].replace('0.8', '0.1'),
                'borderWidth': 2,
                'fill': True,
                'tension': 0.4  # Сглаживание кривой
            })

        return {
            'labels': labels,
            'datasets': datasets
        }

    def handle_currencies_page(self, query_params):
        """Страница ВСЕХ валют."""
        # Получаем валюты из базы данных
        currencies_data = c_r_controller._read()
        currencies = []

        # Преобразуем данные в объекты Currency для шаблона
        for data in currencies_data:
            try:
                currency = Currency(
                    id=data['id'],
                    num_code=int(data['num_code']),
                    char_code=data['char_code'],
                    name=data['name'],
                    value=data['value'],
                    nominal=data['nominal']
                )
                currencies.append(currency)
            except ValueError as e:
                print(f"Ошибка при создании объекта Currency: {e}")
                continue

        # Проверяем, запрошено ли принудительное обновление
        update = 'refresh' in query_params
        if update:
            # Обновляем данные из API
            currencies_data = load_currencies_from_api()
            if currencies_data:
                # Очищаем таблицу и загружаем новые данные
                c_r_controller.__cursor.execute("DELETE FROM currency")
                c_r_controller._create(currencies_data)

                # Обновляем список валют
                currencies_data = c_r_controller._read()
                currencies = []
                for data in currencies_data:
                    try:
                        currency = Currency(
                            id=data['id'],
                            num_code=int(data['num_code']),
                            char_code=data['char_code'],
                            name=data['name'],
                            value=data['value'],
                            nominal=data['nominal']
                        )
                        currencies.append(currency)
                    except ValueError as e:
                        print(f"Ошибка при создании объекта Currency: {e}")
                        continue

        html_content = template_currencies.render(
            navigation=main_navigation,
            currencies=currencies,
            page_title="Список валют",
            last_update=time.strftime("%H:%M:%S"),
            update_status="Обновлено" if update else ""
        )
        self.send_html_response(html_content)

    def handle_author_page(self):
        """Страница автора - рендерим шаблон author.html"""
        html_content = template_author.render(
            navigation=main_navigation,
            author=main_author,
            app=main_app,
            page_title="Об авторе"
        )
        self.send_html_response(html_content)

    def handle_currency_delete(self, query_params):
        """Обработка удаления валюты"""
        currency_id = query_params.get('id', [None])[0]
        if currency_id:
            try:
                c_r_controller._delete(int(currency_id))
                result = f"Валюта с ID {currency_id} успешно удалена"
            except Exception as e:
                result = f"Ошибка при удалении валюты: {e}"
        else:
            result = "Не указан ID валюты"

        html_content = template_index.render(
            navigation=main_navigation,
            myapp="CurrenciesListApp",
            author_name=main_author.name,
            group=main_author.group,
            current_time=time.strftime("%H:%M:%S"),
            currencies=c_r_controller._read(),
            result=result
        )
        self.send_html_response(html_content)

    def handle_currency_show(self):
        """Обработка показа всех валют - используем шаблон currency_show.html"""
        data = c_r_controller._read()
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        html_content = template_currency_show.render(
            json_data=json_data
        )
        self.send_html_response(html_content)

    def handle_currency_update(self, query_params):
        """Обработка обновления курса валюты"""

        result = ""
        updated_currency = None
        new_value = None

        # Перебираем все параметры запроса
        for param_name, param_values in query_params.items():
            if param_values and param_values[0]:
                # Проверяем, является ли параметр кодом валюты (3 буквы)
                if len(param_name) == 3 and param_name.isalpha():
                    try:
                        currency_code = param_name.upper()
                        new_value = float(param_values[0])

                        # Проверяем, существует ли валюта в базе
                        existing_currency = c_r_controller._read(currency_code)

                        if existing_currency:
                            # Обновляем курс валюты
                            success = c_r_controller._update({currency_code: new_value})
                            if success:
                                currency_name = existing_currency[0]['name']
                                result = f'Курс {currency_name} ({currency_code}) успешно обновлен на {new_value}'
                                updated_currency = currency_code
                            else:
                                result = f'Не удалось обновить курс {currency_code}'
                        else:
                            result = f'Валюта с кодом {currency_code} не найдена в базе данных'

                        # Прерываем цикл после первой найденной валюты
                        break

                    except ValueError:
                        result = f'Некорректное значение курса для {param_name} (должно быть числом)'
                        break

        if not result:
            result = 'Не указаны параметры обновления (например: /currency/update?USD=95.5 или /currency/update?EUR=105.3)'

        html_content = template_index.render(
            navigation=main_navigation,
            myapp="CurrenciesListApp",
            author_name=main_author.name,
            group=main_author.group,
            current_time=time.strftime("%H:%M:%S"),
            currencies=c_r_controller._read(),
            result=result
        )
        self.send_html_response(html_content)

    def handle_404_error(self):
        """Страница ошибки 404 - рендерим шаблон 404.html"""
        html_content = template_404.render(
            navigation=main_navigation,
            page_title="404 - Страница не найдена",
            requested_path=self.path
        )
        self.send_html_response(html_content, 404)


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
    print('server is running')
    print("Сервер запущен на http://localhost:8080")
    httpd.serve_forever()
