# pyutilities
В этом репозитории складываются некоторые куски кода, которые могут
понадобиться в разных проектах. Это сделано просто чтобы не переписывать
одно и то же несколько раз.
Ещё тут есть просто интересные штуки. В частности, в ридми ниже пишутся
неочевидные особенности питона.

## Небольшие находки
  - У каждого файлового объекта (в том числе и `sys.stdout`) есть аттрибут `buffer`.
    `buffer` - тот же файл, но откртый в byte режиме. Я так понял, он ещё вроде
    и буфферизирует вывод.

  - Немного о `_`:
    * Используется в качестве переменной.
      - В интерактивной оболочке сохраняет последнее выисленное значение.
        ```python
        >>> 2 ** 10
        1024
        >>> _ * 2
        2048
        ```

      - Удобно использовать в циклах `for _ in generator: ... `, где нет
        необходимости сохранять значение переменной итерирования.

      - В генераторах и лямбда функциях.
        ```python
        bar = [chr(_) for _ in range(0, 255)]
        s = lambda _: _[3]
        ```

      - В Django переменную `_` принято использовать как алиас функции перевода.

    * Приватные свойства класса принято называть `_foo_method`. Это не только
      соглашение между программистами. Некоторые встроенные вещи также зависят от
      того как названа переменная. Например `help` не отображает в списке функций
      методы, начинающиеся с `_`.

    * Специальные методы имеют вид `__foo__`

    * Защищённые при наследовании методы имеют вид `__foo`

  - Модуль `logging` - годная замена дебаггингу принтами. Нужно как-нибудь сделать
    `logger_setup` - функцию, которая настраивает разные удобные логгеры и
    перестать пользоваться принтами при дебаге. Вместе с ним идут в комплекте
    `logging.config`, `logging.handler`.

  - У finally есть применение. Как сказано в документации, он выполняется всегда
    После выхода из try. Совсем всегда. Даже если наверх пробрасывается
    исключение, не обрабатываемое в данном блоке try и если внутри блоков try или
    except выполнен возврат.
    ```python
    >>> def foo():
    ...     try:
    ...         return
    ...     except IndexError:
    ...         return
    ...     finally:
    ...         print('execute finally')
    ...
    >>> foo()
    execute finally
    ```

  - Чтобы объект мог учавствовать в контекстном операторе необходимо реализовать
    методы `__enter__` и `__exit__`.

  - `yield` имеет некоторые приложения:
    * `yield from`
    * `value = (yield value)`
    * `generator.send`, `generator.throw`, `generator.close`

  - Надо бы почитать про ключевое слово `async`

  - `import inspect` содержит какую-то магию анализирующую код. С его помощью
    можно, например, получить сигнатуру функции. Возможно, понадобиться при
    реализации каррирования.

  - Встроенные декораторы:
    * `@classmethod` - - делает функцию методом класса (функцией класса,
      принимающей класс как первый аргумент `cls`)

    * `@staticmethod` - делает функцию статической (функцией класса, не
      принимающей `self` как первый аргумент)

    * `@property` - объявляет функцию класса свойством. Также к такому
      свойству можно объявить `setter` и `deleter`.
      ```python
      class Foo:
          ...
          @property
          def bar(self):
              ...
              return self.attr

          @bar.setter
          def bar(self, value):
              ...
              self.attr = value

          @bar.deleter
          def bar(self):
              ...
              self.attr = ''
      f = Foo()
      f.bar = 7
      ```
      Вообще, про дескрипторы данных много есть всего интересного.

  - Когда при деплое есть ограничение на количество загружаемых файлов
    исполняемого кода, можно просто сжать их в .zip файл. Питон умеет искать
    модули для импорта в архивах, разумеется, если они есть в путях.

  - Если перед завершением выполнения кода (естественным образом или в
    брошенного исключения) необходимо что-то обязательно выполнить (например,
    сохранить состояние каких-то переменных в файле), это можно сделать используя
    `import atexit`.

  - В `Python3.x` появилась удобная функция `str.maketrans`. Она может делать
    множественные замены. В том числе свапать одновременно.
    ```python
    >>> s = 'hello world'
    >>> s.replace('o', '').replace(' ', '').replace('e', '')  # Выглядит неочень
    'hllwrld'
    >>> s.translate(str.maketrans({'o':'', ' ': '', 'e':''})) # Уже лечше
    'hllwrld'
    >>> s.translate(str.maketrans('o':'e', 'e':'o', ' ':''})) # Бывает незаменимо без костылей
    'hollewerld'
    >>> s.translate(str.maketrans('oe', 'eo', ' '))           # Более короткий вариант записи
    'hollewerld'
    ```

  - Может быть это сверх очевидно, но для меня было открытием, что питон поддерживает
    такой синтаксис:
    ```python
    >>> class A():
    ...     def __getitem__(self, value):
    ...         print(value)
    ...
    >>> data = A()
    >>> data[['magic']]
    ['magic']
    >>> data[1, 1, 4, 7]
    (1, 1, 4, 7)
    >>> data[::-1, 1, 1:1, "lol", lambda _: _]
    (slice(None, None, -1), 1, slice(1, 1, None), 'lol', <function <lambda> at 0x7f95a619cea0>)
    ```

  - Профайлеры используются для сбора статистики по работе программы. Например, сколько по времени/памяти работают
    функции или отдельные строки.
    * В стандартной библиотеке есть некоторые тулзы ([Глава 27](https://docs.python.org/3.6/library/profile.html)). 
    * В этом цикле статей 
    ([1](https://habrahabr.ru/company/mailru/blog/201594/),
    [2](https://habrahabr.ru/company/mailru/blog/201778/),
    [3](https://habrahabr.ru/company/mailru/blog/202832/),
    [4(про дебаг, но тоде интересно)](https://habrahabr.ru/company/mailru/blog/205426/))
    всё очень круто описано, в том числе как всё использовать
    * [Тут](https://www.huyng.com/posts/python-performance-analysis) тоже есть что-то.

  - Про интерпретаторы
    * [Как]( https://m.habrahabr.ru/post/124418/) написать интерпретатор своего собственного языка программирования (PyPy).
    * [Статья](https://m.habrahabr.ru/post/209812/) про интерпретаторы питона.
      CPython, Cython, Jython, IronPython, PyPy, Brython и другие.
    * [Ещё что-то](http://www.opennet.ru/opennews/art.shtml?num=31482).

  - Из питона можно послылать сигналы.
    Например это то же самое, что и программа упала с сегфолтом:
    ```python
    >>> import signal, os
    >>> os.kill(os.getpid(), signal.SIGSEGV)
    ```
