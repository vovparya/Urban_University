'''
Домашнее задание по теме "Сложные моменты и исключения в стеке вызовов функции".
Цель: понять как работают исключения внутри функций и как обрабатываются
эти исключения на практике при помощи try-except.

Задача "План перехват":
Напишите 2 функции:
Функция personal_sum(numbers):
Должна принимать коллекцию numbers.
Подсчитывать сумму чисел в numbers путём перебора и увеличивать переменную result.
Если же при переборе встречается данное типа отличного от числового, то обработать
исключение TypeError, увеличив счётчик incorrect_data на 1.
В конечном итоге функция возвращает кортеж из двух значений: result - сумма чисел,
incorrect_data - кол-во некорректных данных.
Функция calculate_average(numbers)
Среднее арифметическое - сумма всех данных делённая на их количество.
Должна принимать коллекцию numbers и возвращать: среднее арифметическое всех чисел.
Внутри для подсчёта суммы используйте функцию personal_sum написанную ранее.
Т.к. коллекция numbers может оказаться пустой, то обработайте
исключение ZeroDivisionError при делении на 0 и верните 0.
Также в numbers может быть записана не коллекция, а другие типы данных, например числа. Обработайте исключение
TypeError выводя строку 'В numbers записан некорректный тип данных'. В таком случае функция просто вернёт None.

Пункты задачи:
Создайте функцию personal_sum на основе условий задачи.
Создайте функцию calculate_average на основе условий задачи.
Вызовите функцию calculate_average несколько раз, передав в неё данные разных вариаций.
Пример результата выполнения программы:
Пример выполнения программы:
print(f'Результат 1: {calculate_average("1, 2, 3")}') # Строка перебирается, но каждый символ - строковый тип
print(f'Результат 2: {calculate_average([1, "Строка", 3, "Ещё Строка"])}') # Учитываются только 1 и 3
print(f'Результат 3: {calculate_average(567)}') # Передана не коллекция
print(f'Результат 4: {calculate_average([42, 15, 36, 13])}') # Всё должно работать

Вывод на консоль:
Некорректный тип данных для подсчёта суммы - 1
Некорректный тип данных для подсчёта суммы - ,
Некорректный тип данных для подсчёта суммы -
Некорректный тип данных для подсчёта суммы - 2
Некорректный тип данных для подсчёта суммы - ,
Некорректный тип данных для подсчёта суммы -
Некорректный тип данных для подсчёта суммы - 3
Результат 1: 0
Некорректный тип данных для подсчёта суммы - Строка
Некорректный тип данных для подсчёта суммы - Ещё Строка
Результат 2: 2.0
В numbers записан некорректный тип данных
Результат 3: None
Результат 4: 26.5
_______________________________________________________________________________________________________
'''


def personal_sum(numbers):
    result = 0
    incorrect_data = 0

    for num in numbers:
        try:
            # Пробуем добавить число к результату
            result += num
        except TypeError:
            # Увеличиваем счётчик некорректных данных и выводим сообщение
            incorrect_data += 1
            print(f'Некорректный тип данных для подсчёта суммы - {num}')

    return result, incorrect_data


def calculate_average(numbers):
    try:
        # Функция "hasattr(obj, name)" проверяет, имеет ли объект "obj" атрибут с именем "name".
        # В моём случае проверяется, является ли объект "numbers" итерируемым.
        if not hasattr(numbers, '__iter__'):  # "__iter__" — присутствует у всех итерируемых объектов.
            raise TypeError("Входной параметр не является коллекцией")

            # Если у объекта есть этот атрибут "__iter__" (т.е. он возвращает итератор),
            # это значит, что он может быть итерирован с помощью циклов (например, `for`).
            #
            # Функция проверяет, имеет ли объект "numbers" атрибут "__iter__".
            # Если атрибута нет (то есть "numbers" не является итерируемым объектом), условие вернёт "True",
            # и код внутри блока "if" выполнится, отображая исключение "TypeError".

        total, incorrect_data = personal_sum(numbers)

        # Вычисляем количество корректных данных
        count = len(numbers) - incorrect_data

        if count == 0:
            return 0
        return total / count
    except TypeError:
        print('В numbers записан некорректный тип данных')
        return None


# Примеры вызовов функции calculate_average
print(f'Результат 1: {calculate_average("1, 2, 3")}')  # Строка перебирается, но каждый символ - строковый тип
print(f'Результат 2: {calculate_average([1, "Строка", 3, "Ещё Строка"])}')  # Учитываются только 1 и 3
print(f'Результат 3: {calculate_average(567)}')  # Передана не коллекция
print(f'Результат 4: {calculate_average([42, 15, 36, 13])}')  # Всё должно работать
