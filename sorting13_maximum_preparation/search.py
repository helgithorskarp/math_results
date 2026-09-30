"""Depth-free L109 probes with exact marked-input budgets."""
import argparse
import hashlib
import importlib.util
import json
import sys
import resource
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUBLIC = HERE.parent / 'sorting13_pure_maximum_exclusions'
sys.path.insert(0, str(PUBLIC))
from sequential_sat import generate, neg, replay


def augment(w, choices, pairs, bits, pruning, gates, freeze, tight, exact_maximum=False, max_preparations=None):
    selected = pruning['critical_single_bounds'] + pruning['selected_mixed_bounds'] + pruning['designated_bounds']
    selected = list({(r['x'], r['y']): r for r in selected}.values())
    events = {}
    for row in selected:
        x, y = row['x'], row['y']
        hits = [w.var() for _ in range(gates)]
        for t in range(gates):
            for j, (a, b) in enumerate(pairs):
                c = choices[t][j]
                outside = [bits[x][t][a], bits[x][t][b], neg(bits[y][t][a]), neg(bits[y][t][b])]
                for v in outside:
                    w.add(-c, neg(v), hits[t])
                w.add(-c, -hits[t], *outside)
        w.at_most(hits, row['cap'] + gates - 16)
        events[x, y] = hits
    if gates == 16 and tight:
        # The new threshold cut bounds the static zero0 trajectory by one.
        # The separate one-zero1 row forces that sole0-gate to be(0,1).
        root = [choices[t][pairs.index((0, 1))] for t in range(gates)]
        w.exactly_one(root)
        for t in range(gates):
            for j, pair in enumerate(pairs):
                if 0 in pair and pair != (0, 1):
                    w.add(-choices[t][j])
        phase = [[w.var() for _ in range(3)] for _ in range(gates + 1)]
        for p in phase:
            w.exactly_one(p)
        w.add(phase[0][0]); w.add(phase[-1][2])
        for t in range(gates):
            for s in range(3):
                for j, pair in enumerate(pairs):
                    if s == 0:
                        dest = 1 if pair == (5, 7) else 0 if 5 not in pair and 8 not in pair else None
                    elif s == 1:
                        dest = 2 if pair == (7, 8) else 1 if 7 not in pair and 8 not in pair else None
                    else:
                        dest = 2 if 8 not in pair else None
                    if dest is None:
                        w.add(-phase[t][s], -choices[t][j])
                    else:
                        w.add(-phase[t][s], -choices[t][j], phase[t+1][dest])
        post = []
        early67 = []
        for t in range(gates):
            incident = w.var()
            w.equivalent_or(incident, [choices[t][j] for j, (a, b) in enumerate(pairs) if b == 7])
            p = w.var(); post.append(p)
            w.add(-p, phase[t][2]); w.add(-p, incident)
            w.add(p, -phase[t][2], -incident)
            for j, (a, b) in enumerate(pairs):
                if b == 7 and a < 5:
                    w.add(-phase[t][2], -choices[t][j])
            e = w.var(); early67.append(e)
            c = choices[t][pairs.index((6, 7))]
            w.add(-e, phase[t][0]); w.add(-e, c); w.add(e, -phase[t][0], -c)
        w.exactly_one(post)
        early = w.var(); w.equivalent_or(early, early67)
        for t in range(gates):
            w.add(-phase[t][2], -choices[t][pairs.index((5, 7))], early)
        if exact_maximum:
            for i, count in zip((3, 4, 5, 7, 8), (4, 4, 2, 4, 1)):
                w.at_most([neg(v) for v in events[1 << i, 511]], gates-count)
            kernel = [w.var() for _ in range(gates)]
            for t in range(gates):
                w.equivalent_or(kernel[t], [events[1 << i, 511][t] for i in (3, 4, 5, 7, 8)])
            w.at_most(kernel, 5); w.at_most([neg(v) for v in kernel], gates-5)
            if max_preparations is not None:
                assert max_preparations >= 0
                # All five maximum events are at or before the unique(7,8)
                # root. Root by gate5+p therefore covers at most p nongates
                # before completion, retaining every allowed interleaving.
                w.add(*[choices[t][pairs.index((7,8))]
                        for t in range(min(gates, 5 + max_preparations))])
        else:
            assert max_preparations is None
    if freeze:
        assert gates == len(freeze)
        for t, pair in enumerate(freeze):
            w.add(choices[t][pairs.index(tuple(pair))])
    return dict(reference_budget=16, witness_count=len(selected),
                pruning_sha256=hashlib.sha256((HERE / 'fixture.json').read_bytes()).hexdigest(),
                tight_cut=bool(tight and gates == 16),
                exact_maximum=bool(exact_maximum and tight and gates == 16),
                maximum_nonkernel_preparations=max_preparations,
                exact_maximum_dependency='Independent21-word cover in fixture.json/check_structure.py; committed7436 binary exclusions',
                filters='No selected depth, lexicographic, future-interval, repeated-pair or nonredundancy restriction')


