ОТЧЁТ

1. Цель работы
Создать простое клиент-серверное приложение на Python без серверных фреймворков.

Освоить работу с HTTPServer и маршрутизацию запросов.

Применять шаблонизатор Jinja2 для отображения данных.

Реализовать модели предметной области (User, Currency, UserCurrency, App, Author) с геттерами и сеттерами.

Структурировать код в соответствии с архитектурой MVC.

Получать данные о курсах валют через функцию get_currencies и отображать их пользователям.

Реализовать функциональность подписки пользователей на валюты и отображение динамики их изменения.

Научиться создавать тесты для моделей и серверной логики.

2. Описание предметной области

   
Модели

Author

name - имя автора

group - учебная группа

App

name - название приложения

version - версия приложения

author - объект Author

User

id - уникальный идентификатор

name - имя пользователя 

Currency

id - уникальный идентификатор

num_code - цифровой код

char_code - символьный код

name - название валюты

value - курс

nominal - номинал (за сколько единиц валюты указан курс)

UserCurrency

id - уникальный идентификатор

user_id - внешний ключ к User

currency_id - внешний ключ к Currency

Реализует связь «много ко многим» между пользователями и валютами.

3. Структура проекта


myapp/

Файл	Назначение

models/__init__.py	импорт всех моделей

models/author.py	класс Author

models/app.py	класс App

models/user.py	класс User

models/currency.py	класс Currency

models/user_currency.py	класс UserCurrency

static/ css, js, изображения

