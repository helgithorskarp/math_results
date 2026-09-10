"""Exhaustive small-instance test of the canonical-anchor reduction."""
from encode import build_case,decode
from orbits import sidon,orbit_catalog
from itertools import combinations
from pysat.solvers import Solver
from pathlib import Path
import json
n=14;sizes=[5,5,4]
rows=[list(r) for r in combinations(range(n),5) if sidon(r)]
ordered=orbit_catalog(rows,[1]*n);rank={tuple(r):i//2 for i,r in enumerate(ordered)}
partitions=[]
for a,b in combinations(rows,2):
    if set(a)&set(b):continue
    small=sorted(set(range(n))-set(a)-set(b))
    if sidon(small):partitions.append([a,b,small])
assert partitions
checks=0;rejected=0;covered=set()
for j in range(len(ordered)//2):
    anchor=ordered[2*j];f,m=build_case(n,sizes,ordered,j)
    with Solver(name='g3',bootstrap_with=f.clauses) as solver:
        for index,part in enumerate(partitions):
            for reflected in [False,True]:
                transformed=[sorted(n-1-x for x in r) if reflected else r for r in part]
                if anchor not in transformed[:2]:continue
                other=next(r for r in transformed[:2] if r!=anchor);small=transformed[2]
                coloring={x:c for c,r in enumerate([other,small]) for x in r}
                ok=solver.solve(assumptions=[i*2+coloring[x]+1 for i,x in enumerate(m['domain'])])
                expected=rank[tuple(other)]>=j
                assert ok==expected,(j,part,reflected,ok,expected)
                if ok:
                    assert decode(solver.get_model(),m)==[other,small]
                    assert j==min(rank[tuple(r)] for r in part[:2])
                    covered.add(index)
                else:rejected+=1
                checks+=1
assert len(covered)==len(partitions)
report={'n':n,'profile':sizes,'sidon_five_sets':len(rows),'reflection_orbits':len(rows)//2,'unlabeled_partitions':len(partitions),'anchored_assignment_checks':checks,'earlier_orbit_rejections':rejected,'all_partitions_covered':True}
print(json.dumps(report))
