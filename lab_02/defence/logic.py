from numpy import linspace
from sympy import lambdify, diff
from sympy.abc import x

EPS = 10**-8


# Поиск корня на промежутке методом половинного деления
def find_root_on_seg(start, stop, func, eps, n_max):
    if abs(func(stop)) <= eps:
        return stop, 0, 0
    for i in range(n_max):
        if abs(func(start)) <= eps:
            return start, i, 0
        mid = (stop + start) / 2
        if func(start) * func(mid-EPS) <= 0:
            stop = mid
        else:
            start = mid
    return start, n_max, 1


# Поиск знакопеременных отрезков
def find_root_segments(func, start, stop, step):
    x_arr = list(linspace(start, stop, round((stop-start)/step) + 1))
    root_segments = []
    last_y = func(x_arr[0])
    for i, arg in enumerate(x_arr[1:], start=1):
        new_y = func(arg - EPS)
        if last_y * new_y <= 0:
            root_segments.append((x_arr[i-1], arg))
        last_y = func(arg)
    if root_segments and root_segments[-1][1] == x_arr[-1]:
        return root_segments
    if func(x_arr[-2]+EPS) * func(x_arr[-1]) <= 0:
        root_segments.append((x_arr[-2], x_arr[-1]))
    return root_segments


# Полная обработка функции
def find_all_roots(function, start, stop, step, nmax, eps):
    result = []
    root_segments = find_root_segments(function, start, stop, step)
    for seg in root_segments:
        arg, iters, err_code = find_root_on_seg(*seg, function, eps, nmax)
        result.append((*seg, arg, function(arg), iters, err_code))
    return result


# Поиск данных о корнях 0, 1, 2 порядка
def find_012_order_roots(function, start, stop, step, nmax, eps):
    functions = [lambdify(x, diff(function, x, i)) for i in range(3)]
    data = [find_all_roots(functions[i], start, stop, step, nmax, eps) for i in range(3)]
    return data


# Выделение корня из результата
def extract_roots(data, func):
    return list(zip(*[(res[2], func(res[2])) for res in data if res[5] == 0]))
