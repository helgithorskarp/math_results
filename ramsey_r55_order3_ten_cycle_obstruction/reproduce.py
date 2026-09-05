#!/usr/bin/env python3
"""Reconstruct six formulas and reproduce the five certified exclusions.

Large formulas and proof traces are kept in the requested work directory,
which must be outside this Git repository. A timeout is never an exclusion.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def file_info(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return dict(bytes=path.stat().st_size, sha256=digest.hexdigest())


def run(args, log=None, expected_code=0, timeout=None):
    args = list(map(str, args))
    if log is None:
        process = subprocess.run(args, cwd=HERE, timeout=timeout,
                                 env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    else:
        with log.open('w') as output:
            process = subprocess.run(args, cwd=HERE, stdout=output,
                                     stderr=subprocess.STDOUT, timeout=timeout)
    if process.returncode != expected_code:
        raise RuntimeError(f'Expected exit {expected_code}, got {process.returncode}: {args}; log={log}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--kissat', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    if work == HERE.parent or HERE.parent in work.parents:
        parser.error('generated formulas and traces must be outside the repository')
    work.mkdir(parents=True, exist_ok=True)
    kissat, drat = args.kissat.resolve(), args.drat_trim.resolve()
    version = subprocess.check_output([str(kissat), '--version'], text=True).strip()
    if version != '4.0.4':
        raise RuntimeError(f'Tested Kissat version is 4.0.4; supplied {version}')
    expected = json.loads((HERE/'result.json').read_text())
    if [c['red_cycles'] for c in expected['cases']] != list(range(6)):
        raise ValueError('Expected complete internal-color case coverage')
    if [c['red_cycles'] for c in expected['cases'] if c['status'] == 'excluded'] != [0,1,2,3,5]:
        raise ValueError('Expected exactly five claimed exclusions; r=4 stays open')
    report = dict(kissat_version=version, kissat=file_info(kissat),
                  drat_trim=file_info(drat), cases=[], complete=False,
                  all_cases_excluded=False)
    run([sys.executable, HERE/'audit.py'])
    checker = work/'check_formula'
    run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror',
         HERE/'check_formula.cpp', '-o', checker])
    for case in expected['cases']:
        r = case['red_cycles']
        full, proof = work/f'full_r{r}.cnf', work/f'full_r{r}.drat'
        print(f'CASE r={r}: generating and reconstructing all five-sets', flush=True)
        run([sys.executable, HERE/'generate.py', '--red-cycles', r, '--output', full])
        if file_info(full) != case['formula']:
            raise ValueError(f'Canonical formula mismatch for r={r}')
        run([checker, r, full])
        if case['status'] == 'unresolved':
            report['cases'].append(dict(red_cycles=r, formula=file_info(full),
                                       formula_audited=True, proof_verified=False,
                                       status='unresolved'))
            (work/'reproduction.json').write_text(json.dumps(report, indent=2)+'\n')
            print(f'CASE r={r}: formula audited; no exclusion claimed', flush=True)
            continue
        print(f'CASE r={r}: solving with a 180-second solver limit', flush=True)
        start = time.monotonic()
        solve_log = work/f'full_r{r}.solve.log'
        run([kissat, '--time=180', full, proof], solve_log, expected_code=20, timeout=360)
        if 's UNSATISFIABLE' not in solve_log.read_text():
            raise ValueError('solver did not report UNSAT')
        solve_seconds = time.monotonic()-start
        print(f'CASE r={r}: replaying the proof', flush=True)
        start = time.monotonic()
        replay_log = work/f'full_r{r}.replay.log'
        run([drat, full, proof, '-t', 240], replay_log, timeout=360)
        if 's VERIFIED' not in replay_log.read_text():
            raise ValueError('proof checker did not verify the trace')
        row = dict(red_cycles=r, variables=case['variables'], clauses=case['clauses'],
                   formula=file_info(full), proof=file_info(proof),
                   proof_matches_reference=file_info(proof) == case['reference_drat'],
                   solve_seconds=solve_seconds, replay_seconds=time.monotonic()-start,
                   formula_audited=True, proof_verified=True, status='excluded')
        report['cases'].append(row)
        (work/'reproduction.json').write_text(json.dumps(report, indent=2)+'\n')
        print(f'CASE r={r}: VERIFIED; reference proof hash match={row["proof_matches_reference"]}', flush=True)
    report['complete'] = True
    (work/'reproduction.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS: ten-cycle red counts 0,1,2,3,5 excluded; r=4 remains open')


if __name__ == '__main__':
    main()
