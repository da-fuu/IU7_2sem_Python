from numpy import linspace
from sympy import lambdify, diff
from sympy.abc import x

EPS = 10**-8


# Поиск корня методом Ньютона
def find_root_from_point(arg, func, derivative, eps, n_max):
    for i in range(n_max):
        der = derivative(arg)
        if abs(der) < EPS:
            return -1, arg
        if abs(func(arg)) < eps:
            return i, arg
        arg = arg - func(arg) / derivative(arg)
    return -2, arg


# Поиск корня на промежутке
def find_root_on_seg(start, stop, func, derivative, eps, n_max):
    iters, arg = find_root_from_point(start, func, derivative, eps, n_max)
    if iters < 0 or not (start - EPS <= arg <= stop + EPS):
        iters, arg = find_root_from_point(stop, func, derivative, eps, n_max)
    if iters < 0:
        return arg, n_max, -iters
    if not (start - EPS <= arg <= stop + EPS):
        return arg, iters, 3
    return arg, iters, 0


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
def find_all_roots(function, derivative, start, stop, step, nmax, eps):
    result = []
    root_segments = find_root_segments(function, start, stop, step)
    for seg in root_segments:
        arg, iters, err_code = find_root_on_seg(*seg, function, derivative, eps, nmax)
        result.append((*seg, arg, function(arg), iters, err_code))
    return result


# Рисование графика
def find_012_order_roots(function, start, stop, step, nmax, eps):
    functions = [lambdify(x, diff(function, x, i)) for i in range(4)]
    data = [find_all_roots(functions[i], functions[i+1], start, stop, step, nmax, eps) for i in range(3)]
    return data


# Выделение корня из результата
def extract_roots(data, func):
    return list(zip(*[(res[2], func(res[2])) for res in data if res[5] == 0]))
