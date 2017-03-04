#! /usr/bin/env python3


class LabelException(Exception):
    """Исключение, прокидываемое лэйблом для выхода из опратора контекста."""

    def __init__(self, label=None):
        self.label = label


class Label:
    """Лэйбл цикла.

    Реализовывает лэйблы циклов с помощью оператора контекста. Для выхода
    из оператора контекста, соответствующему данному лэйблу необходимо
    сделать вызов объекта лэйбла. При этом будет брошено `LabelException`.

    :Example:

    >>> with Label() as label1:
    ...     for i in range(3):
    ...         print('i:', i)
    ...         if i == 1:
    ...             label1()
    ...
    i: 0
    i: 1
    >>> with Label() as label1:   # При вложеных лэйблах переходит именно на
    ...     for i in range(3):    # тот лэйбл, который был вызван.
    ...         print('i:', i)
    ...         with Label() as label2:
    ...             for j in range(3):
    ...                 print('i: %d, j: %d' % (i, j))
    ...                 if i == 1 and j == 0:
    ...                     label1()
    ...
    i: 0
    i: 0, j: 0
    i: 0, j: 1
    i: 0, j: 2
    i: 1
    i: 1, j: 0

    """

    def __repr__(self):
        return '<Label %x>' % id(self)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if getattr(exception_value, 'label', None) is self:
            return True

    def __call__(self):
        raise LabelException(self)

if __name__ == '__main__':
    with Label() as c1:
        for i in range(3):
            print('i:', i)
            if i == 1:
                c1()
    print()

    with Label() as c1:
        for i in range(3):
            print('i:', i)
            for j in range(3):
                print('i: %d, j: %d' % (i, j))
                if i == 1 and j == 0:
                    c1()
    print()

    with Label() as c1:
        for i in range(3):
            print('i:', i)
            with Label() as c2:
                for j in range(3):
                    print('i: %d, j: %d' % (i, j))
                    if i == 1 and j == 0:
                        c1()
    print()

    with Label() as c1:
        for i in range(3):
            print('i:', i)
            with Label() as c2:
                for j in range(3):
                    print('i: %d, j: %d' % (i, j))
                    if i == 1 and j == 0:
                        c2()
