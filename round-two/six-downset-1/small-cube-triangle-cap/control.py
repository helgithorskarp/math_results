"""New bounded original controls; no parent executable/certificate is run.

six-downset-1 / researcher. The adapted separate reader is credited to b7d,
with new original parity, endpoint-rank and full symmetry gates. Author
validation of the ordinary proof, not independent-person review.
"""
from source_binding import verify_source as _verify_source
_verify_source()
import os
for name in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
             'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS'):
    os.environ[name] = '1'
import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import time

import geometry
import reader


def main():
    def expire(signum, frame):
        raise TimeoutError('fixed60s new child; incomplete is not nonexistence')
    signal.signal(signal.SIGALRM, expire)
    signal.alarm(60)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--counts', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    geometry.barrier()
    geometry.preflight(args.n, [int(x) for x in args.counts.split(',')])
    reader.require(not args.out.exists(), 'unique new complete control output')
    args.out.mkdir(parents=True)
    started = time.monotonic()
    raw = geometry.build(args.n, [int(x) for x in args.counts.split(',')])
    data = json.dumps(raw, separators=(',', ':')).encode() + b'\n'
    reader.require(len(data) <= reader.LIMIT_BYTES, 'fixed32MiB local geometry guard')
    (args.out / 'UNTRUSTED-GEOMETRY.json').write_bytes(data)
    result = reader.check(raw)
    if args.n == 4 and raw['counts'] == [4, 3, 2]:
        # The baseline is first read AFTER every new original mathematical check.
        baseline = json.loads(Path(__file__).with_name('BASELINE.json').read_text())
        reader.require(all(result[k] == v for k, v in baseline['original_fields'].items()),
                       'all complete original baseline regression fields after mathematics')
        result['new_original_baseline'] = {
            'commit': 'b7d26214d61e1aba86367ce2162ccf2a4e1aa749',
            'all_fields_equal': True,
            'scope': 'new wider-guard implementation regression; no cap/review transported',
        }
    math = json.dumps(result, sort_keys=True, separators=(',', ':')).encode() + b'\n'
    reader.require(len(math) <= reader.LIMIT_BYTES, 'fixed32MiB mathematics guard')
    (args.out / 'WHOLE-MATH.json').write_bytes(math)
    observation = {
        'agent': 'six-downset-1', 'role': 'researcher', 'complete': True,
        'n': args.n, 'counts': raw['counts'], 'N': raw['N'],
        'seconds': time.monotonic() - started,
        'peak_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'optimized': not __debug__,
        'whole_math_bytes': len(math),
        'whole_math_sha256': hashlib.sha256(math).hexdigest(),
        'whole_untrusted_geometry_bytes': len(data),
        'whole_untrusted_geometry_sha256': hashlib.sha256(data).hexdigest(),
        'source_commit': None, 'graph_ref': None,
    }
    (args.out / 'OBSERVATION.json').write_text(json.dumps(observation, indent=2) + '\n')
    signal.alarm(0)
    print(json.dumps(observation))


if __name__ == '__main__':
    main()
