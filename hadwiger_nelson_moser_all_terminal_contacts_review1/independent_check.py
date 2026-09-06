#!/usr/bin/env python3
"""Independent exact audit of the all-contact Moser terminal theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_moser_all_terminal_contacts"
POSITIVE = ROOT / "hadwiger_nelson_long_terminal_gluing"
POINTS = ROOT / "hadwiger_nelson_nonmono159_214_lowden2"
SCALE2 = 12 * 12


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    require(len(a) == len(b), "field dimensions")
    return tuple(x + y for x, y in zip(a, b))


def multiply(a: tuple[int, ...], b: tuple[int, ...], radicals: tuple[int, ...]) -> tuple[int, ...]:
    """Multiply in the squarefree basis indexed by radical-subset bitmasks."""
    dimension = 1 << len(radicals)
    require(len(a) == len(b) == dimension, "field dimensions")
    out = [0] * dimension
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            common = i & j
            factor = 1
            for bit, radical in enumerate(radicals):
                if common & (1 << bit):
                    factor *= radical
            out[i ^ j] += x * y * factor
    return tuple(out)


def norm_numerator(p: tuple[tuple[int, ...], tuple[int, ...]],
                   q: tuple[tuple[int, ...], tuple[int, ...]],
                   radicals: tuple[int, ...]) -> tuple[int, ...]:
    dx = tuple(x - y for x, y in zip(p[0], q[0]))
    dy = tuple(x - y for x, y in zip(p[1], q[1]))
    return add(multiply(dx, dx, radicals), multiply(dy, dy, radicals))


def squared_distance_is(p, q, value: int, radicals: tuple[int, ...]) -> bool:
    return norm_numerator(p, q, radicals) == (SCALE2 * value,) + (0,) * ((1 << len(radicals)) - 1)


def audit_kernel() -> dict:
    certificate_path = TARGET / "certificate.json"
    certificate = json.loads(certificate_path.read_text())
    require(certificate["scale"] == 12 and certificate["basis"] == ["1", "sqrt3", "sqrt11", "sqrt33"],
            "kernel field convention")
    radicals = (3, 11)

    def point(raw):
        require(len(raw) == 2 and all(len(part) == 4 for part in raw), "kernel coordinate")
        return tuple(tuple(int(x) for x in part) for part in raw)

    expected_m = (
        ((0, 0, 0, 0), (0, 0, 0, 0)),
        ((12, 0, 0, 0), (0, 0, 0, 0)),
        ((6, 0, 0, 0), (0, 6, 0, 0)),
        ((18, 0, 0, 0), (0, 6, 0, 0)),
        ((10, 0, 0, 0), (0, 0, 2, 0)),
        ((5, 0, 0, -1), (0, 5, 1, 0)),
        ((15, 0, 0, -1), (0, 5, 3, 0)),
    )
    spindle = tuple(point(raw) for raw in certificate["M"])
    require(spindle == expected_m and len(set(spindle)) == 7, "specified spindle transcription")
    points = tuple(point(raw) for raw in certificate["C"])
    require(len(points) == len(set(points)) == 25 and set(spindle) <= set(points), "25-point kernel")
    spindle_indices = tuple(points.index(p) for p in spindle)
    pair_norms = {edge: norm_numerator(points[edge[0]], points[edge[1]], radicals)
                  for edge in itertools.combinations(range(25), 2)}
    require(len(pair_norms) == 300, "all kernel pair norms")

    circle_rows = certificate["circle_pairs"]
    require([tuple(row[:2]) for row in circle_rows] == list(itertools.combinations(range(7), 2)),
            "all 21 spindle pairs")
    witnessed = set()
    circle_checks = 0
    for i, j, a, b in circle_rows:
        require(a != b and 0 <= a < 25 and 0 <= b < 25, "two distinct circle witnesses")
        for witness in (a, b):
            require(squared_distance_is(points[witness], spindle[i], 1, radicals)
                    and squared_distance_is(points[witness], spindle[j], 1, radicals),
                    "invalid common unit neighbour")
            witnessed.add(witness)
            circle_checks += 2
    require(witnessed == set(range(25)) and circle_checks == 84, "complete two-circle witness union")

    external_indices = tuple(i for i in range(25) if i not in spindle_indices)
    require(list(external_indices) == certificate["D_indices"] and len(external_indices) == 18,
            "external double-neighbour domain")
    external = tuple(points[i] for i in external_indices)
    neighbours = [
        [i for i, m in enumerate(spindle) if squared_distance_is(p, m, 1, radicals)]
        for p in external
    ]
    require(neighbours == certificate["D_neighbours"] and all(len(row) == 2 for row in neighbours),
            "every external point has exactly two spindle neighbours")

    distance_rows = {
        value: [list(edge) for edge in itertools.combinations(range(18), 2)
                if squared_distance_is(external[edge[0]], external[edge[1]], value, radicals)]
        for value in (1, 7, 9)
    }
    require(distance_rows[1] == certificate["D_unit_edges"], "external unit graph")
    require(distance_rows[7] == certificate["D_sqrt7_pairs"], "external sqrt7 pairs")
    require(distance_rows[9] == certificate["D_distance3_pairs"], "external distance-three pairs")
    require((len(distance_rows[1]), len(distance_rows[7]), len(distance_rows[9])) == (6, 4, 0),
            "external pair counts")
    require(len({v for edge in distance_rows[7] for v in edge}) == 8, "sqrt7 matching")
    require(sum(value == (SCALE2, 0, 0, 0) for value in pair_norms.values()) == 53,
            "complete 25-point unit graph")

    colours = certificate["M_colours"]
    spindle_edges = [edge for edge in itertools.combinations(range(7), 2)
                     if squared_distance_is(spindle[edge[0]], spindle[edge[1]], 1, radicals)]
    require(colours == [0, 1, 2, 3, 1, 3, 2] and len(spindle_edges) == 11,
            "specified spindle colouring")
    require(all(colours[a] != colours[b] for a, b in spindle_edges), "improper spindle colouring")
    lists = [sorted(set(range(4)) - {colours[i] for i in row}) for row in neighbours]
    require(lists == certificate["D_lists"], "available lists")
    require(Counter(map(len, lists)) == Counter({2: 15, 3: 3}), "two/three-list split")
    require(all(set(lists[a]).isdisjoint(lists[b]) for a, b in distance_rows[7]),
            "sqrt7 endpoints do not force inequality")

    two_list = {i for i, row in enumerate(lists) if len(row) == 2}
    two_edges = [edge for edge in map(tuple, distance_rows[1]) if set(edge) <= two_list]
    degree = Counter(v for edge in two_edges for v in edge)
    require(len(two_list) == 15 and len(two_edges) == 2 and sorted(degree.values()) == [1, 1, 2],
            "two-list graph is P3 plus isolates")
    require(all(lists[a] != lists[b] for a, b in two_edges), "adjacent two-lists differ")

    return {
        "certificate": identity(certificate_path),
        "kernel_points": 25,
        "external_double_neighbours": 18,
        "circle_witness_unit_checks": circle_checks,
        "all_kernel_pair_norms": 300,
        "spindle_unit_edges": len(spindle_edges),
        "external_unit_edges": len(distance_rows[1]),
        "external_sqrt7_pairs": len(distance_rows[7]),
        "external_distance3_pairs": len(distance_rows[9]),
        "two_lists": 15,
        "three_lists": 3,
        "two_list_edges": len(two_edges),
        "two_list_graph": "P3 plus 12 isolated vertices",
    }


def parse_points(path: Path) -> tuple:
    lines = path.read_text().splitlines()
    require(lines and lines[0] == "# scale 12", "point-file scale")
    points = []
    for line in lines[1:]:
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        require(len(values) == 16, "eight-basis complex coordinate")
        points.append((values[:8], values[8:]))
    return tuple(points)


def canonical_pattern(target: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    order = tuple(dict.fromkeys(target))
    pattern = "".join(str(order.index(value)) for value in target)
    palette = order + tuple(sorted(set("0123") - set(order)))
    require(len(palette) == 4, "palette permutation")
    return pattern, palette


def audit_positive_extensions() -> dict:
    radicals = (3, 5, 11)
    certificate_path = POSITIVE / "certificate.json"
    certificate = json.loads(certificate_path.read_text())
    cases = ((159, (141, 142, 144), 7, 646, 60), (214, (186, 187), 9, 977, 12))
    reports = []
    total_pair_checks = total_canonical_checks = total_expanded_checks = total_assignments = 0
    for n, terminals, terminal_distance, expected_edges, expected_assignments in cases:
        path = POINTS / f"points{n}.tsv"
        points = parse_points(path)
        require(len(points) == len(set(points)) == n, "distinct gadget points")
        edges = [edge for edge in itertools.combinations(range(n), 2)
                 if squared_distance_is(points[edge[0]], points[edge[1]], 1, radicals)]
        require(len(edges) == expected_edges, "strict gadget unit-edge count")
        require(all(squared_distance_is(points[a], points[b], terminal_distance, radicals)
                    for a, b in itertools.combinations(terminals, 2)), "terminal distances")

        record = certificate[str(n)]
        require(tuple(record["terminals"]) == terminals, "terminal indices")
        witnesses = {row["pattern"]: row["colours"] for row in record["extensions"]}
        required_patterns = {"001", "010", "011", "012"} if n == 159 else {"01"}
        require(set(witnesses) == required_patterns, "canonical positive-pattern domain")
        for pattern, colouring in witnesses.items():
            require(len(colouring) == n and set(colouring) <= set("0123"), "canonical colouring")
            require("".join(colouring[v] for v in terminals) == pattern, "canonical terminal pattern")
            require(all(colouring[a] != colouring[b] for a, b in edges), "canonical witness conflict")
            total_canonical_checks += len(edges)

        assignments = 0
        for target in itertools.product("0123", repeat=len(terminals)):
            if len(set(target)) == 1:
                continue
            pattern, palette = canonical_pattern(target)
            source = witnesses[pattern]
            colouring = "".join(palette[int(value)] for value in source)
            require(tuple(colouring[v] for v in terminals) == target, "expanded terminal assignment")
            require(all(colouring[a] != colouring[b] for a, b in edges), "expanded witness conflict")
            assignments += 1
            total_expanded_checks += len(edges)
        require(assignments == expected_assignments, "complete nonmonochromatic assignments")
        total_assignments += assignments
        total_pair_checks += n * (n - 1) // 2
        reports.append({
            "vertices": n,
            "coordinate_file": identity(path),
            "unit_edges": len(edges),
            "terminal_indices": list(terminals),
            "squared_terminal_distance": terminal_distance,
            "terminal_assignments": assignments,
        })

    require(total_pair_checks == 35_352 and total_canonical_checks == 3_561,
            "full gadget definition-level checks")
    require(total_assignments == 72 and total_expanded_checks == 50_484,
            "full positive-extension replay")
    return {
        "certificate": identity(certificate_path),
        "gadgets": reports,
        "exact_pair_norm_checks": total_pair_checks,
        "canonical_witness_edge_checks": total_canonical_checks,
        "terminal_assignments": total_assignments,
        "expanded_edge_checks": total_expanded_checks,
    }


def audit_combinatorics() -> dict:
    # Verify every leaf-triangle extension case in the Gallai-tree argument.
    two_lists = tuple(itertools.combinations(range(4), 2))
    leaf_cases = 0
    for left, right in itertools.permutations(two_lists, 2):
        for cut_colour in range(4):
            require(any(a != cut_colour and b != cut_colour and a != b
                        for a in left for b in right), "leaf-triangle extension")
            leaf_cases += 1
    require(leaf_cases == 120, "all unequal two-list leaf cases")
    require(not any(a != 0 and b != 0 and a != b for a in (0, 1) for b in (0, 1)),
            "equal-list obstruction control")

    # In a hypothetical auxiliary K4, every edge has length 1 or sqrt(7).
    # Unit adjacency must be transitive because two unit steps have distance
    # at most 2 < sqrt(7). Enumerate the resulting edge signatures.
    vertices = range(4)
    edges = tuple(itertools.combinations(vertices, 2))
    signatures = []
    for long_bits in itertools.product((False, True), repeat=6):
        if sum(long_bits) > 3:
            continue
        unit = {edge for edge, is_long in zip(edges, long_bits) if not is_long}
        transitive = all((tuple(sorted((a, c))) in unit)
                         for a, b, c in itertools.permutations(vertices, 3)
                         if tuple(sorted((a, b))) in unit and tuple(sorted((b, c))) in unit)
        if transitive:
            signatures.append(sum(long_bits))
    require(Counter(signatures) == Counter({3: 4, 0: 1}), "only K4 or K3-plus-point signatures")

    budget_cases = []
    for copies_a in range(5):
        for copies_b in range(5):
            private_vertices = 156 * copies_a + 212 * copies_b
            if private_vertices <= 508:
                require(copies_a + copies_b <= 3, "four copies fit budget")
                if copies_a + copies_b == 3:
                    require(copies_b == 0, "three-copy case involving B fits budget")
                budget_cases.append((copies_a, copies_b))

    degree_cases = []
    for sets in range(1, 4):
        for memberships in range(1, sets + 1):
            generic_bound = (sets - memberships) + memberships
            if sets <= 2:
                require(generic_bound <= 2, "two-set terminal degree")
            if sets == 3:
                require(sets - memberships <= 2, "three-A double-neighbour degree")
            degree_cases.append((sets, memberships, generic_bound))

    return {
        "leaf_triangle_list_cases": leaf_cases,
        "equal_two_list_obstruction_checked": True,
        "K4_edge_signatures_checked": 64,
        "K4_transitive_signatures_with_at_most_three_long_edges": len(signatures),
        "K4_remaining_forms": "one all-unit K4 or four unit-triangle/sqrt7-centre signatures",
        "budget_pairs_checked": 25,
        "budget_pairs_fitting_private_vertex_bound": len(budget_cases),
        "terminal_degree_parameter_cases": len(degree_cases),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(__debug__, "run with assertions enabled")
    report = {
        "status": "PASS",
        "verdict": "all terminal contacts extend under the stated spindle-disjoint terminal-only hypotheses",
        "kernel": audit_kernel(),
        "positive_extensions": audit_positive_extensions(),
        "combinatorics": audit_combinatorics(),
        "source_commit_reviewed": "061fb2c248515bf6c7385304d2ea53187de4a44c",
        "target_artifact": "bafkreig35dkfwsnf4zwzx3nlknxmraobceoeh26qkdnbujiv3ycls7fpvy",
        "vertices_at_most": 508,
        "spindle_disjoint_required": True,
        "private_interiors_required": True,
        "terminal_only_new_edges_required": True,
        "target_graph_found": False,
        "python": ".".join(map(str, __import__("sys").version_info[:3])),
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": report["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
