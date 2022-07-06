import functools
from datetime import datetime


def log(func):
    """логирование в файл log.txt"""

    @functools.wraps(func)
    def wrapper_log(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        myFile = open('log.txt', 'a', encoding='UTF8')
        myFile.write(f'\n\n {datetime.now()}  ----------------------------Вызываем {func.__name__}--------------------'
                     f'-----------\n')
        myFile.write(f'Параметры запроса:\n')
        myFile.write(f'\n{signature[47:]}\n')
        status, result = func(*args, **kwargs)
        myFile.write(f'\n {datetime.now()}  ---------------------------Функция {func.__name__!r} вернула значение-----'
                     f'------------\n')
        myFile.write(f"\nКод ответа - {status}\n\nТело ответа:\n\n {result}")
        myFile.close()
        return status, result
    return wrapper_log