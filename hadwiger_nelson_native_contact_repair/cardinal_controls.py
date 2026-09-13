#!/usr/bin/env python3
"""Truth-table audit of guarded native-cardinality conditions."""
from itertools import product
from pysat.solvers import Solver
import json
count=0
for n in range(7):
 for required in range(1,5):
  for bits in product((0,1),repeat=n+1):
   with Solver(name='minicard') as s:
    clones=list(range(n+2,n+2+required))
    s.add_atmost(list(range(2,n+2))+clones,n)
    for y in clones:s.add_clause([-1,y]);s.add_clause([1,-y])
    assumptions=[1 if bits[0] else -1]+[(i+2) if not b else -(i+2) for i,b in enumerate(bits[1:])]
    actual=s.solve(assumptions=assumptions);expected=not bits[0] or sum(bits[1:])>=required
    if actual!=expected:raise ValueError('guarded cardinality mismatch')
    count+=1
print(json.dumps({'status':'PASS','assignments':count,'neighbours_through':6,'required_selected_neighbours_through':4}))
