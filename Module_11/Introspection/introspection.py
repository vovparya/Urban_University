'''
Домашнее задание по теме "Интроспекция"
Цель задания:

Закрепить знания об интроспекции в Python.
Создать персональную функции для подробной интроспекции объекта.

Задание:
Необходимо создать функцию, которая принимает объект (любого типа) в качестве аргумента и проводит интроспекцию
этого объекта, чтобы определить его тип, атрибуты, методы, модуль, и другие свойства.

1. Создайте функцию introspection_info(obj), которая принимает объект obj.
2. Используйте встроенные функции и методы интроспекции Python для получения информации о переданном объекте.
3. Верните словарь или строки с данными об объекте, включающий следующую информацию:
  - Тип объекта.
  - Атрибуты объекта.
  - Методы объекта.
  - Модуль, к которому объект принадлежит.
  - Другие интересные свойства объекта, учитывая его тип (по желанию).


Пример работы:
number_info = introspection_info(42)
print(number_info)

Вывод на консоль:
{'type': 'int', 'attributes': [...], 'methods': ['__abs__', '__add__', ...], 'module': '__main__'}

Рекомендуется создавать свой класс и объект для лучшего понимания
_________________________________________________________________________________________________________
'''

import inspect


def introspection_info(obj):
    """
    Функция проводит интроспекцию объекта и возвращает информацию о нем.

    Args:
      obj: Объект для интроспекции.

    Returns:
      Словарь с информацией об объекте.
    """

    info = {
        'type': type(obj).__name__,
        'attributes': [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith('__')],
        'methods': [method for method in dir(obj) if callable(getattr(obj, method)) and not method.startswith('__')],
        'module': obj.__class__.__module__ if hasattr(obj.__class__, '__module__') else None,
    }

    if isinstance(obj, (int, float)):
        info['value'] = obj
    elif isinstance(obj, str):
        info['length'] = len(obj)
    elif isinstance(obj, (list, tuple, set)):
        info['length'] = len(obj)
        info['elements_type'] = type(obj[0]).__name__ if obj else None
    elif inspect.isclass(obj):
        info['bases'] = [base.__name__ for base in obj.__bases__]

    return info


# Пример использования:
class MyClass:
    class_attribute = "Значение атрибута класса"

    def __init__(self, value):
        self.instance_attribute = value

    def instance_method(self):
        print("Метод экземпляра класса")


my_object = MyClass("Значение атрибута экземпляра")
object_info = introspection_info(my_object)
print(object_info)

number_info = introspection_info(42)
print(number_info)
