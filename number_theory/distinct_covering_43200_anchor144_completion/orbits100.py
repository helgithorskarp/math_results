"""Pinned quinary second-digit action at missing100; all other coordinates fixed.

This is an application of the credited pinned-digit lemma, not a claim about
the full stabilizer. Exact pure formulas; no solver or private forest imported.
"""
from itertools import combinations

N, Q = 43200, 10800
BASE = (8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72)
COMMON = (0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13,33,29)
PARENTS = tuple(COMMON + (a,) for a in (31,))
QUINARY_PINS = frozenset((3,8,13))
GENERATORS = tuple((u,v) for root in range(5)
                   for u,v in combinations([root+5*j for j in range(5)
                                             if root+5*j not in QUINARY_PINS],2))


def physical(period,x,u,v):
    if period not in (N,Q) or type(x) is not int or not 0 <= x < period:
        raise ValueError('A physical point in one of the two declared periods')
    if (type(u) is not int or type(v) is not int or not 0 <= u < 25
            or not 0 <= v < 25 or u%5 != v%5):
        raise ValueError('Swap two second-digit leaves under one quinary root')
    if u==v:return x
    H=period//25
    delta=H*((v-u)*pow(H,-1,25)%25)
    return (x+delta)%period if x%25==u else (x-delta)%period if x%25==v else x


def representative(a):
    if type(a) is not int or not 0 <= a < 100:
        raise ValueError('A raw phase modulo100')
    leaf=a%25
    target=leaf if leaf in QUINARY_PINS else min(leaf%5+5*j for j in range(5)
                                                if leaf%5+5*j not in QUINARY_PINS)
    return (a%4+4*((target-a%4)*pow(4,-1,25)%25))%100


def transport(period,x,a):
    return physical(period,x,a%25,representative(a)%25)


REPRESENTATIVES=tuple(sorted({representative(a) for a in range(100)}))
