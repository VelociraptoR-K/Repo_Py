import doctest
import sys
import os

# Временно перенаправляем stdout, чтобы не видеть вывод benchmark при импорте
old_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')

try:
    import Optimization_For_Integration
finally:
    sys.stdout = old_stdout

if __name__ == "__main__":
    print("=" * 50)
    print("ЗАПУСК DOCTESTS")
    print("=" * 50)

    # Запускаем doctests из модуля
    result = doctest.testmod(
        Optimization_For_Integration,
        verbose=True  # Показываем детали выполнения
    )

    print("\n" + "=" * 50)
    print(f"РЕЗУЛЬТАТ: {result.attempted} тестов выполнено")

    if result.failed == 0:
        print("ВСЕ DOCTESTS ПРОЙДЕНЫ")
        exit_code = 0
    else:
        print(f"ПРОВАЛЕНО: {result.failed}/{result.attempted}")
        exit_code = 1

    exit(exit_code)