import numpy as np
from numpy.linalg import det


# Поиск расстояния между точками
def get_dist(a, b):
    return np.hypot(*(a - b))


# Найти описанную окружность около треугольника по точкам
def calc_circum(a, b, c):
    points = np.array((a, b, c))
    sq_sum = np.sum(points**2, axis=1)

    d = 2 * det((points[:, 0], points[:, 1], np.ones(3)))
    x = det((sq_sum, points[:, 1], np.ones(3))) / d
    y = -det((sq_sum, points[:, 0], np.ones(3))) / d
    center = np.array((x, y))
    return center, get_dist(a, center)


# Проверка того, лежит ли точка вне окружности
def is_outside(point, circle):
    return get_dist(point, circle[0]) > circle[1]


# Найти окружность через 2 конца диаметра
def get_circ_by_diam(a, b):
    return (a+b)/2, get_dist(a, b) / 2


# Найти минимальный круг через 2 точки и одну из точек множества
def min_disc_2_p(points, a, b):
    circle = get_circ_by_diam(a, b)
    for point in points:
        if is_outside(point, circle):
            circle = calc_circum(point, a, b)
    return circle


# Найти минимальный круг через точку и 2 точки множества
def min_disc_1_p(points, new_point):
    points = np.random.permutation(points)
    circle = get_circ_by_diam(points[0], new_point)
    for i in range(1, points.shape[0]):
        if is_outside(points[i], circle):
            circle = min_disc_2_p(points[:i], points[i], new_point)
    return circle


# Найти минимальный круг покрывающий все точки
def calc_circle(points):
    points = np.random.permutation(points)
    if points.shape[0] == 1:
        points = np.concatenate((points, points))
    circle = get_circ_by_diam(points[0], points[1])
    for i in range(2, points.shape[0]):
        if is_outside(points[i], circle):
            circle = min_disc_1_p(points[:i], points[i])
    return circle
