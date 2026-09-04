#!/usr/bin/env python3
"""Build the normalized cyclic matching-cover CNF (not the full 43-vertex graph).

Blue means matching edges; each fiber is an independent blue triple.
One-hot variables encode the 15 free Z/3 shifts. Anchor shifts are zero.
"""
from itertools import combinations
import sys
PAIRS=list(combinations(range(1,7),2))
def var(i,j,d):return 1+3*PAIRS.index((i,j))+d
# TRUE means blue edge; red edges are complements.
T=46

def edge(u,v):
 i,a=divmod(u,3);j,b=divmod(v,3)
 if i==j:return 0
 if i==0:return T if a==b else 0
 return var(i,j,(b-a)%3)
clauses=set()
for i,j in PAIRS:
 vs=[var(i,j,d) for d in range(3)]
 clauses.add(tuple(vs))
 for a,b in combinations(vs,2):clauses.add((-a,-b))
base=len(clauses)
for vs in combinations(range(21),5):
 es={edge(u,v) for u,v in combinations(vs,2)}
 if 0 not in es:clauses.add(tuple(sorted(-e for e in es if e!=T)))
 if T not in es:clauses.add(tuple(sorted(e for e in es if e!=0)))
clauses={tuple(sorted(c)) for c in clauses}
cs=sorted(clauses,key=lambda c:(len(c),c))
sys.stdout.write(f'p cnf 45 {len(cs)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in cs))
