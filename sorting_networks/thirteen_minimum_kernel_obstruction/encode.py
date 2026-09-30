"""Exact sequential F10 encoding with the proved five-kernel cover.

No future-component, pure-side, lexicographic or selected-depth filter.
Encoding/RUP helper algorithms are reused from the cited sibling sources.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import shutil
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'thirteen_prefix_frontier'))
from filtered_encoding import Encoding
from pysat.solvers import Solver
from sat_encoding import failures


def build(c, budget, solver, body, kernels=True):
    enc = Encoding(8, budget, solver, body, intervals=False,
                   pure_sides=False, disjoint_lex=False)
    for r in c['F_single_threshold_bounds']:
        enc.add_row(r['state'])
        enc.touch_bound(r['state'], r['high_cap'] + budget - 10, 1)
        enc.touch_bound(r['state'], r['low_cap'] + budget - 10, 0)
    enc.card([u[0] for u in enc.used], 1)
    enc.card([u[7] for u in enc.used], 1)
    enc.touch_bound(253, 2, 0)
    for row in enc.choice:
        for k, pair in enumerate(enc.pairs):
            if (0 in pair and pair != (0, 1)) or (7 in pair and pair != (6, 7)):
                enc.add([-row[k]])
    if kernels:
        guards = []
        for word in c['F_minimum_kernels']:
            starts = [0] if len(word) == 2 else range(budget - 2)
            for t in starts:
                guard = enc.new(); guards.append(guard)
                for j, pair in enumerate(word):
                    enc.add([-guard, enc.choice[t + j][enc.pairs.index(tuple(pair))]])
                for s in range(t):
                    for i in (0, 1, 2):
                        enc.add([-guard, -enc.used[s][i]])
        enc.add(guards)
    return enc


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--budget', type=int, choices=[10, 11], default=10)
    p.add_argument('--solver', choices=['g4', 'g3', 'm22'], default='g4')
    p.add_argument('--seconds', type=float, default=30)
    p.add_argument('--dimacs', type=Path)
    p.add_argument('--proof', type=Path)
    p.add_argument('--no-solve', action='store_true')
    p.add_argument('--no-kernels', action='store_true')
    p.add_argument('--freeze-known', action='store_true')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    assert args.seconds > 0
    assert args.budget == 10 or args.freeze_known
    assert not args.freeze_known or args.budget == 11
    assert args.proof is None or (args.dimacs and args.solver in ('g3', 'g4'))
    c = json.loads((HERE / 'certificate.json').read_text())
    f = json.loads((HERE / 'fixture.json').read_text())
    body_path = args.dimacs.with_suffix('.body.tmp') if args.dimacs else None
    body = body_path.open('w') if body_path else None
    start = time.monotonic()
    enc = build(c, args.budget, args.solver, body, not args.no_kernels)
    record = {'agent': 'six-sorting-1', 'role': 'researcher',
              'budget': args.budget, 'target': 'F', 'solver': args.solver,
              'solver_threads': 1, 'complete_at_target_budget': args.budget == 10,
              'command': sys.argv, 'kernel_block': not args.no_kernels}
    if body:
        body.close()
        with args.dimacs.open('w') as dst, body_path.open() as src:
            dst.write(f'p cnf {enc.top} {enc.clauses}\n')
            shutil.copyfileobj(src, dst)
        body_path.unlink()
        record['dimacs'] = {'variables': enc.top, 'clauses': enc.clauses,
                            'sha256': hashlib.sha256(args.dimacs.read_bytes()).hexdigest()}
    if args.proof:
        enc.solver.delete()
        enc.solver = Solver(name=args.solver, with_proof=True)
        with args.dimacs.open() as src:
            for line in src:
                if line.startswith('p'):
                    continue
                values = list(map(int, line.split()))
                assert values[-1] == 0
                enc.solver.add_clause(values[:-1])
    if args.no_solve:
        record['status'] = 'generated_not_solved'
    else:
        assumptions = enc.assume_gates(f['known_F11']) if args.freeze_known else []
        timer = threading.Timer(args.seconds, enc.solver.interrupt)
        timer.daemon = True; timer.start()
        try:
            answer = enc.solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
        finally:
            timer.cancel(); timer.join(); enc.solver.clear_interrupt()
        if answer:
            word = enc.decode()
            assert not failures(8, word, c['cases'][1]['F_states'])
            full = c['cases'][1]['prefix34'] + [[a + 2, b + 2] for a, b in word]
            assert not failures(13, full, range(8192))
            record.update({'word': word, 'full_boolean_checked': 8192,
                           'status': 'SAT_checked_positive_control' if args.freeze_known else 'SAT_checked_construction'})
        elif answer is False:
            record['status'] = 'solver_UNSAT_requires_separate_certificate_check'
            if args.proof:
                trace = enc.solver.get_proof()
                args.proof.write_text('\n'.join(trace) + '\n')
                record['native_proof_sha256'] = hashlib.sha256(args.proof.read_bytes()).hexdigest()
        else:
            record['status'] = 'UNKNOWN_no_exclusion'
    record.update({'encoding': enc.describe(), 'elapsed_seconds': time.monotonic() - start,
                   'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    enc.solver.delete()
    args.out.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({k: record[k] for k in ('status', 'elapsed_seconds', 'peak_rss_kib_linux')}))


if __name__ == '__main__':
    main()
