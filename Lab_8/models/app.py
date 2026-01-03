from models import Author

class App():
    """Класс, представляющий приложение."""

    def __init__(self, name:str, version:str, author: Author):
        """
        Инициализирует объект приложения.

        Args:
            name: название приложения
            version: версия приложения
            author: объект Author
        """
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name:str):
        if isinstance(name, str) and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании названия приложения')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version: str):
        if not isinstance(version, str):
            raise TypeError('Версия должна быть строкой')

        parts = version.split('.')
        if len(parts) != 3:
            raise ValueError('Некорректная версия приложения')

        for part in parts:
            if not part.isdigit():
                raise ValueError('Все части версии должны быть числами')

        self.__version = version

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError('Автор должен быть объектом класса Author')
