#!/usr/bin/env python3
"""Standalone physical certificate verifier; no theorem/normalizer imports."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def read_graph(path):
    rows = [line.split() for line in Path(path).read_text().splitlines()]
    require(bool(rows) and len(rows[0]) == 2, "graph header")
    n, m = map(int, rows[0])
    require(1 <= n <= 63 and m >= 0 and len(rows) == m + 1, "graph dimensions")
    edges = set()
    for row in rows[1:]:
        require(len(row) == 2, "edge row")
        u, v = map(int, row)
        require(0 <= u < v < n and (u, v) not in edges, "edge domain")
        edges.add((u, v))
    return n, edges


def verify(n, edges, certificate):
    require(type(certificate) is dict, "certificate object")
    require(type(certificate.get("n")) is int and certificate["n"] == n,
            "certificate order")
    kind = certificate.get("kind")
    if kind == "monochromatic_five":
        require(set(certificate) == {"kind", "n", "color", "vertices"}, "five keys")
        color = certificate["color"]; s = certificate["vertices"]
        require(type(color) is int and color in (0, 1), "five color")
        require(type(s) is list and len(s) == 5 and all(type(v) is int and 0 <= v < n for v in s)
                and len(set(s)) == 5, "five vertices")
        require(all(int(tuple(sorted(e)) in edges) == color for e in it.combinations(s, 2)),
                "not monochromatic")
        return {"status": "VERIFIED_PHYSICAL_FIVE", "n": n, "color": color,
                "vertices": sorted(s)}
    require(kind == "pentagon_frame", "not a proof-bearing outcome")
    require(set(certificate) == {"kind", "n", "flip", "order"}, "frame keys")
    flip = certificate["flip"]; order = certificate["order"]
    require(type(flip) is int and flip in (0, 1), "flip domain")
    require(type(order) is list and len(order) == n and
            all(type(v) is int for v in order) and sorted(order) == list(range(n)),
            "not a vertex permutation")
    require(n >= 27, "frame order")
    moved = {pair: int(tuple(sorted((order[pair[0]], order[pair[1]]))) in edges) ^ flip
             for pair in it.combinations(range(n), 2)}
    # Explicitly construct required cycles by edges, not producer modulo arithmetic.
    required = {(0, 1): 1}
    required.update({(u, v): 1 for u in (0, 1) for v in range(2, 7)})
    for block in ([2, 3, 4, 5, 6], [7, 8, 9, 10, 11], [12, 13, 14, 15, 16],
                  [17, 18, 19, 20, 21], [22, 23, 24, 25, 26]):
        red = {tuple(sorted((block[i], block[(i + 1) % 5]))) for i in range(5)}
        required.update({pair: int(pair in red) for pair in it.combinations(block, 2)})
    require(len(required) == 61 and all(moved[e] == c for e, c in required.items()),
            "required frame pair fails")
    # Every pair, including every cross pair, is transported. Round-trip all of them.
    inverse = {old: new for new, old in enumerate(order)}
    require(all((moved[tuple(sorted((inverse[u], inverse[v])))] ^ flip) == int((u, v) in edges)
                for u, v in it.combinations(range(n), 2)), "transport round trip")
    packed = ''.join(str(c) for _, c in sorted(moved.items()))
    free = ''.join(str(c) for e, c in sorted(moved.items()) if e not in required)
    return {"status": "VERIFIED_PHYSICAL_FRAME", "n": n, "fixed_pairs": 61,
            "transported_pairs": len(moved), "free_variables": len(free),
            "normalized_edge_count": sum(moved.values()),
            "normalized_bitstring_sha256": hashlib.sha256(packed.encode()).hexdigest(),
            "free_bitstring_sha256": hashlib.sha256(free.encode()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(*read_graph(args.graph), json.loads(args.certificate.read_text())), sort_keys=True))
