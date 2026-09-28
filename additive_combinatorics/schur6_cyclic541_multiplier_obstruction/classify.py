#!/usr/bin/env python3
"""Exact orbit-hypergraph enumeration; Python 3.11+, standard library only."""
import hashlib
import itertools
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def orbit_hypergraph(p, h):
    require(p > 2 and all(p % d for d in range(2, math.isqrt(p) + 1)), "not prime")
    h = set(h)
    require(1 in h and p - 1 in h and all(0 < x < p for x in h), "bad subgroup")
    require(all(x * y % p in h for x in h for y in h), "not closed")
    orbits, owner = [], {}
    for x in range(1, p):
        if x in owner:
            continue
        orbit = tuple(sorted(x * a % p for a in h))
        for y in orbit:
            require(y not in owner, "overlapping cosets")
            owner[y] = len(orbits)
        orbits.append(orbit)
    edges = {
        tuple(sorted({owner[x], owner[y], owner[(x + y) % p]}))
        for x in range(1, p)
        for y in range(x, p)
        if (x + y) % p
    }
    return orbits, edges


def enumerate_normalized(orbits, edges, target):
    """All independent target-sets containing orbit 0, not just a witness."""
    n = len(orbits)
    require(1 <= target <= n, "invalid target")
    forbidden = 0
    pair = [0] * n
    triple = [[0] * n for _ in range(n)]
    for edge in edges:
        if len(edge) == 1:
            forbidden |= 1 << edge[0]
        elif len(edge) == 2:
            a, b = edge
            pair[a] |= 1 << b
            pair[b] |= 1 << a
        else:
            for a, b, c in itertools.permutations(edge):
                triple[a][b] |= 1 << c
    nodes, answers = 0, []

    def visit(chosen, candidates):
        nonlocal nodes
        nodes += 1
        if len(chosen) == target:
            answers.append(tuple(chosen))
            return
        while candidates and len(chosen) + candidates.bit_count() >= target:
            bit = candidates & -candidates
            candidates ^= bit
            v = bit.bit_length() - 1
            blocked = pair[v]
            for u in chosen:
                blocked |= triple[u][v]
            visit(chosen + [v], candidates & ~blocked)

    if not forbidden & 1:
        visit([0], ((1 << n) - 1) & ~1 & ~forbidden & ~pair[0])
    return answers, nodes


def scaling_classes(p, orbits, normalized):
    owner = {x: i for i, orbit in enumerate(orbits) for x in orbit}
    representatives = set()
    all_sets = set()
    sizes = {}
    for selected in normalized:
        images = {
            tuple(sorted(owner[a * orbits[i][0] % p] for i in selected))
            for a in range(1, p)
        }
        canonical = min(images)
        representatives.add(canonical)
        all_sets.update(images)
        sizes[canonical] = len(images)
    return sorted(representatives), all_sets, sizes


def run():
    p = 541
    # -48 has order 10; closure, cardinality, and the subgroup are checked.
    h = sorted({pow(493, j, p) for j in range(10)})
    require(len(h) == 10 and pow(493, 10, p) == 1, "wrong order")
    orbits, edges = orbit_hypergraph(p, h)
    eight, nodes8 = enumerate_normalized(orbits, edges, 8)
    nine, nodes9 = enumerate_normalized(orbits, edges, 9)
    require(not nine and eight, "claimed maximum failed")
    classes, all_sets, sizes = scaling_classes(p, orbits, eight)
    representatives = [[orbits[i][0] for i in c] for c in classes]
    fixture = json.loads(Path(__file__).with_name("extremal_representatives.json").read_text())
    require(fixture == {"modulus": p, "subgroup": h, "representatives": representatives},
            "extremal fixture mismatch")
    raw = json.dumps(eight, separators=(",", ":")).encode()
    report = {
        "modulus": p,
        "subgroup": h,
        "cosets": len(orbits),
        "hyperedges_by_size": {str(k): sum(len(e) == k for e in edges) for k in (1, 2, 3)},
        "maximum_cosets": 8,
        "maximum_residues": 80,
        "normalized_maximum_sets": len(eight),
        "maximum_sets": len(all_sets),
        "scaling_classes": len(classes),
        "class_sizes": [sizes[c] for c in classes],
        "normalized_catalog_sha256": hashlib.sha256(raw).hexdigest(),
        "enumeration_nodes_target8": nodes8,
        "enumeration_nodes_target9": nodes9,
    }
    return report, eight


if __name__ == "__main__":
    print(json.dumps(run()[0], indent=2, sort_keys=True))
