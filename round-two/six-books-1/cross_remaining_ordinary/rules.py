"""Separate coordinate model and the displayed ordinary set calculations."""
from itertools import combinations

CYCLE = ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
P,S,H,K,C,L = 13,50,43,23,3,60
OWN = (40,20)
PATH_A = ((0,4),(4,3),(1,2),(2,5))
PATH_D = ((0,5),(5,2),(1,3),(3,4))

def covers(w):
    return all((w>>i&1) or (w>>j&1) for i,j in CYCLE)

def independent(w, edges=CYCLE):
    return all(not ((w>>i&1) and (w>>j&1)) for i,j in edges)

def build(r, rows, sy):
    red = [0]*16
    def e(i,j):
        red[i] |= 1<<j
        red[j] |= 1<<i
    for j in (1,2,*range(3,11)):
        e(0,j)
    for j in (2,11,12):
        e(1,j)
    for j in range(9,16):
        e(2,j)
    for i,j in CYCLE:
        e(i+3,j+3)
    for j,w in enumerate(OWN):
        for i in range(6):
            if w>>i&1:
                e(j+9,i+3)
    for j,w in enumerate((6,5) if r==0 else (5,6)):
        for k in range(3):
            if w>>k&1:
                e(j+9,k+13)
    for j,w in enumerate((6,3)):
        for k in range(3):
            if w>>k&1:
                e(j+11,k+13)
    for j,w in enumerate((*sy,*rows)):
        for i in range(6):
            if w>>i&1:
                e(j+11,i+3)
    degrees = (10,10,9,*([10]*8),6+sy[0].bit_count(),
               6+sy[1].bit_count(),6+rows[0].bit_count(),
               6+rows[1].bit_count(),7+rows[2].bit_count())
    qr = tuple(degrees[i]-red[i].bit_count() for i in range(16))
    return tuple(red),degrees,qr

def allowances(red, d):
    result = {}
    for i,j in combinations(range(16),2):
        b = (3 if red[i]>>j&1 else d[i]+d[j]-14)
        b -= (red[i]&red[j]).bit_count()
        result[i,j] = result[j,i] = b
    return result

def permutation(which):
    p = list(range(16))
    if which=='phi':
        pairs = ((0,1),(2,4),(3,5))
    elif which=='psi':
        pairs = ((2,3),(4,5))
        p[9],p[10] = 10,9
    else:
        raise ValueError('explicit phi or psi')
    for i,j in pairs:
        p[3+i],p[3+j] = 3+j,3+i
    return tuple(p)

def row_transport(w,p):
    return sum(1<<(p[i+3]-3) for i in range(6) if w>>i&1)
