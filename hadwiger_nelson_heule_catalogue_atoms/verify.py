#!/usr/bin/env python3
"""Independent exact source/edge/positive-colouring/exhaustive-family checker.

No producer import, native solver, or floating-point arithmetic.
"""
import argparse
import ast
import hashlib
import json
import math
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
RADICALS = (1, 3, 5, 15, 11, 33, 55, 165)


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def plus(a, b):
    c = a.copy()
    for d, v in b.items():
        c[d] = c.get(d, 0) + v
    return {d: v for d, v in c.items() if v}


def times(a, b):
    c = {}
    for d, u in a.items():
        for e, v in b.items():
            common = math.gcd(d, e)
            radical = d * e // (common * common)
            c[radical] = c.get(radical, 0) + u * v * common
    return {d: v for d, v in c.items() if v}


def opposite(a):
    return {d: -v for d, v in a.items()}


def rational_function(e):
    """Keep numerator and denominator separately; no field inversions."""
    if isinstance(e, ast.Constant) and type(e.value) is int:
        return ({1: e.value} if e.value else {}), {1: 1}
    if isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.USub):
        n, d = rational_function(e.operand)
        return opposite(n), d
    if isinstance(e, ast.Call):
        demand(isinstance(e.func, ast.Name) and e.func.id == 'sqrt'
               and len(e.args) == 1 and not e.keywords, 'unsupported call')
        n, d = rational_function(e.args[0])
        demand(set(n) <= {1} and set(d) == {1}, 'nonrational radicand')
        q = Fraction(n.get(1, 0), d[1])
        demand(q > 0, 'nonpositive radicand')
        z = q.numerator * q.denominator
        square = 1
        for p in (3, 5, 11):
            while z % (p * p) == 0:
                square *= p
                z //= p * p
        demand(z in RADICALS, 'unexpected square class')
        return {z: square}, {1: q.denominator}
    if isinstance(e, ast.BinOp):
        a, b = rational_function(e.left)
        c, d = rational_function(e.right)
        if isinstance(e.op, ast.Add):
            return plus(times(a, d), times(c, b)), times(b, d)
        if isinstance(e.op, ast.Sub):
            return plus(times(a, d), opposite(times(c, b))), times(b, d)
        if isinstance(e.op, ast.Mult):
            return times(a, c), times(b, d)
        if isinstance(e.op, ast.Div):
            demand(bool(c), 'division by zero')
            return times(a, d), times(b, c)
    raise ValueError('unsupported expression')


def read_points(text):
    points = []
    for row in text.splitlines():
        row = row.strip()
        demand(row.startswith('{') and row.endswith('}'), 'bad pair delimiters')
        row = row[1:-1].replace('Sqrt[', 'sqrt(').replace(']', ')')
        tree = ast.parse('(' + row + ')', mode='eval').body
        demand(isinstance(tree, ast.Tuple) and len(tree.elts) == 2, 'bad pair')
        p = []
        for e in tree.elts:
            numerator, denominator = rational_function(e)
            # In this pinned corpus every expanded denominator is a monomial.
            demand(len(denominator) == 1, 'nonmonomial denominator')
            d, coefficient = next(iter(denominator.items()))
            scaled = {r: Fraction(288 * v, coefficient * d)
                      for r, v in times(numerator, {d: 1}).items()}
            demand(all(r in RADICALS for r in scaled), 'coordinate field')
            demand(all(x.denominator == 1 for x in scaled.values()), 'coordinate scale')
            p.extend(int(scaled.get(r, 0)) for r in RADICALS)
        points.append(tuple(p))
    demand(len(points) == len(set(points)), 'coincident source labels')
    return points


def geometry(directory):
    manifest = json.loads((HERE / 'inputs.json').read_text())
    demand([x['vertices'] for x in manifest['sources']] == [510, 517, 529, 553], 'source family')
    sources = []
    for item in manifest['sources']:
        data = (Path(directory) / item['name']).read_bytes()
        demand(len(data) == item['bytes'], 'source byte count')
        demand(hashlib.sha256(data).hexdigest() == item['sha256'], 'source digest')
        pp = read_points(data.decode())
        demand(len(pp) == item['vertices'], 'source order')
        sources.append(set(pp))
    points = sorted(set().union(*sources))
    keyed = {}
    for v, p in enumerate(points):
        # Sign change of sqrt(5) changes precisely the coefficients whose
        # squarefree radicand is divisible by 5.
        fixed = all(not p[8 * axis + i] for axis in (0, 1)
                    for i, d in enumerate(RADICALS) if d % 5 == 0)
        member = sum(2**i for i, s in enumerate(sources) if p in s)
        keyed.setdefault((0 if fixed else 1, member), []).append(v)
    atoms = [keyed[key] for key in sorted(keyed)]
    edges = []
    for u, p in enumerate(points):
        for v in range(u):
            q = points[v]
            norm = {}
            for start in (0, 8):
                delta = {d: p[start + i] - q[start + i]
                         for i, d in enumerate(RADICALS) if p[start + i] != q[start + i]}
                norm = plus(norm, times(delta, delta))
            if norm == {1: 288**2}:
                edges.append((v, u))
    edges.sort()
    return points, atoms, edges, sorted(keyed)


