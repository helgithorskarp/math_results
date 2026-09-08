#!/usr/bin/env python3
"""Verify the preserved counterexample under both Python modes; no solver."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def main():
    names = []
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if Path(name).name != name or name in names:
            raise ValueError('unsafe/duplicate manifest path')
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != digest:
            raise ValueError(('manifest mismatch', name))
        names.append(name)
    for mode in ([], ['-O']):
        result = subprocess.run([sys.executable, *mode, '-B', str(HERE/'check.py')],
                                check=True, capture_output=True)
        if result.stderr or result.stdout != (HERE/'CHECK.json').read_bytes():
            raise ValueError(('witness replay mismatch', mode, result.stderr.decode()))
    print(json.dumps({'status': 'REPRODUCED_FAILED_TRIANGLE_SUPPORT_GATE',
                      'manifest_entries': len(names), 'python_modes': 2,
                      'solver_calls': 0, 'global43_branch_decided': False,
                      'good43_found': False}, sort_keys=True))


if __name__ == '__main__':
    main()
