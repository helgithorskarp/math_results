#!/usr/bin/env python3
"""Small arithmetic, source-validation, and colouring-search controls."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("pair_verify", HERE / "verify.py")
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def brute_extension(order, edges, terminals, pattern):
    return next((word for word in product(range(4), repeat=order)
                 if tuple(word[v] for v in terminals) == pattern
                 and all(word[i] != word[j] for i, j in edges)), None)


def controls():
    basis = [V.basis(i) for i in range(V.N)]
    arithmetic = 0
    modular = 0
    for x in basis:
        for y in basis:
            z = V.mul(x, y)
            need(V.bar(z) == V.mul(V.bar(x), V.bar(y)), "conjugation product")
            need(V.evaluate(z) == V.evaluate(x) * V.evaluate(y) % V.MOD,
                 "modular product")
            arithmetic += 1
            modular += 1
    source = json.loads(
        (V.ROOT / "hadwiger_nelson_snail_dihedral" / "seed.json").read_text()
    )
    bad = [list(row) for row in source["moser_rows"]]
    bad[0] = bad[0][:-1]
    rejected_source = False
    try:
        V.source_points(bad)
    except ValueError:
        rejected_source = True
    need(rejected_source, "malformed source accepted")

    # Compare deterministic extension discovery with brute force on all graphs
    # through four vertices and every consistent pin of vertices 0 and 1.
    search_cases = 0
    complete_edges = tuple(combinations(range(4), 2))
    for mask in range(1 << len(complete_edges)):
        edges = tuple(edge for i, edge in enumerate(complete_edges) if mask >> i & 1)
        for pattern in product(range(4), repeat=2):
            brute = brute_extension(4, edges, (0, 1), pattern)
            if brute is None:
                continue
            word, _ = V.find_extension(4, edges, (0, 1), pattern)
            need(tuple(word[v] for v in (0, 1)) == pattern, "control pins")
            need(all(word[i] != word[j] for i, j in edges), "control edge")
            search_cases += 1
    return {
        "verified": True,
        "basis_product_conjugation_checks": arithmetic,
        "basis_product_modular_checks": modular,
        "positive_small_graph_search_cases": search_cases,
        "malformed_source_rejected": rejected_source,
    }


if __name__ == "__main__":
    print(json.dumps(controls(), indent=2, sort_keys=True))
