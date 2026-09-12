#!/usr/bin/env python3
"""Validate only the physical graph in a SAT witness, from definitions."""
import argparse,itertools,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('solver_log',type=Path);a=p.parse_args()
n=43;pairs=list(itertools.combinations(range(n),2));assignment={}
for line in a.solver_log.read_text().splitlines():
    if not line.startswith('v '):continue
    for x in map(int,line.split()[1:]):
        if 1<=abs(x)<=len(pairs):
            assert abs(x) not in assignment or assignment[abs(x)]==(x>0)
            assignment[abs(x)]=x>0
assert len(assignment)==len(pairs),'Incomplete physical assignment'
edges={e for i,e in enumerate(pairs,1) if assignment[i]};universe=set(range(n))
neighbors=[{v for v in range(n) if u!=v and tuple(sorted((u,v))) in edges} for u in range(n)]
for s in itertools.combinations(range(n),5):
    colors={e in edges for e in itertools.combinations(s,2)}
    assert len(colors)==2,('Monochromatic five-set',s,colors)
for graph in [neighbors,[universe-neighbors[u]-{u} for u in range(n)]]:
    for s in itertools.combinations(range(n),3):
        covered=set(s)
        for u in s:covered.update(graph[u])
        assert covered!=universe,('Dominating triple',s)
print(json.dumps({'n':n,'edges':len(edges),'every_five_set_bichromatic':True,'no_dominating_triple_in_either_color':True,'physical_edges':sorted(edges)},indent=2))
