#!/usr/bin/env python3
"""Independent census, normalization audit, construction, and DRAT replay."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_order3_eleven_core194_a5_fixed"
DIRECT = ROOT / "ramsey_r55_order3_eleven_core194_direct"
BASE_IDENTITY = {
    "bytes": 14_883_777,
    "sha256": "f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c",
}
TYPES = ((5, 0, 2), (5, 1, 1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def variable(a: int, b: int) -> int:
    """Reconstruct the accepted direct formula's physical primary numbering."""
    require(0 <= a < b < 43, "physical pair")
    if b < 33:
        i, phase_a = divmod(a, 3)
        j, phase_b = divmod(b, 3)
        if i == j:
            return 321 if i < 4 else -321
        rank = i * (21 - i) // 2 + j - i - 1
        return 1 + 3 * rank + (phase_b - phase_a) % 3
    if a >= 33:
        i, j = a - 33, b - 33
        return 166 + i * (19 - i) // 2 + j - i - 1
    return 211 + 11 * (b - 33) + a // 3


def contact_units(moving: tuple[int, int, int], fixed: tuple[int, int, int]) -> list[int]:
    units: list[int] = []
    moving_contacts = [kind for kind, count in enumerate(moving) for _ in range(count)]
    require(len(moving_contacts) == 7, "seven moving triangles")
    for cycle, contact in enumerate(moving_contacts, start=4):
        u_var = 211 + cycle
        v_var = 222 + cycle
        units.extend((u_var if contact != 2 else -u_var,
                      v_var if contact != 1 else -v_var))

    fixed_contacts = [kind for kind, count in enumerate(fixed) for _ in range(count)]
    require(len(fixed_contacts) == 8, "eight other fixed vertices")
    for offset, contact in enumerate(fixed_contacts):
        u_var = 167 + offset
        v_var = 175 + offset
        units.extend((u_var if contact != 2 else -u_var,
                      v_var if contact != 1 else -v_var))
    require(len(units) == 30 and len({abs(unit) for unit in units}) == 30,
            "thirty distinct physical contact units")
    return units


def case_id(counts: tuple[int, ...]) -> str:
    return "a%d_b%d_c%d_x%d_y%d_z%d" % counts


def read_census(path: Path) -> dict:
    types: list[dict] = []
    rows: list[dict] = []
    grand: dict[str, int] | None = None
    for line in path.read_text().splitlines():
        fields = line.split()
        require(fields, "blank census line")
        if fields[0] == "type":
            require(len(fields) == 16, "malformed type summary")
            require(fields[4::2] == ["total", "allowed", "profiles", "swaps", "permutations", "labeled"],
                    "type summary labels")
            types.append({
                "moving_counts": list(map(int, fields[1:4])),
                "fixed_words": int(fields[5]),
                "allowed_fixed_words": int(fields[7]),
                "normalized_profiles": int(fields[9]),
                "coupled_swaps": int(fields[11]),
                "distinct_normalizing_permutations": int(fields[13]),
                "labeled_full_star_weight": int(fields[15]),
            })
        elif fields[0] == "row":
            require(len(fields) == 11, "malformed census row")
            values = tuple(map(int, fields[1:]))
            counts = values[:6]
            rows.append({
                "counts": list(counts),
                "fixed_words": values[6],
                "red_degrees": list(values[7:9]),
                "labeled_assignments": values[9],
                "id": case_id(counts),
            })
        elif fields[0] == "grand":
            require(len(fields) == 5 and fields[1] == "profiles" and fields[3] == "labeled",
                    "malformed grand summary")
            grand = {"normalized_profiles": int(fields[2]), "labeled_full_star_weight": int(fields[4])}
        else:
            raise RuntimeError("unknown census record")

    expected_types = [
        {"moving_counts": [5, 0, 2], "fixed_words": 6561, "allowed_fixed_words": 577,
         "normalized_profiles": 10, "coupled_swaps": 0,
         "distinct_normalizing_permutations": 486, "labeled_full_star_weight": 24234},
        {"moving_counts": [5, 1, 1], "fixed_words": 6561, "allowed_fixed_words": 4074,
         "normalized_profiles": 9, "coupled_swaps": 1512,
         "distinct_normalizing_permutations": 3415, "labeled_full_star_weight": 171108},
    ]
    require(types == expected_types, "complete independent type censuses")
    require(grand == {"normalized_profiles": 19, "labeled_full_star_weight": 195342},
            "complete independent grand census")
    require(len(rows) == 19 and sum(row["labeled_assignments"] for row in rows) == 195342,
            "nineteen canonical rows and full labeled weight")
    return {"types": types, "rows": rows, **grand,
            "method": "direct C++ enumeration of both sets of all 3^8 fixed-contact words"}


