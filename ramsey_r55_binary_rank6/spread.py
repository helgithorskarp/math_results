#!/usr/bin/env python3
"""An explicit symplectic spread from GF(8); output is a tiny certificate."""
import json


def multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 8:
            a ^= 0b1011  # t^3+t+1
        b >>= 1
    return result


def trace(a):
    square = multiply(a, a)
    return a ^ square ^ multiply(square, square)


def produce():
    dual = [next(b for b in range(8) if all(trace(multiply(1 << i, b)) == int(i == j)
                                          for i in range(3))) for j in range(3)]
    inverse = {}
    for bits in range(8):
        field = 0
        for i in range(3):
            if bits >> i & 1:
                field ^= dual[i]
        inverse[field] = bits
    classes = [[x | (inverse[multiply(slope, x)] << 3) for x in range(1, 8)]
               for slope in range(8)]
    classes.append([bits << 3 for bits in range(1, 8)])
    return {"field_polynomial_bits": 11, "dual_basis": dual,
            "coordinate_convention": "x bits0..2, trace-dual y bits3..5",
            "zero_color": 0, "classes": classes}


if __name__ == "__main__":
    print(json.dumps(produce(), indent=2))
