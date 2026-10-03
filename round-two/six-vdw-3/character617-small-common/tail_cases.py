"""Enumerate the entire weighted physical column domain and bitwise tail gate."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ("prefixes", "canonical", "output"):
        p.add_argument("--" + flag, type=Path, required=True)
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--stop", type=int, required=True)
    o = p.parse_args()
    parent = json.loads(o.prefixes.read_text())
    canonical = json.loads(o.canonical.read_text())
    lookup = {tuple(r["A"]): r for r in parent["records"]}
    cases = []
    offset = 0
    for r in canonical["records"]:
        for c in r["choices"]:
            n = sum(c["coefficients"][:c["allowed_prefix_bad_budget"] + 1])
            cases.append((r["A"], c, offset, offset + n))
            offset += n
    if offset != 21247 or not 0 <= o.start < o.stop <= offset:
        raise ValueError("Entire21247 canonical physical incidence domain")
    rows = [q for q in range(1, 617) if pow(q, 308, 617) == 1]
    v = {(1 + j * d) % 617 for d in (285, 314, 362, 381, 409, 570) for j in range(1, 7)}
    ratios = v | {pow(t, -1, 617) for t in v}
    vb = {192, 239, 286, 336, 383, 430}
    db = vb | {pow(t, -1, 617) for t in vb}
    if len(rows) != 308 or len(v) != 33 or len(ratios) != 66 or len(db) != 12 or v & {pow(t, -1, 617) for t in v}:
        raise ValueError("Literal1+j*delta ratio graph convention")
    adjacent = {q: sum(1 << (q * t % 617) for t in ratios) for q in rows}
    bad = {q: sum(1 << (q * t % 617) for t in db) for q in rows}
    results = []
    for case_id, (a, c, start, stop) in enumerate(cases):
        if stop <= o.start or start >= o.stop:
            continue
        r = lookup[tuple(a)]
        def cost(t):
            return sum(bad[q] >> t & 1 for q in a)
        budget = c["allowed_prefix_bad_budget"]
        common_cost = sum(cost(t) for t in c["B0"])
        remaining_budget = budget - common_cost
        if remaining_budget < 0:
            raise ValueError("Positive weighted coefficient with too-costly common subset")
        subsets = []

        def visit(groups, i, used, total_cost):
            if i == len(groups):
                subsets.append(tuple(sorted((*c["B0"], *used))))
                return
            for ts, w in groups[i]:
                if total_cost + w <= remaining_budget:
                    visit(groups, i + 1, (*used, *ts), total_cost + w)

        def group(ts, cardinality):
            return [(tuple(choice), sum(cost(t) for t in choice))
                    for choice in itertools.combinations(ts, cardinality)
                    if sum(cost(t) for t in choice) <= remaining_budget]

        if c["outside"] == "ten_singleton":
            visit([group(ts, 2) for ts in r["singleton"]], 0, (), 0)
        elif c["outside"] == "nine_singleton":
            for short in range(5):
                visit([group(ts, 1 if i == short else 2) for i, ts in enumerate(r["singleton"])], 0, (), 0)
        elif c["outside"] == "nine_one_double":
            for i, j, ts in r["double"]:
                groups = [group(uu, 1 if k in (i, j) else 2) for k, uu in enumerate(r["singleton"])]
                visit([group(ts, 1), *groups], 0, (), 0)
        else:
            raise ValueError("Closed physical coefficient case")
        subsets.sort()
        if len(subsets) != stop - start or len(set(subsets)) != len(subsets):
            raise ValueError("Actual unique weighted column count differs from independent coefficient")
        for rank in range(max(0, o.start - start), min(len(subsets), o.stop - start)):
            b = subsets[rank]
            bmask = sum(1 << t for t in b)
            prefix_bad = sum(cost(t) for t in b)
            deficit = 9 if c["outside"] == "nine_singleton" else 10
            tail2 = []
            tail3_good = []
            for q in rows:
                if q in a:
                    continue
                d = (bmask & ~adjacent[q]).bit_count()
                if d in (2, 3):
                    bad_count = (bmask & bad[q]).bit_count()
                    if d == 2:
                        tail2.append([q, bad_count])
                    elif bad_count == 0:
                        tail3_good.append(q)
            good2 = sum(w == 0 for _, w in tail2)
            near_applicable = c["balance"] == [11, 13] or deficit == 9
            needed = 6 if c["balance"] == [11, 13] else 7
            near_min_bad = sum(sorted(w for _, w in tail2)[:needed]) if near_applicable and len(tail2) >= needed else None
            near = near_applicable and near_min_bad is not None and prefix_bad + near_min_bad <= 2
            tight = prefix_bad == 0 and (good2 >= needed - 1 and bool(tail3_good)
                     if near_applicable else good2 >= 7)
            results.append({"global_index": start + rank, "case_id": case_id, "rank": rank,
                            "B": list(b), "prefix_bad": prefix_bad, "prefix_deficit": deficit,
                            "tail2": tail2, "tail3_good": tail3_good, "near_min_bad": near_min_bad,
                            "near_pass": bool(near), "tight_pass": bool(tight), "tail_gate_pass": bool(near or tight)})
    if len(results) != o.stop - o.start or [r["global_index"] for r in results] != list(range(o.start, o.stop)):
        raise ValueError("Whole disjoint physical incidence rank range omitted")
    result = {"schema": "character617-physical-tail-part-v1", "start": o.start, "stop": o.stop,
              "canonical_records_sha256": canonical["records_sha256"], "physical_domain": 21247,
              "survivors": sum(r["tail_gate_pass"] for r in results), "records": results}
    o.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
