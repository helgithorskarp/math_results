"""Declared pinned-digit action at missing72, with higher digits fixed.

Pure exact formulas; no solver or private forest imported. This applies the
published pinned-digit lemma, without claiming a maximal stabilizer.
"""
from itertools import combinations

N, Q = 43200, 10800
BASE = (8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60)
COMMON = (0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13)
PARENTS = tuple(COMMON + tail for tail in ((6,29),(33,29),(33,59)))
BINARY_PINS = frozenset((0,2,3,4,6))
TERNARY_PINS = frozenset((0,1,3,6))
GENERATORS = ((2,3,1,5),(3,2,4,7),(3,2,2,5),(3,2,2,8),(3,2,5,8))


def digit_swap(leaf, p, k, u, v):
    power = p**k
    if u == v:
        return leaf
    if (not 0 <= u < power or not 0 <= v < power
            or u % (power//p) != v % (power//p)):
        raise ValueError('Swap two kth-digit leaves under the same root')
    return leaf + v-u if leaf%power == u else leaf+u-v if leaf%power == v else leaf


def physical(period, x, p, k, u, v):
    if period not in (N,Q):
        raise ValueError('Use one of the two declared periods')
    power = 1
    while period % (power*p) == 0:
        power *= p
    cofactor = period//power
    leaf = digit_swap(x%power,p,k,u,v)
    return (x%cofactor + cofactor*((leaf-x%cofactor)*pow(cofactor,-1,power)%power))%period


def target_leaf(leaf,p,k,pins):
    if leaf in pins:
        return leaf
    root = leaf % (p**(k-1))
    return min(root + p**(k-1)*j for j in range(p) if root+p**(k-1)*j not in pins)


def representative(a):
    if type(a) is not int or not 0 <= a < 72:
        raise ValueError('Raw phase modulo72 required')
    binary = target_leaf(a%8,2,3,BINARY_PINS)
    ternary = target_leaf(a%9,3,2,TERNARY_PINS)
    return (binary+8*((ternary-binary)*pow(8,-1,9)%9))%72


def transport(period,x,a):
    r = representative(a)
    y = physical(period,x,2,3,a%8,r%8)
    return physical(period,y,3,2,a%9,r%9)


REPRESENTATIVES = tuple(sorted({representative(a) for a in range(72)}))
