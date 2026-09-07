#!/usr/bin/env python3
"""Run the frozen aggregate formula and certify either SAT or UNSAT output."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path
import resource
import subprocess
import time


N = 43
A_SIZE = 20
B_SIZE = 23


def file_sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def dot(a: int, b: int) -> int:
    return (a & b).bit_count() & 1


def rank(rows: list[int], width: int) -> int:
    basis = [0] * width
    result = 0
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if basis[pivot]:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                result += 1
                break
    return result


def rows_from_code(code: int) -> list[int]:
    counts = [(code >> (2 * value)) & 3 for value in range(15)]
    zeros = 20 - sum(counts)
    rows = [0] * zeros + [
        value for value in range(1, 16) for _ in range(counts[value - 1])
    ]
    if zeros not in (0, 1) or len(rows) != A_SIZE or rank(rows, 4) != 4:
        raise ValueError("invalid selected row code")
    return rows


def parse_assignment(path: Path, variables: int) -> tuple[str, dict[int, bool]]:
    status = None
    assignment: dict[int, bool] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("s "):
            status = line[2:].strip()
        elif line.startswith("v "):
            for token in line[2:].split():
                literal = int(token)
                if not literal:
                    continue
                variable = abs(literal)
                value = literal > 0
                if variable in assignment and assignment[variable] != value:
                    raise AssertionError("inconsistent witness")
                assignment[variable] = value
    if status == "SATISFIABLE" and set(assignment) != set(range(1, variables + 1)):
        raise AssertionError(("incomplete witness", len(assignment), variables))
    return status or "MISSING", assignment


def clause_audit(cnf: Path, assignment: dict[int, bool]) -> dict:
    clauses = 0
    with cnf.open("r", encoding="ascii") as handle:
        header = handle.readline().split()
        if header[:2] != ["p", "cnf"] or len(header) != 4:
            raise AssertionError("CNF header")
        variables, declared = map(int, header[2:])
        if set(assignment) != set(range(1, variables + 1)):
            raise AssertionError("assignment domain")
        for line in handle:
            values = list(map(int, line.split()))
            if not values or values[-1] != 0:
                raise AssertionError("CNF syntax")
            if not any(assignment[abs(literal)] == (literal > 0)
                       for literal in values[:-1]):
                raise AssertionError(("unsatisfied clause", clauses))
            clauses += 1
    if clauses != declared:
        raise AssertionError("CNF clause count")
    return {"variables": variables, "clauses": clauses}


def decode_candidate(metadata: dict, assignment: dict[int, bool]) -> dict:
    selectors = metadata["cover"]["selector_variables"]
    selected = [index for index, variable in enumerate(selectors) if assignment[variable]]
    if len(selected) != 1:
        raise AssertionError(("selected tasks", selected))
    task_index = selected[0]
    row_code = metadata["cover"]["row_codes"][task_index]
    rows = rows_from_code(row_code)

    row_variables = metadata["maps"]["row_label_variables"]
    decoded_rows = []
    for variables in row_variables:
        chosen = [value for value, variable in enumerate(variables) if assignment[variable]]
        if len(chosen) != 1:
            raise AssertionError(("row one-hot", chosen))
        decoded_rows.append(chosen[0])
    if decoded_rows != rows:
        raise AssertionError("selected task and row labels disagree")

    column_variables = metadata["maps"]["column_label_variables"]
    columns = []
    for variables in column_variables:
        chosen = [value for value, variable in enumerate(variables) if assignment[variable]]
        if len(chosen) != 1:
            raise AssertionError(("column one-hot", chosen))
        columns.append(chosen[0])
    if columns != sorted(columns):
        raise AssertionError("columns not sorted")
    populations = Counter(columns)
    if populations[0] > 2 or any(populations[value] > 5 for value in range(1, 16)):
        raise AssertionError("column cap")
    if len(populations) > 8 or rank(columns, 4) != 4:
        raise AssertionError("column support")
    if 0 in rows and populations[0]:
        raise AssertionError("simultaneous zero")

    internal = {
        tuple(map(int, key.split(","))): variable
        for key, variable in metadata["maps"]["internal_variables"].items()
    }
    cross = {
        tuple(map(int, key.split(","))): variable
        for key, variable in metadata["maps"]["cross_variables"].items()
    }
    red_edges = []
    edge_colours: dict[tuple[int, int], bool] = {}
    for edge in combinations(range(N), 2):
        first, second = edge
        if edge in internal:
            red = assignment[internal[edge]]
        else:
            expected = bool(dot(rows[first], columns[second - A_SIZE]))
            red = assignment[cross[edge]]
            if red != expected:
                raise AssertionError(("cross edge", edge, red, expected))
        edge_colours[edge] = red
        if red:
            red_edges.append([first, second])

    red_fives = 0
    blue_fives = 0
    first_violation = None
    for vertices in combinations(range(N), 5):
        colours = [edge_colours[edge] for edge in combinations(vertices, 2)]
        if all(colours):
            red_fives += 1
            first_violation = first_violation or ["red", list(vertices)]
        if not any(colours):
            blue_fives += 1
            first_violation = first_violation or ["blue", list(vertices)]
    if first_violation:
        raise AssertionError(("physical five-set violation", first_violation))

    degrees = [sum(edge_colours[tuple(sorted((vertex, other)))]
                   for other in range(N) if other != vertex)
               for vertex in range(N)]
    if min(degrees) < 18 or max(degrees) > 24:
        raise AssertionError("degree interval")

    row_counts = Counter(rows)
    contacts = {value: sum(dot(value, column) for column in columns)
                for value in range(1, 16) if row_counts[value] == 3}
    if any(not 10 <= count <= 13 for count in contacts.values()):
        raise AssertionError("tripled contact")

    row_pairs_checked = 0
    for first, second in combinations(range(A_SIZE), 2):
        if rows[first] != rows[second]:
            continue
        distance = sum(
            edge_colours[tuple(sorted((first, other)))]
            != edge_colours[tuple(sorted((second, other)))]
            for other in range(A_SIZE) if other not in (first, second)
        )
        if distance < 8:
            raise AssertionError(("row pair distance", first, second, distance))
        row_pairs_checked += 1
    column_pairs_checked = 0
    for first, second in combinations(range(B_SIZE), 2):
        if columns[first] != columns[second]:
            continue
        physical_first = A_SIZE + first
        physical_second = A_SIZE + second
        distance = sum(
            edge_colours[tuple(sorted((physical_first, A_SIZE + other)))]
            != edge_colours[tuple(sorted((physical_second, A_SIZE + other)))]
            for other in range(B_SIZE) if other not in (first, second)
        )
        if distance < 8:
            raise AssertionError(("column pair distance", first, second, distance))
        column_pairs_checked += 1

    red_rows = [sum(dot(row, column) << position
                    for position, column in enumerate(columns)) for row in rows]
    blue_rows = [row ^ ((1 << B_SIZE) - 1) for row in red_rows]
    red_rank = rank(red_rows, B_SIZE)
    blue_rank = rank(blue_rows, B_SIZE)
    if red_rank != 4 or blue_rank < 4:
        raise AssertionError(("cut ranks", red_rank, blue_rank))

    mask = sum(int(edge_colours[edge]) << index
               for index, edge in enumerate(combinations(range(N), 2)))
    return {
        "schema": "verified-good43-edge-list-v1",
        "n": N,
        "row_task_index": task_index,
        "row_code": row_code,
        "rows": rows,
        "columns": columns,
        "column_support": sorted(populations),
        "red_edges": red_edges,
        "red_hex": format(mask, "0226x"),
        "red_edge_count": len(red_edges),
        "red_degrees": degrees,
        "red_cut_rank": red_rank,
        "blue_cut_rank": blue_rank,
        "tripled_contacts": contacts,
        "equal_row_pairs_checked": row_pairs_checked,
        "equal_column_pairs_checked": column_pairs_checked,
        "five_sets_checked": 962598,
        "red_fives": red_fives,
        "blue_fives": blue_fives,
        "status": "SAT_VERIFIED_GOOD43",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--transcript", type=Path, required=True)
    parser.add_argument("--checker-transcript", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()

    frozen = json.loads(args.frozen.read_text())
    for name, expected in frozen["inputs"].items():
        path = args.frozen.parent / name
        if file_sha256(path) != expected:
            raise AssertionError(("frozen input changed", name))
    if file_sha256(args.cnf) != frozen["cnf_sha256"]:
        raise AssertionError("frozen CNF changed")
    if file_sha256(args.solver) != frozen["solver_sha256"]:
        raise AssertionError("solver changed")
    if file_sha256(args.checker) != frozen["checker_sha256"]:
        raise AssertionError("checker changed")
    for path in (args.witness, args.proof, args.transcript,
                 args.checker_transcript, args.candidate, args.result):
        if path.exists():
            raise ValueError(f"refusing existing output {path}")

    metadata = json.loads(args.metadata.read_text())
    seconds = frozen["seconds_limit"]
    command = [str(args.solver), "-q", "-t", str(seconds),
               "-w", str(args.witness), str(args.cnf), str(args.proof)]
    before_usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = time.monotonic()
    run = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, check=False, timeout=seconds + 120)
    elapsed = time.monotonic() - started
    after_usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    args.transcript.write_text(run.stdout)
    result = {
        "schema": "rank4-all-row-support8-production-v1",
        "command": command,
        "seconds_limit": seconds,
        "solver_exit": run.returncode,
        "solver_seconds": elapsed,
        "solver_user_seconds": after_usage.ru_utime - before_usage.ru_utime,
        "solver_system_seconds": after_usage.ru_stime - before_usage.ru_stime,
        "child_max_rss_kib": after_usage.ru_maxrss,
        "cnf_sha256": file_sha256(args.cnf),
        "cnf_bytes": args.cnf.stat().st_size,
        "variables": metadata["formula"]["variables"],
        "clauses": metadata["formula"]["clauses"],
        "solver_version": subprocess.run([str(args.solver), "--version"],
                                         capture_output=True, text=True,
                                         check=True).stdout.strip(),
        "solver_sha256": file_sha256(args.solver),
        "checker_sha256": file_sha256(args.checker),
    }
    witness_status, assignment = parse_assignment(
        args.witness, metadata["formula"]["variables"]
    )
    result["witness_status"] = witness_status
    if run.returncode == 10 and witness_status == "SATISFIABLE":
        result["clause_audit"] = clause_audit(args.cnf, assignment)
        candidate = decode_candidate(metadata, assignment)
        args.candidate.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n")
        result["candidate_sha256"] = file_sha256(args.candidate)
        result["status"] = "SAT_VERIFIED_GOOD43"
    elif (run.returncode == 20 and witness_status == "UNSATISFIABLE"
          and args.proof.is_file() and args.proof.stat().st_size):
        checked_started = time.monotonic()
        checked = subprocess.run([str(args.checker), str(args.cnf), str(args.proof)],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, check=False, timeout=2 * seconds + 600)
        result["checker_seconds"] = time.monotonic() - checked_started
        args.checker_transcript.write_text(checked.stdout)
        result["checker_exit"] = checked.returncode
        if checked.returncode == 0 and "s VERIFIED" in checked.stdout:
            result.update({
                "status": "UNSAT_PROOF_VERIFIED",
                "proof_bytes": args.proof.stat().st_size,
                "proof_sha256": file_sha256(args.proof),
            })
        else:
            result.update({
                "status": "PROOF_REJECTED",
                "checker_output_tail": checked.stdout[-2000:],
            })
    else:
        result.update({
            "status": "UNKNOWN",
            "proof_bytes": args.proof.stat().st_size if args.proof.exists() else 0,
            "solver_output_tail": run.stdout[-2000:],
        })
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
