#!/usr/bin/env python3
"""Fetch only public pinned inputs; verify all bytes before placing them."""
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

HERE = Path(__file__).resolve().parent


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else HERE.parents[2]
    data = json.loads((HERE / 'INPUTS.json').read_text())
    for row in data['files']:
        destination = root / row['path']
        body = destination.read_bytes() if destination.exists() else None
        if body is None or len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['sha256']:
            url = 'https://raw.githubusercontent.com/helgithorskarp/math_results/' + row['commit'] + '/' + row['path']
            with urllib.request.urlopen(url, timeout=25) as response:
                body = response.read()
        if len(body) != row['bytes'] or hashlib.sha256(body).hexdigest() != row['sha256']:
            raise ValueError('changed pinned input: ' + row['path'])
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(body)
    print('PASS public pinned inputs', len(data['files']))


if __name__ == '__main__':
    main()
