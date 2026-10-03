"""Prove complete unique physical selection coverage and merge exact tail tests."""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("producer", "checker", "optimized", "canonical", "output"):
        p.add_argument("--" + name, required=True, type=Path)
    o = p.parse_args()
    canonical = json.loads(o.canonical.read_text())
    cases = []
    offset = 0
    for prefix in canonical["records"]:
        for choice in prefix["choices"]:
            count = sum(choice["coefficients"][:choice["allowed_prefix_bad_budget"] + 1])
            cases.append({"A": prefix["A"], "choice": choice, "start": offset, "stop": offset + count})
            offset += count
    if offset != 21247 or len(cases) != 542:
        raise ValueError("Complete independently counted weighted selection registry")
    names = sorted(q.name for q in o.producer.glob("range-*.json"))
    if not names or any(names != sorted(q.name for q in directory.glob("range-*.json"))
                        for directory in (o.checker, o.optimized)):
        raise ValueError("Whole physical part domains differ")
    cursor = 0
    counts = collections.Counter()
    by_balance = collections.Counter()
    survivors_by_balance = collections.Counter()
    maximum_tail2 = collections.Counter()
    maximum_good_tail2 = collections.Counter()
    previous_case, previous_b = None, None
    survivors = []
    digest = hashlib.sha256()
    part_pins = {}
    for name in names:
        raw = (o.producer / name).read_bytes()
        if any(raw != (directory / name).read_bytes() for directory in (o.checker, o.optimized)):
            raise ValueError("Entire producer/literal-normal/literal-optimized transcript differs")
        part_pins[name] = hashlib.sha256(raw).hexdigest()
        d = json.loads(raw)
        if d["start"] != cursor or not cursor < d["stop"] <= offset:
            raise ValueError("Noncontiguous full physical incidence coverage")
        if d["physical_domain"] != offset or d["canonical_records_sha256"] != canonical["records_sha256"]:
            raise ValueError("Whole canonical registry dependency")
        if len(d["records"]) != d["stop"] - cursor or d["survivors"] != sum(r["tail_gate_pass"] for r in d["records"]):
            raise ValueError("Whole exact physical transcript cardinality")
        for r in d["records"]:
            if r["global_index"] != cursor or not 0 <= r["case_id"] < len(cases):
                raise ValueError("Exact physical interval case coverage")
            c = cases[r["case_id"]]
            if not c["start"] <= cursor < c["stop"] or r["rank"] != cursor - c["start"]:
                raise ValueError("Physical case cardinality rank omitted")
            b = tuple(r["B"])
            if previous_case == r["case_id"] and not previous_b < b:
                raise ValueError("Duplicate actual physical columns across part boundary")
            previous_case, previous_b = r["case_id"], b
            counts[r["case_id"]] += 1
            balance = "/".join(map(str, c["choice"]["balance"]))
            by_balance[balance] += 1
            maximum_tail2[balance] = max(maximum_tail2[balance], len(r["tail2"]))
            maximum_good_tail2[balance] = max(maximum_good_tail2[balance], sum(w == 0 for _, w in r["tail2"]))
            if r["tail_gate_pass"]:
                survivors_by_balance[balance] += 1
                survivors.append({"A": c["A"], "choice": c["choice"], **r})
            digest.update(json.dumps(r, sort_keys=True, separators=(",", ":")).encode() + b"\n")
            cursor += 1
    if cursor != offset or any(counts[i] != c["stop"] - c["start"] for i, c in enumerate(cases)):
        raise ValueError("Incomplete cardinality proof for any physical selection case")
    result = {"schema": "character617-small-common-tail-complete-v1", "physical_domain": offset,
              "selection_cases": len(cases), "canonical_prefixes": canonical["canonical_prefixes"],
              "canonical_records_sha256": canonical["records_sha256"], "whole_record_stream_sha256": digest.hexdigest(),
              "part_count": len(names), "whole_triple_part_sha256": part_pins,
              "incidences_by_balance": dict(sorted(by_balance.items())),
              "maximum_tail2_by_balance": dict(sorted(maximum_tail2.items())),
              "maximum_good_tail2_by_balance": dict(sorted(maximum_good_tail2.items())),
              "survivors_by_balance": {k: survivors_by_balance[k] for k in sorted(by_balance)},
              "survivors": survivors}
    o.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("survivors", "whole_triple_part_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main()
