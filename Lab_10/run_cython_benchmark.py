import math
import time
import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Optimization_For_Integration import integrate, integrate_async, integrate_async_processes


def compile_cython():
    """Компиляция Cython модуля."""
    try:
        result = subprocess.run(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Cython скомпилирован")
            return True
        else:
            print(f"Ошибка компиляции: {result.stderr}")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def benchmark():
    """Основной бенчмарк."""
    print("=" * 60)
    print("БЕНЧМАРК CYTHON ОПТИМИЗАЦИИ")
    print("=" * 60)

    # Проверяем доступность Cython
    CYTHON_AVAILABLE = False
    try:
        import cython_integrate
        CYTHON_AVAILABLE = True
    except ImportError:
        print("Cython модуль не найден")

    # Компилируем если нужно
    if not CYTHON_AVAILABLE:
        if compile_cython():
            import importlib
            importlib.invalidate_caches()
            try:
                import cython_integrate
                CYTHON_AVAILABLE = True
            except ImportError:
                print("Cython недоступен после компиляции")
                CYTHON_AVAILABLE = False
        else:
            CYTHON_AVAILABLE = False

    if not CYTHON_AVAILABLE:
        print("Пропускаем Cython тесты")
        return

    n_iter = 100000

    # 1. Сравнение с итерацией 1 (без параллелизации)
    print("\n1. Сравнение с итерацией 1 (без параллелизации):")
    print("-" * 40)

    # Python
    start = time.time()
    result_py = integrate(math.sin, 0, math.pi, n_iter=n_iter)
    time_py = time.time() - start
    print(f"Python:  {time_py:.6f} сек, результат={result_py:.6f}")

    # Cython
    start = time.time()
    result_cy = cython_integrate.integrate_cython(math.sin, 0, math.pi, n_iter)
    time_cy = time.time() - start
    print(f"Cython:  {time_cy:.6f} сек, результат={result_cy:.6f}")
    print(f"Ускорение: {time_py / time_cy:.2f}x")

    # 2. Сравнение с итерацией 2 (потоки)
    print("\n2. Сравнение с итерацией 2 (потоки), n_jobs=4:")
    print("-" * 40)

    n_jobs = 4

    # Python потоки
    start = time.time()
    result_threads = integrate_async(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
    time_threads = time.time() - start
    print(f"Python потоки: {time_threads:.6f} сек")

    # Cython параллельная версия
    start = time.time()
    result_cy_parallel = cython_integrate.integrate_cython_parallel(
        math.sin, 0, math.pi, n_jobs, n_iter
    )
    time_cy_parallel = time.time() - start
    print(f"Cython:         {time_cy_parallel:.6f} сек")
    print(f"Ускорение: {time_threads / time_cy_parallel:.2f}x")

    # 3. Сравнение с итерацией 3 (процессы)
    print("\n3. Сравнение с итерацией 3 (процессы), n_jobs=4:")
    print("-" * 40)

    # Python процессы
    start = time.time()
    result_processes = integrate_async_processes(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
    time_processes = time.time() - start
    print(f"Python процессы: {time_processes:.6f} сек")
    print(f"Ускорение Cython/Процессы: {time_processes / time_cy_parallel:.2f}x")

    # 4. Проверка HTML аннотаций
    print("\n4. HTML аннотации:")
    print("-" * 40)
    if os.path.exists("cython_integrate.html"):
        print("Файл аннотаций создан: cython_integrate.html")
    else:
        print("Запустите: python setup.py build_ext --inplace")
        print("для генерации аннотаций")


if __name__ == "__main__":
    benchmark()