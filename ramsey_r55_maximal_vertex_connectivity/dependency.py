#!/usr/bin/env python3
"""Pin the complete prior separator18 proof package; no network needed."""
import hashlib
from pathlib import Path

DIRECTORY = 'ramsey_r55_separator18_classification'
COMMIT = '4b6455643c0dba1222231b66c1dedca699cf03e9'
MANIFEST_SHA256 = '1f3d9a3b32f5c5574846fb1c0a6a753922e2391445e6e06934d0be1e4d69580b'


def checked_parent():
    parent = Path(__file__).resolve().parent.parent / DIRECTORY
    manifest = (parent/'SHA256SUMS').read_bytes()
    if hashlib.sha256(manifest).hexdigest() != MANIFEST_SHA256:
        raise ValueError('prior separator18 manifest mismatch')
    names = []
    for line in manifest.decode().splitlines():
        digest, name = line.split('  ', 1)
        if Path(name).name != name or name in names:
            raise ValueError('unsafe/duplicate prior dependency path')
        if hashlib.sha256((parent/name).read_bytes()).hexdigest() != digest:
            raise ValueError(('prior dependency file mismatch', name))
        names.append(name)
    if len(names) != 19:
        raise ValueError('incomplete prior dependency package')
    return parent
