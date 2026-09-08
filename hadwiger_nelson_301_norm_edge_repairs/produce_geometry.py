#!/usr/bin/env python3
"""Search the h3981 parallelogram/norm obstruction on a supplied repaired graph."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from functools import reduce
from itertools import combinations
from math import gcd, lcm
from pathlib import Path

from flint import fmpq, fmpq_mat, nmod_mat


def odd_wheel(adjacency):
    for hub in sorted(adjacency):
        neighbours = adjacency[hub]
        colour = {}
        parent = {}
        for root in sorted(neighbours):
            if root in colour:
                continue
            colour[root] = 0
            parent[root] = None
            queue = deque([root])
            while queue:
                vertex = queue.popleft()
                for other in sorted(adjacency[vertex] & neighbours):
                    if other not in colour:
                        colour[other] = 1 - colour[vertex]
                        parent[other] = vertex
                        queue.append(other)
                    elif colour[other] == colour[vertex]:
                        left_path = []
                        right_path = []
                        left, right = vertex, other
                        while left is not None:
                            left_path.append(left)
                            left = parent[left]
                        while right is not None:
                            right_path.append(right)
                            right = parent[right]
                        join = next(item for item in left_path if item in right_path)
                        rim = left_path[: left_path.index(join) + 1] + list(reversed(right_path[: right_path.index(join)]))
                        return {"type": "odd_wheel", "hub": hub, "rim": rim}
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    graph = json.loads(args.graph.read_text())
    vertices = graph["labels"]
    position = {vertex: index for index, vertex in enumerate(vertices)}
    edges = {tuple(edge) for edge in graph["edges"]}
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    cycles = set()
    for left, right in combinations(vertices, 2):
        for second, fourth in combinations(sorted(adjacency[left] & adjacency[right]), 2):
            cycle = [left, second, right, fourth]
            canonical = min(
                tuple(order[index:] + order[:index])
                for order in (cycle, list(reversed(cycle)))
                for index in range(4)
            )
            cycles.add(canonical)
    diagonal_pairs = sorted({tuple(sorted((cycle[index], cycle[index + 2]))) for cycle in cycles for index in range(2)})
    blocked = {}
    for left, right in diagonal_pairs:
        key = f"{left},{right}"
        if (left, right) in edges:
            blocked[key] = {"type": "edge"}
            continue
        quotient = {
            vertex: {left if neighbour == right else neighbour for neighbour in adjacency[vertex]}
            for vertex in vertices
            if vertex != right
        }
        quotient[left] |= adjacency[right]
        witness = odd_wheel(quotient)
        if witness:
            blocked[key] = witness
    mandatory_cycles = [
        cycle
        for cycle in sorted(cycles)
        if all(f"{min(cycle[index], cycle[index + 2])},{max(cycle[index], cycle[index + 2])}" in blocked for index in range(2))
    ]

    rows = []
    for cycle in mandatory_cycles:
        row = [0] * len(vertices)
        for index, vertex in enumerate(cycle):
            row[position[vertex]] = (-1) ** index
        rows.append(row)
    rows.append([int(vertex == vertices[0]) for vertex in vertices])
    echelon, rank = fmpq_mat(rows).rref()
    pivots = [next(column for column in range(len(vertices)) if echelon[row, column]) for row in range(rank)]
    free = [column for column in range(len(vertices)) if column not in pivots]
    signature = {column: [fmpq(int(column == other)) for other in free] for column in free}
    for row, column in enumerate(pivots):
        signature[column] = [-echelon[row, other] for other in free]
    dimension = len(free)

    gram = []
    edge_order = sorted(edges)
    for left, right in edge_order:
        difference = [a - b for a, b in zip(signature[position[left]], signature[position[right]])]
        gram.append([
            (1 if first == second else 2) * difference[first] * difference[second]
            for first in range(dimension)
            for second in range(first, dimension)
        ])
    prime = 1000000007

    def residue(value):
        return int(value.numerator) % prime * pow(int(value.denominator), -1, prime) % prime

    augmented = nmod_mat([[residue(value) for value in row] + [1] for row in gram], prime)
    augmented_echelon, augmented_rank = augmented.transpose().rref()
    selected = [next(column for column in range(len(gram)) if augmented_echelon[row, column]) for row in range(augmented_rank)]
    linear_echelon, linear_rank = fmpq_mat([gram[index] for index in selected]).transpose().rref()
    internal_pivots = [next(column for column in range(len(selected)) if linear_echelon[row, column]) for row in range(linear_rank)]
    free_selected = [column for column in range(len(selected)) if column not in internal_pivots]
    receipt = {
        "source_sha256": hashlib.sha256(args.graph.read_bytes()).hexdigest(),
        "all_four_cycles": len(cycles),
        "diagonal_pairs": len(diagonal_pairs),
        "blocked_diagonal_pairs": len(blocked),
        "mandatory_four_cycles": len(mandatory_cycles),
        "anchored_rank": rank,
        "coordinate_parameters": dimension,
        "affine_gram_rank": augmented_rank,
        "linear_gram_rank": linear_rank,
        "contradictory_norm_identity_found": bool(free_selected),
    }
    if not free_selected:
        print(json.dumps(receipt, indent=2, sort_keys=True))
        args.output.write_text(json.dumps({"receipt": receipt}, separators=(",", ":"), sort_keys=True) + "\n")
        return

    selected_free = free_selected[0]
    multipliers = [fmpq(0) for _ in selected]
    multipliers[selected_free] = fmpq(1)
    for row, column in enumerate(internal_pivots):
        multipliers[column] = -linear_echelon[row, selected_free]
    denominator = lcm(*(int(value.denominator) for value in multipliers))
    integer_multipliers = [int(value * denominator) for value in multipliers]
    divisor = reduce(gcd, integer_multipliers)
    integer_multipliers = [value // divisor for value in integer_multipliers]
    if sum(integer_multipliers) < 0:
        integer_multipliers = [-value for value in integer_multipliers]
    support = [(index, value) for index, value in zip(selected, integer_multipliers) if value]
    if not sum(integer_multipliers):
        raise ValueError("zero unit-edge sum")
    if any(sum(value * gram[index][entry] for index, value in support) for entry in range(len(gram[0]))):
        raise ValueError("invalid norm identity")
    used = {
        f"{min(cycle[index], cycle[index + 2])},{max(cycle[index], cycle[index + 2])}"
        for cycle in mandatory_cycles
        for index in range(2)
    }
    receipt["norm_identity_edges"] = len(support)
    receipt["unit_norm_sum"] = sum(integer_multipliers)
    certificate = {
        "receipt": receipt,
        "cycles": mandatory_cycles,
        "diagonal_obstructions": {key: blocked[key] for key in sorted(used)},
        "translation_anchor": vertices[0],
        "rank_prime": prime,
        "affine_rank": rank,
        "free_labels": [vertices[index] for index in free],
        "parametrization": [
            [[parameter, int(value.numerator), int(value.denominator)] for parameter, value in enumerate(signature[index]) if value]
            for index in range(len(vertices))
        ],
        "norm_weights": [[edge_order[index][0], edge_order[index][1], value] for index, value in support],
        "weight_sum": sum(integer_multipliers),
    }
    args.output.write_text(json.dumps(certificate, separators=(",", ":"), sort_keys=True) + "\n")
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
