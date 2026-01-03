import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Author, App, User, Currency, UserCurrency


def test_author_creation_and_setters():
    """Тест: проверка создания автора и сеттеров"""
    author = Author("Тест", "P3124")

    # Геттеры
    assert author.name == "Тест"
    assert author.group == "P3124"

    # Сеттеры с корректными значениями
    author.name = "Новое Имя"
    author.group = "P3120"
    assert author.name == "Новое Имя"
    assert author.group == "P3120"

    # Исключения при некорректных значениях
    try:
        author.name = ""
        assert False, "Должно быть исключение"
    except ValueError:
        pass

    try:
        author.name = 123
        assert False, "Должно быть исключение"
    except ValueError:
        pass


def test_app_creation_and_version():
    """Тест приложения и валидации версии"""
    author = Author("Автор", "P3124")
    app = App("МоеПриложение", "1.0.0", author)

    assert app.name == "МоеПриложение"
    assert app.version == "1.0.0"
    assert app.author == author

    # Корректные версии
    app.version = "2.1.3"
    assert app.version == "2.1.3"

    # Исключения
    try:
        app.version = "1.0"
        assert False, "Должно быть исключение"
    except ValueError:
        pass

    try:
        app.version = "1.a.0"
        assert False, "Должно быть исключение"
    except ValueError:
        pass


def test_user_email_validation():
    """Тест валидации email пользователя"""
    user = User(1, "Пользователь", "test@mail.com")

    assert user.email == "test@mail.com"

    # Корректный email
    user.email = "new@example.ru"
    assert user.email == "new@example.ru"

    # Исключения
    try:
        user.email = "invalid"
        assert False, "Должно быть исключение"
    except ValueError:
        pass

    try:
        user.email = "a@b"
        assert False, "Должно быть исключение"
    except ValueError:
        pass


def test_currency_validation():
    """Тест валидации валюты"""
    currency = Currency(1, 840, "USD", "Доллар", 90.5, 1)

    # Проверка char_code
    try:
        currency.char_code = "usd"  # должен быть верхний регистр
        assert False, "Должно быть исключение"
    except ValueError:
        pass

    # Проверка value
    try:
        currency.value = -10
        assert False, "Должно быть исключение"
    except ValueError:
        pass

    # Проверка nominal
    try:
        currency.nominal = 0
        assert False, "Должно быть исключение"
    except ValueError:
        pass


def test_user_currency():
    """Тест подписки на валюту"""
    uc = UserCurrency(1, 1, 1)

    assert uc.id == 1
    assert uc.user_id == 1
    assert uc.currency_id == 1
    assert uc.subscribed_at > 0  # timestamp установлен

    # Сеттеры
    uc.user_id = 2
    uc.currency_id = 3
    assert uc.user_id == 2
    assert uc.currency_id == 3
