'''
Домашнее задание по теме "Выбор элементов и функции в SQL запросах"

Цель: научится использовать функции внутри запросов языка SQL и использовать их в решении задачи.

Задача "Средний баланс пользователя":
Для решения этой задачи вам понадобится решение предыдущей.
Для решения необходимо дополнить существующий код:
Удалите из базы данных not_telegram.db запись с id = 6.
Подсчитать общее количество записей.
Посчитать сумму всех балансов.
Вывести в консоль средний баланс всех пользователей.

Пример результата выполнения программы:
Выполняемый код:
# Код из предыдущего задания
# Удаление пользователя с id=6
# Подсчёт кол-ва всех пользователей
# Подсчёт суммы всех балансов
print(all_balances / total_users)
connection.close()

Вывод на консоль:
700.0
____________________________________________________________________________
'''

import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('../module_14_1/not_telegram.db')
cursor = conn.cursor()

# Удаление пользователя с id = 6
cursor.execute("DELETE FROM Users WHERE id = 6")

# Подсчёт общего количества записей
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

# Подсчёт суммы всех балансов
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

# Вывод среднего баланса
cursor.execute("SELECT AVG(balance) FROM Users")
average_balance = cursor.fetchone()[0]
print("Средний баланс всех пользователей:", average_balance)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
