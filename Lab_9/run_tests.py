import pytest
import sys

if __name__ == "__main__":
    # Запускаем все тесты
    result = pytest.main(["testing/", "-v"])
    sys.exit(result)