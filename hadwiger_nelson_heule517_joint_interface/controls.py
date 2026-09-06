#!/usr/bin/env python3
"""Exhaust small ordinary colourings versus both encodings and orbit removal."""
from itertools import product
import json
from pysat.solvers import Solver
import engine as E

def sat(n,cs):
    with Solver(name='cadical195',bootstrap_with=cs) as s: return s.solve()

fixtures=[([0,1,2],[],[0,1]),([0,1,2],[(0,1),(1,2)],[0,2]),
          ([0,1,2],[(0,1),(0,2),(1,2)],[0,1,2])]
projections=0
for vertices,edges,boundary in fixtures:
    expected=set()
    for c in product(range(4),repeat=len(vertices)):
        if c[0]!=0 or any(c[u]==c[v] for u,v in edges):continue
        expected.add(E.normalized(''.join(map(str,c)),vertices,boundary)[0])
    n,cs=E.cnf(vertices,edges)
    for row in sorted(expected):
        # Check this whole boundary row is feasible, then exclude its orbit.
        fixes=[[4*v+int(c)+1] for v,c in zip(boundary,row)]
        assert sat(n,cs+fixes)
        cs+=E.blocking(row,vertices,boundary);projections+=1
    assert not sat(n,cs)

# Small-side comparisons use a fixed two-vertex boundary and every boundary row.
case_checks=0
for selected in [[],[2],[3],[2,3]]:
    for pattern in map(''.join,product('0123',repeat=2)):
        boundary=[0,1];cross=[(0,2),(1,2),(1,3)];se=[(2,3)]
        expected=False
        for colors in product(range(4),repeat=len(selected)):
            cmap=dict(zip(selected,colors));fixed=dict(zip(boundary,map(int,pattern)))
            if any(u in cmap and v in cmap and cmap[u]==cmap[v] for u,v in se):continue
            if any(v in cmap and fixed[u]==cmap[v] for u,v in cross):continue
            expected=True;break
        n,cs=E.small_case(selected,se,cross,boundary,pattern)
        assert sat(n,cs)==expected;case_checks+=1
# One vertex adjacent to four differently coloured boundary vertices is blocked.
n,cs=E.small_case([4],[],[(i,4) for i in range(4)],list(range(4)),'0123')
assert not sat(n,cs)
print(json.dumps({'small_projection_patterns':projections,'small_side_assignments':case_checks,
                  'rainbow_block_control':True,'production_queries_repeated':0}))
