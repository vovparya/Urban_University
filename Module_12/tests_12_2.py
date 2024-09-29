'''
Домашнее задание по теме "Методы Юнит-тестирования"
Цель: освоить методы, которые содержит класс TestCase.

Задача:
В первую очередь скачайте исходный код, который нужно обложить тестами с GitHub. (Можно скопировать)
В этом коде сможете обнаружить дополненный с предыдущей задачи класс Runner и новый класс Tournament.
Изменения в классе Runner:
Появился атрибут speed для определения скорости бегуна.
Метод __eq__ для сравнивания имён бегунов.
Переопределены методы run и walk, теперь изменение дистанции зависит от скорости.
Класс Tournament представляет собой класс соревнований, где есть дистанция, которую нужно пробежать и список участников.
Также присутствует метод start, который реализует логику бега по предложенной дистанции.

Напишите класс TournamentTest, наследованный от TestCase. В нём реализуйте следующие методы:

setUpClass - метод, где создаётся атрибут класса all_results. Это словарь
в который будут сохраняться результаты всех тестов.
setUp - метод, где создаются 3 объекта:
Бегун по имени Усэйн, со скоростью 10.
Бегун по имени Андрей, со скоростью 9.
Бегун по имени Ник, со скоростью 3.
tearDownClass - метод, где выводятся all_results по очереди в столбец.

Так же методы тестирования забегов, в которых создаётся объект Tournament на дистанцию 90. У объекта класса Tournament
запускается метод start, который возвращает словарь в переменную all_results. В конце вызывается метод assertTrue,
в котором сравниваются последний объект из all_results
(брать по наибольшему ключу) и предполагаемое имя последнего бегуна.
Напишите 3 таких метода, где в забегах участвуют (порядок передачи в объект Tournament соблюсти):
Усэйн и Ник
Андрей и Ник
Усэйн, Андрей и Ник.
Как можно понять: Ник всегда должен быть последним.

Дополнительно (не обязательно, не влияет на зачёт):
В данной задаче, а именно в методе start класса Tournament, допущена логическая ошибка. В результате его работы бегун
с меньшей скоростью может пробежать некоторые дистанции быстрее, чем бегун с большей.
Попробуйте решить эту проблему и обложить дополнительными тестами.
Пример результата выполнения тестов:
Вывод на консоль:
{1: Усэйн, 2: Ник}
{1: Андрей, 2: Ник}
{1: Андрей, 2: Усэйн, 3: Ник}

Ran 3 tests in 0.001s
OK

Примечания:
Ваш код может отличаться от строгой последовательности описанной в задании. Главное - схожая логика работы тестов
и наличие всех перечисленных переопределённых методов из класса TestCase.
________________________________________________________________________________________________________________
'''

import unittest
from runner_and_tournament import Runner, Tournament


class TournamentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.usain = Runner("Усэйн", 10)
        self.andrey = Runner("Андрей", 9)
        self.nick = Runner("Ник", 3)

    @classmethod
    def tearDownClass(cls):
        for key, value in cls.all_results.items():
            finishers_string = ", ".join(  # Соединяем строки с помощью ", "
                f"{place}: {runner.name}"
                for place, runner in value.items()
            )
            print(f"{{{finishers_string}}}")  # Выводим в фигурных скобках

    def test_usain_nick(self):
        tournament = Tournament(90, self.usain, self.nick)
        self.all_results["Усэйн и Ник"] = tournament.start()
        last_runner_name = self.all_results["Усэйн и Ник"][max(self.all_results["Усэйн и Ник"].keys())].name
        self.assertTrue(last_runner_name == self.nick.name)

    def test_andrey_nick(self):
        tournament = Tournament(90, self.andrey, self.nick)
        self.all_results["Андрей и Ник"] = tournament.start()
        last_runner_name = self.all_results["Андрей и Ник"][max(self.all_results["Андрей и Ник"].keys())].name
        self.assertTrue(last_runner_name == self.nick.name)

    def test_usain_andrey_nick(self):
        tournament = Tournament(90, self.usain, self.andrey, self.nick)
        self.all_results["Усэйн, Андрей и Ник"] = tournament.start()
        last_runner_name = self.all_results["Усэйн, Андрей и Ник"][
            max(self.all_results["Усэйн, Андрей и Ник"].keys())].name
        self.assertTrue(last_runner_name == self.nick.name)


if __name__ == '__main__':
    unittest.main()
