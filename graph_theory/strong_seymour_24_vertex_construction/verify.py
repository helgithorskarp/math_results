#!/usr/bin/env python3
"""Check the explicit Hall certificate and exact primal/dual identities."""
from __future__ import annotations
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from construction import blowup, cyclic_data, hall_rows

HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def determinant(matrix: list[list[int]]) -> Fraction:
    a = [[Fraction(v) for v in row] for row in matrix]
    answer = Fraction(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        answer *= a[i][i]
        for j in range(i + 1, len(a)):
            ratio = a[j][i] / a[i][i]
            a[j] = [x - ratio * y for x, y in zip(a[j], a[i])]
    return answer


def check_vertices(adj: list[list[int]], fibres: list[list[int]], sources: list[list[int]], scale: int) -> list[tuple[int, int]]:
    sizes = []
    for p, fibre in enumerate(fibres):
        witness = {v for j in sources[p] for v in fibres[j]}
        for root in fibre:
            first = {j for j, bit in enumerate(adj[root]) if bit}
            second = {v for u in first for v, bit in enumerate(adj[u]) if bit} - first - {root}
            neighbors = {v for u in witness for v in second if adj[u][v]}
            require(witness <= first, 'source outside first neighborhood')
            require(len(witness) - len(neighbors) == scale, 'wrong Hall deficiency')
            sizes.append((len(witness), len(neighbors)))
    return sizes


def main() -> None:
    c = json.loads((HERE / 'certificate.json').read_text())
    require(c['schema'] == 1, 'unsupported certificate schema')
    out, weights, sources, dual = (c[k] for k in ('out_neighbors', 'weights', 'hall_sources', 'dual_multipliers'))
    q = len(out)
    # Gibbons, constant-nine note (2.3): verify the prior-art identification.
    prior_out = [{2, 4, 5, 6, 7}, {0, 3, 4, 8}, {1, 4, 5, 6, 8},
                 {0, 2, 5, 7}, {3, 5, 7}, {1, 6, 7}, {1, 3, 4},
                 {1, 2, 6, 8}, {0, 3, 4, 5, 6}]
    label_map = [6, 4, 5, 0, 2, 8, 7, 1, 3]
    require(sorted(label_map) == list(range(q)), 'invalid prior-art label map')
    require(all({label_map[j] for j in out[i]} == prior_out[label_map[i]] for i in range(q)),
            'prior-art quotient identification failed')
    prior_weights = [1, 3, 1, 3, 1, 1, 1, 3, 1]
    require([prior_weights[j] for j in label_map] == [1] * 6 + [3] * 3,
            'prior balanced weights disagree')
    require(q == 9 and sum(weights) == 24, 'wrong construction size')
    require((out, weights, sources) == cyclic_data(1, 2, 5), 'cyclic parameter rule differs from certificate')
    a, targets = hall_rows(out, sources)
    expected_closed = {
        0: {(1, 7, 8): (0, -3, 1), (1, 8): (0, -2, 0),
            (1, 7): (0, -2, 0), (7,): (0, -2, 1), (1,): (0, 0, -1)},
        3: {(0, 1, 2, 4, 6): (3, 0, -1), (2, 4, 6): (1, 0, 0),
            (0, 1, 2): (3, 0, -2), (2,): (1, 0, -1), (1,): (1, 0, -1)},
        6: {(0, 4, 5, 7): (-1, 1, 0), (0, 7): (0, -1, 0),
            (0, 4): (-1, 1, -1), (4,): (-2, 1, 0), (0,): (0, 0, -1)},
    }
    subset_count = 0
    for root, expected in expected_closed.items():
        op = set(out[root])
        singleton = {j: set(out[j]) - op - {root} for j in op}
        closed = {}
        ordered = sorted(op)
        for bits in range(1 << len(ordered)):
            subset_count += 1
            src = {v for i, v in enumerate(ordered) if bits >> i & 1}
            dest = set().union(*(singleton[v] for v in src))
            closure = {j for j in op if singleton[j] <= dest}
            if src and src == closure:
                row = [int(j in src) - int(j in dest) for j in range(q)]
                closed[tuple(sorted(src))] = tuple(sum(row[j:j + 3]) for j in (0, 3, 6))
        require(closed == expected, 'universal symbolic table failure')
    require(subset_count == 56, 'wrong symbolic coverage')
    defects = [sum(x * y for x, y in zip(row, weights)) for row in a]
    require(defects == [1] * q, 'primal certificate failure')
    require(len(dual) == q and all(type(x) is int and x > 0 for x in dual), 'invalid dual')
    require([sum(dual[i] * a[i][j] for i in range(q)) for j in range(q)] == [1] * q, 'dual identity failure')
    det = determinant(a)
    require(det == 13 and sum(dual) == 24, 'wrong determinant or dual total')
    adj, fibres = blowup(out, weights)
    text = '\n'.join(''.join(map(str, row)) for row in adj) + '\n'
    require(text == (HERE / 'tournament24.txt').read_text(), 'literal tournament differs from quotient expansion')
    all_sizes = check_vertices(adj, fibres, sources, 1)
    balanced, fibres = blowup(out, weights, balanced=True)
    check_vertices(balanced, fibres, sources, 1)
    scaled, fibres = blowup(out, [2 * x for x in weights], balanced=True)
    check_vertices(scaled, fibres, sources, 2)
    # Negative fixtures exercise mathematical validation, without relying on assert.
    rejected = 0
    for bad_weights in ([0] + weights[1:], [True] + weights[1:]):
        try:
            blowup(out, bad_weights)
        except ValueError:
            rejected += 1
    bad_sources = [row[:] for row in sources]
    bad_sources[0] = [0]
    try:
        hall_rows(out, bad_sources)
    except ValueError:
        rejected += 1
    bad_out = [row[:] for row in out]
    bad_out[0].append(1)
    try:
        blowup(bad_out, weights)
    except ValueError:
        rejected += 1
    require(rejected == 4, 'malformed input accepted')
    damaged = [row[:] for row in adj]
    damaged[0] = [0] * len(adj)
    try:
        check_vertices(damaged, blowup(out, weights)[1], sources, 1)
    except ValueError:
        rejected += 1
    require(rejected == 5, 'damaged Hall certificate accepted')
    result = {
        'status': 'VERIFIED', 'order': 24, 'quotient_order': q,
        'weights': weights, 'hall_targets': targets, 'map_to_gibbons_labels': label_map, 'root_deficiencies': defects,
        'vertex_hall_sizes': all_sizes, 'determinant': int(det),
        'dual_multipliers': dual, 'dual_total': sum(dual),
        'balanced_degree_counts': {str(d): [sum(r) for r in balanced].count(d) for d in sorted(set(map(sum, balanced)))},
        'checked_vertices': 24 + 24 + 48, 'negative_cases_rejected': rejected,
        'symbolic_subsets_checked': subset_count, 'nonempty_closed_rows': 15,
        'tournament_sha256': hashlib.sha256(text.encode()).hexdigest(),
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
