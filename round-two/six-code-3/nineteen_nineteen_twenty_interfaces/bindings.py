"""SHA-pinned published predicates; no private corpus is a premise."""
import hashlib
import importlib.util
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / 'nineteen_twenty_twenty_interfaces'


def load(name, filename, checksum):
    path = PRIOR / filename
    if hashlib.sha256(path.read_bytes()).hexdigest() != checksum:
        raise ValueError('published source changed: ' + filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(PRIOR))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


producer = load('published_67_mask', 'produce.py',
                '4c02d9bff8a715e1c0ae502deef60de57643484bed2121c1affebaa36d133569')
verifier = load('published_67_literal', 'verify.py',
                'b3f95c741d304796cbe2d41e94feee68d750bf5e1926c692aa67496cccb4beda')
p = producer.p
v = verifier.v
Native = producer.Native


def swap_mask(word):
    a, b = bool(word & (1 << 15)), bool(word & (1 << 16))
    return word ^ ((1 << 15) | (1 << 16)) if a != b else word


def swap_points(word):
    return frozenset(16 if i == 15 else 15 if i == 16 else i for i in word)
