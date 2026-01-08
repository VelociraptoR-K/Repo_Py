1. Цель работы
   
Реализовать CRUD (Create, Read, Update, Delete) для сущностей бизнес-логики приложения.
Освоить работу с SQLite в памяти (:memory:) через модуль sqlite3.
Понять принципы первичных и внешних ключей и их роль в связях между таблицами.
Выделить контроллеры для работы с БД и для рендеринга страниц в отдельные модули.
Использовать архитектуру MVC и соблюдать разделение ответственности.
Отображать пользователям таблицу с валютами, на которые они подписаны.
Реализовать полноценный роутер, который обрабатывает GET-запросы и выполняет сохранение/обновление данных и рендеринг страниц.
Научиться тестировать функционал на примере сущностей currency и user с использованием unittest.mock.

1.2
Первичные ключи (PRIMARY KEY) нужны для уникальной идентификации каждой записи (строки) в таблице, обеспечивая целостность данных, позволяя быстро находить, связывать и управлять информацией, так как они должны быть уникальными и не могут быть пустыми (NULL).
Внешние ключи (FOREIGN KEY) позволяют установить связи между таблицами.

2. Описание моделей, их свойств и связей:
   
1. Currency (Валюта)

class Currency:
    def __init__(self, id: int, num_code: int, char_code: str, name: str, value: float, nominal: int):
        self.__id = id           # Первичный ключ
        self.__num_code = num_code  # Цифровой код (3 цифры)
        self.__char_code = char_code # Символьный код (3 буквы)
        self.__name = name       # Название валюты
        self.__value = value     # Текущий курс
        self.__nominal = nominal # Номинал
   
2. User (Пользователь)

class User:
    def __init__(self, id: int, name: str, email: str):
        self.__id = id          # Первичный ключ
        self.__name = name      # Имя пользователя
        self.__email = email    # Email пользователя
      
3. UserCurrency (Подписка пользователя на валюту)

class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: int, subscribed_at: float = None):
        self.__id = id          # Первичный ключ
        self.__user_id = user_id    # Внешний ключ к User
        self.__currency_id = currency_id  # Внешний ключ к Currency
        self.__subscribed_at = subscribed_at  # Время подписки
        
Связи между таблицами:

Один-ко-многим: Один пользователь может иметь много подписок на валюты

Один-ко-многим: Одна валюта может быть в подписках у многих пользователей


3. Структура проекта с назначением файлов.

myapp/

Файл Назначение

controllers/__init__.py импорт всех контроллеров

controllers/currencycontroller.py класс CurrencyController

controllers/databasecontroller.py класс CurrencyRatesCRUD

models/__init__.py импорт всех моделей

models/author.py класс Author

models/app.py класс App

models/user.py класс User

models/currency.py класс Currency

models/user_currency.py класс UserCurrency

static/ css, js, изображения

templates/*.html шаблоны страниц

myapp.py запуск сервера и маршрутизация

utils/currencies_api.py функция get_currencies

testing/ файлы для тестов

run_tests.py запуск всех тестов

logger.py логирование запросов

4-5. Реализация CRUD представлена в файле controllers/databasecontrollers
Примеры SQL-запросов (скриншоты работы приложения):

Главная страница:


<img width="1458" height="1286" alt="image" src="https://github.com/user-attachments/assets/075d92d1-bf36-4474-bef9-a7871ffcaaaa" />


Таблица с валютами:


<img width="2549" height="1289" alt="image" src="https://github.com/user-attachments/assets/cebd9b3d-c6e6-4393-ac9f-33aa6daeed19" />


После удаления юаня:


<img width="2439" height="1288" alt="image" src="https://github.com/user-attachments/assets/dac54b60-f97a-49c9-8ee1-e5efb6f4c449" />


currency/show (валюта здесь тоже обновляется и удаляется):


<img width="1798" height="1253" alt="image" src="https://github.com/user-attachments/assets/d92cd089-56ff-4b57-b61c-d6b5226e9688" />


6. Примеры тестов с unittest.mock и результаты их выполнения.



 def test_list_currencies(self):
     mock_db = MagicMock()
     mock_db._read.return_value = [{"id":1, "char_code":"USD", "value":90}]
     controller = CurrencyController(mock_db)
     result = controller.list_currencies()
     self.assertEqual(result[0]['char_code'], "USD")
     mock_db._read.assert_called_once()

 def test_update_currency(self):
     """Тестирование метода update_currency."""
     # Создаем mock-объект базы данных
     mock_db = MagicMock()
     controller = CurrencyController(mock_db)
     # Тестируемые данные
     test_char_code = "EUR"
     test_value = 105.5
     result = controller.update_currency(test_char_code, test_value)
     self.assertIsNone(result)
     mock_db._update.assert_called_once()
     mock_db._update.assert_called_with({test_char_code: test_value})

 def test_delete_currency(self):
     """Тестирование метода delete_currency."""
     mock_db = MagicMock()
     controller = CurrencyController(mock_db)
     # Тестируемые данные
     test_currency_id = 5
     result = controller.delete_currency(test_currency_id)
     mock_db._delete.assert_called_once()
     mock_db._delete.assert_called_with(test_currency_id)
     self.assertIsNone(result)


Результаты выполнения: "C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp\.venv\Scripts\python.exe" "C:/Program Files/JetBrains/PyCharm 2025.2.3/plugins/python-ce/helpers/pycharm/_jb_pytest_runner.py" --path "C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp\testing\test_currency_controller.py" 
Testing started at 21:44 ...
Launching pytest with arguments C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp\testing\test_currency_controller.py --no-header --no-summary -q in C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp

============================= test session starts =============================
collecting ... collected 3 items

testing/test_currency_controller.py::TestCurrencyController::test_delete_currency PASSED [ 33%]
testing/test_currency_controller.py::TestCurrencyController::test_list_currencies PASSED [ 66%]
testing/test_currency_controller.py::TestCurrencyController::test_update_currency PASSED [100%]

============================== 3 passed in 0.05s ==============================

Process finished with exit code 0

7. Выводы:

1. Применение архитектуры MVC:

Model: Классы в папке models представляют бизнес-сущности и их логику

View: Шаблоны в папке templates отвечают за представление данных

Controller: Классы в папке controllers управляют бизнес-логикой и взаимодействием с БД

Преимущества:

Четкое разделение ответственности

Легкость поддержки и модификации

2. Работа с SQLite:

Использована база данных в памяти (:memory:)

Реализованы параметризованные запросы для защиты от SQL-инъекций

Созданы таблицы с первичными и внешними ключами

Обеспечена целостность данных через связи между таблицами

Первичные ключи (PRIMARY KEY):

Уникально идентифицируют каждую запись

Автоматически инкрементируются (AUTOINCREMENT)

Используются для связей с другими таблицами

Внешние ключи (FOREIGN KEY):

Обеспечивают ссылочную целостность данных

Запрещают удаление записей, на которые есть ссылки

Реализуют связи между таблицами

3. Обработка маршрутов

Использован BaseHTTPRequestHandler для обработки HTTP-запросов

Реализована маршрутизация на основе URL-путей

Поддержка GET-параметров через parse_qs

Обработка ошибок (404 страница)

Примеры маршрутов:

/ - главная страница

/currencies - список валют

/currency/update?USD=9999.67 - обновление курса

/currency/delete?id=3 - удаление валюты

4. Рендеринг шаблонов

Использован шаблонизатор Jinja2

Передача данных из контроллера в представление

Наследование шаблонов и повторное использование компонентов

Проект демонстрирует полный цикл разработки веб-приложения с использованием современных подходов к безопасности, тестированию и архитектуре разделения файлов.