def vertex_mapping(kind: str) -> list[int]:
    mapping = list(range(43))
    if kind == "coupled":
        mapping[33], mapping[34] = 34, 33
        for phase in range(3):
            mapping[27 + phase], mapping[30 + phase] = 30 + phase, 27 + phase
    elif kind == "endpoint_only":
        mapping[33], mapping[34] = 34, 33
    elif kind.startswith("fixed_"):
        left = int(kind.split("_")[1])
        mapping[left], mapping[left + 1] = left + 1, left
    else:
        raise RuntimeError("unknown vertex mapping")
    return mapping


def primary_mapping(vertices: list[int]) -> dict[int, int]:
    require(sorted(vertices) == list(range(43)), "vertex bijection")
    mapping: dict[int, int] = {}
    for a, b in itertools.combinations(range(43), 2):
        source = variable(a, b)
        c, d = sorted((vertices[a], vertices[b]))
        image = variable(c, d)
        if abs(source) == 321:
            require(image == source, "constant physical color preserved")
            continue
        require(1 <= source <= 320 and 1 <= image <= 320, "primary maps to primary")
        require(source not in mapping or mapping[source] == image, "orbit map is well defined")
        mapping[source] = image
    require(sorted(mapping) == list(range(1, 321)), "all source primaries mapped")
    require(sorted(mapping.values()) == list(range(1, 321)), "primary bijection")
    return mapping


def transport_literals(literals, mapping: dict[int, int]) -> tuple[int, ...]:
    return tuple(sorted(mapping[abs(literal)] if literal > 0 else -mapping[abs(literal)]
                        for literal in literals))


def complete_symmetry_audit(base: Path) -> dict:
    with base.open() as stream:
        require(stream.readline() == "p cnf 320 366069\n", "complete BLUE base header")
        clauses = {tuple(sorted(map(int, line.split()[:-1]))) for line in stream}
    require(len(clauses) == 366069, "all complete base clauses are distinct")

    names = ["coupled", "endpoint_only"] + [f"fixed_{vertex}" for vertex in range(35, 42)]
    moving_511 = set(contact_units((5, 1, 1), (8, 0, 0))[:14])
    results = []
    for name in names:
        mapping = primary_mapping(vertex_mapping(name))
        for clause in clauses:
            require(transport_literals(clause, mapping) in clauses, f"base symmetry {name}")
        moved = set(transport_literals(moving_511, mapping))
        if name == "endpoint_only":
            require(moved != moving_511, "endpoint-only swap must not preserve normalized moving child")
        else:
            require(moved == moving_511, f"moving child preservation {name}")
        results.append({"name": name, "clause_images": len(clauses),
                        "normalized_511_moving_child_preserved": moved == moving_511})
    return {
        "complete_base_clauses": len(clauses),
        "generators": results,
        "clause_images_checked": len(clauses) * len(names),
        "endpoint_only_child_normalization_rejected": True,
    }


