import timeit
import matplotlib.pyplot as plt
import random
from functools import lru_cache

@lru_cache()
def fact_iterative_lru(n: int) -> int:
    """Нерекурсивный кэшированный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def fact_iterative(n: int) -> int:
    """Нерекурсивный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

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

    res_iterative_lru = []
    res_iterative = []

    for n in test_data:
      res_iterative_lru.append(benchmark(fact_iterative_lru, n))
      res_iterative.append(benchmark(fact_iterative, n))

    # Визуализация
    plt.plot(test_data, res_iterative_lru, label="Кэшированный итеративный")
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение кэшированного итеративного и итеративного факториала")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

