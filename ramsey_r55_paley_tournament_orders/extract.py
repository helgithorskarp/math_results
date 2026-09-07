#!/usr/bin/env python3
"""Return two physical forbidden five-sets from a Paley43 vertex order."""
import itertools as it
import json
import sys


def graph(order):
    if type(order) is not list or len(order)!=43 or any(type(x) is not int for x in order) or sorted(order)!=list(range(43)):
        raise ValueError('expected a permutation of 0..42')
    pos={v:i for i,v in enumerate(order)}
    Q={x*x%43 for x in range(1,43)}
    matrix=[[0]*43 for _ in range(43)]
    for u,v in it.combinations(range(43),2):
        matrix[u][v]=matrix[v][u]=int(((v-u)%43 in Q)==(pos[u]<pos[v]))
    return matrix


def extract(order):
    matrix=graph(order); root=order[0]; witnesses=[]
    for side in (1,0):
        vertices=[v for v in range(43) if v!=root and matrix[root][v]==side]
        found=None
        for c,k in ((side,4),(1-side,5)):
            for q in it.combinations(vertices,k):
                if all(matrix[u][v]==c for u,v in it.combinations(q,2)):
                    found={'vertices':sorted((*q,root)) if k==4 else list(q),'color':c}
                    break
            if found is not None: break
        if found is None: raise ValueError('the proved obstruction failed')
        witnesses.append(found)
    return {'root':root,'witnesses':witnesses}


if __name__=='__main__':
    with open(sys.argv[1],encoding='utf8') as f: order=json.load(f)
    print(json.dumps(extract(order),sort_keys=True,indent=2))
