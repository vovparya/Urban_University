import sqlite3

DB_NAME = 'products.db'


def initiate_db():
    """Создаём таблицу Products, если её ещё нет."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            price INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
    ''')
    conn.commit()
    conn.close()


def get_all_products():
    """Возвращаем все записи из таблицы Products."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products


def add_some_products():
    """Добавляем продукты в базу данных (для тестов)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    products_to_add = [
        ('Product1', 'Описание 1', 1500),
        ('Product2', 'Описание 2', 2000),
        ('Product3', 'Описание 3', 3000),
        ('Product4', 'Описание 4', 1000)
    ]
    cursor.executemany("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", products_to_add)
    conn.commit()
    conn.close()


def add_user(username, email, age):
    """Добавляем нового пользователя в таблицу Users."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO Users (username, email, age) VALUES (?, ?, ?)", (username, email, age))
        conn.commit()
    except sqlite3.IntegrityError:  # Обрабатываем ошибки дубликата username
        return False
    finally:
        conn.close()
    return True


def is_included(username):
    """Проверяем, существует ли пользователь с заданным username."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return bool(result)
