import math
import time
from Optimization_For_Integration import integrate_async, integrate_async_processes


def benchmark_simple():
    print("=" * 60)
    print("БЕНЧМАРК NOGIL")
    print("=" * 60)

    print("\n1. ЗАМЕРЫ ПРОИЗВОДИТЕЛЬНОСТИ:")
    print("-" * 40)

    n_iter = 100000
    n_jobs_list = [2, 4, 6]

    for n_jobs in n_jobs_list:
        print(f"\nn_jobs = {n_jobs}:")

        # Python потоки (с GIL)
        start = time.time()
        result = integrate_async(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
        time_threads = time.time() - start

        # Python процессы (без GIL)
        start = time.time()
        result = integrate_async_processes(math.sin, 0, math.pi, n_jobs=n_jobs, n_iter=n_iter)
        time_processes = time.time() - start

        print(f"  Python потоки (с GIL):    {time_threads:.6f} сек")
        print(f"  Python процессы (без GIL): {time_processes:.6f} сек")
        print(f"  Ускорение процессов: {time_threads / time_processes:.2f}x")


if __name__ == "__main__":
    benchmark_simple()