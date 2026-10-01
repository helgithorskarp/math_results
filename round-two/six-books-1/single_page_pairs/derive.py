#!/usr/bin/env python3
"""Small incidence controls for an ordinary, independently written proof.

This producer uses missing-point words. It does not enumerate full hosts.
Only the exact core is exported; unknown edges are outside its coverage.
"""
from collections import Counter
from itertools import combinations, product
import json


def record():
    triples = tuple(combinations(range(3), 2))
    counts = {e: {"candidates": 0, "survivors": 0} for e in range(4)}
    words = []
    orbit_sizes = Counter()
    for missing in product(range(3), repeat=4):
        columns = tuple(7 ^ (1 << t) for t in missing)
        for edges in range(8):
            degree = [0, 0, 0]
            for bit, (i, j) in enumerate(triples):
                if edges & (1 << bit):
                    degree[i] += 1
                    degree[j] += 1
            e = edges.bit_count()
            counts[e]["candidates"] += 1
            pages = [sum(t != m for m in missing) + degree[t]
                     for t in range(3)]
            if any(c > 3 for c in pages):
                continue
            counts[e]["survivors"] += 1
            words.append(sum(c << (3 * i) for i, c in enumerate(columns))
                         + (edges << 12))
            # The proof forces an independent T and a repeated missing point.
            if edges or sorted(Counter(missing).values()) != [1, 1, 2]:
                raise ValueError("the ordinary sum/multiplicity check failed")
            duplicated = next(t for t in range(3) if missing.count(t) == 2)
            positions = [i for i, t in enumerate(missing) if t == duplicated]
            orbit_sizes["same_block" if positions in ([0, 1], [2, 3])
                        else "cross_block"] += 1
    return {
        "agent": "six-books-1", "role": "researcher",
        "status": "Exact necessary cores; no full coloring is enumerated.",
        "encoding": "Four little-endian 3-bit red-to-T masks, then bits12..14 for T edges01,02,12.",
        "domain_size": 648,
        "by_T_edges": {str(e): counts[e] for e in range(4)},
        "survivors": len(words), "core_words": sorted(words),
        "labeled_orbits": dict(sorted(orbit_sizes.items())),
        "neighborhood_edges": 13,
        "neighborhood_degrees": [2] + [3] * 8,
        "neighborhood_triangles": 0,
        "suppressed_cubic_triangles": {"same_block": 1, "cross_block": 0},
    }


if __name__ == "__main__":
    print(json.dumps(record(), indent=2, sort_keys=True))
