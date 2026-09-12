#!/usr/bin/env python3
"""Definition-level audit of the rooted point-link factorization."""

from __future__ import annotations

import argparse
import itertools
import json
import math


def pairs(n: int):
    return itertools.combinations(range(n), 2)


def decode_hex(n: int, text: str) -> list[int]:
    edge_count = n * (n - 1) // 2
    text = text.strip().lower()
    if len(text) != (edge_count + 3) // 4 or any(
            char not in "0123456789abcdef" for char in text):
        raise ValueError("invalid hexadecimal graph")
    bits = [int(char, 16) >> shift & 1 for char in text for shift in range(4)]
    if any(bits[edge_count:]):
        raise ValueError("nonzero padding bit")
    return bits[:edge_count]


def matrix_of(n: int, bits: list[int]) -> list[list[int]]:
    if len(bits) != n * (n - 1) // 2 or any(bit not in (0, 1) for bit in bits):
        raise ValueError("invalid physical edge vector")
    matrix = [[0] * n for _ in range(n)]
    for bit, (u, v) in zip(bits, pairs(n), strict=True):
        matrix[u][v] = matrix[v][u] = bit
    return matrix


def monochromatic(matrix: list[list[int]], vertices: tuple[int, ...],
                  color: int) -> bool:
    return all(matrix[u][v] == color for u, v in itertools.combinations(vertices, 2))


def audit(n: int, bits: list[int], root: int = 0) -> dict:
    matrix = matrix_of(n, bits)
    red_side = tuple(v for v in range(n) if v != root and matrix[root][v])
    blue_side = tuple(v for v in range(n) if v != root and not matrix[root][v])
    side_of = {v: matrix[root][v] for v in range(n) if v != root}
    direct_red = direct_blue = 0
    root_red = root_blue = 0
    unmixed_red = unmixed_blue = 0
    mixed_red = mixed_blue = 0
    active_red = active_blue = 0
    unsatisfied_red = unsatisfied_blue = 0
    split_active: dict[str, int] = {}

    for five in itertools.combinations(range(n), 5):
        red = monochromatic(matrix, five, 1)
        blue = monochromatic(matrix, five, 0)
        direct_red += red
        direct_blue += blue
        if root in five:
            root_red += red
            root_blue += blue
            continue
        side_count = sum(side_of[v] for v in five)
        if side_count in (0, 5):
            unmixed_red += red
            unmixed_blue += blue
            continue

        mixed_red += red
        mixed_blue += blue
        internal = []
        cross = []
        for u, v in itertools.combinations(five, 2):
            (internal if side_of[u] == side_of[v] else cross).append(matrix[u][v])
        red_possible = all(internal)
        blue_possible = not any(internal)
        if red_possible:
            active_red += 1
            unsatisfied_red += all(cross)
            key = f"red_{side_count}+{5-side_count}"
            split_active[key] = split_active.get(key, 0) + 1
        if blue_possible:
            active_blue += 1
            unsatisfied_blue += not any(cross)
            key = f"blue_{side_count}+{5-side_count}"
            split_active[key] = split_active.get(key, 0) + 1

    degrees = [sum(row) for row in matrix]
    report = {
        "n": n,
        "root": root,
        "root_degree": len(red_side),
        "red_side_size": len(red_side),
        "blue_side_size": len(blue_side),
        "red_edges": sum(bits),
        "degrees": degrees,
        "direct_red_K5": direct_red,
        "direct_blue_K5": direct_blue,
        "root_red_K5": root_red,
        "root_blue_K5": root_blue,
        "unmixed_red_K5": unmixed_red,
        "unmixed_blue_K5": unmixed_blue,
        "mixed_red_K5": mixed_red,
        "mixed_blue_K5": mixed_blue,
        "active_red_cross_clauses": active_red,
        "active_blue_cross_clauses": active_blue,
        "active_cross_clauses": active_red + active_blue,
        "unsatisfied_red_cross_clauses": unsatisfied_red,
        "unsatisfied_blue_cross_clauses": unsatisfied_blue,
        "split_active": dict(sorted(split_active.items())),
    }
    report["factorization_identity"] = (
        direct_red == root_red + unmixed_red + mixed_red and
        direct_blue == root_blue + unmixed_blue + mixed_blue and
        mixed_red == unsatisfied_red and mixed_blue == unsatisfied_blue)
    report["status"] = "GOOD_GRAPH" if direct_red + direct_blue == 0 else "NOT_GOOD_GRAPH"
    return report


def target_spec() -> dict:
    branches = []
    for degree in (18, 19, 20):
        other = 42 - degree
        master_variables = degree * (degree - 1) // 2 + other * (other - 1) // 2
        cross_variables = degree * other
        master_clauses = (math.comb(degree, 4) + math.comb(degree, 5) +
                          math.comb(other, 4) + math.comb(other, 5))
        branches.append({
            "root_degree": degree,
            "red_side_size": degree,
            "blue_side_size": other,
            "root_variables_fixed": 42,
            "master_internal_variables": master_variables,
            "inner_cross_variables": cross_variables,
            "free_variables_after_root_fixing": master_variables + cross_variables,
            "physical_edge_coordinates_total": 42 + master_variables + cross_variables,
            "master_link_clauses": master_clauses,
            "cross_clause_widths": [4, 6],
            "normalized_red_edge_upper_bound": 451,
            "degree_interval": [degree, 24],
        })
    return {"status": "EXACT_TARGET_SPEC", "n": 43, "branches": branches}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int)
    parser.add_argument("--hex")
    parser.add_argument("--root", type=int, default=0)
    parser.add_argument("--target-spec", action="store_true")
    args = parser.parse_args()
    if args.target_spec:
        if args.n is not None or args.hex is not None:
            parser.error("--target-spec takes no graph")
        report = target_spec()
    else:
        if args.n is None or args.hex is None:
            parser.error("--n and --hex are required")
        report = audit(args.n, decode_hex(args.n, args.hex), args.root)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
