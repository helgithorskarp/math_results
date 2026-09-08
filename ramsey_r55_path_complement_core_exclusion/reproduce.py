"""Hash-pinned solver-free replay in two Python modes."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def main():
    count = 0
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        p = HERE/name
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            raise ValueError('source hash mismatch: '+name)
        count += 1
    for mode in ([], ['-O']):
        for script, arguments, expected in [
            ('derive.py', [], 'TABLE.json'),
            ('derive.py', ['--witnesses'], 'WITNESSES.json'),
            ('check.py', [], 'CHECK.json'),
            ('controls.py', [], 'CONTROLS.json'),
        ]:
            run = subprocess.run([sys.executable, *mode, '-B', str(HERE/script),
                                  *arguments], capture_output=True, check=True)
            if run.stderr:
                raise ValueError('unexpected stderr from '+script)
            if run.stdout != (HERE/expected).read_bytes():
                raise ValueError('replay differs: '+expected)
    return {'status': 'REPRODUCED_COMPLETE_HEREDITARY_CORE_EXCLUSION',
            'manifest_entries': count, 'python_modes': 2,
            'solver_calls': 0, 'excluded_core_order': 26,
            'exact_class_maximum': 25, 'good43_found': False}


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
