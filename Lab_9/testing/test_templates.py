import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from jinja2 import Environment, FileSystemLoader

# Настройка Jinja2
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def test_index_template_variables():
    """Тест передачи переменных в index.html"""
    template = env.get_template('index.html')

    result = template.render(
        myapp="Тестовое приложение",
        author_name="Иван",
        group="P3124",
        navigation=[{'caption': 'Главная', 'href': '/'}],
        currencies=[],
        result="",
        current_time="12:00:00"
    )

    assert "Тестовое приложение" in result
    assert "Иван" in result
    assert "P3124" in result
    assert "Главная" in result
    assert 'href="/"' in result


def test_users_template():
    """Тест шаблона users.html с циклом"""
    template = env.get_template('users.html')

    users = [
        {'id': 1, 'name': 'Иван', 'email': 'ivan@test.com'},
        {'id': 2, 'name': 'Мария', 'email': 'maria@test.com'}
    ]

    result = template.render(
        navigation=[],
        users=users,
        page_title="Пользователи"
    )

    assert 'Иван' in result
    assert 'Мария' in result
    assert 'ivan@test.com' in result
    assert 'href="/user?id=1"' in result
    assert 'href="/user?id=2"' in result


def test_currencies_template_conditions():
    """Тест условий в currencies.html"""
    template = env.get_template('currencies.html')

    # Тест с данными
    result_with_data = template.render(
        navigation=[],
        currencies=[{'char_code': 'USD', 'name': 'Доллар', 'num_code': 840,
                     'value': 90.5, 'nominal': 1}],
        page_title="Валюты",
        last_update="12:00:00",
        update_status=False
    )

    assert 'USD' in result_with_data
    assert 'Доллар' in result_with_data
    assert '90.5' in result_with_data or '90,5' in result_with_data

    # Тест без данных
    result_empty = template.render(
        navigation=[],
        currencies=[],
        page_title="Валюты",
        last_update="12:00:00",
        update_status=False
    )

    assert 'Не удалось загрузить' in result_empty
    assert 'color: red' in result_empty or 'red' in result_empty


def test_user_template_conditions():
    """Тест условий в user.html"""
    template = env.get_template('user.html')

    # Тест с пользователем
    result_with_user = template.render(
        navigation=[],
        user={'id': 1, 'name': 'Иван', 'email': 'test@mail.com'},
        subscribed_currencies=[],
        chart_data='{}',
        page_title="Пользователь"
    )

    assert 'Иван' in result_with_user
    assert 'test@mail.com' in result_with_user

    # Тест с ошибкой
    result_error = template.render(
        navigation=[],
        error_message="Ошибка загрузки",
        page_title="Ошибка"
    )

    assert 'Ошибка' in result_error
    assert 'Ошибка загрузки' in result_error


def test_author_template():
    """Тест шаблона author.html"""
    template = env.get_template('author.html')

    result = template.render(
        navigation=[],
        author={'name': 'Иван', 'group': 'P3124'},
        app={'name': 'Приложение', 'version': '1.0.0'},
        page_title="Об авторе"
    )

    assert 'Иван' in result
    assert 'P3124' in result
    assert 'Приложение' in result
    assert '1.0.0' in result


def test_404_template():
    """Тест шаблона 404.html"""
    template = env.get_template('404.html')

    result = template.render(
        navigation=[],
        page_title="404",
        requested_path="/test"
    )

    assert '404' in result
    assert '/test' in result
    assert 'Вернуться на главную' in result


def test_all_templates_exist():
    """Тест существования шаблонов"""
    templates = ['index.html', 'users.html', 'currencies.html',
                 'user.html', 'author.html', '404.html']
    for template_name in templates:
        template = env.get_template(template_name)
        assert template is not None