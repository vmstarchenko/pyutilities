# pyutilities
Some tools for python

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
      свойству можно объявить `setter` и `deletter`.
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
      ```
      Вообще, про дескрипторы данных много есть всего интересного.
