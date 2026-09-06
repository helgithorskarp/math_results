#!/usr/bin/env python3
"""Clean-room review of the Core194 one-empty multiplicity exclusion.

This checker imports no module from the reviewed package.  It reconstructs
the physical order-three edge-orbit numbering, derives the six possible
one-empty signature multisets, generates the six complete CNF children from
the freshly rebuilt guarded base, and (optionally) produces and replays one
DRAT proof at a time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from itertools import combinations
from pathlib import Path


CORE_INDEX = 194
CORE_WORD = "100110110110110100"
LABELED_MULTIPLICITY = 81
BASE_IDENTITY = {
    "bytes": 24_968_396,
    "sha256": "f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf",
}
BASE_VARIABLES = 34_320
BASE_CLAUSES = 617_932
PAIRS = tuple(combinations(range(4), 2))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> dict[str, int | str]:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return {"bytes": path.stat().st_size, "sha256": h.hexdigest()}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def rotation(vertex: int) -> int:
    if vertex >= 33:
        return vertex
    return 3 * (vertex // 3) + (vertex % 3 + 1) % 3


def physical_primary_ids() -> dict[tuple[int, int], int]:
    """Recover all 320 primary variable IDs from the literal action."""
    unused = set(combinations(range(43), 2))
    moving: list[tuple[tuple[int, int], frozenset[tuple[int, int]]]] = []
    fixed: list[tuple[tuple[int, int], frozenset[tuple[int, int]]]] = []
    links: list[tuple[tuple[int, int], frozenset[tuple[int, int]]]] = []
    while unused:
        first = min(unused)
        orbit = {first}
        edge = tuple(sorted(map(rotation, first)))
        while edge != first:
            orbit.add(edge)
            edge = tuple(sorted(map(rotation, edge)))
        unused.difference_update(orbit)
        representative = min(orbit)
        a, b = representative
        item = (representative, frozenset(orbit))
        if b < 33:
            if a // 3 != b // 3:
                moving.append(item)
        elif a >= 33:
            fixed.append(item)
        else:
            links.append(item)
    moving.sort(key=lambda item: (
        item[0][0] // 3,
        item[0][1] // 3,
        (item[0][1] - item[0][0]) % 3,
    ))
    fixed.sort(key=lambda item: item[0])
    links.sort(key=lambda item: (item[0][1], item[0][0] // 3))
    ordered = moving + fixed + links
    require(len(ordered) == 320, "physical primary-orbit count")
    ids: dict[tuple[int, int], int] = {}
    for variable, (_, orbit) in enumerate(ordered, 1):
        for edge in orbit:
            require(edge not in ids, "edge orbit overlap")
            ids[edge] = variable
    require(len(ids) == len(tuple(combinations(range(43), 2))) - 11 * 3,
            "all non-internal physical pairs covered")
    return ids


def core_colors(ids: dict[tuple[int, int], int]) -> dict[int, bool]:
    variables = []
    for i, j in PAIRS:
        for shift in range(3):
            variables.append(ids[tuple(sorted((3 * i, 3 * j + shift)))])
    require(variables == list(range(1, 10)) + list(range(31, 37)) + list(range(58, 61)),
            "literal Core194 variable order")
    return {variable: bit == "1" for variable, bit in zip(variables, CORE_WORD)}


def complementary_k4s(ids: dict[tuple[int, int], int]) -> list[dict[str, object]]:
    colors = core_colors(ids)

    def red(a: int, b: int) -> bool:
        if a // 3 == b // 3:
            return True
        return colors[ids[tuple(sorted((a, b)))]]

    witnesses = []
    for omitted in range(4):
        vertices = [v for v in range(12) if v // 3 != omitted]
        candidates = [
            list(group)
            for group in combinations(vertices, 4)
            if all(red(a, b) for a, b in combinations(group, 2))
        ]
        require(candidates, f"red K4 in complementary core {omitted}")
        witnesses.append({"omitted": omitted, "red_k4": min(candidates)})
    return witnesses


def weak_compositions(total: int, parts: int):
    """Stars-and-bars enumeration, deliberately different from the producer."""
    for bars in combinations(range(total + parts - 1), parts - 1):
        boundaries = (-1,) + bars + (total + parts - 1,)
        yield tuple(boundaries[i + 1] - boundaries[i] - 1 for i in range(parts))


def prefix_key(mask: int) -> tuple[int, ...]:
    return tuple((mask >> i) & 1 for i in range(4))


def derive_one_empty_cases() -> tuple[list[dict[str, object]], dict[str, object]]:
    survivors = []
    examined = 0
    for counts in weak_compositions(9, 10):
        examined += 1
        singletons = counts[:4]
        pairs = counts[4:]
        if any(value < 1 for value in singletons):
            continue
        if any(singletons[i] + pairs[k] > 2 or singletons[j] + pairs[k] > 2
               for k, (i, j) in enumerate(PAIRS)):
            continue
        masks = [0]
        for i, multiplicity in enumerate(singletons):
            masks.extend([1 << i] * multiplicity)
        for (i, j), multiplicity in zip(PAIRS, pairs):
            masks.extend([(1 << i) | (1 << j)] * multiplicity)
        require(len(masks) == 10, "ten fixed signatures")
        masks.sort(key=prefix_key)
        missing = [pair for pair, multiplicity in zip(PAIRS, pairs) if multiplicity == 0]
        require(singletons == (1, 1, 1, 1), "one-empty singleton rigidity")
        require(len(missing) == 1 and sorted(pairs) == [0, 1, 1, 1, 1, 1],
                "one-empty pair rigidity")
        survivors.append({
            "branch": "one",
            "id": f"one_{missing[0][0]}{missing[0][1]}",
            "index": CORE_INDEX,
            "masks": masks,
            "missing_pair": list(missing[0]),
        })
    survivors.sort(key=lambda case: case["id"])
    require(examined == 48_620, "complete stars-and-bars domain")
    require(len(survivors) == 6, "exactly six one-empty patterns")
    return survivors, {"weak_compositions": examined, "survivors": len(survivors)}


def expected_cases() -> tuple[list[dict[str, object]], dict[str, object]]:
    one, summary = derive_one_empty_cases()
    cases = [{"branch": "multiple", "id": "multiple", "index": CORE_INDEX}] + one
    cases.sort(key=lambda case: case["id"])
    return cases, summary


def case_units(case: dict[str, object], ids: dict[tuple[int, int], int]) -> list[int]:
    if case["branch"] == "multiple":
        return [-ids[(3 * i, 34)] for i in range(4)]
    units = []
    masks = case["masks"]
    require(isinstance(masks, list) and len(masks) == 10 and masks[0] == 0,
            "one-empty mask list")
    for fixed, mask in zip(range(34, 43), masks[1:]):
        for i in range(4):
            variable = ids[(3 * i, fixed)]
            units.append(variable if int(mask) & (1 << i) else -variable)
    require(len(units) == 36, "36 later-prefix units")
    return units


def inspect_base(path: Path, ids: dict[tuple[int, int], int]) -> dict[str, object]:
    require(digest(path) == BASE_IDENTITY, "fresh guarded-base identity")
    wanted = {-ids[(3 * i, 33)] for i in range(4)}
    found: set[int] = set()
    with path.open("rb") as stream:
        require(stream.readline() == b"p cnf 34320 617932\n", "guarded-base header")
        clauses = 0
        for raw in stream:
            clauses += 1
            require(raw.endswith(b" 0\n"), f"DIMACS terminator at clause {clauses}")
            literals = [int(token) for token in raw.split()[:-1]]
            require(literals and all(1 <= abs(literal) <= BASE_VARIABLES for literal in literals),
                    f"DIMACS literals at clause {clauses}")
            if len(literals) == 1 and literals[0] in wanted:
                found.add(literals[0])
        require(clauses == BASE_CLAUSES, "guarded-base clause count")
    require(found == wanted, "base forces the first empty four-bit prefix")
    return {
        "identity": BASE_IDENTITY,
        "variables": BASE_VARIABLES,
        "clauses": BASE_CLAUSES,
        "first_empty_prefix_units": sorted(found),
    }


def make_child(base: Path, output: Path, units: list[int]) -> dict[str, int | str]:
    with base.open("rb") as source, output.open("wb") as target:
        require(source.readline() == b"p cnf 34320 617932\n", "base header during child generation")
        target.write(f"p cnf {BASE_VARIABLES} {BASE_CLAUSES + len(units)}\n".encode())
        shutil.copyfileobj(source, target)
        for literal in units:
            target.write(f"{literal} 0\n".encode())
    return digest(output)


def inspect_child(base: Path, child: Path, units: list[int]) -> dict[str, object]:
    with base.open("rb") as source, child.open("rb") as target:
        require(source.readline() == b"p cnf 34320 617932\n", "base header")
        require(target.readline() == f"p cnf {BASE_VARIABLES} {BASE_CLAUSES + len(units)}\n".encode(),
                "child header")
        line = 0
        for raw in source:
            line += 1
            require(target.readline() == raw, f"base retained at clause {line}")
        for literal in units:
            require(target.readline() == f"{literal} 0\n".encode(), "exact child unit")
        require(target.read() == b"", "exact child EOF")
    return {
        "entire_guarded_base_retained": True,
        "variables": BASE_VARIABLES,
        "clauses": BASE_CLAUSES + len(units),
        "added_units": len(units),
    }


def replay(drat: Path, cnf: Path, proof: Path, log: Path, seconds: int) -> dict[str, object]:
    before = time.monotonic()
    with log.open("w", encoding="utf-8") as stream:
        checked = subprocess.run(
            [str(drat), str(cnf), str(proof), "-t", str(seconds)],
            stdout=stream,
            stderr=subprocess.STDOUT,
            timeout=seconds + 60,
            check=False,
        )
    text = log.read_text(encoding="utf-8")
    require(checked.returncode == 0 and "s VERIFIED" in text, f"DRAT replay failed for {cnf.name}")
    rat = re.search(r"(\d+) RAT lemmas in core", text)
    require(rat is not None, "missing RAT-core statistic")
    return {
        "verified": True,
        "exit_code": checked.returncode,
        "rat_core_lemmas": int(rat.group(1)),
        "seconds": round(time.monotonic() - before, 6),
        "log": digest(log),
    }


def solve_one(kissat: Path, drat: Path, cnf: Path, work: Path,
              solve_seconds: int, replay_seconds: int) -> dict[str, object]:
    proof = work / (cnf.stem + ".review1.drat")
    solve_log = work / (cnf.stem + ".review1.solve.log")
    before = time.monotonic()
    with solve_log.open("w", encoding="utf-8") as stream:
        solved = subprocess.run(
            [str(kissat), f"--time={solve_seconds}", str(cnf), str(proof)],
            stdout=stream,
            stderr=subprocess.STDOUT,
            timeout=solve_seconds + 60,
            check=False,
        )
    solve_elapsed = round(time.monotonic() - before, 6)
    text = solve_log.read_text(encoding="utf-8")
    require(solved.returncode == 20 and "s UNSATISFIABLE" in text,
            f"fresh solver did not refute {cnf.name}")
    checked = replay(drat, cnf, proof, work / (cnf.stem + ".review1.replay.log"), replay_seconds)
    return {
        "status": "excluded",
        "solver_exit_code": solved.returncode,
        "solve_seconds": solve_elapsed,
        "solve_log": digest(solve_log),
        "proof": digest(proof),
        "replay": checked,
    }


def negative_controls(cases: list[dict[str, object]], ids: dict[tuple[int, int], int]) -> list[str]:
    rejected = []

    def reject(name: str, function) -> None:
        try:
            function()
        except (ValueError, KeyError, IndexError, TypeError):
            rejected.append(name)
        else:
            raise ValueError("accepted malformed control " + name)

    reject("lost_one_empty_case", lambda: require(len(cases[:-1]) == 7, "seven-case coverage"))
    bad = json.loads(json.dumps(cases[1]))
    bad["masks"][1] = 0
    reject("duplicate_empty_prefix", lambda: require(case_units(bad, ids) == case_units(cases[1], ids), "exact units"))
    bad = json.loads(json.dumps(cases[1]))
    bad["missing_pair"] = [0, 0]
    reject("bad_missing_pair", lambda: require(bad in cases, "derived cases"))
    bad_units = case_units(cases[0], ids)
    reject("positive_second_empty_literal", lambda: require(bad_units[0] > 0, "negative empty units"))
    reject("fixed_edge_in_tail", lambda: require(all(abs(v) > 210 for v in [166]), "moving-fixed units only"))
    require(len(rejected) == 5, "all negative controls")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--solve-seconds", type=int, default=20)
    parser.add_argument("--replay-seconds", type=int, default=300)
    parser.add_argument("--solve", action="store_true")
    args = parser.parse_args()
    require(args.solve_seconds > 0 and args.replay_seconds > 0, "positive limits")
    require(not args.work.resolve().is_relative_to(args.target.resolve().parent), "external work directory")
    args.work.mkdir(parents=True, exist_ok=True)

    target_cases = json.loads((args.target / "cases.json").read_text(encoding="utf-8"))
    certificate = json.loads((args.target / "certificate.json").read_text(encoding="utf-8"))
    published = json.loads((args.target / "result.json").read_text(encoding="utf-8"))
    boundary = json.loads((args.target / "boundary.json").read_text(encoding="utf-8"))

    ids = physical_primary_ids()
    witnesses = complementary_k4s(ids)
    cases, classification = expected_cases()
    require(target_cases == cases, "submitted cases equal independently derived cases")
    require(certificate == {
        "bits": CORE_WORD,
        "index": CORE_INDEX,
        "labeled": LABELED_MULTIPLICITY,
        "one_empty_patterns": [
            {"masks": case["masks"], "missing_pair": case["missing_pair"]}
            for case in cases if case["branch"] == "one"
        ],
        "red_k4_witnesses": witnesses,
    }, "submitted certificate equals independent derivation")
    require(boundary["one_empty_branch_excluded"] is True, "claimed one-empty exclusion")
    require(boundary["multiple_empty_branch_excluded"] is False, "multiple-empty remains open")
    require(boundary["new_whole_core_exclusions"] == [], "no whole-Core194 exclusion")
    require(boundary["remaining_full_classes"] == 17 and boundary["remaining_full_labeled"] == 9153,
            "unchanged whole-core boundary")

    base = inspect_base(args.base, ids)
    published_by_id = {row["id"]: row for row in published["cases"]}
    generated = []
    for case in cases:
        units = case_units(case, ids)
        child = args.work / (case["id"] + ".review1.cnf")
        identity = make_child(args.base, child, units)
        audit = inspect_child(args.base, child, units)
        require(identity == published_by_id[case["id"]]["formula"],
                f"formula identity for {case['id']}")
        generated.append({
            "id": case["id"],
            "branch": case["branch"],
            "formula": identity,
            "audit": audit,
            "units_sha256": hashlib.sha256((" ".join(map(str, units)) + "\n").encode()).hexdigest(),
        })

    proof_rows = []
    if args.solve:
        require(args.kissat is not None and args.drat_trim is not None, "solver and checker required")
        require(args.kissat.is_file() and args.drat_trim.is_file(), "solver/checker files")
        for case in cases:
            if case["branch"] != "one":
                continue
            row = solve_one(
                args.kissat,
                args.drat_trim,
                args.work / (case["id"] + ".review1.cnf"),
                args.work,
                args.solve_seconds,
                args.replay_seconds,
            )
            row["id"] = case["id"]
            row["matches_published_proof"] = row["proof"] == published_by_id[case["id"]]["proof"]
            proof_rows.append(row)

    result = {
        "all_checks_passed": (not args.solve) or len(proof_rows) == 6,
        "scope": "Core194 one-empty branch only; implies at least two empty fixed signatures, not whole-core exclusion",
        "python": sys.version.split()[0],
        "reviewed_source": {
            name: digest(args.target / name)
            for name in ("PROOF.md", "boundary.json", "cases.json", "certificate.json", "result.json")
        },
        "physical_primary_orbits": 320,
        "core": {
            "index": CORE_INDEX,
            "bits": CORE_WORD,
            "labeled_multiplicity": LABELED_MULTIPLICITY,
            "complementary_red_k4s": witnesses,
        },
        "classification": {
            **classification,
            "one_empty_cases": [case["id"] for case in cases if case["branch"] == "one"],
            "case_cover": "six one-empty patterns plus one multiple-empty complement",
        },
        "base": base,
        "children": generated,
        "negative_controls_rejected": negative_controls(cases, ids),
        "tools": {
            "kissat": digest(args.kissat) if args.kissat else None,
            "drat_trim": digest(args.drat_trim) if args.drat_trim else None,
        },
        "proofs": proof_rows,
        "conclusion": {
            "one_empty_branch_excluded": len(proof_rows) == 6,
            "multiple_empty_branch_tested": False,
            "new_whole_core_exclusions": [],
            "remaining_full_classes": 17,
            "remaining_full_labeled": 9153,
            "target_graph": False,
        },
        "trust_boundary": [
            "accepted forced-empty, intrinsic-anchor, and sharp-pair inequalities",
            "accepted Core194 maximal-attachment result underlying the guarded clauses",
            "semantic correctness of the freshly reconstructed inherited guarded base beyond its checked boundary",
            "ordinary CPython, compiler, hardware, SHA-256, Kissat proof emission, and drat-trim",
        ],
    }
    atomic_json(args.report, result)
    require(result["all_checks_passed"], "proof production/replay not requested or incomplete")
    print(json.dumps({
        "all_checks_passed": True,
        "one_empty_cases": len(proof_rows),
        "proof_replays": sum(row["replay"]["verified"] for row in proof_rows),
        "whole_core_excluded": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
