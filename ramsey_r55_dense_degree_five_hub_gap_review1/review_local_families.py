#!/usr/bin/env python3
"""Independent literal audit of the 20-edge and 16-edge local families.

This reviewer program imports no submitted Python module.  It decodes the
two endpoint interfaces, derives every red-K4/blue-K5 clause from physical
subsets, performs subsumption, scans the complete Boolean cube, and checks
the submitted local certificates.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
FAMILIES = (
    {
        "label": "interfaces_1_2",
        "package": "ramsey_r55_type126_twenty_edge_kernel",
        "interfaces": (1, 2),
        "free": 20,
        "consensus_sha256": "cf3b3770875a7fc3737549be56e0c85747519052c807133ed0bef6796b40b82d",
        "certificate_sha256": "7f15ff1804647529b2bc6e60ea8298e8eb7af73c85c7833fcb7421cd3a89f6bc",
        "minimal": 37,
        "negative_lengths": {2: 29},
        "positive_lengths": {2: 2, 3: 2, 4: 2, 5: 2},
        "models": 434,
        "base": 99,
        "dense": [318252, 730323],
        "model_sha256": "99b93296ab9aa6ded652b5f24509465d25cb7810c196a71b22055d5194d06dcd",
    },
    {
        "label": "interfaces_3_4",
        "package": "ramsey_r55_type126_sixteen_edge_kernel",
        "interfaces": (3, 4),
        "free": 16,
        "consensus_sha256": "637c20a886d5a0d3cec87af9b096b0d48538872c9beb5e507d32179d2e2d35d6",
        "certificate_sha256": "5e61e574d1f88a62ab42d4eb91213ebac8c985fd14ab0e10d38f434fbf34cfdc",
        "minimal": 26,
        "negative_lengths": {2: 20, 3: 3},
        "positive_lengths": {2: 3},
        "models": 181,
        "base": 101,
        "dense": [27818, 37717],
        "model_sha256": "5c5f82175ea41fd9b54aa3d31a39597f415890eada945192c6b011500ad954f9",
    },
)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> set[tuple[int, int]]:
    require(record and all(63 <= ord(ch) <= 126 for ch in record), "invalid graph6 characters")
    order = ord(record[0]) - 63
    require(order == 22, "unexpected graph6 order")
    needed = order * (order - 1) // 2
    bits = "".join(f"{ord(ch) - 63:06b}" for ch in record[1:])
    require(len(bits) == ((needed + 5) // 6) * 6 and "1" not in bits[needed:], "bad graph6 length/padding")
    result: set[tuple[int, int]] = set()
    offset = 0
    for v in range(order):
        for u in range(v):
            if bits[offset] == "1":
                result.add((u, v))
            offset += 1
    return result


def derive_minimal_clauses(
    fixed: dict[tuple[int, int], int], variables: dict[tuple[int, int], int]
) -> set[frozenset[int]]:
    clauses: set[frozenset[int]] = set()
    # A red K4 is forbidden; a blue K5 is forbidden.
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
            if blocked:
                continue
            require(literals, "fixed partial interface already violates a Ramsey condition")
            clauses.add(frozenset(literals))
    return {row for row in clauses if not any(other < row for other in clauses)}


def enumerate_models(clauses: set[frozenset[int]], variable_count: int) -> list[int]:
    """Exhaust the full cube with bit-mask clause tests, independent of producer recursion."""
    encoded: list[tuple[int, int]] = []
    universe = (1 << variable_count) - 1
    for clause in clauses:
        positive = sum(1 << (literal - 1) for literal in clause if literal > 0)
        negative = sum(1 << (-literal - 1) for literal in clause if literal < 0)
        encoded.append((positive, negative))
    return [
        mask
        for mask in range(1 << variable_count)
        if all((mask & positive) or ((~mask & universe) & negative) for positive, negative in encoded)
    ]


def check_family(source: Path, inputs: dict, config: dict) -> dict:
    package = source / config["package"]
    consensus_path = package / "CONSENSUS.json"
    certificate_path = package / "LOCAL_CERTIFICATE.json"
    require(digest(consensus_path) == config["consensus_sha256"], f"{config['label']}: consensus identity")
    require(digest(certificate_path) == config["certificate_sha256"], f"{config['label']}: certificate identity")
    consensus = json.loads(consensus_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    first_index, second_index = config["interfaces"]
    require(consensus["interfaces"] == [first_index, second_index], f"{config['label']}: interface indices")

    permutation = consensus["second_to_first"]
    require(sorted(permutation) == list(range(22)), f"{config['label']}: relabeling is not bijective")
    require(
        set(permutation[:16]) == set(range(16))
        and set(permutation[16:21]) == set(range(16, 21))
        and permutation[21] == 21,
        f"{config['label']}: relabeling does not preserve A/S/z",
    )
    first = decode_graph6(inputs["interfaces"][first_index])
    second_original = decode_graph6(inputs["interfaces"][second_index])
    second = {tuple(sorted((permutation[u], permutation[v]))) for u, v in second_original}
    free_edges = sorted(first ^ second)
    declared_free = [tuple(edge) for edge in consensus["free_common_edges"]]
    require(len(first) == len(second) == 109, f"{config['label']}: endpoint density")
    require(free_edges == declared_free and len(free_edges) == config["free"], f"{config['label']}: exact disagreement set")
    require(all(u < 16 and 16 <= v < 21 for u, v in free_edges), f"{config['label']}: disagreement outside A-S")
    require(certificate["free_common_edges"] == consensus["free_common_edges"], f"{config['label']}: certificate edge order")

    free_set = set(free_edges)
    fixed = {
        edge: int(edge in first)
        for edge in combinations(range(22), 2)
        if edge not in free_set
    }
    variables = {edge: i for i, edge in enumerate(free_edges, 1)}
    minimal = derive_minimal_clauses(fixed, variables)
    negative = sorted(tuple(sorted(-literal for literal in row)) for row in minimal if all(x < 0 for x in row))
    positive = sorted(tuple(sorted(row)) for row in minimal if all(x > 0 for x in row))
    require(not any(any(x < 0 for x in row) and any(x > 0 for x in row) for row in minimal), f"{config['label']}: mixed minimal clause")
    require(len(minimal) == config["minimal"], f"{config['label']}: minimal clause count")
    require(dict(Counter(map(len, negative))) == config["negative_lengths"], f"{config['label']}: negative clause profile")
    require(dict(Counter(map(len, positive))) == config["positive_lengths"], f"{config['label']}: positive clause profile")
    if config["free"] == 20:
        expected_negative = sorted(tuple(row) for row in certificate["conflict_edges"])
    else:
        expected_negative = sorted(tuple(row) for row in certificate["forbidden_hyperedges"])
    require(negative == expected_negative, f"{config['label']}: displayed forbidden family")
    require(positive == sorted(tuple(row) for row in certificate["required_meeting_sets"]), f"{config['label']}: displayed meeting family")

    models = enumerate_models(minimal, config["free"])
    stream = "".join(f"{model}\n" for model in models).encode()
    require(len(models) == config["models"] and models == certificate["models"], f"{config['label']}: complete model stream")
    require(sha256(stream).hexdigest() == config["model_sha256"] == certificate["model_sha256"], f"{config['label']}: model stream hash")
    base = sum(fixed.values())
    histogram = dict(sorted(Counter(base + model.bit_count() for model in models).items()))
    require(base == config["base"] == certificate["fixed_red_base"], f"{config['label']}: fixed red base")
    require({str(k): v for k, v in histogram.items()} == certificate["density_histogram"], f"{config['label']}: density histogram")
    dense = [model for model in models if base + model.bit_count() == 109]
    endpoint_masks = sorted(
        sum(1 << (variables[edge] - 1) for edge in variables if edge in graph)
        for graph in (first, second)
    )
    require(dense == endpoint_masks == config["dense"] == certificate["dense_models"], f"{config['label']}: dense endpoints")

    for model in models:
        degrees = [0] * 22
        for edge in combinations(range(22), 2):
            red = fixed.get(edge)
            if red is None:
                red = bool(model & (1 << (variables[edge] - 1)))
            if red:
                degrees[edge[0]] += 1
                degrees[edge[1]] += 1
        require([v for v, degree in enumerate(degrees) if degree == 5] == [21], f"{config['label']}: unique hub")

    result = {
        "dense_models": dense,
        "density_histogram": {str(k): v for k, v in histogram.items()},
        "fixed_red_base": base,
        "free_edges": config["free"],
        "minimal_clauses": len(minimal),
        "model_sha256": sha256(stream).hexdigest(),
        "valid_local_fillings": len(models),
    }
    if config["free"] == 16:
        triples = [row for row in negative if len(row) == 3]
        pair_only = set(minimal) - {frozenset(-x for x in row) for row in triples}
        pair_only_models = enumerate_models(pair_only, config["free"])
        require(len(pair_only_models) == certificate["triple_necessity"]["pair_only_model_count"] == 203, "interfaces_3_4: pair-only count")
        witnesses = certificate["triple_necessity"]["witnesses"]
        require([tuple(row["removed_hyperedge"]) for row in witnesses] == triples, "interfaces_3_4: triple witness order")
        for item in witnesses:
            removed = frozenset(-x for x in item["removed_hyperedge"])
            relaxed = minimal - {removed}
            relaxed_models = enumerate_models(relaxed, config["free"])
            exceptions = sorted(set(relaxed_models) - set(models))
            require(len(exceptions) == item["witnesses_without_this_triple"], "interfaces_3_4: omitted-triple count")
            mask = item["mask"]
            require(mask in exceptions and mask.bit_count() == item["minimum_red_positions"], "interfaces_3_4: witness mask")
            red_four = [int(x) for x in item["red_four"]]
            require(len(red_four) == 4, "interfaces_3_4: malformed red-four witness")
            for edge in combinations(red_four, 2):
                value = fixed.get(edge)
                if value is None:
                    value = bool(mask & (1 << (variables[edge] - 1)))
                require(value == 1, "interfaces_3_4: triple witness is not a red K4")
        result["pair_only_models"] = len(pair_only_models)
        result["essential_triples"] = len(triples)
    result["status"] = "VERIFIED_INDEPENDENT_LOCAL_FAMILY"
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="root of pinned math_source_code_open checkout")
    args = parser.parse_args()
    inputs_path = args.source / "ramsey_r55_dense_degree23_hub_classification" / "inputs.json"
    require(digest(inputs_path) == INPUTS_SHA256, "upstream inputs identity")
    inputs = json.loads(inputs_path.read_text())
    result = {config["label"]: check_family(args.source, inputs, config) for config in FAMILIES}
    result["status"] = "VERIFIED_BOTH_LOCAL_FAMILIES"
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
