#!/usr/bin/env python3
"""Optional discovery replay on the published quotient; not a proof of optimality.

Requires ortools==9.15.6755. The default evidence path does not use it.
"""
import json
from ortools.sat.python import cp_model
from construction import cyclic_data

out, _, _ = cyclic_data(1, 2, 5)
q, cap = len(out), 24
model = cp_model.CpModel()
w = [model.new_int_var(1, cap - q + 1, f'w{i}') for i in range(q)]
model.add(sum(w) <= cap)
for p, neighbors in enumerate(out):
    choices = []
    for mask in range(1, 1 << len(neighbors)):
        src = {v for i, v in enumerate(neighbors) if mask >> i & 1}
        dest = set().union(*(set(out[v]) for v in src)) - set(neighbors) - {p}
        indicator = model.new_bool_var(f'use{p}_{mask}')
        model.add(sum(w[i] for i in src) > sum(w[i] for i in dest)).only_enforce_if(indicator)
        choices.append(indicator)
    model.add_bool_or(choices)
model.minimize(sum(w))
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = 1
solver.parameters.random_seed = 1440
solver.parameters.max_time_in_seconds = 60
status = solver.solve(model)
if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
    raise RuntimeError('No feasible witness returned: ' + solver.status_name(status))
weights = [solver.value(x) for x in w]
# Check the returned assignment with ordinary Python integers and all subsets.
for p, neighbors in enumerate(out):
    best = 0
    for mask in range(1, 1 << len(neighbors)):
        src = {v for i, v in enumerate(neighbors) if mask >> i & 1}
        dest = set().union(*(set(out[v]) for v in src)) - set(neighbors) - {p}
        best = max(best, sum(weights[i] for i in src) - sum(weights[i] for i in dest))
    if best < 1:
        raise ValueError('Solver returned an invalid Hall witness')
print(json.dumps({'status': 'FEASIBLE WITNESS VERIFIED', 'weights': weights, 'total': sum(weights)}, sort_keys=True))
