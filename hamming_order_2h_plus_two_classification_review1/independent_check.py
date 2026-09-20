#!/usr/bin/env python3
"""Independent finite audit of the order-(2h+2) Hamming-core theorem.

This checker deliberately does not import the target package.  Its main finite
test enumerates vertex subsets in several heterogeneous Hamming hosts, computes
induced degrees from the definition, and then recognizes the three theorem
forms by explicit line assignments.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from itertools import combinations, product
from math import comb


Vertex = tuple[int, ...]


def require(condition: bool, context: object) -> None:
    """A verification check that remains active under ``python -O``."""
    if not condition:
        raise RuntimeError(f"verification failed: {context!r}")


@dataclass(frozen=True)
class Host:
    sizes: tuple[int, ...]
    vertices: tuple[Vertex, ...]
    neighbours: tuple[int, ...]
    lines: tuple[int, ...]


def make_host(sizes: tuple[int, ...]) -> Host:
    if not sizes or min(sizes) < 1:
        raise ValueError("host factors must be positive")
    vertices = tuple(product(*(range(n) for n in sizes)))
    index = {v: i for i, v in enumerate(vertices)}

    neighbours = []
    for v in vertices:
        mask = 0
        for direction, order in enumerate(sizes):
            for symbol in range(order):
                if symbol != v[direction]:
                    w = v[:direction] + (symbol,) + v[direction + 1 :]
                    mask |= 1 << index[w]
        neighbours.append(mask)

    line_masks: list[int] = []
    for direction in range(len(sizes)):
        groups: dict[tuple[int, ...], int] = {}
        for i, v in enumerate(vertices):
            fixed = v[:direction] + v[direction + 1 :]
            groups[fixed] = groups.get(fixed, 0) | (1 << i)
        line_masks.extend(groups.values())

    # Factors of order one can produce duplicate geometric lines.  The theorem
    # concerns geometric coordinate lines, so canonicalize their vertex sets.
    return Host(sizes, vertices, tuple(neighbours), tuple(sorted(set(line_masks))))


def mask_from_vertices(host: Host, chosen: set[Vertex]) -> int:
    lookup = {v: i for i, v in enumerate(host.vertices)}
    return sum(1 << lookup[v] for v in chosen)


def induced_min_degree(host: Host, mask: int) -> int:
    if mask == 0:
        raise ValueError("minimum degree of the empty set is undefined")
    answer = len(host.vertices)
    pending = mask
    while pending:
        bit = pending & -pending
        i = bit.bit_length() - 1
        answer = min(answer, (host.neighbours[i] & mask).bit_count())
        pending ^= bit
    return answer


def essential_dimension(host: Host, mask: int) -> int:
    chosen = [host.vertices[i] for i in range(len(host.vertices)) if mask >> i & 1]
    return sum(len({v[j] for v in chosen}) > 1 for j in range(len(host.sizes)))


def assignments_on_two_lines(mask: int, first: int, second: int):
    """Yield disjoint assignments whose union is mask, one part per line."""
    if mask & ~(first | second):
        return
    only_first = mask & first & ~second
    only_second = mask & second & ~first
    intersection = mask & first & second
    if intersection == 0:
        yield only_first, only_second
    else:
        # Distinct Hamming lines meet in at most one point.  Assign that point
        # to exactly one of the two vertex-disjoint line subsets.
        require(intersection.bit_count() == 1, ("line intersection", intersection))
        yield only_first | intersection, only_second
        yield only_first, only_second | intersection


def every_point_meets(host: Host, small: int, large: int) -> bool:
    pending = small
    while pending:
        bit = pending & -pending
        i = bit.bit_length() - 1
        if not (host.neighbours[i] & large):
            return False
        pending ^= bit
    return True


def theorem_forms(host: Host, mask: int, h: int) -> frozenset[str]:
    """Recognize (L), (E), and (U) exactly from their definitions."""
    forms: set[str] = set()
    if any(mask & ~line == 0 for line in host.lines):
        forms.add("L")

    for p, first in enumerate(host.lines):
        for second in host.lines[p + 1 :]:
            for a, b in assignments_on_two_lines(mask, first, second):
                sizes = (a.bit_count(), b.bit_count())
                if sizes == (h + 1, h + 1):
                    forms.add("E")
                if sizes == (h + 2, h) and every_point_meets(host, b, a):
                    forms.add("U")
                if sizes == (h, h + 2) and every_point_meets(host, a, b):
                    forms.add("U")
    return frozenset(forms)


def shell_data(host: Host, mask: int, vertex_index: int, h: int):
    """Return the directional profile and both sides of the shell inequality."""
    v = host.vertices[vertex_index]
    profile = []
    for direction in range(len(host.sizes)):
        count = 0
        for i, w in enumerate(host.vertices):
            if not (mask >> i & 1):
                continue
            if all(v[j] == w[j] for j in range(len(v)) if j != direction):
                count += v != w
        if count:
            profile.append(count)
    degree = sum(profile)
    twice_lower = 2 * (1 + degree) + sum(a * (h - a) for a in profile)
    return tuple(sorted(profile, reverse=True)), twice_lower, 2 * mask.bit_count()


def enumerate_host(sizes: tuple[int, ...], h: int) -> dict[str, int]:
    host = make_host(sizes)
    order = 2 * h + 2
    if order > len(host.vertices):
        raise ValueError("host is too small")
    result = {"subsets": comb(len(host.vertices), order), "cores": 0,
              "L": 0, "E": 0, "U": 0, "overlaps": 0}
    for choice in combinations(range(len(host.vertices)), order):
        mask = sum(1 << i for i in choice)
        if induced_min_degree(host, mask) < h:
            continue
        result["cores"] += 1
        forms = theorem_forms(host, mask, h)
        require(bool(forms), (sizes, choice, forms))
        if len(forms) > 1:
            result["overlaps"] += 1
        for form in forms:
            result[form] += 1
        for i in choice:
            _, lower_twice, order_twice = shell_data(host, mask, i, h)
            require(lower_twice <= order_twice,
                    ("shell inequality", sizes, choice, i, lower_twice, order_twice))
    return result


def cross_edges(host: Host, first: int, second: int) -> int:
    total = 0
    pending = first
    while pending:
        bit = pending & -pending
        i = bit.bit_length() - 1
        total += (host.neighbours[i] & second).bit_count()
        pending ^= bit
    return total


def witness_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []

    def add(name: str, sizes: tuple[int, ...], chosen: set[Vertex], h: int,
            expected: set[str], expected_dimension: int, expected_cross: int | None = None,
            split: tuple[set[Vertex], set[Vertex]] | None = None) -> None:
        host = make_host(sizes)
        mask = mask_from_vertices(host, chosen)
        forms = theorem_forms(host, mask, h)
        require(forms == frozenset(expected), (name, forms))
        require(induced_min_degree(host, mask) >= h, (name, "minimum degree"))
        require(essential_dimension(host, mask) == expected_dimension,
                (name, "essential dimension"))
        if split is not None:
            first = mask_from_vertices(host, split[0])
            second = mask_from_vertices(host, split[1])
            require(cross_edges(host, first, second) == expected_cross,
                    (name, "cross edges"))
        records.append({"name": name, "forms": sorted(expected),
                        "minimum_degree": induced_min_degree(host, mask),
                        "dimension": essential_dimension(host, mask),
                        "cross_edges": expected_cross})

    line = {(a,) for a in range(14)}
    add("single_line", (14,), line, 6, {"L"}, 1)

    parallel_a = {(a, 0) for a in range(7)}
    parallel_b = {(a, 1) for a in range(7)}
    add("equal_direction_matching", (7, 2), parallel_a | parallel_b, 6,
        {"E"}, 2, 7, (parallel_a, parallel_b))

    separated_a = {(a, 0, 0) for a in range(7)}
    separated_b = {(a, 1, 1) for a in range(7)}
    add("separated_lines", (7, 2, 2), separated_a | separated_b, 6,
        {"E"}, 3, 0, (separated_a, separated_b))

    star_a = {(a, 0) for a in range(7)}
    star_b = {(0, b) for b in range(1, 8)}
    add("different_direction_star_overlap", (8, 8), star_a | star_b, 6,
        {"E", "U"}, 2, 7, (star_a, star_b))

    skew_a = {(a, 0, 0) for a in range(7)}
    skew_b = {(0, b, 1) for b in range(7)}
    add("third_direction_unique_edge", (7, 7, 2), skew_a | skew_b, 6,
        {"E"}, 3, 1, (skew_a, skew_b))

    matching_large = {(a, 0) for a in range(8)}
    matching_small = {(a, 1) for a in range(6)}
    add("unequal_parallel_matching", (8, 2), matching_large | matching_small,
        6, {"U"}, 2, 6, (matching_large, matching_small))

    u_star_large = {(a, 0) for a in range(8)}
    u_star_small = {(0, b) for b in range(1, 7)}
    add("unequal_star_overlap", (8, 7), u_star_large | u_star_small, 6,
        {"E", "U"}, 2, 6, (u_star_large, u_star_small))
    return records


def sharp_h5_record() -> dict[str, object]:
    host = make_host((4, 3))
    mask = (1 << len(host.vertices)) - 1
    profiles = {shell_data(host, mask, i, 5)[0] for i in range(len(host.vertices))}
    require(induced_min_degree(host, mask) == 5, "h=5 minimum degree")
    require(theorem_forms(host, mask, 5) == frozenset(), "h=5 forms")
    require(profiles == {(3, 2)}, ("h=5 profiles", profiles))
    return {"host": [4, 3], "order": 12, "minimum_degree": 5,
            "forms": [], "profiles": [[3, 2]]}


def elementary_line_facts() -> dict[str, int]:
    host = make_host((3, 3, 3))
    triangles = 0
    for triple in combinations(range(len(host.vertices)), 3):
        if all(host.neighbours[i] >> j & 1 for i, j in combinations(triple, 2)):
            triangles += 1
            triangle = sum(1 << i for i in triple)
            require(any(triangle & ~line == 0 for line in host.lines),
                    ("triangle outside lines", triple))

    outside_checks = 0
    for line in host.lines:
        for i in range(len(host.vertices)):
            if not (line >> i & 1):
                outside_checks += 1
                require((host.neighbours[i] & line).bit_count() <= 1,
                        ("outside point has two line neighbours", line, i))
    return {"triangles": triangles, "outside_point_line_checks": outside_checks}


def audit() -> dict[str, object]:
    enumerations = []
    expected = {
        (2, 8): {"subsets": 120, "cores": 120, "L": 0, "E": 64, "U": 56, "overlaps": 0},
        (2, 9): {"subsets": 3060, "cores": 1800, "L": 0, "E": 1296, "U": 504, "overlaps": 0},
        (3, 7): {"subsets": 116280, "cores": 3, "L": 0, "E": 3, "U": 0, "overlaps": 0},
        (3, 6): {"subsets": 3060, "cores": 0, "L": 0, "E": 0, "U": 0, "overlaps": 0},
        (4, 4): {"subsets": 120, "cores": 0, "L": 0, "E": 0, "U": 0, "overlaps": 0},
        (4, 5): {"subsets": 38760, "cores": 0, "L": 0, "E": 0, "U": 0, "overlaps": 0},
        (2, 2, 6): {"subsets": 1961256, "cores": 0, "L": 0, "E": 0, "U": 0, "overlaps": 0},
    }
    for sizes, wanted in expected.items():
        observed = enumerate_host(sizes, 6)
        require(observed == wanted, (sizes, observed))
        enumerations.append({"host": list(sizes), **observed})

    record = {
        "h6_enumerations": enumerations,
        "line_facts": elementary_line_facts(),
        "witnesses": witness_records(),
        "sharp_h5": sharp_h5_record(),
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    record["result_sha256"] = hashlib.sha256(canonical).hexdigest()
    return record


if __name__ == "__main__":
    result = audit()
    total_subsets = sum(r["subsets"] for r in result["h6_enumerations"])
    total_cores = sum(r["cores"] for r in result["h6_enumerations"])
    print(f"h=6 subsets enumerated: {total_subsets}")
    print(f"h=6 cores classified: {total_cores}")
    for row in result["h6_enumerations"]:
        print("host " + "x".join(map(str, row["host"])) +
              f": subsets={row['subsets']} cores={row['cores']} " +
              f"L={row['L']} E={row['E']} U={row['U']} overlaps={row['overlaps']}")
    print("line facts: " + json.dumps(result["line_facts"], sort_keys=True))
    overlap_witnesses = sum(len(row["forms"]) > 1 for row in result["witnesses"])
    print(f"explicit boundary witnesses: {len(result['witnesses'])}")
    print(f"explicit E/U overlap witnesses: {overlap_witnesses}")
    print("h=5 sharp control: K4xK3, profile=(3,2), unclassified")
    print(f"result sha256: {result['result_sha256']}")
    print("all independent exact checks passed")
