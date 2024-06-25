my_list = [42, 69, 0, 322, 13, 0, 99, -5, 9, 8, 7, -6, 5]

index = 0

while index < len(my_list):
    if my_list[index] < 0:
        break
    if my_list[index] != 0:
        print(my_list[index])
    index += 1
