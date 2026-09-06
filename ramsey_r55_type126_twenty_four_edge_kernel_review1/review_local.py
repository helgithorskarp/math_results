#!/usr/bin/env python3
"""Independent local audit of the submitted 24-edge partial graph.

No submitted Python module is imported.  The checker decodes the two source
interfaces, derives the physical Ramsey clauses on 22 vertices, removes
subsumed clauses, enumerates all models with a generic partial-clause search,
and verifies the claimed local census and dense endpoints.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


EXPECTED_SHA256 = {
    "inputs": "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2",
    "consensus": "7fa72225a69391ada04c0828529764320bc3b061fc91103d40c26a4b9c3018ad",
    "certificate": "9ee093415a0308eecf5bbec8b1b54e64b7fed0550308f85786a9c0a1bcedb506",
}


def fail(message: str) -> None:
    raise ValueError(message)


def decode_graph6(record: str) -> tuple[int, set[tuple[int, int]]]:
    if not record or any(not 63 <= ord(ch) <= 126 for ch in record):
        fail("invalid graph6 characters")
    order = ord(record[0]) - 63
    if not 0 <= order < 63:
        fail("only short graph6 records are accepted")
    needed = order * (order - 1) // 2
    bits = "".join(f"{ord(ch) - 63:06b}" for ch in record[1:])
    if len(bits) != ((needed + 5) // 6) * 6 or any(ch == "1" for ch in bits[needed:]):
        fail("invalid graph6 length or padding")
    edges: set[tuple[int, int]] = set()
    offset = 0
    for v in range(order):
        for u in range(v):
            if bits[offset] == "1":
                edges.add((u, v))
            offset += 1
    return order, edges


def derive_minimal_clauses(
    fixed: dict[tuple[int, int], int], variables: dict[tuple[int, int], int]
) -> set[tuple[int, ...]]:
    clauses: set[tuple[int, ...]] = set()
    for size, wanted, sign in ((4, 1, -1), (5, 0, 1)):
        for vertices in combinations(range(22), size):
            literals: list[int] = []
            blocked = False
            for edge in combinations(vertices, 2):
                if edge in fixed:
                    if fixed[edge] != wanted:
                        blocked = True
                        break
                else:
                    literals.append(sign * variables[edge])
            if not blocked:
                if not literals:
                    fail("fixed partial graph already violates a Ramsey condition")
                clauses.add(tuple(literals))
    frozen = [(clause, frozenset(clause)) for clause in clauses]
    return {
        clause
        for clause, members in frozen
        if not any(other_members < members for other, other_members in frozen if other != clause)
    }


def enumerate_models(clauses: set[tuple[int, ...]], variable_count: int) -> list[int]:
    """Generic clause search; assignments use bit i for DIMACS variable i+1."""
    rows = tuple(tuple(clause) for clause in clauses)
    models: list[int] = []

    def visit(variable: int, true_mask: int) -> None:
        assigned_mask = (1 << variable) - 1
        for clause in rows:
            satisfied = False
            unresolved = False
            for literal in clause:
                bit = 1 << (abs(literal) - 1)
                if not assigned_mask & bit:
                    unresolved = True
                elif (literal > 0) == bool(true_mask & bit):
                    satisfied = True
                    break
            if not satisfied and not unresolved:
                return
        if variable == variable_count:
            models.append(true_mask)
            return
        visit(variable + 1, true_mask)
        visit(variable + 1, true_mask | (1 << variable))

    visit(0, 0)
    return sorted(models)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", type=Path, help="upstream dense-hub inputs.json")
    parser.add_argument("consensus", type=Path, help="submitted CONSENSUS.json")
    parser.add_argument("certificate", type=Path, help="submitted LOCAL_CERTIFICATE.json")
    args = parser.parse_args()

    paths = {"inputs": args.inputs, "consensus": args.consensus, "certificate": args.certificate}
    for label, path in paths.items():
        if sha256(path.read_bytes()).hexdigest() != EXPECTED_SHA256[label]:
            fail(f"unexpected {label} file identity")
    inputs = json.loads(args.inputs.read_text())
    consensus = json.loads(args.consensus.read_text())
    certificate = json.loads(args.certificate.read_text())
    if consensus.get("interfaces") != [10, 11]:
        fail("wrong interface pair")
    permutation = consensus.get("second_to_first")
    if not isinstance(permutation, list) or sorted(permutation) != list(range(22)):
        fail("invalid interface relabeling")
    if set(permutation[:16]) != set(range(16)) or set(permutation[16:21]) != set(range(16, 21)) or permutation[21] != 21:
        fail("relabeling does not preserve the distinguished cells")

    n1, first = decode_graph6(inputs["interfaces"][10])
    n2, second_original = decode_graph6(inputs["interfaces"][11])
    second = {tuple(sorted((permutation[u], permutation[v]))) for u, v in second_original}
    free_edges = sorted(first ^ second)
    declared_free = [tuple(edge) for edge in consensus.get("free_common_edges", [])]
    if n1 != 22 or n2 != 22 or len(first) != 109 or len(second) != 109:
        fail("source interface order or density mismatch")
    if free_edges != declared_free or len(free_edges) != 24:
        fail("the declared 24-edge family is not the exact endpoint consensus")
    if any(not (u < 16 <= v < 21) for u, v in free_edges):
        fail("a disagreement lies outside the A-to-S attachment rectangle")

    fixed = {
        edge: int(edge in first)
        for edge in combinations(range(22), 2)
        if edge not in set(free_edges)
    }
    variables = {edge: index for index, edge in enumerate(free_edges, 1)}
    minimal = derive_minimal_clauses(fixed, variables)
    negative_pairs = sorted(tuple(sorted(-literal for literal in clause)) for clause in minimal if all(literal < 0 for literal in clause))
    positive_rows = sorted(tuple(clause) for clause in minimal if all(literal > 0 for literal in clause))
    if len(minimal) != 40 or len(negative_pairs) != 30 or any(len(row) != 2 for row in negative_pairs):
        fail("unexpected minimal negative-clause family")
    if len(positive_rows) != 10 or Counter(map(len, positive_rows)) != {2: 2, 3: 6, 4: 1, 6: 1}:
        fail("unexpected minimal positive-clause family")
    if any(any(literal < 0 for literal in clause) and any(literal > 0 for literal in clause) for clause in minimal):
        fail("unexpected mixed minimal clause")

    models = enumerate_models(minimal, len(variables))
    if len(models) != 995:
        fail(f"wrong local model count: {len(models)}")
    stream = "".join(f"{model}\n" for model in models).encode()
    if models != certificate.get("models") or sha256(stream).hexdigest() != certificate.get("model_sha256"):
        fail("local model stream differs from the submitted certificate")

    base_density = sum(fixed.values())
    histogram = dict(sorted(Counter(base_density + model.bit_count() for model in models).items()))
    if base_density != 97 or {str(k): v for k, v in histogram.items()} != certificate.get("density_histogram"):
        fail("density polynomial mismatch")
    dense_models = [model for model in models if base_density + model.bit_count() == 109]
    endpoint_masks = sorted(
        sum(1 << (variables[edge] - 1) for edge in variables if edge in graph)
        for graph in (first, second)
    )
    if dense_models != endpoint_masks or dense_models != certificate.get("dense_models"):
        fail("density-109 endpoints mismatch")

    for model in models:
        degrees = [0] * 22
        for edge in combinations(range(22), 2):
            red = fixed.get(edge)
            if red is None:
                red = bool(model & (1 << (variables[edge] - 1)))
            if red:
                degrees[edge[0]] += 1
                degrees[edge[1]] += 1
        if [vertex for vertex, degree in enumerate(degrees) if degree == 5] != [21]:
            fail("a local model does not have the claimed unique degree-five hub")

    result = {
        "dense_models": dense_models,
        "density_histogram": {str(k): v for k, v in histogram.items()},
        "fixed_red_base": base_density,
        "free_edges": len(free_edges),
        "minimal_clauses": len(minimal),
        "model_sha256": sha256(stream).hexdigest(),
        "status": "VERIFIED_LOCAL_24_EDGE_FAMILY",
        "valid_local_fillings": len(models),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
