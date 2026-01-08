class User():
    """Класс для представления данных пользователя."""

    def __init__(self, id:int, name:str, email:str):
        """
        Инициализирует объект пользователя.

        Args:
            id: уникальный идентификатор
            name: имя пользователя
            email: почта пользователя
        """
        self.__id: int = id
        self.__name: str = name
        self.__email: str = email

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id: int):
        if isinstance(id, int) and id >= 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании id пользователя')


    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя')


    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, email: str):
        if isinstance(email, str) and '@' in email and '.' in email and len(email) >= 5:
            self.__email = email
        else:
            raise ValueError('Ошибка при задании почты пользователя')
