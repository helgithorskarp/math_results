"""Regenerate the entire independent q4 audit record in serial exact phases."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
THREADS = ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS']

def regenerate():
    env = dict(os.environ)
    for name in THREADS:
        env[name] = '1'
    records = {}
    with tempfile.TemporaryDirectory(prefix='q4-review-', dir=ROOT) as scratch:
        for phase, source in [('symbolic', 'symbolic.py'),
                              ('original', 'original.py'), ('binding', 'bind.py')]:
            output = Path(scratch) / (phase + '.json')
            command = [sys.executable, '-B']
            if not __debug__:
                command.append('-O')
            command += [str(ROOT / source), '--output', str(output)]
            run = subprocess.run(command, env=env, capture_output=True, timeout=45)
            if run.returncode:
                raise RuntimeError(phase + ': ' + run.stderr.decode())
            records[phase] = json.loads(output.read_bytes())
    return (json.dumps(records, sort_keys=True, separators=(',', ':')) + '\n').encode()

def compare(actual, expected):
    # Compare EVERY mathematical byte; hashes are reporting, not acceptance.
    if actual != expected:
        raise ValueError('entire regenerated mathematical record differs')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    payload = regenerate()
    if args.check:
        compare(payload, args.check.read_bytes())
    if args.write:
        args.write.write_bytes(payload)
    print(json.dumps(dict(status='complete independent q4 original-space audit',
                          record_bytes=len(payload),
                          record_sha256=hashlib.sha256(payload).hexdigest(),
                          phases=3, signs=18, literal_h=[2, 3],
                          producer_code_used=False), sort_keys=True))

if __name__ == '__main__':
    main()