def construct_child(base: Path, child: Path, counts: tuple[int, ...]) -> list[int]:
    with base.open("rb") as source, child.open("wb") as destination:
        require(source.readline() == b"p cnf 320 366069\n", "accepted BLUE base header")
        destination.write(b"p cnf 320 366099\n")
        while block := source.read(1 << 20):
            destination.write(block)
        units = contact_units(counts[:3], counts[3:])
        for unit in units:
            destination.write(f"{unit} 0\n".encode())
    return units


def inspect_child(base: Path, child: Path, expected_units: list[int]) -> None:
    with base.open("rb") as source, child.open("rb") as candidate:
        require(source.readline() == b"p cnf 320 366069\n", "base header")
        require(candidate.readline() == b"p cnf 320 366099\n", "child header")
        while block := source.read(1 << 20):
            require(candidate.read(len(block)) == block, "entire accepted base body retained")
        tail = []
        for line in candidate:
            fields = line.split()
            require(len(fields) == 2 and fields[1] == b"0", "unit-clause tail")
            tail.append(int(fields[0]))
    require(tail == expected_units, "exact physical 30-unit tail and EOF")


def exact_status(path: Path, expected: str) -> None:
    statuses = [line for line in path.read_text().splitlines() if line.startswith("s ")]
    require(statuses == [expected], "unexpected solver status transcript")


