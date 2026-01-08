import sqlite3
from typing import List, Dict, Any, Optional


class CurrencyRatesCRUD:
    """Контроллер для CRUD операций с таблицей валют."""

    def __init__(self, currency_rates_obj=None):
        """
        Инициализирует контроллер.

        Args:
            currency_rates_obj: объект с данными о валютах (для обратной совместимости)
        """
        self.__con = sqlite3.connect(':memory:')
        self.__cursor = self.__con.cursor()
        self.__currency_rates_obj = currency_rates_obj
        self.__createtable()

    def __createtable(self):
        """Создает таблицы в базе данных согласно схеме из задания."""
        # Исправляем структуру таблицы согласно заданию
        self.__con.execute("""
            CREATE TABLE currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL,
                name TEXT NOT NULL,
                value FLOAT,
                nominal INTEGER
            )
        """)

        # Создаем таблицу пользователей для внешних ключей
        self.__con.execute("""
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        # Создаем таблицу связей пользователей с валютами
        self.__con.execute("""
            CREATE TABLE user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id)
            )
        """)

        self.__con.commit()

    def _create(self, currencies_data: List[Dict[str, Any]] = None):
        """
        Добавляет валюты в базу данных.

        Args:
            currencies_data: список словарей с данными о валютах.
                            Если None, использует данные из currency_rates_obj
        """
        if currencies_data is None and self.__currency_rates_obj:
            # Для обратной совместимости с существующим кодом
            __params = self.__currency_rates_obj.values
            data = []
            for el in __params:
                if len(el) >= 5:
                    data.append({
                        "num_code": str(el[0]),  # Конвертируем в строку
                        "char_code": el[1],
                        "name": el[2],
                        "value": float(el[3]),
                        "nominal": int(el[4])
                    })
        else:
            data = currencies_data

        if data:
            __sqlquery = """
                INSERT INTO currency(num_code, char_code, name, value, nominal) 
                VALUES(:num_code, :char_code, :name, :value, :nominal)
            """
            self.__cursor.executemany(__sqlquery, data)
            self.__con.commit()

    def create_currency(self, num_code: str, char_code: str, name: str,
                        value: float, nominal: int) -> int:
        """
        Создает новую валюту в базе данных.

        Args:
            num_code: цифровой код валюты
            char_code: символьный код валюты
            name: название валюты
            value: курс валюты
            nominal: номинал

        Returns:
            int: ID созданной записи
        """
        query = """
            INSERT INTO currency(num_code, char_code, name, value, nominal) 
            VALUES(?, ?, ?, ?, ?)
        """
        self.__cursor.execute(query, (num_code, char_code, name, value, nominal))
        self.__con.commit()
        return self.__cursor.lastrowid

    def _read(self, currency_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Читает данные о валютах из базы данных.

        Args:
            currency_code: символьный код валюты для фильтрации (опционально)

        Returns:
            List[Dict[str, Any]]: список словарей с данными о валютах
        """
        if currency_code:
            if not isinstance(currency_code, str) or len(currency_code) != 3:
                raise ValueError("Код валюты должен быть строкой из 3 символов")
            cur = self.__con.execute(
                "SELECT * FROM currency WHERE char_code = ?",
                (currency_code,)
            )
        else:
            cur = self.__con.execute("SELECT * FROM currency ORDER BY char_code")

        result_data = []
        for _row in cur:
            _d = {
                'id': int(_row[0]),
                'num_code': _row[1],
                'char_code': _row[2],
                'name': _row[3],
                'value': float(_row[4]),
                'nominal': int(_row[5])
            }
            result_data.append(_d)
        return result_data

    def _delete(self, currency_id: int) -> bool:
        """
        Удаляет валюту по ID.

        Args:
            currency_id: ID валюты для удаления

        Returns:
            bool: True если удаление успешно
        """
        # Сначала удаляем связанные записи из user_currency
        self.__cursor.execute("DELETE FROM user_currency WHERE currency_id = ?", (currency_id,))
        # Затем удаляем валюту
        self.__cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.__con.commit()
        return self.__cursor.rowcount > 0

    def _update(self, currency: Dict[str, float]) -> bool:
        """
        Обновляет курс валюты.

        Args:
            currency: словарь {код_валюты: новое_значение}

        Returns:
            bool: True если обновление успешно
        """
        currency_code = list(currency.keys())[0]
        currency_value = list(currency.values())[0]

        self.__cursor.execute(
            "UPDATE currency SET value = ? WHERE char_code = ?",
            (currency_value, currency_code)
        )
        self.__con.commit()
        return self.__cursor.rowcount > 0

    def update_currency_value(self, currency_id: int, new_value: float) -> bool:
        """
        Обновляет курс валюты по ID.

        Args:
            currency_id: ID валюты
            new_value: новое значение курса

        Returns:
            bool: True если обновление успешно
        """
        self.__cursor.execute(
            "UPDATE currency SET value = ? WHERE id = ?",
            (new_value, currency_id)
        )
        self.__con.commit()
        return self.__cursor.rowcount > 0

    def __del__(self):
        self.__cursor = None
        self.__con.close()