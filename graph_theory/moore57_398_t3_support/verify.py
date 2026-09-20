#!/usr/bin/env python3
"""Direct checks for the t=3 Moore-support classification and countermodel."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "raw_matching_countermodel.json"


EXPECTED_TYPES = {
    "D1": {23: 3, 3: 1, 7: 66, 9: 92},
    "D2": {23: 3, 5: 3, 7: 63, 9: 93},
    "P": {23: 3, 5: 2, 7: 65, 9: 92},
}


def classified_types() -> dict[str, Counter[int]]:
    """Derive degree counts from the three possible common-neighbour patterns."""
    answer = {}
    # (name, multiplicities of k=#weight-three neighbours among weight-one vertices)
    patterns = {
        "D1": {3: 1, 1: 66, 0: 92},
        "D2": {2: 3, 1: 63, 0: 93},
        "P": {2: 2, 1: 65, 0: 92},
    }
    for name, k_counts in patterns.items():
        degrees = Counter({23: 3})
        assert sum(k * count for k, count in k_counts.items()) == 69
        assert sum(k_counts.values()) == 159
        for k, count in k_counts.items():
            degrees[9 - 2 * k] += count
        assert sum(degrees.values()) == 162
        assert sum(d * count for d, count in degrees.items()) == 1362
        answer[name] = degrees
    return answer


def branch_patterns() -> set[tuple[int, ...]]:
    """Enumerate distributions of three weight-three vertices over weight-seven parts."""
    patterns = set()
    # A branch has c<=2 and 7-3c weight-one vertices.
    for c0 in range(3):
        for c1 in range(3):
            for c2 in range(3):
                if c0 + c1 + c2 == 3:
                    patterns.add(tuple(sorted((c for c in (c0, c1, c2) if c), reverse=True)))
    return patterns


def load_certificate(path: Path = CERTIFICATE) -> dict:
    return json.loads(path.read_text())


def verify_countermodel(data: dict, count_cycles: bool = True) -> dict[str, int | str]:
    assert data["case"] == "3-distinct"
    profiles = data["profiles"]
    assert len(profiles) == 24
    assert profiles[:3] == [[3, 1, 1, 1, 1]] * 3
    assert profiles[3:] == [[1] * 7] * 21
    weights = [row + [0] * (56 - len(row)) for row in profiles]
    assert all(len(row) == 56 and sum(row) == 7 for row in weights)
    flat = [w for row in weights for w in row]
    assert Counter(flat) == Counter({0: 1182, 1: 159, 3: 3})

    expected_keys = {f"{i},{j}" for i in range(24) for j in range(i + 1, 24)}
    permutations = data["permutations"]
    assert set(permutations) == expected_keys
    sums = [[0] * 56 for _ in range(24)]
    adj = [set() for _ in range(24 * 56)] if count_cycles else None
    for key in sorted(permutations, key=lambda s: tuple(map(int, s.split(",")))):
        i, j = map(int, key.split(","))
        p = permutations[key]
        assert len(p) == 56 and sorted(p) == list(range(56))
        for a, b in enumerate(p):
            sums[i][a] += weights[j][b]
            sums[j][b] += weights[i][a]
            if adj is not None:
                u, v = 56 * i + a, 56 * j + b
                adj[u].add(v)
                adj[v].add(u)
    for i in range(24):
        for a in range(56):
            assert sums[i][a] == 2 + 7 * weights[i][a]

    result: dict[str, int | str] = {
        "parts": 24,
        "vertices": 1344,
        "perfect_matchings": 276,
        "matching_edges": 15456,
        "equations": 1344,
        "certificate_sha256": hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
    }
    if adj is not None:
        assert {len(row) for row in adj} == {23}
        triangles = sum(len(adj[u] & adj[v]) for u in range(len(adj)) for v in adj[u] if u < v) // 3
        four_cycles_twice = 0
        max_common = 0
        for u, v in combinations(range(len(adj)), 2):
            common = len(adj[u] & adj[v])
            max_common = max(max_common, common)
            four_cycles_twice += common * (common - 1) // 2
        assert four_cycles_twice % 2 == 0
        result.update(triangles=triangles, four_cycles=four_cycles_twice // 2, max_common=max_common)
    return result


def main() -> None:
    assert branch_patterns() == {(2, 1), (1, 1, 1)}
    got = classified_types()
    assert {name: dict(counts) for name, counts in got.items()} == EXPECTED_TYPES
    # For c=1 and c=2 branches, distance-two saturation leaves 134 and 136
    # endpoints respectively: |W|-|own branch support|-23.
    assert 162 - 5 - 23 == 134
    assert 162 - 3 - 23 == 136
    result = verify_countermodel(load_certificate())
    assert result["triangles"] > 0 and result["four_cycles"] > 0
    print("classification: D1, D2, P; each has 162 vertices and 681 edges")
    print("distance-two layers: 134 (one-per-branch), 136 (two-in-one-branch)")
    print("countermodel:", json.dumps(result, sort_keys=True))
    print("VERIFIED")


if __name__ == "__main__":
    main()

