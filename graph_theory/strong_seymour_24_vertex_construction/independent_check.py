#!/usr/bin/env python3
"""No imports from the constructor, Hall checker, or optimization solver.

Read the literal tournament, exhaust all Hall subsets, then check the full
three-parameter deficiency formula by vertex-level augmenting paths.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def validate(g: list[int]) -> None:
    n = len(g)
    need(n > 0, 'empty graph')
    for i, a in enumerate(g):
        need(type(a) is int and 0 <= a < 1 << n and not a >> i & 1, 'bad row')
        for j in range(i):
            need(((a >> j) & 1) + ((g[j] >> i) & 1) == 1, 'not a tournament')


def neighborhoods(g: list[int], v: int) -> tuple[list[int], int]:
    left = [i for i in range(len(g)) if g[v] >> i & 1]
    reach = 0
    for i in left:
        reach |= g[i]
    return left, reach & ~(g[v] | (1 << v))


def matching(g: list[int], left: list[int], right: int) -> int:
    mate: dict[int, int] = {}
    def visit(u: int, seen: set[int]) -> bool:
        for v in range(len(g)):
            if right >> v & 1 and g[u] >> v & 1 and v not in seen:
                seen.add(v)
                if v not in mate or visit(mate[v], seen):
                    mate[v] = u
                    return True
        return False
    return sum(visit(u, set()) for u in left)


def all_hall(g: list[int], left: list[int], right: int) -> tuple[int, int]:
    unions = [0] * (1 << len(left))
    maximum = 0
    for s in range(1, len(unions)):
        bit = s & -s
        unions[s] = unions[s ^ bit] | (g[left[bit.bit_length() - 1]] & right)
        maximum = max(maximum, s.bit_count() - unions[s].bit_count())
    return maximum, len(unions)


def direct_family(a: int, b: int, c: int) -> tuple[list[int], list[tuple[str, int, int]]]:
    labels = [(kind, i, j) for kind, size in zip('ABC', (a, b, c)) for i in range(3) for j in range(size)]
    def beats(x: tuple[str, int, int], y: tuple[str, int, int]) -> bool:
        k, i, u = x
        l, j, v = y
        if k == l:
            return u < v if i == j else (j - i) % 3 == 1
        if {k, l} == {'A', 'B'}:
            return k == 'B'
        if {k, l} == {'A', 'C'}:
            return i != j if k == 'A' else i == j
        return i == j if k == 'B' else i != j
    graph = [sum(1 << j for j, y in enumerate(labels) if i != j and beats(x, y)) for i, x in enumerate(labels)]
    return graph, labels


def main() -> None:
    data = (HERE / 'tournament24.txt').read_bytes()
    lines = data.decode('ascii').splitlines()
    need(len(lines) == 24 and all(len(s) == 24 and set(s) <= {'0', '1'} for s in lines), 'invalid matrix text')
    g = [sum((c == '1') << j for j, c in enumerate(s)) for s in lines]
    validate(g)
    direct, _ = direct_family(1, 2, 5)
    need(g == direct, 'cyclic rule and literal matrix disagree')
    profile, subsets = [], 0
    for v in range(24):
        left, right = neighborhoods(g, v)
        m = matching(g, left, right)
        deficiency, count = all_hall(g, left, right)
        need(deficiency == len(left) - m > 0, 'matching / exhaustive Hall disagreement')
        profile.append([len(left), right.bit_count(), m, deficiency])
        subsets += count
    records, checked = [], 0
    for a, b, c in itertools.product(range(1, 7), repeat=3):
        graph, labels = direct_family(a, b, c)
        validate(graph)
        delta = {'A': max(0, c - 2 * b), 'B': max(a, 3 * a - c), 'C': max(0, b - a)}
        sizes = dict(zip('ABC', (a, b, c)))
        strong = 0
        defects = []
        for v, (kind, i, depth) in enumerate(labels):
            left, right = neighborhoods(graph, v)
            actual = len(left) - matching(graph, left, right)
            expected = sizes[kind] - 1 - depth + delta[kind]
            need(actual == expected, 'universal formula audit failure')
            defects.append(actual)
            strong += actual == 0
            checked += 1
        need(strong == 3 * (c <= 2 * b) + 3 * (b <= a), 'strong count formula failure')
        records.append([a, b, c, strong, defects])
    # The ordinary transitive tournament has a strong sink: a useful opposite fixture.
    transitive = [sum(1 << j for j in range(i + 1, 24)) for i in range(24)]
    need(neighborhoods(transitive, 23) == ([], 0), 'bad sink fixture')
    need(matching(transitive, [], 0) == 0, 'sink should be strong')
    bad = g[:]
    bad[0] |= 1
    try:
        validate(bad)
    except ValueError:
        pass
    else:
        raise ValueError('loop was accepted')
    print(json.dumps({
        'status': 'INDEPENDENT CHECK PASSED',
        'literal_order': 24, 'literal_profile': profile, 'literal_strong_vertices': [],
        'hall_subsets_exhausted': subsets,
        'parameter_range': [1, 6], 'parameter_triples': len(records),
        'expanded_vertices_checked': checked,
        'parameter_audit_sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
        'tournament_sha256': hashlib.sha256(data).hexdigest(),
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
