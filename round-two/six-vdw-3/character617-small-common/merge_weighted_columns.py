"""Complete weighted coefficient coverage and whole independent comparison."""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("producer", "checker", "optimized", "domain", "output"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    domain = json.loads(a.domain.read_text())
    cursor = 0
    totals = collections.Counter()
    records = []
    parts = sorted(a.producer.glob("range-*.json"))
    for directory in (a.checker, a.optimized):
        if [p.name for p in parts] != [p.name for p in sorted(directory.glob("range-*.json"))]:
            raise ValueError("Incomplete weighted transcript file set")
    for part in parts:
        raw = part.read_bytes()
        if any(raw != (d / part.name).read_bytes() for d in (a.checker, a.optimized)):
            raise ValueError("Whole weighted independent transcripts differ")
        d = json.loads(raw)
        if d["start"] != cursor or d["stop"] <= cursor or d["prefix_records_sha256"] != domain["records_sha256"]:
            raise ValueError("Gap, overlap or changed physical weighted domain")
        cursor = d["stop"]
        totals.update(d["incidences"])
        records.extend(d["records"])
    if cursor != domain["selected_prefixes"] or len({tuple(r["A"]) for r in records}) != len(records):
        raise ValueError("Whole selected domain or unique physical prefix labels omitted")
    raw = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    result = {"schema": "character617-weighted-prefix-column-complete-v1",
              "parent_prefixes": domain["parent_prefixes"], "selected_input_prefixes": cursor,
              "selected_records_sha256": domain["records_sha256"],
              "surviving_prefixes": len(records), "incidences": dict(sorted(totals.items())),
              "records_sha256": hashlib.sha256(raw).hexdigest(), "records": records}
    a.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, sort_keys=True))


if __name__ == "__main__":
    main()
