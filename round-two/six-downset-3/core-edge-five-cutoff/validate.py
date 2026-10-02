"""Serial full normal/-O records under the same native-thread/time guards."""
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONPATH', None)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    records, runs = [], []
    with tempfile.TemporaryDirectory(prefix='downset-core-five-') as temporary:
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            output = Path(temporary)/(mode+'.json')
            start = time.monotonic()
            child = subprocess.run([sys.executable, *flags, str(here/'verify.py'), '--record', str(output)],
                                   cwd=here, env=env, capture_output=True, text=True, timeout=60)
            runs.append({'mode': mode, 'exit_code': child.returncode, 'seconds': round(time.monotonic()-start, 6),
                         'stdout': child.stdout, 'stderr': child.stderr})
            if child.returncode:
                raise ValueError(runs[-1])
            records.append(json.loads(output.read_text()))
    expected = json.loads((here/'RESULT.json').read_text())
    if records[0] != records[1] or records[0] != expected:
        raise ValueError('ENTIRE normal/optimized/frozen mathematical payloads differ')
    receipt = {'agent': 'six-downset-3', 'role': 'researcher', 'python': sys.version.split()[0],
               'entire_normal_optimized_frozen_records_agree': True,
               'record_sha256': hashlib.sha256(json.dumps(expected, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
               'runs': runs, 'peak_child_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               'math_guard_seconds': 60, 'native_threads': 1, 'serial_math_jobs': True, 'scope': 'unchanged1CPU2GiB',
               'negative_orders': len(expected['negative_cases']),
               'all_original_nonempty_positions': sum(x['literal']['positions'] for x in expected['negative_cases']+expected['new_positive_cases']),
               'all_original_weighted_entries': sum(x['literal']['weighted_entries'] for x in expected['negative_cases']+expected['new_positive_cases']),
               'whole_positive_positions': sum(x['whole_positions'] for x in expected['new_positive_cases']),
               'whole_unit_gaps': [x['whole_projected_unit_gap'] for x in expected['new_positive_cases']],
               'semantic_damages': len(expected['semantic_damages_rejected']),
               'trust_boundary': 'ordinary infinite/complement/empty/rank/label bridges unformalized; two PSD algorithms by one author; independently unreviewed'}
    if args.receipt:
        if args.receipt.exists():
            raise ValueError('Refusing to overwrite validation receipt')
        args.receipt.write_text(json.dumps(receipt, sort_keys=True, indent=2)+'\n')
    print(json.dumps(receipt, sort_keys=True))


if __name__ == '__main__':
    main()
