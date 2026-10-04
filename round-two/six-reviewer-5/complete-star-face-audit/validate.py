"""Full-record serial replays and nine independent semantic damage gates."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import time


def need(p, label):
    if not p:
        raise ValueError(label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True, type=Path)
    arg = parser.parse_args()
    root = Path(__file__).resolve().parent
    record = (root/'RECORD.json').read_bytes()
    environment = dict(os.environ)
    for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        environment[name] = '1'
    receipt = {'interpreter': sys.version, 'native_threads': 1, 'serial_children': 1,
               'guard_seconds_per_child': 45, 'positive_children': [], 'controls': []}
    controls = ('force-small-stars', 'drop-empty-row', 'omit-complements',
                'omit-empty-metric', 'naive-cap', 'omit-upper-pair-sum',
                'alter-seed-empty-loop', 'missing-swap-factor', 'wrong-weighted-degree')
    with tempfile.TemporaryDirectory(prefix='complete-face-independent-') as tmp:
        tmp = Path(tmp)
        def run(mode, damage=''):
            output = tmp/'whole-record.json'
            command = [sys.executable, '-I', '-B']+(['-O'] if mode == 'optimized' else [])
            command += [str(root/'check.py'), '--out', str(output)]
            if damage:
                command += ['--damage', damage]
            start = time.monotonic()
            child = subprocess.run(command, env=environment, capture_output=True, timeout=45)
            row = {'mode': mode, 'exit_code': child.returncode,
                   'seconds': time.monotonic()-start,
                   'peak_child_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
            return child, row, output
        for mode in ('normal', 'optimized', 'cold'):
            child, row, output = run(mode)
            need(child.returncode == 0, child.stderr.decode())
            need(output.read_bytes() == record, 'whole independent record differs')
            row.update(record_bytes=len(record), record_sha256=hashlib.sha256(record).hexdigest())
            receipt['positive_children'].append(row)
        for mode in ('normal', 'optimized'):
            for damage in controls:
                child, row, unused = run(mode, damage)
                need(child.returncode != 0 and b'ValueError' in child.stderr,
                     'semantic damage did not reject: '+damage)
                row.update(name=damage, rejected=True,
                           failure=child.stderr.decode().strip().splitlines()[-1])
                receipt['controls'].append(row)
    arg.out.write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'positive': 3, 'rejections': len(receipt['controls']),
                      'record_sha256': hashlib.sha256(record).hexdigest()}))


if __name__ == '__main__':
    main()
