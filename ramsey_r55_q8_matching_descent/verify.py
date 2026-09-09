"""Independent graph counts and finite-difference matching polynomials."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import random
import subprocess
import tempfile


def read(path):
    lines = Path(path).read_text().splitlines()
    n, k, tail = map(int, lines[0].split())
    pairs = list(it.combinations(range(n), 2))
    if len(lines) != 3 or len(lines[1]) != len(pairs) or len(lines[2]) != len(pairs):
        raise ValueError('input length')
    if set(lines[1] + lines[2]) - {'0', '1'}:
        raise ValueError('input bit')
    a = [0] * n
    for (u, v), bit in zip(pairs, lines[1]):
        if bit == '1':
            a[u] |= 1 << v
            a[v] |= 1 << u
    return n, k, tail, pairs, a, lines[2]


def toggle(a, edge):
    u, v = edge
    a[u] ^= 1 << v
    a[v] ^= 1 << u


def cliques(a, mask, k):
    if k == 0:
        return 1
    if mask.bit_count() < k:
        return 0
    total = 0
    while mask:
        bit = mask & -mask
        mask ^= bit
        v = bit.bit_length() - 1
        total += cliques(a, mask & a[v], k - 1)
    return total


def complement(a):
    allv = (1 << len(a)) - 1
    return [allv ^ (1 << v) ^ a[v] for v in range(len(a))]


def costs(a, k, tail):
    allv = (1 << len(a)) - 1
    return [cliques(a, allv, k), cliques(complement(a), allv, k),
            cliques(a, allv & ~((1 << tail) - 1), 4)]


def flip_delta(a, k, tail, edge):
    u, v = edge
    red = bool(a[u] >> v & 1)
    blue = complement(a)
    cr = a[u] & a[v]
    cb = blue[u] & blue[v]
    nr = cliques(a, cr, k - 2)
    nb = cliques(blue, cb, k - 2)
    result = nb - nr if red else nr - nb
    if u >= tail and v >= tail:
        t = cr & ~((1 << tail) - 1)
        extra = cliques(a, t, 2)
        result += -extra if red else extra
    return result


def matchings(n, pairs, fixed):
    # Different construction: rotate a circle of vertices around a fixed pivot.
    N = n + n % 2
    idmap = {e: i for i, e in enumerate(pairs)}
    circle = list(range(N - 1))
    result = []
    for r in range(N - 1):
        edges = [(N - 1, circle[0])]
        edges += [(circle[j], circle[-j]) for j in range(1, N // 2)]
        ids = [idmap[tuple(sorted(e))] for e in edges if max(e) < n]
        result.append(sorted(i for i in ids if fixed[i] == '0'))
        circle = circle[-1:] + circle[:-1]
    # Producer uses increasing modular pivot rather than the circle's decreasing one.
    result = [result[0]] + list(reversed(result[1:]))
    seen = [x for m in result for x in m]
    if sorted(seen) != [i for i, f in enumerate(fixed) if f == '0']:
        raise ValueError('edge partition')
    return result


def finite_difference(a, k, tail, pairs, m):
    linear = [flip_delta(a, k, tail, pairs[e]) for e in m]
    b = [[0] * len(m) for _ in m]
    for i, e in enumerate(m):
        toggle(a, pairs[e])
        for j in range(i):
            b[i][j] = b[j][i] = flip_delta(a, k, tail, pairs[m[j]]) - linear[j]
        toggle(a, pairs[e])
    return sum(costs(a, k, tail)), linear, b


def parse_poly(text):
    values = list(map(int, text.split()))
    m, c = values[:2]
    if len(values) != 2 + m + m * m:
        raise ValueError('polynomial dimensions')
    a = values[2:2 + m]
    b = [values[2 + m + i * m:2 + m + (i + 1) * m] for i in range(m)]
    return c, a, b


def literal_cost(a, k, tail):
    def color(q, target):
        return all(bool(a[u] >> v & 1) == target for u, v in it.combinations(q, 2))
    red = blue = 0
    for q in it.combinations(range(len(a)), k):
        red += color(q, True)
        blue += color(q, False)
    extra = sum(color(q, True) for q in it.combinations(range(tail, len(a)), 4))
    return [red, blue, extra]


def controls(exe, out):
    out.mkdir()
    rng = random.Random(550843)
    cases = assignments = 0
    # Complete small graph input families, then deterministic larger fixtures.
    fixtures = [(n, bits) for n in (3, 4) for bits in range(1 << (n * (n - 1) // 2))]
    fixtures += [(n, rng.getrandbits(n * (n - 1) // 2)) for n in (5, 7, 8) for _ in range(6)]
    for n, word in fixtures:
        pairs = list(it.combinations(range(n), 2))
        k = 3 if n <= 4 else 5
        tail = n if n <= 4 else 2
        bits = ''.join(str(word >> i & 1) for i in range(len(pairs)))
        fixed = ''.join('1' if n >= 5 and i % 7 == 0 else '0' for i in range(len(pairs)))
        path = out / 'input.txt'
        path.write_text(f'{n} {k} {tail}\n{bits}\n{fixed}\n')
        _, _, _, _, a, _ = read(path)
        if costs(a, k, tail) != literal_cost(a, k, tail):
            raise ValueError('graph counter')
        for r, m in enumerate(matchings(n, pairs, fixed)):
            poly = finite_difference(a, k, tail, pairs, m)
            emitted = parse_poly(subprocess.check_output([str(exe), 'poly', str(path), str(r)], text=True))
            if emitted != poly:
                raise ValueError(('polynomial', n, word, r, emitted, poly))
            c, lin, b = poly
            best = c
            for mask in range(1 << len(m)):
                aa = a.copy()
                active = [j for j in range(len(m)) if mask >> j & 1]
                for j in active:
                    toggle(aa, pairs[m[j]])
                score = sum(literal_cost(aa, k, tail))
                algebra = c + sum(lin[i] for i in active) + sum(b[i][j] for i, j in it.combinations(active, 2))
                if score != algebra:
                    raise ValueError('literal polynomial truth table')
                best = min(best, score)
                assignments += 1
            value, mask = map(int, subprocess.check_output([str(exe), 'min', str(path), str(r)], text=True).split())
            if value != best or (best == c and mask != 0):
                raise ValueError('minimum or identity tie')
            cases += 1
    result = {'status': 'SMALL_LITERAL_CONTROLS_PASS', 'graphs':len(fixtures), 'matching_cases': cases, 'literal_assignments': assignments}
    (out / 'RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='mode', required=True)
    p = sub.add_parser('controls')
    p.add_argument('executable', type=Path)
    p.add_argument('out', type=Path)
    args = parser.parse_args()
    if args.mode == 'controls':
        controls(args.executable.resolve(), args.out)


if __name__ == '__main__':
    main()
