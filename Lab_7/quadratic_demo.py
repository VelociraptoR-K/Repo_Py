import logging
import math
from logger import logger

logging.basicConfig(
    filename="quadratic.log",
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s"
)

def solve_quadratic_raw(a, b, c):
    """
    Решает квадратное уравнение с внутренним логированием.
    Используется для демонстрации разных уровней логирования.
    """
    logging.info(f"Solving equation: {a}x^2 + {b}x + {c} = 0")

    # Ошибка типов - CRITICAL
    for name, value in zip(("a", "b", "c"), (a, b, c)):
        if not isinstance(value, (int, float)):
            logging.critical(f"Parameter '{name}' must be a number, got: {value}")
            raise TypeError(f"Coefficient '{name}' must be numeric")

    # Ошибка: a == 0 - ERROR
    if a == 0:
        logging.error("Coefficient 'a' cannot be zero")
        raise ValueError("a cannot be zero")

    d = b * b - 4 * a * c
    logging.debug(f"Discriminant: {d}")  # DEBUG информация

    # Дискриминант < 0 - WARNING
    if d < 0:
        logging.warning("Discriminant < 0: no real roots")
        return None

    # Один корень - INFO
    if d == 0:
        x = -b / (2 * a)
        logging.info("One real root")
        return (x,)

    # Два корня - INFO
    root1 = (-b + math.sqrt(d)) / (2 * a)
    root2 = (-b - math.sqrt(d)) / (2 * a)
    logging.info("Two real roots computed")
    return root1, root2


# Обёрнутая функция с декоратором @logger
@logger
def solve_quadratic(a, b, c):
    """
    Версия функции с двойным логированием:
    1. Через декоратор @logger (логирует вызовы и исключения)
    2. Через внутренний logging (логирует детали с разными уровнями)
    """
    return solve_quadratic_raw(a, b, c)


def run_demo():
    """Запуск демонстрации всех случаев"""
    print("=== ДЕМОНСТРАЦИЯ РАЗНЫХ УРОВНЕЙ ЛОГИРОВАНИЯ ===\n")

    # Тест 1: Два корня (INFO)
    print("1. Два корня (должен быть INFO в логах):")
    print("   Уравнение: x² - 3x + 2 = 0")
    try:
        result = solve_quadratic(1, -3, 2)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    print()

    # Тест 2: Один корень (INFO)
    print("2. Один корень (должен быть INFO в логах):")
    print("   Уравнение: x² + 2x + 1 = 0")
    try:
        result = solve_quadratic(1, 2, 1)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    print()

    # Тест 3: Нет действительных корней (WARNING)
    print("3. Нет действительных корней (должен быть WARNING):")
    print("   Уравнение: x² + 2x + 5 = 0")
    try:
        result = solve_quadratic(1, 2, 5)
        print(f"   Результат: {result} (возвращает None)")
    except Exception as e:
        print(f"   Ошибка: {e}")
    print()

    # Тест 4: Некорректные данные (CRITICAL → ERROR)
    print("4. Некорректные данные (должен быть CRITICAL → ERROR):")
    print("   Уравнение: 'abc'x² + 2x + 1 = 0")
    try:
        result = solve_quadratic("abc", 2, 1)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Поймано исключение: {type(e).__name__}: {e}")
    print()

    # Тест 5: a = 0 (ERROR)
    print("5. a = 0 (должен быть ERROR):")
    print("   Уравнение: 0x² + 2x + 1 = 0")
    try:
        result = solve_quadratic(0, 2, 1)
        print(f"   Результат: {result}")
    except Exception as e:
        print(f"   Поймано исключение: {type(e).__name__}: {e}")
    print()

if __name__ == "__main__":
    run_demo()