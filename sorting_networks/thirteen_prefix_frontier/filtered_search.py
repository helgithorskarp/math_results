"""Reproducible sequential SAT/CEGIS frontier; UNKNOWN proves no exclusion."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform
import resource
import shutil
import sys
import threading
import time

import pysat
from filtered_encoding import Encoding, canonicalize
from sat_encoding import failures, scalar

HERE = Path(__file__).resolve().parent


def limited(enc, seconds, assumptions):
    timer = threading.Timer(seconds, enc.solver.interrupt)
    timer.daemon = True
    timer.start()
    try:
        return enc.solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
    finally:
        timer.cancel()
        timer.join()
        enc.solver.clear_interrupt()


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1048576), b''):
            h.update(block)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--case', type=int, required=True, choices=[1, 2])
    p.add_argument('--budget', type=int, default=20)
    p.add_argument('--solver', choices=['m22', 'g3', 'g4'], default='m22')
    p.add_argument('--seconds', type=float, default=45)
    p.add_argument('--segments', type=int, default=4)
    p.add_argument('--mode', choices=['full', 'cegis'], default='full')
    p.add_argument('--no-deletion-bounds', action='store_true')
    p.add_argument('--no-constants', action='store_true')
    p.add_argument('--no-intervals', action='store_true')
    p.add_argument('--no-pure-sides', action='store_true')
    p.add_argument('--no-disjoint-lex', action='store_true')
    p.add_argument('--mixed-bounds', type=Path)
    p.add_argument('--mixed-limit', type=int)
    p.add_argument('--route-branch', choices=['max_once', 'min_once'])
    p.add_argument('--no-phase-bans', action='store_true')
    p.add_argument('--branch-shortcut', action='store_true')
    p.add_argument('--freeze-known', action='store_true')
    p.add_argument('--seed-deletion', type=int)
    p.add_argument('--self-check', action='store_true')
    p.add_argument('--dimacs', type=Path)
    p.add_argument('--no-solve', action='store_true')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    assert args.budget >= 0 and args.seconds > 0 and args.segments > 0
    assert args.mode == 'full' or args.no_deletion_bounds
    assert args.dimacs is None or args.mode == 'full'
    assert not args.branch_shortcut or args.route_branch is not None
    cert = json.loads((HERE / 'certificate.json').read_text())
    case = cert['cases'][args.case]
    states = case['states']
    prefix = cert['prefix'] + case['tournament']
    known = case['known_21_suffix']
    assert not failures(11, known, states)
    if not args.no_disjoint_lex:
        known, known_swaps = canonicalize(known)
    else:
        known_swaps = 0
    started = time.monotonic()
    record = {'agent': 'six-sorting-1', 'role': 'researcher',
              'case': args.case, 'budget': args.budget, 'mode': args.mode,
              'deletion_bounds': not args.no_deletion_bounds,
              'certificate_sha256': file_hash(HERE / 'certificate.json'),
              'pysat_version': pysat.__version__, 'solver': args.solver,
              'python_version': platform.python_version(), 'command': sys.argv,
              'solver_threads': 1, 'segments': [], 'counterexamples_added': [],
              'freeze_known': args.freeze_known}
    record['route_branch'] = args.route_branch
    record['known_disjoint_swaps'] = known_swaps
    record['known_order_used'] = known
    enc = None

    def save(status):
        record['status'] = status
        record['elapsed_seconds'] = time.monotonic() - started
        record['cpu_seconds'] = time.process_time()
        record['peak_rss_kib_linux'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if enc is not None:
            record['encoding'] = enc.describe()
        temporary = args.out.with_suffix(args.out.suffix + '.tmp')
        temporary.write_text(json.dumps(record, indent=2) + '\n')
        temporary.replace(args.out)

    save('encoding')
    if args.self_check:
        from check_filters import main as check_filters
        record['self_check'] = check_filters()
    body_path = args.dimacs.with_suffix(args.dimacs.suffix + '.body.tmp') if args.dimacs else None
    body = body_path.open('w') if body_path else None
    enc = Encoding(11, args.budget, args.solver, body,
                   constants=not args.no_constants,
                   intervals=not args.no_intervals,
                   pure_sides=not args.no_pure_sides,
                   disjoint_lex=not args.no_disjoint_lex)
    active = states if args.mode == 'full' else [x for x in states if x.bit_count() in (1, 2, 9, 10)]
    for x in active:
        enc.add_row(x)
    if not args.no_deletion_bounds:
        for j, x in enumerate(states):
            enc.touch_bound(x, case['maximum_suffix_touch_limits'][j] + args.budget - 20, 1)
            enc.touch_bound(x, case['minimum_suffix_touch_limits'][j] + args.budget - 20, 0)
    if args.mixed_bounds:
        mixed = json.loads(args.mixed_bounds.read_text())
        rows = next(c for c in mixed['cases'] if c['case'] == args.case)['strict_middle7_rows']
        if args.mixed_limit is not None:
            assert args.mixed_limit >= 0
            rows = rows[:args.mixed_limit]
        record['mixed_certificate_sha256'] = file_hash(args.mixed_bounds)
        record['mixed_bounds_added'] = len(rows)
        for r in rows:
            enc.mixed_touch_bound(r['high_mask'], r['nonlow_mask'],
                                  r['suffix_union_cap'] + args.budget - 20)
    if args.case == 1:
        for i in range(4):
            enc.forbid_permanent_pair((i, 10))
    if not args.no_phase_bans:
        enc.phase_redundancies()
    if args.route_branch:
        enc.route_branch(args.route_branch)
    if args.branch_shortcut:
        enc.branch_shortcut()
    if body:
        body.close()
        with args.dimacs.open('w') as final, body_path.open() as source:
            final.write(f'p cnf {enc.top} {enc.clauses}\n')
            shutil.copyfileobj(source, final)
        body_path.unlink()
        record['dimacs'] = {'path': str(args.dimacs), 'bytes': args.dimacs.stat().st_size,
                            'sha256': file_hash(args.dimacs)}
    assumptions = []
    if args.freeze_known:
        assert args.budget == len(known)
        assumptions = enc.assume_gates(known)
    elif args.seed_deletion is not None:
        assert args.budget == len(known) - 1 and 0 <= args.seed_deletion < len(known)
        seed = known[:args.seed_deletion] + known[args.seed_deletion + 1:]
        positive = set(enc.assume_gates(seed))
        enc.solver.set_phases([c if c in positive else -c for row in enc.choice for c in row])
    save('ready')
    print(json.dumps({'event': 'ready', **enc.describe()}), flush=True)
    if args.no_solve:
        save('INSTANCE_generated_without_solving')
        enc.solver.delete()
        return
    for segment in range(args.segments):
        start_segment = time.monotonic()
        answer = limited(enc, args.seconds, assumptions)
        event = {'segment': segment, 'seconds': time.monotonic() - start_segment,
                 'answer': answer, **enc.describe()}
        record['segments'].append(event)
        print(json.dumps({'event': 'segment', **event}), flush=True)
        if answer is False:
            save('solver_UNSAT_unchecked_fixed_prefix_only')
            break
        if answer is None:
            save('UNKNOWN')
            continue
        gates = enc.decode()
        bad = failures(11, gates, states)
        record['latest_candidate'] = gates
        record['latest_candidate_failures'] = len(bad)
        if not bad:
            assert not failures(13, prefix + gates, range(8192))
            record['verified_comparators'] = prefix + gates
            save('SAT_independently_verified_all_8192_inputs')
            print(json.dumps({'event': 'verified', 'size': len(prefix) + len(gates)}), flush=True)
            break
        assert args.mode == 'cegis'
        for x in bad:
            enc.add_row(x)
        record['counterexamples_added'].append(bad)
        save('counterexamples_added')
    else:
        save('UNKNOWN')
    enc.solver.delete()
    print(json.dumps({'event': 'finished', 'status': record['status'],
                      'elapsed_seconds': record['elapsed_seconds']}), flush=True)


if __name__ == '__main__':
    main()
