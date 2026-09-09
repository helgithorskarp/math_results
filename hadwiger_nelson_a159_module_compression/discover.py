#!/usr/bin/env python3
"""Optional SAT witness discovery. No negative solver answer proves a claim."""
from pathlib import Path
from itertools import combinations
import argparse
import hashlib
import json
import platform
import time
import pysat
from pysat.solvers import Glucose42

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'hadwiger_nelson_nonmono159_214_lowden2/points159.tsv'
TERMINALS = [141, 142, 144]
RAD = [1, 3, 5, 15, 11, 33, 55, 165]


def mul(a, b):
    out = [0] * 8
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i ^ j] += x * y * RAD[i & j]
    return out


def build():
    points = [tuple(map(int, row.split())) for row in SOURCE.read_text().splitlines()
              if row.strip() and not row.startswith('#')]
    if len(points) != 159 or len(set(points)) != 159:
        raise ValueError('source points')
    edges = []
    for i, j in combinations(range(159), 2):
        dx = [a-b for a, b in zip(points[i][:8], points[j][:8])]
        dy = [a-b for a, b in zip(points[i][8:], points[j][8:])]
        if [a+b for a, b in zip(mul(dx, dx), mul(dy, dy))] == [144]+[0]*7:
            edges.append((i, j))
    if len(edges) != 646:
        raise ValueError('source edges')
    return edges


def run(out):
    out.mkdir(exist_ok=False, parents=True)
    start = time.monotonic()
    edges = build()
    # x(v,c)=4v+c+1. a(v)=637+v; a(v) guards its incident edges.
    def x(v, c): return 4*v+c+1
    def active(v): return 637+v
    clauses = []
    for v in range(159):
        clauses.append([x(v, c) for c in range(4)])
        clauses.extend([[-x(v, c), -x(v, d)] for c, d in combinations(range(4), 2)])
    for v, w in edges:
        clauses.extend([[-active(v), -active(w), -x(v, c), -x(w, c)] for c in range(4)])
    clauses.extend([[x(v, 0)] for v in TERMINALS])
    dimacs = 'p cnf 795 %d\n' % len(clauses) + ''.join(' '.join(map(str, c))+' 0\n' for c in clauses)
    cert = {'terminals': TERMINALS, 'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'deletion_colourings': []}
    unresolved = []
    with Glucose42(bootstrap_with=clauses) as solver:
        for v in range(159):
            if v in TERMINALS:
                continue
            solver.conf_budget(1000000)
            ans = solver.solve_limited(assumptions=[active(w) if w != v else -active(w) for w in range(159)])
            if ans:
                pos = {z for z in solver.get_model() if z > 0}
                word = ''.join('-' if w == v else str(next(c for c in range(4) if x(w, c) in pos))
                               for w in range(159))
                if any(word[a] == word[b] for a, b in edges if v not in (a, b)):
                    raise ValueError('decoded edge conflict')
                if any(word[t] != '0' for t in TERMINALS):
                    raise ValueError('decoded terminal conflict')
                cert['deletion_colourings'].append({'deleted': v, 'colours': word})
            else:
                unresolved.append({'deleted': v, 'solver_answer': 'UNSAT' if ans is False else 'UNKNOWN'})
            (out/'certificate.json').write_text(json.dumps(cert, indent=2)+'\n')
            print(json.dumps({'queried_private_vertex': v, 'positive': len(cert['deletion_colourings']),
                              'unresolved': len(unresolved)}), flush=True)
        stats = solver.accum_stats()
    (out/'producer_edges.json').write_text(json.dumps(edges, separators=(',', ':'))+'\n')
    summary = {'python': platform.python_version(), 'python_sat': pysat.__version__, 'solver': 'Glucose42',
               'new_solver_queries': 156, 'conflict_budget_per_query': 1000000,
               'clauses': len(clauses), 'variables': 795, 'base_cnf_sha256': hashlib.sha256(dimacs.encode()).hexdigest(),
               'positive_deletion_witnesses': len(cert['deletion_colourings']), 'unresolved': unresolved,
               'solver_statistics': stats, 'elapsed_seconds': time.monotonic()-start,
               'negative_answers_are_not_certificates': True}
    (out/'DISCOVERY.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    run(parser.parse_args().out)
