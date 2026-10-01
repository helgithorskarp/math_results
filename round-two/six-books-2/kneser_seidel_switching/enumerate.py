#!/usr/bin/env python3
"""Direct exhaustive control: all cuts of KG(7,2), modulo complement.

This program uses literal graph codegrees, no root-degree or shape pruning.
It is validation of PROOF.md, not a completeness premise of that proof.
"""

import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path


def census():
    pairs = list(itertools.combinations(range(7), 2))
    point_masks = [(1 << a) | (1 << b) for a, b in pairs]
    base = [sum(1 << j for j, q in enumerate(point_masks) if not p & q)
            for p in point_masks]
    whole = (1 << 21) - 1
    records = []
    scanned = 0
    # Root pair 01 is graph vertex zero. Exactly one of a cut and its
    # complement omits this vertex. The remaining twenty bits are free.
    for assignment in range(1 << 20):
        scanned += 1
        cut = assignment << 1
        rows = [base[i] ^ (cut ^ (whole if cut >> i & 1 else 0))
                for i in range(21)]
        red_max = 0
        valid = True
        for i in range(21):
            neighbors = rows[i] & ((1 << i) - 1)
            while neighbors:
                bit = neighbors & -neighbors
                j = bit.bit_length() - 1
                neighbors -= bit
                pages = (rows[i] & rows[j]).bit_count()
                if pages > 3:
                    valid = False
                    break
                red_max = max(red_max, pages)
            if not valid:
                break
        if not valid:
            continue
        blue_max = 0
        for i in range(21):
            for j in range(i):
                if not rows[i] >> j & 1:
                    pages = (whole & ~(rows[i] | rows[j])
                             & ~((1 << i) | (1 << j))).bit_count()
                    blue_max = max(blue_max, pages)
        records.append([cut, red_max, blue_max])
    if scanned != 1 << 20:
        raise RuntimeError("Incomplete cut domain")
    digest = hashlib.sha256(json.dumps(records, separators=(",", ":"))
                            .encode("ascii")).hexdigest()
    return {
        "cuts_scanned": scanned,
        "red_B4_free_cuts": len(records),
        "maximum_blue_pages_histogram": dict(sorted(collections.Counter(
            str(r[2]) for r in records).items(), key=lambda x: int(x[0]))),
        "record_sha256": digest,
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, required=True,
                        help="Local compact record file; do not use a tracked path")
    args = parser.parse_args()
    result = census()
    args.records.parent.mkdir(parents=True, exist_ok=True)
    args.records.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"},
                     indent=2))


if __name__ == "__main__":
    main()
