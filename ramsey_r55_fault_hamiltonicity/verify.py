#!/usr/bin/env python3
"""Independent exact checks for the fault-Hamiltonicity receiver package."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def adjacent_on_cycle(n: int, pair: tuple[int, int]) -> bool:
    a, b = pair
    return abs(a - b) == 1 or {a, b} == {0, n - 1}


def independent_formula(n: int, k: int) -> int:
    # k-subsets of a labeled n-cycle with no consecutive pair.
    return n * math.comb(n - k - 1, k - 1) // k


def direct_receiver_summary(n: int) -> dict[str, object]:
    free_pairs = [p for p in combinations(range(n), 2) if not adjacent_on_cycle(n, p)]
    index = {pair: i + 1 for i, pair in enumerate(free_pairs)}
    cycle_hist: dict[int, int] = {}
    width_hist: dict[int, int] = {}
    digest = hashlib.sha256()
    # The header is known once the zero-edge cycle subsets have been counted.
    for five in combinations(range(n), 5):
        physical_pairs = tuple(combinations(five, 2))
        red_fixed = sum(adjacent_on_cycle(n, pair) for pair in physical_pairs)
        cycle_hist[red_fixed] = cycle_hist.get(red_fixed, 0) + 1
    expected_clauses = math.comb(n, 5) + cycle_hist.get(0, 0)
    header = f"p cnf {len(index)} {expected_clauses}\n".encode("ascii")
    dimacs_digest = hashlib.sha256(header)
    dimacs_bytes = len(header)
    clause_count = 0
    for five in combinations(range(n), 5):
        physical_pairs = tuple(combinations(five, 2))
        red_fixed = sum(adjacent_on_cycle(n, pair) for pair in physical_pairs)
        red_clause = tuple(-index[pair] for pair in physical_pairs if pair in index)
        line = (" ".join(map(str, red_clause)) + " 0\n").encode("ascii")
        digest.update(line)
        dimacs_digest.update(line)
        dimacs_bytes += len(line)
        width_hist[len(red_clause)] = width_hist.get(len(red_clause), 0) + 1
        clause_count += 1
        if red_fixed == 0:
            blue_clause = tuple(index[pair] for pair in physical_pairs)
            line = (" ".join(map(str, blue_clause)) + " 0\n").encode("ascii")
            digest.update(line)
            dimacs_digest.update(line)
            dimacs_bytes += len(line)
            width_hist[len(blue_clause)] = width_hist.get(len(blue_clause), 0) + 1
            clause_count += 1
    return {
        "n": n,
        "physical_edges": math.comb(n, 2),
        "fixed_cycle_edges": n,
        "variables": len(index),
        "five_sets": math.comb(n, 5),
        "cycle_edge_histogram": {str(k): cycle_hist[k] for k in sorted(cycle_hist)},
        "clauses": clause_count,
        "unfixed_clauses": 2 * math.comb(n, 5),
        "removed_satisfied_clauses": math.comb(n, 5) - cycle_hist.get(0, 0),
        "clause_width_histogram": {str(k): width_hist[k] for k in sorted(width_hist)},
        "clause_stream_sha256": digest.hexdigest(),
        "dimacs_bytes": dimacs_bytes,
        "dimacs_sha256": dimacs_digest.hexdigest(),
    }


def decode_graph6(text: str) -> list[int]:
    text = text.strip()
    need(text and ord(text[0]) < 126, "only compact graph6 order is supported")
    n = ord(text[0]) - 63
    bits: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        need(0 <= value < 64, "bad graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    need(len(bits) >= math.comb(n, 2), "short graph6 record")
    rows = [0] * n
    offset = 0
    for high in range(1, n):
        for low in range(high):
            if bits[offset]:
                rows[low] |= 1 << high
                rows[high] |= 1 << low
            offset += 1
    return rows


def monochromatic_fives(rows: list[int]) -> tuple[int, int, int]:
    red = blue = checked = 0
    for five in combinations(range(len(rows)), 5):
        checked += 1
        red_edges = sum((rows[u] >> v) & 1 for u, v in combinations(five, 2))
        red += red_edges == 10
        blue += red_edges == 0
    return checked, red, blue


def control_check(expected: dict[str, object]) -> None:
    dependency = json.loads((HERE / "DEPENDENCIES.json").read_text())
    for key in ("target_specific_input", "independent_accepting_review", "positive_control"):
        item = dependency[key]
        path = (HERE / item["path"]).resolve()
        need(path.is_file(), f"missing dependency {key}")
        need(sha256(path) == item["sha256"], f"dependency hash {key}")

    source = (HERE / dependency["positive_control"]["path"]).resolve()
    rows = decode_graph6(source.read_text())
    control = json.loads((HERE / "CONTROL42.json").read_text())
    cycle = control["cycle_old_labels"]
    n = len(rows)
    need(sorted(cycle) == list(range(n)), "control cycle is not a permutation")
    need(all((rows[cycle[i]] >> cycle[(i + 1) % n]) & 1 for i in range(n)),
         "control cycle has a blue edge")
    checked, red, blue = monochromatic_fives(rows)
    degrees = [row.bit_count() for row in rows]
    actual = {
        "vertices": n,
        "red_edges": sum(degrees) // 2,
        "minimum_red_degree": min(degrees),
        "maximum_red_degree": max(degrees),
        "five_subsets_checked": checked,
        "red_k5": red,
        "blue_k5": blue,
    }
    need(actual == expected["control42"], "control42 physical statistics")

    # Relabel new i as old cycle[i], then check every physical edge and five-set.
    relabeled = [0] * n
    for i, old_i in enumerate(cycle):
        for j, old_j in enumerate(cycle):
            if (rows[old_i] >> old_j) & 1:
                relabeled[i] |= 1 << j
    need(all((relabeled[i] >> ((i + 1) % n)) & 1 for i in range(n)),
         "relabeling did not fix the standard cycle")
    need(monochromatic_fives(relabeled) == (checked, 0, 0),
         "relabeling changed goodness")
    for i, j in combinations(range(n), 2):
        need(((relabeled[i] >> j) & 1) == ((rows[cycle[i]] >> cycle[j]) & 1),
             "physical relabel mismatch")


def theorem_arithmetic(expected: dict[str, object]) -> None:
    statuses = []
    for deleted in range(16):
        connectivity = 18 - deleted
        traceable = deleted <= 15 and (connectivity >= 4 or connectivity == 3)
        hamiltonian = connectivity >= 4
        hamilton_connected = connectivity >= 5
        statuses.append((deleted, connectivity, traceable, hamiltonian, hamilton_connected))
    need(all(row[2] for row in statuses), "traceability threshold")
    need(all(row[3] == (row[0] <= 14) for row in statuses), "Hamilton threshold")
    need(all(row[4] == (row[0] <= 13) for row in statuses), "Hamilton-connected threshold")

    cycles = sum(math.comb(43, k) for k in range(29, 44))
    paths = sum(math.comb(43, k) * math.comb(k, 2) for k in range(30, 44))
    rooted = sum(math.comb(41, s) for s in range(14))
    need(cycles == expected["cycles_each_color_lengths_29_to_43"], "cycle count")
    need(paths == expected["endpoint_paths_each_color_orders_30_to_43"], "path count")
    need(rooted == expected["cycles_through_each_colored_edge_lengths_30_to_43"],
         "edge-rooted cycle count")


def small_semantic_control(expected: dict[str, object]) -> None:
    n = 7
    free_pairs = [p for p in combinations(range(n), 2) if not adjacent_on_cycle(n, p)]
    index = {pair: i for i, pair in enumerate(free_pairs)}
    clauses: list[tuple[int, ...]] = []
    for five in combinations(range(n), 5):
        physical_pairs = tuple(combinations(five, 2))
        free = tuple(index[pair] for pair in physical_pairs if pair in index)
        # Signed zero-based literals: +(i+1) is red, -(i+1) is blue.
        clauses.append(tuple(-(i + 1) for i in free))
        if len(free) == 10:
            clauses.append(tuple(i + 1 for i in free))

    admissible = mismatches = 0
    for word in range(1 << len(free_pairs)):
        formula_ok = True
        for clause in clauses:
            if not any(
                bool((word >> (abs(literal) - 1)) & 1) == (literal > 0)
                for literal in clause
            ):
                formula_ok = False
                break
        physical_ok = True
        for five in combinations(range(n), 5):
            red_edges = 0
            for pair in combinations(five, 2):
                red_edges += (
                    1 if adjacent_on_cycle(n, pair)
                    else (word >> index[pair]) & 1
                )
            if red_edges in (0, 10):
                physical_ok = False
                break
        mismatches += formula_ok != physical_ok
        admissible += physical_ok
    actual = {
        "assignments": 1 << len(free_pairs),
        "admissible": admissible,
        "formula_mismatches": mismatches,
    }
    need(actual == expected["small_n7_semantic_control"], "small formula semantics")


def main() -> None:
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    direct = direct_receiver_summary(43)
    projected = {key: expected[key] for key in direct}
    need(direct == projected, "independent target receiver summary")
    need(direct["cycle_edge_histogram"]["0"] == independent_formula(43, 5),
         "independent-set formula on C43")

    producer = subprocess.run(
        [sys.executable, "-B", str(HERE / "generate.py"), "--summary"],
        check=True, text=True, capture_output=True,
    )
    need(json.loads(producer.stdout) == direct, "producer/checker mismatch")
    theorem_arithmetic(expected)
    small_semantic_control(expected)
    control_check(expected)
    print("VERIFIED_FAULT_HAMILTONICITY_RECEIVER")


if __name__ == "__main__":
    main()
