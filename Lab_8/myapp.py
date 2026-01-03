from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency, UserCurrency
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from utils.currencies_api import get_currencies, get_historical_data
import time
import json

env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")
template_author = env.get_template("author.html")
template_404 = env.get_template("404.html")

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
data= []

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
            current_time = time.strftime("%H:%M:%S")
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
                    # Получаем текущие курсы валют
                    currencies = self.get_all_currencies()

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
                                    'subscribed_at': time.strftime("%Y-%m-%d", time.localtime(subscription.subscribed_at))
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
        Получает ID валюты по её коду.
        """
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

    def get_all_currencies(self, force_update: bool = False):
        """
        Получает ВСЕ валюты
        Args:
            force_update: принудительное обновление данных
        Returns:
            Список объектов Currency или None при ошибке
        """
        current_time = time.time()

        # Проверяем, нужно ли обновлять кэш
        if (force_update or cache['data'] is None or current_time - cache['last_update'] > cache['cache_duration']):
            print("Получение валют из Центробанка...")

            try:
                codes = get_currencies() # Специально вызываем без аргументов для получения списка валют
                currencies_data = get_currencies(codes)
                currencies = []
                currency_id = 1

                for el in currencies_data:
                    c = Currency(
                        id=currency_id,
                        num_code=el['num_code'],
                        char_code=el['code'],
                        name=el['name'],
                        value=el['value'],
                        nominal=el['nominal']
                    )
                    currencies.append(c)
                    currency_id += 1

                # Обновляем кэш
                cache['data'] = currencies
                cache['last_update'] = current_time

            except Exception as e:
                print(f"Ошибка при получении валют: {e}")
                if cache['data'] is None:
                    return None
        return cache['data']

    def handle_currencies_page(self, query_params):
        """Страница ВСЕХ валют."""
        # Проверяем, запрошено ли принудительное обновление
        update = 'refresh' in query_params

        currencies = self.get_all_currencies(update)

        # Форматируем время последнего обновления
        last_update = time.strftime("%H:%M:%S", time.localtime(cache['last_update']))

        html_content = template_currencies.render(
            navigation=main_navigation,
            currencies=currencies,
            page_title="Список валют",
            last_update=last_update,
            update_status=update
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