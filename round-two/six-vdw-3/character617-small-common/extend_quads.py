"""Cover c=2/3 five-row prefixes by all304 physical extensions per quad."""
import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path


def labels(mask):
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quads", type=Path, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    domain = json.loads(args.quads.read_text())
    quads = domain["records"]
    encoded = json.dumps(quads, sort_keys=True, separators=(",", ":")).encode()
    if domain["records_sha256"] != hashlib.sha256(encoded).hexdigest() or len(quads) != 64108:
        raise ValueError("Complete checked quadruple domain")
    if not 0 <= args.start < args.stop <= len(quads):
        raise ValueError("Disjoint extension domain")
    rows = [q for q in range(1, 617) if pow(q, 308, 617) == 1]
    v = {(1 + j * d) % 617 for d in (285, 314, 362, 381, 409, 570)
         for j in range(1, 7)}
    ratios = v | {pow(t, -1, 617) for t in v}
    masks = {q: sum(1 << (q * t % 617) for t in ratios) for q in rows}
    if len(v) != 33 or len(ratios) != 66 or any(m.bit_count() != 66 for m in masks.values()):
        raise ValueError("Actual endpoint support convention")
    physical = {}
    histogram = collections.Counter()
    lifted_capacity_presentations = 0
    for quad in quads[args.start:args.stop]:
        a = quad["A"]
        common4 = masks[a[0]] & masks[a[1]] & masks[a[2]] & masks[a[3]]
        if labels(common4) != quad["C"]:
            raise ValueError("Quad whole common set")
        for q in rows:
            if q in a:
                continue
            common = common4 & masks[q]
            size = common.bit_count()
            histogram[size] += 1
            if size not in (2, 3):
                continue
            full = tuple(sorted((*a, q)))
            u_masks = []
            for i in range(5):
                m = masks[full[(i + 1) % 5]]
                for j in range(5):
                    if j != i:
                        m &= masks[full[j]]
                u_masks.append(m & ~common)
            u = [m.bit_count() for m in u_masks]
            if sum(min(2, n) for n in u) < 8:
                continue
            lifted_capacity_presentations += 1
            pairs = []
            for i, j in itertools.combinations(range(5), 2):
                m = (1 << 617) - 1
                for k in range(5):
                    if k not in (i, j):
                        m &= masks[full[k]]
                m &= ~masks[full[i]] & ~masks[full[j]]
                pairs.append((i, j, m))
            choose2 = [math.comb(n, 2) for n in u]
            p10 = math.prod(choose2)
            p9_single = sum(u[i] * math.prod(choose2[j] for j in range(5) if j != i)
                            for i in range(5))
            p9_double = sum(m.bit_count() * u[i] * u[j] *
                            math.prod(choose2[k] for k in range(5) if k not in (i, j))
                            for i, j, m in pairs)
            record = {"A": list(full), "C": labels(common),
                      "singleton": [labels(m) for m in u_masks],
                      "double": [[i, j, labels(m)] for i, j, m in pairs],
                      "p10": p10, "p9_single": p9_single, "p9_double": p9_double}
            if physical.setdefault(full, record) != record:
                raise ValueError("Different presentations disagree on physical prefix")
    result = {"schema": "character617-small-common-extension-part-v1",
              "start": args.start, "stop": args.stop,
              "quad_records_sha256": domain["records_sha256"],
              "raw_trials": sum(histogram.values()), "common_histogram": sorted(histogram.items()),
              "capacity_presentations": lifted_capacity_presentations,
              "records": [r for _, r in sorted(physical.items())]}
    if result["raw_trials"] != 304 * (args.stop - args.start):
        raise ValueError("All physical fifth rows must be included")
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "records"} |
                     {"distinct_prefixes_in_part": len(physical)}))


if __name__ == "__main__":
    main()
