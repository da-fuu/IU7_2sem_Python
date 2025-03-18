import numpy as np
from itertools import combinations


def line_intersect_segment(line, segment):
    return (np.cross(segment[0]-line[0], line[1]-line[0]) >= 0) == (np.cross(segment[1]-line[0], line[1]-line[0]) <= 0)


def calc_intersecting_tr(line, triangles):
    count = 0
    for triangle in triangles:
        for edge in combinations(triangle, r=2):
            if line_intersect_segment(line, np.array(edge)):
                count += 1
                break
    return count


def calc_line(points, triangles):
    points = np.array(points)
    triangles = np.array(triangles)
    max_tr = 0
    max_line = None
    for pair in combinations(points, r=2):
        pair = np.array(pair)
        curr = calc_intersecting_tr(pair, triangles)
        if curr > max_tr:
            max_tr = curr
            max_line = pair.flatten()

    return max_line


def enlarge_ray(ray: np.ndarray, width, height):
    vec = ray[0] - ray[1]
    if vec[0] > 0:
        k1 = (width - ray[1][0]) / vec[0]
    elif vec[0] < 0:
        k1 = (0 - ray[1][0]) / vec[0]
    else:
        k1 = None

    if vec[1] > 0:
        k2 = (height - ray[1][1]) / vec[1]
    elif vec[1] < 0:
        k2 = (0 - ray[1][1]) / vec[1]
    else:
        k2 = None

    if k1 is None:
        ray[0] = ray[1] + vec * k2
        return
    if k2 is None:
        ray[0] = ray[1] + vec * k1
        return
    ray[0] = ray[1] + vec * max(k1, k2)


def enlarge(line: np.ndarray, width, height):
    line = line.reshape(2, 2)
    enlarge_ray(line, width, height)
    line = np.flip(line)
    enlarge_ray(line, width, height)
    return line.flatten()
