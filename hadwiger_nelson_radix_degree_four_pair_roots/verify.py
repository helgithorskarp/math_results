#!/usr/bin/env python3
"""Solver-free exact verifier for the degree-four pair-root certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp

import produce


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(residual_path, certificate_path):
    residual = json.loads(Path(residual_path).read_text())
    certificate = json.loads(Path(certificate_path).read_text())
    require(residual["schema"] == "hn-radix-complete-pair-propagation-v1", "residual schema")
    require(certificate["schema"] == "hn-radix-degree-four-pair-roots-v1", "certificate schema")
    require(certificate["source_residual_sha256"] == produce.digest(residual), "residual digest")

    rows, _events, factors, factor_edges, base_edges, collisions, _simple, _circle = produce.architecture.build()
    del rows
    degrees = [produce.architecture.degree(factor) for factor in factors]
    require(certificate["curve_inventory_sha256"] == produce.architecture.digest(factors), "curve inventory")
    pairs = [
        row for row in residual["remaining_six"]
        if 4 in (degrees[row[0]], degrees[row[1]])
    ]
    require(len(pairs) == 160, "degree-four pair count")
    require(
        all(
            row[2] == 1
            and degrees[row[0]] * degrees[row[1]] == 2 * row[3]
            and row[3] <= 16
            for row in pairs
        ),
        "degree-four pair invariants",
    )
    require(certificate["pair_count"] == len(pairs), "certificate pair count")
    require(certificate["pair_sha256"] == produce.digest(pairs), "pair digest")
    require(certificate["maximum_bezout_allowance"] == max(row[3] for row in pairs), "maximum allowance")
    require(certificate["total_bezout_allowance"] == sum(row[3] for row in pairs), "total allowance")
    degree_histogram = {
        f"{left}_{right}": count
        for (left, right), count in sorted(
            Counter((degrees[row[0]], degrees[row[1]]) for row in pairs).items()
        )
    }
    require(certificate["degree_pair_histogram"] == degree_histogram, "degree histogram")

    x, y, s = sp.symbols("x y s")
    factor_expressions = [produce.expression(factor, x, y) for factor in factors]
    collision_sparse = list(map(produce.collision_parts, collisions))
    expected_sources = defaultdict(list)
    expected_data = {}
    expected_pair_rows = []
    complex_components = 0
    for row in pairs:
        a, b = row[:2]
        keys = []
        for q, xx, yy in produce.generic_components(
            factor_expressions[a], factor_expressions[b], x, y, s
        ):
            real_roots = int(q.count_roots(-sp.oo, sp.oo))
            if not real_roots:
                complex_components += 1
                continue
            key = produce.component_key(q, xx, yy, s)
            expected_sources[key].append([a, b])
            expected_data[key] = (q, xx, yy, real_roots)
            keys.append(produce.digest(key))
        expected_pair_rows.append({"pair": [a, b], "real_component_keys": keys})
    require(certificate["pair_components"] == expected_pair_rows, "pair-component decomposition")
    require(
        certificate["complex_only_irreducible_components"] == complex_components,
        "complex-only count",
    )

    certified = {row["component_key"]: row for row in certificate["components"]}
    require(len(certified) == len(certificate["components"]), "duplicate component key")
    require(set(certified) == {produce.digest(key) for key in expected_data}, "component key set")
    active_histogram = Counter()
    chromatic_histogram = Counter()
    real_embeddings = 0
    for key in sorted(expected_data):
        q, xx, yy, real_roots = expected_data[key]
        row = certified[produce.digest(key)]
        require(row["q"] == list(key[0]), "q encoding")
        require(row["x"] == list(key[1]), "x encoding")
        require(row["y"] == list(key[2]), "y encoding")
        require(row["source_pairs"] == sorted(expected_sources[key]), "component sources")
        require(row["real_embeddings"] == real_roots, "Sturm real-root count")

        evaluates_to_zero = produce.component_evaluator(q, xx, yy, s)
        active = [index for index, factor in enumerate(factors) if evaluates_to_zero(factor)]
        require(row["active_curves"] == active, "active-curve set")
        collision_rows = [
            index
            for index, (real, imaginary) in enumerate(collision_sparse)
            if evaluates_to_zero(real) and evaluates_to_zero(imaginary)
        ]
        require(row["collision_rows"] == collision_rows, "collision set")

        if collision_rows:
            # The checked algebraic fact is the collision.  The three-colour
            # implication is the independently accepted h4119/h4141 theorem.
            require(row["chromatic_number_upper_bound"] == 3, "collision upper bound")
            require(row["three_colouring"] is None, "collision stores no label colouring")
            require(row["four_colouring"] is None, "collision stores no label colouring")
        else:
            edges = sorted(base_edges + [edge for curve in active for edge in factor_edges[curve]])
            require(len(edges) == len(set(edges)), "event-edge owner overlap")
            three = row["three_colouring"]
            four = row["four_colouring"]
            require(row["chromatic_number_upper_bound"] == 3, "injective upper bound")
            require(isinstance(three, list) and len(three) == 243, "three-colour word length")
            require(set(three) <= {0, 1, 2}, "three-colour alphabet")
            require(all(three[a] != three[b] for a, b in edges), "three-colour edge replay")
            require(isinstance(four, list) and len(four) == 243, "four-colour word length")
            require(set(four) <= {0, 1, 2, 3}, "four-colour alphabet")
            require(all(four[a] != four[b] for a, b in edges), "four-colour edge replay")

        active_histogram[(len(active), sum(len(factor_edges[curve]) for curve in active))] += real_roots
        chromatic_histogram[row["chromatic_number_upper_bound"]] += real_roots
        real_embeddings += real_roots

    active_summary = {
        f"{curves}_curves_{edges}_event_edges": count
        for (curves, edges), count in sorted(active_histogram.items())
    }
    chromatic_summary = {str(key): value for key, value in sorted(chromatic_histogram.items())}
    require(certificate["distinct_real_components"] == len(expected_data), "real component count")
    require(certificate["real_parameter_embeddings"] == real_embeddings, "real embedding count")
    require(certificate["active_curve_edge_histogram_by_embedding"] == active_summary, "active histogram")
    require(certificate["chromatic_upper_bound_histogram_by_embedding"] == chromatic_summary, "chromatic histogram")
    without_self = dict(certificate)
    claimed = without_self.pop("result_sha256_without_self")
    require(claimed == produce.digest(without_self), "self-excluding result digest")
    return {
        "certificate_sha256": file_digest(certificate_path),
        "source_residual_sha256": certificate["source_residual_sha256"],
        "pair_count": len(pairs),
        "total_bezout_allowance": sum(row[3] for row in pairs),
        "distinct_real_components": len(expected_data),
        "real_parameter_embeddings": real_embeddings,
        "chromatic_upper_bound_histogram_by_embedding": chromatic_summary,
        "status": "PASS",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    summary = verify(args.residual, args.certificate)
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(summary == expected, "EXPECTED.json mismatch")
    print(json.dumps(summary, indent=2, sort_keys=True))
