#!/usr/bin/env python3
"""Read the literal matrix; import no construction, certificate, or checker code.

Use directed-distance neighborhoods, iterative matching, exhaustive Hall sets,
and an independent five-reversal construction from the cyclic nine-part rule.
"""
from __future__ import annotations
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def validate(g: list[set[int]]) -> None:
    n = len(g)
    for i in range(n):
        need(i not in g[i] and g[i] <= set(range(n)), 'invalid row')
        for j in range(i):
            need((j in g[i]) != (i in g[j]), 'invalid tournament edge')


def link(g: list[set[int]], v: int) -> tuple[list[int], set[int]]:
    reach = set().union(*(g[u] for u in g[v]))
    return sorted(g[v]), reach - g[v] - {v}


def matching(g: list[set[int]], left: list[int], right: set[int]) -> int:
    left_mate: dict[int, int] = {}
    right_mate: dict[int, int] = {}
    for start in left:
        queue = deque([start])
        seen_left = {start}
        parent: dict[int, int] = {}
        end = None
        while queue and end is None:
            u = queue.popleft()
            for v in sorted(g[u] & right):
                if v in parent:
                    continue
                parent[v] = u
                if v not in right_mate:
                    end = v
                    break
                other = right_mate[v]
                if other not in seen_left:
                    queue.append(other)
                    seen_left.add(other)
        while end is not None:
            u = parent[end]
            old = left_mate.get(u)
            left_mate[u] = end
            right_mate[end] = u
            end = old
    return len(left_mate)


def hall_maximum(g: list[set[int]], left: list[int], right: set[int]) -> tuple[int, int]:
    maximum, count = 0, 0
    for size in range(len(left) + 1):
        for source in itertools.combinations(left, size):
            neighbors = set().union(*(g[u] & right for u in source))
            maximum = max(maximum, size - len(neighbors))
            count += 1
    return maximum, count


def surgery(a: int, b: int, c: int) -> tuple[list[set[int]], list[tuple[int, int]], list[int]]:
    # Original kind, cyclic index, size. A1 is removed; B0, B2 and the C parts split.
    descriptors = [('A', 0, a), ('A', 2, a), ('B', 0, a), ('B', 0, a),
        ('B', 1, b), ('B', 2, a), ('B', 2, a), ('C', 0, a), ('C', 0, c),
        ('C', 1, c), ('C', 1, a), ('C', 2, a), ('C', 2, c)]
    reversals = {(0, 7), (6, 7), (7, 10), (3, 11), (4, 11)}
    labels = [(i, depth) for i, (_, _, size) in enumerate(descriptors) for depth in range(size)]
    def beats(p: int, q: int) -> bool:
        kind, i, _ = descriptors[p]
        other, j, _ = descriptors[q]
        if kind == other:
            answer = p < q if i == j else (j - i) % 3 == 1
        elif {kind, other} == {'A', 'B'}:
            answer = kind == 'B'
        elif {kind, other} == {'A', 'C'}:
            answer = i != j if kind == 'A' else i == j
        else:
            answer = i == j if kind == 'B' else i != j
        return not answer if tuple(sorted((p, q))) in reversals else answer
    graph = [{j for j, (q, v) in enumerate(labels)
              if (u < v if p == q else beats(p, q))} for p, u in labels]
    return graph, labels, [size for _, _, size in descriptors]


def deficits(a: int, b: int, c: int) -> list[int]:
    return [max(0, c - 3*a, c - 2*a - b), max(0, c-a-b),
        max(0, b-a, b-c, a-2*c), max(0, b-a, b-c, a-2*c),
        max(a, 3*a-c),
        max(0, a-c, 2*a-2*c, 3*a-b, 4*a-b-c),
        max(0, a-c, 2*a-2*c, 3*a-b, 4*a-b-c),
        max(0, b+c-5*a, c-3*a), max(0, b-a),
        max(0, a-c, 3*a-b), max(0, a-c, 3*a-b, 4*a-b-c),
        max(0, c-a-b), max(0, b-a)]


def main() -> None:
    data = (HERE / 'tournament23.txt').read_bytes()
    lines = data.decode('ascii').splitlines()
    need(len(lines) == 23 and all(len(s) == 23 and set(s) <= {'0', '1'} for s in lines), 'bad literal matrix')
    graph = [{j for j, bit in enumerate(row) if bit == '1'} for row in lines]
    validate(graph)
    direct, _, _ = surgery(1, 2, 4)
    need(graph == direct, 'literal and five-reversal construction differ')
    profile, subsets = [], 0
    for v in range(23):
        left, right = link(graph, v)
        size = matching(graph, left, right)
        delta, count = hall_maximum(graph, left, right)
        need(delta == len(left) - size > 0, 'literal matching / Hall check failed')
        profile.append([len(left), len(right), size, delta])
        subsets += count
    records, vertices = [], 0
    for a, b, c in itertools.product(range(1, 7), repeat=3):
        g, labels, sizes = surgery(a, b, c)
        validate(g)
        delta = deficits(a, b, c)
        actual = []
        for v, (part, depth) in enumerate(labels):
            left, right = link(g, v)
            defect = len(left) - matching(g, left, right)
            need(defect == sizes[part] - 1 - depth + delta[part], 'parameter formula failure')
            actual.append(defect)
            vertices += 1
        strong = sum(d == 0 for d in actual)
        need(strong == sum(d == 0 for d in delta), 'strong count failure')
        need((strong == 0) == (a < b < 3*a and c > max(3*a, a+b)), 'exact chamber failure')
        records.append([a, b, c, strong, actual])
    # Opposite fixture: a sink is strong because the empty matching covers its empty out-set.
    transitive = [set(range(i + 1, 5)) for i in range(5)]
    need(link(transitive, 4) == ([], set()) and matching(transitive, [], set()) == 0, 'sink fixture failure')
    print(json.dumps({'status': 'INDEPENDENT CHECK PASSED', 'literal_order': 23,
        'literal_profile': profile, 'literal_strong_vertices': [],
        'hall_subsets_exhausted': subsets, 'parameter_range': [1, 6],
        'parameter_triples': len(records), 'expanded_vertices_checked': vertices,
        'parameter_audit_sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
        'tournament_sha256': hashlib.sha256(data).hexdigest()}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
