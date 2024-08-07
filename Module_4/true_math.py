'''
`true_math.py` часть домашнего задания 'module_4_1':
   - Импортируем `inf` (бесконечность) из модуля `math`.
   - Определяем функцию `divide`, которая:
     - Проверяет, равен ли второй аргумент (`second`) нулю.
     - Если да, возвращает `inf` (бесконечность).
     - Если нет, возвращает результат деления первого аргумента (`first`) на второй (`second`).
___________________________________________________________________________________
'''

from math import inf


def divide(first, second):
    if second == 0:
        return inf
    else:
        return first / second
