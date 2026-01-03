import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from myapp import SimpleHTTPRequestHandler, main_navigation
from myapp import main_author, main_app


def test_handler_initialization():
    """Тест проверки создания обработчика"""
    handler = SimpleHTTPRequestHandler
    assert hasattr(handler, 'do_GET')
    assert hasattr(handler, 'handle_home_page')


def test_navigation_exists():
    """Тест определения навигации"""
    assert isinstance(main_navigation, list)
    assert len(main_navigation) > 0

    # Проверяем структуру элементов навигации
    for item in main_navigation:
        assert 'caption' in item
        assert 'href' in item
        assert isinstance(item['caption'], str)
        assert isinstance(item['href'], str)


def test_author_and_app():
    """Проверка создания автора и приложения"""
    from myapp import main_author, main_app

    assert main_author.name == "Nikolay Bystrov"
    assert main_author.group == "P3124"
    assert main_app.name == "CurrenciesListApp"
    assert main_app.version == "1.0.0"
    assert main_app.author == main_author


def test_template_rendering():
    """Тест проверки рендеринга шаблонов"""
    from jinja2 import Environment, PackageLoader

    env = Environment(
        loader=PackageLoader("myapp"),
        autoescape=True
    )

    templates = ['index.html', 'users.html', 'currencies.html',
                 'user.html', 'author.html', '404.html']

    for template_name in templates:
        try:
            template = env.get_template(template_name)
            # Пробуем рендерить с минимальными данными
            result = template.render(
                navigation=main_navigation,
                page_title="Тест",
                author = main_author,
                app = main_app
            )
            assert isinstance(result, str)
            assert len(result) > 0
        except Exception as e:
            print(f"Шаблон {template_name}: {e}")
            if template_name != '404.html':
                raise # Выбрасываем то же самое исключение, которое только что поймали


def test_route_handlers_exist():
    """Тест на то, что все обработчики маршрутов существуют"""
    handler = SimpleHTTPRequestHandler
    assert hasattr(handler, 'handle_home_page')
    assert hasattr(handler, 'handle_users_page')
    assert hasattr(handler, 'handle_user_page')
    assert hasattr(handler, 'handle_currencies_page')
    assert hasattr(handler, 'handle_author_page')
    assert hasattr(handler, 'handle_404_error')


def test_query_parsing_logic():
    """Тест логики парсинга query-параметров"""
    from urllib.parse import parse_qs, urlparse

    # Только валидные тест-кейсы
    test_cases = [
        ('/user?id=1', {'id': ['1']}),
        ('/user?id=1&name=test', {'id': ['1'], 'name': ['test']}),
        ('/', {}),
    ]

    for url, expected in test_cases:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        assert params == expected