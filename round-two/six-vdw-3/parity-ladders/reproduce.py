#!/usr/bin/env python3
"""Generate, independently audit, and compare compact expected evidence."""

import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workdir', type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    work = (args.workdir or source / 'build').resolve()
    work.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                'NUMEXPR_NUM_THREADS'):
        environment[key] = '1'
    started = time.monotonic()

    def child(command):
        run = subprocess.run(command, capture_output=True, text=True,
                             env=environment, timeout=45)
        if run.returncode:
            raise RuntimeError('child failed: ' + run.stderr)
        return json.loads(run.stdout)

    generated = child([sys.executable, str(source / 'generate.py'),
                       '--output', str(work / 'model103.cnf')])
    expected = json.loads((source / 'expected.json').read_text())
    checks = []
    for flags in ([], ['-O']):
        result = child([sys.executable, *flags, str(source / 'check.py'),
                        '--model', str(work / 'model103.cnf'),
                        '--fixture', str(source / 'q23.json')])
        if result != expected:
            raise ValueError('complete checked output differs from expected')
        checks.append(result)
    for key in ('q', 'variables', 'clauses', 'distinct_ladders', 'sha256'):
        if generated[key] != checks[0]['model103'][key]:
            raise ValueError('generator/checker metadata differs at ' + key)
    (work / 'checked.json').write_text(json.dumps(checks[0], indent=2,
                                               sort_keys=True) + '\n')
    print(json.dumps({
        'status': 'VERIFIED_PARITY_LADDER_REPRODUCTION',
        'model_sha256': generated['sha256'],
        'normal_and_optimized_checks': len(checks),
        'elapsed_seconds': time.monotonic() - started,
        'peak_child_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    }, sort_keys=True))


if __name__ == '__main__':
    main()
