"""Three serial fresh combined-reader runs; no old standalone replay."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); root = Path(__file__).resolve().parent
    if args.out.exists() or args.out.resolve().is_relative_to(root):
        raise ValueError('fresh reproduction directory outside source required')
    args.out.mkdir(parents=True)
    env = dict(os.environ)
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS'):
        env[key] = '1'
    seal = json.loads((root/'SOURCE.json').read_bytes())
    cold = args.out/'isolated-source'; cold.mkdir()
    for name in list(seal['files'])+['SOURCE.json']:
        shutil.copyfile(root/name, cold/name)
    records = []; originals = []
    for mode, source, options in [('normal', root, []), ('optimized', root, ['-O']),
                                  ('cold-isolated', cold, [])]:
        start = time.monotonic()
        p = subprocess.run([sys.executable, '-I', *options, str(source/'reader.py')],
                           env=env, capture_output=True, timeout=45)
        elapsed = time.monotonic()-start
        if p.returncode:
            raise ValueError('incomplete/failed '+mode+': '+p.stderr.decode())
        originals.append(p.stdout)
        (args.out/(mode+'.json')).write_bytes(p.stdout)
        records.append({'mode': mode, 'seconds': elapsed, 'bytes': len(p.stdout),
                        'SHA256': hashlib.sha256(p.stdout).hexdigest()})
        (args.out/'progress.json').write_text(json.dumps(records, indent=2)+'\n')
    if not all(value == originals[0] for value in originals):
        raise ValueError('ENTIRE combined math records disagree')
    expected = (root/'EXPECTED.json').read_bytes()
    if originals[0] != expected:
        raise ValueError('ENTIRE expected record differs')
    result = {'actual_agent': 'six-downset-3', 'role': 'researcher',
              'UTC': datetime.now(timezone.utc).isoformat(), 'runs': records,
              'whole_three_records_and_expected_equal': True,
              'peak_child_RSS_KiB': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'fixed_child_seconds': 45, 'serial_native_threads': 1,
              'old_standalone_or_original_candidate_PSD_checker_run': False,
              'source_snapshot_SHA256': hashlib.sha256((root/'SOURCE.json').read_bytes()).hexdigest(),
              'independent_review_or_formal_proof': False}
    (args.out/'RECEIPT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
