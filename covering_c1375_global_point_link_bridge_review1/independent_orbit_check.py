#!/usr/bin/env python3
"""Independent incidence-graph audit of the C(13,7,5) bridge orbit table.

This deliberately does not import the reviewed generator.  It reads the
41-block source cover directly, extracts the 20-block second link, and asks
NetworkX's generic colored-graph isomorphism engine for all automorphisms of
the link's bipartite incidence graph.  It then recomputes the induced orbits
on six-subsets of the eleven link points.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx


POINTS = tuple(range(2, 13))


def read_cover(path: Path) -> list[tuple[int, ...]]:
    rows: list[tuple[int, ...]] = []
    for raw in path.read_text(encoding="ascii").splitlines():
        text = raw.split("#", 1)[0].strip()
        if text:
            rows.append(tuple(sorted(map(int, text.split()))))
    assert len(rows) == len(set(rows)) == 41
    assert all(len(row) == 6 and set(row) <= set(range(1, 13)) for row in rows)
    assert all(
        any(set(target) <= set(row) for row in rows)
        for target in combinations(range(1, 13), 4)
    )
    return rows


def extract_second_link(cover: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    assert sum(1 in row for row in cover) == 20
    link = [tuple(x for x in row if x != 1) for row in cover if 1 in row]
    assert len(link) == len(set(link)) == 20
    assert all(len(row) == 5 and set(row) <= set(POINTS) for row in link)
    assert all(
        any(set(target) <= set(row) for row in link)
        for target in combinations(POINTS, 3)
    )
    degree = Counter(x for row in link for x in row)
    assert sorted(degree.values()) == [9] * 10 + [10]
    return link


def incidence_automorphisms(link: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    graph = nx.Graph()
    for point in POINTS:
        graph.add_node(("p", point), color="point")
    for index, row in enumerate(link):
        block = ("b", index)
        graph.add_node(block, color="block")
        graph.add_edges_from((block, ("p", point)) for point in row)

    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph,
        graph,
        node_match=nx.algorithms.isomorphism.categorical_node_match("color", None),
    )
    permutations: set[tuple[int, ...]] = set()
    for mapping in matcher.isomorphisms_iter():
        permutation = tuple(mapping[("p", point)][1] for point in POINTS)
        assert set(permutation) == set(POINTS)
        permutations.add(permutation)
    assert len(permutations) == 240
    return permutations


def orbit_rows(
    permutations: set[tuple[int, ...]],
) -> list[tuple[int, tuple[int, ...]]]:
    domain = set(combinations(POINTS, 6))
    unseen = set(domain)
    rows: list[tuple[int, tuple[int, ...]]] = []
    while unseen:
        seed = min(unseen)
        orbit = {
            tuple(sorted(permutation[x - 2] for x in seed))
            for permutation in permutations
        }
        assert orbit <= domain
        representative = min(orbit)
        assert representative == seed
        rows.append((len(orbit), representative))
        unseen -= orbit
    assert sum(size for size, _ in rows) == len(domain) == 462
    assert len(rows) == 12
    return rows


def expected_text(rows: list[tuple[int, tuple[int, ...]]]) -> str:
    out = [
        "automorphisms=240",
        "six_subset_orbits=12 domain=462",
        "orbit\tsize\trepresentative",
    ]
    out.extend(
        f"{index}\t{size}\t" + " ".join(map(str, representative))
        for index, (size, representative) in enumerate(rows)
    )
    return "\n".join(out) + "\n"


def counting_checks() -> None:
    assert 77 * 7 - 13 * 41 == 6
    assert 41 * 6 - 12 * 20 == 6
    assert 41 * 15 - 66 * 9 == 21
    assert all(5 * (20 + a) - 11 * 9 == 1 + 5 * a for a in range(7))

    partitions: list[tuple[int, ...]] = []

    def visit(remainder: int, ceiling: int, prefix: tuple[int, ...]) -> None:
        if remainder == 0:
            partitions.append(prefix)
            return
        for part in range(min(remainder, ceiling), 0, -1):
            visit(remainder - part, part, prefix + (part,))

    visit(6, 6, ())
    allowed = [partition for partition in partitions if max(partition) <= 4]
    assert len(allowed) == 9
    assert set(partitions) - set(allowed) == {(6,), (5, 1)}


def coverage_prefix(link: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    ground = tuple(range(13))
    fixed = [frozenset((0, 1, *row)) for row in link]
    b_blocks = [(0, *row) for row in combinations(POINTS, 6)]
    c_blocks = [(1, *row) for row in combinations(POINTS, 6)]
    d_blocks = list(combinations(POINTS, 7))
    primary = [frozenset(row) for row in b_blocks + c_blocks + d_blocks]
    assert len(primary) == 1254
    clauses: list[tuple[int, ...]] = []
    for target in combinations(ground, 5):
        target_set = frozenset(target)
        if any(target_set <= block for block in fixed):
            continue
        clause = tuple(
            variable
            for variable, block in enumerate(primary, 1)
            if target_set <= block
        )
        assert clause
        clauses.append(clause)
    assert len(clauses) == 902
    return clauses


def read_primary_prefix(path: Path, length: int) -> tuple[int, int, list[tuple[int, ...]]]:
    variables = clauses = None
    body: list[tuple[int, ...]] = []
    with path.open("r", encoding="ascii") as handle:
        for raw in handle:
            if raw.startswith("c"):
                continue
            if raw.startswith("p cnf "):
                _, _, raw_variables, raw_clauses = raw.split()
                variables, clauses = int(raw_variables), int(raw_clauses)
                continue
            if len(body) < length:
                values = tuple(map(int, raw.split()))
                assert values and values[-1] == 0
                body.append(values[:-1])
            else:
                break
    assert variables is not None and clauses is not None and len(body) == length
    return variables, clauses, body


def audit_generated(
    cnf_dir: Path,
    manifest_path: Path,
    expected_prefix: list[tuple[int, ...]],
) -> None:
    rows = list(csv.DictReader(manifest_path.open(encoding="ascii"), delimiter="\t"))
    assert len(rows) == 13
    for row in rows:
        filename = "e0.cnf" if row["case"] == "e0" else f"e1-orbit{row['orbit']}.cnf"
        path = cnf_dir / filename
        assert path.stat().st_size == int(row["bytes"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        variables, clauses, actual_prefix = read_primary_prefix(path, len(expected_prefix))
        assert variables == int(row["vars"])
        assert clauses == int(row["clauses"])
        assert actual_prefix == expected_prefix


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cover", type=Path)
    parser.add_argument("expected", type=Path)
    parser.add_argument("--cnf-dir", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    if (args.cnf_dir is None) != (args.manifest is None):
        parser.error("--cnf-dir and --manifest must be supplied together")

    counting_checks()
    cover = read_cover(args.cover)
    link = extract_second_link(cover)
    permutations = incidence_automorphisms(link)
    rows = orbit_rows(permutations)
    actual = expected_text(rows)
    expected = args.expected.read_text(encoding="ascii")
    assert actual == expected
    if args.cnf_dir is not None and args.manifest is not None:
        audit_generated(args.cnf_dir, args.manifest, coverage_prefix(link))
    print("independent_incidence_graph_check=PASS")
    print(f"networkx={nx.__version__}")
    print("source_cover_blocks=41 second_link_blocks=20 covered_triples=165")
    print("second_link_degree_profile=10,9^10")
    print("automorphisms=240 six_subset_orbits=12 orbit_size_sum=462")
    print("orbit_sizes=" + ",".join(str(size) for size, _ in rows))
    print("orbit_table_sha256=" + hashlib.sha256(actual.encode("ascii")).hexdigest())
    print("counting_identities=PASS degree_excess_profiles=9")
    if args.cnf_dir is not None:
        print("generated_manifest_rows=13 primary_coverage_prefixes=PASS")


if __name__ == "__main__":
    main()
