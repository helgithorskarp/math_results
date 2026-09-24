#!/usr/bin/env python3
"""Regenerate CNF, obtain DRAT, and check both DRAT and translated LRAT."""
import argparse
import hashlib
import json
import platform
import subprocess
import time
from pathlib import Path
import pysat
from pysat.solvers import Solver
from cases import enumerate_cases
from encoding import build
from strict_rup import check as check_lrat


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def run_checker(command, path, success):
    result = subprocess.run(command, capture_output=True, text=True, timeout=600)
    path.write_text(result.stdout + result.stderr)
    if result.returncode or success not in [line.strip() for line in result.stdout.splitlines()]:
        raise RuntimeError(f'Checker failed: {command}; inspect {path}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True, help='Outside the source checkout')
    ap.add_argument('--drat-trim', type=Path, required=True)
    ap.add_argument('--case', help='Optional single case ID')
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    cases = enumerate_cases()
    if args.case:
        cases = [c for c in cases if c['id'] == args.case]
        if not cases:
            raise ValueError('Unknown case ID')
    summary = {'python': platform.python_version(), 'python_sat': pysat.__version__,
               'solver': 'Glucose 4.1 (python-sat glucose4)',
               'lrat_checker': 'strict_rup.py (RUP-only; rejects RAT)',
               'case_count': len(cases), 'cases': []}
    for case in cases:
        start = time.monotonic()
        stem = args.work / case['id']
        cnf, drat, lrat = [stem.with_suffix(s) for s in ('.cnf', '.drat', '.lrat')]
        model = build(case['edges'])
        with cnf.open('w') as f:
            f.write(f'p cnf {model.pool.top} {len(model.clauses)}\n')
            for clause in model.clauses:
                f.write(' '.join(map(str, clause)) + ' 0\n')
        with Solver(name='glucose4', bootstrap_with=model.clauses, with_proof=True) as solver:
            if solver.solve() is not False:
                raise RuntimeError(f'{case["id"]}: exclusion failed')
            proof = solver.get_proof()
            if not proof or proof[-1] != '0':
                # Glucose can detect an initial unit-propagation conflict
                # while bootstrapping and emit no trace. An empty-clause
                # RUP step is valid precisely when the checker confirms it.
                proof.append('0')
            drat.write_text('\n'.join(proof) + '\n')
            stats = solver.accum_stats()
        run_checker([str(args.drat_trim.resolve()), str(cnf), str(drat), '-L', str(lrat)],
                    stem.with_suffix('.drat.log'), 's VERIFIED')
        lrat_result = check_lrat(cnf, lrat)
        stem.with_suffix('.strict.log').write_text(json.dumps(lrat_result,sort_keys=True)+'\n')
        record = {**case, 'variables': model.pool.top, 'clauses': len(model.clauses),
                  'cnf_sha256': digest(cnf), 'drat_sha256': digest(drat),
                  'lrat_sha256': digest(lrat), 'drat_bytes': drat.stat().st_size,
                  'lrat_bytes': lrat.stat().st_size,
                  'drat_verified': True, 'lrat_verified': True,
                  'strict_rup': lrat_result,
                  'conflicts': stats['conflicts'], 'seconds': round(time.monotonic()-start, 6)}
        summary['cases'].append(record)
        (args.work / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        print(json.dumps(record), flush=True)
    if not args.case:
        assert len(summary['cases']) == 25
    print(f'All {len(cases)} cases have checked DRAT and LRAT certificates.', flush=True)


if __name__ == '__main__':
    main()
