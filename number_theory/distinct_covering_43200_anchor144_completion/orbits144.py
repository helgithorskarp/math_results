"""Product subgroup for the prescribed22-class72:31,100:93,108:6 question.

Binary action fixes the full16 leaves4 and14, and all required lower leaves.
Ternary action exchanges only lower9 leaves2,5,8, preserving full27 leaf6.
The cofactor25 is fixed. No maximal stabilizer or completion claim is made.
"""
N, Q = 43200, 10800
BASE = (8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60,72,100,108)
PARENT = (0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13,33,29,31,93,6)
BINARY_PINS8 = frozenset((0,2,3,4,6,7))
BINARY_PINS16 = frozenset((4,14))
TERNARY_PINS9 = frozenset((0,1,3,4,6))
TERNARY_PINS27 = frozenset((6,))
GENERATORS = (('binary',3,1,5),) + tuple(
    ('binary',4,r,r+8) for r in range(8) if r not in (4,6)) + (
    ('ternary',2,2,5), ('ternary',2,2,8), ('ternary',2,5,8))


def change(leaf, prime, k, u, v):
    if (prime not in (2,3) or k not in ((3,4) if prime==2 else (2,))
            or type(u) is not int or type(v) is not int
            or not 0 <= u < prime**k or not 0 <= v < prime**k
            or u % (prime**(k-1)) != v % (prime**(k-1))):
        raise ValueError('A same-root digit swap at one declared level')
    return leaf+v-u if leaf % (prime**k)==u else leaf+u-v if leaf % (prime**k)==v else leaf


def physical(period, x, family, k, u, v):
    if period not in (N,Q) or type(x) is not int or not 0 <= x < period:
        raise ValueError('A physical point in a declared period')
    if family == 'binary':
        axis = 64 if period==N else 16
        leaf = change(x%axis, 2, k, u, v)
    elif family == 'ternary':
        axis = 27
        leaf = change(x%axis, 3, k, u, v)
    else:
        raise ValueError('A declared prime coordinate')
    cofactor = period//axis
    return (x%cofactor+cofactor*((leaf-x%cofactor)*pow(cofactor,-1,axis)%axis))%period


def representative(a):
    if type(a) is not int or not 0 <= a < 144:
        raise ValueError('A raw144 phase')
    leaf = a%16
    if leaf%8 == 5:
        leaf -= 4
    if leaf%8 not in (4,6):
        leaf %= 8
    ternary = 2 if a%9 in (2,5,8) else a%9
    return (leaf+16*((ternary-leaf)*pow(16,-1,9)%9))%144


def transport(period, x, a):
    r = representative(a)
    y = x
    leaf = a%16
    if a%8 != r%8:
        y = physical(period,y,'binary',3,a%8,r%8)
        leaf += r%8-a%8
    if leaf != r%16:
        y = physical(period,y,'binary',4,leaf,r%16)
    if a%9 != r%9:
        y = physical(period,y,'ternary',2,a%9,r%9)
    return y


REPRESENTATIVES = tuple(sorted({representative(a) for a in range(144)}))