def solve(path,conflicts,seconds):
    import pysat
    from pysat.solvers import Glucose4
    start=time.monotonic();meta=json.loads(path.with_suffix('.meta.json').read_text())
    result=dict(instance=str(path),solver='Glucose4 via python-sat',pysat=pysat.__version__,
                conflict_budget=conflicts,wall_budget_seconds=seconds,cnf_sha256=meta['cnf_sha256'])
    with Glucose4(with_proof=True,use_timer=True) as solver:
        with path.open() as stream:
            for line in stream:
                if line.strip() and line[:1] not in 'cp':solver.add_clause([int(v) for v in line.split()[:-1]])
        print(json.dumps(dict(stage='loaded',variables=solver.nof_vars(),clauses=solver.nof_clauses(),seconds=time.monotonic()-start)),flush=True)
        timer=threading.Timer(seconds,solver.interrupt);timer.start();solver.conf_budget(conflicts)
        try:status=solver.solve_limited(expect_interrupt=True)
        finally:timer.cancel();timer.join();solver.clear_interrupt()
        result['status']='SAT' if status is True else 'UNSAT_unchecked' if status is False else 'UNKNOWN'
        result.update(stats=solver.accum_stats(),solver_seconds=solver.time())
        if status is True:
            model=solver.get_model();positive={v for v in model if v>0}
            word=[meta['pairs'][next(j for j,v in enumerate(row) if v in positive)] for row in meta['choices']]
            replay(meta['wires'],meta['states'],word)
            result['network']=word;path.with_suffix('.model.json').write_text(json.dumps(model)+'\n')
        if status is False:
            proof=solver.get_proof();assert proof and proof[-1].strip()=='0'
            path.with_suffix('.drat').write_text('\n'.join(proof)+'\n')
            result['proof_sha256']=hashlib.sha256(path.with_suffix('.drat').read_bytes()).hexdigest()
    result.update(seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    path.with_suffix('.result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('command', choices=['generate', 'solve'])
    p.add_argument('--path', type=Path, required=True)
    p.add_argument('--gates', type=int, default=16)
    p.add_argument('--tight-cut', action='store_true')
    p.add_argument('--exact-maximum', action='store_true')
    p.add_argument('--max-preparations', type=int)
    p.add_argument('--freeze-control', action='store_true')
    p.add_argument('--conflicts', type=int, default=30000)
    p.add_argument('--seconds', type=float, default=40)
    a = p.parse_args()
    if a.command == 'generate':
        pruning = json.loads((HERE / 'fixture.json').read_text())
        freeze = pruning['control18'] if a.freeze_control else None
        gates = len(freeze) if freeze else a.gates
        meta = generate(9, pruning['states'], gates, a.path, commute=False, encode_sorted=True,
                        augment=lambda w, c, ps, bs: augment(w, c, ps, bs, pruning, gates, freeze, a.tight_cut or a.exact_maximum, a.exact_maximum, a.max_preparations))
        print(json.dumps({k: v for k, v in meta.items() if k not in ('choices', 'pairs', 'states')}), flush=True)
    else:
        solve(a.path, a.conflicts, a.seconds)


if __name__ == '__main__':
    main()
