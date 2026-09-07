#!/usr/bin/env python3
"""Independent audit of the complete rank-four good43 task cover."""

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import json
import subprocess
import tempfile


EXPECTED_TABLE_SHA256 = "bd1161b4261eb1ee3f8bc2cd0104a062c858bf38d596cf725acbfb195b158bac"
EXPECTED_AUDIT_SHA256 = "4ce493a63cf754fc7329d8236820d8cb53e442089b403e5ffa638fb098c44c29"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rank(vectors):
    basis = {}
    for value in vectors:
        while value:
            bit = value.bit_length() - 1
            if bit in basis:
                value ^= basis[bit]
            else:
                basis[bit] = value
                break
    return len(basis)


def matrices():
    """Enumerate GL(4,2) by filtering all binary 4-by-4 matrices."""
    result = []
    for encoded in range(1 << 16):
        columns = tuple((encoded >> (4 * k)) & 15 for k in range(4))
        if rank(columns) != 4:
            continue
        image = []
        for x in range(16):
            y = 0
            for k, column in enumerate(columns):
                if x >> k & 1:
                    y ^= column
            image.append(y)
        result.append(tuple(image))
    require(len(result) == 20160 and len(set(result)) == 20160, "GL(4,2) enumeration")
    return result


def span_mask(vectors):
    span = {0}
    for vector in vectors:
        span |= {x ^ vector for x in span}
    return sum(1 << x for x in span)


@lru_cache(maxsize=None)
def join(left, right):
    xs = [x for x in range(16) if left >> x & 1]
    ys = [y for y in range(16) if right >> y & 1]
    result = 0
    for x in xs:
        for y in ys:
            result |= 1 << (x ^ y)
    return result


def cycles(image):
    seen = {0}
    result = []
    for start in range(1, 16):
        if start in seen:
            continue
        cycle = []
        x = start
        while x not in seen:
            seen.add(x)
            cycle.append(x)
            x = image[x]
        require(x == start, "invalid permutation cycle")
        result.append(tuple(cycle))
    return result


