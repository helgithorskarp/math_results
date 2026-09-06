#!/usr/bin/env python3
"""Independent semantic audit of the 348 physical-matrix Ramsey kernels.

This reviewer implementation imports no module from the submitted package.
It reads the replayed matrices and DIMACS files, independently enumerates
all candidate monochromatic K5s by recursive clique search, and compares the
resulting clause sets.  CNF and matrix identities are also checked against
the compact submitted manifest.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ORDER = 43
ACTIVE = 40
PAIR_COUNT = ORDER * (ORDER - 1) // 2
EXPECTED_CASES = 29 * 12
EXPECTED_FREE = 413
EXPECTED_ACTIVE_FREE = 296
EXPECTED_MANIFEST_SHA256 = "42e4692b75d87d3a34345238da60502d77c1b62b6ce20699473ff4e24f9c0a00"
EXPECTED_INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
EXPECTED_CATALOGUE_SHA256 = "f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02"
EXPECTED_CONSENSUS_SHA256 = "7fa72225a69391ada04c0828529764320bc3b061fc91103d40c26a4b9c3018ad"


def fail(message: str) -> None:
    raise ValueError(message)


def decode_graph6(record: str) -> set[tuple[int, int]]:
    order = ord(record[0]) - 63
    bits = "".join(f"{ord(ch) - 63:06b}" for ch in record[1:])
    needed = order * (order - 1) // 2
    if order != 22 or len(bits) != ((needed + 5) // 6) * 6 or "1" in bits[needed:]:
        fail("invalid source graph6 record")
    edges: set[tuple[int, int]] = set()
    offset = 0
    for v in range(order):
        for u in range(v):
            if bits[offset] == "1":
                edges.add((u, v))
            offset += 1
    return edges


def literal_markings(edges: set[tuple[int, int]]) -> list[tuple[int, ...]]:
    neighbors = [v for v in range(21) if (v, 21) in edges]
    if len(neighbors) != 5:
        fail("source interface has the wrong hub neighborhood")
    result = []
    for marking in permutations(neighbors):
        okay = all(
            ((min(marking[i], marking[j]), max(marking[i], marking[j])) in edges) == (i < 2 <= j)
            for i, j in combinations(range(5), 2)
        )
        if okay:
            result.append(marking)
    if len(result) != 12:
        fail("source interface does not have 12 literal K2,3 markings")
    return result


def build_expected_matrix(
    edges: set[tuple[int, int]],
    columns: list[int],
    marking: tuple[int, ...],
    consensus_free: set[tuple[int, int]] | None,
) -> bytes:
    physical = [[2] * ORDER for _ in range(ORDER)]

    def put(u: int, v: int, value: int | bool) -> None:
        if u > v:
            u, v = v, u
        value = int(value)
        if u == v or physical[u][v] not in (2, value):
            fail("conflicting physical pin")
        physical[u][v] = physical[v][u] = value

    for edge in combinations(range(22), 2):
        if consensus_free is None or edge not in consensus_free:
            put(*edge, edge in edges)
    for vertex in range(43):
        if vertex != 22:
            put(22, vertex, vertex < 22)
    for vertex in range(23, 43):
        put(21, vertex, vertex < 40)
    quadratic_residues = {value * value % 17 for value in range(1, 17)}
    for u, v in combinations(range(17), 2):
        put(u + 23, v + 23, (u - v) % 17 in quadratic_residues)
    for column, vertex in zip(columns, marking):
        for core_vertex in range(17):
            put(vertex, core_vertex + 23, bool(column & (1 << core_vertex)))

    raw = bytes(ord("0") + physical[u][v] for u, v in combinations(range(43), 2))
    expected_free = 389 if consensus_free is None else 413
    if raw.count(b"2") != expected_free:
        fail(f"wrong reconstructed free-edge count: {raw.count(b'2')}")
    neighborhood = [22, *sorted(marking), *range(23, 40)]
    density = sum(physical[u][v] for u, v in combinations(neighborhood, 2))
    if density != 116:
        fail(f"wrong reconstructed equality density: {density}")
    return raw


def read_matrix(path: Path) -> tuple[list[list[int]], dict[tuple[int, int], int]]:
    raw = path.read_bytes()
    if len(raw) != PAIR_COUNT or any(ch not in b"012" for ch in raw):
        fail(f"invalid physical matrix: {path}")
    color = [[-1] * ORDER for _ in range(ORDER)]
    variables: dict[tuple[int, int], int] = {}
    offset = 0
    next_variable = 1
    for u in range(ORDER):
        for v in range(u + 1, ORDER):
            value = raw[offset] - ord("0")
            offset += 1
            color[u][v] = color[v][u] = value
            if value == 2:
                variables[u, v] = next_variable
                next_variable += 1
    if len(variables) != EXPECTED_FREE:
        fail(f"wrong free-edge count in {path}: {len(variables)}")
    active_free = sum(v < ACTIVE for _, v in variables)
    if active_free != EXPECTED_ACTIVE_FREE:
        fail(f"wrong active free-edge count in {path}: {active_free}")
    return color, variables


def candidate_cliques(color: list[list[int]], wanted: int):
    """Yield each candidate K5 once using only compatible-edge recursion."""
    adjacency = [0] * ACTIVE
    for u in range(ACTIVE):
        for v in range(u + 1, ACTIVE):
            if color[u][v] in (wanted, 2):
                adjacency[u] |= 1 << v
                adjacency[v] |= 1 << u

    def visit(chosen: tuple[int, ...], candidates: int):
        needed = 5 - len(chosen)
        while candidates.bit_count() >= needed:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            if needed == 1:
                yield chosen + (vertex,)
            else:
                yield from visit(chosen + (vertex,), candidates & adjacency[vertex])

    yield from visit((), (1 << ACTIVE) - 1)


def expected_clauses(
    color: list[list[int]], variables: dict[tuple[int, int], int]
) -> set[frozenset[int]]:
    clauses: set[frozenset[int]] = set()
    for wanted, sign in ((0, 1), (1, -1)):
        for vertices in candidate_cliques(color, wanted):
            clause = frozenset(
                sign * variables[edge]
                for edge in combinations(vertices, 2)
                if edge in variables
            )
            if not clause:
                fail("physical matrix already contains a fixed monochromatic K5")
            clauses.add(clause)
    return clauses


def read_dimacs(path: Path) -> tuple[int, set[frozenset[int]]]:
    declared_variables = declared_clauses = None
    clauses: set[frozenset[int]] = set()
    observed_rows = 0
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        fields = line.split()
        if fields[0] == "p":
            if fields[:2] != ["p", "cnf"] or len(fields) != 4 or declared_variables is not None:
                fail(f"invalid DIMACS header: {path}")
            declared_variables, declared_clauses = map(int, fields[2:])
            continue
        if declared_variables is None or fields[-1] != "0":
            fail(f"invalid DIMACS clause: {path}")
        literals = [int(value) for value in fields[:-1]]
        if not literals or any(value == 0 or abs(value) > declared_variables for value in literals):
            fail(f"invalid DIMACS literal: {path}")
        clause = frozenset(literals)
        if len(clause) != len(literals) or any(-value in clause for value in clause):
            fail(f"repeated or complementary literals: {path}")
        clauses.add(clause)
        observed_rows += 1
    if declared_variables is None or declared_clauses != observed_rows or len(clauses) != observed_rows:
        fail(f"DIMACS count or duplicate mismatch: {path}")
    return declared_variables, clauses


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("replay", type=Path, help="directory containing replayed .matrix and .cnf files")
    parser.add_argument("manifest", type=Path, help="submitted MANIFEST.json")
    parser.add_argument("inputs", type=Path, help="accepted dense-hub inputs.json")
    parser.add_argument("catalogue", type=Path, help="accepted dense-hub certificate.json")
    parser.add_argument("consensus", type=Path, help="submitted CONSENSUS.json")
    args = parser.parse_args()

    manifest_raw = args.manifest.read_bytes()
    if sha256(manifest_raw).hexdigest() != EXPECTED_MANIFEST_SHA256:
        fail("unexpected submitted manifest identity")
    manifest = json.loads(manifest_raw)
    if len(manifest) != EXPECTED_CASES:
        fail(f"wrong manifest length: {len(manifest)}")
    pinned = (
        (args.inputs, EXPECTED_INPUTS_SHA256, "inputs"),
        (args.catalogue, EXPECTED_CATALOGUE_SHA256, "catalogue"),
        (args.consensus, EXPECTED_CONSENSUS_SHA256, "consensus"),
    )
    for path, expected_hash, label in pinned:
        if file_sha256(path) != expected_hash:
            fail(f"unexpected {label} identity")
    inputs = json.loads(args.inputs.read_text())
    catalogue = json.loads(args.catalogue.read_text())
    consensus = json.loads(args.consensus.read_text())
    first = decode_graph6(inputs["interfaces"][10])
    second_original = decode_graph6(inputs["interfaces"][11])
    relabeling = consensus["second_to_first"]
    if sorted(relabeling) != list(range(22)):
        fail("invalid consensus relabeling")
    second = {tuple(sorted((relabeling[u], relabeling[v]))) for u, v in second_original}
    consensus_free = set(map(tuple, consensus["free_common_edges"]))
    if first ^ second != consensus_free or len(consensus_free) != 24:
        fail("consensus is not the exact endpoint disagreement set")
    families = [family for family in catalogue["families"] if family["type"] == 126]
    if len(families) != 1 or len(families[0]["representatives"]) != 29:
        fail("wrong type-126 equality catalogue")
    representatives = [row["columns"] for row in families[0]["representatives"]]
    if any(len(row) != 5 or sum(column.bit_count() for column in row) != 37 for row in representatives):
        fail("malformed type-126 equality representative")
    target_markings = literal_markings(first)
    expected_keys = {(j, k) for j in range(29) for k in range(12)}
    seen_keys: set[tuple[int, int]] = set()
    target_matrices: dict[tuple[int, int], bytes] = {}
    total_clauses = 0
    for index, row in enumerate(manifest, 1):
        key = tuple(row["key"])
        if key not in expected_keys or key in seen_keys:
            fail(f"invalid or duplicate key: {key}")
        seen_keys.add(key)
        stem = f"{key[0]}-{key[1]}"
        matrix_path = args.replay / f"{stem}.matrix"
        cnf_path = args.replay / f"{stem}.cnf"
        reconstructed = build_expected_matrix(
            first, representatives[key[0]], target_markings[key[1]], consensus_free
        )
        if matrix_path.read_bytes() != reconstructed:
            fail(f"physical reconstruction mismatch: {stem}")
        target_matrices[key] = reconstructed
        if file_sha256(matrix_path) != row["matrix_sha256"]:
            fail(f"matrix hash mismatch: {stem}")
        if file_sha256(cnf_path) != row["cnf_sha256"]:
            fail(f"CNF hash mismatch: {stem}")
        color, variables = read_matrix(matrix_path)
        declared_variables, actual = read_dimacs(cnf_path)
        expected = expected_clauses(color, variables)
        if declared_variables != EXPECTED_FREE or actual != expected:
            fail(f"semantic CNF mismatch: {stem}")
        if len(actual) != row["clauses"] or row["variables"] != EXPECTED_FREE:
            fail(f"manifest count mismatch: {stem}")
        total_clauses += len(actual)
        if index % 12 == 0:
            print(f"{index} of {EXPECTED_CASES} cases semantically verified", flush=True)
    if seen_keys != expected_keys:
        fail("incomplete marked cohort")

    pairs = list(combinations(range(43), 2))
    pair_index = {edge: index for index, edge in enumerate(pairs)}
    transport_checks = 0
    for interface, source_edges in ((10, first), (11, second_original)):
        mapping = list(range(43)) if interface == 10 else relabeling + list(range(22, 43))
        for source_marking_index, source_marking in enumerate(literal_markings(source_edges)):
            transported_marking = tuple(mapping[vertex] for vertex in source_marking)
            target_marking_index = target_markings.index(transported_marking)
            for representative_index, columns in enumerate(representatives):
                original = build_expected_matrix(source_edges, columns, source_marking, None)
                target = target_matrices[representative_index, target_marking_index]
                for source_index, (u, v) in enumerate(pairs):
                    mapped_edge = tuple(sorted((mapping[u], mapping[v])))
                    destination = pair_index[mapped_edge]
                    if target[destination] != ord("2") and target[destination] != original[source_index]:
                        fail("a target fixed color is not implied by an original template")
                    if original[source_index] == ord("2") and target[destination] != ord("2"):
                        fail("transport pins an originally free edge")
                    transport_checks += 1
    if transport_checks != 696 * PAIR_COUNT:
        fail("incomplete endpoint transport audit")

    result = {
        "active_vertices": ACTIVE,
        "cases": EXPECTED_CASES,
        "kernel_edge_variables": EXPECTED_ACTIVE_FREE,
        "manifest_sha256": sha256(manifest_raw).hexdigest(),
        "physical_free_edges": EXPECTED_FREE,
        "status": "VERIFIED_GLOBAL_RECONSTRUCTION_TRANSPORT_AND_CNF_SEMANTICS",
        "total_distinct_clauses": total_clauses,
        "transport_checks": transport_checks,
        "unconstrained_outside_edges": EXPECTED_FREE - EXPECTED_ACTIVE_FREE,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
