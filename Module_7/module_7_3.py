'''
Домашнее задание по теме "Оператор "with".
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.

Цель: применить на практике оператор with, вспомнить написание кода в парадигме ООП.

Задача "Найдёт везде":
Напишите класс WordsFinder, объекты которого создаются следующим образом:
WordsFinder('file1.txt, file2.txt', 'file3.txt', ...).
Объект этого класса должен принимать при создании неограниченного количество названий файлов и
записывать их в атрибут file_names в виде списка или кортежа.

Также объект класса WordsFinder должен обладать следующими методами:
get_all_words - подготовительный метод, который возвращает словарь следующего вида:
{'file1.txt': ['word1', 'word2'], 'file2.txt': ['word3', 'word4'], 'file3.txt': ['word5', 'word6', 'word7']}
Где:
'file1.txt', 'file2.txt', ''file3.txt'' - названия файлов.
['word1', 'word2'], ['word3', 'word4'], ['word5', 'word6', 'word7'] - слова содержащиеся в этом файле.
Алгоритм получения словаря такого вида в методе get_all_words:
Создайте пустой словарь all_words.
Переберите названия файлов и открывайте каждый из них, используя оператор with.
Для каждого файла считывайте единые строки, переводя их в нижний регистр (метод lower()).
Избавьтесь от пунктуации [',', '.', '=', '!', '?', ';', ':', ' - '] в строке. (тире обособлено пробелами, это
не дефис в слове).
Разбейте эту строку на элементы списка методом split(). (разбивается по умолчанию по пробелу)
В словарь all_words запишите полученные данные, ключ - название файла, значение - список из слов этого файла.

find(self, word) - метод, где word - искомое слово. Возвращает словарь, где ключ - название файла,
значение - позиция первого такого слова в списке слов этого файла.
count(self, word) - метод, где word - искомое слово. Возвращает словарь, где ключ - название файла,
значение - количество слова word в списке слов этого файла.
В методах find и count пользуйтесь ранее написанным методом get_all_words для
получения названия файла и списка его слов.
Для удобного перебора одновременно ключа(названия) и значения(списка слов)
можно воспользоваться методом словаря - item().

for name, words in get_all_words().items():
  # Логика методов find или count

Пример результата выполнения программы:
Представим, что файл 'test_file.txt' содержит следующий текст:


Пример выполнения программы:
finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words()) # Все слова
print(finder2.find('TEXT')) # 3 слово по счёту
print(finder2.count('teXT')) # 4 слова teXT в тексте всего

Вывод на консоль:
{'test_file.txt': ["it's", 'a', 'text', 'for', 'task', 'найти', 'везде', 'используйте', 'его',
'для', 'самопроверки', 'успехов', 'в', 'решении', 'задачи', 'text', 'text', 'text']}
{'test_file.txt': 3}
{'test_file.txt': 4}

Примечания:
Регистром слов при поиске можно пренебречь. ('teXT' ~ 'text')
Решайте задачу последовательно - написав один метод, проверьте результаты его работы.
______________________________________________________________________________________________________
'''

import string


class WordsFinder:
    # Конструктор __init__:
    # принимает неограниченное количество аргументов (названий файлов) и сохраняет их в
    # атрибуте file_names в виде кортежа.
    def __init__(self, *file_names):
        # Сохраняем названия файлов в виде кортежа
        self.file_names = file_names

    def get_all_words(self):
        # Метод get_all_words:
        #    - Создает пустой словарь all_words.
        #    - Перебирает названия файлов и открывает каждый файл с помощью оператора with.
        #    - Читает содержимое файла, переводит его в нижний регистр и убирает пунктуацию с помощью метода translate.
        #    - Разбивает текст на слова с помощью метода split() и добавляет их в словарь,
        #      где ключ - название файла, а значение - список слов.
        all_words = {}

        # Перебираем названия файлов
        for file_name in self.file_names:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    # Читаем все строки файла
                    content = file.read().lower()  # Переводим в нижний регистр
                    # Убираем пунктуацию
                    content = content.translate(str.maketrans('', '', string.punctuation))
                    # Разбиваем текст на слова
                    words = content.split()
                    # Записываем в словарь
                    all_words[file_name] = words
            except FileNotFoundError:
                print(f"Файл {file_name} не найден.")

        return all_words

    def find(self, word):
        # Метод find:
        #    - Принимает слово для поиска, приводит его к нижнему регистру и создает пустой словарь result.
        #    - Вызывает метод get_all_words для получения всех слов из файлов.
        #    - Перебирает файлы и их слова, проверяет наличие искомого слова и сохраняет позицию первого
        #      вхождения (прибавляя 1 для соответствия индексации).
        word = word.lower()  # Приводим к нижнему регистру
        result = {}
        all_words = self.get_all_words()

        for file_name, words in all_words.items():
            if word in words:
                position = words.index(word) + 1  # Позиция слова
                result[file_name] = position

        return result

    def count(self, word):
        # Метод count:
        #    - Аналогично методу find, но вместо нахождения позиции считает
        #      количество вхождений искомого слова в каждом файле.
        word = word.lower()  # Приводим к нижнему регистру
        result = {}
        all_words = self.get_all_words()

        for file_name, words in all_words.items():
            count = words.count(word)  # Считаем количество вхождений слова
            if count > 0:
                result[file_name] = count

        return result


# Пример выполнения программы:
finder2 = WordsFinder('test_file.txt')
print(finder2.get_all_words())  # Все слова
print(finder2.find('TEXT'))  # 3 слово по счёту
print(finder2.count('teXT'))  # 4 слова teXT в тексте всего
