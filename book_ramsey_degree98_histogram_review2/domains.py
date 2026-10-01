"""Complete cubic carriers, with literal graph coverage and no catalogue."""
from itertools import combinations, combinations_with_replacement
from collections import defaultdict
from incidence import need


def matrix(n, edges):
    a=[[0]*n for _ in range(n)]
    for u,v in edges:a[u][v]=a[v][u]=1
    need(all(sum(row)==3 for row in a),'noncubic domain graph')
    return a


def gram(a, degrees=None):
    n=len(a);common=[[sum(a[i][k]*a[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    if degrees is None:
        return [[5*(i==j)+3-a[i][j]-common[i][j] for j in range(n)] for i in range(n)]
    return [[degrees[i]-4 if i==j else (2 if a[i][j] else degrees[i]+degrees[j]-15)-common[i][j]
             for j in range(n)] for i in range(n)]


def tails(n, edge_count=None):
    pairs=tuple(combinations(range(n),2));bucket=defaultdict(list)
    choices=combinations(range(len(pairs)),edge_count) if edge_count is not None else (tuple(i for i in range(len(pairs)) if word>>i&1) for word in range(1<<len(pairs)))
    for indices in choices:
        edges=tuple(pairs[i] for i in indices);deg=[0]*n
        for u,v in edges:deg[u]+=1;deg[v]+=1
        bucket[tuple(deg)].append(edges)
    return bucket


def cubic10():
    bucket=tails(6);graphs=[];profiles=0
    inside=tuple(combinations((1,2,3),2))
    for iw in range(8):
        es=[p for i,p in enumerate(inside) if iw>>i&1]
        needrows=[2-sum(z in p for p in es) for z in (1,2,3)]
        for cols in combinations_with_replacement(range(8),6):
            if any(sum(c>>i&1 for c in cols)!=needrows[i] for i in range(3)):continue
            profiles+=1
            cross=[(1+i,4+j) for j,c in enumerate(cols) for i in range(3) if c>>i&1]
            residual=tuple(3-c.bit_count() for c in cols)
            for tail in bucket.get(residual,()):
                edges=tuple(sorted([(0,1),(0,2),(0,3)]+es+cross+[(4+u,4+v) for u,v in tail]))
                matrix(10,edges);graphs.append(edges)
    need(len(graphs)==len(set(graphs)),'duplicate cubic10 input')
    return tuple(sorted(graphs)),profiles


def marked_cubic8():
    bucket=tails(5,4);graphs=[]
    for b in combinations(range(5),2):
        for c in combinations(range(5),2):
            for z in combinations(range(5),3):
                residual=tuple(3-(i in b)-(i in c)-(i in z) for i in range(5))
                for tail in bucket.get(residual,()):
                    es=[(0,1)]+[(0,3+i) for i in b]+[(1,3+i) for i in c]+[(2,3+i) for i in z]+[(3+u,3+v) for u,v in tail]
                    edges=tuple(sorted(es));matrix(8,edges);graphs.append(edges)
    need(len(graphs)==len(set(graphs)),'duplicate marked cubic8 input')
    return tuple(sorted(graphs))
