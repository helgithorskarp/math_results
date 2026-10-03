"""Serial complete normal/-O replay, one bounded child per phase.

Generated records stay in a temporary directory. A timeout or failed
check stops this route without any mathematical nonexistence inference.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time

PHASES = ('mean', 'residual', 'joint', 'positive', 'positive23', 'uniform', 'damage')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    if args.receipt and args.receipt.exists():
        raise ValueError('Refusing to overwrite a validation receipt')
    here = Path(__file__).resolve().parent
    expected = json.loads((here/'RESULT.json').read_text())
    if set(expected) != set(PHASES):
        raise ValueError('Changed full mathematical phase coverage')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONPATH', None)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    modes, runs = [], []
    with tempfile.TemporaryDirectory(prefix='downset-core-six-') as temporary:
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            records = {}
            for phase in PHASES:
                output = Path(temporary)/(mode+'-'+phase+'.json')
                start = time.monotonic()
                try:
                    child = subprocess.run([sys.executable, *flags, str(here/'verify.py'),
                                            '--phase', phase, '--record', str(output)],
                                           cwd=here, env=env, capture_output=True, text=True, timeout=60)
                except subprocess.TimeoutExpired:
                    raise ValueError('Stopped at unchanged 60s child guard; no mathematical conclusion: '+phase)
                row = {'mode': mode, 'phase': phase, 'exit_code': child.returncode,
                       'seconds': round(time.monotonic()-start, 6),
                       'stdout': child.stdout, 'stderr': child.stderr}
                runs.append(row)
                if child.returncode:
                    raise ValueError(row)
                records[phase] = json.loads(output.read_text())
                if records[phase] != expected[phase]:
                    raise ValueError('Entire frozen mathematical phase differs: '+phase)
                print(json.dumps({'mode': mode, 'phase': phase, 'seconds': row['seconds'],
                                  'complete_frozen_phase_equal': True}), flush=True)
            modes.append(records)
    if modes[0] != modes[1] or modes[0] != expected:
        raise ValueError('ENTIRE normal/optimized/frozen mathematical records differ')
    negative = expected['mean']+expected['residual']
    positive = [expected['positive'], expected['positive23']]
    receipt = {'agent': 'six-downset-3', 'role': 'researcher', 'python': sys.version.split()[0],
               'entire_normal_optimized_frozen_records_agree': True,
               'record_sha256': hashlib.sha256(json.dumps(expected, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
               'phase_record_sha256': {p: hashlib.sha256(json.dumps(expected[p], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
                                       for p in PHASES},
               'runs': runs, 'peak_child_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'math_guard_seconds': 60, 'native_threads': 1, 'serial_math_jobs': True,
               'scope': 'unchanged1CPU2GiB',
               'all_original_negative_positions': sum(r['literal']['positions'] for r in negative)+expected['joint']['original_ordered_positions'],
               'all_original_positive_nonempty_positions': sum(r['literal']['positions'] for r in positive),
               'whole_positive_positions': sum(r['whole_positions'] for r in positive),
               'whole_unit_gaps': [r['whole_projected_unit_gap'] for r in positive],
               'unbounded_shifted_positive_coefficients': sum(r['coefficient_count'] for r in expected['uniform']['signs'].values()),
               'necessary_polynomial_terms': expected['uniform']['necessary_polynomial_count'],
               'semantic_damages': len(expected['damage']['semantic_damages_rejected']),
               'trust_boundary': 'ordinary infinite/complement/empty/rank/label bridges and credited premises unformalized; two algorithms by one author; independently unreviewed'}
    if args.receipt:
        args.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'runs'}, sort_keys=True), flush=True)


if __name__ == '__main__':
    main()
