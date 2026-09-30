"""Constructive sequential SAT/CEGIS on the checked endpoint frontiers.

Encoding helpers are reused from the cited sibling thirteen_prefix_frontier.
Neither UNKNOWN nor an uncertified solver UNSAT is a published exclusion.
"""
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

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / 'thirteen_prefix_frontier'))
import pysat
from filtered_encoding import Encoding, canonicalize
from sat_encoding import failures, scalar


def counted(word, x):
    h = l = 0
    for a, b in word:
        A, B = x >> a & 1, x >> b & 1
        h += bool(A or B); l += not (A and B)
        if A > B:
            x ^= (1 << a) | (1 << b)
    return x, h, l


def frontier(c, f, target):
    if target == 'Z':
        limits = {r['state']: (r['high_cap'], r['low_cap'])
                  for r in c['single_threshold_bounds']}
        return 11, 19, c['Z_states'], limits, c['prefix25'], f['known21']
    limits = {}
    for r in c['single_threshold_bounds']:
        x, h, l = counted(c['nullary_minimum_kernel'], r['state'])
        x >>= 1
        new = (r['high_cap'] - h, r['low_cap'] - l)
        old = limits.get(x, new)
        limits[x] = tuple(min(a, b) for a, b in zip(new, old))
    assert set(limits) == set(c['W_states'])
    return (10, 17, c['W_states'], limits,
            c['prefix25'] + c['nullary_minimum_kernel'], c['W_known19'])


def kernel_block(enc, kernels):
    """One kernel block, arbitrary preceding gates disjoint from0/1/5.

    The unary gate is NOT forced to the front. Following binary merges
    commute left across gates disjoint from their current support.
    """
    branches = []
    for word in kernels:
        starts = [0] if len(word) == 2 else range(enc.budget - len(word) + 1)
        for t in starts:
            guard = enc.new(); branches.append(guard)
            for j, pair in enumerate(word):
                enc.add([-guard, enc.choice[t + j][enc.pairs.index(tuple(pair))]])
            for s in range(t):
                for i in (0, 1, 5):
                    enc.add([-guard, -enc.used[s][i]])
    enc.add(branches)


