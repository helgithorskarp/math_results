#!/usr/bin/env python3
"""Separate author implementation of the signed-column certificates.

Uses the earlier separate literal-capacity/table checker; imports no main
generator or signed-column generator. The expanded column identity is
evaluated before cancellation, and full records can be compared.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

from degree106_independent import PAIRS, positive_table, require, screen

FORMS = (
    ("P7", {(i, i + 1) for i in range(6)}, 2),
    ("P3+C4", {(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (3, 6)}, 1),
    ("P2+C5", {(0, 1), (2, 3), (3, 4), (4, 5), (5, 6), (2, 6)}, 0),
)


def fingerprint(records):
    return sha256(json.dumps(sorted(records), separators=(",", ":")).encode()).hexdigest()


def check_form(name, edges, bound):
    neighbors = [{j for j in range(7) if i != j and (min(i, j), max(i, j)) in edges}
                 for i in range(7)]
    h = list(map(len, neighbors))
    tables = {a: positive_table(h, a + 2) for a in range(bound + 1)}
    negative = [t for t in combinations(range(7), 2) if sum(h[b] for b in t) <= 3]
    counts, by_a, margins = Counter(), Counter(), Counter()
    raw, records, certificates = [], [], []
    for ones in combinations(range(7), 2):
        weight = sum(h[b] for b in ones)
        for a in range(bound + 1):
            for defect in combinations_with_replacement(range(21), 6 - weight - a):
                status, data = screen(edges, ones, a, defect)
                counts[status] += 1
                raw.append([list(ones), a, list(defect), status])
                if data is None:
                    continue
                _, s, u, q = data
                for ts in combinations_with_replacement(negative, a):
                    negative_load = [sum(b in row for row in ts) for b in range(7)]
                    if sum(negative_load[b] for b in ones) != q:
                        continue
                    positive_load = tuple(u[b] + negative_load[b] for b in range(7))
                    for hs in tables[a].get(positive_load, ()):
                        if any(s[b][z] < sum(b in row and z in row for row in ts + hs)
                               for b in range(7) for z in range(7)):
                            continue
                        record = [list(ones), a, list(defect), [list(row) for row in ts],
                                  [list(row) for row in hs]]
                        v = [positive_load[b] + negative_load[b] for b in range(7)]
                        # Do not reuse the main's cancelled formula. Start
                        # with r^T(PM), r^T(ML), r^T(h+k-6), and the
                        # coefficient of r*M, in that order.
                        d = []
                        for b in range(7):
                            value = sum(s[b][z] for z in ones) - u[b]
                            value -= sum(u[z] for z in neighbors[b])
                            value += 2 * h[b] + (2 * a + 2) - 3 * 2
                            value += (1 - h[b] - int(b in ones)) * u[b] - v[b]
                            d.append(value)
                        negative_budget = sum(2 * 6 - 21 + 10 * 2 - 2 ** 2
                                              - 2 * sum(h[b] for b in row) for row in ts)
                        forced = sum(-value for value in d if value < 0)
                        require(forced > negative_budget >= 0, "a signed-column certificate failed")
                        records.append(record)
                        certificates.append([record, d, negative_budget, forced])
                        margins[forced - negative_budget] += 1
                        by_a[a] += 1
    return {"name": name, "raw_states": len(raw), "state_counts": dict(sorted(counts.items())),
            "states_sha256": fingerprint(raw), "signed_configurations": len(records),
            "configurations_by_a": dict(sorted(by_a.items())), "signed_sha256": fingerprint(records),
            "strict_margin_histogram": dict(sorted(margins.items())),
            "certificates_sha256": fingerprint(certificates), "survivors": 0}, {
                "name": name, "configurations": sorted(records), "certificates": sorted(certificates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compare-records", type=Path, help="optional complete entry comparison")
    args = parser.parse_args()
    forms, records = [], []
    for name, edges, bound in FORMS:
        result, entries = check_form(name, edges, bound)
        forms.append(result)
        records.append(entries)
    expected = json.loads(Path(__file__).with_name("degree106_columns_expected.json").read_text())
    require(json.loads(json.dumps(forms)) == expected["forms"], "separate signed-column domains differ")
    if args.compare_records:
        require(records == json.loads(args.compare_records.read_text()), "complete certificate entries differ")
    print(json.dumps({"agent": "six-books-1", "role": "researcher",
                      "status": "all 6446 signed-column certificates passed",
                      "entry_by_entry_comparison": bool(args.compare_records),
                      "forms": forms}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
