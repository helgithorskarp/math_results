#!/usr/bin/env python3
"""Solver-free checker for the fixed Snail-D3 triangle-gluing cohort."""
from __future__ import annotations

import argparse
import base64
import hashlib
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hadwiger_nelson_snail_dihedral"
sys.path.insert(0, str(PARENT))

import independent_field as q  # type: ignore  # noqa: E402

P = 1_000_001_539
ROOTS = (512562457, 103889680, 157886017, 2545130)  # a,b,c,e
PINS = {
    "seed.json": "9d03aaf2233e7b96109484a1fe3c8d311025bb95186b6927d517d716e774f614",
    "certificate.json": "c217efc0649faf986475dac157e7f2ac4bb992e4f4ac88a108e3217808d20dc3",
    "geometry.py": "2d25983290e6e912bc434f8286e6d2771d893949af83fb16433d1bb74b4bfc0e",
    "independent_field.py": "a3c053154d7ba19b9651eee4d0a10a5917446f35a99574cf42e1154e37a39324",
}
FIXED_CASE = (9, 3)
PERMUTATIONS = tuple(itertools.permutations(range(3)))
F = Fraction
ONE = tuple(F(x) for x in q.ONE)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def mul(x, y):
    return tuple(F(a) for a in q.product(x, y))


def bar(x):
    return tuple(F(a) for a in q.bar(x))


def norm(x):
    return mul(x, bar(x))


def inverse(x):
    """Invert a field element by an exact 16-by-16 linear solve."""
    basis = [tuple(F(i == j) for i in range(16)) for j in range(16)]
    columns = [mul(x, b) for b in basis]
    matrix = [
        [columns[j][i] for j in range(16)] + [F(i == 0)]
        for i in range(16)
    ]
    for column in range(16):
        pivot = next((r for r in range(column, 16) if matrix[r][column]), None)
        require(pivot is not None, "noninvertible normalization edge")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [x / divisor for x in matrix[column]]
        for row in range(16):
            if row == column or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[column])]
    result = tuple(row[-1] for row in matrix)
    require(mul(x, result) == ONE, "inverse audit")
    return result


def normalize(points, ordered_triangle):
    start, end, _ = (points[i] for i in ordered_triangle)
    multiplier = inverse(sub(end, start))
    return [mul(sub(point, start), multiplier) for point in points]


def residue_basis():
    a, b, c, e = ROOTS
    require((a * a + 3) % P == 0, "a residue")
    require((b * b + 11) % P == 0, "b residue")
    require((c * c - 5) % P == 0, "c residue")
    require((e * e + 3320 - 632 * a * b) % P == 0, "e residue")
    return tuple(
        pow(a, i & 1, P)
        * pow(b, (i >> 1) & 1, P)
        * pow(c, (i >> 2) & 1, P)
        * pow(e, (i >> 3) & 1, P)
        % P
        for i in range(16)
    )


RESIDUES = residue_basis()


@lru_cache(maxsize=None)
def residue(x):
    total = 0
    for value, basis_value in zip(x, RESIDUES):
        value = F(value)
        require(value.denominator % P, "normalization denominator at modulus")
        total += value.numerator * pow(value.denominator, -1, P) * basis_value
    return total % P


