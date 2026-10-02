"""A bounded untrusted CaDiCaL proposal; only strict replay can prove UNSAT."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def require(ok, message):
    if not ok:
        raise ValueError(message)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('model', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--solver', required=True, type=Path)
    a = p.parse_args()
    require(not any(a.output.with_suffix(s).exists() for s in ['.json', '.drup', '.log']), 'fresh proposal paths')
    raw = a.model.read_bytes()
    d = json.loads(raw)
    require((d['model_kind'], d['field_prime'], d['row_half'], d['AP_length'],
             d['subgroup'], d['fixed_first_coset_row'], d['palette'], d['variables']) ==
            ('arbitrary_subgroup_antipodal_regular', 31, 10, 7, [1, 5, 25], 16, False, 100),
            'audited production family')
    cnf = a.model.with_suffix('.cnf')
    expected = (f"p cnf {d['variables']} {len(d['clauses'])}\n" +
                ''.join(' '.join(map(str, c)) + ' 0\n' for c in d['clauses'])).encode()
    require(cnf.read_bytes() == expected, 'whole DIMACS bytes')
    solver = a.solver.resolve()
    version = subprocess.run([str(solver), '--version'], capture_output=True, text=True,
                             timeout=5, check=True).stdout.strip()
    require(version == '1.9.5', 'recorded native version')
    env = dict(os.environ)
    for k in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
        env[k] = '1'
    trace = a.output.with_suffix('.drup')
    command = [str(solver), '--no-binary', '-c', '49900', '-t', '30', str(cnf), str(trace)]
    started = time.monotonic()
    native = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, env=env)
    timeout = False
    try:
        stdout, stderr = native.communicate(timeout=32)
    except subprocess.TimeoutExpired:
        timeout = True
        native.kill()
        stdout, stderr = native.communicate()
    a.output.with_suffix('.log').write_text(stdout + stderr)
    stats = {}
    for label in ['conflicts', 'decisions', 'propagations', 'restarts']:
        m = re.search(r'^c ' + label + r':\s*(\d+)', stdout, re.MULTILINE)
        stats[label] = int(m.group(1)) if m else None
    status = {0: 'UNKNOWN', 10: 'PARTIAL_SAT_PROPOSAL', 20: 'UNVERIFIED_UNSAT_PROPOSAL'}.get(
        native.returncode, 'INCOMPLETE_EXECUTION')
    if timeout:
        status = 'INCOMPLETE_TIMEOUT'
    elif stats['conflicts'] is None:
        status = 'INCOMPLETE_STATISTICS'
    elif stats['conflicts'] > 49900:
        status = 'BUDGET_OVERSHOOT'
    result = {'author': 'six-vdw-1', 'role': 'researcher', 'status': status,
              'native_returncode': native.returncode, 'statistics': stats,
              'requested_conflicts': 49900, 'actual_conflict_ceiling': 50000,
              'native_seconds_guard': 30, 'subprocess_seconds_guard': 32,
              'solver_version': version, 'solver_sha256': hashlib.sha256(solver.read_bytes()).hexdigest(),
              'model_sha256': hashlib.sha256(raw).hexdigest(),
              'cnf_sha256': hashlib.sha256(expected).hexdigest(),
              'elapsed_seconds': time.monotonic() - started,
              'proof_is_mathematical_exclusion': False}
    if status == 'UNVERIFIED_UNSAT_PROPOSAL':
        result['native_ascii_sha256'] = hashlib.sha256(trace.read_bytes()).hexdigest()
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps(result, sort_keys=True), flush=True)
    if status != 'UNVERIFIED_UNSAT_PROPOSAL':
        raise SystemExit(2)
