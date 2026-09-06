#!/usr/bin/env python3
"""Tiny exact colouring controls for activation, and omission-cover rejection."""
from itertools import product
import json
from pysat.solvers import Solver
import engine as E
from verify import cover

checks=0
for selected in [[],[2],[3],[2,3]]:
    for pat in map(''.join,product('0123',repeat=2)):
        data={'small':[2,3],'small_edges':[(2,3)],'cross_edges':[(0,2),(1,2),(1,3)],
              'boundary':[0,1],'profiles':[{'pattern':pat}]}
        n,cs=E.activated_case(data,0)
        assumptions=[(9+i)*(1 if v in selected else -1) for i,v in enumerate([2,3])]
        expected=False
        for vals in product(range(4),repeat=len(selected)):
            c=dict(zip(selected,vals));f=dict(zip([0,1],map(int,pat)))
            if 2 in c and 3 in c and c[2]==c[3]:continue
            if any(v in c and c[v]==f[u] for u,v in data['cross_edges']):continue
            expected=True;break
        with Solver(name='cadical195',bootstrap_with=cs) as solver:
            assert solver.solve(assumptions=assumptions)==expected
        checks+=1
# A blocked vertex is harmless when inactive, and impossible when active.
data={'small':[4],'small_edges':[],'cross_edges':[(i,4) for i in range(4)],
      'boundary':[0,1,2,3],'profiles':[{'pattern':'0123'}]}
n,cs=E.activated_case(data,0)
with Solver(name='cadical195',bootstrap_with=cs) as solver:
    assert solver.solve(assumptions=[-5]) and not solver.solve(assumptions=[5])

out=cover([{0,1},{0,2},{1,2}],list(range(10)));assert out['nine_sets_checked']==10
try:cover([{0,1},{0,2}],list(range(10)))
except ValueError:pass
else:raise RuntimeError('incomplete cover accepted')
print(json.dumps({'activated_colouring_cases':checks,'inactive_and_active_rainbow_controls':2,
                  'tiny_nine_omission_sets':10,'incomplete_cover_rejected':True,
                  'production_queries_repeated':0}))
