"""Rebuild and compare the whole exact record in two fresh processes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).resolve().parent
    expected = json.loads((root / 'expected.json').read_text())
    for name, wanted in expected['source_sha256'].items():
        require(hashlib.sha256((root / name).read_bytes()).hexdigest() == wanted,
                'Checked source changed: ' + name)
    env = os.environ.copy()
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'NUMEXPR_MAX_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    runs = []
    records = []
    for options in (['-B'], ['-O', '-B']):
        start = time.monotonic()
        result = subprocess.run([sys.executable, *options, str(root / 'check.py')],
                                cwd=root, env=env, capture_output=True, text=True,
                                timeout=20, check=True)
        record = json.loads(result.stdout)
        raw = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
        require(hashlib.sha256(raw).hexdigest() == expected['whole_record_sha256'],
                'Whole exact mathematical record changed')
        for name, value in expected['summary'].items():
            require(record[name] == value, 'Summary mismatch: ' + name)
        records.append(record)
        runs.append({'options': options, 'seconds': time.monotonic() - start,
                     'whole_record_sha256': hashlib.sha256(raw).hexdigest(),
                     'returncode': result.returncode})
    require(records[0] == records[1], 'Normal/optimized records differ')
    print(json.dumps({'agent': 'six-covering-2', 'role': 'researcher',
                      'runs': runs, 'full_records_equal': True,
                      'summary': expected['summary'],
                      'child_guard_seconds': 20, 'numerical_threads': 1,
                      'one_job_at_a_time': True}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
