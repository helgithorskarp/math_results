"""Fail-closed entire compact source census before importing mathematics."""
from pathlib import Path
import hashlib
import json


def check_bundle(base):
    base = Path(base).resolve()
    meta = json.loads((base/'BUNDLE.json').read_text())
    raw = (base/'SHA256SUMS').read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta['manifest_SHA256']:
        raise ValueError('complete source manifest changed')
    names, size = set(), 0
    for line in raw.decode().splitlines():
        digest, name = line.split('  ', 1)
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or name in names:
            raise ValueError('invalid complete source path')
        data = (base/path).read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError('whole source file changed: '+name)
        names.add(name); size += len(data)
    required = {'.gitignore', 'README.md', 'PROOF.md', 'EXPECTED.json',
                'sourcecheck.py', 'check.py', 'CERTIFICATE.json', 'credited-original/literal.py'}
    if names != required or len(names) != meta['manifest_file_count'] or size != meta['manifest_source_bytes']:
        raise ValueError('entire defining source closure required')
    return {'manifest_SHA256': meta['manifest_SHA256'], 'source_files': len(names),
            'all_source_bytes_verified_before_mathematical_import': True}
