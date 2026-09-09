#!/usr/bin/env python3
"""Solver-free semantic and RUP check of all 238 switching exclusions.

This checker imports neither the formula generator nor the collector.  It
reconstructs each pinned base graph directly, checks that every compact input
clause forbids a physical monochromatic K5, and checks every proof addition by
plain repeated unit propagation (RUP).  It is deliberately small and is not
formally verified.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json
import time

INPUT_SHA256 = "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"
LENGTHS = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def parse_clause(line):
    values = list(map(int, line.split()))
    need(values and values[-1] == 0 and 0 not in values[:-1],
         "bad clause terminator")
    values.pop()
    need(len(set(values)) == len(values), "repeated literal")
    need(not any(-value in values for value in values), "tautological clause")
    return values


def parse_sections(path, core):
    sections = []
    current = None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if line.startswith("c source "):
            fields = line.split()
            need(len(fields) == 3 and fields[:2] == ["c", "source"],
                 f"{path.name}:{number}: bad source marker")
            index = int(fields[2])
            need(index == len(sections), f"{path.name}:{number}: source order")
            current = []
            sections.append(current)
        else:
            need(current is not None, f"{path.name}:{number}: content before source")
            current.append(line)
    need(len(sections) == 238, f"{path.name}: expected 238 sections")
    if core:
        for index, lines in enumerate(sections):
            need(lines and lines[0].startswith("p cnf "),
                 f"core {index}: missing header")
            fields = lines[0].split()
            need(len(fields) == 4 and fields[:3] == ["p", "cnf", "42"],
                 f"core {index}: bad header")
            need(int(fields[3]) == len(lines) - 1,
                 f"core {index}: clause count")
            sections[index] = lines[1:]
    return sections


def pinned_sources(path):
    need(sha256(path.read_bytes()).hexdigest() == INPUT_SHA256,
         "pinned source identity")
    data = json.loads(path.read_text())
    rows = data["complete_additional_objective_12_rotation_representatives"]
    need(data["order"] == 43 and data["edge_count"] == 903,
         "source dimensions")
    need(len(rows) == 238 and len({tuple(row) for row in rows}) == 238,
         "complete unique source list")
    edges = list(combinations(range(43), 2))
    for index, row in enumerate(rows):
        need(row == sorted(set(row)), f"source {index}: canonical toggle list")
        need(all(0 <= value < len(edges) for value in row),
             f"source {index}: toggle range")
    return rows


def base_graph(toggle_indices):
    toggles = set(toggle_indices)
    red = [[False] * 43 for _ in range(43)]
    for index, (u, v) in enumerate(combinations(range(43), 2)):
        length = min((v - u) % 43, (u - v) % 43)
        red[u][v] = red[v][u] = (length in LENGTHS) ^ (index in toggles)
    return red


def physical_core(lines, toggle_indices):
    red = base_graph(toggle_indices)
    database = set()
    colors = Counter()
    widths = Counter()
    for line in lines:
        row = parse_clause(line)
        need(len(row) in (4, 5), "core clause is not width 4 or 5")
        need(all(1 <= abs(value) <= 42 for value in row),
             "core literal outside normalized switch range")
        assignment = {abs(value): int(value < 0) for value in row}
        if len(row) == 4:
            assignment[0] = 0
        need(len(assignment) == 5, "core clause is not on five physical vertices")
        color_set = {int(red[u][v]) ^ assignment[u] ^ assignment[v]
                     for u, v in combinations(sorted(assignment), 2)}
        need(len(color_set) == 1, "core clause is not a physical monochromatic K5")
        colors[str(color_set.pop())] += 1
        widths[str(len(row))] += 1
        frozen = frozenset(row)
        need(frozen not in database, "duplicate physical core clause")
        database.add(frozen)
    need(database, "empty physical core")
    return database, colors, widths


def rup(database, candidate):
    if any(-value in candidate for value in candidate):
        return True
    true = {-value for value in candidate}
    changed = True
    while changed:
        changed = False
        for row in database:
            if row & true:
                continue
            remaining = [value for value in row if -value not in true]
            if not remaining:
                return True
            if len(remaining) == 1 and remaining[0] not in true:
                true.add(remaining[0])
                changed = True
    return False


def verify_proof(core, lines):
    database = Counter(core)
    statistics = Counter()
    empty = False
    for number, line in enumerate(lines, 1):
        need(not empty, "proof continues after empty clause")
        deleted = line.startswith("d ")
        row = parse_clause(line[2:] if deleted else line)
        need(all(1 <= abs(value) <= 42 for value in row),
             "proof literal outside 1..42")
        frozen = frozenset(row)
        if deleted:
            statistics["deletions"] += 1
            if frozen not in database:
                statistics["absent_deletions"] += 1
            elif database[frozen] == 1:
                del database[frozen]
            else:
                database[frozen] -= 1
            continue
        statistics["additions"] += 1
        need(rup(database, frozen), f"addition fails RUP at proof line {number}")
        statistics["rup_additions"] += 1
        database[frozen] += 1
        empty = not row
    need(empty, "proof does not derive the empty clause")
    return statistics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("cores", type=Path)
    parser.add_argument("proofs", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    sources = pinned_sources(args.source)
    core_sections = parse_sections(args.cores, core=True)
    proof_sections = parse_sections(args.proofs, core=False)
    totals = Counter()
    colors = Counter()
    widths = Counter()
    case_core_counts = []
    for index, (toggles, core_lines, proof_lines) in enumerate(
            zip(sources, core_sections, proof_sections)):
        core, case_colors, case_widths = physical_core(core_lines, toggles)
        proof = verify_proof(core, proof_lines)
        case_core_counts.append(len(core))
        colors.update(case_colors)
        widths.update(case_widths)
        totals.update(proof)
        if not args.quiet and ((index + 1) % 25 == 0 or index == 237):
            print(json.dumps({"checked_sources": index + 1}), flush=True)
    report = {
        "status": "VERIFIED_COMPLETE_238_SOURCE_SWITCH_CLASS_EXCLUSION",
        "source_count": 238,
        "physical_core_clauses": sum(case_core_counts),
        "physical_core_clauses_min": min(case_core_counts),
        "physical_core_clauses_max": max(case_core_counts),
        "physical_core_color_counts": dict(sorted(colors.items())),
        "physical_core_width_counts": dict(sorted(widths.items())),
        "proof_totals": dict(sorted(totals.items())),
        "source_sha256": sha256(args.source.read_bytes()).hexdigest(),
        "cores_sha256": sha256(args.cores.read_bytes()).hexdigest(),
        "proofs_sha256": sha256(args.proofs.read_bytes()).hexdigest(),
        "verification_seconds": time.monotonic() - started,
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
