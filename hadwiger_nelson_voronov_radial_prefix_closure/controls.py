#!/usr/bin/env python3
"""Independent floating-point control for the exact certificate."""

from collections import defaultdict, deque
import cmath
from itertools import combinations
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
phi0 = cmath.exp(1j * math.pi / 12)
phi1 = math.sqrt(6) / 3 + 1j * math.sqrt(3) / 3


def canonical(values, digits=10):
    result = {}
    for value in values:
        result.setdefault((round(value.real, digits),
                           round(value.imag, digits)), value)
    return tuple(result[key] for key in sorted(result))


m1 = canonical((0j,) + tuple(phi0 ** a * phi1 ** b
                             for a in range(24) for b in (-1, 0, 1)))
m2 = canonical(left + right for left in m1 for right in m1
               if abs(left + right) <= 1 + 1e-9)
assert (len(m1), len(m2)) == (73, 865)

shells = defaultdict(list)
for point in m2:
    shells[round(abs(point), 9)].append(point)
prefixes = []
accumulated = []
for radius in sorted(shells):
    accumulated.extend(shells[radius])
    prefixes.append((radius, canonical(accumulated)))
counts = [len(points) for _, points in prefixes]
assert counts == [1, 25, 73, 121, 145, 217, 241, 289, 337, 361,
                  433, 457, 505, 553, 577, 649, 673, 721, 769, 793, 865]

valid = []
for left in prefixes:
    for right in prefixes:
        nl, nr = len(left[1]), len(right[1])
        if nl >= nr and nl + nr - 1 <= 508:
            valid.append((left, right))
maximal = [pair for pair in valid if not any(
    len(other[0][1]) >= len(pair[0][1]) and
    len(other[1][1]) >= len(pair[1][1]) and
    (len(other[0][1]) > len(pair[0][1]) or
     len(other[1][1]) > len(pair[1][1]))
    for other in valid)]
pair_rows = sorted((len(left[1]), len(right[1]), left[0] + right[0])
                   for left, right in maximal)
assert [(left, right) for left, right, _ in pair_rows] == [
    (241, 241), (289, 217), (361, 145),
    (433, 73), (457, 25), (505, 1)]
assert max(total for _, _, total in pair_rows) < 1

k505 = next(points for _, points in prefixes if len(points) == 505)
edges = []
closest_nonedge = 1.0
largest_edge_error = 0.0
for left, right in combinations(range(len(k505)), 2):
    error = abs(abs(k505[left] - k505[right]) ** 2 - 1)
    if error < 1e-9:
        edges.append((left, right))
        largest_edge_error = max(largest_edge_error, error)
    else:
        closest_nonedge = min(closest_nonedge, error)
assert len(edges) == 216
assert closest_nonedge > 1e-5

adjacency = [[] for _ in k505]
for left, right in edges:
    adjacency[left].append(right)
    adjacency[right].append(left)
colours = [-1] * len(k505)
for root in range(len(k505)):
    if colours[root] >= 0:
        continue
    colours[root] = 0
    queue = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if colours[neighbour] < 0:
                colours[neighbour] = 1 - colours[vertex]
                queue.append(neighbour)
            else:
                assert colours[neighbour] != colours[vertex]

output = {
    "status": "controls_passed",
    "arithmetic": "independent complex double reconstruction",
    "m1_vertices": len(m1),
    "m2_vertices": len(m2),
    "shell_cumulative_counts": counts,
    "maximal_pairs_and_radius_sums": pair_rows,
    "k505_edges": len(edges),
    "largest_accepted_squared_distance_error": largest_edge_error,
    "closest_rejected_squared_distance_error": closest_nonedge,
    "k505_bipartite": True
}
(HERE / "CONTROLS.json").write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))
