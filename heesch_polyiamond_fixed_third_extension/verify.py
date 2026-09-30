"""Definition-level geometry and cold native/DRAT certificate replay."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time

from shared import BASE, PARENT, g, footprint, vertices, masks, star, write, parent_patterns
from generate import inputs, inventory, seed_formula, fourth


def geometry():
    shape, fixture, fixed, cases = inputs()
    inv = inventory(shape, fixed)
    candidates = inv[0]
    assert inv[-1]['candidates'] == 6208
    hole = json.loads((BASE / 'hole.json').read_text())
    checked = parent_patterns.check(shape, hole)
    assert checked == {'verified': True, 'hole_area_units': 2, 'copies': 2}
    occupied = set().union(*(footprint(shape, q) for q in fixed))
    halo = set(inv[2])
    rows = []
    for case in cases:
        poses = fourth(fixed, candidates, case)
        union = set()
        for q in poses:
            f = footprint(shape, q)
            assert len(f) == 214 and union.isdisjoint(f)
            union.update(f)
        assert halo <= union
        triangles = {vertices(t) for t in union}
        assert all(g.star(v) <= triangles for v in masks(occupied))
        mesh, _v, _polygon = g.mesh(triangles)
        assert mesh['chi'] == 1
        prior_vertices = {g.point(v, q) for q in fixed if q['level'] == 3 for t in shape for v in t}
        assert all(prior_vertices & {g.point(v, q) for t in shape for v in t} for q in poses[len(fixed):])
        encoded = json.dumps(sorted(union), separators=(',', ':')) + '\n'
        digest = hashlib.sha256(encoded.encode()).hexdigest()
        rows.append({'name': case['name'], 'copies': len(poses), 'mesh': mesh, 'union_sha256': digest})
    original = [q for q in fixture if q['level'] <= 4]
    assert {g.key(q) for q in fourth(fixed, candidates, cases[0])} == {g.key(q) for q in original}
    assert len({r['union_sha256'] for r in rows}) == 4
    return {'inventory': inv[-1], 'hole': checked, 'fourth_prefixes': rows}


def formula(case_name, work, checker):
    shape, fixture, fixed, cases = inputs()
    third_inventory = inventory(shape, fixed)
    if case_name == 'final':
        inv = third_inventory
        clauses, report = seed_formula(fixed, inv)
        # Each cut is justified by a strict-continuation lemma, not by
        # rejecting an untested model. Original imports the parent lemma.
        clauses.extend([[-j for j in row['selected_indices']] for row in cases])
        report['certified_continuation_nogoods'] = len(cases)
    else:
        row = next(c for c in cases if c['name'] == case_name)
        fixed = fourth(fixed, third_inventory[0], row)
        del third_inventory
        inv = inventory(shape, fixed)
        clauses, report = seed_formula(fixed, inv)
        report['certified_continuation_nogoods'] = 0
    nv = len(inv[0])
    path = work / 'instance.cnf'
    with path.open('w') as handle:
        handle.write(f'p cnf {nv} {len(clauses)}\n')
        for clause in clauses:
            handle.write(' '.join(map(str, clause)) + ' 0\n')
    report.update({'case': case_name, 'variables': nv, 'clauses': len(clauses),
                   'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    write(work / 'pre-solver.json', report)
    from pysat.solvers import Solver
    with Solver(name='glucose4', bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(20000)
        status = solver.solve_limited()
        if status is None:
            raise RuntimeError('UNKNOWN at native guard; no mathematical exclusion')
        assert status is False, 'not refuted; no mathematical exclusion'
        proof = '\n'.join(solver.get_proof()) + '\n'
        report['solver_stats'] = solver.accum_stats()
    trace = work / 'proof.drat'
    trace.write_text(proof)
    result = subprocess.run([str(checker.resolve()), str(path.resolve()), str(trace.resolve())],
                            capture_output=True, text=True, timeout=10)
    log = result.stdout + result.stderr
    (work / 'drat-check.txt').write_text(log)
    assert result.returncode == 0 and 's VERIFIED' in log, (result.returncode, log)
    report.update({'proof_bytes': len(proof.encode()), 'proof_sha256': hashlib.sha256(proof.encode()).hexdigest(),
                   'checker_returncode': result.returncode, 'status': 'UNSAT; independently DRAT-verified'})
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--phase', choices=('geometry', 'formula'), required=True)
    ap.add_argument('--case', choices=('A', 'B', 'C', 'final'))
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--checker', type=Path)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    if args.phase == 'geometry':
        scope = 'geometry'
        report = geometry()
    else:
        assert args.case and args.checker and args.checker.is_file()
        scope = args.case
        report = formula(args.case, args.work, args.checker)
    # Compare the canonical JSON schema, including integer mesh-angle keys.
    report = json.loads(json.dumps(report))
    expected = json.loads((BASE / 'expected.json').read_text())
    for key, value in expected.get(scope, {}).items():
        assert report[key] == value, (scope, key, report[key], value)
    report.update({'agent': 'six-heesch-2', 'role': 'researcher',
                   'seconds': round(time.monotonic() - start, 3),
                   'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
    write(args.work / (scope + '-result.json'), report)
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
