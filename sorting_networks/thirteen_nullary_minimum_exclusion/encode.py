"""Regenerate the nine complete sequential F10 encodings and native proofs.

Reuse, with citation, Encoding from the thirteen_prefix_frontier source.
No layer, future-interval, pure-side, kernel or lexicographic filter is used.
Generated CNFs/proofs belong in the caller's scratch directory, not Git.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'thirteen_prefix_frontier'))
from filtered_encoding import Encoding
from pysat.solvers import Solver


def build(source, budget, body=None):
    e = Encoding(8, budget, 'g4', body, intervals=False, pure_sides=False, disjoint_lex=False)
    for z, high, low, hw, lw in source['single_threshold_rows']:
        e.add_row(z)
        e.touch_bound(z, high + budget - 10, 1)
        e.touch_bound(z, low + budget - 10, 0)
    e.touch_bound(255 ^ (1 << source['minimum_leaf_cap1']), 1 + budget - 10, 0)
    return e


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--index', type=int)
    parser.add_argument('--no-solve', action='store_true')
    parser.add_argument('--positive', action='store_true')
    parser.add_argument('--seconds', type=float, default=30)
    args = parser.parse_args(); assert args.seconds > 0
    c = json.loads((HERE / 'certificate.json').read_text())
    f = json.loads((HERE / 'fixture.json').read_text())
    metadata = {r['index']: r for r in c['proofs']}
    args.scratch.mkdir(parents=True, exist_ok=True)
    sources = [s for s in c['sources'] if args.index is None or s['index'] == args.index]
    assert sources
    if args.positive:
        sources = [next(s for s in c['sources'] if s['index'] == 8)]
    for source in sources:
        start = time.monotonic(); index = source['index']; budget = 11 if args.positive else 10
        if args.positive:
            e = build(source, budget)
            assert e.solver.solve(assumptions=e.assume_gates(f['known_F38_11']))
            assert list(map(list, e.decode())) == f['known_F38_11']; e.solver.delete()
            print(json.dumps({'index': index, 'status': 'SAT eleven-gate positive encoding control'}), flush=True)
            continue
        stem = args.scratch / f'F{index}-size10'; body_path = stem.with_suffix('.body.tmp')
        with body_path.open('w') as body:
            e = build(source, budget, body)
        cnf = stem.with_suffix('.cnf')
        with cnf.open('w') as dst, body_path.open() as src:
            dst.write(f'p cnf {e.top} {e.clauses}\n'); shutil.copyfileobj(src, dst)
        body_path.unlink()
        m = metadata[index]
        assert e.top == m['variables'] and e.clauses == m['clauses']
        assert hashlib.sha256(cnf.read_bytes()).hexdigest() == m['full_cnf_sha256']
        e.solver.delete()
        if args.no_solve:
            print(json.dumps({'index': index, 'status': 'Exact fullCNF hash reproduced'}), flush=True)
            continue
        solver = Solver(name='g4', with_proof=True)
        for line in cnf.open():
            if not line.startswith('p'):
                row = list(map(int, line.split())); assert row[-1] == 0; solver.add_clause(row[:-1])
        timer = threading.Timer(args.seconds, solver.interrupt); timer.daemon = True; timer.start()
        try:
            answer = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel(); timer.join(); solver.clear_interrupt()
        assert answer is False, 'SAT needs direct witness checking; timeout/UNKNOWN is no exclusion'
        proof = stem.with_suffix('.drat'); proof.write_text('\n'.join(solver.get_proof()) + '\n')
        solver.delete()
        assert hashlib.sha256(proof.read_bytes()).hexdigest() == m['native_proof_sha256'], 'Use the pinned solver package; check any alternative trace independently'
        print(json.dumps({'index': index, 'status': 'Native proof regenerated; run check_proof.py',
                          'elapsed_seconds': time.monotonic() - start}), flush=True)


if __name__ == '__main__':
    main()
