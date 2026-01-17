import math

# Basic 3D vector helpers

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def length(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def normalize(a):
    l = length(a)
    if l == 0:
        return (0.0, 0.0, 0.0)
    return (a[0] / l, a[1] / l, a[2] / l)


def clamp(v, lo=0, hi=255):
    return int(max(lo, min(hi, v)))


def reflect(v, n):
    # Reflect v around normal n: v - 2*(v.n)*n
    vn = dot(v, n)
    return sub(v, scale(n, 2 * vn))