templates/*.html	шаблоны страниц

myapp.py	запуск сервера и маршрутизация

utils/currencies_api.py	функция get_currencies

testing/ файлы для тестов

run_tests.py запуск всех тестов

logger.py логирование запросов


4. Описание реализации

Для каждого класса созданы приватные атрибуты с геттерами и сеттерами, включающими проверку типов и бизнес-логику. Все свойства защищены двойным подчеркиванием (__name). Сеттеры выполняют валидацию (длина строк, формат email, диапазоны значений). Для валют проверяется регистр символьных кодов и положительность значений. В ходе работы над моделями попытался приблизиться к тем данным, которые обычно отображаются на сайтах похожего типа, но при этом, чтобы было проще, не стал делать их слишком много. Сервер построен на базе стандартного модуля http.server. Маршрутизация реализована через self.path в методе do_GET(). Query-параметры (например, ?id=3) парсятся с помощью urllib.parse.parse_qs(). Jinja2 инициализируется один раз при старте приложения для повышения производительности, так как шаблоны не подгружаются заново при каждом запросе. Функция get_currencies из модуля utils.currencies_api.py интегрирована с кэшированием для снижения нагрузки на API.


5-6. Примеры работы приложения:

<img width="1040" height="780" alt="image" src="https://github.com/user-attachments/assets/ba1ae052-a9eb-44b3-91f9-b06483146869" />


<img width="873" height="552" alt="image" src="https://github.com/user-attachments/assets/82cf92e5-08b7-4afe-b7c5-a32076f3fa8c" />


<img width="1007" height="612" alt="image" src="https://github.com/user-attachments/assets/f5c0377b-cd49-43e8-b967-525f2081a73e" />


<img width="2537" height="1184" alt="image" src="https://github.com/user-attachments/assets/1e0ae7c9-588b-4311-bc65-d3f92d64650a" />


<img width="2312" height="897" alt="image" src="https://github.com/user-attachments/assets/dcfc3037-58e1-477a-a6a9-496b8669c244" />


<img width="2254" height="852" alt="image" src="https://github.com/user-attachments/assets/141eed9d-a985-4f51-b785-4088cd358068" />


<img width="2559" height="1287" alt="image" src="https://github.com/user-attachments/assets/40c1a8ba-e10f-42c0-a6be-020bc21979f7" />


<img width="2462" height="1112" alt="image" src="https://github.com/user-attachments/assets/3fa5b931-8818-4a02-87b5-b8310d5b7cdd" />


<img width="2559" height="1119" alt="image" src="https://github.com/user-attachments/assets/55b1b40e-faf5-4d0b-8c81-f5909cbda3ea" />

Для графиков использовал Chart.js, так как это легковесная библиотека для графиков + интерактивность (при наведении показываются точные значения)

7. Тестирование проводилось с помощью фреймворка pytest. Пример тестов для:
Моделей:


<img width="816" height="836" alt="image" src="https://github.com/user-attachments/assets/0c044dc9-e6a5-4ec7-b155-da85bb5de956" />


Контроллера:


<img width="669" height="327" alt="image" src="https://github.com/user-attachments/assets/a47d4a0a-2675-4571-b69a-5d506c6b2a6c" />


Функции get_currencies:


<img width="778" height="316" alt="image" src="https://github.com/user-attachments/assets/ac2e0dd7-d039-4777-8c7c-2a2c44f4c347" />


Вывод результатов тестов:

"C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp\.venv\Scripts\python.exe" "C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp\run_tests.py" 
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Николай\OneDrive\Dokumenty\PyCharm проекты\currenciesapp
collecting ... collected 25 items

testing/test_controller.py::test_handler_initialization PASSED           [  4%]
testing/test_controller.py::test_navigation_exists PASSED                [  8%]
testing/test_controller.py::test_author_and_app PASSED                   [ 12%]
testing/test_controller.py::test_template_rendering PASSED               [ 16%]
testing/test_controller.py::test_route_handlers_exist PASSED             [ 20%]
testing/test_controller.py::test_query_parsing_logic PASSED              [ 24%]
testing/test_get_currencies.py::test_get_currencies_returns_list PASSED  [ 28%]
testing/test_get_currencies.py::test_get_specific_currencies PASSED      [ 32%]
testing/test_get_currencies.py::test_get_historical_data_structure PASSED [ 36%]
testing/test_get_currencies.py::test_historical_data_length PASSED       [ 40%]
testing/test_get_currencies.py::test_multiple_currencies PASSED          [ 44%]
testing/test_get_currencies.py::test_api_functions_exist PASSED          [ 48%]
testing/test_models.py::test_author_creation_and_setters PASSED          [ 52%]
testing/test_models.py::test_app_creation_and_version PASSED             [ 56%]
testing/test_models.py::test_user_email_validation PASSED                [ 60%]
testing/test_models.py::test_currency_validation PASSED                  [ 64%]
testing/test_models.py::test_user_currency PASSED                        [ 68%]
testing/test_templates.py::test_index_template_variables PASSED          [ 72%]
testing/test_templates.py::test_index_template_loop PASSED               [ 76%]
testing/test_templates.py::test_users_template PASSED                    [ 80%]
testing/test_templates.py::test_currencies_template_conditions PASSED    [ 84%]
testing/test_templates.py::test_user_template_conditions PASSED          [ 88%]
testing/test_templates.py::test_author_template PASSED                   [ 92%]
testing/test_templates.py::test_404_template PASSED                      [ 96%]
testing/test_templates.py::test_all_templates_exist PASSED               [100%]

======================== 25 passed in 91.19s (0:01:31) ========================

Process finished with exit code 0 

8. Выводы:

В ходе работы возникли некоторые проблемы: не прошёл 1 тест:

=========================== short test summary info ===========================

FAILED testing/test_controller.py::test_template_rendering - jinja2.exception...

======================== 1 failed, 24 passed in 0.47s =========================

Проблема была в том, что передал не все параметры для шаблона author.html

Данные о графиках и подписках пользователей долго подгружаются: проблема была в огромном количестве запросов к API Центробанка, поэтому сделал быструю версию с тестовыми данными.

Блокировка при импорте модуля

Проблема: При импорте myapp.py запускался сервер

Решение: Добавление условия if __name__ == "__main__"

Применение принципов MVC
Model (Модели)

models/ - бизнес-логика, валидация

Не зависят от представления или контроллера

View (Представление)

templates/ - шаблоны Jinja2

Только отображение данных, без логики

Controller (Контроллер)

myapp.py - обработка запросов, маршрутизация

Связывает модели и представления

В ходе лабораторной работы я узнал, как создать собственной HTTP-сервера без фреймворков. Хорошо разобрался в теме работы клиент-сервера, наглядно наблюдая логи кодов состояния HTTP в консоли. При работе с Jinja2 узнал, как передавать сложные структуры данных в шаблоны. При работе с API курсов валют, узнал, что можно применить кэширование для снижения нагрузки на сервер и ускорения загрузки страницы.
