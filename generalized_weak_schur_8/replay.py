#!/usr/bin/env python3
"""Regenerate, audit, solve, and independently check the global N=365 instance."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from audit import audit


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--drat-trim', type=Path, required=True)
    args = parser.parse_args()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(root / 'encode.py'), '--n', '365', '--r', '171',
                    '--out', str(args.out)], check=True)
    result = json.loads((args.out / 'result.json').read_text())
    if result['status'] != 'UNSAT':
        raise RuntimeError(f'No proof produced: {result["status"]}')
    report = audit(args.out / 'input.cnf', 365, 8, 171)
    expected = json.loads((root / 'expected.json').read_text())
    if report['sha256'] != expected['files']['input.cnf']['sha256']:
        raise RuntimeError('CNF differs from the published instance')
    (args.out / 'audit.json').write_text(json.dumps(report, indent=2) + '\n')
    with (args.out / 'check.log').open('w') as log:
        process = subprocess.run([str(args.drat_trim.resolve()), str(args.out / 'input.cnf'),
                                  str(args.out / 'proof.drat'), '-U'],
                                 stdout=log, stderr=subprocess.STDOUT)
    checked = (args.out / 'check.log').read_text()
    if process.returncode != 0 or 's VERIFIED' not in checked:
        raise RuntimeError('Independent RUP proof verification failed; see check.log')
    summary = {'status': 'VERIFIED_WS8_2_EQUALS_365', 'cnf_sha256': report['sha256'],
               'proof_sha256': digest(args.out / 'proof.drat'),
               'input_clauses': report['clauses'], 'variables': report['variables'],
               'checker_exit_code': process.returncode}
    (args.out / 'verified.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
