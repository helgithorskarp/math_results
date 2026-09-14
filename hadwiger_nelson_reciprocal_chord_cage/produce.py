#!/usr/bin/env python3
"""Generate the compact positive-colouring certificate using Q(zeta_30)."""

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path

N = 30
KS = (2, 3, 4, 5, 8, 9, 14)
TERMINAL_ADDRESSES = (
    (2, 0), (3, 2), (3, 0), (8, 1),
    (4, 0), (9, 7), (9, 0), (14, 13),
)


def dump(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"


def trim(poly):
    poly = list(poly)
    while poly and not poly[-1]:
        poly.pop()
    return poly


def exact_division(a, b):
    a, b = trim(a), trim(b)
    quotient = [0] * max(0, len(a) - len(b) + 1)
    while a and len(a) >= len(b):
        coefficient = a[-1] // b[-1]
        shift = len(a) - len(b)
        quotient[shift] = coefficient
        for j, value in enumerate(b):
            a[shift + j] -= coefficient * value
        a = trim(a)
    if a:
        raise ValueError("nonexact cyclotomic division")
    return trim(quotient)


def cyclotomics(limit):
    answer = {}
    for n in range(1, limit + 1):
        poly = [-1] + [0] * (n - 1) + [1]
        for d in range(1, n):
            if n % d == 0:
                poly = exact_division(poly, answer[d])
        answer[n] = poly
    return answer


PHI = tuple(cyclotomics(N)[N])
DEGREE = len(PHI) - 1
ZERO = (Fraction(0),) * DEGREE
ONE = (Fraction(1),) + (Fraction(0),) * (DEGREE - 1)
X = (Fraction(0), Fraction(1)) + (Fraction(0),) * (DEGREE - 2)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def subtract(a, b):
    return add(a, neg(b))


def multiply(a, b):
    raw = [Fraction(0)] * (2 * DEGREE - 1)
    for j, x in enumerate(a):
        if x:
            for k, y in enumerate(b):
                if y:
                    raw[j + k] += x * y
    for exponent in range(len(raw) - 1, DEGREE - 1, -1):
        coefficient = raw[exponent]
        if coefficient:
            for j in range(DEGREE):
                raw[exponent - DEGREE + j] -= coefficient * PHI[j]
    return tuple(raw[:DEGREE])


def power(a, exponent):
    answer = ONE
    while exponent:
        if exponent & 1:
            answer = multiply(answer, a)
        a = multiply(a, a)
        exponent //= 2
    return answer


POWERS = tuple(power(X, j) for j in range(N))
CONJUGATE_BASIS = tuple(POWERS[(-j) % N] for j in range(DEGREE))


def solve(matrix, right):
    rows = [list(row) + [value] for row, value in zip(matrix, right)]
    for column in range(len(rows)):
        pivot = next((r for r in range(column, len(rows))
                      if rows[r][column]), None)
        if pivot is None:
            raise ValueError("singular multiplication matrix")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [x / scale for x in rows[column]]
        for r in range(len(rows)):
            if r != column and rows[r][column]:
                scale = rows[r][column]
                rows[r] = [x - scale * y
                           for x, y in zip(rows[r], rows[column])]
    return tuple(row[-1] for row in rows)


def inverse(a):
    basis = [tuple(Fraction(i == j) for i in range(DEGREE))
             for j in range(DEGREE)]
    columns = [multiply(a, b) for b in basis]
    matrix = [[columns[j][i] for j in range(DEGREE)]
              for i in range(DEGREE)]
    return solve(matrix, ONE)


def conjugate(a):
    answer = ZERO
    for coefficient, basis in zip(a, CONJUGATE_BASIS):
        if coefficient:
            answer = add(answer, tuple(coefficient * x for x in basis))
    return answer


def norm(a):
    return multiply(a, conjugate(a))


def geometry():
    points = [ZERO]
    addresses = [(0, 0)]
    index = {ZERO: 0}
    address_index = {}
    for k in KS:
        denominator = subtract(ONE, POWERS[k])
        coefficient = inverse(denominator)
        if multiply(coefficient, denominator) != ONE:
            raise ValueError("failed exact inverse")
        for j in range(N):
            point = multiply(POWERS[j], coefficient)
            if point not in index:
                index[point] = len(points)
                points.append(point)
                addresses.append((k, j))
            address_index[(k, j)] = index[point]
    edges = [(a, b) for a, b in combinations(range(len(points)), 2)
             if norm(subtract(points[a], points[b])) == ONE]
    terminals = tuple(address_index[a] for a in TERMINAL_ADDRESSES)
    return points, addresses, edges, terminals


def adjacency(vertex_count, edges):
    answer = [set() for _ in range(vertex_count)]
    for a, b in edges:
        answer[a].add(b)
        answer[b].add(a)
    return answer


def colour(adj, pinned, number_of_colours):
    """Deterministic DSATUR; returned words are checked independently."""
    colours = list(pinned)
    unavailable = [set() for _ in adj]
    uncoloured = set()
    for v, c in enumerate(colours):
        if c < 0:
            uncoloured.add(v)
        else:
            if any(colours[w] == c for w in adj[v]):
                return None
            for w in adj[v]:
                unavailable[w].add(c)

    def search():
        if not uncoloured:
            return True
        v = max(uncoloured,
                key=lambda x: (len(unavailable[x]), len(adj[x]), -x))
        for c in range(number_of_colours):
            if c in unavailable[v]:
                continue
            colours[v] = c
            uncoloured.remove(v)
            changed = []
            impossible = False
            for w in adj[v]:
                if w in uncoloured and c not in unavailable[w]:
                    unavailable[w].add(c)
                    changed.append(w)
                    if len(unavailable[w]) == number_of_colours:
                        impossible = True
            if not impossible and search():
                return True
            for w in changed:
                unavailable[w].remove(c)
            uncoloured.add(v)
            colours[v] = -1
        return False

    return colours if search() else None


def canonical_patterns(terminal_edges):
    answer = []
    for word in product(range(4), repeat=8):
        if word[0] != 0:
            continue
        if any(word[j] > 1 + max(word[:j], default=-1) for j in range(8)):
            continue
        if any(word[a] == word[b] for a, b in terminal_edges):
            continue
        answer.append(word)
    return answer


def encode_field(a):
    return [[x.numerator, x.denominator] for x in a]


def produce():
    if PHI != (1, 1, 0, -1, -1, -1, 0, 1, 1):
        raise ValueError("unexpected Phi_30")
    if power(X, N) != ONE:
        raise ValueError("bad thirtieth root")
    points, addresses, edges, terminals = geometry()
    if len(points) != 211:
        raise ValueError("unexpected collision")
    adj = adjacency(len(points), edges)
    terminal_edges = [(a, b) for a, b in combinations(range(8), 2)
                      if terminals[b] in adj[terminals[a]]]
    patterns = canonical_patterns(terminal_edges)
    three = colour(adj, [-1] * len(points), 3)
    if three is None:
        raise ValueError("missing three-colouring")
    rows = []
    for pattern in patterns:
        pinned = [-1] * len(points)
        for vertex, c in zip(terminals, pattern):
            pinned[vertex] = c
        witness = colour(adj, pinned, 4)
        if witness is None:
            raise ValueError("nonextending pattern " + "".join(map(str, pattern)))
        rows.append({"pattern": "".join(map(str, pattern)),
                     "word": "".join(map(str, witness))})
    return {
        "version": 1,
        "source": "reciprocal_chord_cage_30",
        "coordinates": [encode_field(p) for p in points],
        "three_colour_word": "".join(map(str, three)),
        "terminal_rows": rows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    obj = produce()
    args.out.write_text(dump(obj))
    print(dump({"vertices": len(obj["coordinates"]),
                "terminal_patterns": len(obj["terminal_rows"]),
                "certificate_bytes": args.out.stat().st_size}), end="")


if __name__ == "__main__":
    main()
