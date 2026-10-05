"""Fixed source census before arithmetic imports; consistency, not authentication."""
import hashlib
import json
import os
from pathlib import Path

FILES = (
    'PROOF.md', 'RANK-BRIDGE.md', 'README.md', 'DEPENDENCIES.json',
    'PROVENANCE.json', 'geometry.py', 'reader.py', 'control.py',
    'adverse.py', 'source_adverse.py', 'source_binding.py', 'verify.py',
    'BASELINE.json', 'EXPECTED.json',
)
LIMIT = 32 * 1024 * 1024


def require(ok, message):
    if not ok:
        raise ValueError(message)


def verify_source(root=None):
    root = Path(__file__).resolve().parent if root is None else Path(root)
    source = root / 'SOURCE.json'
    require(source.is_file() and not source.is_symlink()
            and source.stat().st_size <= 65536, 'source envelope size')
    raw = source.read_bytes()
    authority = os.environ.get('SMALL_CUBE_SOURCE_SHA256')
    if authority:
        require(hashlib.sha256(raw).hexdigest() == authority, 'source envelope binding')
    data = json.loads(raw)
    require(type(data) is dict and set(data) == {
        'version', 'agent', 'role', 'defining_files', 'whole_expected'}, 'source envelope schema')
    require(type(data['version']) is int and data['version'] == 1
            and data['agent'] == 'six-downset-1' and data['role'] == 'researcher',
            'source envelope identity')
    files = data['defining_files']
    require(type(files) is dict and set(files) == set(FILES), 'source census')
    for name in FILES:
        pin = files[name]
        require(type(pin) is dict and set(pin) == {'bytes', 'sha256'}
                and type(pin['bytes']) is int and 0 < pin['bytes'] <= LIMIT
                and type(pin['sha256']) is str and len(pin['sha256']) == 64
                and all(c in '0123456789abcdef' for c in pin['sha256']), 'source pin schema')
        path = root / name
        require(path.is_file() and not path.is_symlink()
                and path.stat().st_size == pin['bytes'], 'source file binding: ' + name)
        require(hashlib.sha256(path.read_bytes()).hexdigest() == pin['sha256'],
                'source file binding: ' + name)
    require(data['whole_expected'] == files['EXPECTED.json'], 'whole expected source binding')
    return data
