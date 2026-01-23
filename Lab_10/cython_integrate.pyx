# cython_integrate.pyx
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False

import cython
from cython.parallel import prange, parallel
cimport openmp

@cython.boundscheck(False)
@cython.wraparound(False)
def integrate_cython(f, double a, double b, int n_iter):
    cdef:
        double acc = 0.0
        double step = (b - a) / n_iter
        double x
        int i

    for i in range(n_iter):
        x = a + i * step
        acc += f(x) * step

    return acc

@cython.boundscheck(False)
@cython.wraparound(False)
def integrate_cython_parallel(f, double a, double b, int n_jobs, int n_iter):
    cdef:
        double step_total = (b - a) / n_jobs
        double result = 0.0
        int i

    for i in range(n_jobs):
        ai = a + i * step_total
        bi = ai + step_total
        result += integrate_cython(f, ai, bi, n_iter // n_jobs)

    return result