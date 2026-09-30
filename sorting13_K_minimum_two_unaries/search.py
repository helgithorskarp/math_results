"""Exact arbitrary-depth six-word K18 completion formula.

Author and executing agent: six-sorting-2, researcher. Native solving is
optional; the published core/RUP can be checked without a solver.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'sorting13_pure_maximum_exclusions'
INTERVAL = HERE.parent / 'sorting13_suffix_interval_transfer'
FIXTURE = HERE.parent / 'sorting13_double_pure_obstruction' / 'fixture.json'
sys.path.insert(0, str(BASE))
from sequential_sat import generate, replay
from necessities import augment as established_necessities
from minimum import minimum_dfa, extra_bounds
from activity import encode as activity
from boundary_ranks import encode as boundary_ranks

spec = importlib.util.spec_from_file_location('published_interval_encoder', INTERVAL / 'interval_blocks.py')
intervals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intervals)


def canonicalize(word):
    word = [tuple(pair) for pair in word]
    changed = True
    while changed:
        changed = False
        for t in range(len(word) - 1):
            if word[t] > word[t + 1] and not set(word[t]) & set(word[t + 1]):
                word[t], word[t + 1] = word[t + 1], word[t]
                changed = True
    return word


def source_check():
    manifest = json.loads((HERE / 'source-manifest.json').read_text())
    for name, expected in manifest['files'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name


def make(path, frozen=None):
    source_check()
    assert hashlib.sha256((INTERVAL / 'interval_blocks.py').read_bytes()).hexdigest() == \
        json.loads((INTERVAL / 'certificate.json').read_text())['encoder_sha256']
    f = json.loads(FIXTURE.read_text())
    pruning = json.loads((HERE / 'pruning.json').read_text())
    cuts = json.loads((HERE / 'all-cuts.json').read_text())
    gates = len(frozen) if frozen is not None else 18
    assert gates >= 18
    if frozen is not None:
        frozen = canonicalize(frozen)

    def augment(w, choices, pairs, bits):
        result = established_necessities(w, choices, pairs, bits, pruning, gates,
                                        1 if gates == 18 else 0, frozen, gates == 18)
        extra_bounds(w, choices, pairs, bits, cuts['additional_cuts'], gates)
        minimum_dfa(w, choices, pairs, gates)
        result.update(minimum_dfa_states=7,
                      minimum_kernel_class='exactly one unary, six words',
                      minimum_kernel_selection=None, additional_witnesses=75,
                      total_witnesses=108,
                      additional_cuts_sha256=hashlib.sha256((HERE / 'all-cuts.json').read_bytes()).hexdigest(),
                      no_unary_front_loading=True, sorted_required=True,
                      scope=f'All45 pairs in all{gates} sequential positions; arbitrary intervening comparators and depth')
        before_variables, before_clauses = w.variables, w.clauses
        partitions = intervals.encode(w, choices, pairs, gates, 10)
        for cut in partitions[0]:
            w.add(-cut)
        interval_variables = w.variables - before_variables
        interval_clauses = w.clauses - before_clauses
        assert interval_variables == 9 * (gates + 1)
        assert interval_clauses == 513 * gates + 18
        before_variables, before_clauses = w.variables, w.clauses
        states = sorted(x for x in bits if x != ((1 << x.bit_count()) - 1) << (10 - x.bit_count()))
        assert len(states) == 116
        swaps = activity(w, choices, pairs, bits, states, gates)
        activity_variables = w.variables - before_variables
        activity_clauses = w.clauses - before_clauses
        before_variables, before_clauses = w.variables, w.clauses
        boundary_ranks(w, partitions, bits, 10, gates)
        assert w.variables == before_variables
        result.update(agent='six-sorting-2', role='researcher',
                      suffix_components_are_intervals=True, interval_partitions=512,
                      interval_source_commit='4b9ba67c332172a1592920b14f5e291ab0c4589c',
                      interval_source_graph='bafkreigtu3vcclhx5av6kphyhybdxvkzjuqh6yyoqeiyic63peuqmgyvx4',
                      interval_encoder_sha256=hashlib.sha256((INTERVAL / 'interval_blocks.py').read_bytes()).hexdigest(),
                      interval_variables=interval_variables, interval_clauses=interval_clauses,
                      interval_cuts=partitions, connected_initial_graph=True,
                      all_actual_gates_active=True, activity_states=states,
                      activity_flags=swaps, activity_variables=activity_variables,
                      activity_clauses=activity_clauses,
                      boundary_rank_conservation=True, boundary_rank_variables=0,
                      boundary_rank_clauses=w.clauses-before_clauses,
                      commute_lexicographic=True,
                      frozen_positive_control=frozen is not None,
                      filters='Actual suffix intervals, connected full graph and boundary rank conservation; actual gate activity; existential ordering of adjacent disjoint comparators; no layer/depth restriction or unary front-loading',
                      necessity_scope='Necessary/existential for K18; longer frozen words are checked positive controls only')
        return result

    return generate(10, f['K_states'], gates, path, commute=True,
                    encode_sorted=True, augment=augment)


def solve(path, conflicts, seconds):
    import pysat
    from pysat.solvers import Glucose4
    assert 0 < conflicts <= 30000 and 0 < seconds <= 40, 'No cap escalation'
    start = time.monotonic()
    meta = json.loads(path.with_suffix('.meta.json').read_text())
    result = dict(agent='six-sorting-2', role='researcher', solver='Glucose4 via python-sat',
                  pysat=pysat.__version__, conflict_budget=conflicts,
                  wall_budget_seconds=seconds, cnf_sha256=meta['cnf_sha256'])
    with Glucose4(with_proof=True, use_timer=True) as solver:
        with path.open() as stream:
            for line in stream:
                if line.strip() and line[:1] not in 'cp':
                    solver.add_clause([int(v) for v in line.split()[:-1]])
        timer = threading.Timer(max(0.001, seconds - (time.monotonic() - start)), solver.interrupt)
        timer.start()
        solver.conf_budget(conflicts)
        try:
            status = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
            timer.join()
            solver.clear_interrupt()
        result['status'] = 'SAT' if status is True else 'UNSAT_unchecked' if status is False else 'UNKNOWN'
        result.update(stats=solver.accum_stats(), solver_seconds=solver.time())
        if status is True:
            model = solver.get_model()
            positive = {v for v in model if v > 0}
            word = [meta['pairs'][next(j for j, v in enumerate(row) if v in positive)]
                    for row in meta['choices']]
            replay(meta['wires'], meta['states'], word)
            result['network'] = word
            path.with_suffix('.model.json').write_text(json.dumps(model) + '\n')
        if status is False:
            proof = solver.get_proof()
            assert proof and proof[-1].strip() == '0'
            path.with_suffix('.drat').write_text('\n'.join(proof) + '\n')
    result.update(seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path.with_suffix('.result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result), flush=True)


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=('generate', 'solve'))
    p.add_argument('--path', required=True, type=Path)
    p.add_argument('--freeze', type=Path)
    p.add_argument('--conflicts', type=int, default=30000)
    p.add_argument('--seconds', type=float, default=40)
    args = p.parse_args()
    if args.command == 'generate':
        word = json.loads(args.freeze.read_text()) if args.freeze else None
        meta = make(args.path, word)
        info = {k: v for k, v in meta.items() if k not in ('states', 'choices', 'pairs')}
        info['extra'] = {k: v for k, v in info['extra'].items()
                         if k not in ('interval_cuts', 'activity_states', 'activity_flags')}
        print(json.dumps(info), flush=True)
    else:
        solve(args.path, args.conflicts, args.seconds)


if __name__ == '__main__':
    main()
