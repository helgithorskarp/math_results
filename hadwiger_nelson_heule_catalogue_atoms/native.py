#!/usr/bin/env python3
"""Producer: parse pinned Mathematica coordinates and build their exact union."""
import argparse
import ast
import hashlib
import json
import math
import re
import urllib.request
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
RADICALS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 288
SQRT5_POSITIONS = (2, 3, 6, 7, 10, 11, 14, 15)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def source_files(directory, download=False):
    manifest = json.loads((HERE / 'inputs.json').read_text())
    directory = Path(directory)
    if download:
        directory.mkdir(parents=True, exist_ok=True)
    paths = []
    for item in manifest['sources']:
        p = directory / item['name']
        if download and not p.exists():
            data = urllib.request.urlopen(item['url'], timeout=60).read()
            require(hashlib.sha256(data).hexdigest() == item['sha256'], 'download hash')
            p.write_bytes(data)
        data = p.read_bytes()
        require(len(data) == item['bytes'], 'input size')
        require(hashlib.sha256(data).hexdigest() == item['sha256'], 'input hash')
        paths.append(p)
    return paths


def scalar(a):
    return (F(a),) + (F(0),) * 7


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    c = [F(0)] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    c[i ^ j] += x * y * RADICALS[i & j]
    return tuple(c)


def inv(a):
    require(any(a), 'zero denominator')
    b, c = scalar(1), a
    for bit in (4, 2, 1):
        conjugate = tuple(-x if i & bit else x for i, x in enumerate(c))
        b, c = mul(b, conjugate), mul(c, conjugate)
    require(not any(c[1:]) and c[0] != 0, 'norm inversion failed')
    return tuple(x / c[0] for x in b)


def evaluate(e):
    if isinstance(e, ast.Constant) and type(e.value) is int:
        return scalar(e.value)
    if isinstance(e, ast.Name) and re.fullmatch('r[0-7]', e.id):
        return tuple(F(i == int(e.id[1])) for i in range(8))
    if isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.USub):
        return neg(evaluate(e.operand))
    if isinstance(e, ast.BinOp):
        a, b = evaluate(e.left), evaluate(e.right)
        if isinstance(e.op, ast.Add):
            return add(a, b)
        if isinstance(e.op, ast.Sub):
            return add(a, neg(b))
        if isinstance(e.op, ast.Mult):
            return mul(a, b)
        if isinstance(e.op, ast.Div):
            return mul(a, inv(b))
    raise ValueError('unsupported expression: ' + ast.dump(e))


def parse(text):
    points = []
    for line in text.splitlines():
        line = line.strip()
        require(line.startswith('{') and line.endswith('}'), 'coordinate pair')
        for d in ('11/3', '5/3'):
            numerator = int(d.split('/')[0]) * 3
            line = line.replace('Sqrt[' + d + ']', f'(Sqrt[{numerator}]/3)')
        for i, d in enumerate(RADICALS):
            line = line.replace(f'Sqrt[{d}]', f'r{i}')
        parts = line[1:-1].split(',')
        require(len(parts) == 2, 'coordinate arity')
        p = tuple(x * SCALE for s in parts
                  for x in evaluate(ast.parse(s.strip(), mode='eval').body))
        require(all(x.denominator == 1 for x in p), 'coordinate scale')
        points.append(tuple(int(x) for x in p))
    require(len(set(points)) == len(points), 'duplicate source point')
    return points


def square(x):
    a = [0] * 8
    for i, u in enumerate(x):
        if u:
            a[0] += u * u * RADICALS[i]
            for j in range(i + 1, 8):
                if x[j]:
                    a[i ^ j] += 2 * u * x[j] * RADICALS[i & j]
    return a


def unit(p, q):
    a = square([p[i] - q[i] for i in range(8)])
    b = square([p[8 + i] - q[8 + i] for i in range(8)])
    return a[0] + b[0] == SCALE**2 and all(a[i] + b[i] == 0 for i in range(1, 8))


def build(directory):
    ss = [set(parse(p.read_text())) for p in source_files(directory)]
    points = sorted(set.union(*ss))
    atoms = {}
    for v, p in enumerate(points):
        membership = sum(1 << j for j, s in enumerate(ss) if p in s)
        side = int(any(p[k] for k in SQRT5_POSITIONS))
        atoms.setdefault((side, membership), []).append(v)
    edges = [(u, v) for u, v in combinations(range(len(points)), 2)
             if unit(points[u], points[v])]
    return dict(points=points, edges=edges,
                atoms=[dict(side=k[0], membership=k[1], vertices=vs)
                       for k, vs in sorted(atoms.items())])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--download', action='store_true')
    ap.add_argument('--out', type=Path)
    args = ap.parse_args()
    source_files(args.inputs, args.download)
    graph = build(args.inputs)
    if args.out:
        args.out.write_text(json.dumps(graph, separators=(',', ':')) + '\n')
    print(json.dumps(dict(vertices=len(graph['points']), edges=len(graph['edges']),
                          atoms=len(graph['atoms'])), sort_keys=True))
