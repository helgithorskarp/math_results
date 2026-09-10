#!/usr/bin/env python3
"""Exact controls for boundary_sinks.md; Python standard library only."""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from verify import graph, require, hoffman_singleton_edges, check_girth_and_identities


def local_identity(G):
    d=list(map(len,G));w=[x-6 for x in d]
    s=[sum(w[u] for u in row) for row in G];S=sum(w)
    for v in range(len(G)):
        far=[u for u in range(len(G)) if u!=v and u not in G[v] and not (G[u]&G[v])]
        lhs=sum(s[u] for u in G[v])
        rhs=S-s[v]+(d[v]-1)*w[v]-sum(w[u] for u in far)
        require(lhs==rhs,"local weighted identity mismatch")


def rational_rank(matrix):
    A=[list(map(Fraction,row)) for row in matrix];r=0
    for j in range(len(A[0])):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r]
        pivot=A[r][j];A[r]=[x/pivot for x in A[r]]
        for k in range(r+1,len(A)):
            if A[k][j]:
                factor=A[k][j];A[k]=[a-factor*b for a,b in zip(A[k],A[r])]
        r+=1
    return r


def main():
    edges=hoffman_singleton_edges()
    for deleted in (set(),{(0,1)},{(0,1),(2,3)}):
        G=graph(50,sorted(edges-deleted));check_girth_and_identities(G);local_identity(G)
    data=json.loads((Path(__file__).parent/'lower_bound_54_185.json').read_text())
    G=graph(data['n'],data['edges']);check_girth_and_identities(G);local_identity(G)
    print('PASS: local weighted identity on four graph controls')
    require(50-7+6-2 < 7*7,'degree-seven exceptional contradiction')
    possible=[c for c in range(1,4) if c+2<=7-2*c]
    require(possible==[1] and 6*max(possible)<12,'degree-six exceptional contradiction')
    print('PASS: arithmetic in both exceptional-vertex exclusions')
    d=list(map(len,G));T=[v for v in range(len(G)) if d[v]==8 and sum(d[u] for u in G[v])==len(G)-1]
    require(T==[50,51,52,53],'sink control changed')
    require(all(v not in G[u] for u,v in combinations(T,2)),'sink control is not independent')
    P=[[len(G[u]&G[v])+(v in G[u])-7*(u==v) for v in range(54)] for u in range(54)]
    require(all(P[u][v]==1 for u in range(54) for v in T),'sink polynomial column identity')
    nullity=54-rational_rank(P)
    require(nullity==2*(len(T)-1)==6,'quadratic eigenspace rank control')
    print('PASS: four independent degree-eight sinks; exact polynomial nullity 6')


if __name__=='__main__':main()
