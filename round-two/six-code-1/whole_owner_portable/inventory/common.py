"""Exact serialization and the unchanged whole-case resource guards."""
import hashlib
import json
from pathlib import Path
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(encode(value)).hexdigest()


def freeze(value):
    return tuple(freeze(a) for a in value) if isinstance(value, (list, tuple)) else value


def put(path, value):
    Path(path).write_bytes(encode(value) + b'\n')


class Guard(RuntimeError):
    pass


class Budget:
    def __init__(self, name):
        self.name, self.states, self.start = name, 0, time.monotonic()

    def tick(self, n=1):
        self.states += n
        if self.states > 100000 or time.monotonic() - self.start > 10:
            raise Guard('original100000-state/10s whole case: ' + self.name)

    def receipt(self):
        return {'case': self.name, 'states': self.states,
                'elapsed_seconds': time.monotonic() - self.start}


def source_pins():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'SOURCE_MANIFEST.json').read_bytes())
    for pin in manifest['source_files']:
        path = root / pin['name']
        need(path.parent == root and path.is_file(), 'literal local source pin')
        raw = path.read_bytes()
        need(len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'],
             'entire frozen source bytes: ' + pin['name'])
    return root, manifest
