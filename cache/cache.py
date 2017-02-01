#! /usr/bin/env python3

"""Расширенный кэширующий декоратор.

Оборачивает функцию, кэшируя результат от входных параметров.

В классе `storage` должны быть реализованы следующие методы:
 * __contains__(self, value)
 * __getitem__(self, value)
 * __setitem__(self, key, value)
 * clear(self)

.. module:: cache

:Example:

>>> from cache import cache
>>> log = lambda *args, **kargs: print("I print my args", args, kargs)
>>> cached_log = cache(log)
>>> cached_log(1, x=3)
I print my args (1,) {'x': 3}
>>> cached_log(1, x=3)

:Example:

>>> from cache import md5_hash_args, cache
>>> from urllib.request import urlopen
>>> storage = dict()
>>> cached_urlopen = cache(urlopen, storage, md5_hash_args)
>>> cached_urlopen("https://www.python.org/").read()[:50]
b'<!doctype html>\n<!--[if lt IE 7]>   <html class="n'

.. todo:: Сделать class FileSystemStorage, который сохраняет кэш в
    файловой системе
.. todo:: Добавить тесты и описание

"""

from hashlib import md5 as hashlib_md5
from json import loads as json_loads, dumps as json_dumps


class JsonStorage(dict):
    """Сохраняет кэш в json файлы.

    :Example:

    >>> storage = JsonStorage("test.json")
    >>> storage
    {}

    """

    def __init__(self, filename, initial_value=None):
        self._filename = str(filename)
        try:
            with open(filename, 'r') as file:
                super(JsonStorage, self).__init__(json_loads(file.read()))
        except (FileNotFoundError, ValueError):
            initial_value = {} if initial_value is None else initial_value
            super(JsonStorage, self).__init__(initial_value)

    def __del__(self):
        with open(self._filename, 'w') as file:
            file.write(json_dumps(self))
        del self

    def __repr__(self):
        return super(JsonStorage, self).__repr__()


def simple_hash_args(args, kargs):
    """Находит хэш для аргументов.

    Sort kargs and calc hash(args, tuple(kargs))

    :param args: ordered arguments
    :type args: tuple
    :param kargs: unordered arguments
    :type args: dict
    :returns: hash of got arguments
    :rtype: str

    .. note:: может быть полезна для при кэшировании только для текущей
        сессии интерпретатора.

    """
    kargs = list(kargs.items())
    kargs.sort()
    return hash((args, tuple(kargs)))


def md5_hash_args(args, kargs):
    """Находит хэш для аргументов используя md5.

    :param args: ordered arguments
    :type args: tuple
    :param kargs: unordered arguments
    :type args: dict
    :returns: hash of got arguments
    :rtype: str

    .. note:: может быть полезна для при кэшировании данных между
        разными сессиями интерпретатора.

    """
    kargs = list(kargs.items())
    kargs.sort()
    return str(hashlib_md5(('%s:%s' % (repr(args), repr(tuple(kargs)))).encode())
               .digest())[2:-1]


def cache(function, storage=None, hash_function=simple_hash_args):
    """Кэширующий декоратор.

    Обёрнутая функция имеет `force_call` аттрибут, который может использоваться
    для принудительного вызова первоначальной функции. Вызов `force_call`
    обновляет значение в кэше.

    :param function: Оборачиваемая функция
    :param storage: Объект для сохранения кэша
    :param hash_function: Функция, хэширующая аргументы
    :returns: Значение вызываемой функции

    """
    storage = dict() if storage is None else storage

    def cached(*args, **kargs):
        args_hash = hash_function(args, kargs)
        if args_hash in storage:
            data = storage[args_hash]
            return data
        data = function(*args, **kargs)
        storage[args_hash] = data
        return data

    def force_call(*args, **kargs):
        """Принудтельно вызвать функцю и обновить кэш."""
        args_hash = hash_function(args, kargs)
        data = function(*args, **kargs)
        storage[args_hash] = data
        return data

    def cache_clear():
        """Clear storage object"""
        storage.clear()

    cached.__doc__ = function.__doc__
    cached.force_call = force_call
    cached.cache_clear = cache_clear
    return cached


def main():
    def test_func(*args, **kargs):
        print('call', args, kargs)
        return (args, kargs)

    storage = JsonStorage('.005.json')
    test_func = cache(test_func, storage, md5_hash_args)

    test_func(2, k=1)
    test_func(2, k=1)
    test_func(2, k=3)
    print("Clear")
    test_func.cache_clear()
    test_func(2, k=1)
    test_func(2, k=1)
    test_func(2, k=1)
    print('Storage:', storage)


if __name__ == '__main__':
    main()
