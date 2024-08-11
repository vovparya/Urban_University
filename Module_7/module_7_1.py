'''
Цель: закрепить знания о работе с файлами (чтение/запись) решив задачу.

Задача "Учёт товаров":
Необходимо реализовать 2 класса Product и Shop, с помощью которых будет производиться запись в файл с продуктами.
Объекты класса Product будут создаваться следующим образом - Product('Potato', 50.0, 'Vagetables')
и обладать следующими свойствами:
Атрибут name - название продукта (строка).
Атрибут weight - общий вес товара (дробное число) (5.4, 52.8 и т.п.).
Атрибут category - категория товара (строка).
Метод __str__, который возвращает строку в формате '<название>, <вес>, <категория>'.
Все данные в строке разделены запятой с пробелами.

Объекты класса Shop будут создаваться следующим образом - Shop() и обладать следующими свойствами:
Инкапсулированный атрибут __file_name = 'products.txt'.
Метод get_products(self), который считывает всю информацию из файла __file_name, закрывает его и возвращает
единую строку со всеми товарами из файла __file_name.
Метод add(self, *products), который принимает неограниченное количество объектов класса Product.
Добавляет в файл __file_name каждый продукт из products, если его ещё нет в файле (по названию).
Если такой продукт уже есть, то не добавляет и выводит строку 'Продукт <название> уже есть в магазине' .

Пример результата выполнения программы:
Пример работы программы:
s1 = Shop()
p1 = Product('Potato', 50.5, 'Vegetables')
p2 = Product('Spaghetti', 3.4, 'Groceries')
p3 = Product('Potato', 5.5, 'Vegetables')

print(p2) # __str__

s1.add(p1, p2, p3)

print(s1.get_products())

Вывод на консоль:
Первый запуск:
Spaghetti, 3.4, Groceries
Продукт Potato уже есть в магазине
Potato, 50.5, Vegetables
Spaghetti, 3.4, Groceries
Второй запуск:
Spaghetti, 3.4, Groceries
Продукт Potato уже есть в магазине
Продукт Spaghetti уже есть в магазине
Продукт Potato уже есть в магазине
Potato, 50.5, Vegetables
Spaghetti, 3.4, Groceries

Примечания:
Не забывайте при записи в файл добавлять спец. символ перехода на следующую строку в конце - '\n'.
При проверке на существование товара в методе add можно вызывать метод get_products для получения текущих продуктов.
Не забывайте закрывать файл вызывая метод close() у объектов файла.

____________________________________________________________________________________________
'''


class Product:
    def __init__(self, name, weight, category):
        self.name = name
        self.weight = weight
        self.category = category

    def __str__(self):
        return f"{self.name}, {self.weight}, {self.category}"


class Shop:
    def __init__(self):
        self.__file_name = 'products.txt'

    def get_products(self):
        try:
            with open(self.__file_name, 'r') as file:
                return file.read().strip()  # Считываем все содержимое файла и убираем пробелы по краям
        except FileNotFoundError:
            return "Файл не найден."

    def add(self, *products):
        existing_products = self.get_products().splitlines() if self.get_products() else []
        for product in products:
            '''
            В языке Python имеется 3 способа создавать (генерировать) списки:
            - при помощи циклов;
            - при помощи функции map();
            - при помощи list comprehension - Мы это еще не изучали, но пробую использовать его 
                (https://smartiqa.ru/blog/python-list-comprehension).
            '''
            if product.name in [p.split(', ')[0] for p in existing_products]:
                '''
                p.split(', ') - метод split разбивает строку 'p' на части, используя запятую и пробел (', ') 
                в качестве разделителя. Это означает, что если строка продукта имеет формат,
                "Potato, 50.5, Vegetables", то split преобразует ее в список:["Potato", "50.5", "Vegetables"].
                
                p.split(', ')[0] - здесь мы берем только первый 
                элемент из полученного списка, то есть имя(название) продукта. 
                Таким образом, p.split(', ')[0] возвращает имя продукта, которое находится перед первым 
                разделителем (запятой и пробелом).
                
                for p in existing_products - ну а это простой цикл, который перебирает каждый элемент `p` в 
                списке existing_products.
                            
                В итоге, [p.split(', ')[0] for p in existing_products] создает список имен всех продуктов, 
                которые уже находятся в файле products.txt. Это позволяет в последующей 
                проверке (if product.name in [...]) сравнить имя нового продукта с уже существующими именами 
                продуктов в файле. Если имя продукта уже присутствует, выдается сообщение о том, 
                что продукт уже есть в магазине.
                '''
                print(f'Продукт {product.name} уже есть в магазине')
            else:
                with open(self.__file_name, 'a') as file:
                    file.write(str(product) + '\n')  # Записываем продукт в файл с переходом на новую строку


# Пример работы программы
s1 = Shop()
p1 = Product('Potato', 50.5, 'Vegetables')
p2 = Product('Spaghetti', 3.4, 'Groceries')
p3 = Product('Potato', 5.5, 'Vegetables')

print(p2)  # __str

s1.add(p1, p2, p3)  # Добавляем продукты

print(s1.get_products())  # Получаем список продуктов
