my_list = [42, 69, 0, 322, 13, 0, 99, -5, 9, 8, 7, -6, 5]

for i in my_list:
    if i > 0:
        print(i, end=' ')
    elif i < 0:
        break

