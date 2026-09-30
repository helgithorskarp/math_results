#!/usr/bin/env python3
"""Pinned prior primitives and literal checks for the mixed-star proof."""
import hashlib
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent
WORK = Path(os.environ.get('MIXED_WORK', str(BASE / '.work'))).resolve()
SOURCE = Path(os.environ.get('MIXED_DEPENDENCY', str(BASE.parent / 'a18_6_5_double_221_pair'))).resolve()
manifest = json.loads((BASE / 'DEPENDENCY.json').read_text())
for name, expected in manifest['files'].items():
    if hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() != expected:
        raise RuntimeError('pinned dependency bytes differ: ' + name)
spec = importlib.util.spec_from_file_location('oldmodels', SOURCE / 'models.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def write(name, value):
    WORK.mkdir(parents=True, exist_ok=True)
    temporary = WORK / (name + '.tmp')
    temporary.write_text(json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n')
    temporary.replace(WORK / name)


def points(word):
    return tuple(z for z in range(18) if word >> z & 1)


def edge_image(edges, permutation):
    return tuple(sorted(tuple(sorted((permutation[a], permutation[b]))) for a, b in edges))


def validate_second(template, common, cover, expected_leave):
    shortened = [tuple([17] + list(t)) for t in common] + [points(w) for w in cover]
    if len(shortened) != 20 or any(len(q) != 4 for q in shortened):
        raise RuntimeError('bad second-star dimensions')
    if any(len(set(a) & set(b)) > 1 for a, b in combinations(shortened, 2)):
        raise RuntimeError('second-star pair conflict')
    star = sorted(sum(1 << z for z in q) | 1 for q in shortened)
    first = [w | (1 << 17) for w in template['star']]
    union = sorted(set(first + star))
    if len(union) != 37 or any((a & b).bit_count() > 2 for a, b in combinations(union, 2)):
        raise RuntimeError('invalid joint star')
    full_leave = {(a, b) for a, b in combinations(range(1, 18), 2)
                  if not any((w >> a & 1) and (w >> b & 1) for w in star)}
    actual_old = tuple(sorted(e for e in full_leave if 17 not in e))
    if actual_old != expected_leave:
        raise RuntimeError('second-star leave mismatch')
    deficit = {z: 5 - sum(w >> z & 1 for w in star) for z in range(1, 18)}
    if deficit[17] != 2 or sorted(v for v in deficit.values() if v) != [1, 1, 1, 2]:
        raise RuntimeError('second-star positive deficit profile mismatch')
    return star


def historical_baseline():
    raw = (SOURCE / 'acl69.txt').read_bytes()
    words = [int(row, 2) for row in raw.splitlines()]
    if len(words) != 69 or len(set(words)) != 69 or any(w.bit_count() != 5 for w in words) or any(
            (a & b).bit_count() > 2 for a, b in combinations(words, 2)):
        raise RuntimeError('invalid historical69 baseline')
    centers = []
    for x in range(18):
        if sum(w >> x & 1 for w in words) != 20:
            continue
        row = sorted((5 - sum((w >> x & 1) and (w >> y & 1) for w in words)
                      for y in range(18) if y != x), reverse=True)
        if any(t < 0 for t in row) or sum(row) != 5:
            raise RuntimeError('invalid baseline deficit row')
        if [t for t in row if t] == [2, 2, 1]:
            centers.append(x)
    if centers != [3]:
        raise RuntimeError('historical profile changed')
    return dict(words=69, raw_sha256=hashlib.sha256(raw).hexdigest(),
                coordinate0='rightmost binary digit', profile221_centers=centers)
