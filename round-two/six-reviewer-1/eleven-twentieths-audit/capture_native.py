"""OPTIONAL late native execution/instrumentation, NOT independent primary code.

Run only on a separately fetched pinned author directory AFTER PRIMARY_SEAL.
Capture every complete vector before the author's ordinary hash discards it.
The author module is executed only here, never by the independent checker.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


def run(source):
    spec = importlib.util.spec_from_file_location('late_author_corroboration', source/'verify.py')
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    pins = {name: dict(bytes=len((source/name).read_bytes()),
                       sha256=hashlib.sha256((source/name).read_bytes()).hexdigest())
            for name in native.PINS}
    native.typed_equal(pins, json.loads((source/'MANIFEST.json').read_text())['files'], 'manifest')
    original_digest, vectors = native.digest, []
    def capture(value):
        if isinstance(value, list) and all(type(x) is str for x in value):
            vectors.append(value[:])
        return original_digest(value)
    native.digest = capture
    expected, whole = native.compute('')
    native.typed_equal(expected, json.loads((source/'EXPECTED.json').read_text()))
    if len(vectors) != 57+48*7:
        raise ValueError('complete late native vector census')
    return dict(agent='six-reviewer-1', role='independent mathematical reviewer',
                late_native_corroboration_NOT_primary=True,
                expected=expected, whole=whole, all393_complete_native_vectors=vectors)


if __name__ == '__main__':
    print(json.dumps(run(Path(sys.argv[1]).resolve()), sort_keys=True, separators=(',', ':')))
