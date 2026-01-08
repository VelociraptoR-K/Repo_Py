import sys
import functools
import logging
import typing

def logger(func=None,*,handle=sys.stdout) -> typing.Callable:
    """
    Параметризуемый декоратор для логирования вызовов функций.

    Args:
        func: Декорируемая функция. Если None, декоратор вызывается с параметрами.
        handle: Объект для логирования: logging.Logger или поток с методом write().

    Returns:
        Декорированная функция
    """
    if func is None:
        return lambda func: logger(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        message = f"Calling {func.__name__} with args={args}, kwargs={kwargs}"
        if isinstance(handle, logging.Logger):
            handle.info(message)
        else:
            handle.write(message+"\n")

        try:
            result = func(*args, **kwargs)
            if isinstance(handle, logging.Logger):
                handle.info(f"{func.__name__} returned {result}")
            else:
                handle.write(f"{func.__name__} returned {result}\n\n")
            return result
        except Exception as e:
            if isinstance(handle, logging.Logger):
                handle.error(f"{func.__name__} raised {type(e).__name__}: {str(e)}")
            else:
                handle.write(f"{func.__name__} raised {type(e).__name__}: {str(e)}" + "\n")
            raise e

    return inner


