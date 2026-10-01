"""Cold offline serial replay; expected data are never overwritten."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    here, work = Path(__file__).resolve().parent, args.work.resolve()
    if work == here or here in work.parents:
        raise ValueError('generated corpus must stay outside source directory')
    if work.exists() and any(work.iterdir()):
        raise ValueError('cold work directory must be empty')
    work.mkdir(parents=True, exist_ok=True)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'BLIS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
        os.environ[name] = '1'
    import controls
    import construction
    import upper
    from core import encoded
    started = time.monotonic()
    record = {'agent': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
              'controls': controls.audit(), 'construction': construction.audit(),
              'upper': upper.audit(work / 'upper')}
    record = json.loads(encoded(record))
    (work / 'RESULT.json').write_bytes(encoded(record))
    expected = json.loads((here / 'EXPECTED.json').read_text())
    if record != expected:
        raise ValueError('complete replay differs from frozen preceding evidence')
    validation = {'agent': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
                  'status': 'PASS_COLD_COMPLETE_REPLAY', 'optimized_python': bool(sys.flags.optimize),
                  'python': sys.version.split()[0], 'seconds': time.monotonic() - started,
                  'peak_RSS_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  'expected_sha256': hashlib.sha256((here / 'EXPECTED.json').read_bytes()).hexdigest(),
                  'threads': 1, 'solver': 'independent Python ordinary maximum clique; no author module executes'}
    (work / 'VALIDATION.json').write_text(json.dumps(validation, indent=2) + '\n')
    print(json.dumps(validation, sort_keys=True))

if __name__ == '__main__':
    main()
