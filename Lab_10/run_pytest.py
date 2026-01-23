import math
import sys
import os
import pytest

# Добавляем путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Optimization_For_Integration import integrate


def test_known_integral_trigonometric():
    result = integrate(math.sin, 0, math.pi, n_iter=10000)
    assert pytest.approx(result, abs=0.01) == 2.0


def test_known_integral_polynomial():
    result = integrate(lambda x: x ** 2, 0, 1, n_iter=10000)
    assert pytest.approx(result, abs=0.001) == 1 / 3


def test_iterations_stability_small_change():
    """Проверка устойчивости к изменению числа итераций (малое изменение)."""
    result1 = integrate(math.sin, 0, math.pi, n_iter=1000)
    result2 = integrate(math.sin, 0, math.pi, n_iter=2000)

    assert abs(result1 - result2) < 0.1, \
        f"Слишком большая разница при изменении итераций: {abs(result1 - result2)}"


def test_iterations_stability_large_change():
    """Проверка устойчивости к изменению числа итераций (большое изменение)."""
    result1 = integrate(math.sin, 0, math.pi, n_iter=100)
    result2 = integrate(math.sin, 0, math.pi, n_iter=10000)

    error1 = abs(result1 - 2.0)
    error2 = abs(result2 - 2.0)

    assert error2 < error1 or error2 < 0.1, \
        f"Большее n_iter не дало улучшения точности: error1={error1}, error2={error2}"


if __name__ == "__main__":
    # Запускаем все тесты из этого файла
    result = pytest.main([__file__, "-v", "--tb=short"])
    sys.exit(result)