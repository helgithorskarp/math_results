"""Seal check before imports, whole-record normal/-O replays and live controls."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def seal(root):
    lines = (root / 'SHA256SUMS').read_text().splitlines()
    seen = set()
    for line in lines:
        digest, name = line.split('  ', 1)
        need(len(digest) == 64 and all(x in '0123456789abcdef' for x in digest), 'seal encoding')
        need(name not in seen and '/' not in name and name != 'SHA256SUMS', 'seal paths')
        need(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest,
             'preimport seal mismatch: ' + name)
        seen.add(name)
    need(seen == {'check.py', 'validate.py', 'PROOF.md', 'REVIEW.md', 'README.md',
                  'RECORD.json', 'SOURCE.json'}, 'entire frozen file census')


def main():
    need(len(sys.argv) <= 2, 'validator argument count')
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else Path(__file__).resolve().parent
    seal(root)
    expected = (root / 'RECORD.json').read_bytes()
    env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'BLIS_NUM_THREADS'):
        env[name] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    controls = ('count', 'basis', 'metric', 'standard-sign', 'harmonic-sign', 'upper-metric')
    results = []
    for mode in ([], ['-O']):
        start = time.monotonic()
        command = [sys.executable, '-B', *mode, str(root / 'check.py')]
        positive = subprocess.run(command, env=env, capture_output=True, timeout=45)
        need(positive.returncode == 0 and positive.stdout == expected and not positive.stderr,
             'ENTIRE canonical positive record in ' + repr(mode))
        rejected = []
        for control in controls:
            result = subprocess.run([*command, control], env=env, capture_output=True, timeout=45)
            need(result.returncode != 0 and b'ValueError:' in result.stderr,
                 'live semantic control must reject: ' + control)
            rejected.append({'control': control, 'exit_code': result.returncode,
                             'last_error': result.stderr.decode().strip().splitlines()[-1]})
        results.append(dict(mode='optimized' if mode else 'normal', whole_record_bytes=len(expected),
                            whole_record_sha256=hashlib.sha256(expected).hexdigest(),
                            semantic_rejections=rejected, seconds=time.monotonic() - start))
    print(json.dumps(dict(actual_agent='six-reviewer-5', role='independent mathematical reviewer',
                          interpreter=sys.version, serial_math_jobs=1, native_threads=1,
                          fixed_child_timeout_seconds=45, validation=results), sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
