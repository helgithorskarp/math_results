#!/usr/bin/env python3
"""Definition-level positive tests and the forced-half-cell identities."""
from itertools import combinations
import verify_certificate as v

def graph(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges: adj[a].add(b);adj[b].add(a)
    return adj

def has_clique(adj,vertices,size,red=True):
    return any(all((b in adj[a])==red for a,b in combinations(q,2))
               for q in combinations(vertices,size))

def audit_partition(adj,k):
    n=len(adj);near=[s&set(range(k)) for s in adj[:k]]
    counts={}
    for z in range(k,n):
        x=sum(1<<i for i in range(k) if i in adj[z])
        counts[x]=counts.get(x,0)+1
    tested=0
    for a,b,cap in v.all_roots(near):
        A=v.vertices(a,k);B=v.vertices(b,k)
        # Directly test every actual vertex, without signature/set-intersection logic.
        common=[z for z in range(n) if z not in A|B
                and all(i in adj[z] for i in A) and all(i not in adj[z] for i in B)]
        fixed=sum(z<k for z in common)
        mass=sum(value for x,value in counts.items() if x&a==a and not x&b)
        v.require(mass+fixed==len(common),'literal common-set partition')
        v.require(not has_clique(adj,common,5-len(A)),'red extension rule')
        v.require(not has_clique(adj,common,5-len(B),False),'blue extension rule')
        v.require(mass<=cap,'valid graph rejected by root union')
        tested+=1
    return tested

def sharp_fixture(red_size,blue_size,cell_edges,cell_n):
    k=red_size+blue_size;n=k+cell_n
    edges=list(combinations(range(red_size),2))
    edges += [(a,k+b) for a in range(red_size) for b in range(cell_n)]
    edges += [(k+a,k+b) for a,b in cell_edges]
    adj=graph(n,edges)
    v.require(not has_clique(adj,range(n),5) and not has_clique(adj,range(n),5,False),'positive Ramsey fixture')
    # Move one cell vertex into the exceptional core: its contribution must be subtracted.
    audit_partition(adj,k+1)
    near=[s&set(range(k+1)) for s in adj[:k+1]]
    a=(1<<red_size)-1;b=((1<<blue_size)-1)<<red_size
    v.require(v.root_bound(a,b,near)==cell_n-1,'sharp fixture core subtraction')
    return n

def gap_identities():
    # Degree labels (19,20,20,20,20,22), core K_{3,3} plus edge 1--5.
    A=(0,1,5);B=(2,3,4)
    near=graph(6,[(a,b) for a in A for b in B]+[(1,5)])
    demands=[37]+[d-len(s) for d,s in zip((19,20,20,20,20,22),near)]
    v.require(demands==[37,16,16,17,17,17,18],'gap degree demands')
    lam=(6,-3,0,-2,-2,-2,0)
    v.require(sum(x*y for x,y in zip(lam,demands))==72,'gap equality value')
    common=((0,33,2),(1,12,1),(1,20,1),(1,24,1),(2,33,2))
    v.require(sum(w*v.root_bound(a,b,near) for a,b,w in common)==63,'gap common bound')
    v.require(all(v.root_bound(a,1,near)==3 for a in (38,42,50)),'gap triangle bounds')
    tested=0
    for x in range(64):
        S=v.vertices(x,6);T=set(range(6))-S
        if -2*(0 in S)-len(S&{1,2,3,4})+int(5 in S)>-2: continue
        if has_clique(near,S,4) or has_clique(near,T,4,False): continue
        tested+=1
        L=6-3*int(0 in S)-2*len(S&set(B))
        C=sum(w for a,b,w in common if x&a==a and not x&b)
        tri=lambda a: int(x&a==a and not x&1)
        v.require(L<=C+2*tri(50)+2*int(x==46),'pointwise lower-half identity')
        v.require(L<=C+2*tri(38)+2*tri(42)-2*int(x==46),'pointwise upper-half identity')
    v.require(tested==47,'gap signature coverage')
    # Summing gives 72 <= 63+6+2*y_46 and 72 <= 63+12-2*y_46.
    v.require(72-(63+6)==3 and (63+12)-72==3,'forced twice-cell-count equals three')
    return tested

def main():
    v.check_ramsey_table()
    tested=0
    pairs=list(combinations(range(5),2))
    for mask in range(1<<len(pairs)):
        adj=graph(5,[e for i,e in enumerate(pairs) if mask>>i&1])
        if has_clique(adj,range(5),5) or has_clique(adj,range(5),5,False): continue
        for k in (3,4,5): tested+=audit_partition(adj,k)
    cycle=[(i,(i+1)%5) for i in range(5)]
    wagner=[(i,(i+1)%8) for i in range(8)]+[(i,i+4) for i in range(4)]
    v.require(sharp_fixture(2,2,cycle,5)==9,'C5 fixture size')
    v.require(sharp_fixture(2,1,wagner,8)==11,'Wagner fixture size')
    print(f'PASS all 1022 labeled Ramsey graphs on five vertices, three partitions, {tested} root tests')
    print('PASS sharp 9-vertex and 11-vertex fixtures test union capacities and core subtraction')
    print(f'PASS {gap_identities()} literal signature checks force 2*y_46=3 in the integrality-gap core')
    print('SCOPE small validation fixtures, not 43-vertex target witnesses')

if __name__=='__main__': main()