def unpack(text, length=348):
    require(type(text) is str, "word type")
    data = base64.b64decode(text, validate=True)
    require(len(data) == (length + 3) // 4, "word length")
    require(base64.b64encode(data).decode() == text, "canonical base64")
    word = [(data[i // 4] >> (2 * (i % 4))) & 3 for i in range(length)]
    if length % 4:
        require(data[-1] >> (2 * (length % 4)) == 0, "word padding")
    return word


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(certificate):
    for name, digest in PINS.items():
        require(sha256(PARENT / name) == digest, f"dependency hash: {name}")
    parent = json.loads((PARENT / "certificate.json").read_text())
    require(parent["complete"] is True and len(parent["cases"]) == 812, "parent coverage")
    seed_triangle = tuple(parent["seed_triangle"])
    require(len(seed_triangle) == 3 and len(set(seed_triangle)) == 3, "seed triangle")
    four_cases = [(r[0], r[1]) for r in parent["cases"] if r[3] == 4]
    require(len(four_cases) == 655, "four-chromatic case count")
    fixed_row = next(r for r in parent["cases"] if tuple(r[:2]) == FIXED_CASE)
    require(fixed_row[3] == 4 and len(fixed_row[4]) == 113, "fixed source gate")

    require(certificate.get("version") == 1, "certificate version")
    require(certificate.get("family") == "fixed Snail-D3 canonical-triangle gluing", "family")
    require(tuple(certificate.get("fixed_case", ())) == FIXED_CASE, "fixed case")
    require(certificate.get("second_case_order") == [list(x) for x in four_cases], "case order")
    require(certificate.get("permutation_order") == [list(x) for x in PERMUTATIONS], "permutation order")
    require(certificate.get("address_order") ==
            "174 fixed formal addresses then 174 moved formal addresses", "address order")
    dependencies = dict(certificate.get("dependencies", {}))
    for name in ("seed.json", "certificate.json", "geometry.py"):
        require(dependencies.get(name) == PINS[name], f"certificate dependency: {name}")
    rows = certificate.get("rows")
    require(type(rows) is list and len(rows) == 655 * 6, "row count")

    row_index = 0
    edge_checks = pair_checks = modular_survivors = colour_checks = 0

    def internal_edges(points):
        """Reconstruct one input's complete edge set as formal-index pairs."""
        nonlocal edge_checks, pair_checks, modular_survivors
        first = {}
        for index, point in enumerate(points):
            first.setdefault(point, index)
        representatives = sorted(first.values())
        values = {i: residue(points[i]) for i in representatives}
        bars = {i: residue(bar(points[i])) for i in representatives}
        result = []
        for i, j in itertools.combinations(representatives, 2):
            pair_checks += 1
            if (values[i] - values[j]) * (bars[i] - bars[j]) % P != 1:
                continue
            modular_survivors += 1
            if norm(sub(points[i], points[j])) == ONE:
                result.append((i, j))
                edge_checks += 1
        return result

    def edge_key(x, y):
        return (x, y) if x < y else (y, x)

    seed = q.exact_seed()
    base_formal, _ = q.exact_addresses(seed, *FIXED_CASE)
    require(len(base_formal) == 174, "base formal order")
    base_points = normalize(base_formal, seed_triangle)
    qbase = base_points[seed_triangle[2]]
    base_set = set(base_points)
    require(len(base_set) == 157, "base physical order")
    base_edge_indices = internal_edges(base_points)

    order_hist = Counter()
    collision_hist = Counter()
    cross_hist = Counter()
    best = None
    for case in four_cases:
        formal, _ = q.exact_addresses(seed, *case)
        require(len(formal) == 174, "moved formal order")
        canonical = normalize(formal, seed_triangle)
        moved_edge_indices = internal_edges(canonical)
        for permutation in PERMUTATIONS:
            row = rows[row_index]
            row_index += 1
            require(type(row) is list and len(row) == 8, "row shape")
            centre, axis, stored_permutation, packed, expected_order, expected_edges, expected_collisions, expected_cross = row
            require((centre, axis) == case, "row case")
            require(tuple(stored_permutation) == permutation, "row permutation")
            ordered = tuple(seed_triangle[i] for i in permutation)
            moved = normalize(formal, ordered)
            qpoint = moved[ordered[2]]
            if qpoint == qbase:
                reflected = False
            elif bar(qpoint) == qbase:
                moved = [bar(z) for z in moved]
                reflected = True
            else:
                raise ValueError("triangle orientation")
            require(tuple(moved[seed_triangle[i]] for i in permutation) ==
                    tuple(base_points[i] for i in seed_triangle), "triangle gluing")

            word = unpack(packed)
            formal_points = base_points + moved
            colours = {}
            for point, colour in zip(formal_points, word):
                if point in colours:
                    require(colours[point] == colour, "collision colour consistency")
                else:
                    colours[point] = colour
            moved_set = set(moved)
            physical = sorted(colours)
            require(len(physical) == expected_order, "physical order")
            collisions = len(base_set & moved_set)
            require(collisions == expected_collisions, "collision count")
            edges = {edge_key(base_points[i], base_points[j])
                     for i, j in base_edge_indices}
            edges.update(edge_key(moved[i], moved[j])
                         for i, j in moved_edge_indices)
            base_only = sorted(base_set - moved_set)
            moved_only = sorted(moved_set - base_set)
            base_values = [(point, residue(point), residue(bar(point))) for point in base_only]
            moved_values = [(point, residue(point), residue(bar(point))) for point in moved_only]
            cross = 0
            for x, vx, bx in base_values:
                for y, vy, by in moved_values:
                    pair_checks += 1
                    if (vx - vy) * (bx - by) % P != 1:
                        continue
                    modular_survivors += 1
                    if norm(sub(x, y)) != ONE:
                        continue
                    edges.add(edge_key(x, y))
                    edge_checks += 1
                    cross += 1
            require(len(edges) == expected_edges, "edge count")
            require(cross == expected_cross, "new cross-edge count")
            for x, y in edges:
                require(colours[x] != colours[y], "monochromatic unit edge")
                colour_checks += 1
            order_hist[expected_order] += 1
            collision_hist[collisions] += 1
            cross_hist[cross] += 1
            score = (cross, collisions, len(edges), -expected_order)
            if best is None or score > best[0]:
                best = (score, {
                    "second_case": list(case),
                    "permutation": list(permutation),
                    "chirality": "reflected" if reflected else "direct",
                    "vertices": expected_order,
                    "edges": len(edges),
                    "collisions": collisions,
                    "new_cross_edges": cross,
                })

    summary = certificate.get("summary", {})
    require(summary.get("status") == "ALL_PLACEMENTS_FOUR_COLOURABLE", "summary status")
    require(summary.get("placements") == 3930 and summary.get("sat_cases") == 3930, "summary coverage")
    require(summary.get("orders") == {str(k): v for k, v in sorted(order_hist.items())}, "order histogram")
    require(summary.get("collisions") == {str(k): v for k, v in sorted(collision_hist.items())}, "collision histogram")
    require(summary.get("new_cross_edges") == {str(k): v for k, v in sorted(cross_hist.items())}, "cross histogram")
    expected_best = {k: v for k, v in summary.get("best_placement", {}).items()
                     if k not in {"proper_four_colouring", "permuted_second_triangle"}}
    # The producer labels its concrete triangle by physical ids; this checker
    # uses the canonical permutation.  All invariant best-case fields agree.
    for key in ("second_case", "chirality", "vertices", "edges", "collisions", "new_cross_edges"):
        require(expected_best.get(key) == best[1].get(key), f"best field: {key}")
    return {
        "verified": True,
        "status": "ALL_PLACEMENTS_FOUR_COLOURABLE",
        "fixed_case": list(FIXED_CASE),
        "fixed_vertices": len(base_set),
        "fixed_archived_nonthree_core_order": 113,
        "second_cases": len(four_cases),
        "placements": len(rows),
        "vertices_range": [min(order_hist), max(order_hist)],
        "unit_edges_range": [min(int(r[5]) for r in rows), max(int(r[5]) for r in rows)],
        "collisions_range": [min(collision_hist), max(collision_hist)],
        "new_cross_edges_range": [min(cross_hist), max(cross_hist)],
        "best_placement": best[1],
        "physical_pairs_checked": pair_checks,
        "modular_survivors": modular_survivors,
        "unit_edges_checked": edge_checks,
        "colour_edge_checks": colour_checks,
        "solver_used": False,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify(json.loads(args.certificate.read_text()))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.check_expected:
        require(text == (HERE / "EXPECTED.json").read_text(), "expected output")
    print(text, end="")


if __name__ == "__main__":
    main()
