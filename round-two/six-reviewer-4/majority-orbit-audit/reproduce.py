"""Fresh, serial normal/-O reconstruction with complete record comparison."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from pathlib import Path

SOURCE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(command):
    environment = dict(os.environ)
    for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        environment[key] = '1'
    result = subprocess.run(command, cwd=SOURCE, env=environment, capture_output=True,
                            text=True, timeout=20)
    need(result.returncode == 0, result.stderr or result.stdout)
    return result.stdout


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    work = args.work.resolve()
    need(SOURCE not in work.parents and SOURCE != work, 'work must be outside source')
    work.mkdir(parents=True, exist_ok=True)
    need(not any(work.iterdir()), 'work must initially be empty')
    expected = json.loads((SOURCE / 'expected.json').read_text())
    started = time.monotonic()
    outputs = []
    for optimized in (False, True):
        mode = 'optimized' if optimized else 'normal'
        base = [sys.executable] + (['-O'] if optimized else [])
        cert = work / (mode + '.csv')
        run(base + [str(SOURCE / 'construct.py'), str(cert)])
        need(cert.read_bytes() == (SOURCE / 'certificate.csv').read_bytes(), 'entire generated certificate')
        record = work / (mode + '.json')
        summary = json.loads(run(base + [str(SOURCE / 'independent.py'), str(cert), '--record', str(record)]))
        need(summary == expected['summary'], 'entire independent summary')
        need(hashlib.sha256(record.read_bytes()).hexdigest() == expected['entire_record_sha256'],
             'entire mathematical record')
        controls = json.loads(run(base + [str(SOURCE / 'controls.py'), str(cert)]))
        need(controls == expected['controls'], 'all semantic controls')
        outputs.append((record.read_bytes(), controls))
    need(outputs[0] == outputs[1], 'entire normal/-O record and controls')
    need(hashlib.sha256((SOURCE / 'certificate.csv').read_bytes()).hexdigest() == expected['certificate_sha256'],
         'certificate checksum')
    print(json.dumps({'status': 'FRESH_COMPLETE_INDEPENDENT_MAJORITY_AUDIT',
                      'elapsed_seconds': time.monotonic() - started,
                      'child_peak_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                      'summary': expected['summary'], 'controls': len(expected['controls']['labels']),
                      'entire_record_sha256': expected['entire_record_sha256']}, sort_keys=True))
