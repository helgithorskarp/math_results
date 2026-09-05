#!/usr/bin/env python3
"""Check the activation oracle using independently defined finite colourability."""
from pathlib import Path
import json
import sys
import time
from pysat.solvers import Solver
import activation

sys.path.insert(0, str(activation.REPO / 'hadwiger_nelson_parts509_quantified_mindegree'))
import verify_degree

start = time.monotonic()
cases = []
for case in verify_degree.fixtures():
    rows,meta = activation.encode(case)
    checked = cores = 0
    with Solver(name='cadical195', bootstrap_with=rows) as solver:
        for mask in range(1 << case['n']):
            X = {v for v in range(case['n']) if mask >> v & 1}
            expected = verify_degree.colour(case, X) is not None
            truth = solver.solve(assumptions=[v+1 for v in sorted(X)])
            assert truth == expected, (case['name'], mask)
            if truth:
                activation.decode(case, meta, solver.get_model(), X)
            else:
                core = solver.get_core()
                assert core and all(v > 0 and v-1 in X for v in core)
                assert verify_degree.colour(case, {v-1 for v in core}) is None
                cores += 1
            checked += 1
    cases.append(dict(name=case['name'], selections=checked, noncolourable_cores=cores))
source,U = activation.input_data()
rows,meta = activation.encode(source)
real=[]
with Solver(name='cadical195', bootstrap_with=rows, use_timer=True) as solver:
    for name,labels,expected in [('record509',set(range(374,509)),False),
                                  ('delete397',set(range(374,509))-{397},True)]:
        X={v for v,label in enumerate(U) if label in labels}
        solver.conf_budget(100000)
        answer=solver.solve_limited(assumptions=[v+1 for v in sorted(X)])
        assert answer == expected, (name,answer)
        if answer:activation.decode(source,meta,solver.get_model(),X)
        else:assert set(solver.get_core()) <= {v+1 for v in X}
        real.append(dict(name=name,truth=answer,seconds=solver.time()))
result=dict(status='ACTIVATION COLOURABILITY AND CORE CONTROLS VERIFIED',
            fixtures=len(cases), selections=sum(c['selections'] for c in cases),
            noncolourable_cores=sum(c['noncolourable_cores'] for c in cases),
            real_controls=real, cases=cases, seconds=time.monotonic()-start,
            full_activation_variables=meta['variables'],full_activation_clauses=meta['clauses'])
print(json.dumps(result,indent=2,sort_keys=True))
