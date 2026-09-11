from itertools import product,combinations
from functools import lru_cache

def normalize(p):
    inv=pow(next(x for x in p if x),-1,5)
    return tuple(x*inv%5 for x in p)

@lru_cache(None)
def points(n):
    return tuple(p for p in product(range(5),repeat=n) if any(p) and next(x for x in p if x)==1)

@lru_cache(None)
def lines(n):
    pts=points(n); index={p:i for i,p in enumerate(pts)}; result=set()
    for a,b in combinations(pts,2):
        line={index[b]}
        for t in range(5):line.add(index[normalize(tuple((x+t*y)%5 for x,y in zip(a,b)))])
        result.add(tuple(sorted(line)))
    return tuple(sorted(result))

@lru_cache(None)
def hyperplanes(n):
    pts=points(n)
    return tuple(tuple(i for i,p in enumerate(pts) if sum(x*y for x,y in zip(p,h))%5==0) for h in pts)
