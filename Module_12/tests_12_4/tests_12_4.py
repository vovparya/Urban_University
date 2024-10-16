'''
Домашнее задание по теме "Логирование"
Если вы решали старую версию задачи, проверка будет производиться по ней.
Ссылка на старую версию тут.
Цель: получить опыт использования простейшего логирования совместно с тестами.

Задача "Логирование бегунов":
В первую очередь скачайте исходный код, который нужно обложить тестами с GitHub. (Можно скопировать)
Основное обновление - выбрасывание исключений, если передан неверный
тип в name и если передано отрицательное значение в speed.

Для решения этой задачи вам понадобиться класс RunnerTest из предыдущей задачи.
В модуле tests_12_4.py импортируйте пакет logging и настройте basicConfig на следующие параметры:
Уровень - INFO
Режим - запись с заменой('w')
Название файла - runner_tests.log
Кодировка - UTF-8
Формат вывода - на своё усмотрение, обязательная информация: уровень логирования, сообщение логирования.

Дополните методы тестирования в классе RunnerTest следующим образом:
test_walk:
Оберните основной код конструкцией try-except.
При создании объекта Runner передавайте отрицательное значение в speed.
В блок try добавьте логирование INFO с сообщением '"test_walk" выполнен успешно'
В блоке except обработайте исключение соответствующего типа и логируйте его на
уровне WARNING с сообщением "Неверная скорость для Runner".
test_run:
Оберните основной код конструкцией try-except.
При создании объекта Runner передавайте что-то кроме строки в name.
В блок try добавьте логирование INFO с сообщением '"test_run" выполнен успешно'
В блоке except обработайте исключение соответствующего типа и логируйте его на уровне
WARNING с сообщением "Неверный тип данных для объекта Runner".
_______________________________________________________________________________________________________
'''

import unittest
import logging
from rt_with_exceptions import Runner

logging.basicConfig(
    level=logging.INFO,
    filename='runner_tests.log',
    filemode='w',
    encoding='utf-8',
    format='%(asctime)s | %(levelname)s | %(message)s'
)


class RunnerTest(unittest.TestCase):
    is_frozen = False

    def freeze_test(func):
        def wrapper(*args, **kwargs):
            if RunnerTest.is_frozen:
                raise unittest.SkipTest("Тесты в этом кейсе заморожены")
            return func(*args, **kwargs)

        return wrapper

    @freeze_test
    def test_walk(self):
        """Тестирование метода walk с отрицательной скоростью."""
        try:
            runner = Runner('Вася', -5)
            runner.walk()
        except ValueError as e:
            logging.warning("Неверная скорость для Runner: %s", e)
        else:
            logging.info('"test_walk" выполнен успешно')
            self.fail("ValueError не было выброшено")

    @freeze_test
    def test_run(self):
        """Тестирование метода run с неверным типом для имени."""
        try:
            runner = Runner(123, 5)
            runner.run()
        except TypeError as e:
            logging.warning("Неверный тип данных для объекта Runner: %s", e)
        else:
            logging.info('"test_run" выполнен успешно')
            self.fail("TypeError не было выброшено")


if __name__ == "__main__":
    unittest.main()
