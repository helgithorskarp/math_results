#!/usr/bin/env python3
"""Optional bounded seed rediscovery; proof replay needs no solver."""
import argparse
import json
import time
from collections import Counter
from pathlib import Path
import native
import produce

def formula(n, edges):
    def x(v, c):
        return 4*v+c+1
    def active(v):
        return 4*n+v+1
    cnf = []
    for v in range(n):
        cnf.append([-active(v)]+[x(v, c) for c in range(4)])
        for c in range(4):
            for d in range(c):
                cnf.append([-x(v, c), -x(v, d)])
    for u, v in edges:
        for c in range(4):
            cnf.append([-x(u, c), -x(v, c)])
    return cnf

def main():
    from pysat.solvers import Cadical195
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); args.out.mkdir(parents=True, exist_ok=False)
    hp, edges, inv, terms = produce.build(); n = len(hp)
    cnf = formula(n, edges); degree = Counter(v for e in edges for v in e)
    reps = sorted((v for v in range(n) if v <= inv[v] and v not in terms), key=lambda v: (degree[v], v))
    def assumptions(deleted=None):
        return [(4*n+v+1)*(-1 if v == deleted else 1) for v in range(n)]
    def word(model, deleted=None):
        positive = set(z for z in model if z > 0)
        w = ''.join('-' if v == deleted else str(next(c for c in range(4) if 4*v+c+1 in positive)) for v in range(n))
        native.require(all(w[u] != w[v] for u, v in edges if deleted not in (u, v)), 'solver model invalid')
        return w
    with Cadical195(bootstrap_with=cnf) as solver:
        solver.conf_budget(200000)
        answer = solver.solve_limited(assumptions=assumptions())
        native.require(answer is True, 'baseline not decided SAT')
        baseline = word(solver.get_model())
    source = dict(version='degrey-terminal-cover-v1', target=508, terminals=terms, baseline=baseline, steps=[])
    trace = []; closed = False
    with Cadical195(bootstrap_with=cnf) as solver:
        for v in reps:
            before = solver.accum_stats()['conflicts']; start = time.monotonic()
            solver.conf_budget(200000)
            answer = solver.solve_limited(assumptions=assumptions(v)+[4*terms[0]+1, 4*terms[1]+2])
            trace.append(dict(deleted=v, answer=answer, conflicts=solver.accum_stats()['conflicts']-before, seconds=time.monotonic()-start))
            if answer is True:
                w = word(solver.get_model(), v)
                native.require(w[terms[0]] != w[terms[1]], 'terminal pins violated')
                source['steps'].append(dict(kind='seed', deleted=v, word=w))
            (args.out/'seeds.json').write_text(json.dumps(source, separators=(',', ':'))+'\n')
            (args.out/'query_trace.json').write_text(json.dumps(trace, indent=2)+'\n')
            # No budget increase: every orbit is queried at most once.
            try:
                result = produce.generate(source)
            except ValueError as error:
                if str(error) != 'seed set does not close target':
                    raise
            else:
                (args.out/'certificate.json').write_text(json.dumps(result, separators=(',', ':'))+'\n')
                closed = True
                break
    print(json.dumps(dict(complete_target_gate=closed, queries=len(trace),
                          sat=sum(r['answer'] is True for r in trace),
                          unknown=sum(r['answer'] is None for r in trace))))

if __name__ == '__main__':
    main()
