"""Exact prefix-column incidence coefficients with0..2 bad endpoint edges."""
import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path


def multiply(a, b):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(3)]


def product(polys):
    result = [1, 0, 0]
    for p in polys:
        result = multiply(result, p)
    return result


def shift(poly, cost):
    return [poly[k - cost] if k >= cost else 0 for k in range(3)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefixes", type=Path, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    corpus = json.loads(options.prefixes.read_text())
    records = corpus["records"]
    if not 0 <= options.start < options.stop <= len(records):
        raise ValueError("Exact physical prefix range")
    vbad = {192, 239, 286, 336, 383, 430}
    dbad = vbad | {pow(t, -1, 617) for t in vbad}
    if len(dbad) != 12:
        raise ValueError("Published bad-ratio split")
    output = []
    totals = collections.Counter()
    for r in records[options.start:options.stop]:
        c = len(r["C"])
        if not r["p10"] and (c == 2 or not r["p9_single"] + r["p9_double"]):
            continue
        a = r["A"]
        iq = [pow(q, -1, 617) for q in a]
        def cost(t):
            return sum(t * z % 617 in dbad for z in iq)
        linear = []
        pairs = []
        for ts in r["singleton"]:
            n = collections.Counter(cost(t) for t in ts)
            linear.append([n[0], n[1], n[2]])
            pairs.append([math.comb(n[0], 2), n[0] * n[1],
                          n[0] * n[2] + math.comb(n[1], 2)])
        f10 = product(pairs)
        f9s = [0, 0, 0]
        for i in range(5):
            term = product([linear[i]] + [pairs[j] for j in range(5) if j != i])
            f9s = [x + y for x, y in zip(f9s, term)]
        f9d = [0, 0, 0]
        for i, j, ts in r["double"]:
            n = collections.Counter(cost(t) for t in ts)
            term = product([[n[0], n[1], n[2]], linear[i], linear[j]] +
                           [pairs[k] for k in range(5) if k not in (i, j)])
            f9d = [x + y for x, y in zip(f9d, term)]
        choices = []
        if c == 2:
            b0 = r["C"]
            vector = shift(f10, sum(cost(t) for t in b0))
            choices.append({"balance": [12, 12], "B0": b0, "outside": "ten_singleton",
                            "allowed_prefix_bad_budget": 0, "coefficients": vector})
            totals["12/12:c2,s2,k10"] += vector[0]
        elif c == 3:
            b0 = r["C"]
            cc = sum(cost(t) for t in b0)
            vector = shift(f10, cc)
            choices.append({"balance": [11, 13], "B0": b0, "outside": "ten_singleton",
                            "allowed_prefix_bad_budget": 2, "coefficients": vector})
            totals["11/13:c3,s3,k10"] += sum(vector)
            for b0_tuple in itertools.combinations(r["C"], 2):
                b0 = list(b0_tuple)
                vector = shift(f10, sum(cost(t) for t in b0))
                choices.append({"balance": [12, 12], "B0": b0, "outside": "ten_singleton",
                                "allowed_prefix_bad_budget": 0, "coefficients": vector})
                totals["12/12:c3,s2,k10"] += vector[0]
            for name, f9, budget in (("nine_singleton", f9s, 2), ("nine_one_double", f9d, 0)):
                vector = shift(f9, cc)
                choices.append({"balance": [12, 12], "B0": r["C"], "outside": name,
                                "allowed_prefix_bad_budget": budget, "coefficients": vector})
                totals["12/12:c3,s3,k9," + ("single" if budget else "double")] += sum(vector[:budget + 1])
        else:
            raise ValueError("Small whole common scope")
        useful = [s for s in choices if sum(s["coefficients"][:s["allowed_prefix_bad_budget"] + 1])]
        if useful:
            output.append({"A": a, "choices": useful})
    result = {"schema": "character617-weighted-prefix-column-part-v1",
              "start": options.start, "stop": options.stop,
              "prefix_records_sha256": corpus["records_sha256"],
              "incidences": dict(sorted(totals.items())), "records": output}
    options.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
