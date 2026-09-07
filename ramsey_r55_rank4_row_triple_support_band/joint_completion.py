#!/usr/bin/env python3
"""Joint physical completion search for the full-row-support rank-four stratum.

The A-side factor list contains every nonzero vector of F_2^4 and optionally
the zero vector.  Its remaining occurrences range over every multiplicity
pattern allowed by the row cap three.  For one GL(4,2) orbit representative,
the B-side labels are existential one-hot variables covering every sorted,
spanning 23-list satisfying the retained zero and nonzero multiplicity caps.
All 443 within-side edges are physical Boolean variables.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path
import shutil
import subprocess
import time


N = 43
A_SIZE = 20
B_SIZE = 23


def dot(x: int, y: int) -> int:
    return (x & y).bit_count() & 1


def linear_map(images: tuple[int, int, int, int], x: int) -> int:
    value = 0
    for i, image in enumerate(images):
        if (x >> i) & 1:
            value ^= image
    return value


def generators() -> tuple[tuple[int, int, int, int], ...]:
    result = []
    for i in range(3):
        basis = [1, 2, 4, 8]
        basis[i], basis[i + 1] = basis[i + 1], basis[i]
        result.append(tuple(basis))
    result.append((3, 2, 4, 8))
    return tuple(result)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(linear_map(left, linear_map(right, 1 << i)) for i in range(4))


def full_group() -> set[tuple[int, int, int, int]]:
    identity = (1, 2, 4, 8)
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators():
            nxt = compose(generator, current)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def group_size() -> int:
    return len(full_group())


def stabilizer(row_record: dict) -> list[tuple[int, int, int, int]]:
    populations = Counter(range(1, 16))
    populations.update(row_record["extras"])
    return [
        transformation
        for transformation in full_group()
        if Counter(
            linear_map(transformation, value)
            for value in populations.elements()
        ) == populations
    ]


def image_mask(mask: int, transformation: tuple[int, ...]) -> int:
    result = 0
    for value in range(1, 16):
        if mask & (1 << (value - 1)):
            result |= 1 << (linear_map(transformation, value) - 1)
    return result


def dual_map(transformation: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """Return the inverse-transpose action preserving the standard dot product."""
    images = [0] * 16
    for candidate in range(16):
        source = sum(dot(transformation[i], candidate) << i for i in range(4))
        images[source] = candidate
    result = tuple(images[1 << i] for i in range(4))
    if any(dot(linear_map(transformation, x), linear_map(result, y)) != dot(x, y)
           for x in range(16) for y in range(16)):
        raise RuntimeError("dual action failed dot-product check")
    return result


def row_orbits() -> tuple[list[dict], dict]:
    """Enumerate all capped full-nonzero-support A multisets modulo GL(4,2)."""
    records = []
    totals = {}
    for zero_rows in (0, 1):
        extra_count = 5 - zero_rows
        extras = [
            values
            for values in combinations_with_replacement(range(1, 16), extra_count)
            if max(Counter(values).values()) <= 2
        ]
        unseen = set(extras)
        orbit_records = []
        while unseen:
            seed = min(unseen)
            unseen.remove(seed)
            queue = deque([seed])
            orbit = []
            while queue:
                current = queue.popleft()
                orbit.append(current)
                for generator in generators():
                    image = tuple(sorted(linear_map(generator, x) for x in current))
                    if image in unseen:
                        unseen.remove(image)
                        queue.append(image)
            representative = min(orbit)
            profile = tuple(sorted(Counter(representative).values(), reverse=True))
            orbit_records.append({
                "zero_rows": zero_rows,
                "extras": list(representative),
                "extra_profile": list(profile),
                "orbit_size": len(orbit),
            })
        orbit_records.sort(key=lambda item: (item["extra_profile"], item["extras"]))
        totals[str(zero_rows)] = {
            "extra_multisets": len(extras),
            "orbits": len(orbit_records),
            "orbit_size_sum": sum(item["orbit_size"] for item in orbit_records),
        }
        records.extend(orbit_records)
    for index, item in enumerate(records):
        item["orbit_index"] = index
    census = {
        "gl4_size": group_size(),
        "row_orbits": len(records),
        "by_zero_rows": totals,
    }
    if census["gl4_size"] != 20160 or len(records) != 16:
        raise RuntimeError(f"unexpected row orbit census: {census}")
    return records, census


class StreamCNF:
    def __init__(self, body_path: Path):
        self.body_path = body_path
        self.handle = body_path.open("w", encoding="ascii")
        self.variables = 0
        self.clauses = 0

    def new_var(self) -> int:
        self.variables += 1
        return self.variables

    def add(self, literals) -> None:
        unique = []
        seen = set()
        for literal in literals:
            if -literal in seen:
                return
            if literal not in seen:
                seen.add(literal)
                unique.append(literal)
        self.handle.write(" ".join(map(str, unique)) + " 0\n")
        self.clauses += 1

    def at_most(self, literals: list[int], bound: int,
                gate: int | None = None) -> None:
        """Sinz sequential encoding of sum(literals) <= bound."""
        def emit(clause) -> None:
            self.add(([-gate] if gate is not None else []) + list(clause))

        n = len(literals)
        if bound >= n:
            return
        if bound < 0:
            emit([])
            return
        if bound == 0:
            for literal in literals:
                emit([-literal])
            return
        state = [[self.new_var() for _ in range(bound)] for _ in range(n - 1)]
        emit([-literals[0], state[0][0]])
        for j in range(1, bound):
            emit([-state[0][j]])
        for i in range(1, n - 1):
            emit([-literals[i], state[i][0]])
            emit([-state[i - 1][0], state[i][0]])
            for j in range(1, bound):
                emit([-literals[i], -state[i - 1][j - 1], state[i][j]])
                emit([-state[i - 1][j], state[i][j]])
        for i in range(1, n):
            emit([-literals[i], -state[i - 1][bound - 1]])

    def at_least(self, literals: list[int], bound: int,
                 gate: int | None = None) -> None:
        self.at_most([-literal for literal in literals], len(literals) - bound,
                     gate)

    def finish(self, cnf_path: Path) -> None:
        self.handle.close()
        with cnf_path.open("wb") as output:
            output.write(f"p cnf {self.variables} {self.clauses}\n".encode("ascii"))
            with self.body_path.open("rb") as body:
                shutil.copyfileobj(body, output, length=1024 * 1024)
        self.body_path.unlink()


def edge_rank(rows: list[int], width: int) -> int:
    basis = [0] * width
    rank = 0
    for value in rows:
        current = value
        while current:
            pivot = current.bit_length() - 1
            if basis[pivot]:
                current ^= basis[pivot]
            else:
                basis[pivot] = current
                rank += 1
                break
    return rank


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def build_formula(row_record: dict, cnf_path: Path,
                  nonzero_support_size: int | None = None,
                  nonzero_support_set: tuple[int, ...] | None = None,
                  nonzero_support_maximum: int | None = None,
                  support_symmetry_break: bool = False) -> dict:
    zero_rows = row_record["zero_rows"]
    row_labels = ([0] if zero_rows else []) + list(range(1, 16)) + row_record["extras"]
    if len(row_labels) != A_SIZE or edge_rank(row_labels, 4) != 4:
        raise RuntimeError("invalid row factor list")

    formula = StreamCNF(cnf_path.with_suffix(cnf_path.suffix + ".body"))
    internal = {}
    for side in (range(A_SIZE), range(A_SIZE, N)):
        for edge in combinations(side, 2):
            internal[edge] = formula.new_var()
    if len(internal) != 443:
        raise RuntimeError("internal-edge allocation error")

    label = [[formula.new_var() for _ in range(16)] for _ in range(B_SIZE)]
    contact = {
        (u, j): formula.new_var()
        for u in range(1, 16)
        for j in range(B_SIZE)
    }

    # Exactly one label per B vertex and canonical nondecreasing label order.
    for j in range(B_SIZE):
        formula.add(label[j])
        for x, y in combinations(label[j], 2):
            formula.add([-x, -y])
    for j in range(B_SIZE - 1):
        for larger in range(1, 16):
            for smaller in range(larger):
                formula.add([-label[j][larger], -label[j + 1][smaller]])

    # Zero is forbidden on B if it occurs on A, otherwise its cap is two.
    if zero_rows:
        for j in range(B_SIZE):
            formula.add([-label[j][0]])
    else:
        for j in range(B_SIZE - 2):
            formula.add([-label[j][0], -label[j + 2][0]])
    for value in range(1, 16):
        for j in range(B_SIZE - 5):
            formula.add([-label[j][value], -label[j + 5][value]])

    if sum(option is not None for option in (
            nonzero_support_size, nonzero_support_set,
            nonzero_support_maximum)) > 1:
        raise ValueError("choose an exact, fixed, or maximum support constraint")
    if nonzero_support_set is not None:
        support = tuple(sorted(set(nonzero_support_set)))
        if support != nonzero_support_set or not support or support[0] < 1 or support[-1] > 15:
            raise ValueError("fixed nonzero support must be a sorted subset of 1..15")
        if edge_rank(list(support), 4) != 4:
            raise ValueError("fixed nonzero support does not span F_2^4")
        support_lookup = set(support)
        for value in range(1, 16):
            if value in support_lookup:
                formula.add([label[j][value] for j in range(B_SIZE)])
            else:
                for j in range(B_SIZE):
                    formula.add([-label[j][value]])

    support_variables = [formula.new_var() for _ in range(15)]
    for value in range(1, 16):
        used = support_variables[value - 1]
        for j in range(B_SIZE):
            formula.add([-label[j][value], used])
        formula.add([-used] + [label[j][value] for j in range(B_SIZE)])

    if nonzero_support_size is not None:
        if not 4 <= nonzero_support_size <= 15:
            raise ValueError("nonzero support size must lie in [4,15]")
        formula.at_least(support_variables, nonzero_support_size)
        formula.at_most(support_variables, nonzero_support_size)
    if nonzero_support_maximum is not None:
        if not 4 <= nonzero_support_maximum <= 15:
            raise ValueError("nonzero support maximum must lie in [4,15]")
        formula.at_most(support_variables, nonzero_support_maximum)

    support_symmetry_clauses = 0
    canonical_valid_supports = None
    row_stabilizer_size = None
    if support_symmetry_break:
        row_stabilizer = stabilizer(row_record)
        column_stabilizer = [dual_map(transformation)
                             for transformation in row_stabilizer]
        row_stabilizer_size = len(row_stabilizer)
        canonical_valid_supports = 0
        for mask in range(1 << 15):
            canonical = min(image_mask(mask, transformation)
                            for transformation in column_stabilizer)
            if mask != canonical:
                formula.add([
                    -support_variables[i] if mask & (1 << i)
                    else support_variables[i]
                    for i in range(15)
                ])
                support_symmetry_clauses += 1
            elif mask.bit_count() >= 5 and edge_rank(
                    [value for value in range(1, 16)
                     if mask & (1 << (value - 1))], 4) == 4:
                canonical_valid_supports += 1

    # V spans F_2^4 exactly when no nonzero functional vanishes on all labels.
    for normal in range(1, 16):
        formula.add([
            label[j][value]
            for j in range(B_SIZE)
            for value in range(16)
            if dot(normal, value)
        ])

    # Contact bits are the physical dot products U_i . V_j.
    for u in range(1, 16):
        for j in range(B_SIZE):
            c = contact[u, j]
            for value in range(16):
                formula.add([-label[j][value], c if dot(u, value) else -c])

    # The h3771 contact condition for every tripled nonzero row class.
    populations = Counter(row_labels)
    tripled = sorted(value for value, count in populations.items() if value and count == 3)
    for value in tripled:
        contacts = [contact[value, j] for j in range(B_SIZE)]
        formula.at_least(contacts, 10)
        formula.at_most(contacts, 13)

    # Every equal-cross-row physical pair has at least eight A-side
    # distinguishers.  Encode all pairs, including all three in a tripled class.
    repeated_pairs = []
    for value in range(1, 16):
        vertices = [i for i, row in enumerate(row_labels) if row == value]
        repeated_pairs.extend(combinations(vertices, 2))
    distinguisher_vars = 0
    for first, second in repeated_pairs:
        differences = []
        for other in range(A_SIZE):
            if other in (first, second):
                continue
            a = internal[tuple(sorted((first, other)))]
            b = internal[tuple(sorted((second, other)))]
            d = formula.new_var()
            distinguisher_vars += 1
            differences.append(d)
            formula.add([a, b, -d])
            formula.add([a, -b, d])
            formula.add([-a, b, d])
            formula.add([-a, -b, -d])
        formula.at_least(differences, 8)

    # The same universal pair bound applies on B whenever two column labels
    # agree.  Equality is detected from the one-hot labels; all their A-side
    # contacts then coincide, so the required distinguishers lie in B.
    equal_column_pair_gates = 0
    column_distinguisher_variables = 0
    for first, second in combinations(range(B_SIZE), 2):
        equal = formula.new_var()
        equal_column_pair_gates += 1
        for value in range(16):
            formula.add([-label[first][value], -label[second][value], equal])
        differences = []
        for other in range(B_SIZE):
            if other in (first, second):
                continue
            a = internal[tuple(sorted((A_SIZE + first, A_SIZE + other)))]
            b = internal[tuple(sorted((A_SIZE + second, A_SIZE + other)))]
            d = formula.new_var()
            column_distinguisher_variables += 1
            differences.append(d)
            formula.add([a, b, -d])
            formula.add([a, -b, d])
            formula.add([-a, b, d])
            formula.add([-a, -b, -d])
        formula.at_least(differences, 8, equal)

    def edge_variable(first: int, second: int) -> int | None:
        if first > second:
            first, second = second, first
        if second < A_SIZE or first >= A_SIZE:
            return internal[first, second]
        row_label = row_labels[first]
        if row_label == 0:
            return None
        return contact[row_label, second - A_SIZE]

    # R(4,5)=25 forces every red degree into [18,24].  Repeated literals in a
    # B-vertex degree list represent distinct incident edges that share their
    # color because the corresponding A rows have equal factor labels.
    degree_aux_before = formula.variables
    for vertex in range(N):
        incident = []
        for other in range(N):
            if other == vertex:
                continue
            edge = edge_variable(vertex, other)
            if edge is not None:
                incident.append(edge)
        formula.at_least(incident, 18)
        formula.at_most(incident, 24)
    degree_auxiliary_variables = formula.variables - degree_aux_before

    ramsey_clauses = 0
    for vertices in combinations(range(N), 5):
        edges = [edge_variable(*edge) for edge in combinations(vertices, 2)]
        if None not in edges:
            formula.add([-edge for edge in edges])
            ramsey_clauses += 1
        formula.add([edge for edge in edges if edge is not None])
        ramsey_clauses += 1

    formula.finish(cnf_path)
    return {
        "row_labels": row_labels,
        "tripled_labels": tripled,
        "repeated_pairs": [list(pair) for pair in repeated_pairs],
        "distinguisher_variables": distinguisher_vars,
        "equal_column_pair_gates": equal_column_pair_gates,
        "column_distinguisher_variables": column_distinguisher_variables,
        "degree_auxiliary_variables": degree_auxiliary_variables,
        "nonzero_support_size": nonzero_support_size,
        "nonzero_support_set": list(nonzero_support_set) if nonzero_support_set else None,
        "nonzero_support_maximum": nonzero_support_maximum,
        "support_variables": support_variables,
        "support_symmetry_break": support_symmetry_break,
        "support_symmetry_clauses": support_symmetry_clauses,
        "canonical_valid_supports": canonical_valid_supports,
        "row_stabilizer_size": row_stabilizer_size,
        "variables": formula.variables,
        "clauses": formula.clauses,
        "ramsey_clauses": ramsey_clauses,
        "internal_variables": {f"{a},{b}": variable for (a, b), variable in internal.items()},
        "label_variables": label,
        "contact_variables": {f"{u},{j}": variable for (u, j), variable in contact.items()},
    }


def read_assignment(path: Path) -> dict[int, bool]:
    assignment = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line[0] in "cs":
            continue
        if line[0] == "v":
            line = line[1:]
        for token in line.split():
            literal = int(token)
            if literal:
                assignment[abs(literal)] = literal > 0
    return assignment


def extract_candidate(metadata: dict, assignment: dict[int, bool]) -> dict:
    row_labels = metadata["row_labels"]
    label_vars = metadata["label_variables"]
    column_labels = []
    for variables in label_vars:
        chosen = [value for value, variable in enumerate(variables) if assignment.get(variable)]
        if len(chosen) != 1:
            raise RuntimeError(f"invalid one-hot model: {chosen}")
        column_labels.append(chosen[0])
    if column_labels != sorted(column_labels):
        raise RuntimeError("column labels are not sorted")

    internal = {
        tuple(map(int, key.split(","))): variable
        for key, variable in metadata["internal_variables"].items()
    }
    contacts = {
        tuple(map(int, key.split(","))): variable
        for key, variable in metadata["contact_variables"].items()
    }
    red_edges = []
    for first, second in combinations(range(N), 2):
        if second < A_SIZE or first >= A_SIZE:
            red = assignment[internal[first, second]]
        else:
            row_label = row_labels[first]
            red = False if row_label == 0 else assignment[contacts[row_label, second - A_SIZE]]
            if red != bool(dot(row_label, column_labels[second - A_SIZE])):
                raise RuntimeError("contact model disagrees with factor labels")
        if red:
            red_edges.append([first, second])

    edge_set = {tuple(edge) for edge in red_edges}
    for vertices in combinations(range(N), 5):
        colors = [edge in edge_set for edge in combinations(vertices, 2)]
        if all(colors) or not any(colors):
            raise RuntimeError(f"solver model has monochromatic five-set {vertices}")

    red_rows = [sum(dot(u, v) << j for j, v in enumerate(column_labels)) for u in row_labels]
    blue_rows = [row ^ ((1 << B_SIZE) - 1) for row in red_rows]
    return {
        "column_labels": column_labels,
        "red_edges": red_edges,
        "red_edge_count": len(red_edges),
        "red_cut_rank": edge_rank(red_rows, B_SIZE),
        "blue_cut_rank": edge_rank(blue_rows, B_SIZE),
        "status": "SAT_VERIFIED_GOOD43",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--nonzero-support", type=int)
    parser.add_argument("--nonzero-support-maximum", type=int)
    parser.add_argument("--nonzero-support-set")
    parser.add_argument("--keep-cnf", action="store_true")
    args = parser.parse_args()
    orbits, census = row_orbits()
    if not 0 <= args.orbit < len(orbits):
        raise ValueError("orbit index out of range")

    generated_at = time.monotonic()
    fixed_support = None
    if args.nonzero_support_set:
        fixed_support = tuple(map(int, args.nonzero_support_set.split(",")))
    metadata = build_formula(
        orbits[args.orbit], args.cnf, args.nonzero_support, fixed_support,
        args.nonzero_support_maximum
    )
    generation_seconds = time.monotonic() - generated_at
    cnf_hash = file_sha256(args.cnf)
    witness = args.cnf.with_suffix(args.cnf.suffix + ".sol")
    solved_at = time.monotonic()
    run = subprocess.run(
        [str(args.solver), "-q", "--sat", "-t", str(args.seconds),
         "-w", str(witness), str(args.cnf)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
        timeout=args.seconds + 30,
    )
    solver_seconds = time.monotonic() - solved_at
    result = {
        "schema": "rank4-row-full-joint-completion-v1",
        "row_orbit_census": census,
        "row_orbit": orbits[args.orbit],
        "formula": {
            "variables": metadata["variables"],
            "clauses": metadata["clauses"],
            "ramsey_clauses": metadata["ramsey_clauses"],
            "bytes": args.cnf.stat().st_size,
            "sha256": cnf_hash,
            "generation_seconds": generation_seconds,
        },
        "solver": subprocess.run(
            [str(args.solver), "--version"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        "seconds_limit": args.seconds,
        "solver_seconds": solver_seconds,
        "solver_exit": run.returncode,
    }
    if run.returncode == 10:
        result["candidate"] = extract_candidate(metadata, read_assignment(witness))
        result["status"] = "SAT_VERIFIED_GOOD43"
    elif run.returncode == 20:
        result["status"] = "UNSAT_NO_PUBLIC_PROOF"
    else:
        result["status"] = "UNKNOWN"
        result["solver_output_tail"] = run.stdout[-2000:]
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    if not args.keep_cnf:
        args.cnf.unlink()
    if witness.exists():
        witness.unlink()


if __name__ == "__main__":
    main()
