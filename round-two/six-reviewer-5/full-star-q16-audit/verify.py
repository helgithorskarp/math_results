"""Whole-source closure before the independent exact validation."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--source-only', action='store_true')
    a = p.parse_args()
    root = Path(__file__).resolve().parent
    names = {'CERTIFICATE.json', 'DEPENDENCIES.json', 'LITERATURE.md', 'PROOF.md',
             'PROVENANCE.json', 'README.md', 'RECORD.json', 'REVIEW.md',
             'VALIDATION.json', 'check.py', 'validate.py', 'verify.py'}
    rows = [line.split('  ') for line in (root/'SHA256SUMS').read_text().splitlines()]
    if len(rows) != len(names) or {row[1] for row in rows} != names:
        raise ValueError('entire source manifest/census')
    for digest, name in rows:
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest:
            raise ValueError('whole source mismatch: '+name)
    if a.source_only:
        a.out.write_text('whole source closure passed\n')
    else:
        subprocess.run([sys.executable, '-I', '-B', str(root/'validate.py'),
                        '--out', str(a.out)], check=True)


if __name__ == '__main__':
    main()
