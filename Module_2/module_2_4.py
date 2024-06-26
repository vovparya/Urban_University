
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

primes = []
not_primes = []

 # Если `is_prime` после проверок остается `True`, то число добавляем в список `primes`.
 # В противном случае (если `is_prime` равно `False`), добавляем число в список `not_primes`.

for number in numbers:
    is_prime = True
    if number <= 1:
        is_prime = False
    else:
        for i in range(2, number):
            if number % i == 0:
                is_prime = False
                break
    if is_prime:
        primes.append(number)
    elif number > 1:
        not_primes.append(number)

print(f"Primes: {primes}")
print(f"Not Primes: {not_primes}")
