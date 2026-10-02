"""Literal old-label shell and physical red/blue spine counts.

No prescribed Q rows, census, certificate, or external file is an input.
"""
from itertools import combinations

OLD = ((1,8,9),(0,),(6,7),(4,5),(3,7,9),(3,6,8),
       (2,5,9),(2,4,8),(0,5,7),(0,4,6))
OLD_MAP = (2,1,3,4,5,6,7,8,9,10)
LABELS = ('u','v','a',*(f'X{i}' for i in range(6)),
          'SX0','SX1','SY0','SY1','T0','T1','T2')

def build(r, rows, sy, old_map=OLD_MAP):
    if r not in (0,1) or len(rows)!=3 or len(sy)!=2:
        raise ValueError('two actual r labels, three T and two SY rows')
    if any(not isinstance(w,int) or not 0<=w<64 for w in (*rows,*sy)):
        raise ValueError('six-bit row domain')
    if tuple(old_map)!=OLD_MAP:
        raise ValueError('literal old-label/coordinate bridge changed')
    red = [set() for _ in range(16)]
    def edge(i,j):
        red[i].add(j)
        red[j].add(i)
    for i in range(10):
        edge(0,old_map[i])
        for j in OLD[i]:
            if i<j:
                edge(old_map[i],old_map[j])
    if sum(len(red[i]&set(range(1,11))) for i in range(1,11))!=26:
        raise ValueError('thirteen literal neighborhood edges')
    for j in (11,12):
        edge(1,j)
    for j in range(11,16):
        edge(2,j)
    sx = ((14,15),(13,15)) if r==0 else ((13,15),(14,15))
    for i,row in zip((9,10),sx):
        for j in row:
            edge(i,j)
    for i,row in ((11,(14,15)),(12,(13,14))):
        for j in row:
            edge(i,j)
    for z,w in zip((11,12,13,14,15),(*sy,*rows)):
        for i in range(6):
            if w>>i&1:
                edge(z,3+i)
    degrees = [10,10,9]+[10]*8
    qr = [degrees[i]-len(red[i]) for i in range(11)]
    for i in range(11,16):
        qi = 4-len(red[i]&set(range(11,16)))
        qr.append(qi)
        degrees.append(len(red[i])+qi)
    if any(not 0<=q<=6 for q in qr):
        raise ValueError('rank outside six-point Q')
    return tuple(frozenset(s) for s in red),tuple(degrees),tuple(qr)

def allowances(red, degrees):
    """Derive Q-intersection caps from physical colored-spine page counts.

    On a blue pair, known common blue pages plus 6-qi-qj+|Qi cap Qj|
    give the same allowance as the equivalent red-codegree expression.
    """
    known = frozenset(range(16))
    result = {}
    for i,j in combinations(range(16),2):
        if j in red[i]:
            b = 3-len(red[i]&red[j])
        else:
            blue = len((known-red[i]-{i})&(known-red[j]-{j}))
            qi = degrees[i]-len(red[i])
            qj = degrees[j]-len(red[j])
            b = qi+qj-blue
        result[i,j] = result[j,i] = b
    return result
