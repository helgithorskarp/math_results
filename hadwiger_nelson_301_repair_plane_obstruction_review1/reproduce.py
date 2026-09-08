#!/usr/bin/env python3
"""Independent exact audit of the 301-vertex plane obstruction."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from pathlib import Path


GRAPH_SHA256 = "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb"
CERTIFICATE_SHA256 = "728c5af3dc90c6e01ac74c13d78768cae997f6fe91d39dfa1076600bfb61ab42"
AUDIT_PRIME = 998244353


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def rank_mod_prime(rows: list[list[int]], prime: int) -> int:
    """Row rank using dense, left-to-right modular Gaussian elimination."""
    matrix = [[entry % prime for entry in row] for row in rows]
    height = len(matrix)
    width = len(matrix[0])
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, height) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for row in range(height):
            if row == pivot_row or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (left - scale * right) % prime
                for left, right in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == height:
            break
    return pivot_row


def quotient_edges(edges: set[tuple[int, int]], first: int, second: int) -> set[tuple[int, int]]:
    """Identify second with first and discard loops."""
    image: set[tuple[int, int]] = set()
    for left, right in edges:
        left = first if left == second else left
        right = first if right == second else right
        if left != right:
            image.add(tuple(sorted((left, right))))
    return image


def sparse_parameters(raw_rows: list[list[list[int]]], columns: int) -> list[dict[int, Fraction]]:
    result: list[dict[int, Fraction]] = []
    for raw_row in raw_rows:
        row: dict[int, Fraction] = {}
        for column, numerator, denominator in raw_row:
            require(type(column) is int and 0 <= column < columns, "parameter column")
            require(column not in row, "duplicate parameter column")
            require(
                type(numerator) is int
                and type(denominator) is int
                and numerator != 0
                and denominator > 0,
                "parameter coefficient",
            )
            row[column] = Fraction(numerator, denominator)
        result.append(row)
    return result


def audit(graph: dict, certificate: dict) -> dict:
    labels = graph["labels"]
    require(labels == sorted(set(labels)) and len(labels) == 301, "graph labels")
    position = {label: index for index, label in enumerate(labels)}
    raw_edges = graph["edges"]
    edges = {tuple(edge) for edge in raw_edges}
    require(raw_edges == [list(edge) for edge in sorted(edges)], "edge order or duplication")
    require(len(edges) == 1452, "edge count")
    require(all(left < right and left in position and right in position for left, right in edges), "simple graph")
    require(certificate["source_sha256"] == GRAPH_SHA256, "certificate source hash")

    linear_rows: list[list[int]] = []
    required_pairs: set[str] = set()
    direct = 0
    wheels = 0
    wheel_lengths: dict[int, int] = {}
    cycles_seen: set[tuple[int, ...]] = set()
    witnesses = certificate["diagonal_obstructions"]

    for raw_cycle in certificate["cycles"]:
        cycle = tuple(raw_cycle)
        require(len(cycle) == 4 and len(set(cycle)) == 4, "degenerate four-cycle")
        require(cycle not in cycles_seen, "duplicate four-cycle")
        cycles_seen.add(cycle)
        require(
            all(tuple(sorted((cycle[i], cycle[(i + 1) % 4]))) in edges for i in range(4)),
            "four-cycle edge",
        )

        for i in range(2):
            first, second = sorted((cycle[i], cycle[i + 2]))
            key = f"{first},{second}"
            require(key in witnesses, "missing diagonal witness")
            if key in required_pairs:
                continue
            required_pairs.add(key)
            witness = witnesses[key]
            if witness["type"] == "edge":
                require((first, second) in edges, "false edge inequality")
                direct += 1
                continue
            require(witness["type"] == "odd_wheel", "unknown diagonal witness")
            quotient = quotient_edges(edges, first, second)
            hub = witness["hub"]
            rim = witness["rim"]
            require(second not in rim and hub != second, "noncanonical quotient vertex")
            require(hub in position and hub not in rim, "wheel hub")
            require(
                len(rim) >= 3 and len(rim) % 2 == 1 and len(set(rim)) == len(rim),
                "odd simple wheel rim",
            )
            require(all(vertex in position for vertex in rim), "wheel vertex")
            require(all(tuple(sorted((hub, vertex))) in quotient for vertex in rim), "wheel spoke")
            require(
                all(tuple(sorted((rim[i], rim[(i + 1) % len(rim)]))) in quotient for i in range(len(rim))),
                "wheel rim edge",
            )
            wheels += 1
            wheel_lengths[len(rim)] = wheel_lengths.get(len(rim), 0) + 1

        row = [0] * len(labels)
        for i, vertex in enumerate(cycle):
            row[position[vertex]] = 1 if i % 2 == 0 else -1
        linear_rows.append(row)

    require(required_pairs == set(witnesses), "unused diagonal witness")
    require(len(cycles_seen) == 279, "four-cycle count")
    require((direct, wheels) == (276, 282), "diagonal witness counts")
    require(wheel_lengths == {3: 266, 5: 10, 7: 6}, "wheel length census")

    anchor = certificate["translation_anchor"]
    require(anchor in position, "translation anchor")
    anchor_row = [0] * len(labels)
    anchor_row[position[anchor]] = 1
    linear_rows.append(anchor_row)

    free_labels = certificate["free_labels"]
    require(len(free_labels) == 55 and len(set(free_labels)) == 55, "free labels")
    parameters = sparse_parameters(certificate["parametrization"], len(free_labels))
    require(len(parameters) == len(labels), "parameter row count")
    for column, label in enumerate(free_labels):
        require(parameters[position[label]] == {column: Fraction(1)}, "free-row identity")

    for equation in linear_rows:
        total: dict[int, Fraction] = {}
        for vertex_index, coefficient in enumerate(equation):
            if not coefficient:
                continue
            for column, value in parameters[vertex_index].items():
                total[column] = total.get(column, Fraction()) + coefficient * value
        require(not any(total.values()), "kernel vector violates parallelogram equations")

    independent_rank = rank_mod_prime(linear_rows, AUDIT_PRIME)
    require(independent_rank == 246, "independent modular rank")
    require(certificate["affine_rank"] == 246, "claimed rank")
    # The 55 identity rows give 55 independent rational null vectors.  Rank
    # at least 246 modulo AUDIT_PRIME and rank-nullity give equality over Q.
    require(independent_rank + len(free_labels) == len(labels), "rank-nullity")

    gram: dict[tuple[int, int], Fraction] = {}
    weight_sum = 0
    norm_edges: set[tuple[int, int]] = set()
    for left, right, weight in certificate["norm_weights"]:
        edge = (left, right)
        require(edge in edges and edge not in norm_edges, "norm-identity edge")
        require(type(weight) is int and weight != 0, "norm-identity weight")
        norm_edges.add(edge)
        weight_sum += weight
        difference = parameters[position[left]].copy()
        for column, value in parameters[position[right]].items():
            difference[column] = difference.get(column, Fraction()) - value
        difference = {column: value for column, value in difference.items() if value}
        columns = sorted(difference)
        for offset, column in enumerate(columns):
            for other in columns[offset:]:
                coefficient = difference[column] * difference[other]
                if column != other:
                    coefficient *= 2
                key = (column, other)
                gram[key] = gram.get(key, Fraction()) + weight * coefficient

    require(len(norm_edges) == 18, "norm support")
    require(weight_sum == certificate["weight_sum"] == 708, "unit norm sum")
    require(not any(gram.values()), "quadratic identity")

    return {
        "status": "REPRODUCED_ACCEPT_H3981",
        "graph_sha256": GRAPH_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "vertices": len(labels),
        "edges": len(edges),
        "mandatory_four_cycles": len(cycles_seen),
        "direct_diagonal_edges": direct,
        "quotient_odd_wheels": wheels,
        "odd_wheel_rim_lengths": {str(key): wheel_lengths[key] for key in sorted(wheel_lengths)},
        "independent_rank_prime": AUDIT_PRIME,
        "anchored_rank": independent_rank,
        "coordinate_parameters": len(free_labels),
        "norm_identity_edges": len(norm_edges),
        "unit_norm_sum": weight_sum,
        "scope": "no plane unit-edge map, including noninjective maps",
    }


def rejected_controls(graph: dict, certificate: dict) -> list[str]:
    cases: list[tuple[str, dict, dict]] = []

    changed = copy.deepcopy(certificate)
    changed["diagonal_obstructions"].pop(next(iter(changed["diagonal_obstructions"])))
    cases.append(("missing_diagonal", graph, changed))

    changed = copy.deepcopy(certificate)
    wheel = next(value for value in changed["diagonal_obstructions"].values() if value["type"] == "odd_wheel")
    wheel["rim"][0] = wheel["hub"]
    cases.append(("bad_quotient_wheel", graph, changed))

    changed = copy.deepcopy(certificate)
    row = next(row for row in changed["parametrization"] if row)
    row[0][1] += 1
    cases.append(("bad_kernel", graph, changed))

    changed = copy.deepcopy(certificate)
    changed["norm_weights"][0][2] += 1
    changed["weight_sum"] += 1
    cases.append(("bad_norm_identity", graph, changed))

    rejected: list[str] = []
    for name, trial_graph, trial_certificate in cases:
        try:
            audit(trial_graph, trial_certificate)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError(f"accepted corrupted certificate: {name}")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository", type=Path)
    parser.add_argument("work", type=Path)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    source = args.repository / "hadwiger_nelson_h516_k23free_edge_repair" / "graph.json"
    certificate_path = args.repository / "hadwiger_nelson_301_repair_plane_obstruction" / "certificate.json"
    graph_bytes = source.read_bytes()
    certificate_bytes = certificate_path.read_bytes()
    require(hashlib.sha256(graph_bytes).hexdigest() == GRAPH_SHA256, "graph file hash")
    require(hashlib.sha256(certificate_bytes).hexdigest() == CERTIFICATE_SHA256, "certificate file hash")
    graph = json.loads(graph_bytes)
    certificate = json.loads(certificate_bytes)
    receipt = audit(graph, certificate)
    receipt["rejected_controls"] = rejected_controls(graph, certificate)
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    (args.work / "receipt.json").write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
