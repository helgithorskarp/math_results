#!/usr/bin/env python3
"""Bounded serial whole-record replays and specific mathematical damage controls.

The producer imports no expected record or predecessor.  This harness compares
entire independently produced JSON objects and, if requested, the full credited
review8955 tangent matrix.  It is validation, not independent analytic review.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
import time


def need(ok, label):
    if not ok:
        raise RuntimeError(label)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--scratch', type=Path, required=True)
    p.add_argument('--baseline', type=Path)
    args = p.parse_args()
    here = Path(__file__).resolve().parent
    scratch = args.scratch.resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    frozen_raw = (here/'EXPECTED.json').read_bytes()
    frozen = json.loads(frozen_raw)
    env = os.environ.copy()
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[key] = '1'
    rows = []

    def child(name, command, expected_error=None):
        start = time.monotonic()
        try:
            r = subprocess.run(command, capture_output=True, text=True, timeout=45, env=env,
                               cwd=scratch)
        except subprocess.TimeoutExpired:
            (scratch/'INCOMPLETE.json').write_text(json.dumps({'status':'incomplete timeout; no mathematical inference',
                'child':name, 'guard_seconds':45, 'completed_children':rows}, indent=2)+'\n')
            raise
        row = {'name':name, 'command':command, 'exit':r.returncode,
               'seconds':time.monotonic()-start, 'guard_seconds':45,
               'peak_child_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'stdout':r.stdout, 'stderr':r.stderr}
        (scratch/(name+'-run.json')).write_text(json.dumps(row, indent=2)+'\n')
        if expected_error is None:
            need(r.returncode == 0, 'successful producer child: '+name)
        else:
            need(r.returncode != 0 and 'CertificateError: '+expected_error in r.stderr,
                 'specific intended mathematical rejection: '+name)
            row['intended_error'] = expected_error
        rows.append(row)
        return row

    for name, options in [('local-normal', []), ('local-optimized', ['-O'])]:
        out = scratch/(name+'.json')
        child(name, [sys.executable, *options, str(here/'derive.py'), '--expected',
                     str(here/'EXPECTED.json'), '--output', str(out)])
        need(json.loads(out.read_bytes()) == frozen, 'entire regenerated record: '+name)
        need(out.read_bytes() == frozen_raw, 'canonical output bytes: '+name)
    with tempfile.TemporaryDirectory(prefix='source-only-', dir=scratch) as cold:
        cold = Path(cold)
        shutil.copy2(here/'derive.py', cold/'derive.py')
        need(sorted(x.name for x in cold.iterdir()) == ['derive.py'], 'cold source-only input')
        out = cold/'record.json'
        child('cold-isolated-optimized', [sys.executable, '-I', '-O', str(cold/'derive.py'),
                                         '--output', str(out)])
        need(json.loads(out.read_bytes()) == frozen, 'entire cold output record')
        need(out.read_bytes() == frozen_raw, 'canonical cold output bytes')
        shutil.copy2(out, scratch/'cold-isolated-optimized.json')
    damages = [
        ('drop-one-mean-column', 'whole sharp rank-one remainder'),
        ('reverse-multiplier-column', 'full-13 bordered Jacobian'),
        ('erase-level-row', 'full-13 bordered Jacobian'),
        ('omit-sixth-critical-cube', 'whole all-eight cubic moment'),
        ('wrong-real-reflection', 'all-12 signed-radius conjugation'),
    ]
    for damage, error in damages:
        child(damage, [sys.executable, '-O', str(here/'derive.py'), '--damage', damage], error)
    baseline = None
    if args.baseline:
        raw = args.baseline.read_bytes()
        previous = json.loads(raw)
        need(previous['agent'] == 'six-reviewer-1' and previous['tangent_axes_and_pairs'] == 78,
             'credited independent-review baseline identity')
        need(frozen['scaled_tangent_matrix'] == previous['tangent_matrix'],
             'all144 entries of the credited review8955 matrix')
        need(frozen['signs']['aT']['normal_form'] == previous['tangent_a'], 'credited transverse coefficient')
        baseline = {'source_commit':'af8744b970f35769564fba7cb7c53377281661ca',
                    'reader':'https://github.com/helgithorskarp/math_results/blob/af8744b970f35769564fba7cb7c53377281661ca/round-two/six-reviewer-1/analytic-minimizer-audit/expected.json',
                    'sha256':hashlib.sha256(raw).hexdigest(), 'whole_tangent_entries':144,
                    'entire_entries_compared_before_hash':True,
                    'meaning':'validation of the credited finite baseline, not new research or transfer of a review'}
    summary = {'schema':'exact-skew-germ-validation-v1', 'agent':'six-sendov-3', 'role':'researcher',
               'python':sys.version, 'libraries':'Python standard library only; fractions.Fraction',
               'whole_successful_replays':3, 'intended_optimized_mathematical_rejections':5,
               'all_complete_records_compared_before_hash':True,
               'record_bytes':len(frozen_raw), 'record_sha256':hashlib.sha256(frozen_raw).hexdigest(),
               'max_child_seconds':max(x['seconds'] for x in rows),
               'peak_child_kib':max(x['peak_child_kib'] for x in rows),
               'guard_seconds_per_child':45, 'native_threads':1, 'serial_math_children':1,
               'no_timeout_or_resource_hit':True, 'baseline':baseline,
               'child_seconds':{x['name']:x['seconds'] for x in rows},
               'trust_boundary':'Finite exact validation only. Ordinary global analytic proof is unformalized and independently unreviewed.'}
    (scratch/'VALIDATION.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
