#!/usr/bin/env python3
"""Enumerate the whole denominator <= 2 family, using the trace bound.

No segment matching or field division is used. See README.md for completeness.
Outputs exactly the sorted placement rows consumed by the geometry checker.
"""

import argparse
from collections import Counter
from itertools import product
from pathlib import Path

RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (0,) * 8


def add(a, b):
    return tuple(x + y for x, y in zip(a, b, strict=True))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    out = [0] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i ^ j] += x * y * RADICANDS[i & j]
    return tuple(out)


def scale(a, d):
    return tuple(x * d for x in a)


def points(path):
    rows = path.read_text().splitlines()
    if rows[0] != '# scale 12':
        raise ValueError('expected scale 12')
    result = []
    for row in rows:
        if not row or row.startswith('#'):
            continue
        p = tuple(map(int, row.split()))
        if len(p) != 16:
            raise ValueError('bad coordinate row')
        result.append((p[:8], p[8:]))
    if len(set(result)) != len(result):
        raise ValueError('duplicate input point')
    return result


def orientations():
    # At common denominator 2, the field trace gives
    # a0^2 + b0^2 + 3(a1^2 + b1^2) = 4.
    # Every coefficient on sqrt(5), sqrt(11), or their products vanishes.
    result = []
    for a0, b0, a1, b1 in product(range(-2, 3), range(-2, 3),
                                   range(-1, 2), range(-1, 2)):
        if a0*a0 + b0*b0 + 3*(a1*a1 + b1*b1) != 4:
            continue
        c = (a0, a1, 0, 0, 0, 0, 0, 0)
        s = (b0, b1, 0, 0, 0, 0, 0, 0)
        if add(mul(c, c), mul(s, s)) != (4,) + (0,)*7:
            continue
        d = 2
        if all(x % 2 == 0 for x in c + s):
            d = 1
            c = tuple(x // 2 for x in c)
            s = tuple(x // 2 for x in s)
        for reflected in (False, True):
            result.append((reflected, d, c, s))
    result.sort()
    if len(result) != 24 or len(set(result)) != 24:
        raise AssertionError('orientation classification failed')
    return result


def image(p, reflected, c, s):
    x, y = p
    cx, sy, sx, cy = mul(c, x), mul(s, y), mul(s, x), mul(c, y)
    if reflected:
        return add(cx, sy), add(sx, neg(cy))
    return add(cx, neg(sy)), add(sx, cy)


def encode(values):
    return ','.join(map(str, values))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('left', type=Path)
    parser.add_argument('right', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    left, right = points(args.left), points(args.right)
    if (len(left), len(right)) != (159, 214):
        raise ValueError('expected the pinned 159- and 214-point inputs')
    histogram = Counter()
    selected = 0
    with args.output.open('x') as out:
        for reflected, d, c, s in orientations():
            target = [(scale(x, d), scale(y, d)) for x, y in left]
            source = [image(p, reflected, c, s) for p in right]
            differences = Counter(
                (tuple(x-y for x, y in zip(px, qx, strict=True)),
                 tuple(x-y for x, y in zip(py, qy, strict=True)))
                for px, py in target for qx, qy in source
            )
            supported = sorted((t, m) for t, m in differences.items() if m >= 2)
            selected += bool(supported)
            for (tx, ty), m in supported:
                histogram[m] += 1
                out.write(f'placement={m};reflected={int(reflected)};denominator={d};'
                          f'c={encode(c)};s={encode(s)};tx={encode(tx)};ty={encode(ty)}\n')
    print('all_denominator_le_2_orientations=24')
    print(f'selected_orientations={selected}')
    print(f'placements_with_at_least_two_overlaps={sum(histogram.values())}')
    print(f'pair_certificates={sum(m*(m-1)//2*n for m, n in histogram.items())}')
    for m, n in sorted(histogram.items()):
        print(f'overlap_{m}={n}')
    print('exact_scan=true')


if __name__ == '__main__':
    main()
