#!/usr/bin/env python3
"""Generate the complete receiver relation under finite resource limits.

Needs python-sat/cadical195. All generated tables, CNFs and logs belong outside
the repository. A timeout preserves partial rows and is not completeness.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from geometry import H, PERMS, reconstruct, cnf, proper, require
from verify import verify

HERE = Path(__file__).resolve().parent


def worker(a):
    from pysat.solvers import Solver
    g = reconstruct(HERE / 'points.tsv')
    B = g['boundary']
    clauses, var = cnf(H, g['host_edges'])
    clauses.append([var(0, 0)])
    seen = set()
    status = 'INCOMPLETE_PATTERN_LIMIT'
    start = time.monotonic()
    journal = a.out / 'host_relation.tsv'
    require(not journal.exists(), 'use a fresh output directory; preserve prior census')
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        with journal.open('w', buffering=1) as table:
            while len(seen) < a.max_patterns:
                if not solver.solve():
                    status = 'COMPLETE_SOLVER_UNSAT'
                    break
                model = {x for x in solver.get_model() if x > 0}
                col = {v: next(c for c in range(4) if var(v, c) in model) for v in H}
                p = min(PERMS, key=lambda p: tuple(p[col[v]] for v in B))
                col = {v: p[c] for v, c in col.items()}
                word = ''.join(str(col[v]) for v in H)
                proper(word, H, g['host_edges'])
                pattern = ''.join(str(col[v]) for v in B)
                require(pattern not in seen, 'duplicate orbit')
                seen.add(pattern)
                table.write(pattern + '\t' + word + '\n')
                for p in PERMS:
                    solver.add_clause([-var(v, p[col[v]]) for v in B if v != 0])
                if len(seen) % 1000 == 0:
                    print(json.dumps(dict(patterns=len(seen), seconds=time.monotonic()-start)),
                          flush=True)
    if status == 'COMPLETE_SOLVER_UNSAT':
        verify(a.out, journal)
    result = dict(status=status, canonical_patterns=len(seen), seconds=time.monotonic()-start,
                  independently_checked_UNSAT_proof=False)
    (a.out / 'enumeration.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--seconds', type=int, default=1200)
    ap.add_argument('--max-patterns', type=int, default=100000)
    ap.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    a = ap.parse_args()
    require(a.seconds > 0 and a.max_patterns > 0, 'positive limits')
    a.out.mkdir(parents=True, exist_ok=True)
    if a.worker:
        worker(a)
        return
    command = [sys.executable, str(Path(__file__).resolve()), '--worker',
               '--out', str(a.out.resolve()), '--max-patterns', str(a.max_patterns)]
    try:
        subprocess.run(command, check=True, timeout=a.seconds)
    except subprocess.TimeoutExpired:
        (a.out / 'enumeration.json').write_text(json.dumps({
            'status': 'INCOMPLETE_WALL_LIMIT', 'complete': False,
            'note': 'Partial positive rows preserved; no completeness inference.'}) + '\n')
        raise SystemExit(2)


if __name__ == '__main__':
    main()