def colour_checks(atoms, edges, certificate):
    demand(certificate.get('version') == 'heule-catalogue-atoms-v1', 'certificate version')
    demand(type(certificate.get('target')) is int and certificate['target'] == 508, 'target')
    n = sum(map(len, atoms))
    k = len(atoms)
    demand(sorted(v for a in atoms for v in a) == list(range(n)), 'partition')
    covers = certificate.get('covers')
    demand(type(covers) is list and len(covers) > 0, 'empty covers')
    masks = []
    incidences = 0
    for cover in covers:
        mask, word = cover.get('mask'), cover.get('word')
        demand(type(mask) is int and 0 <= mask < 2**k, 'mask range')
        demand(type(word) is str and len(word) == n, 'word length')
        for a, vertices in enumerate(atoms):
            alphabet = '0123' if (mask // 2**a) % 2 else '-'
            demand(all(word[v] in alphabet for v in vertices), 'word support or colour')
        for u, v in edges:
            if word[u] != '-' and word[v] != '-':
                demand(word[u] != word[v], 'monochromatic unit edge')
                incidences += 1
        masks.append(mask)
    demand(len(set(masks)) == len(masks), 'duplicate cover')
    return masks, incidences


def complete_family(weights, masks, limit):
    """Downward Boolean transform, then inspect EVERY selector assignment."""
    k = len(weights)
    demand(all(type(w) is int and w > 0 for w in weights), 'atom weights')
    size = 2**k
    covered = bytearray(size)
    for mask in masks:
        demand(type(mask) is int and 0 <= mask < size, 'cover mask range')
        covered[mask] = 1
    for i in range(k):
        step = 2**i
        for start in range(0, size, 2 * step):
            for j in range(start, start + step):
                if covered[j + step]:
                    covered[j] = 1
    # Gray-code scan updates the cardinality by the single changed block.
    previous, order, admissible, exact, maximal = 0, 0, 0, 0, 0
    for number in range(size):
        mask = number ^ (number // 2)
        if number:
            changed = mask ^ previous
            i = changed.bit_length() - 1
            order += weights[i] if mask & changed else -weights[i]
        if order <= limit:
            admissible += 1
            exact += (order == limit)
            demand(covered[mask], f'uncovered assignment {mask} of order {order}')
            if all(mask & 2**i or order + w > limit for i, w in enumerate(weights)):
                maximal += 1
        previous = mask
    return dict(assignments=size, admissible=admissible, exact_target=exact,
                maximal_admissible=maximal,
                downward_coverage_sha256=hashlib.sha256(covered).hexdigest())


def verify(directory, certificate):
    points, atoms, edges, keys = geometry(directory)
    masks, incidences = colour_checks(atoms, edges, certificate)
    weights = list(map(len, atoms))
    result = complete_family(weights, masks, 508)
    result.update(verified=True, record_improvement=False, target=508,
                  arbitrary_target_subsets_classified=False,
                  vertices=len(points), edges=len(edges), pair_checks=len(points)*(len(points)-1)//2,
                  atoms=len(atoms), atom_keys=[list(key) for key in keys], atom_weights=weights,
                  colour_words=len(masks), checked_edge_incidences=incidences,
                  cover_orders=[list(item) for item in sorted(Counter(sum(w for i, w in enumerate(weights) if m & 2**i) for m in masks).items())],
                  coordinate_sha256=hashlib.sha256(''.join(' '.join(map(str, p))+'\n' for p in points).encode()).hexdigest(),
                  edge_sha256=hashlib.sha256(''.join(f'{u} {v}\n' for u, v in edges).encode()).hexdigest())
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--certificate', type=Path, default=HERE/'certificate.json')
    ap.add_argument('--check-expected', action='store_true')
    args = ap.parse_args()
    result = verify(args.inputs, json.loads(args.certificate.read_text()))
    if args.check_expected:
        demand(result == json.loads((HERE/'expected.json').read_text()), 'expected report mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))
