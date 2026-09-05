#!/usr/bin/env python3
"""Regenerate and check all five cases; no SAT solver or external data needed."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def run(args):
    subprocess.run(list(map(str, args)), check=True, cwd=HERE,
                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))


def check_info(path, expected):
    content = path.read_bytes()
    if len(content) != expected['bytes'] or hashlib.sha256(content).hexdigest() != expected['sha256']:
        raise ValueError(f'bytes/hash mismatch: {path}')


def verify(work):
    expected = json.loads((HERE/'result.json').read_text())
    run([sys.executable, HERE/'audit.py'])
    checker = work/'check_formula'
    run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror',
         HERE/'check_formula.cpp', '-o', checker])
    for case in expected['cases']:
        r = case['red_cycles']
        full = work/f'full_r{r}.cnf'
        print(f'CASE r={r}: regenerating every five-set', flush=True)
        run([sys.executable, HERE/'generate.py', '--red-cycles', r, '--output', full])
        check_info(full, case['full_formula'])
        run([checker, r, full])
        core, proof = HERE/f'core_r{r}.cnf', HERE/f'proof_r{r}.rup'
        check_info(core, case['core'])
        check_info(proof, case['rup'])
        require_lines = len(proof.read_text().splitlines())
        if require_lines != case['rup_additions']:
            raise ValueError('proof addition count')
        run([sys.executable, HERE/'check_certificate.py', '--full', full,
             '--core', core, '--proof', proof])
        print(f'CASE r={r}: PASS', flush=True)
    print('PASS: order-three type 1^19 3^8 is excluded; minimum moving 3-cycles is 9')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, help='retain generated formulas/checker in this directory')
    args = parser.parse_args()
    if args.work:
        args.work.mkdir(parents=True, exist_ok=True)
        verify(args.work.resolve())
    else:
        with tempfile.TemporaryDirectory(prefix='r55-order3-k8-') as directory:
            verify(Path(directory))


if __name__ == '__main__':
    main()
