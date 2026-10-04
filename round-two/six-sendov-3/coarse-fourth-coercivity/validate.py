"""Bounded SERIAL normal/optimized, cold, damage and preimport verification."""
from pathlib import Path
import argparse
import hashlib
import json
import resource
import shutil
import subprocess
import sys
import tempfile
import time
import os

HERE = Path(__file__).resolve().parent
THREADS = ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS']
MATH_FILES = ['arithmetic.py', 'coercivity.py', 'verify.py', 'EXPECTED.json']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--summary', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    baseline = args.baseline.resolve()
    results = []
    env = dict(os.environ)
    env.update({name: '1' for name in THREADS})

    def run(label, directory, optimized=False, options=(), expected_reject=False):
        command = [sys.executable, '-B']+(['-O'] if optimized else [])+[
            str(directory/'verify.py'), '--baseline', str(baseline)]+list(options)
        start = time.monotonic()
        try:
            completed = subprocess.run(command, cwd=directory, env=env,
                                       capture_output=True, text=True, timeout=45)
        except subprocess.TimeoutExpired:
            raise RuntimeError('INCOMPLETE: fixed45s guard; no mathematical conclusion')
        (args.scratch/(label+'.stdout')).write_text(completed.stdout)
        (args.scratch/(label+'.stderr')).write_text(completed.stderr)
        seconds = time.monotonic()-start
        if expected_reject:
            if completed.returncode != 1 or 'REJECT:' not in completed.stderr:
                raise RuntimeError('missing intended rejection: '+label)
            if label.startswith('source-') and 'preimport source seal: coercivity.py' not in completed.stderr:
                raise RuntimeError('source damage was not stopped before mathematical import')
            if label.startswith('fixture-') and 'ENTIRE strict canonical expected record' not in completed.stderr:
                raise RuntimeError('fixture damage did not reach the whole-record gate: '+label)
            record = None
        else:
            if completed.returncode != 0:
                raise RuntimeError('positive verification failed: '+label+' '+completed.stderr)
            record = json.loads(completed.stdout)
            if record.get('complete') is not True:
                raise RuntimeError('positive verification incomplete: '+label)
        results.append({'label': label, 'optimized': optimized,
                        'intended_reject': expected_reject, 'exit_code': completed.returncode,
                        'seconds': seconds, 'whole_output': record})
        print(label, 'complete rejection' if expected_reject else 'complete verification', flush=True)

    with tempfile.TemporaryDirectory(prefix='coarse-fourth-', dir=args.scratch) as raw:
        cold = Path(raw)
        for line in (HERE/'SHA256SUMS').read_text().splitlines():
            _, name = line.split('  ', 1)
            shutil.copyfile(HERE/name, cold/name)
        shutil.copyfile(HERE/'SHA256SUMS', cold/'SHA256SUMS')
        for optimized in (False, True):
            suffix = 'O' if optimized else 'N'
            run('local-'+suffix, HERE, optimized)
            run('cold-'+suffix, cold, optimized)
            for damage in ('sixth_sign', 'missing_norm_payment', 'quadratic_skew_sign', 'frozen_moving_phi'):
                run('math-'+damage+'-'+suffix, HERE, optimized,
                    ('--damage', damage), True)
            for damage in ('normal_coefficient', 'dropped_phi_term', 'boolean_as_integer', 'sign_as_number'):
                run('fixture-'+damage+'-'+suffix, HERE, optimized,
                    ('--fixture-damage', damage), True)
            target = cold/'coercivity.py'
            original = target.read_bytes()
            target.write_bytes(original+b'\nraise RuntimeError("mathematical import occurred")\n')
            run('source-'+suffix, cold, optimized, expected_reject=True)
            target.write_bytes(original)
    summary = {'agent': 'six-sendov-3', 'role': 'researcher', 'complete': True,
               'python': sys.version.split()[0], 'math_source_hashes': {
                   name: hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in MATH_FILES},
               'native_threads': {name: '1' for name in THREADS},
               'maximum_simultaneous_mathematical_children': 1,
               'per_child_timeout_seconds': 45, 'positive_runs': 4,
               'intended_rejections': 18, 'all_cases': results,
               'peak_child_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'analytic_bridges_unformalized': True, 'independent_review': False}
    args.summary.write_text(json.dumps(summary, indent=2)+'\n')


if __name__ == '__main__':
    main()
