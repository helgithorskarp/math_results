#!/usr/bin/env python3
"""Independent reconstruction and semantic CNF audit for three Ramsey families.

No submitted code is imported.  For 1,044 cases this checker reconstructs
the physical partial graph from pinned data, derives candidate monochromatic
K5 clauses through recursive clique enumeration, compares the complete clause
set with fresh replay files and manifests, and audits endpoint transport.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path


ORDER = 43
ACTIVE = 40
PAIRS = list(combinations(range(ORDER), 2))
PAIR_INDEX = {edge: i for i, edge in enumerate(PAIRS)}
INPUTS_SHA256 = "8e17676c21e4b9c5b03c21e6fdba25d9d9325b77d0f1ee4f2718681c7db2fca2"
CATALOGUE_SHA256 = "f0fa14352dff513957204e078c7cc3fdf00ece103fdef7599f0b63e492a79a02"
FAMILIES = (
    {
        "label": "interface_9",
        "package": "ramsey_r55_dense_degree_five_hub_gap",
        "replay": "interface9",
        "interface": 9,
        "other": None,
        "free": 389,
        "active_free": 272,
        "manifest_sha256": "1488ce29cca3576c6afc8398d6fed0ea4c814d38a06fa4a512f1157df75567d2",
        "consensus_sha256": None,
    },
    {
        "label": "interfaces_1_2",
        "package": "ramsey_r55_type126_twenty_edge_kernel",
        "replay": "interfaces1-2",
        "interface": 1,
        "other": 2,
        "free": 409,
        "active_free": 292,
        "manifest_sha256": "fe9e7cbb7847ff5c5bff24ff11560d0957bc3b2d74a1c657900fe6bdd92f538f",
        "consensus_sha256": "cf3b3770875a7fc3737549be56e0c85747519052c807133ed0bef6796b40b82d",
    },
    {
        "label": "interfaces_3_4",
        "package": "ramsey_r55_type126_sixteen_edge_kernel",
        "replay": "interfaces3-4",
        "interface": 3,
        "other": 4,
        "free": 405,
        "active_free": 288,
        "manifest_sha256": "31a12430849216fbf8673dd820f688d0a6008d3d6e88898299a33989d3fc77f3",
        "consensus_sha256": "637c20a886d5a0d3cec87af9b096b0d48538872c9beb5e507d32179d2e2d35d6",
    },
)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> set[tuple[int, int]]:
    require(record and all(63 <= ord(ch) <= 126 for ch in record), "invalid graph6 characters")
    order = ord(record[0]) - 63
    require(order == 22, "unexpected graph6 order")
    needed = order * (order - 1) // 2
    bits = "".join(f"{ord(ch) - 63:06b}" for ch in record[1:])
    require(len(bits) == ((needed + 5) // 6) * 6 and "1" not in bits[needed:], "bad graph6 length/padding")
    result: set[tuple[int, int]] = set()
    offset = 0
    for v in range(order):
        for u in range(v):
            if bits[offset] == "1":
                result.add((u, v))
            offset += 1
    return result


def literal_markings(edges: set[tuple[int, int]]) -> list[tuple[int, ...]]:
    neighbors = [v for v in range(21) if tuple(sorted((v, 21))) in edges]
    require(neighbors == list(range(16, 21)), "unexpected degree-five neighborhood")
    result = [
        marking
        for marking in permutations(neighbors)
        if all(
            (tuple(sorted((marking[i], marking[j]))) in edges) == (i < 2 <= j)
            for i, j in combinations(range(5), 2)
        )
    ]
    require(len(result) == 12, "expected twelve literal K2,3 markings")
    return result


def build_matrix(
    edges: set[tuple[int, int]],
    columns: list[int],
    marking: tuple[int, ...],
    consensus_free: set[tuple[int, int]] | None,
) -> bytes:
    colors = [[2] * ORDER for _ in range(ORDER)]

    def put(u: int, v: int, value: int | bool) -> None:
        if u > v:
            u, v = v, u
        value = int(value)
        require(u != v and colors[u][v] in (2, value), "conflicting physical pin")
        colors[u][v] = colors[v][u] = value

    for edge in combinations(range(22), 2):
        if consensus_free is None or edge not in consensus_free:
            put(*edge, edge in edges)
    for vertex in range(ORDER):
        if vertex != 22:
            put(22, vertex, vertex < 22)
    for vertex in range(23, ORDER):
        put(21, vertex, vertex < 40)
    residues = {x * x % 17 for x in range(1, 17)}
    for u, v in combinations(range(17), 2):
        put(u + 23, v + 23, (u - v) % 17 in residues)
    for column, vertex in zip(columns, marking):
        for t in range(17):
            put(vertex, t + 23, bool(column & (1 << t)))

    raw = bytes(ord("0") + colors[u][v] for u, v in PAIRS)
    neighborhood = [22, *range(16, 21), *range(23, 40)]
    require(sum(colors[u][v] for u, v in combinations(neighborhood, 2)) == 116, "wrong equality density")
    return raw


def read_matrix(path: Path, expected_free: int, expected_active: int):
    raw = path.read_bytes()
    require(len(raw) == len(PAIRS) and all(ch in b"012" for ch in raw), f"invalid physical matrix: {path}")
    color = [[-1] * ORDER for _ in range(ORDER)]
    variables: dict[tuple[int, int], int] = {}
    for edge, byte in zip(PAIRS, raw):
        value = byte - ord("0")
        u, v = edge
        color[u][v] = color[v][u] = value
        if value == 2:
            variables[edge] = len(variables) + 1
    require(len(variables) == expected_free, f"wrong physical variable count: {path}")
    active = {number for (u, v), number in variables.items() if v < ACTIVE}
    require(len(active) == expected_active, f"wrong active variable count: {path}")
    return color, variables, active


def candidate_cliques(color: list[list[int]], wanted: int):
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


def expected_clauses(color: list[list[int]], variables: dict[tuple[int, int], int]) -> set[frozenset[int]]:
    result: set[frozenset[int]] = set()
    for wanted, sign in ((0, 1), (1, -1)):
        for vertices in candidate_cliques(color, wanted):
            clause = frozenset(
                sign * variables[edge]
                for edge in combinations(vertices, 2)
                if edge in variables
            )
            require(clause, "matrix contains a fixed monochromatic K5")
            result.add(clause)
    return result


def read_dimacs(path: Path) -> tuple[int, set[frozenset[int]]]:
    declared_variables = declared_clauses = None
    rows = 0
    clauses: set[frozenset[int]] = set()
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        fields = line.split()
        if fields[0] == "p":
            require(fields[:2] == ["p", "cnf"] and len(fields) == 4 and declared_variables is None, f"bad DIMACS header: {path}")
            declared_variables, declared_clauses = map(int, fields[2:])
            continue
        require(declared_variables is not None and fields[-1] == "0", f"bad DIMACS row: {path}")
        literals = [int(value) for value in fields[:-1]]
        require(literals and all(0 < abs(value) <= declared_variables for value in literals), f"bad DIMACS literal: {path}")
        clause = frozenset(literals)
        require(len(clause) == len(literals) and not any(-value in clause for value in clause), f"degenerate DIMACS clause: {path}")
        clauses.add(clause)
        rows += 1
    require(declared_variables is not None and declared_clauses == rows == len(clauses), f"DIMACS count/duplicate mismatch: {path}")
    return declared_variables, clauses


def prepare_family(source: Path, inputs: dict, config: dict):
    package = source / config["package"]
    manifest_path = package / "MANIFEST.json"
    require(digest(manifest_path) == config["manifest_sha256"], f"{config['label']}: manifest identity")
    manifest = json.loads(manifest_path.read_text())
    require(len(manifest) == 348, f"{config['label']}: manifest length")
    first = decode_graph6(inputs["interfaces"][config["interface"]])
    require(len(first) == 109, f"{config['label']}: source density")
    consensus = None
    consensus_free = None
    if config["other"] is not None:
        consensus_path = package / "CONSENSUS.json"
        require(digest(consensus_path) == config["consensus_sha256"], f"{config['label']}: consensus identity")
        consensus = json.loads(consensus_path.read_text())
        require(consensus["interfaces"] == [config["interface"], config["other"]], f"{config['label']}: interface pair")
        permutation = consensus["second_to_first"]
        require(sorted(permutation) == list(range(22)), f"{config['label']}: relabeling")
        second = decode_graph6(inputs["interfaces"][config["other"]])
        transported = {tuple(sorted((permutation[u], permutation[v]))) for u, v in second}
        consensus_free = set(map(tuple, consensus["free_common_edges"]))
        require(first ^ transported == consensus_free, f"{config['label']}: exact endpoint disagreement")
    return manifest, first, consensus, consensus_free


def audit_transport(
    inputs: dict,
    representatives: list[list[int]],
    config: dict,
    consensus: dict,
    targets: dict[tuple[int, int], bytes],
) -> int:
    first = decode_graph6(inputs["interfaces"][config["interface"]])
    target_markings = literal_markings(first)
    checks = 0
    multiplicity = {key: 0 for key in targets}
    for interface in (config["interface"], config["other"]):
        source_edges = decode_graph6(inputs["interfaces"][interface])
        mapping = list(range(ORDER)) if interface == config["interface"] else consensus["second_to_first"] + list(range(22, ORDER))
        edge_map = [PAIR_INDEX[tuple(sorted((mapping[u], mapping[v])))] for u, v in PAIRS]
        seen_markings: set[int] = set()
        for source_marking_index, marking in enumerate(literal_markings(source_edges)):
            transported_marking = tuple(mapping[v] for v in marking)
            target_marking_index = target_markings.index(transported_marking)
            seen_markings.add(target_marking_index)
            for representative_index, columns in enumerate(representatives):
                original = build_matrix(source_edges, columns, marking, None)
                target = targets[representative_index, target_marking_index]
                for source_position, destination in enumerate(edge_map):
                    require(target[destination] == ord("2") or target[destination] == original[source_position], f"{config['label']}: target pin not implied")
                    if original[source_position] == ord("2"):
                        require(target[destination] == ord("2"), f"{config['label']}: transport pins a free edge")
                    checks += 1
                multiplicity[representative_index, target_marking_index] += 1
        require(seen_markings == set(range(12)), f"{config['label']}: marking transport incomplete")
    require(set(multiplicity.values()) == {2} and checks == 696 * len(PAIRS), f"{config['label']}: endpoint transport coverage")
    return checks


def check_family(source: Path, replay_root: Path, inputs: dict, representatives: list[list[int]], config: dict) -> dict:
    manifest, first, consensus, consensus_free = prepare_family(source, inputs, config)
    markings = literal_markings(first)
    replay = replay_root / config["replay"] / "cohort"
    expected_keys = {(j, k) for j in range(29) for k in range(12)}
    seen_keys: set[tuple[int, int]] = set()
    targets: dict[tuple[int, int], bytes] = {}
    total_clauses = 0
    minimum = None
    maximum = None
    for position, row in enumerate(manifest, 1):
        raw_key = tuple(row["key"])
        if config["other"] is None:
            require(raw_key[:2] == (9, 126), "interface_9: malformed manifest key")
            key = raw_key[2:]
            stem = "-".join(map(str, raw_key))
        else:
            key = raw_key
            stem = "-".join(map(str, key))
        require(key in expected_keys and key not in seen_keys, f"{config['label']}: duplicate/invalid key")
        seen_keys.add(key)
        reconstructed = build_matrix(first, representatives[key[0]], markings[key[1]], consensus_free)
        require(reconstructed.count(b"2") == config["free"], f"{config['label']}: reconstructed free count")
        matrix_path = replay / f"{stem}.matrix"
        cnf_path = replay / f"{stem}.cnf"
        require(matrix_path.read_bytes() == reconstructed, f"{config['label']}: matrix reconstruction {stem}")
        require(digest(matrix_path) == row["matrix_sha256"], f"{config['label']}: matrix hash {stem}")
        require(digest(cnf_path) == row["cnf_sha256"], f"{config['label']}: CNF hash {stem}")
        color, variables, active = read_matrix(matrix_path, config["free"], config["active_free"])
        declared_variables, actual = read_dimacs(cnf_path)
        expected = expected_clauses(color, variables)
        require(declared_variables == config["free"] and actual == expected, f"{config['label']}: semantic CNF {stem}")
        used = {abs(literal) for clause in actual for literal in clause}
        require(used == active, f"{config['label']}: exact active support {stem}")
        require(row["variables"] == config["free"] and row["clauses"] == len(actual), f"{config['label']}: manifest counts {stem}")
        targets[key] = reconstructed
        total_clauses += len(actual)
        minimum = len(actual) if minimum is None else min(minimum, len(actual))
        maximum = len(actual) if maximum is None else max(maximum, len(actual))
        if position % 24 == 0:
            print(f"{config['label']}: {position}/348 semantic cases", flush=True)
    require(seen_keys == expected_keys and len(set(targets.values())) == 348, f"{config['label']}: complete distinct cohort")
    transport_checks = 0
    if consensus is not None:
        transport_checks = audit_transport(inputs, representatives, config, consensus, targets)
    return {
        "cases": len(seen_keys),
        "clause_range": [minimum, maximum],
        "kernel_edge_variables": config["active_free"],
        "manifest_sha256": config["manifest_sha256"],
        "physical_free_edges": config["free"],
        "status": "VERIFIED_INDEPENDENT_GLOBAL_SEMANTICS",
        "total_distinct_clauses": total_clauses,
        "transport_checks": transport_checks,
        "unconstrained_outside_edges": config["free"] - config["active_free"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="root of pinned math_source_code_open checkout")
    parser.add_argument("replay", type=Path, help="root holding the three fresh replay directories")
    args = parser.parse_args()
    upstream = args.source / "ramsey_r55_dense_degree23_hub_classification"
    inputs_path = upstream / "inputs.json"
    catalogue_path = upstream / "certificate.json"
    require(digest(inputs_path) == INPUTS_SHA256, "upstream inputs identity")
    require(digest(catalogue_path) == CATALOGUE_SHA256, "upstream catalogue identity")
    inputs = json.loads(inputs_path.read_text())
    catalogue = json.loads(catalogue_path.read_text())
    families = [family for family in catalogue["families"] if family["type"] == 126]
    require(len(families) == 1 and len(families[0]["representatives"]) == 29, "type-126 equality catalogue")
    representatives = [row["columns"] for row in families[0]["representatives"]]
    require(all(len(row) == 5 and sum(column.bit_count() for column in row) == 37 for row in representatives), "malformed equality columns")
    result = {
        config["label"]: check_family(args.source, args.replay, inputs, representatives, config)
        for config in FAMILIES
    }
    result["cases"] = sum(item["cases"] for item in result.values())
    result["status"] = "VERIFIED_ALL_1044_GLOBAL_KERNEL_SEMANTICS"
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
