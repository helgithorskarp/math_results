#!/usr/bin/env python3
"""Exhaustive small controls for factorization and sparse-minimum normalization."""

from __future__ import annotations

import itertools
import json

import factorization


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    graph_words = root_audits = normalization_audits = 0
    for n in range(1, 7):
        edge_count = n * (n - 1) // 2
        edge_list = list(itertools.combinations(range(n), 2))
        for word in range(1 << edge_count):
            bits = [(word >> i) & 1 for i in range(edge_count)]
            matrix = factorization.matrix_of(n, bits)
            for root in range(n):
                report = factorization.audit(n, bits, root)
                require(report["factorization_identity"], "factorization identity failed")
                root_audits += 1

            red_edges = sum(bits)
            if 2 * red_edges > edge_count:
                bits = [1 - bit for bit in bits]
                matrix = factorization.matrix_of(n, bits)
                red_edges = edge_count - red_edges
            degrees = [sum(row) for row in matrix]
            root = min(range(n), key=degrees.__getitem__)
            require(2 * red_edges <= edge_count, "sparse orientation failed")
            require(degrees[root] == min(degrees), "minimum root failed")
            require(degrees[root] * n <= 2 * red_edges, "average-degree bound failed")
            normalization_audits += 1
            graph_words += 1

    expected = {
        18: (429, 432, 64758),
        19: (424, 437, 58008),
        20: (421, 440, 53998),
    }
    for branch in factorization.target_spec()["branches"]:
        degree = branch["root_degree"]
        require((branch["master_internal_variables"],
                 branch["inner_cross_variables"],
                 branch["master_link_clauses"]) == expected[degree],
                "target specification differs")
        require(branch["free_variables_after_root_fixing"] == 861,
                "free variable partition failed")
        require(branch["physical_edge_coordinates_total"] == 903,
                "physical variable partition failed")

    print(json.dumps({
        "status": "PASS",
        "exhaustive_graph_words": graph_words,
        "root_factorization_audits": root_audits,
        "sparse_minimum_normalization_audits": normalization_audits,
        "target_branches": 3,
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
