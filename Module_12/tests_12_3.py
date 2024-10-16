'''
Домашнее задание по теме "Систематизация и пропуск тестов".
Цель: понять на практике как объединять тесты при помощи TestSuite. Научиться пропускать тесты при помощи встроенных в
unittest декораторов.

Задача "Заморозка кейсов":
Подготовка:
В этом задании используйте те же TestCase, что и в предыдущем: RunnerTest и TournamentTest.
Часть 1. TestSuit.
Создайте модуль suite_12_3.py для описания объекта TestSuite. Укажите на него переменной с произвольным названием.
Добавьте тесты RunnerTest и TournamentTest в этот TestSuit.
Создайте объект класса TextTestRunner, с аргументом verbosity=2.
Часть 2. Пропуск тестов.
Классы RunnerTest дополнить атрибутом is_frozen = False и TournamentTest атрибутом is_frozen = True.
Напишите соответствующий декоратор к каждому методу (кроме @classmethod), который при значении is_frozen = False будет
выполнять тесты, а is_frozen = True - пропускать и выводить сообщение 'Тесты в этом кейсе заморожены'.
Таким образом вы сможете контролировать пропуск всех тестов в TestCase изменением всего одного атрибута.
Запустите TestSuite и проверьте полученные результаты тестов из обоих TestCase.
Пример результата выполнения тестов:
Вывод на консоль:
test_challenge (tests_12_3.RunnerTest.test_challenge) ... ok
test_run (tests_12_3.RunnerTest.test_run) ... ok
test_walk (tests_12_3.RunnerTest.test_walk) ... ok
test_first_tournament (tests_12_3.TournamentTest.test_first_tournament) ... skipped 'Тесты в этом кейсе заморожены'
test_second_tournament (tests_12_3.TournamentTest.test_second_tournament) ... skipped 'Тесты в этом кейсе заморожены'
test_third_tournament (tests_12_3.TournamentTest.test_third_tournament) ... skipped 'Тесты в этом кейсе заморожены'
----------------------------------------------------------------------
Ran 6 tests in 0.000s OK (skipped=3)
____________________________________________________________________________________
'''

import unittest


class RunnerTest(unittest.TestCase):
    is_frozen = False  # Атрибут для управления пропуском тестов

    def freeze_test(func):
        def wrapper(*args, **kwargs):
            if RunnerTest.is_frozen:
                raise unittest.SkipTest("Тесты в этом кейсе заморожены")
            return func(*args, **kwargs)

        return wrapper

    @freeze_test
    def test_challenge(self):
        self.assertEqual(1, 1)

    @freeze_test
    def test_run(self):
        self.assertEqual(1 + 1, 2)

    @freeze_test
    def test_walk(self):
        self.assertTrue(True)


class TournamentTest(unittest.TestCase):
    is_frozen = True  # Атрибут для управления пропуском тестов

    def freeze_test(func):
        def wrapper(*args, **kwargs):
            if TournamentTest.is_frozen:
                raise unittest.SkipTest("Тесты в этом кейсе заморожены")
            return func(*args, **kwargs)

        return wrapper

    @freeze_test
    def test_first_tournament(self):
        self.assertTrue(True)

    @freeze_test
    def test_second_tournament(self):
        self.assertTrue(True)

    @freeze_test
    def test_third_tournament(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
