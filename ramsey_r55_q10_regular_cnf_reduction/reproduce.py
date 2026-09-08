#!/usr/bin/env python3
"""Run the literal implication audit and the complete h3959 replay.

Requires either existing frozen branch files or an empty directory for exact
byte reconstruction. No SAT solver, historical solver logs, or DRAT is used.
"""
import argparse
import hashlib
import json
import resource
import subprocess
import sys
import time
from pathlib import Path
from rebuild import verify_package

ROOT = Path(__file__).resolve().parent


def invoke(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode or result.stderr:
        raise ValueError('child failed: ' + result.stdout + result.stderr)
    return json.loads(result.stdout)


def residual(audited):
    inputs = json.loads((ROOT / 'INPUTS.json').read_text())
    historical = json.loads((ROOT / 'HISTORICAL_RESULT.json').read_text())
    history = {r['branch']: r for r in historical['branches']}
    rows = []
    for original, checked in zip(inputs['rows'], audited['files']):
        name = original['branch']
        if history[name]['cnf_sha256'] != checked['sha256'] or history[name]['outcome'] != 'UNKNOWN':
            raise ValueError('historical inventory mismatch')
        closed = checked['regular_endpoint_bridge'] is not None
        rows.append({'branch': name, 'filename': original['filename'], 'sha256': checked['sha256'],
                     'red_degree': original['red_degree'], 'blue_degree': original['blue_degree'],
                     'historical_solver_status': 'UNKNOWN',
                     'mathematical_status': 'THEOREM_CERTIFIED_UNSAT' if closed else 'UNKNOWN',
                     'decision_basis': 'checked literal CNF implication + h3959' if closed else None,
                     'retain_in_unresolved_queue': not closed})
    return {'status': 'CERTIFIED_TWO_OF_FOUR_FROZEN_Q10_REGULAR_CNFS_UNSAT',
            'task': inputs['task'], 'defined_inventory': 'the four final frozen even-regular CNF jobs',
            'before_unknown_jobs': 4, 'new_theorem_certified_unsat_jobs': 2,
            'remaining_unknown_jobs': 2, 'rows': rows,
            'previous_odd_degree_parity_exclusions': [19, 21, 23],
            'whole_q10_task_decided': False, 'target43_found': False,
            'new_solver_calls': 0, 'historical_solver_or_drat_verdicts_changed': False,
            'theorem_ref': json.loads((ROOT/'PROVENANCE.json').read_text())['theorem_ref'],
            'theorem_source_commit': json.loads((ROOT/'PROVENANCE.json').read_text())['theorem_commit'],
            'denominator_warning': '2/4 concerns this finite job inventory, not a fraction of all good43 graphs or all h3887 tasks'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--catalog', required=True, help='pinned complete r45_24.g6 input for h3959')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--branches', help='directory containing all four frozen CNFs')
    group.add_argument('--rebuild', help='empty output directory; reconstruct the same four CNFs')
    args = parser.parse_args()
    start = time.monotonic()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest:
            raise ValueError('source manifest: ' + name)
    dependencies = json.loads((ROOT/'DEPENDENCIES.json').read_text())
    paths = {r['directory']: verify_package(ROOT.parent, r) for r in dependencies}
    py = [sys.executable, '-B']
    if args.rebuild:
        rebuilt = invoke([*py, str(ROOT/'rebuild.py'), '--output', str(Path(args.rebuild).resolve())])
        if rebuilt != json.loads((ROOT/'EXPECTED_REBUILD.json').read_text()):
            raise ValueError('rebuild receipt mismatch')
    directory = str(Path(args.branches or args.rebuild).resolve())
    expected_audit = json.loads((ROOT/'EXPECTED_AUDIT.json').read_text())
    expected_controls = json.loads((ROOT/'EXPECTED_CONTROLS.json').read_text())
    for flag in ([], ['-O']):
        mode = [sys.executable, *flag, '-B']
        audited = invoke([*mode, str(ROOT/'audit.py'), '--branches', directory])
        if audited != expected_audit:
            raise ValueError('literal audit mismatch')
        if invoke([*mode, str(ROOT/'controls.py')]) != expected_controls:
            raise ValueError('control mismatch')
    theorem = invoke([*py, str(paths['ramsey_r55_regular18_overlap_exclusion']/'reproduce.py'),
                      '--catalog', str(Path(args.catalog).resolve())])
    if theorem['status'] != 'REPRODUCED_COMPLETE_REGULAR18_AND24_EXCLUSION':
        raise ValueError('h3959 theorem replay')
    reduction = residual(audited)
    if reduction != json.loads((ROOT/'REDUCTION.json').read_text()):
        raise ValueError('residual manifest mismatch')
    print(json.dumps({'status': reduction['status'], 'modes': ['normal', 'assertions_disabled'],
                      'reconstruction': bool(args.rebuild), 'theorem_replay': theorem['status'],
                      'remaining_unknown_branches': [r['branch'] for r in reduction['rows']
                                                     if r['retain_in_unresolved_queue']],
                      'reduction_sha256': hashlib.sha256((ROOT/'REDUCTION.json').read_bytes()).hexdigest(),
                      'new_solver_calls': 0, 'elapsed_seconds': time.monotonic()-start,
                      'max_child_rss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}, indent=2))


if __name__ == '__main__':
    main()
