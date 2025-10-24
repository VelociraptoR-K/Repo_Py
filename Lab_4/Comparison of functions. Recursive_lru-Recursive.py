import timeit
import matplotlib.pyplot as plt
import random
from functools import lru_cache

@lru_cache()
def fact_recursive_lru(n: int) -> int:
    """Рекурсивный кэшированный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive_lru(n - 1)

def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)

def benchmark(func, n, number=1, repeat=5):
    def setup():
        """Очищает кэш перед каждым повторением"""
        if hasattr(func, 'cache_clear'):
            func.cache_clear()

    """Возвращает среднее время выполнения func(n)"""
    times = timeit.repeat(lambda: func(n),setup=setup, number=number, repeat=repeat)
    return min(times)

def main():
    # фиксированный набор данных
    random.seed(42)
    test_data = list(range(10, 300, 10))

    res_recursive_lru = []
    res_recursive = []

    for n in test_data:
      res_recursive_lru.append(benchmark(fact_recursive_lru, n))
      res_recursive.append(benchmark(fact_recursive, n))

    # Визуализация
    plt.plot(test_data, res_recursive_lru, label="Кэшированный рекурсивный")
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение кэшированного рекурсивного и рекурсивного факториала")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

