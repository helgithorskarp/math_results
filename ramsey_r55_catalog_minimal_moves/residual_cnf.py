#!/usr/bin/env python3
"""Emit the nonzero radius-seven residual after forbidding minimal moves."""

import argparse
import csv
import hashlib
from itertools import combinations
from pathlib import Path

from analyze_minimal_moves import HERE, ROOT, direct


def residual_clauses(graph, radius, forbidden, clique_order=5):
    n = len(graph)
    pairs = [(u, v) for v in range(1, n) for u in range(v)]
    number = {pair: i + 1 for i, pair in enumerate(pairs)}
    m = len(pairs)
    levels = radius + 1

    def threshold(i, level):
        return m + 1 + levels * i + level - 1

    for i in range(m):
        yield (-i-1, threshold(i, 1))
        if i:
            for level in range(1, levels+1):
                yield (-threshold(i-1, level), threshold(i, level))
            for level in range(2, levels+1):
                yield (-i-1, -threshold(i-1, level-1), threshold(i, level))
    yield (-threshold(m-1, levels),)
    for vertices in combinations(range(n), clique_order):
        present, absent = [], []
        for u, v in combinations(vertices, 2):
            (present if graph[u] & (1 << v) else absent).append(number[u,v])
        if len(absent) <= radius:
            yield tuple(present) + tuple(-x for x in absent)
        if len(present) <= radius:
            yield tuple(-x for x in present) + tuple(absent)
    yield tuple(range(1, m+1))  # Exclude the zero move.
    for edges in forbidden:
        yield tuple(-number[edge] for edge in edges)


def small_test():
    # All 1024 flip assignments on this five-vertex Ramsey graph, four radii.
    n = 5
    graph = [0]*n
    for u, v in [(0,1),(1,2),(2,3),(3,4),(0,4)]:
        graph[u] |= 1 << v
        graph[v] |= 1 << u
    pairs = [(u,v) for v in range(1,n) for u in range(v)]
    forbidden = [((0,1),), ((0,2),(1,3))]
    tested = positive = 0
    for radius in [1,2,3,4]:
        clauses = list(residual_clauses(graph, radius, forbidden, clique_order=3))
        m = len(pairs)
        for mask in range(1 << m):
            values = {i+1: bool(mask & (1 << i)) for i in range(m)}
            prefix = 0
            for i in range(m):
                prefix += values[i+1]
                for level in range(1, radius+2):
                    values[m+1+(radius+1)*i+level-1] = prefix >= level
            actual = all(any(values[abs(x)] == (x > 0) for x in clause) for clause in clauses)
            flipped = {pair for i,pair in enumerate(pairs) if mask & (1 << i)}
            changed = graph.copy()
            for u,v in flipped:
                changed[u] ^= 1 << v
                changed[v] ^= 1 << u
            expected = (0 < len(flipped) <= radius
                        and not any(set(f) <= flipped for f in forbidden)
                        and not direct.contains_clique(changed, 3)
                        and not direct.contains_clique(direct.complement(changed), 3))
            if actual != expected:
                raise RuntimeError(("small encoding mismatch", radius, mask))
            tested += 1
            positive += expected
    if not 0 < positive < tested:
        raise RuntimeError("small tests must cover positive and negative assignments")
    print(f"canonical_threshold_extension_checks={tested} positives={positive} PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--parent", type=int)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.self_test:
        small_test()
        return
    if args.parent is None or not 0 <= args.parent < 328 or args.output is None:
        parser.error("provide --parent in 0..327 and --output")
    certificate = HERE / "MINIMAL_MOVES.tsv"
    # The analysis command derives this certificate from the pinned maps.
    if hashlib.sha256(certificate.read_bytes()).hexdigest() != "27bfe713c711ab319bb9eb909cec997049e48c68e22539bbb54f543daea68896":
        raise RuntimeError("minimal-move certificate hash")
    with certificate.open() as stream:
        rows = [r for r in csv.DictReader(stream, delimiter="\t") if int(r['parent']) == args.parent]
    forbidden = [tuple(direct.parse_edge(s) for s in r['flips'].split(';')) for r in rows]
    if not 2 <= len(forbidden) <= 9 or any(len(f) not in (1,4) for f in forbidden):
        raise RuntimeError("unexpected forbidden supports")
    catalog = ROOT / "ramsey_r55_catalog_edge_radius6_classification/r55_42some.g6"
    if hashlib.sha256(catalog.read_bytes()).hexdigest() != "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb":
        raise RuntimeError("catalog hash")
    graph = direct.decode_graph6(catalog.read_text().splitlines()[args.parent])
    nvars, count = 7749, 0
    header = f"p cnf {0:12d} {0:12d}\n"
    with args.output.open("w+", encoding="ascii", newline="\n") as output:
        output.write(header)
        for clause in residual_clauses(graph, 7, forbidden):
            output.write(" ".join(map(str, clause)) + " 0\n")
            count += 1
        output.seek(0)
        output.write(f"p cnf {nvars:12d} {count:12d}\n")
    sha = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(f"parent={args.parent} variables={nvars} clauses={count} "
          f"minimal_blocks={len(forbidden)} sha256={sha}")


if __name__ == "__main__":
    main()
