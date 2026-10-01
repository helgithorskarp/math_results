"""Independent type-count method; no generator imports. Same stated author.

Uses a partition multinomial and counts W supports by intersection size.
Written proof bridges remain analytic; these are not valid-host counts.
"""
from copy import deepcopy
from math import comb, factorial
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def reconstruct():
    rows = []
    for p in (1, 2):
        for q in (1, 2):
            for r in (0, 1, 2):
                cells = (r, 5 - p - r, 5 - q - r, p + q + r - 2)
                require(sum(cells) == 8 and min(cells) >= 0, "Z partition")
                z_count = factorial(8)
                for n in cells:
                    z_count //= factorial(n)
                for c in (0, 1, 2):
                    w_count = choose(2, p) * choose(p, c) * choose(2 - p, q - c)
                    if not w_count:
                        continue
                    available = p + q + r - c
                    require(available <= r + 2, "union lower bound")
                    if r == 2:
                        require(available <= 4 and 6 - available >= 2, "triple intersection lower bound")
                    if r == 1 and available == 3:
                        require(p + q - c == 2, "W coverage equality")
                        require(choose(available, 3) == 1, "unique neighbor triple")
                    rows.append([p, q, r, c, available, z_count * w_count])
    rows.sort()
    choices = choose(8, 4) * choose(2, 1) + choose(8, 3)
    # Triples are four-point sets with exactly one omitted point.
    histogram = {"2": sum(i != j for i in range(4) for j in range(4)),
                 "3": sum(i == j for i in range(4) for j in range(4))}
    return {"five_set_choices": choices, "ordered_input_pairs": choices ** 2,
            "type_records": rows, "parent_retained_pairs": sum(row[-1] for row in rows),
            "overlap_two_excluded": sum(row[-1] for row in rows if row[2] == 2),
            "overlap_one_equality_excluded": sum(row[-1] for row in rows if row[2] == 1 and row[4] < 3),
            "retained_templates": sum(row[-1] for row in rows if row[2] == 0 or (row[2] == 1 and row[4] == 3)),
            "four_point_triple_intersections": histogram}


def validate(record, expected):
    require(record == expected, "all compact type/count entries")
    require(record["parent_retained_pairs"] == record["overlap_two_excluded"]
            + record["overlap_one_equality_excluded"] + record["retained_templates"], "count partition")
    require(record["four_point_triple_intersections"] == {"2": 12, "3": 4}, "literal triple intersections")


def main():
    raw = (HERE / "expected.json").read_bytes()
    record = json.loads(raw)
    expected = reconstruct()
    validate(record, expected)
    bad = []
    for key in ("parent_retained_pairs", "overlap_two_excluded", "retained_templates"):
        damaged = deepcopy(record)
        damaged[key] += 1
        bad.append(damaged)
    damaged = deepcopy(record)
    damaged["type_records"][0][-1] += 1
    bad.append(damaged)
    damaged = deepcopy(record)
    damaged["four_point_triple_intersections"]["2"] -= 1
    bad.append(damaged)
    for damaged in bad:
        try:
            validate(damaged, expected)
        except ValueError:
            continue
        raise ValueError("corrupted type record accepted")
    print(json.dumps({"status": "PASS", "retained_templates": record["retained_templates"],
                      "rejected_forged_records": len(bad), "type_records": len(record["type_records"]),
                      "expected_sha256": hashlib.sha256(raw).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