def direct_spanning_burnside(group):
    """Count only spanning fixed profiles, with span carried in the DP state."""
    fixed_sums = [0, 0]
    type_histogram = Counter()
    for image in group:
        cs = cycles(image)
        type_histogram[tuple(sorted(map(len, cs)))] += 1
        dp = {(0, 1): 1}  # (weight, exact linear-span bitmask)
        for cycle in cs:
            length = len(cycle)
            added_span = span_mask(cycle)
            nxt = defaultdict(int)
            for (weight, current_span), count in dp.items():
                nxt[weight, current_span] += count
                merged = join(current_span, added_span)
                for digit in (1, 2, 3):
                    new_weight = weight + digit * length
                    if new_weight <= 20:
                        nxt[new_weight, merged] += count
            dp = nxt
        for index, weight in enumerate((19, 20)):
            fixed_sums[index] += dp.get((weight, 0xFFFF), 0)
    require(all(total % len(group) == 0 for total in fixed_sums), ("Burnside integrality", fixed_sums))
    return {
        "cycle_types": len(type_histogram),
        "fixed_spanning_sums": fixed_sums,
        "spanning_orbits": [total // len(group) for total in fixed_sums],
    }


def raw_profile_counts():
    polynomial = [1] + [0] * 20
    for _ in range(15):
        nxt = [0] * 21
        for weight, count in enumerate(polynomial):
            for digit in range(4):
                if weight + digit <= 20:
                    nxt[weight + digit] += count
        polynomial = nxt
    return [polynomial[19], polynomial[20]]


def formula_dimensions():
    one_hot = 23 * (1 + comb(16, 2))
    star_implications = 23 * 15 * 16
    spanning = 15
    sorting = 22 * sum(range(16))
    caps = (23 - 2) + 15 * (23 - 5)
    ordinary_base = 1 + one_hot + star_implications + spanning + sorting + caps
    variables = 1 + 443 + 23 * 16 + 15 * 23
    ramsey = 2 * comb(43, 5)
    zero_tautologies = comb(42, 4) - comb(19, 4)
    # Sixteen occurrence gates, 315 two-input AND gates, fifteen 21-input
    # triple gates, and the final exact-sector guard clause.
    known_guard_clauses = 16 * 24 + 15 * (21 * 3 + 22) + 1
    known_guard_variables = 16 + 15 * 21 + 15
    result = {
        "affine_rows": {
            "variables": variables,
            "base_clauses": ordinary_base + 8,
            "ramsey_clauses": ramsey,
            "clauses": ordinary_base + 8 + ramsey,
        },
        "known_profile_guard": {
            "variables": variables + known_guard_variables,
            "base_clauses": ordinary_base + known_guard_clauses,
            "ramsey_clauses": ramsey,
            "clauses": ordinary_base + known_guard_clauses + ramsey,
        },
        "ordinary": {
            "variables": variables,
            "base_clauses": ordinary_base,
            "ramsey_clauses": ramsey,
            "clauses": ordinary_base + ramsey,
        },
        "zero_row": {
            "variables": variables,
            "base_clauses": ordinary_base + 23,
            "ramsey_clauses": ramsey - zero_tautologies,
            "clauses": ordinary_base + 23 + ramsey - zero_tautologies,
        },
    }
    require(result == {
        "affine_rows": {"variables": 1157, "base_clauses": 11258, "ramsey_clauses": 1925196, "clauses": 1936454},
        "known_profile_guard": {"variables": 1503, "base_clauses": 12910, "ramsey_clauses": 1925196, "clauses": 1938106},
        "ordinary": {"variables": 1157, "base_clauses": 11250, "ramsey_clauses": 1925196, "clauses": 1936446},
        "zero_row": {"variables": 1157, "base_clauses": 11273, "ramsey_clauses": 1817142, "clauses": 1828415},
    }, "formula dimensions")
    return result


def check_committed_audit(target, dimensions):
    evidence = json.loads((target / "EXPECTED_AUDIT.json").read_text())
    require(evidence["status"] == "VERIFIED_ALL_PATTERN_RANK4_TASK_HANDOFF", "audit status")
    require(evidence["controls"]["category_counts"] == {
        "affine_rows": 5,
        "known_profile_guard": 4,
        "ordinary": 5841,
        "zero_row": 5109,
    }, "audit categories")
    require(len(evidence["instances"]) == 4, "audit instance count")
    for instance in evidence["instances"]:
        category = instance["category"]
        for key, expected in dimensions[category].items():
            require(instance[key] == expected, ("instance dimension", category, key))
        require(instance["physical_clauses_checked"] == instance["ramsey_clauses"], "physical clause audit")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--work-root", type=Path, required=True)
    args = parser.parse_args()
    table = args.target / "row_cover.tsv"
    require(sha256(table.read_bytes()).hexdigest() == EXPECTED_TABLE_SHA256, "row table hash")

    group = matrices()
    burnside = direct_spanning_burnside(group)
    require(burnside["cycle_types"] == 12, "cycle-type count")
    require(burnside["spanning_orbits"] == [5109, 5850], "direct spanning Burnside count")
    require(raw_profile_counts() == [71475600, 83372562], "raw profile count")

    source = Path(__file__).with_name("orbit_check.cpp")
    with tempfile.TemporaryDirectory(prefix="rank4-cover-review-", dir=args.work_root) as directory:
        binary = Path(directory) / "orbit_check"
        subprocess.run(
            ["g++", "-std=c++17", "-Wall", "-Wextra", "-Wpedantic", "-O3", source, "-o", binary],
            check=True,
        )
        output = subprocess.run([binary, table], check=True, text=True, capture_output=True)
    orbit_table = json.loads(output.stdout)
    require(orbit_table == {
        "canonical_map_checks": 220933440,
        "category_counts": {
            "affine_rows": 5,
            "known_profile_guard": 4,
            "ordinary": 5841,
            "zero_row": 5109,
        },
        "group_order": 20160,
        "matrix_candidates": 65536,
        "profile_mass": [71475180, 83372457],
        "table_rows": 10959,
        "status": "VERIFIED_INDEPENDENT_ORBIT_TABLE",
    }, "independent orbit table")

    dimensions = formula_dimensions()
    check_committed_audit(args.target, dimensions)
    result = {
        "audit_sha256_replayed_separately": EXPECTED_AUDIT_SHA256,
        "direct_spanning_burnside": burnside,
        "formula_dimensions": dimensions,
        "orbit_table": orbit_table,
        "raw_profiles": raw_profile_counts(),
        "row_cover_sha256": EXPECTED_TABLE_SHA256,
        "status": "VERIFIED_INDEPENDENT_RANK4_TASK_COVER_REVIEW",
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
