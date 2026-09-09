"""Definition-level four-row covering census for small triangle hypergraphs."""
from itertools import combinations, product

def triangles(n, edges):
    edges={tuple(sorted(e)) for e in edges}
    return [sum(1<<v for v in t) for t in combinations(range(n),3)
            if all(tuple(e) in edges for e in combinations(t,2))]

def count(n, edges):
    ts=triangles(n,edges);full=(1<<n)-1
    free=[s for s in range(1<<n) if not any(s&t==t for t in ts)]
    return sum(a|b|c|d==full for a,b,c,d in product(free,repeat=4))

def columns(n, edges):
    ts=triangles(n,edges)
    return sum(not any(all(word[v] & bit for v in range(n) if t>>v&1)
                       for t in ts for bit in (1,2,4,8))
               for word in product(range(1,16),repeat=n))
