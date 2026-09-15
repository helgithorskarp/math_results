#!/usr/bin/env python3
"""Re-enumerate the host relation with durable witnesses and a wall-clock cap.

Needs python-sat with cadical195. Enumeration order/witnesses may vary by version;
on complete termination the canonical pattern SET must equal the frozen table.
The published completeness proof is regenerated from the frozen table by verify.py.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
from receiver import H, PERMS, reconstruct, cnf, require, proper

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
    with Solver(name='cadical195', bootstrap_with=clauses) as solver:
        with (a.out / 'enumerated.tsv').open('w', buffering=1) as table:
            while len(seen) < a.max_patterns:
                if not solver.solve():
                    status = 'COMPLETE_SOLVER_UNSAT'
                    break
                model = {x for x in solver.get_model() if x > 0}
                col = {v: next(c for c in range(4) if var(v, c) in model) for v in H}
                perm = min(PERMS, key=lambda p: tuple(p[col[v]] for v in B))
                col = {v: perm[c] for v, c in col.items()}
                word = ''.join(str(col[v]) for v in H)
                proper(word, H, g['host_edges'])
                pattern = ''.join(str(col[v]) for v in B)
                require(pattern not in seen, 'duplicate orbit')
                seen.add(pattern)
                table.write(pattern + '\t' + word + '\n')
                for p in PERMS:
                    solver.add_clause([-var(v, p[col[v]]) for v in B if v != 0])
                if len(seen) % 100 == 0:
                    print(len(seen), round(time.monotonic() - start, 2), flush=True)
    if status == 'COMPLETE_SOLVER_UNSAT':
        frozen = {r.split('\t')[0] for r in (HERE / 'host_relation.tsv').read_text().splitlines()}
        require(seen == frozen, 'full canonical relation agrees with frozen table')
    result = dict(status=status,canonical_patterns=len(seen),seconds=time.monotonic()-start,
                  proof_checked=False)
    (a.out / 'enumeration.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--seconds', type=int, default=900)
    ap.add_argument('--max-patterns', type=int, default=30000)
    ap.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    a = ap.parse_args()
    require(a.seconds > 0 and a.max_patterns > 0, 'positive finite bounds')
    a.out.mkdir(parents=True, exist_ok=True)
    if a.worker:
        worker(a)
        return
    command = [sys.executable, str(Path(__file__).resolve()), '--worker', '--out',
               str(a.out.resolve()), '--max-patterns', str(a.max_patterns)]
    try:
        subprocess.run(command, check=True, timeout=a.seconds)
    except subprocess.TimeoutExpired:
        (a.out / 'enumeration.json').write_text(json.dumps({
            'status': 'INCOMPLETE_WALL_LIMIT', 'proof_checked': False,
            'note': 'Partial witness rows preserved; no completeness claim.'}) + '\n')
        raise SystemExit(2)


if __name__ == '__main__':
    main()
