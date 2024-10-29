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
