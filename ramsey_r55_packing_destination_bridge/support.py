"""Pinned imports and exact 43-vertex physical representation."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import importlib
import importlib.util
import json
import re
import sys

HERE = Path(__file__).resolve().parent
PAIRS = list(combinations(range(43), 2))
INDEX = {p: i + 1 for i, p in enumerate(PAIRS)}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

@lru_cache(None)
def parents():
    for row in json.loads((HERE / 'DEPENDENCIES.json').read_text()):
        directory = HERE.parent / row['directory']
        raw = (directory / row['manifest']).read_bytes()
        need(sha(raw) == row['sha256'], 'dependency manifest')
        entries = (dict((name, digest) for digest, name in
                        (line.split('  ', 1) for line in raw.decode().splitlines()))
                   if row['manifest'] == 'SHA256SUMS' else json.loads(raw))
        for name, digest in entries.items():
            need(sha((directory / name).read_bytes()) == digest, 'dependency ' + name)
    old = HERE.parent / 'ramsey_r55_maximal_block_order'
    sys.path.insert(0, str(old))
    ordered = importlib.import_module('ordered')
    need(Path(ordered.__file__).resolve().parent == old.resolve(), 'module origin')
    modules = ordered.dependencies.load()
    path = HERE.parent / 'ramsey_r55_packing_augmentation' / 'transport.py'
    spec = importlib.util.spec_from_file_location('_accepted_exchange', path)
    exchange = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exchange)
    return ordered, modules['family'], exchange

def matrix(obj):
    need(type(obj) is dict and type(obj.get('n')) is int and obj['n'] == 43, 'graph order')
    h = obj.get('red_hex')
    need(type(h) is str and re.fullmatch('[0-9a-f]{226}', h) is not None,
         'physical word format')
    word = int(h, 16)
    need(word < 1 << 903, 'physical word padding')
    a = [[0] * 43 for _ in range(43)]
    for k, (u, v) in enumerate(PAIRS):
        a[u][v] = a[v][u] = (word >> k) & 1
    return a

def graph(a, order=None):
    order = list(range(43)) if order is None else order
    return {'n': 43, 'red_hex': format(sum(a[order[u]][order[v]] << k
                                        for k, (u, v) in enumerate(PAIRS)), '0226x')}

def binding(obj):
    return sha(json.dumps(obj, sort_keys=True, separators=(',', ':')).encode())

def bad_five(a, vertices=range(43)):
    # Local certificates suffice for a rejected domain; this is not a target test.
    for s in combinations(vertices, 5):
        colors = {a[u][v] for u, v in combinations(s, 2)}
        if len(colors) == 1:
            return {'vertices': list(s), 'color': colors.pop()}
    return None
