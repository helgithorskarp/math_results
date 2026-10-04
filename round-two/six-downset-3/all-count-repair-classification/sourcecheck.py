"""Whole compact source gate; external generated records remain untrusted."""
from pathlib import Path
import hashlib
import json


def check_bundle(base):
    base = Path(base).resolve()
    manifest = base/'SHA256SUMS'
    metadata = json.loads((base/'BUNDLE.json').read_text())
    raw = manifest.read_bytes()
    if hashlib.sha256(raw).hexdigest() != metadata['manifest_SHA256']:
        raise ValueError('complete source manifest changed')
    files = {}
    for line in raw.decode().splitlines():
        digest, name = line.split('  ', 1)
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or name in files:
            raise ValueError('invalid complete source path')
        contents = (base/path).read_bytes()
        if hashlib.sha256(contents).hexdigest() != digest:
            raise ValueError('whole source file changed: '+name)
        files[name] = len(contents)
    if len(files) != metadata['manifest_file_count'] or sum(files.values()) != metadata['manifest_source_bytes']:
        raise ValueError('incomplete compact source census')
    required = {'.gitignore', 'README.md', 'PROOF.md', 'EXPECTED.json', 'sourcecheck.py',
                'polynomial.py', 'generate.py', 'check.py', 'FINITE-CERTIFICATE.json', 'credited-original/literal.py'}
    if set(files) != required:
        raise ValueError('entire defining source closure required')
    return {'manifest_SHA256': metadata['manifest_SHA256'], 'source_files': len(files),
            'all_source_bytes_verified_before_mathematical_import': True}
