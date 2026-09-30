"""Bounded replay: lower, oracle, pair slices, and deficit certificate.

All negative answers require a cold independently checked DRAT trace. A cached
status alone is never accepted. Generated data must stay outside this source.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time

import geometry as g
from encode import selector, saturation, text_cnf


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def unit_conflict(clauses):
    assigned = set()
    while True:
        changed = False
        for c in clauses:
            if any(v in assigned for v in c):
                continue
            rest = [v for v in c if -v not in assigned]
            if not rest:
                return True
            if len(rest) == 1:
                assigned.add(rest[0]); changed = True
        if not changed:
            return False


def check_trace(folder, checker, expected, clauses=None):
    cnf = (folder / 'instance.cnf').read_bytes()
    assert sha(cnf) == expected['cnf_sha256']
    proof = folder / 'proof.drat'
    assert proof.exists()
    run = subprocess.run([str(checker.resolve()), str((folder / 'instance.cnf').resolve()),
                          str(proof.resolve())], capture_output=True, text=True, timeout=10)
    log = run.stdout + run.stderr
    if run.returncode == 1 and 'c trivial UNSAT' in log:
        if clauses is None:
            lines = cnf.decode().splitlines()
            clauses = [list(map(int, line.split()))[:-1] for line in lines if not line.startswith(('p', 'c'))]
        assert unit_conflict(clauses)
    assert 's VERIFIED' in log and (run.returncode == 0 or
           run.returncode == 1 and 'c trivial UNSAT' in log)
    (folder / 'drat-check.txt').write_text(log)
    return {'status': 'UNSAT; independently DRAT-verified',
            'cnf_sha256': sha(cnf), 'proof_sha256': sha(proof.read_bytes()),
            'proof_bytes': proof.stat().st_size}


def negative(clauses, nv, folder, checker, expected):
    from pysat.solvers import Solver
    folder.mkdir(exist_ok=True)
    cnf = text_cnf(nv, clauses)
    actual = {'variables': nv, 'clauses': len(clauses), 'cnf_sha256': sha(cnf.encode())}
    assert actual == {k: expected[k] for k in actual}, actual
    (folder / 'instance.cnf').write_text(cnf)
    with Solver(name='glucose4', bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(20000)
        decision = solver.solve_limited()
        assert decision is False, 'SAT or UNKNOWN gives no exclusion'
        proof = '\n'.join(solver.get_proof()) + '\n'
        (folder / 'proof.drat').write_text(proof)
        actual['solver_stats'] = solver.accum_stats()
    actual.update(check_trace(folder, checker, expected, clauses))
    write(folder / 'result.json', actual)
    return actual


def lower(shape, poses):
    _, vertices, _ = g.mesh(shape)
    diameter = max(max(f(v) for v in vertices)-min(f(v) for v in vertices)
                   for f in (lambda v: v[0], lambda v: v[1], lambda v: v[0]+v[1]))
    used = set(); layers = [set() for _ in range(6)]; copies = []; counts = [0]*6
    for p in poses:
        k = p['level']; assert type(k) is int and 0 <= k <= 5
        g.check.isometry(p['matrix'])
        assert all(type(x) is int for x in p['translation'])
        f = {g.move(t, p) for t in shape}
        assert all(g.cell(t) == t for t in f)
        assert len(f) == 214 and used.isdisjoint(f)
        if k == 0:
            assert g.key(p) == g.key(g.IDENTITY)
        used.update(f); layers[k].update(f); copies.append((k, f)); counts[k] += 1
    assert counts == [1, 5, 11, 23, 39, 52]
    rows = []; prefixes = []; current = set()
    for k in range(6):
        current = current | layers[k]; prefixes.append(current)
        stats, vs, _ = g.mesh(current)
        if k < 5:
            assert all(g.star(v) <= current | layers[k+1] for v in vs)
        rows.append({'level': k, 'cells': stats['cells'], 'chi': stats['chi'],
                     'layer_copies': counts[k], 'cumulative_copies': sum(counts[:k+1])})
    for k, f in copies:
        if k:
            assert {v for t in f for v in t} & {v for t in layers[k-1] for v in t}
    assert g.mesh(shape)[0]['boundary_angles'] == {60: 11, 120: 25, 180: 3, 240: 25, 300: 8}
    assert diameter == 24
    return {'cells': 214, 'diameter_bound': diameter, 'prefixes': rows}


def arithmetic():
    supplies = 8
    multiplicity = supplies + 1           # eight distinct recipients plus self
    assert supplies*multiplicity == 72
    assert 214 < 16*24**2
    fails = lambda k: 214*73**k > 16*24**2*(k+1)**2*72**k
    assert not fails(1314) and fails(1315)
    assert 73*145**2 > 72*146**2           # ratio increases for k>=144
    return {'assignment_multiplicity_bound': 9, 'growth_ratio': [73, 72],
            'first_area_contradiction_depth': 1315, 'finite_upper': 1316,
            'depth_slack': 2}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--phase', choices=('lower', 'oracle', 'pairs', 'deficit'), required=True)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--checker', type=Path)
    ap.add_argument('--start', type=int, default=0)
    ap.add_argument('--stop', type=int)
    a = ap.parse_args(); start = time.monotonic()
    work = a.work.resolve()
    assert not work.is_relative_to(g.BASE), 'generated data must stay outside source'
    work.mkdir(parents=True, exist_ok=True)
    expected = json.loads((g.BASE / 'expected.json').read_text())
    shape, poses = g.inputs()
    if a.phase == 'lower':
        result = {'lower': lower(shape, poses), 'arithmetic': arithmetic()}
        assert result == {k: expected[k] for k in result}
    elif a.phase == 'oracle':
        import oracle
        result = oracle.run()
        assert result == expected['oracle']
    else:
        assert a.checker and a.checker.is_file(), 'independent DRAT checker required'
        _, tips, corners, raw, wide = g.catalogues(shape)
        allowed = set(expected['retained_indices'])
        excluded = [r['attachment'] for r in expected['pair_negatives']]
        assert allowed.isdisjoint(excluded) and allowed | set(excluded) == set(range(1, 60))
        if a.phase == 'pairs':
            stop = a.stop if a.stop is not None else min(a.start+12, len(excluded))
            assert 0 <= a.start < stop <= len(excluded)
            result = {'pair_negatives_checked': []}
            for row in expected['pair_negatives'][a.start:stop]:
                i = row['attachment']
                ps, _, _, _, clauses = g.complete(shape, corners, wide, [g.IDENTITY, raw[i-1]])
                record = negative(clauses, len(ps), work / f'pair-{i:02d}', a.checker, row)
                result['pair_negatives_checked'].append(i)
                print(json.dumps({'attachment': i, 'variables': len(ps), 'clauses': len(clauses),
                                  'status': record['status']}), flush=True)
        else:
            # Recheck all prerequisite trace bytes. Cached JSON statuses are not axioms.
            for row in expected['pair_negatives']:
                check_trace(work / f'pair-{row["attachment"]:02d}', a.checker, row)
            providers, _, _, outer, nv = selector(shape, tips, raw, allowed, 8)
            _, _, _, capacity, capnv = selector(shape, tips, raw, allowed, 9)
            negative(capacity, capnv, work / 'capacity-nine', a.checker, expected['capacity_nine'])
            outercuts = []
            for case in expected['saturation_cases']:
                selected = case['providers']
                fixed = [g.IDENTITY, *(providers[i-1] for i in selected)]
                label = '-'.join(map(str, selected))
                folder = work / ('saturation-' + label); folder.mkdir(exist_ok=True)
                incoming, feet, occupied, inner, innv, coverings = saturation(shape, tips, raw, allowed, fixed)
                cuts = []
                for j, deep in enumerate(case['deep_negatives']):
                    chosen = deep['selected_providers']
                    assert chosen == sorted(set(chosen)) and all(1 <= i <= len(incoming) for i in chosen)
                    union = set(occupied)
                    for i in chosen:
                        assert union.isdisjoint(feet[i-1]); union.update(feet[i-1])
                    counts = [sum(auto or bool(c & set(chosen)) for auto, c in row) for row in coverings]
                    assert min(counts) >= 8
                    allfixed = fixed + [incoming[i-1] for i in chosen]
                    ps, _, _, _, clauses = g.complete(shape, corners, wide, allfixed)
                    negative(clauses, len(ps), folder / f'deep-{j:02d}', a.checker, deep)
                    cuts.append([-i for i in chosen])
                negative(inner + cuts, innv, folder / 'final', a.checker, case['final'])
                outercuts.append([-i for i in selected])
                print(json.dumps({'saturated_providers': selected, 'deep_cuts': len(cuts),
                                  'status': 'checked forced deficit'}), flush=True)
            record = negative(outer + outercuts, nv, work / 'forced-deficit-final',
                              a.checker, expected['forced_deficit_final'])
            result = {'capacity_at_most': 8, 'forced_deficit_cases': len(outercuts),
                      'forced_deficit_final': record, 'arithmetic': arithmetic()}
    result.update(agent='six-heesch-2', role='researcher', phase=a.phase,
                  seconds=round(time.monotonic()-start, 3),
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    write(work / (a.phase + '-result.json'), result)
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
