#!/usr/bin/env python3
"""Definition-level checks for the alternating fault-path theorem package."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
RED = 1
BLUE = 0


def need(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cycle_color(n: int, pair: tuple[int, int]) -> int | None:
    low, high = pair
    cycle_order = n - 1
    if high == low + 1 and high < cycle_order:
        return RED if low % 2 == 0 else BLUE
    if low == 0 and high == cycle_order - 1:
        return BLUE
    return None


def direct_receiver_summary(n: int) -> dict[str, object]:
    free_pairs = [p for p in combinations(range(n), 2) if cycle_color(n, p) is None]
    index = {pair: i + 1 for i, pair in enumerate(free_pairs)}
    states: Counter[tuple[int, int]] = Counter()
    records: list[tuple[int, ...]] = []
    for five in combinations(range(n), 5):
        physical_pairs = tuple(combinations(five, 2))
        colors = tuple(cycle_color(n, pair) for pair in physical_pairs)
        red = colors.count(RED)
        blue = colors.count(BLUE)
        states[(red, blue)] += 1
        free = tuple(index[pair] for pair, color in zip(physical_pairs, colors) if color is None)
        if blue == 0:
            records.append(tuple(-literal for literal in free))
        if red == 0:
            records.append(free)

    widths = Counter(map(len, records))
    clause_digest = hashlib.sha256()
    header = f"p cnf {len(index)} {len(records)}\n".encode("ascii")
    dimacs_digest = hashlib.sha256(header)
    dimacs_bytes = len(header)
    for clause in records:
        line = (" ".join(map(str, clause)) + " 0\n").encode("ascii")
        clause_digest.update(line)
        dimacs_digest.update(line)
        dimacs_bytes += len(line)
    five_sets = math.comb(n, 5)
    return {
        "n": n,
        "physical_edges": math.comb(n, 2),
        "fixed_cycle_edges": n - 1,
        "fixed_red_edges": (n - 1) // 2,
        "fixed_blue_edges": (n - 1) // 2,
        "variables": len(index),
        "five_sets": five_sets,
        "fixed_edge_color_histogram": {
            f"red_{red}_blue_{blue}": count
            for (red, blue), count in sorted(states.items())
        },
        "clauses": len(records),
        "unfixed_clauses": 2 * five_sets,
        "removed_satisfied_clauses": 2 * five_sets - len(records),
        "clause_width_histogram": {
            str(width): widths[width] for width in sorted(widths)
        },
        "clause_stream_sha256": clause_digest.hexdigest(),
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
    checked = red = blue = 0
    for five in combinations(range(len(rows)), 5):
        checked += 1
        red_edges = sum((rows[u] >> v) & 1 for u, v in combinations(five, 2))
        red += red_edges == 10
        blue += red_edges == 0
    return checked, red, blue


def dependency_and_control_check(expected: dict[str, object]) -> None:
    dependencies = json.loads((HERE / "DEPENDENCIES.json").read_text())
    for key in ("fault_hamiltonicity_input", "connectivity_input", "independent_review", "positive_control"):
        item = dependencies[key]
        path = (HERE / item["path"]).resolve()
        need(path.is_file(), f"missing dependency {key}")
        need(sha256(path) == item["sha256"], f"dependency hash {key}")

    source = (HERE / dependencies["positive_control"]["path"]).resolve()
    rows = decode_graph6(source.read_text())
    control = json.loads((HERE / "CONTROL42.json").read_text())
    cycle = control["alternating_cycle_old_labels"]
    need(sorted(cycle) == list(range(len(rows))), "control cycle is not spanning")
    colors = [
        ((rows[cycle[i]] >> cycle[(i + 1) % len(cycle)]) & 1)
        for i in range(len(cycle))
    ]
    need(colors == [i % 2 == 0 for i in range(len(cycle))], "control cycle does not alternate")
    checked, red, blue = monochromatic_fives(rows)
    degrees = [row.bit_count() for row in rows]
    actual = {
        "vertices": len(rows),
        "red_edges": sum(degrees) // 2,
        "minimum_red_degree": min(degrees),
        "maximum_red_degree": max(degrees),
        "five_subsets_checked": checked,
        "red_k5": red,
        "blue_k5": blue,
        "alternating_cycle_edges": len(cycle),
        "alternating_cycle_red_edges": sum(colors),
        "alternating_cycle_blue_edges": len(colors) - sum(colors),
    }
    need(actual == expected["control42"], "literal good42 control")

    # Relabel new vertex i as old cycle[i] and check the physical object again.
    relabeled = [0] * len(rows)
    for i, old_i in enumerate(cycle):
        for j, old_j in enumerate(cycle):
            if (rows[old_i] >> old_j) & 1:
                relabeled[i] |= 1 << j
    need(
        [((relabeled[i] >> ((i + 1) % len(rows))) & 1) for i in range(len(rows))]
        == [i % 2 == 0 for i in range(len(rows))],
        "relabeling did not fix the standard alternating cycle",
    )
    need(monochromatic_fives(relabeled) == (checked, 0, 0), "relabeling changed goodness")


def mark_pattern(bad: bytearray, ones: int, zeros: int, variable_count: int) -> None:
    free_positions = [i for i in range(variable_count) if not ((ones | zeros) >> i) & 1]
    base = ones
    for subset in range(1 << len(free_positions)):
        word = base
        for j, position in enumerate(free_positions):
            if (subset >> j) & 1:
                word |= 1 << position
        bad[word] = 1


def small_n7_semantic_control(expected: dict[str, object]) -> None:
    n = 7
    free_pairs = [p for p in combinations(range(n), 2) if cycle_color(n, p) is None]
    index = {pair: i for i, pair in enumerate(free_pairs)}
    variable_count = len(free_pairs)
    size = 1 << variable_count

    # Formula-side rejection sets, built from signed clauses.
    clauses: list[tuple[int, ...]] = []
    for five in combinations(range(n), 5):
        pairs = tuple(combinations(five, 2))
        colors = tuple(cycle_color(n, pair) for pair in pairs)
        free = tuple(index[pair] + 1 for pair, color in zip(pairs, colors) if color is None)
        if BLUE not in colors:
            clauses.append(tuple(-literal for literal in free))
        if RED not in colors:
            clauses.append(free)
    formula_bad = bytearray(size)
    for clause in clauses:
        # An unsatisfied positive literal is blue (zero); an unsatisfied
        # negative literal is red (one).
        ones = sum(1 << (abs(literal) - 1) for literal in clause if literal < 0)
        zeros = sum(1 << (literal - 1) for literal in clause if literal > 0)
        mark_pattern(formula_bad, ones, zeros, variable_count)

    # Definition-side rejection sets, rebuilt from physical red-edge counts.
    physical_bad = bytearray(size)
    for five in combinations(range(n), 5):
        pairs = tuple(combinations(five, 2))
        fixed = [cycle_color(n, pair) for pair in pairs if cycle_color(n, pair) is not None]
        free_mask = sum(1 << index[pair] for pair in pairs if pair in index)
        if BLUE not in fixed:  # a red K5 is possible only when every free pair is red
            mark_pattern(physical_bad, free_mask, 0, variable_count)
        if RED not in fixed:  # a blue K5 is possible only when every free pair is blue
            mark_pattern(physical_bad, 0, free_mask, variable_count)

    mismatches = sum(a != b for a, b in zip(formula_bad, physical_bad))
    actual = {
        "variables": variable_count,
        "assignments": size,
        "clauses": len(clauses),
        "admissible": size - sum(physical_bad),
        "formula_mismatches": mismatches,
    }
    need(actual == expected["small_n7_semantic_control"], "small formula semantics")


def theorem_arithmetic(expected: dict[str, object]) -> None:
    # For even orders, check the two ranges in the Bankfalvi inequality:
    # k=2..4 uses the inherited degree floor, while k>=5 uses goodness.
    even_cases = []
    for order in range(28, 43, 2):
        degree_floor = order - 25
        small_k_margins = {str(k): 2 * k * degree_floor - k * k for k in range(2, 5)}
        need(min(small_k_margins.values()) > 0, f"small-k degree margin at {order}")
        even_cases.append(
            {
                "order": order,
                "minimum_each_color_degree": degree_floor,
                "small_k_margins": small_k_margins,
                "largest_k": order // 2 - 1,
                "alternating_hamilton_cycle": True,
            }
        )
    need(even_cases == expected["even_induced_order_cases"], "even-order cycle cases")
    even_count = sum(math.comb(43, order) for order in range(28, 43, 2))
    need(
        even_count == expected["even_induced_sets_with_alternating_hamilton_cycle"],
        "even induced-set count",
    )

    # Check the degree-sum identity edge by edge.  By relabeling it suffices
    # to take canonical disjoint X and Y for each order and k.  Both the all-
    # blue constant term and every one-edge red flip are checked.
    for order in range(28, 43, 2):
        all_edges = tuple(combinations(range(order), 2))
        for k in range(2, order // 2):
            x = set(range(k))
            y = set(range(k, 2 * k))
            z = set(range(2 * k, order))

            # All-blue constant terms.
            left_constant = k * (order - 1)
            right_constant = k * k + k * (k - 1) + k * (order - 2 * k)
            need(left_constant == right_constant, f"identity constant {order},{k}")
            # Delta after changing one edge from blue to red.
            for u, v in all_edges:
                left_delta = (u in x) + (v in x) - (u in y) - (v in y)
                right_delta = (
                    2 * (u in x and v in x)
                    - 2 * (u in y and v in y)
                    + ((u in x and v in z) or (v in x and u in z))
                    - ((u in y and v in z) or (v in y and u in z))
                )
                need(left_delta == right_delta, f"identity coefficient {order},{k},{u},{v}")

    # Odd sets gain a PC Hamilton path with any prescribed endpoint by
    # inserting it into the alternating cycle on the remaining even set.
    cases = []
    for order in range(28, 44):
        source = "alternating_hamilton_cycle" if order % 2 == 0 else "insert_prescribed_endpoint"
        cases.append({"order": order, "source": source, "pc_hamilton_path": True})
    need(cases == expected["induced_order_cases"], "induced-order construction cases")
    count = sum(math.comb(43, order) for order in range(28, 44))
    need(count == expected["induced_sets_with_pc_hamilton_path"], "induced-set count")


def target_run_boundary_check(expected: dict[str, object]) -> None:
    run = json.loads((HERE / "TARGET_RUN.json").read_text())
    need(run["status"] == "UNKNOWN", "bounded run status")
    need(run["mathematical_evidence"] is False, "UNKNOWN promoted to evidence")
    need(run["result"]["model"] is None and run["result"]["proof"] is None, "false terminal artifact")
    for key in ("variables", "clauses", "dimacs_bytes", "dimacs_sha256"):
        run_key = {"dimacs_bytes": "bytes", "dimacs_sha256": "sha256"}.get(key, key)
        need(run["input"][run_key] == expected[key], f"bounded run input {key}")


def main() -> None:
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    direct = direct_receiver_summary(43)
    need(direct == {key: expected[key] for key in direct}, "independent receiver summary")
    producer = subprocess.run(
        [sys.executable, "-B", str(HERE / "generate.py"), "--summary"],
        check=True,
        text=True,
        capture_output=True,
    )
    need(json.loads(producer.stdout) == direct, "producer/checker mismatch")
    theorem_arithmetic(expected)
    small_n7_semantic_control(expected)
    dependency_and_control_check(expected)
    target_run_boundary_check(expected)
    print("VERIFIED_ALTERNATING_FAULT_PATH_RECEIVER")


if __name__ == "__main__":
    main()
