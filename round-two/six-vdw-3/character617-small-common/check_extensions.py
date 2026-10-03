"""Distinct physical missing-pattern census and coefficient check; no producer imports."""
import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quads", type=Path, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.quads.read_text())
    quads = data["records"]
    if len(quads) != 64108 or hashlib.sha256(json.dumps(quads, sort_keys=True,
            separators=(",", ":")).encode()).hexdigest() != data["records_sha256"]:
        raise ValueError("Checked physical quadruple corpus")
    if not 0 <= args.start < args.stop <= len(quads):
        raise ValueError("Exact extension range")
    square = {n * n % 617 for n in range(1, 617)}
    rows = sorted(square)
    columns = [n for n in range(1, 617) if n not in square]
    inv = {q: next(b for b in range(1, 617) if q * b % 617 == 1)
           for q in range(1, 617)}
    support = set()
    for delta in (285, 314, 362, 381, 409, 570):
        x = 1
        for _ in range(6):
            x = (x + delta) % 617
            support.add(x)
    ratios = support | {inv[t] for t in support}
    masks = {q: sum(1 << j for j, t in enumerate(columns) if t * inv[q] % 617 in ratios)
             for q in rows}
    if len(support) != 33 or len(ratios) != 66 or any(m.bit_count() != 66 for m in masks.values()):
        raise ValueError("Literal endpoint graph")

    def actual(mask):
        return [t for j, t in enumerate(columns) if mask >> j & 1]

    histogram = collections.Counter()
    presentations = 0
    records = {}
    all_counts = list(itertools.product(range(3), repeat=5))
    for r in quads[args.start:args.stop]:
        a = r["A"]
        groups = [0] * 16
        for j, t in enumerate(columns):
            missing = sum(1 << i for i, q in enumerate(a) if not (masks[q] >> j & 1))
            groups[missing] |= 1 << j
        if actual(groups[0]) != r["C"]:
            raise ValueError("Literal whole quad common neighborhood")
        for q in rows:
            if q in a:
                continue
            nq = masks[q]
            c_mask = groups[0] & nq
            c = c_mask.bit_count()
            histogram[c] += 1
            if c not in (2, 3):
                continue
            singleton_masks = [groups[1 << i] & nq for i in range(4)] + [groups[0] & ~nq]
            if sum(min(2, m.bit_count()) for m in singleton_masks) < 8:
                continue
            presentations += 1
            unordered = [*a, q]
            full = sorted(unordered)
            position = [full.index(x) for x in unordered]
            singletons = [None] * 5
            for i, m in enumerate(singleton_masks):
                singletons[position[i]] = actual(m)
            doubles = {}
            for i, j in itertools.combinations(range(5), 2):
                m = groups[(1 << i) | (1 << j)] & nq if j < 4 else groups[1 << i] & ~nq
                ii, jj = sorted((position[i], position[j]))
                doubles[ii, jj] = actual(m)
            u = [len(s) for s in singletons]
            p10 = p9_single = p9_double = 0
            # Enumerate all bounded singleton occupancy vectors. The physical
            # coefficient is the product of choose(u_i, n_i); optional one
            # double column must fit both remaining row capacities.
            for counts in all_counts:
                total = sum(counts)
                if total not in (8, 9, 10) or any(n > limit for n, limit in zip(counts, u)):
                    continue
                ways = math.prod(math.comb(limit, n) for n, limit in zip(counts, u))
                if total == 10:
                    p10 += ways
                elif total == 9:
                    p9_single += ways
                else:
                    for (i, j), ts in doubles.items():
                        if counts[i] < 2 and counts[j] < 2:
                            p9_double += ways * len(ts)
            record = {"A": full, "C": actual(c_mask), "singleton": singletons,
                      "double": [[i, j, ts] for (i, j), ts in sorted(doubles.items())],
                      "p10": p10, "p9_single": p9_single, "p9_double": p9_double}
            if records.setdefault(tuple(full), record) != record:
                raise ValueError("Literal presentations disagree")
    result = {"schema": "character617-small-common-extension-part-v1",
              "start": args.start, "stop": args.stop,
              "quad_records_sha256": data["records_sha256"],
              "raw_trials": sum(histogram.values()), "common_histogram": sorted(histogram.items()),
              "capacity_presentations": presentations,
              "records": [r for _, r in sorted(records.items())]}
    if result["raw_trials"] != 304 * (args.stop - args.start):
        raise ValueError("All304 fifth-row extensions per quadruple")
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
