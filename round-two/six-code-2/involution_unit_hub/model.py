"""Primary integer-mask model for the matched unit-hub construction family."""
from collections import deque
from itertools import combinations
from pathlib import Path
import json
import time

TAILS = ((2,4,6),(3,5,7),(8,10,12),(9,11,13))
ROOTS = ((2,14,15,16),(2,5,14,15),(2,8,14,15))
FIXED = tuple(sum(1 << v for v in (0,1)+t) for t in TAILS)

def mask(points):
    return sum(1 << v for v in points)

def points(b):
    return tuple(v for v in range(18) if b >> v & 1)

def flip(b):
    return ((b & 0x15555) << 1) | ((b & 0x2aaaa) >> 1)

def build_local():
    qs = [mask(q) for q in combinations(range(2,18),4)
          if (mask(q) & flip(mask(q))).bit_count() <= 2
          and all((mask(q) & mask(t)).bit_count() <= 1 for t in TAILS)]
    raw = [sum(1 << j for j,b in enumerate(qs)
               if i != j and (a & b).bit_count() <= 1
               and (a & flip(b)).bit_count() <= 2)
           for i,a in enumerate(qs)]
    order = sorted(range(len(qs)),key=lambda i:(raw[i].bit_count(),i))
    inverse = {v:i for i,v in enumerate(order)}
    adjacency = [sum(1 << inverse[j] for j in bits(raw[i])) for i in order]
    return [qs[i] for i in order], adjacency

def bits(pool):
    while pool:
        v = (pool & -pool).bit_length()-1
        yield v
        pool &= pool-1

def write_graph(path, adjacency, qs=None):
    with Path(path).open('w') as f:
        f.write(str(len(adjacency))+'\n')
        for i,a in enumerate(adjacency):
            row = ([qs[i]] if qs is not None else [])+[a.bit_count()]+list(bits(a))
            f.write(' '.join(map(str,row))+'\n')

def generators():
    result = []
    for a,b in [(1,2),(2,3),(4,5),(5,6),(7,8)]:
        p = list(range(18))
        for k in range(2):
            p[2*a+k],p[2*b+k] = p[2*b+k],p[2*a+k]
        result.append(tuple(p))
    p = list(range(18))
    for a,b in [(1,4),(2,5),(3,6)]:
        for k in range(2):
            p[2*a+k],p[2*b+k] = p[2*b+k],p[2*a+k]
    result.append(tuple(p))
    for subset in [(1,2,3),(4,5,6),(7,),(8,)]:
        p = list(range(18))
        for a in subset:
            p[2*a],p[2*a+1] = p[2*a+1],p[2*a]
        result.append(tuple(p))
    return result

def transform(b, p):
    return mask(p[v] for v in points(b))

def classify(qs, adjacency, cases):
    index = {q:i for i,q in enumerate(qs)}
    gs = generators()
    for p in gs:
        if sorted(p) != list(range(18)) or any(p[v^1] != (p[v]^1) for v in range(18)):
            raise ValueError('invalid actual permutation')
        if {transform(b,p) for b in FIXED} != set(FIXED):
            raise ValueError('fixed words not preserved')
    maps = [tuple(index[transform(q,p)] for q in qs) for p in gs]
    for g in maps:
        for i,a in enumerate(adjacency):
            if sum(1 << g[j] for j in bits(a)) != adjacency[g[i]]:
                raise ValueError('graph not preserved')
    identity = tuple(range(18))
    group = {identity}
    queue = deque([identity])
    while queue:
        p = queue.popleft()
        for g in gs:
            image = tuple(g[p[v]] for v in range(18))
            if image not in group:
                group.add(image)
                queue.append(image)
    all_covers = {tuple(s) for ss in cases for s in ss}
    remaining = set(all_covers)
    classes = []
    while remaining:
        seed = min(remaining)
        orbit = {seed}
        queue = deque([seed])
        while queue:
            solution = queue.popleft()
            for g in maps:
                image = tuple(sorted(g[v] for v in solution))
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        hits = all_covers & orbit
        if not hits:
            raise ValueError('missing root coverage')
        remaining -= hits
        classes.append({'representative': list(min(orbit)),
                        'orbit_size':len(orbit),
                        'root_hits':[sum(tuple(s) in orbit for s in ss) for ss in cases]})
    classes.sort(key=lambda c:c['representative'])
    return len(group), classes, sorted(group)

def anchor(qs, solution):
    private = [qs[i] | 1 for i in solution]
    words = sorted(set(FIXED) | set(private) | {flip(b) for b in private})
    if len(words)!=36 or any((a&b).bit_count()>2 for a,b in combinations(words,2)):
        raise ValueError('invalid restored two-star anchor')
    return words

def residual(words):
    rows = []
    for t in combinations(range(2,18),5):
        b = mask(t)
        if points(b)>=points(flip(b)) or (b & flip(b)).bit_count()>2:
            continue
        if all((b&w).bit_count()<=2 for w in words):
            rows.append(b)
    adjacency = [sum(1 << j for j,c in enumerate(rows)
                     if i!=j and (b&c).bit_count()<=2 and (b&flip(c)).bit_count()<=2)
                 for i,b in enumerate(rows)]
    return rows, adjacency

def maximum_cliques(adjacency):
    best = []
    maxima = []
    nodes = 0
    started = time.monotonic()
    def colors(pool):
        ordered,bounds = [],[]
        color = 0
        while pool:
            color += 1
            available = pool
            while available:
                bit = available & -available
                v = bit.bit_length()-1
                ordered.append(v)
                bounds.append(color)
                pool ^= bit
                available &= ~bit & ~adjacency[v]
        return ordered,bounds
    def search(pool,chosen):
        nonlocal nodes
        nodes += 1
        if nodes>3000000 or time.monotonic()-started>30:
            raise TimeoutError('INCOMPLETE')
        if not pool:
            if len(chosen)>len(best):
                best[:] = chosen
                maxima[:] = [tuple(sorted(chosen))]
            elif len(chosen)==len(best):
                maxima.append(tuple(sorted(chosen)))
            return
        ordered,bounds = colors(pool)
        for j in range(len(ordered)-1,-1,-1):
            if len(chosen)+bounds[j]<len(best):
                return
            v = ordered[j]
            search(pool & adjacency[v], chosen+[v])
            pool &= ~(1 << v)
    search((1 << len(adjacency))-1,[])
    if len(set(maxima))!=len(maxima):
        raise ValueError('duplicate maximum cliques')
    return len(best), sorted(maxima), nodes
