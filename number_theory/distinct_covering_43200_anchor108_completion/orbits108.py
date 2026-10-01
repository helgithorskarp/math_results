"""Two-level pinned ternary action for the saved21-class100:43/93 questions.

Pure exact formulas applying the credited pinned-digit lemma. The declared
subgroup fixes the cofactor1600, and is not asserted to be the full stabilizer.
"""
from itertools import combinations

N,Q=43200,10800
BASE=(8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72,100)
COMMON=(0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13,33,29,6)
PARENTS=tuple(COMMON+(a,) for a in (43,93))
PINS9=frozenset((0,1,3,6));PINS27=frozenset((6,))
GENERATORS=((2,4,7),(2,2,5),(2,2,8),(2,5,8))+tuple(
    (3,u,v) for root in range(9)
    for u,v in combinations([root+9*j for j in range(3) if root+9*j not in PINS27],2))


def digit_swap(leaf,k,u,v):
    if (k not in (2,3) or type(u) is not int or type(v) is not int
            or not 0<=u<3**k or not 0<=v<3**k or u%(3**(k-1))!=v%(3**(k-1))):
        raise ValueError('Two same-root ternary leaves at level2 or3')
    if u==v:return leaf
    return leaf+v-u if leaf%(3**k)==u else leaf+u-v if leaf%(3**k)==v else leaf


def physical(period,x,k,u,v):
    if period not in (N,Q) or type(x) is not int or not 0<=x<period:
        raise ValueError('A physical point in one of the two declared periods')
    H=period//27;leaf=digit_swap(x%27,k,u,v)
    return (x%H+H*((leaf-x%H)*pow(H,-1,27)%27))%period


def representative(a):
    if type(a) is not int or not 0<=a<108:raise ValueError('A raw108 phase')
    leaf=a%27;lower=leaf%9
    target=lower if lower in PINS9 else min(lower%3+3*j for j in range(3)
                                           if lower%3+3*j not in PINS9)
    leaf+=target-lower
    targetleaf=leaf if leaf in PINS27 else min(target+9*j for j in range(3)
                                              if target+9*j not in PINS27)
    return (a%4+4*((targetleaf-a%4)*pow(4,-1,27)%27))%108


def transport(period,x,a):
    r=representative(a)
    y=physical(period,x,2,a%9,r%9)
    leaf=(a%27)+(r%9-a%9)
    return physical(period,y,3,leaf,r%27)


REPRESENTATIVES=tuple(sorted({representative(a) for a in range(108)}))