def limited(enc, seconds):
    timer = threading.Timer(seconds, enc.solver.interrupt)
    timer.daemon = True; timer.start()
    try:
        return enc.solver.solve_limited(expect_interrupt=True)
    finally:
        timer.cancel(); timer.join(); enc.solver.clear_interrupt()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--target', choices=['Z', 'W'], required=True)
    p.add_argument('--budget', type=int)
    p.add_argument('--mode', choices=['full', 'cegis'], default='full')
    p.add_argument('--solver', choices=['m22', 'g3', 'g4'], default='m22')
    p.add_argument('--seconds', type=float, default=45)
    p.add_argument('--segments', type=int, default=2)
    p.add_argument('--freeze-known', action='store_true')
    p.add_argument('--seed-deletions', type=int, nargs='*', default=[])
    p.add_argument('--no-kernel-block', action='store_true')
    p.add_argument('--no-intervals', action='store_true')
    p.add_argument('--minimal', action='store_true',
                   help='Omit interval, pure-side, lex, phase, shortcut and kernel-block filters.')
    p.add_argument('--dimacs', type=Path)
    p.add_argument('--proof', type=Path)
    p.add_argument('--no-solve', action='store_true')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    assert args.seconds > 0 and args.segments > 0
    assert args.proof is None or (args.dimacs is not None and args.solver in ('g3', 'g4'))
    assert args.dimacs is None or args.mode == 'full'
    cbytes = (HERE / 'certificate.json').read_bytes()
    c = json.loads(cbytes); f = json.loads((HERE / 'fixture.json').read_text())
    n, optimum_budget, states, limits, prefix, known = frontier(c, f, args.target)
    budget = optimum_budget if args.budget is None else args.budget
    assert budget >= optimum_budget
    known, swaps = canonicalize(known)
    started = time.monotonic()
    record = {'agent': 'six-sorting-1', 'role': 'researcher',
              'target': args.target, 'n': n, 'budget': budget,
              'target_budget': optimum_budget, 'global_size': len(prefix) + budget,
              'complete_for_target_budget': budget == optimum_budget,
              'larger_budget_scope': 'Restricted construction class; route/normal-form filters need not cover all larger completions.',
              'mode': args.mode, 'solver': args.solver, 'solver_threads': 1,
              'python_version': platform.python_version(), 'pysat_version': pysat.__version__,
              'certificate_sha256': hashlib.sha256(cbytes).hexdigest(),
              'command': sys.argv, 'known_disjoint_swaps': swaps,
              'segments': [], 'added_counterexamples': [],
              'kernel_block': args.target == 'Z' and not args.no_kernel_block and not args.minimal,
              'minimal_encoding': args.minimal,
              'route_filters': 'both_single_passage' if n == 11 else 'maximum_single_passage'}
    enc = None

    def save(status):
        record['status'] = status
        record['elapsed_seconds'] = time.monotonic() - started
        record['cpu_seconds'] = time.process_time()
        record['peak_rss_kib_linux'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if enc is not None:
            record['encoding'] = enc.describe()
        tmp = args.out.with_suffix(args.out.suffix + '.tmp')
        tmp.write_text(json.dumps(record, indent=2) + '\n'); tmp.replace(args.out)

    save('encoding')
    body_path = args.dimacs.with_suffix(args.dimacs.suffix + '.body.tmp') if args.dimacs else None
    body = body_path.open('w') if body_path else None
    enc = Encoding(n, budget, args.solver, body,
                   intervals=not args.no_intervals and not args.minimal,
                   pure_sides=not args.minimal, disjoint_lex=not args.minimal)
    active = states if args.mode == 'full' else [
        x for x in states if x.bit_count() in (0, 1, 2, n - 2, n - 1, n)]

    def add_state(x):
        enc.add_row(x)
        h, l = limits[x]
        enc.touch_bound(x, h + budget - optimum_budget, 1)
        enc.touch_bound(x, l + budget - optimum_budget, 0)

    for x in active:
        add_state(x)
    if n == 11:
        if not args.minimal:
            enc.phase_redundancies()
        enc.route_branch('max_once')
        if not args.minimal:
            enc.branch_shortcut()
        enc.route_branch('min_once')
        if not args.minimal:
            enc.branch_shortcut()
        central = c['central_mixed_bound']
        enc.mixed_touch_bound(central['high_mask'], central['nonlow_mask'],
                              central['union_cap'] + budget - optimum_budget)
        if not args.no_kernel_block and not args.minimal:
            kernel_block(enc, c['minimum_kernels'])
    else:
        enc.card([u[9] for u in enc.used], 1)
        for t in range(budget):
            for k, pair in enumerate(enc.pairs):
                if 9 in pair and pair != (8, 9):
                    enc.add([-enc.choice[t][k]])
        shortcuts = [(5, 7), (5, 8), (6, 8)]
        if not args.minimal:
            enc.add([row[enc.pairs.index(pair)] for row in enc.choice for pair in shortcuts])
    if body is not None:
        body.close()
        with args.dimacs.open('w') as final, body_path.open() as source:
            final.write(f'p cnf {enc.top} {enc.clauses}\n')
            shutil.copyfileobj(source, final)
        body_path.unlink()
        record['dimacs'] = {'bytes': args.dimacs.stat().st_size,
                            'sha256': hashlib.sha256(args.dimacs.read_bytes()).hexdigest()}
    if args.proof is not None:
        # Reload the exact exported clauses in a proof-enabled solver. Stream
        # them instead of retaining a second full Python CNF in memory.
        from pysat.solvers import Solver
        enc.solver.delete()
        enc.solver = Solver(name=args.solver, with_proof=True)
        with args.dimacs.open() as source:
            for line in source:
                if line.startswith('p'):
                    continue
                clause = list(map(int, line.split()))
                assert clause[-1] == 0
                enc.solver.add_clause(clause[:-1])
    if args.freeze_known:
        assert budget == len(known)
        assumptions = enc.assume_gates(known)
        result = enc.solver.solve(assumptions=assumptions)
        assert result is True, 'Known positive control rejected by the restrictions.'
        gates = enc.decode()
        assert not failures(n, gates, states)
        full = prefix + ([[a + 1, b + 1] for a, b in gates] if n == 10 else gates)
        assert not failures(13, full, range(8192))
        record['known_gates'] = gates
        record['full_boolean_inputs_checked'] = 8192
        save('SAT_checked_positive_control'); enc.solver.delete(); return
    if args.seed_deletions:
        assert len(known) - len(set(args.seed_deletions)) == budget
        assert all(0 <= i < len(known) for i in args.seed_deletions)
        seed = [g for i, g in enumerate(known) if i not in args.seed_deletions]
        seed, seed_swaps = canonicalize(seed)
        positive = set(enc.assume_gates(seed))
        enc.solver.set_phases([c if c in positive else -c for row in enc.choice for c in row])
        record['seed_disjoint_swaps'] = seed_swaps
    save('ready')
    if args.no_solve:
        save('generated_not_solved'); enc.solver.delete(); return
    for segment in range(args.segments):
        start = time.monotonic(); result = limited(enc, args.seconds)
        record['segments'].append({'segment': segment, 'answer': result,
                                   'seconds': time.monotonic() - start,
                                   'stats': enc.solver.accum_stats()})
        if result is None:
            save('UNKNOWN'); continue
        if result is False:
            if args.proof is not None:
                proof = enc.solver.get_proof()
                args.proof.write_text('\n'.join(proof) + '\n')
                record['proof'] = {'lines': len(proof), 'bytes': args.proof.stat().st_size,
                                   'sha256': hashlib.sha256(args.proof.read_bytes()).hexdigest()}
            save('solver_UNSAT_unchecked_conditional_target_only' if budget == optimum_budget
                 else 'solver_UNSAT_unchecked_restricted_construction_class_only'); break
        gates = enc.decode(); bad = failures(n, gates, states)
        if not bad:
            # The verifier is a scalar Boolean simulator, not the SAT recurrence.
            full = prefix + ([[a + 1, b + 1] for a, b in gates] if n == 10 else gates)
            assert not failures(13, full, range(8192))
            record['gates'] = gates; record['full_network'] = full
            record['full_boolean_inputs_checked'] = 8192
            save('SAT_checked_construction'); break
        assert args.mode == 'cegis'
        record['added_counterexamples'].append(bad)
        for x in bad:
            add_state(x)
        save('counterexamples_added')
    enc.solver.delete()
    print(json.dumps({k: record[k] for k in
                      ('target', 'status', 'elapsed_seconds', 'peak_rss_kib_linux')}))


if __name__ == '__main__':
    main()
