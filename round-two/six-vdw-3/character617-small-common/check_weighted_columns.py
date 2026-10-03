"""Literal physical-column occupancy DP for weighted prefix coefficients."""
import argparse
import collections
import itertools
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefixes", type=Path, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    opt = parser.parse_args()
    corpus = json.loads(opt.prefixes.read_text())
    records = corpus["records"]
    if not 0 <= opt.start < opt.stop <= len(records):
        raise ValueError("Complete selected prefix range")
    square = {x * x % 617 for x in range(1, 617)}
    columns = [t for t in range(1, 617) if t not in square]
    v = set()
    for d in (285, 314, 362, 381, 409, 570):
        x = 1
        for _ in range(6):
            x = (x + d) % 617
            v.add(x)
    inv = {t: next(x for x in range(1, 617) if t * x % 617 == 1) for t in range(1, 617)}
    dset = v | {inv[t] for t in v}
    vbad = {192, 239, 286, 336, 383, 430}
    dbad = vbad | {inv[t] for t in vbad}
    adjacent = {q: {q * t % 617 for t in dset} for q in square}
    bad = {q: {q * t % 617 for t in dbad} for q in square}
    result_records = []
    totals = collections.Counter()

    def factor(ts, cost):
        table = [[0] * 3 for _ in range(3)]
        table[0][0] = 1
        for t in ts:
            w = cost(t)
            if w > 2:
                continue
            for cardinality in (2, 1):
                for budget in range(2, w - 1, -1):
                    table[cardinality][budget] += table[cardinality - 1][budget - w]
        return table

    def combine(factors):
        distribution = {0: 1}
        for p in factors:
            next_distribution = collections.Counter()
            for old_cost, old_count in distribution.items():
                for new_cost, new_count in enumerate(p):
                    if new_count and old_cost + new_cost <= 2:
                        next_distribution[old_cost + new_cost] += old_count * new_count
            distribution = dict(next_distribution)
        return [distribution.get(w, 0) for w in range(3)]

    for r in records[opt.start:opt.stop]:
        c = len(r["C"])
        if not r["p10"] and (c == 2 or not r["p9_single"] + r["p9_double"]):
            continue
        a = r["A"]
        actual_c = []
        actual_u = [[] for _ in range(5)]
        actual_v = {(i, j): [] for i, j in itertools.combinations(range(5), 2)}
        for t in columns:
            missing = tuple(i for i, q in enumerate(a) if t not in adjacent[q])
            if not missing:
                actual_c.append(t)
            elif len(missing) == 1:
                actual_u[missing[0]].append(t)
            elif len(missing) == 2:
                actual_v[missing].append(t)
        if actual_c != r["C"] or actual_u != r["singleton"] or \
                [[i, j, ts] for (i, j), ts in actual_v.items()] != r["double"]:
            raise ValueError("Whole physical parent prefix column types differ")
        def cost(t):
            return sum(t in bad[q] for q in a)
        factors = [factor(ts, cost) for ts in actual_u]
        f10 = combine([f[2] for f in factors])
        f9s = [0, 0, 0]
        for short in range(5):
            term = combine([f[1 if i == short else 2] for i, f in enumerate(factors)])
            f9s = [x + y for x, y in zip(f9s, term)]
        f9d = [0, 0, 0]
        for (i, j), ts in actual_v.items():
            term = combine([f[1 if k in (i, j) else 2] for k, f in enumerate(factors)] +
                           [factor(ts, cost)[1]])
            f9d = [x + y for x, y in zip(f9d, term)]
        choices = []

        def emit(balance, b0, outside, budget, poly, key):
            common_cost = sum(cost(t) for t in b0)
            vector = [poly[w - common_cost] if w >= common_cost else 0 for w in range(3)]
            totals[key] += sum(vector[:budget + 1])
            if sum(vector[:budget + 1]):
                choices.append({"balance": balance, "B0": b0, "outside": outside,
                                "allowed_prefix_bad_budget": budget, "coefficients": vector})
        if c == 2:
            emit([12, 12], r["C"], "ten_singleton", 0, f10, "12/12:c2,s2,k10")
        elif c == 3:
            emit([11, 13], r["C"], "ten_singleton", 2, f10, "11/13:c3,s3,k10")
            for b0 in itertools.combinations(r["C"], 2):
                emit([12, 12], list(b0), "ten_singleton", 0, f10, "12/12:c3,s2,k10")
            emit([12, 12], r["C"], "nine_singleton", 2, f9s, "12/12:c3,s3,k9,single")
            emit([12, 12], r["C"], "nine_one_double", 0, f9d, "12/12:c3,s3,k9,double")
        else:
            raise ValueError("Small-common scope")
        if choices:
            result_records.append({"A": a, "choices": choices})
    result = {"schema": "character617-weighted-prefix-column-part-v1", "start": opt.start,
              "stop": opt.stop, "prefix_records_sha256": corpus["records_sha256"],
              "incidences": dict(sorted(totals.items())), "records": result_records}
    opt.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
