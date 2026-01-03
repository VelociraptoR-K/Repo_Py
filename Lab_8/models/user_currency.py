import time
class UserCurrency():
    """Класс для представления валюты пользователя."""

    def __init__(self, id: int, user_id: int, currency_id: int, subscribed_at: float = None):
        """
        Инициализирует объект валюты пользователя

        Args:
            id: уникальный идентификатор
            user_id: внешний ключ к User
            currency_id: внешний ключ к Currency
            subscribed_at: timestamp когда пользователь подписался
        """
        self.__id: int = id
        self.__user_id: int = user_id
        self.__currency_id: int = currency_id
        self.__subscribed_at: float = subscribed_at or time.time()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if isinstance(id, int) and id > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании уникального идентификатора')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if isinstance(user_id, int) and user_id > 0:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании внешнего ключа к User')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: int):
        if isinstance(currency_id, int) and currency_id > 0:
            self.__currency_id = currency_id
        else:
            raise ValueError('Ошибка при задании внешнего ключа к Currency')

    @property
    def subscribed_at(self):
        return self.__subscribed_at

    @subscribed_at.setter
    def subscribed_at(self, timestamp: float):
        """Устанавливаем время подписки"""
        if isinstance(timestamp, (int, float)):
            self.__subscribed_at = timestamp
        else:
            raise ValueError('Timestamp должен быть числом')
