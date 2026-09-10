#!/usr/bin/env python3
"""Add an exhaustive exact-36 prime-order orbit split to an invariant CNF.

The input format is the DIMACS format emitted by fixed_link_invariant.py.  Its
primary variable i selects cyclic candidate-block orbit i, and each orbit
comment records size 1 or the prime order p of the automorphism.  In branch f,
exactly f fixed orbits and (36-f)/p moving orbits are selected.  The branches
are disjoint and cover exactly the assignments selecting 36 blocks.
"""

from __future__ import annotations

import argparse
import hashlib
import re
from itertools import product
from pathlib import Path

from pysat.card import CardEnc, EncType


ORBIT_RE = re.compile(r"^c orbit ([1-9][0-9]*) size=([1-9][0-9]*)\b")


def read_case(path: Path) -> tuple[list[str], list[tuple[int, ...]], int, list[int]]:
    comments: list[str] = []
    clauses: list[tuple[int, ...]] = []
    declared_variables: int | None = None
    declared_clauses: int | None = None
    orbit_sizes: dict[int, int] = {}
    for line_number, raw in enumerate(path.read_text(encoding="ascii").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("c "):
            if declared_variables is not None:
                raise ValueError(f"comment after header at line {line_number}")
            comments.append(line)
            match = ORBIT_RE.match(line)
            if match:
                variable, size = map(int, match.groups())
                if variable in orbit_sizes:
                    raise ValueError(f"duplicate orbit variable {variable}")
                orbit_sizes[variable] = size
            continue
        if line.startswith("p "):
            if declared_variables is not None:
                raise ValueError("multiple DIMACS headers")
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError(f"bad DIMACS header: {line}")
            declared_variables, declared_clauses = map(int, fields[2:])
            continue
        if declared_variables is None:
            raise ValueError(f"clause before header at line {line_number}")
        literals = tuple(map(int, line.split()))
        if not literals or literals[-1] != 0 or 0 in literals[:-1]:
            raise ValueError(f"bad clause at line {line_number}")
        clause = literals[:-1]
        if any(abs(literal) > declared_variables for literal in clause):
            raise ValueError(f"out-of-range literal at line {line_number}")
        clauses.append(clause)
    if declared_variables is None or declared_clauses is None:
        raise ValueError("missing DIMACS header")
    if len(clauses) != declared_clauses:
        raise ValueError((len(clauses), declared_clauses))
    expected_orbits = list(range(1, len(orbit_sizes) + 1))
    if sorted(orbit_sizes) != expected_orbits:
        raise ValueError("orbit variables are not the initial contiguous variables")
    return comments, clauses, declared_variables, [orbit_sizes[i] for i in expected_orbits]


def equality_clauses(
    literals: list[int], bound: int, top_id: int
) -> tuple[int, list[tuple[int, ...]]]:
    if not 0 <= bound <= len(literals):
        raise ValueError((len(literals), bound))
    if bound == 0:
        return top_id, [(-literal,) for literal in literals]
    if bound == len(literals):
        return top_id, [(literal,) for literal in literals]
    encoding = CardEnc.equals(
        lits=literals,
        bound=bound,
        top_id=top_id,
        encoding=EncType.seqcounter,
    )
    return max(top_id, encoding.nv), list(map(tuple, encoding.clauses))


def branch_counts(orbit_sizes: list[int], block_count: int) -> list[tuple[int, int]]:
    nontrivial_sizes = set(orbit_sizes) - {1}
    if len(nontrivial_sizes) != 1:
        raise ValueError(f"expected one nontrivial orbit size, got {nontrivial_sizes}")
    prime = nontrivial_sizes.pop()
    if prime not in {2, 3}:
        raise ValueError(f"expected prime order 2 or 3, got {prime}")
    fixed_count = orbit_sizes.count(1)
    moving_count = orbit_sizes.count(prime)
    return [
        (selected_fixed, (block_count - selected_fixed) // prime)
        for selected_fixed in range(min(fixed_count, block_count) + 1)
        if (block_count - selected_fixed) % prime == 0
        and 0 <= (block_count - selected_fixed) // prime <= moving_count
    ]


def generate(input_path: Path, output_dir: Path, block_count: int) -> None:
    comments, base_clauses, base_variables, orbit_sizes = read_case(input_path)
    nontrivial_sizes = set(orbit_sizes) - {1}
    prime = next(iter(nontrivial_sizes)) if len(nontrivial_sizes) == 1 else None
    if prime not in {2, 3}:
        raise ValueError(f"not a prime-order case: orbit sizes {sorted(set(orbit_sizes))}")
    fixed_variables = [i for i, size in enumerate(orbit_sizes, 1) if size == 1]
    moving_variables = [i for i, size in enumerate(orbit_sizes, 1) if size == prime]
    counts = branch_counts(orbit_sizes, block_count)
    if not counts:
        raise ValueError("exact block count has no feasible orbit-count branch")
    input_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
    output_dir.mkdir(parents=True, exist_ok=True)
    for selected_fixed, selected_moving in counts:
        last_variable = base_variables
        last_variable, fixed_clauses = equality_clauses(
            fixed_variables, selected_fixed, last_variable
        )
        last_variable, moving_clauses = equality_clauses(
            moving_variables, selected_moving, last_variable
        )
        clauses = base_clauses + fixed_clauses + moving_clauses
        output_path = output_dir / (
            f"{input_path.stem}-exact-{block_count}-fixed-{selected_fixed}.cnf"
        )
        with output_path.open("w", encoding="ascii", newline="\n") as handle:
            for comment in comments:
                handle.write(comment + "\n")
            handle.write(f"c source CNF SHA-256: {input_hash}\n")
            handle.write(
                f"c exact block count {block_count}: selected fixed orbits="
                f"{selected_fixed}, selected size-{prime} orbits={selected_moving}\n"
            )
            handle.write("c exact cardinalities encoded by PySAT sequential counters\n")
            handle.write(f"p cnf {last_variable} {len(clauses)}\n")
            for clause in clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")
        print(
            f"{output_path.name}: variables={last_variable} clauses={len(clauses)} "
            f"fixed={selected_fixed}/{len(fixed_variables)} "
            f"moving={selected_moving}/{len(moving_variables)}"
        )


def self_test() -> None:
    for orbit_sizes, block_count in (([1, 1, 3, 3], 4), ([1, 1, 2, 2], 3)):
        branches = branch_counts(orbit_sizes, block_count)
        for values in product((False, True), repeat=len(orbit_sizes)):
            weight = sum(size for size, value in zip(orbit_sizes, values) if value)
            matching = sum(
                sum(values[i] for i, size in enumerate(orbit_sizes) if size == 1)
                == selected_fixed
                and sum(values[i] for i, size in enumerate(orbit_sizes) if size != 1)
                == selected_moving
                for selected_fixed, selected_moving in branches
            )
            if matching != int(weight == block_count):
                raise AssertionError((orbit_sizes, block_count, values, branches, matching))
    print("self-test passed: prime-order branches are disjoint and exact-block complete")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("output_dir", nargs="?", type=Path)
    parser.add_argument("--block-count", type=int, default=36)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        if args.input is None or args.output_dir is None:
            parser.error("input and output_dir are required without --self-test")
        generate(args.input, args.output_dir, args.block_count)


if __name__ == "__main__":
    main()
