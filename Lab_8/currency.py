class Currency:
    """Класс для представления валюты."""

    def __init__(self, id: int, num_code: int, char_code: str, name: str, value: float, nominal: int):
        """
        Инициализирует объект валюты.

        Args:
            id: уникальный идентификатор
            num_code: цифровой код
            char_code: символьный код
            name: название валюты
            value: курс
            nominal:  номинал (за сколько единиц валюты указан курс)
        """
        self.__id: int = id
        self.__num_code: int = num_code
        self.__char_code: str = char_code
        self.__name: str = name
        self.__value: float = value
        self.__nominal: int = nominal

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if isinstance(id, int) and id > 0:
            self.__id = id
        else:
            raise ValueError('Неправильный id валюты')


    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, num_code: int):
        if isinstance(num_code, int) and len(str(num_code)) == 3:
            self.__num_code = num_code
        else:
            raise ValueError('Неправильный код валюты')


    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, char_code: str):
        if isinstance(char_code, str) and len(char_code) == 3 and char_code == char_code.upper():
            self.__char_code= char_code
        else:
            raise ValueError('Неправильный символьный код')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if isinstance(name, str) and len(name) >= 3:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании названия валюты')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: float):
        if isinstance(value, (int,float)) and value > 0:
            self.__value = float(value)
        else:
            raise ValueError('Ошибка при задании курса валюты')

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, nominal: int):
        if isinstance(nominal, int) and nominal > 0:
            self.__nominal = nominal
        else:
            raise ValueError('Ошибка при задании номинала валюты')
