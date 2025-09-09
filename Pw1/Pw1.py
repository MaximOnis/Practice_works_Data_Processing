# Рекурсивна функція для перетворення десяткового числа у двійкову систему(допущено введення від'ємних чисел)
def get_bin(num, result=None):
    if num == 0 and result is None:
        return '0'

    if num < 0:
        return '-' + get_bin(abs(num))

    if result is None:
        result = []

    if num >= 1:
        get_bin(num // 2, result)
        result.append(str(num % 2))
    return ''.join(result)


# Функція для перетворення двійкового числа у десяткове(також допущено від'ємні двійкові числа)
def get_decimal(binar):
    if binar[0] == '-':
        symbols = list(binar[1:])
        sign = -1
    else:
        symbols = list(binar)
        sign = 1

    result = 0
    length = len(symbols) - 1

    for index in range(length + 1):
        result += int(symbols[index]) * (2 ** (length - index))

    result *= sign

    return result


# Тестування
# -10010
print(get_bin(18))
# -18
print(get_decimal(get_bin(18)))

# 0
print(get_bin(0))
# 0
print(get_decimal(get_bin(0)))

# 1
print(get_bin(1))
# 1
print(get_decimal(get_bin(1)))

# 10011
print(get_bin(19))
# 19
print(get_decimal(get_bin(19)))

# 101000001
print(get_bin(321))
# 321
print(get_decimal(get_bin(321)))
