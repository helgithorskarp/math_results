"""Exact geometry and the necessary reconstruction system at 72 points."""
from collections import Counter, deque
from itertools import permutations, product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent))
from projective import points, lines, hyperplanes, normalize

P = points(4)
LINES = lines(4)
PLANES = hyperplanes(4)
PLANE_SETS = tuple(frozenset(h) for h in PLANES)

def matrix_arc(path):
    data = json.loads(path.read_text())
    rows = data['rows']
    assert len(rows) == 4 and len({len(r) for r in rows}) == 1
    c = Counter(normalize(tuple(map(int, col))) for col in zip(*rows))
    return tuple(c[p] for p in P)

def base23():
    return tuple(json.loads((ROOT/'base23.json').read_text())['multiplicities'])

def lift(base):
    weights = dict(zip(points(3), base))
    return tuple(weights[normalize(p[:3])] if any(p[:3]) else 3 for p in P)

def arcs():
    p3 = points(3)
    conic = {i for i,p in enumerate(p3) if (p[0]*p[2]-p[1]*p[1]) % 5 == 0}
    tangents = [h for h in hyperplanes(3) if len(set(h)&conic) == 1]
    b28 = tuple(3 if i in conic else int(not any(i in h for h in tangents))
                for i in range(31))
    return {'E128': matrix_arc(ROOT.parent/'exceptional128.json'),
            'E143': matrix_arc(ROOT/'exceptional143.json'),
            'L23': lift(base23()), 'L28': lift(b28)}

def parameters(K):
    lam = Counter(K)
    size = sum(K)
    assert (218-size) % 5 == 0
    L = (218-size)//5
    B = sum((16-i)*(15-i)//2*(lam[i]-(i==0)) for i in range(4))
    assert (B-15768) % 5 == 0
    return L, 13*L-(B-15768)//5

def flags(K):
    hw = tuple(sum(K[i] for i in h) for h in PLANES)
    return tuple((q,f) for q in range(156) if K[q]==0
                 for f,h in enumerate(PLANES) if q in h and hw[f]==18)

def slots(K, q, f):
    assert (q,f) in flags(K)
    assert all(sum(K[i] for i in l) in (3,8) for l in LINES if q in l)
    return tuple(tuple(i for i in l if i!=q) for l in LINES
                 if q in l and sum(K[i] for i in l)==3
                 and not set(l)<=PLANE_SETS[f])

def reconstruction_rows(K, q, f):
    """(plane index, allowed D-intersection sizes), necessary for A=S+P."""
    for r,h in enumerate(PLANES):
        w = sum(K[i] for i in h)
        assert w % 5 == 3
        if q in h:
            yield r, ((43-w)//5 - 5*int(r==f),)
        else:
            yield r, ((58-w)//5, (33-w)//5)

def apply_matrix(M,p):
    return normalize(tuple(sum(x*y for x,y in zip(row,p))%5 for row in M))

def lift23_cover(K):
    """A verified subgroup action; no claim to the full automorphism group."""
    p3 = points(3); ix3 = {p:i for i,p in enumerate(p3)}; b = base23()
    base_matrices = []
    for perm in permutations(range(3)):
        for x,y in product(range(1,5), repeat=2):
            M = [[0]*3 for _ in range(3)]
            for j,c in enumerate((1,x,y)): M[perm[j]][j] = c
            if all(b[ix3[apply_matrix(M,p)]]==k for p,k in zip(p3,b)):
                base_matrices.append(M)
    matrices = [[[ *row, 0] for row in M]+[[0,0,0,1]] for M in base_matrices]
    for j in range(3):
        M = [[int(i==k) for k in range(4)] for i in range(4)]
        M[3][j] = 1
        matrices.append(M)
    matrices.append([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,2]])
    ix = {p:i for i,p in enumerate(P)}; hi = {h:i for i,h in enumerate(PLANE_SETS)}
    actions = []
    for M in matrices:
        pp = tuple(ix[apply_matrix(M,p)] for p in P)
        assert len(set(pp))==156 and all(K[i]==K[j] for i,j in enumerate(pp))
        hp = tuple(hi[frozenset(pp[i] for i in h)] for h in PLANES)
        actions.append((pp,hp))
    all_flags = set(flags(K)); remaining = set(all_flags); orbits = []
    while remaining:
        rep = min(remaining); seen = {rep}; queue = deque([rep])
        while queue:
            q,f = queue.popleft()
            for pp,hp in actions:
                nxt = pp[q],hp[f]
                assert nxt in all_flags
                if nxt not in seen: seen.add(nxt); queue.append(nxt)
        assert seen<=remaining
        remaining -= seen
        orbits.append({'representative': list(rep), 'flags': sorted(seen)})
    return matrices, orbits
