# cython_integrate_nogil.pyx
# distutils: language=c
# cython: language_level=3

import cython
from libc.math cimport sin

@cython.boundscheck(False)
@cython.wraparound(False)
cdef double integrate_sin_nogil(double a, double b, int n_iter) nogil:
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef double x
    cdef int i

    for i in range(n_iter):
        x = a + i * step
        acc += sin(x) * step

    return acc

def integrate_parallel_nogil(double a, double b, int n_jobs, int n_iter):
    cdef double step_total = (b - a) / n_jobs
    cdef double total = 0.0
    cdef int i

    for i in range(n_jobs):
        ai = a + i * step_total
        bi = ai + step_total
        total += integrate_sin_nogil(ai, bi, n_iter // n_jobs)

    return total

def integrate_sin_single(double a, double b, int n_iter):
    return integrate_sin_nogil(a, b, n_iter)