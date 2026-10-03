"""Select exactly the nonzero physical column cases relevant to the two balances."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--mode", choices=("producer", "checker"), required=True)
    a = p.parse_args()
    parent = json.loads(a.input.read_text())
    records = parent["records"]
    raw = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(raw).hexdigest() != parent["records_sha256"] or len(records) != 105590:
        raise ValueError("Whole independently checked105590-prefix domain")
    selected = []
    for r in records:
        c = len(r["C"])
        if c not in (2, 3):
            raise ValueError("Small whole common scope")
        if a.mode == "producer":
            keep = bool(r["p10"] or c == 3 and (r["p9_single"] + r["p9_double"]))
        else:
            u = [len(ts) for ts in r["singleton"]]
            pair_counts = [math.comb(n, 2) for n in u]
            p10 = math.prod(pair_counts)
            p9s = sum(u[i] * math.prod(pair_counts[j] for j in range(5) if j != i)
                      for i in range(5))
            p9d = sum(len(ts) * u[i] * u[j] * math.prod(pair_counts[k] for k in range(5) if k not in (i, j))
                      for i, j, ts in r["double"])
            if (p10, p9s, p9d) != (r["p10"], r["p9_single"], r["p9_double"]):
                raise ValueError("Unweighted physical coefficients differ")
            keep = p10 > 0 if c == 2 else p10 + p9s + p9d > 0
        if keep:
            selected.append(r)
    raw = json.dumps(selected, sort_keys=True, separators=(",", ":")).encode()
    result = {"schema": "character617-weighted-relevant-prefix-domain-v1",
              "parent_records_sha256": parent["records_sha256"],
              "parent_prefixes": len(records), "selected_prefixes": len(selected),
              "records_sha256": hashlib.sha256(raw).hexdigest(), "records": selected}
    a.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
