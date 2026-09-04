#!/usr/bin/env python3
"""Rebuild, solve, and verify the complete 65-leaf C7 proof tree."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

TOP_VARS = (7, 8, 9, 127)
FIRST_VARS = (10, 17, 24)
SECOND_VARS = (11, 18, 25)
THIRD_VARS = (12, 19)
TOP_REFINED = (3, 5)
SECOND_REFINED = ((3, 0), (3, 1), (3, 2), (3, 4), (5, 0), (5, 2), (5, 4))


def bits(index: int, width: int) -> tuple[int, ...]:
    return tuple((index >> shift) & 1 for shift in reversed(range(width)))


@dataclass(frozen=True)
class Leaf:
    name: str
    units: tuple[tuple[int, int], ...]


def leaves() -> list[Leaf]:
    answer: list[Leaf] = []
    for top in range(16):
        if top not in TOP_REFINED:
            answer.append(Leaf(f"l0-c{top:02d}", tuple(zip(TOP_VARS, bits(top, 4)))))
    for top in TOP_REFINED:
        prefix = tuple(zip(TOP_VARS, bits(top, 4)))
        for first in range(1, 8):
            answer.append(
                Leaf(f"l1-p{top:02d}-c{first:02d}", prefix + tuple(zip(FIRST_VARS, bits(first, 3))))
            )
    refined = set(SECOND_REFINED)
    for top in TOP_REFINED:
        prefix = tuple(zip(TOP_VARS, bits(top, 4))) + tuple(zip(FIRST_VARS, bits(0, 3)))
        for second in range(8):
            if (top, second) not in refined:
                answer.append(
                    Leaf(
                        f"l2-p{top:02d}-c{second:02d}",
                        prefix + tuple(zip(SECOND_VARS, bits(second, 3))),
                    )
                )
    for top, second in SECOND_REFINED:
        prefix = (
            tuple(zip(TOP_VARS, bits(top, 4)))
            + tuple(zip(FIRST_VARS, bits(0, 3)))
            + tuple(zip(SECOND_VARS, bits(second, 3)))
        )
        for third in range(4):
            answer.append(
                Leaf(
                    f"l3-p{top:02d}-m{second:02d}-c{third:02d}",
                    prefix + tuple(zip(THIRD_VARS, bits(third, 2))),
                )
            )
    assert len(answer) == 65
    return answer


def check_partition() -> None:
    variables = TOP_VARS + FIRST_VARS + SECOND_VARS + THIRD_VARS
    tree = leaves()
    for values in itertools.product((0, 1), repeat=len(variables)):
        assignment = dict(zip(variables, values))
        matching = [leaf.name for leaf in tree if all(assignment[var] == bit for var, bit in leaf.units)]
        assert len(matching) == 1, (values, matching)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def write_cube(root: Path, target: Path, leaf: Leaf) -> None:
    lines = root.read_text(encoding="ascii").splitlines()
    header = lines[0].split()
    assert header[:2] == ["p", "cnf"]
    header[3] = str(int(header[3]) + len(leaf.units))
    unit_lines = [f"{var if value else -var} 0" for var, value in leaf.units]
    target.write_text(
        "\n".join([" ".join(header), *lines[1:], *unit_lines, ""]), encoding="ascii"
    )


def process_leaf(
    leaf: Leaf,
    root: Path,
    work: Path,
    solver: Path | None,
    checker: Path | None,
    expected: dict[str, dict[str, object]],
) -> dict[str, object]:
    cnf, proof = work / f"{leaf.name}.cnf", work / f"{leaf.name}.drat"
    write_cube(root, cnf, leaf)
    record: dict[str, object] = {
        "name": leaf.name,
        "units": [[variable, value] for variable, value in leaf.units],
        "cnf_sha256": sha256(cnf),
    }
    if leaf.name in expected:
        record["expected_cnf_match"] = record["cnf_sha256"] == expected[leaf.name]["cnf_sha256"]
    if solver is not None:
        started = time.monotonic()
        result = subprocess.run(
            [solver, cnf, proof], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        record.update(
            solver_returncode=result.returncode,
            solver_seconds=round(time.monotonic() - started, 3),
        )
    if solver is not None or checker is not None:
        assert proof.exists(), f"missing proof for {leaf.name}"
        record["proof_bytes"] = proof.stat().st_size
        record["proof_sha256"] = sha256(proof)
        if leaf.name in expected:
            record["expected_proof_match"] = (
                record["proof_sha256"] == expected[leaf.name]["proof_sha256"]
                and record["proof_bytes"] == expected[leaf.name]["proof_bytes"]
            )
    if checker is not None:
        started = time.monotonic()
        result = subprocess.run(
            [checker, cnf, proof], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        record.update(
            checker_returncode=result.returncode,
            checker_seconds=round(time.monotonic() - started, 3),
            verified=result.returncode == 0 and "s VERIFIED" in result.stdout.replace("\r", "\n"),
        )
    print(json.dumps(record, sort_keys=True), flush=True)
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("work", type=Path)
    parser.add_argument("--solver", type=Path)
    parser.add_argument("--checker", type=Path)
    parser.add_argument("--evidence", type=Path, default=Path(__file__).with_name("result.json"))
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    check_partition()
    evidence = json.loads(args.evidence.read_text(encoding="ascii"))
    expected = {item["name"]: item for item in evidence["leaves"]}
    assert len(expected) == 65
    args.work.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        records = list(
            pool.map(
                lambda leaf: process_leaf(
                    leaf, args.root, args.work, args.solver, args.checker, expected
                ),
                leaves(),
            )
        )
    records.sort(key=lambda record: str(record["name"]))
    summary = {
        "partition_assignments_checked": 4096,
        "leaf_count": len(records),
        "all_cnf_hashes_match": all(record.get("expected_cnf_match") for record in records),
    }
    if args.solver is not None:
        summary["all_unsat"] = all(record.get("solver_returncode") == 20 for record in records)
        summary["all_proof_hashes_match"] = all(
            record.get("expected_proof_match") for record in records
        )
    if args.checker is not None:
        summary["all_proof_hashes_match"] = all(
            record.get("expected_proof_match") for record in records
        )
        summary["all_verified"] = all(record.get("verified") for record in records)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
