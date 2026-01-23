import concurrent.futures as ftres
from functools import partial
from typing import Callable, Union
import math
import time
import timeit


def integrate(f: Callable[[float], float],
              a: Union[int, float],
              b: float,
              *,
              n_iter: int = 10000) -> float:
    """
    Вычисляет площадь под графиком функции численным интегрированием

    Недостаток: плохо работает для быстро меняющихся функций с малым количеством прямоугольников

    Args:
        f: Функция одного вещественного аргумента, интеграл которой вычисляется.
        a: Левая граница интервала интегрирования.
        b: Правая граница интервала интегрирования.
        n_iter: Количество прямоугольников для аппроксимации интеграла.

    Returns:
        Приближенное значение определенного интеграла.

    Examples:
        >>> import math
        >>> result = integrate(math.sin, 0, math.pi, n_iter=10000)
        >>> abs(result - 2.0) < 0.01
        True

        >>> result = integrate(lambda x: x**2, 0, 1, n_iter=10000)
        >>> abs(result - 1/3) < 0.001
        True
    """

    if a >= b:
        raise ValueError(f"a ({a}) должно быть меньше b ({b})")

    acc = 0.0
    step = (b - a) / n_iter
    f_local = f
    a_local = a
    for i in range(n_iter):
        acc += f_local(a_local + i * step) * step
    return acc

def integrate_async(f: Callable[[float], float],
                    a: Union[int, float],
                    b: float,
                    *,
                    n_jobs: int = 2,
                    n_iter: int = 1000) -> float:
    """Параллельное интегрирование с потоками."""

    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    step = (b - a) / n_jobs

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    executor.shutdown(wait=False)
    return sum(f.result() for f in ftres.as_completed(fs))


def integrate_async_processes(f: Callable[[float], float],
                              a: Union[int, float],
                              b: float,
                              *,
                              n_jobs: int = 2,
                              n_iter: int = 1000) -> float:
    """Параллельное интегрирование с процессами."""

    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
    step = (b - a) / n_jobs

    fs = [spawn(a + i * step, a + (i + 1) * step) for i in range(n_jobs)]
    executor.shutdown(wait=False)
    return sum(f.result() for f in ftres.as_completed(fs))


def benchmark_iterations():
    """
    Проводит замер времени выполнения функции integrate для различного количества итераций.

    Returns:
        list: Список с результатами замеров времени
    """
    print("-" * 60)
    print("Замеры integrate() с разным числом итераций:")
    print("-" * 60)

    test_cases = [
        (1000, "1K итераций"),
        (10000, "10K итераций"),
        (100000, "100K итераций"),
        (1000000, "1M итераций"),
    ]
    results = []
    for n_iter, description in test_cases:
        time_taken = timeit.timeit(
            lambda: integrate(math.cos, 0, math.pi, n_iter=n_iter),
            number=10
        ) / 10

        results.append(f"{description}: {time_taken:.6f} секунд")
    return results


def benchmark_threads_processes():
    n_jobs_list = [2, 4,6,8]
    print()
    print("-" * 75)
    print("Сравнение потоков и процессов:")
    print("-" * 75)

    for n_jobs in n_jobs_list:
        start = time.perf_counter()
        result_threads = integrate_async(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=5000)
        time_threads = time.perf_counter() - start

        start = time.perf_counter()
        result_processes = integrate_async_processes(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=5000)
        time_processes = time.perf_counter() - start

        print(f"n_jobs={n_jobs}:")
        print(f"  Потоки: {time_threads:.4f} сек, результат={result_threads:.6f}")
        print(f"  Процессы: {time_processes:.4f} сек, результат={result_processes:.6f}")
        print()

if __name__ == "__main__":
    benchmark_iterations()
    benchmark_threads_processes()
