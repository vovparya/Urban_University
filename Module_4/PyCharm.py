def test_function():
    def inner_function():
        print("Я в области видимости функции test_function")

    inner_function()


# inner_function() - возникает ошибка, так как inner_function() доступна только внутри test_function().
test_function()
