#!/usr/bin/env python3
"""Exact coverage and encoding controls for the seven-edge exclusion."""
from collections import Counter
from itertools import combinations, permutations, product
import json
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver
from seven_edge_sat import motifs, lex_chain
from verify import graph, hoffman_singleton_edges, check_girth_and_identities

HERE=Path(__file__).resolve().parent

def matchings(points):
    if not points:
        yield set();return
    a=points[0]
    for b in points[1:]:
        for rest in matchings([x for x in points if x not in (a,b)]):
            yield rest|{(a,b)}

def coverage():
    M={(2*i,2*i+1) for i in range(5)};counts=Counter()
    for K in matchings(list(range(10))):
        if M&K:continue
        adj=[set() for _ in range(10)]
        for a,b in M|K:adj[a].add(b);adj[b].add(a)
        todo=set(range(10));sizes=[]
        while todo:
            stack=[min(todo)];seen=set(stack)
            while stack:
                for y in adj[stack.pop()]-seen:seen.add(y);stack.append(y)
            todo-=seen;sizes.append(len(seen))
        counts[tuple(sorted(sizes))]+=1
    assert counts=={(10,):384,(4,6):160}
    result=[]
    for name,cycles in [('10',[[0,1,2,3,4]]),('46',[[0,1],[2,3,4]])]:
        K={tuple(sorted((2*i+1,2*j))) for cyc in cycles for i,j in zip(cyc,cyc[1:]+cyc[:1])}
        permutations_of_points=[]
        for perm in permutations(range(5)):
            for flips in product((0,1),repeat=5):
                p=tuple(2*perm[i]+(b^flips[i]) for i in range(5) for b in range(2))
                if {tuple(sorted((p[a],p[b]))) for a,b in K}==K:permutations_of_points.append(p)
        # Reconstruct every raw motif from the representatives, then compare
        # with direct enumeration before any symmetry quotient.
        covered=set()
        for rep in motifs(name):
            orbit={tuple(tuple(sorted(p[x] for x in s)) for s in rep) for p in permutations_of_points}
            assert not (covered&orbit)
            covered|=orbit
        raw=set()
        for I in combinations(range(10),3):
            if any(set(e)<=set(I) for e in M|K):continue
            remaining=sorted(set(range(10))-set(I)-{x^1 for x in I})
            assert len(remaining)==4
            for X in combinations(remaining,2):
                Y=tuple(x for x in remaining if x not in X)
                if X not in M|K and Y not in M|K:raw.add((I,X,Y))
        assert raw==covered
        result.append({'matching':name,'automorphisms':len(permutations_of_points),'raw_motifs':len(raw),'orbits':len(motifs(name))})
    assert [r['automorphisms'] for r in result]==[10,24]
    assert [r['orbits'] for r in result]==[16,9]
    return {'perfect_matchings':{'10':384,'46':160},'motifs':result,'cases':50}

def controls():
    for c in range(9):
        assert c*(c-1)//2-(3*c-6)==(c-3)*(c-4)//2>=0
        assert c*(c-1)//2-(c-1)==(c-1)*(c-2)//2>=0
    assert [m for m in range(14) if 3*m+max(0,2*m-13)<=22]==list(range(8))
    pool=IDPool();cnf=CNF();rows=[[pool.id() for _ in range(4)] for _ in range(2)]
    lex_chain(cnf,pool,rows)
    with Solver(name='g4',bootstrap_with=cnf) as sol:
        for a,b in product(range(16),repeat=2):
            bits=[[bool(x&(1<<(3-i))) for i in range(4)] for x in (a,b)]
            assumptions=[v if bit else -v for row,bs in zip(rows,bits) for v,bit in zip(row,bs)]
            assert sol.solve(assumptions=assumptions)==(a<=b)
    weights=[0,1,2,3]
    for bound in range(7):
        cnf=CardEnc.equals([i+1 for i,w in enumerate(weights) for _ in range(w)],bound=bound,top_id=4,encoding=EncType.seqcounter)
        with Solver(name='g4',bootstrap_with=cnf) as sol:
            for bits in product((False,True),repeat=4):
                assert sol.solve(assumptions=[i+1 if b else -i-1 for i,b in enumerate(bits)])==(sum(w*b for w,b in zip(weights,bits))==bound)
    fixture=json.loads((HERE/'lower_bound_54_185.json').read_text())
    graphs=[graph(50,hoffman_singleton_edges()),graph(fixture['n'],fixture['edges'])]
    for G in graphs:
        check_girth_and_identities(G)
        T={v for v in range(len(G)) if 1+sum(len(G[u]) for u in G[v])==len(G)}
        # Select a proper subset in the regular control to make nontrivial
        # outside vertices and incidence partitions.
        if len(T)==len(G):T=set(sorted(T)[:13])
        assert T
        S=[G[v]&T for v in range(len(G))]
        pairs=sum(len(S[v])*(len(S[v])-1)//2 for v in range(len(G)))
        assert pairs+sum(len(S[t]) for t in T)//2==len(T)*(len(T)-1)//2
        for v in set(range(len(G)))-T:
            occupied=S[v]|set().union(*(S[t] for t in S[v]))
            target=T-occupied;seen=set()
            for u in G[v]-T:
                assert not (seen&S[u]);seen|=S[u]
            assert seen==target
    return {'lex_assignments':256,'weighted_cardinality_assignments':112,'positive_graph_incidence_controls':2}

def main():
    print(json.dumps({'coverage':coverage(),'controls':controls()},sort_keys=True))

if __name__=='__main__':main()
