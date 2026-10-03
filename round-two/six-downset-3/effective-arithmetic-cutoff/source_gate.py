"""Check the entire source packet and unchanged credited parent before imports."""
from pathlib import Path, PurePosixPath
import hashlib
import json

BASE = Path(__file__).resolve().parent


def verify():
    manifest = (BASE / 'SHA256SUMS').read_bytes()
    pin = json.loads((BASE / 'SOURCE-PIN.json').read_text())
    if hashlib.sha256(manifest).hexdigest() != pin['manifest_SHA256']:
        raise ValueError('Complete packet manifest differs')
    expected = {}
    for line in manifest.decode().splitlines():
        digest, name = line.split('  ', 1)
        path = PurePosixPath(name)
        if (len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest)
                or path.is_absolute() or '..' in path.parts or path.as_posix() != name
                or name in expected or name in ('SHA256SUMS', 'SOURCE-PIN.json')):
            raise ValueError('Invalid complete source path or digest')
        expected[name] = digest
    actual = set()
    for path in BASE.rglob('*'):
        relative = path.relative_to(BASE)
        if 'work' in relative.parts or '__pycache__' in relative.parts or path.suffix == '.pyc':
            continue
        if path.is_symlink():
            raise ValueError('Source symlink outside closure')
        if path.is_file() and relative.as_posix() not in ('SHA256SUMS', 'SOURCE-PIN.json'):
            actual.add(relative.as_posix())
    if actual != set(expected) or len(expected) != pin['manifest_entries']:
        raise ValueError('Omitted or unexpected complete source')
    for name, digest in expected.items():
        if hashlib.sha256((BASE / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Complete source differs: ' + name)
    parent = json.loads((BASE / 'PARENT.json').read_text())
    old = BASE / 'credited/uniform-repair-face'
    old_manifest = (old / 'SHA256SUMS').read_bytes()
    if hashlib.sha256(old_manifest).hexdigest() != parent['source_manifest_SHA256']:
        raise ValueError('Credited defining parent manifest differs')
    names = []
    for line in old_manifest.decode().splitlines():
        digest, name = line.split('  ', 1)
        if hashlib.sha256((old / name).read_bytes()).hexdigest() != digest:
            raise ValueError('Credited defining source differs: ' + name)
        names.append(name)
    names.append('SHA256SUMS')
    if (len(names) != parent['source_file_count_including_manifest']
            or sum((old / name).stat().st_size for name in names) != parent['source_bytes']):
        raise ValueError('Whole credited source closure differs')
    return {'manifest_SHA256': pin['manifest_SHA256'],
            'manifest_entries': len(expected),
            'complete_source_files_including_manifest_and_pin': len(expected) + 2,
            'whole_parent_files': len(names),
            'entire_sources_checked_before_mathematical_import': True}


if __name__ == '__main__':
    print(json.dumps(verify(), sort_keys=True))
