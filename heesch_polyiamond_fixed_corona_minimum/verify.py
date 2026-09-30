"""Regenerate the exact CNF, audit local links, and independently check UNSAT."""
import argparse
from collections import Counter
import hashlib
import importlib.metadata
import itertools
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

for variable in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'

from encode import PUBLIC, build, link_clauses, wedges
from check import mesh, star, verify as verify_lower

BASE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def link_oracle(chosen):
    """Connectivity in the geometric edge-incidence graph, no cyclic bits."""
    if not chosen:
        return True
    unseen = set(chosen); stack = [unseen.pop()]
    while stack:
        triangle = stack.pop()
        for other in tuple(unseen):
            if len(set(triangle) & set(other)) == 2:
                unseen.remove(other); stack.append(other)
    return not unseen


def audit_links(cells, original, sixty, pockets):
    variables = {t: i for i, t in enumerate(cells, 1)}
    configurations = 0; flag_assignments = 0; original_angles = Counter()
    for v in sorted(sixty):
        ws = wedges(v); local = [variables.get(t) for t in ws]
        active = [i for i, t in enumerate(ws) if t in variables]
        constraints = link_clauses(local, sixty[v], pockets[v])
        for values in itertools.product((False, True), repeat=len(active)):
            assignment = {local[i]: value for i, value in zip(active, values)}
            chosen = {ws[i] for i, value in zip(active, values) if value}
            valid = link_oracle(chosen)
            for tip, pocket in itertools.product((False, True), repeat=2):
                model = {**assignment, sixty[v]: tip, pockets[v]: pocket}
                accepts = all(any(model[abs(lit)] == (lit > 0) for lit in c) for c in constraints)
                expected = valid and tip == (len(chosen) == 1) and pocket == (len(chosen) == 5)
                assert accepts == expected, (v, chosen, tip, pocket)
                flag_assignments += 1
            configurations += 1
        chosen = set(ws) & original
        assert link_oracle(chosen)
        if 0 < len(chosen) < 6:
            original_angles[60*len(chosen)] += 1
    geometric_angles = mesh(original)[0]['boundary_angles']
    assert dict(original_angles) == geometric_angles
    return {'local_configurations': configurations, 'flag_assignments': flag_assignments,
            'vertices': len(sixty), 'original_angles': dict(sorted(original_angles.items()))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--checker', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    a = ap.parse_args(); a.work.mkdir(parents=True, exist_ok=True)
    start = time.monotonic(); expected = json.loads((BASE/'expected.json').read_text())
    assert digest(PUBLIC/'tile.json') == expected['tile_sha256']
    assert digest(PUBLIC/'coronas.json') == expected['coronas_sha256']
    cells, original, placements, sixty, pockets, clauses, nv = build(214)
    audit = json.loads(json.dumps(audit_links(cells, original, sixty, pockets)))
    assert audit == expected['audit']
    text = f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)
    cnf = a.work/'minimum.cnf'; cnf.write_text(text)
    assert nv == expected['variables'] and len(clauses) == expected['clauses']
    assert len(cells) == expected['domain'] and len(placements) == expected['placements']
    assert digest(cnf) == expected['cnf_sha256']
    from pysat.solvers import Solver
    proof_file = a.work/'minimum.drat'
    with Solver(name='glucose4', bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(20000); result = solver.solve_limited()
        assert result is False, 'no UNSAT claim from SAT, UNKNOWN or an incomplete run'
        proof = '\n'.join(solver.get_proof())+'\n'; proof_file.write_text(proof)
        solver_stats = solver.accum_stats()
    checked = subprocess.run([str(a.checker.resolve()), str(cnf.resolve()), str(proof_file.resolve())],
                             capture_output=True, text=True, timeout=15)
    log = checked.stdout+checked.stderr; (a.work/'drat-check.txt').write_text(log)
    assert checked.returncode == 0 and 's VERIFIED' in log, log
    # This independent checker reads the published triangle mesh and poses,
    # without importing the CNF generator or symbolic marked model.
    attainment = json.loads(json.dumps(verify_lower(PUBLIC/'tile.json', PUBLIC/'coronas.json')))
    assert attainment == json.loads((PUBLIC/'expected.json').read_text())
    record = {'agent': 'six-heesch-2', 'role': 'researcher',
              'claim': 'minimum215 only in the fixed-corona halo positive-angle-surplus family',
              'domain': len(cells), 'placements': len(placements), 'variables': nv,
              'clauses': len(clauses), 'cnf_sha256': digest(cnf),
              'proof_sha256': digest(proof_file), 'proof_bytes': proof_file.stat().st_size,
              'independent_drat_check': 'VERIFIED', 'audit': audit,
              'attainment_cells': attainment['cells'], 'attainment_disc_coronas': 5,
              'python': sys.version.split()[0], 'python_sat': importlib.metadata.version('python-sat'),
              'solver': 'glucose4', 'solver_stats': solver_stats,
              'seconds': round(time.monotonic()-start, 3),
              'peak_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (a.work/'result.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    print(json.dumps(record, indent=2, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
