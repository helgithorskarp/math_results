"""Literal graph membership, physical cardinality and all308-row tail checking."""
import argparse
import collections
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for flag in ("input", "canonical", "output"):
        p.add_argument("--" + flag, type=Path, required=True)
    o = p.parse_args()
    d = json.loads(o.input.read_text())
    canonical = json.loads(o.canonical.read_text())
    squares = {q * q % 617 for q in range(1, 617)}
    rows = sorted(squares)
    columns = {t for t in range(1, 617) if t not in squares}
    inv = {q: next(z for z in range(1, 617) if q * z % 617 == 1) for q in rows}
    positive = set()
    for step in (285, 314, 362, 381, 409, 570):
        q = 1
        for _ in range(6):
            q = (q + step) % 617
            positive.add(q)
    inverse_positive = {next(z for z in range(1, 617) if z * t % 617 == 1) for t in positive}
    ratios = positive | inverse_positive
    vb = {192, 239, 286, 336, 383, 430}
    db = vb | {next(z for z in range(1, 617) if z * t % 617 == 1) for t in vb}
    if len(rows) != 308 or len(positive) != 33 or len(ratios) != 66 or len(db) != 12 or positive & inverse_positive:
        raise ValueError("Literal six-step field ratio graph")
    cases = []
    cursor = 0
    for r in canonical["records"]:
        for c in r["choices"]:
            size = sum(c["coefficients"][:c["allowed_prefix_bad_budget"] + 1])
            cases.append((r["A"], c, cursor, cursor + size))
            cursor += size
    if cursor != 21247 or d["physical_domain"] != cursor or d["canonical_records_sha256"] != canonical["records_sha256"]:
        raise ValueError("Complete independently established weighted physical cardinality")
    expected = []
    previous_case = None
    previous_b = None
    for global_index, r in enumerate(d["records"], d["start"]):
        if r["global_index"] != global_index or not d["start"] <= global_index < d["stop"]:
            raise ValueError("Incidence rank range")
        case_id = r["case_id"]
        if not isinstance(case_id, int) or not 0 <= case_id < len(cases):
            raise ValueError("Physical case label outside complete canonical registry")
        a, c, start, stop = cases[case_id]
        if not start <= global_index < stop or r["rank"] != global_index - start:
            raise ValueError("Case cardinality interval")
        b = r["B"]
        if b != sorted(set(b)) or not set(b) <= columns or len(b) != c["balance"][1]:
            raise ValueError("Actual unique nonsquare column set")
        if previous_case == case_id and not tuple(previous_b) < tuple(b):
            raise ValueError("Physical column duplicates or unsorted ranks")
        previous_case, previous_b = case_id, b
        common = {t for t in columns if all(t * inv[q] % 617 in ratios for q in a)}
        if set(b) & common != set(c["B0"]):
            raise ValueError("Outside ENTIRE physical common set")
        misses = [sum(t * inv[q] % 617 not in ratios for t in b) for q in a]
        outside_patterns = [sum(t * inv[q] % 617 not in ratios for q in a) for t in b if t not in common]
        kind = c["outside"]
        if kind == "ten_singleton":
            valid = misses == [2] * 5 and outside_patterns == [1] * 10
        elif kind == "nine_singleton":
            valid = sorted(misses) == [1, 2, 2, 2, 2] and outside_patterns == [1] * 9
        elif kind == "nine_one_double":
            valid = misses == [2] * 5 and sorted(outside_patterns) == [1] * 8 + [2]
        else:
            raise ValueError("Unknown physical coefficient case")
        if not valid:
            raise ValueError("Physical coefficient pattern or row capacities")
        prefix_bad = sum(t * inv[q] % 617 in db for q in a for t in b)
        if prefix_bad > c["allowed_prefix_bad_budget"]:
            raise ValueError("Weighted prefix budget")
        tail2, tail3 = [], []
        histogram = collections.Counter()
        for q in rows:
            if q in a:
                continue
            missing = sum(t * inv[q] % 617 not in ratios for t in b)
            bad_count = sum(t * inv[q] % 617 in db for t in b)
            if missing == 2:
                tail2.append([q, bad_count]);histogram[bad_count] += 1
            elif missing == 3 and bad_count == 0:
                tail3.append(q)
        deficit = sum(misses)
        needed = 6 if c["balance"] == [11, 13] else 7
        near_applicable = c["balance"] == [11, 13] or deficit == 9
        if near_applicable and len(tail2) >= needed:
            left, minimum = needed, 0
            for cost in sorted(histogram):
                take = min(left, histogram[cost]);minimum += take * cost;left -= take
                if left == 0:
                    break
            near_min_bad = minimum
        else:
            near_min_bad = None
        near = near_applicable and near_min_bad is not None and prefix_bad + near_min_bad <= 2
        tight = prefix_bad == 0 and (histogram[0] >= needed - 1 and bool(tail3)
                 if near_applicable else histogram[0] >= 7)
        computed = {"global_index": global_index, "case_id": case_id, "rank": global_index - start,
                    "B": b, "prefix_bad": prefix_bad, "prefix_deficit": deficit, "tail2": tail2,
                    "tail3_good": tail3, "near_min_bad": near_min_bad,
                    "near_pass": bool(near), "tight_pass": bool(tight), "tail_gate_pass": bool(near or tight)}
        if computed != r:
            raise ValueError("Literal whole tail computation differs")
        expected.append(computed)
    if len(expected) != d["stop"] - d["start"] or not 0 <= d["start"] < d["stop"] <= 21247:
        raise ValueError("Incomplete bounded physical incidence domain")
    result = {"schema": "character617-physical-tail-part-v1", "start": d["start"], "stop": d["stop"],
              "canonical_records_sha256": canonical["records_sha256"], "physical_domain": 21247,
              "survivors": sum(r["tail_gate_pass"] for r in expected), "records": expected}
    o.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
