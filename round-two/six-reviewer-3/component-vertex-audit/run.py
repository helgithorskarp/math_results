"""Rebuild every exact record serially in normal and optimized Python."""
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    expected = json.loads((root / 'RESULTS.json').read_text())['records']
    env = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[key] = '1'
    receipts, normal = [], {}
    for optimized in (False, True):
        for name, file in [('primary', 'check.py'), ('controls', 'controls.py'),
                           ('guards', 'guards.py')]:
            begin = time.monotonic()
            child = subprocess.run([sys.executable] + (['-O'] if optimized else []) + [file],
                                   cwd=root, env=env, capture_output=True, timeout=20)
            if child.returncode:
                raise RuntimeError(file + ': ' + child.stderr.decode())
            json.loads(child.stdout)
            digest = hashlib.sha256(child.stdout).hexdigest()
            if (len(child.stdout) != expected[name]['whole_stdout_bytes'] or
                    digest != expected[name]['whole_stdout_sha256']):
                raise ValueError('whole mathematical record mismatch: ' + name)
            if name in normal and normal[name] != child.stdout:
                raise ValueError('whole normal/optimized bytes differ: ' + name)
            normal[name] = child.stdout
            receipts.append({'name': name, 'optimized': optimized,
                             'whole_stdout_bytes': len(child.stdout),
                             'whole_stdout_sha256': digest,
                             'seconds': time.monotonic() - begin,
                             'cumulative_peak_child_KiB':
                             resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    print(json.dumps({'actual_agent': 'six-reviewer-3',
                      'role': 'independent mathematical reviewer',
                      'all_whole_records_verified': True, 'python': sys.version.split()[0],
                      'native_threads': 1, 'serial': True,
                      'fixed_child_guard_seconds': 20,
                      'successful_children': len(receipts), 'children': receipts},
                     sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
