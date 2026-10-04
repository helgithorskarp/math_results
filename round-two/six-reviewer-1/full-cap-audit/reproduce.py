"""Serial exact replays and six equation-level rejection controls."""
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('output', type=Path)
    args = p.parse_args()
    source = Path(__file__).resolve().with_name('check.py')
    if args.output.exists():
        raise ValueError('output directory already exists')
    args.output.mkdir(parents=True)
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        env[key] = '1'
    rows = []
    reference = None
    for cold in (False, True):
        for optimized in (False, True):
            with tempfile.TemporaryDirectory() as d:
                folder = Path(d)
                target = folder/'check.py' if cold else source
                if cold:
                    shutil.copyfile(source, target)
                record = folder/'record.json'
                cmd = [sys.executable, '-B']+(['-O'] if optimized else [])
                cmd += [str(target), '--output', str(record)]
                begin = time.monotonic()
                r = subprocess.run(cmd, env=env, cwd=folder, capture_output=True, timeout=45)
                if r.returncode:
                    raise ValueError(r.stderr.decode())
                raw = record.read_bytes()
                if reference is None:
                    reference = raw
                    (args.output/'record.json').write_bytes(raw)
                if raw != reference:
                    raise ValueError('complete replay bytes differ')
                rows.append({'cold_source_only': cold, 'optimized': optimized,
                             'seconds': round(time.monotonic()-begin, 6),
                             'whole_record_sha256': hashlib.sha256(raw).hexdigest(),
                             'whole_record_bytes': len(raw), 'exit': r.returncode})
    gates = {'transverse-sign': 'transverse imaginary coefficient',
             'weight': 'positive dual first response',
             'missing-coordinate': 'imaginary inverse coordinate',
             'mean-square': 'entire twelve-coordinate finite cost',
             'cubic-factor': 'physical cubic first variation',
             'slack-sign': 'entire third-response dual real 0'}
    rejected = []
    for fault, gate in gates.items():
        for optimized in (False, True):
            cmd = [sys.executable, '-B']+(['-O'] if optimized else [])
            cmd += [str(source), '--fault', fault]
            r = subprocess.run(cmd, env=env, capture_output=True, timeout=45)
            expected = ('ValueError: '+gate+'\n').encode()
            if r.returncode != 1 or not r.stderr.endswith(expected):
                raise ValueError('specified mathematical fault did not fail its equation: '+fault)
            rejected.append({'fault': fault, 'gate': gate, 'optimized': optimized, 'exit': 1})
    result = {'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
              'python': sys.version, 'standard_library_only': True,
              'serial_children': True, 'native_threads': 1, 'child_timeout_seconds': 45,
              'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'entire_record_bytes': len(reference),
              'entire_record_sha256': hashlib.sha256(reference).hexdigest(),
              'record_count': json.loads(reference)['record_count'],
              'whole_cost_monomials': json.loads(reference)['whole_cost_monomials'],
              'maximum_child_peak_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'complete_replays': rows, 'equation_rejections': rejected}
    (args.output/'validation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
