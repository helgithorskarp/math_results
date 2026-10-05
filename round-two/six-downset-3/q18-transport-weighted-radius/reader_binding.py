"""Whole source binding before mathematical imports; not authentication.

The verified repository commit fixes bytes. Coordinated changes to source
and all seals are not independently detected by this same-author reader.
"""
from pathlib import Path
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check(root):
    root = Path(root).resolve()
    lines = (root/'SHA256SUMS').read_text().splitlines()
    sums = {}
    for line in lines:
        digest, name = line.split('  ', 1)
        require(name not in sums and len(digest) == 64, 'SOURCE_GATE:seal-shape')
        sums[name] = digest
    raw = (root/'SOURCE.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == sums.get('SOURCE.json'), 'SOURCE_GATE:SOURCE.json')
    source = json.loads(raw)
    require(source['actual_agent'] == 'six-downset-3' and source['role'] == 'researcher',
            'SOURCE_GATE:attribution')
    rows = source['defining_files']+source['defining_data_dependencies']
    require(len(rows) == len({row['file'] for row in rows}), 'SOURCE_GATE:manifest-shape')
    for row in rows:
        path = root/row['file']; data = path.read_bytes()
        require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['SHA256']
                and sums.get(row['file']) == row['SHA256'], 'SOURCE_GATE:'+row['file'])
    require(set(sums) == {row['file'] for row in rows}|{'SOURCE.json'}, 'SOURCE_GATE:seal-domain')
    return source
