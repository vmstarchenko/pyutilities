# pyutilities
Some tools for python

## Небольшие находки
  - У каждого файлового объекта (в том числе и `sys.stdout`) есть аттрибут `buffer`.
    `buffer` - тот же файл, но откртый в byte режиме. Я так понял, он ещё вроде
    и буфферизирует вывод.

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
