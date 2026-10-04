"""Verify the entire compact publication source, then reproduce all mathematics."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    arg = p.parse_args()
    root = Path(__file__).resolve().parent
    rows = [line.split('  ') for line in (root/'SHA256SUMS').read_text().splitlines()]
    if any(len(row) != 2 or '/' in row[1] or row[1] in ('', '.', '..') for row in rows):
        raise ValueError('flat owned source manifest')
    names = [row[1] for row in rows]
    if len(set(names)) != len(names) or sorted(names+['SHA256SUMS']) != sorted(x.name for x in root.iterdir() if x.is_file()):
        raise ValueError('complete exact source file census')
    for digest, name in rows:
        raw = (root/name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise ValueError('whole source digest: '+name)
        raw.decode('utf-8')
        if name.endswith('.json'):
            json.loads(raw)
    child = subprocess.run([sys.executable, '-I', '-B', str(root/'validate.py'), '--out', str(arg.out)],
                           capture_output=True, text=True)
    if child.returncode:
        raise RuntimeError(child.stdout+child.stderr)
    receipt = json.loads(arg.out.read_text())
    if len(receipt['positive_children']) != 3 or len(receipt['controls']) != 18:
        raise ValueError('complete public source mathematical replay')
    print(child.stdout.strip())


if __name__ == '__main__':
    main()
