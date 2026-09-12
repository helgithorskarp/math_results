"""Complete 60-variable extensions for the sharp (5,4;2K4) lemma.

True is red. Vertices 0..3 are a red K4; 4..18 induce a fixed R(4,4)
core. No symmetry breaking, auxiliary variables, or degree assumptions.
"""
from itertools import combinations
from pathlib import Path
import hashlib

CATALOG_SHA256 = '53a46ba21cb16805eb07775b60746f783864388538368955e72cbdae5ae8f4e1'
CATALOG_URL = 'https://users.cecs.anu.edu.au/~bdm/data/r44_15.g6'


def graph6(raw):
    raw = raw.strip()
    n = raw[0]-63
    if not 1 <= n <= 62 or len(raw) != 1+(n*(n-1)//2+5)//6:
        raise ValueError('graph6 shape')
    if any(not 63 <= x <= 126 for x in raw):
        raise ValueError('graph6 character')
    bits = ''.join(format(x-63, '06b') for x in raw[1:])
    if any(x != '0' for x in bits[n*(n-1)//2:]):
        raise ValueError('graph6 padding')
    a = [[0]*n for _ in range(n)]
    for bit, (u,v) in zip(bits, ((u,v) for v in range(1,n) for u in range(v))):
        a[u][v] = a[v][u] = int(bit)
    return a


def cores(path):
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise ValueError('catalogue hash')
    records = raw.splitlines()
    if len(records) != 640 or len(set(records)) != 640:
        raise ValueError('catalogue records')
    for row in records:
        a = graph6(row)
        if len(a) != 15 or any(len({a[u][v] for u,v in combinations(S,2)}) == 1
                              for S in combinations(range(15),4)):
            raise ValueError('catalogue membership')
    return records


def canonical(clauses):
    return sorted({tuple(sorted(set(c))) for c in clauses}, key=lambda c:(len(c),c))


def formula(a, forbid_five=True, forbid_pair=True):
    n = len(a)
    def x(w,v):
        return 1+n*w+v
    clauses = []
    if forbid_five:
        # Every mixed red five has k core vertices, 1 <= k <= 4.
        for k in range(1,5):
            for T in combinations(range(n),k):
                if all(a[u][v] for u,v in combinations(T,2)):
                    for S in combinations(range(4),5-k):
                        clauses.append([-x(w,v) for w in S for v in T])
    # A blue four uses exactly one block vertex: the core is R(4,4).
    for T in combinations(range(n),3):
        if all(not a[u][v] for u,v in combinations(T,2)):
            for w in range(4):
                clauses.append([x(w,v) for v in T])
    if not forbid_pair:
        return canonical(clauses)
    possible = []
    for k in range(1,4):
        for S in combinations(range(4),k):
            for T in combinations(range(n),4-k):
                if all(a[u][v] for u,v in combinations(T,2)):
                    mask = sum(1<<w for w in S)+sum(1<<(4+v) for v in T)
                    possible.append((mask,[-x(w,v) for w in S for v in T]))
    for (s,c),(t,d) in combinations(possible,2):
        if not s&t:
            clauses.append(c+d)
    return canonical(clauses)


def dimacs(n, clauses):
    return (f'p cnf {4*n} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
