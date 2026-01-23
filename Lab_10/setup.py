try:
    from setuptools import setup
    from Cython.Build import cythonize
except ImportError:
    print("Установите: pip install setuptools cython")
    exit(1)

setup(
    ext_modules=cythonize("cython_integrate.pyx", annotate=True)
)