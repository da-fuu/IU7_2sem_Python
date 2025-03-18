# Сложение двух цифр
def add_two(a, b):
    a, b = sorted([a, b])
    if a == '0' and b == '<':
        a, b = b, a
    tmp = a+b
    if tmp == '<<':
        return '>', '<'
    elif tmp == '<0':
        return '<', '0'
    elif tmp == '<>' or tmp == '00':
        return '0', '0'
    elif tmp == '0>':
        return '>', '0'
    elif tmp == '>>':
        return '<', '>'


# Сложение трех цифр
def add_three(a, b, c):
    s, carry1 = add_two(a, b)
    s, carry2 = add_two(s, c)
    carry, _ = add_two(carry1, carry2)
    return s, carry


# Сложение двух целых чисел одинаковой длины
def add_uints(a, b):
    carry = '0'
    s = ''
    for i in range(len(a) - 1, -1, -1):
        res, carry = add_three(a[i], b[i], carry)
        s = res + s
    return carry + s


# Подготовка строк
def prepare(ops):
    a, op, b = ops
    if op == '-':
        b = b.replace('>', '|').replace('<', '>').replace('|', '<')
    if '.' not in a:
        a += '.'
    if '.' not in b:
        b += '.'
    a1, a2 = a.split('.')
    b1, b2 = b.split('.')
    a1 = a1.zfill(len(b1))
    b1 = b1.zfill(len(a1))
    if len(a2) > len(b2):
        b2 = b2 + '0' * (len(a2) - len(b2))
    else:
        a2 = a2 + '0' * (len(b2) - len(a2))
    a = a1 + a2
    b = b1 + b2
    return a, b, len(a2)


# Основная функция вычислений
def compute(operands):
    a, b, len_part = prepare(operands)
    res = add_uints(a, b)
    if len_part > 0:
        res = res[:-len_part] + '.' + res[-len_part:]
    res = res.strip('0').removesuffix('.')
    if res == '':
        res = '0'
    if res[0] == '.':
        res = '0' + res
    return res
