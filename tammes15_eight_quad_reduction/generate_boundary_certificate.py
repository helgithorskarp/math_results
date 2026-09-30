#!/usr/bin/env python3
"""Generate exact Bernstein tables from explicit integer polynomials.

Independent of check_boundary_patch.py's complex-product derivation.
CPython >=3.11, standard library; reads no certificate or scratch input.
"""
from fractions import Fraction as F
import json
import sys

import check as prior
from generate_one_five_certificate import bernstein


# Rows have increasing z degree; columns have increasing c degree.
R_ROWS = [
    [0,-12,-56,-32,168,188,-112,-144],
    [4,8,-72,-216,12,448,248,-48],
    [4,28,52,-24,-108,4,52,-8],
    [0,0,4,24,48,40,12,0],
]
S_ROWS = [
    [2,14,30,14,-26,-210,-734,-430,1176,-476,-6080,-7680,-4608,-1728],
    [8,70,198,130,-218,-386,-1486,-2842,2762,10132,3440,-5760,-4320,-1728],
    [12,128,478,550,-718,-1826,-554,-1350,-4006,-614,-1756,-10264,-7152,-576],
    [8,104,516,1022,-282,-3990,-3370,4566,6642,1638,1534,-2268,-5688,-432],
    [2,34,242,806,778,-2274,-5630,-274,6348,-1928,-8236,-2204,-1056,-432],
    [0,2,38,242,578,-118,-2530,-1750,4934,5036,-3564,-3396,672,-144],
    [0,0,2,22,94,122,-382,-1370,-758,1118,-348,-1796,240,-16],
    [0,0,0,-2,-14,-18,58,122,14,74,46,-304,24,0],
    [0,0,0,0,0,-4,-28,-64,-56,-36,-44,-24,0,0],
]


def polynomial(rows):
    terms = {}
    for j, row in enumerate(rows):
        for i, a in enumerate(row):
            e = [0]*prior.NV
            e[0], e[4] = i, j
            if a:
                terms[tuple(e)] = a
    return prior.Poly(terms)


def generate():
    result = {'schema': 1, 'c_interval': ['1/2', '3/5'],
              'z_interval': ['1', '3/2']}
    intervals = {0: (F(1,2), F(3,5)), 4: (F(1), F(3,2))}
    for name, rows, required in [('small_corner_R', R_ROWS, [7,3]),
                                  ('closing_S', S_ROWS, [13,8])]:
        degree, table = bernstein(polynomial(rows), intervals)
        prior.need(degree == required, 'polynomial degrees')
        prior.need(all(F(v)>0 for v in table.values()), 'nonpositive coefficient')
        result[name+'_degree'] = degree
        result[name+'_bernstein'] = [[table[i,j] for j in range(degree[1]+1)]
                                    for i in range(degree[0]+1)]
    return result


if __name__ == '__main__':
    prior.need(not sys.argv[1:], 'usage: generate_boundary_certificate.py')
    print(json.dumps(generate(), indent=2, sort_keys=True))
