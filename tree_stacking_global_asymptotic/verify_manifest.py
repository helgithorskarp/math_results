#!/usr/bin/env python3
"""Verify frozen source/interface hashes. This is not a mathematical checker."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    total = 0
    for relative, entry in manifest['files'].items():
        path = (root / relative).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Invalid or missing source path: ' + relative)
        data = path.read_bytes()
        if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
            raise ValueError('Frozen source mismatch: ' + relative)
        total += len(data)
    for component in manifest['components'].values():
        for kind in ('proof', 'review'):
            entry = manifest['files'][component[kind + '_path']]
            if entry['sha256'] != component[kind + '_sha256']:
                raise ValueError('Interface identity mismatch: ' + kind)
    print(json.dumps({'verified_source_files': len(manifest['files']),
                      'verified_components': len(manifest['components']),
                      'source_bytes_excluding_manifest': total,
                      'scope': 'source integrity and interface identity; no proof verification'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
