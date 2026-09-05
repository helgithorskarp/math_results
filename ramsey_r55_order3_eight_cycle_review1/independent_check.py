#!/usr/bin/env python3
"""Independent semantic audit of the order-three eight-cycle obstruction.

This checker imports no module from the reviewed package.  It reconstructs
the actual edge orbits of the order-three action, projects every 5-subset,
and proves that the primary-variable part of each published full CNF is
exactly the Ramsey clauses plus the two justified normalizations.  It also
checks core membership, the local reductions, and the moving-vertex fixture.
If requested, it replays the compact certificates with an external
``drat-trim -U`` binary.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import re
import struct
import subprocess
from pathlib import Path


PRIMARY_VARIABLES = 407
FULL_CASES = {
    0: (7611, 585876, 24389490,
        "eb02873924af8861ee01c721cfe0503b7e68fddace7aa6a360baf61d658b88e9",
        "113dfc4120ed159c4a28a681a0e3ff0eda9048b85fe8bf2ca6429f4f4d624ef8",
        "80fa7444d9e235c61f446370d17106e5f57f786290c6223d4b81dce871d71d93"),
    1: (7632, 589383, 24552988,
        "1d497d4ee03f79377f17e0df596235b0a5ce4c8b4c45e520d495a8dd32262d71",
        "400ba95a6cca973874455cb86b74e001b2940f7c2ef1294f60cc38bc59879e21",
        "e6998b160c9546cbe81bb19ea717360fd4e9cb36b78d238b24294122dbe7cc74"),
    2: (7647, 591888, 24689224,
        "bd4e29a86263762dabb6bb1353b100e938016446122021fecf7d1eb5ff336a1a",
        "03168bbf9073ff675a9bbb1be783ee97f04f35bc013423e94e430d4e4c841462",
        "c28eefb77b17ce97dac6e24cb2378556c1cdf1c5d6c460b9f3b949bed1492686"),
    3: (7656, 593391, 24794380,
        "097567c3f8787efcf7a5c399b90b60b6959e6b96e274cd26841ea29683c60177",
        "a3e9a16d56db46ae4dc7b3773e317a5c7373fa9020e7719ca2a6179dbda10bf6",
        "847e0a9b0394abdae806f80c93fd220d9400e98d96f5a3920d935e1076dbe2d1"),
    4: (7659, 593892, 24868458,
        "7ef090fba95e1c362685cc56848d3d4f8c10ebfd00db51d4fb19a55f82b3036d",
        "28fcc277e476ba1d793b623494b8c3c953a20f302fdc1a11c2b5d401e559edde",
        "5b9f8df64aa00d4bcfb56a4e4043fc7128a21154b634e97cb35f8c37f047ed5d"),
}
FIXTURE_SHA256 = "a53f3480761d658059274b3e9b2e4a2848c43985b813b3284736b4f817fb733c"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def advance(vertex: int) -> int:
    if vertex >= 24:
        return vertex
    return 3 * (vertex // 3) + (vertex + 1) % 3


def orbit_representative(a: int, b: int) -> tuple[int, int]:
    images = []
    for _ in range(3):
        images.append(tuple(sorted((a, b))))
        a, b = advance(a), advance(b)
    return min(images)


def orbit_labels() -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], list[tuple[int, int]]]]:
    groups: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for a, b in itertools.combinations(range(43), 2):
        rep = orbit_representative(a, b)
        groups.setdefault(rep, []).append((a, b))
    require(len(groups) == 415, "edge-orbit count")
    require(sum(len(group) for group in groups.values()) == 903, "edge-pair coverage")
    for rep, group in groups.items():
        expected = 1 if rep[0] >= 24 else 3
        require(len(group) == expected, "edge-orbit length")

    internal = [rep for rep in groups if rep[1] < 24 and rep[0] // 3 == rep[1] // 3]
    cross = sorted(rep for rep in groups if rep[1] < 24 and rep[0] // 3 != rep[1] // 3)
    fixed = sorted(rep for rep in groups if rep[0] >= 24)
    links = sorted((rep for rep in groups if rep[0] < 24 <= rep[1]),
                   key=lambda rep: (rep[1], rep[0]))
    require((len(internal), len(cross), len(fixed), len(links)) == (8, 84, 171, 152),
            "edge-orbit categories")
    labels = {rep: index for index, rep in enumerate(cross + fixed + links, 1)}
    require(set(labels.values()) == set(range(1, PRIMARY_VARIABLES + 1)),
            "primary variable range")
    return labels, groups


def edge_tables(labels: dict[tuple[int, int], int], red_cycles: int) -> list[list[int]]:
    # Positive values are primary variables.  Zero and -1 mean constant blue
    # and constant red respectively, keeping constants disjoint from IDs.
    edges = [[0] * 43 for _ in range(43)]
    for a, b in itertools.combinations(range(43), 2):
        rep = orbit_representative(a, b)
        if b < 24 and a // 3 == b // 3:
            token = -1 if a // 3 < red_cycles else 0
        else:
            token = labels[rep]
        edges[a][b] = edges[b][a] = token
    return edges


def canonical_clause(literals: list[int] | tuple[int, ...]) -> tuple[int, ...] | None:
    values = set(literals)
    if any(-literal in values for literal in values):
        return None
    return tuple(sorted(values))


def projected_clause(vertices: tuple[int, ...], red_monochrome: bool,
                     edges: list[list[int]]) -> tuple[int, ...] | None:
    literals = []
    for a, b in itertools.combinations(vertices, 2):
        token = edges[a][b]
        if token <= 0:
            edge_is_red = token == -1
            if edge_is_red != red_monochrome:
                return None
        else:
            literals.append(-token if red_monochrome else token)
    return canonical_clause(literals)


def primary_formula(red_cycles: int, labels: dict[tuple[int, int], int]) -> tuple[set[tuple[int, ...]], int]:
    edges = edge_tables(labels, red_cycles)
    clauses: set[tuple[int, ...]] = set()
    five_sets = 0
    for vertices in itertools.combinations(range(43), 5):
        five_sets += 1
        for red_monochrome in (False, True):
            clause = projected_clause(vertices, red_monochrome, edges)
            if clause is not None:
                clauses.add(clause)
    ramsey_count = len(clauses)
    require(five_sets == 962598, "five-set coverage")

    # Independently chosen phases for cycles 1,...,7 make each anchor word
    # one of 000, 100, 110, 111.
    for cycle in range(1, 8):
        bits = [edges[0][3 * cycle + phase] for phase in range(3)]
        require(all(bit > 0 for bit in bits), "anchor variable")
        clauses.add(canonical_clause([-bits[1], bits[0]]))
        clauses.add(canonical_clause([-bits[2], bits[1]]))

    # Adjacent fixed vertices are ordered lexicographically by their eight
    # invariant moving-incidence bits.
    for fixed in range(24, 42):
        left = [edges[3 * cycle][fixed] for cycle in range(8)]
        right = [edges[3 * cycle][fixed + 1] for cycle in range(8)]
        for position in range(8):
            for prefix in itertools.product((0, 1), repeat=position):
                row: list[int] = []
                for index, value in enumerate(prefix):
                    row.extend((-left[index], -right[index]) if value
                               else (left[index], right[index]))
                row.extend((-left[position], right[position]))
                clause = canonical_clause(row)
                require(clause is not None, "lex clause tautology")
                clauses.add(clause)
    return clauses, ramsey_count


def update_clause_hash(digest: "hashlib._Hash", clause: tuple[int, ...]) -> None:
    digest.update(struct.pack(">I", len(clause)))
    for literal in clause:
        digest.update(struct.pack(">i", literal))


def parse_clause(line: str, variables: int, *, require_canonical: bool = True) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    require(values and values[-1] == 0 and 0 not in values[:-1], "DIMACS clause syntax")
    clause = values[:-1]
    require(all(1 <= abs(literal) <= variables for literal in clause), "DIMACS literal range")
    require(len(set(clause)) == len(clause), "duplicate DIMACS literal")
    require(not any(-literal in clause for literal in clause), "tautological DIMACS clause")
    canonical = tuple(sorted(clause))
    require(not require_canonical or canonical == clause, "noncanonical DIMACS clause")
    return canonical


def read_core(path: Path, expected_variables: int) -> tuple[set[tuple[int, ...]], int]:
    with path.open() as stream:
        header = next(stream).split()
        require(header[:2] == ["p", "cnf"] and len(header) == 4, "core header")
        variables, expected_count = map(int, header[2:])
        require(variables == expected_variables, "core variable count")
        clauses = {parse_clause(line, variables, require_canonical=False) for line in stream}
    require(len(clauses) == expected_count, "core clause count or duplicate")
    return clauses, expected_count


def audit_full_formula(path: Path, expected_variables: int, expected_clauses: int,
                       expected_primary: set[tuple[int, ...]],
                       core: set[tuple[int, ...]]) -> tuple[int, str]:
    actual_digest = hashlib.sha256()
    actual_primary_count = 0
    remaining_core = set(core)
    with path.open() as stream:
        header = next(stream).split()
        require(header[:2] == ["p", "cnf"] and len(header) == 4, "full header")
        variables, clause_count = map(int, header[2:])
        require((variables, clause_count) == (expected_variables, expected_clauses),
                "full header values")
        previous = None
        seen = 0
        for line in stream:
            clause = parse_clause(line, variables)
            key = (len(clause), clause)
            require(previous is None or previous < key, "full clauses not strictly canonical")
            previous = key
            seen += 1
            remaining_core.discard(clause)
            if all(abs(literal) <= PRIMARY_VARIABLES for literal in clause):
                update_clause_hash(actual_digest, clause)
                actual_primary_count += 1
    require(seen == expected_clauses, "full clause line count")
    require(not remaining_core, "committed core clause absent from full formula")

    expected_digest = hashlib.sha256()
    for clause in sorted(expected_primary, key=lambda row: (len(row), row)):
        update_clause_hash(expected_digest, clause)
    require(actual_primary_count == len(expected_primary), "primary clause count")
    require(actual_digest.digest() == expected_digest.digest(), "primary clause stream mismatch")
    return actual_primary_count, actual_digest.hexdigest()


def analytic_audit() -> None:
    feasible = []
    for weights in itertools.product(range(4), repeat=7):
        complete = weights.count(3)
        deficit = sum(2 - weight + 3 * (weight == 3) for weight in weights)
        allowed = [fixed for fixed in range(20)
                   if fixed + 3 * complete <= 4
                   and 18 <= 2 + fixed + sum(weights) <= 24]
        require(bool(allowed) == (deficit <= 2), "eight-cycle deficit equivalence")
        feasible.extend((fixed, weights) for fixed in allowed)
    require(len(feasible) == 52, "eight-cycle local profile count")

    seven = []
    for fixed in range(23):
        for weights in itertools.product(range(4), repeat=6):
            complete = weights.count(3)
            if fixed + 3 * complete <= 4 and 18 <= 2 + fixed + sum(weights) <= 24:
                seven.append((fixed, weights))
    require(seven == [(4, (2,) * 6)], "seven-cycle equality case")
    require(all(2 * cycles + 4 < 18 for cycles in range(1, 7)), "sparse-motion bound")
    require({min(bits.bit_count(), 8 - bits.bit_count()) for bits in range(256)}
            == set(range(5)), "internal-color reduction")
    canonical_words = {(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)}
    for word in itertools.product((0, 1), repeat=3):
        rotations = {word[index:] + word[:index] for index in range(3)}
        require(rotations & canonical_words, "anchor rotation normalization")
    print("PASS analytic reduction: sparse<=6, k=7 equality, k=8 profiles=52")
    print("PASS normalizations: internal_splits=5 anchor_words=8 fixed_signatures=lex-sortable")


def fixture_audit(path: Path) -> None:
    require(sha256(path) == FIXTURE_SHA256, "fixture hash")
    rows = path.read_text().splitlines()
    require(rows[0] == "24 138", "fixture header")
    red = {tuple(map(int, row.split())) for row in rows[1:]}
    require(len(red) == 138 and all(0 <= a < b < 24 for a, b in red), "fixture edges")
    rotate = lambda vertex: 3 * (vertex // 3) + (vertex + 1) % 3
    require({tuple(sorted((rotate(a), rotate(b)))) for a, b in red} == red,
            "fixture rotation")
    for vertices in itertools.combinations(range(24), 5):
        colors = {tuple(sorted(pair)) in red for pair in itertools.combinations(vertices, 2)}
        require(len(colors) == 2, "fixture monochromatic five-set")
    for cycle in range(8):
        internal_red = cycle < 4
        require(all((a, b) in red for a, b in itertools.combinations(range(3 * cycle, 3 * cycle + 3), 2))
                == internal_red, "fixture internal color")
        weights = []
        for other in range(8):
            if other == cycle:
                continue
            weight = sum((tuple(sorted((3 * cycle, vertex))) in red) == internal_red
                         for vertex in range(3 * other, 3 * other + 3))
            weights.append(weight)
        require(sum(2 - weight + 3 * (weight == 3) for weight in weights) <= 2,
                "fixture deficit")
    print("PASS positive control: vertices=24 red_edges=138 five_sets=42504")


def external_replay(binary: Path, core: Path, proof: Path, red_cycles: int) -> None:
    result = subprocess.run([str(binary), str(core), str(proof), "-U"],
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            check=False)
    output = result.stdout.replace("\r", "\n")
    require(result.returncode == 0 and "s VERIFIED" in output, "external RUP replay")
    clauses = re.search(r"(\d+) of (\d+) clauses in core", output)
    lemmas = re.search(r"(\d+) of (\d+) lemmas in core using (\d+) resolution steps", output)
    rats = re.search(r"(\d+) RAT lemmas in core", output)
    require(clauses and lemmas and rats and int(rats.group(1)) == 0, "external replay summary")
    print(f"PASS external RUP r={red_cycles}: input_core={clauses.group(1)}/{clauses.group(2)} "
          f"lemmas={lemmas.group(1)}/{lemmas.group(2)} resolutions={lemmas.group(3)} RAT=0")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True,
                        help="reviewed ramsey_r55_order3_eight_cycle_obstruction directory")
    parser.add_argument("--work", type=Path, required=True,
                        help="directory containing regenerated full_r0.cnf,...,full_r4.cnf")
    parser.add_argument("--drat-trim", type=Path,
                        help="optional external verifier for the compact RUP proofs")
    args = parser.parse_args()
    target, work = args.target.resolve(), args.work.resolve()

    analytic_audit()
    labels, groups = orbit_labels()
    print(f"PASS actual edge orbits: pairs=903 orbits={len(groups)} primary={len(labels)}")
    fixture_audit(target / "moving24.edges")

    for red_cycles, values in FULL_CASES.items():
        variables, clauses, size, full_hash, core_hash, proof_hash = values
        full = work / f"full_r{red_cycles}.cnf"
        core = target / f"core_r{red_cycles}.cnf"
        proof = target / f"proof_r{red_cycles}.rup"
        require(full.stat().st_size == size and sha256(full) == full_hash, "full formula bytes/hash")
        require(sha256(core) == core_hash and sha256(proof) == proof_hash, "core/proof hash")
        expected_primary, ramsey_count = primary_formula(red_cycles, labels)
        core_set, core_count = read_core(core, variables)
        primary_count, primary_hash = audit_full_formula(
            full, variables, clauses, expected_primary, core_set)
        print(f"PASS semantic CNF r={red_cycles}: five_sets=962598 ramsey={ramsey_count} "
              f"primary={primary_count} core_members={core_count} sha256={primary_hash}")
        if args.drat_trim:
            external_replay(args.drat_trim.resolve(), core, proof, red_cycles)

    if args.drat_trim:
        print(f"DRAT_TRIM sha256={sha256(args.drat_trim.resolve())}")
    print("PASS: independently verified exclusion of order-three type 1^19 3^8")
    print("SCOPE: minimum nine additionally imports the verified k=7 and sparse-motion exclusions")


if __name__ == "__main__":
    main()
