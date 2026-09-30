#!/usr/bin/env python3
"""Separate exact author check; imports no main or earlier generator.

Literal B-page capacities, defect-vector recursion and bitmask row tables
regenerate the complete domains. With --compare-records, all exceptional
configurations, survivors and counting certificates agree entry by entry.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

POINTS = set(range(7))
PAIRS = list(combinations(range(7), 2))
EDGES = {(0, 1), (2, 3), (3, 4), (4, 5), (5, 6), (2, 6)}
N = [{j for j in POINTS if i != j and (min(i, j), max(i, j)) in EDGES} for i in range(7)]
H = list(map(len, N))
BLUE = [POINTS - n - {i} for i, n in enumerate(N)]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def fingerprint(records):
    return sha256(json.dumps(sorted(records), separators=(",", ":")).encode()).hexdigest()


def row(mask):
    return tuple(i for i in range(7) if (mask >> i) & 1)


def defect_vectors(total, start=0):
    if start == 20:
        yield (total,)
        return
    for amount in range(total + 1):
        for tail in defect_vectors(total - amount, start + 1):
            yield (amount,) + tail


def positive_table():
    masks = [m for m in range(1 << 7) if m.bit_count() == 4 and
             sum(H[b] for b in row(m)) <= 7]
    table = defaultdict(list)
    for i, m in enumerate(masks):
        for n in masks[i:]:
            loads = tuple(((m >> b) & 1) + ((n >> b) & 1) for b in range(7))
            table[loads].append(tuple(sorted((row(m), row(n)))))
    return table


def analyze_shapes(ones, hs, p, cp, s):
    a, b = map(set, hs)
    leaves, cycle, marks = {0, 1}, {2, 3, 4, 5, 6}, set(ones)
    c = len(a & b)
    if marks == leaves:
        require((p, cp, c, s[0][1]) == (0, 0, 3, 0), "leaf-pair shape differs")
        require(a & cycle == b & cycle and len(a & leaves) == len(b & leaves) == 1
                and a & leaves != b & leaves, "leaf-marked rows differ")
        shared = a & b
        require(shared <= cycle and len(shared) == 3, "three common cycle points required")
        pair_supply = [s[x][y] for x, y in combinations(sorted(shared), 2)]
        require(pair_supply == [2] * 3, "shared triple not saturated")
        required_neighbor_load = sum(2 + len(N[x] & shared) for x in shared)
        require(required_neighbor_load > 6, "leaf-marked neighbor load is feasible")
        return ["leaves", 6, required_neighbor_load]
    require(marks <= cycle and leaves <= a and leaves <= b and s[0][1] == 2,
            "cycle-marked rows must both fill leaf pair")
    adjacent = ones[1] in N[ones[0]]
    if adjacent:
        require((p, c) == (0, 2) and not (a & b & cycle), "adjacent marks shape differs")
    else:
        require((p, c) == (1, 4) and a == b == leaves | marks, "nonadjacent marks shape differs")
    # The ordinary rows have eight leaf incidences in total, at most one
    # per row, so exactly four of them lie wholly on the cycle.
    cycle_only = 12 - ((6 - 2) + (6 - 2))
    require(cycle_only == 4, "cycle-only count")
    # A blue H-neighborhood has 6-p ordinary rows. Its leaf demand after
    # subtracting the other H is >=6-2p. At most p are cycle-only.
    mark_budget = 2 * ((6 - p) - (6 - 2 * p))
    pair_lower = 3 * cycle_only - 2 * mark_budget
    unmarked = cycle - marks
    literal_limits = []
    for x, y in combinations(sorted(unmarked), 2):
        limit = (3 - 1 - len(N[x] & N[y]) if y in N[x]
                 else 6 - len(BLUE[x] & BLUE[y]) - (14 - 6 - 6))
        literal_limits.append(limit)
        require(0 <= s[x][y] <= limit == 2, "unmarked pair limit differs")
    require(pair_lower > sum(literal_limits), "cycle-only pair budget is feasible")
    return ["adjacent_cycle" if adjacent else "nonadjacent_cycle", sum(literal_limits), pair_lower]


def reduction():
    tables = positive_table()
    raw, signed, keep, certs = [], [], [], []
    scalar_counts, filters, shapes = Counter(), Counter(), Counter()
    for ones in combinations(range(7), 2):
        columns = [6 + int(b in ones) for b in range(7)]
        weight = sum(H[b] for b in ones)
        capacities = [[0] * 7 for _ in range(7)]
        for i in range(7):
            capacities[i][i] = columns[i]
        for x, y in PAIRS:
            value = (3 - 1 - len(N[x] & N[y]) if y in N[x]
                     else 6 - len(BLUE[x] & BLUE[y]) - (14 - columns[x] - columns[y]))
            capacities[x][y] = capacities[y][x] = value
        for vector in defect_vectors(6 - weight):
            defect = [j for j, amount in enumerate(vector) for _ in range(amount)]
            s = [v[:] for v in capacities]
            for (x, y), amount in zip(PAIRS, vector):
                s[x][y] -= amount
                s[y][x] -= amount
            loads = tuple(sum(s[b]) - 3 * columns[b] for b in range(7))
            if any(not 0 <= s[x][y] <= min(columns[x], columns[y]) for x, y in PAIRS):
                status = "intersection_range"
            elif any(v not in (0, 1, 2) for v in loads):
                status = "row_bounds"
            elif sum(v * v for v in loads) != 4 + 5 * (loads[ones[0]] + loads[ones[1]]) - 2 * s[ones[0]][ones[1]]:
                status = "moment"
            else:
                status = "survive"
            scalar_counts[status] += 1
            raw.append([list(ones), defect, status])
            if status != "survive":
                continue
            for hs in tables.get(loads, ()):
                if any(s[x][y] < sum(x in q and y in q for q in hs)
                       for x in range(7) for y in range(7)):
                    continue
                record = [list(ones), 0, defect, [], [list(q) for q in hs]]
                signed.append(record)
                marks = [len(set(ones) & set(q)) for q in hs]
                if not marks[0] == marks[1] or marks[0] not in (1, 2):
                    filters["positive_sigma_equation"] += 1
                    continue
                p = marks[0] - 1
                cp = 3 + 3 * p - len(set(hs[0]) & set(hs[1]))
                if cp not in range(7 - p):
                    filters["positive_pair_codegree"] += 1
                    continue
                admissible = True
                for q, mark_load in zip(hs, marks):
                    # Direct unsimplified substitution: Pw=6+p+cp,
                    # |H intersect W|=mark_load. The full row budget is
                    # 16+p-mark_load-2Mh before using mark_load=1+p.
                    marked_defect = 6 + p + cp + weight - 4
                    marked_defect -= sum(H[b] for b in q if b in ones) + mark_load
                    marked_defect -= sum(len(N[b] & set(ones)) for b in q)
                    row_budget = 16 + p - mark_load - 2 * sum(H[b] for b in q)
                    admissible &= marked_defect >= 0 and row_budget - marked_defect >= 0
                if not admissible:
                    filters["marked_cross_defects"] += 1
                    continue
                filters["survive"] += 1
                keep.append(record)
                certificate = analyze_shapes(ones, hs, p, cp, s)
                certs.append([record, certificate])
                shapes[certificate[0]] += 1
    return {"raw_states": len(raw), "scalar_counts": dict(sorted(scalar_counts.items())),
            "raw_states_sha256": fingerprint(raw), "signed_configurations": len(signed),
            "signed_sha256": fingerprint(signed), "filter_counts": dict(sorted(filters.items())),
            "shapes": dict(sorted(shapes.items())), "survivors_sha256": fingerprint(keep),
            "counting_certificates_sha256": fingerprint(certs), "excluded_configurations": len(keep)}, {
                "signed": sorted(signed), "survivors": sorted(keep), "certificates": sorted(certs)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-records", type=Path,
                        help="compare every record with a main-checker private stream")
    args = parser.parse_args()
    actual, records = reduction()
    expected = json.loads(Path(__file__).with_name("degree106_p2c5_expected.json").read_text())
    require(actual == expected["reduction"], "separate exact reduction differs")
    if args.compare_records:
        require(records == json.loads(args.compare_records.read_text()), "complete record streams differ")
    print(json.dumps({"agent": "six-books-1", "role": "researcher",
                      "status": "separate necessary-state and counting checks passed",
                      "entry_by_entry_comparison": bool(args.compare_records),
                      "reduction": actual}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