def main() -> None:
    if not __debug__:
        raise RuntimeError("run without -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--solve-seconds", type=int, default=90)
    parser.add_argument("--replay-seconds", type=int, default=600)
    args = parser.parse_args()
    require(not args.work.exists(), "work directory must be fresh")
    require(args.solve_seconds > 0 and args.replay_seconds > 0, "positive limits")
    args.work.mkdir(parents=True)

    census = read_census(args.census)
    public_profiles = json.loads((TARGET / "profiles.json").read_text())
    public_result = json.loads((TARGET / "result.json").read_text())
    require(public_result["complete"] and not public_result["open"], "public complete claim")
    require(not public_result["target_graph"] and not public_result["whole_core_exclusions"],
            "public scope is a conditional branch exclusion")
    public_cases = {row["id"]: row for row in public_result["cases"]}
    expected_ids = [row["id"] for row in census["rows"]]
    require(public_result["excluded"] == expected_ids and sorted(public_cases) == sorted(expected_ids),
            "public nineteen-case cover")

    for public, independent in zip(public_profiles, census["rows"]):
        counts = tuple(independent["counts"])
        require(public["counts"] == independent["counts"], "public canonical counts")
        require(public["red_degrees"] == independent["red_degrees"], "public endpoint degrees")
        require(public["labeled_assignments"] == independent["labeled_assignments"],
                "public labeled profile weight")
        require(public["units"] == contact_units(counts[:3], counts[3:]),
                "public physical unit meanings")

    base = args.work / "blue.cnf"
    generated = subprocess.run(
        [sys.executable, "-B", str(DIRECT / "generate.py"), "--color", "blue", "--output", str(base)],
        text=True, capture_output=True, check=True,
    )
    base_report = json.loads(generated.stdout)
    require(identity(base) == BASE_IDENTITY == base_report["formula"], "accepted direct base regenerated exactly")
    symmetries = complete_symmetry_audit(base)

    version = subprocess.run([str(args.kissat), "--version"], text=True,
                             capture_output=True, check=True).stdout.strip()
    require(version == "4.0.4", "unexpected Kissat version")
    start = time.monotonic()
    cases = []
    for independent in census["rows"]:
        counts = tuple(independent["counts"])
        identifier = independent["id"]
        public = public_cases[identifier]
        cnf = args.work / f"{identifier}.cnf"
        units = construct_child(base, cnf, counts)
        inspect_child(base, cnf, units)
        formula = identity(cnf)
        require(formula == public["formula"], "fresh formula differs from public formula")

        trace = args.work / f"{identifier}.drat"
        solve_log = args.work / f"{identifier}.solve.log"
        solve_start = time.monotonic()
        with solve_log.open("w") as output:
            solved = subprocess.run(
                [str(args.kissat), f"--time={args.solve_seconds}", str(cnf), str(trace)],
                stdout=output, stderr=subprocess.STDOUT, timeout=args.solve_seconds + 60,
            )
        exact_status(solve_log, "s UNSATISFIABLE")
        require(solved.returncode == 20, "Kissat did not return UNSAT")

        replay_log = args.work / f"{identifier}.replay.log"
        replay_start = time.monotonic()
        with replay_log.open("w") as output:
            checked = subprocess.run(
                [str(args.drat_trim), str(cnf), str(trace), "-t", str(args.replay_seconds)],
                stdout=output, stderr=subprocess.STDOUT, timeout=args.replay_seconds + 60,
            )
        replay_text = replay_log.read_text()
        require(checked.returncode == 0 and "s VERIFIED" in replay_text, "full DRAT replay failed")
        rat = re.search(r"(\d+) RAT lemmas in core", replay_text)
        require(rat is not None, "missing full DRAT RAT statistics")
        proof = identity(trace)
        cases.append({
            "id": identifier,
            "counts": list(counts),
            "formula": formula,
            "proof": proof,
            "published_proof_match": proof == public["trace"],
            "rat_core_lemmas": int(rat.group(1)),
            "solve_seconds": round(replay_start - solve_start, 6),
            "replay_seconds": round(time.monotonic() - replay_start, 6),
        })
        print(f"VERIFIED {identifier}", flush=True)

    # Exercise both compact checkers against deliberately false inputs.
    first_child = args.work / f"{expected_ids[0]}.cnf"
    wrong_units = contact_units(tuple(census["rows"][0]["counts"][:3]),
                                tuple(census["rows"][0]["counts"][3:]))
    wrong_units[-1] *= -1
    inspector_rejected_wrong_unit = False
    try:
        inspect_child(base, first_child, wrong_units)
    except RuntimeError:
        inspector_rejected_wrong_unit = True
    require(inspector_rejected_wrong_unit, "formula inspector accepted wrong physical unit")

    sat = args.work / "sat.cnf"
    false_trace = args.work / "false.drat"
    sat.write_text("p cnf 1 1\n1 0\n")
    false_trace.write_text("0\n")
    false_log = args.work / "false.replay.log"
    with false_log.open("w") as output:
        false_check = subprocess.run(
            [str(args.drat_trim), str(sat), str(false_trace), "-t", "10"],
            stdout=output, stderr=subprocess.STDOUT, timeout=20,
        )
    require(false_check.returncode != 0 and "s VERIFIED" not in false_log.read_text(),
            "DRAT checker accepted false refutation")

    report = {
        "status": "PASS",
        "verdict": "both complete Core194 moving types (5,0,2) and (5,1,1) are excluded",
        "census": census,
        "base_formula": identity(base),
        "symmetry_audit": symmetries,
        "cases": cases,
        "all_nineteen_refuted": len(cases) == 19,
        "all_formulas_match_published": all(row["formula"] == public_cases[row["id"]]["formula"] for row in cases),
        "all_proofs_match_published": all(row["published_proof_match"] for row in cases),
        "proof_bytes": sum(row["proof"]["bytes"] for row in cases),
        "inspector_rejected_wrong_unit": inspector_rejected_wrong_unit,
        "false_refutation_rejected": True,
        "execution": "serial; one solver or proof-checker process at a time",
        "kissat_version": version,
        "kissat_binary": identity(args.kissat),
        "drat_trim_binary": identity(args.drat_trim),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "remaining_blue_empty_pair_moving_types": [[4, 1, 2]],
        "whole_core194_excluded": False,
        "red_pair_branch_resolved": False,
        "target_graph_found": False,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "cases": len(cases),
                      "proof_bytes": report["proof_bytes"]}, sort_keys=True))


if __name__ == "__main__":
    main()
