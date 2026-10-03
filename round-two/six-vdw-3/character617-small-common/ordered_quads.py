"""Independently enumerate all increasing anchored threshold-four quadruples."""
import argparse
import json
from pathlib import Path


def inverse(a):
    r, old_r, s, old_s = 617, a, 0, 1
    while r:
        k = old_r // r
        old_r, r = r, old_r - k * r
        old_s, s = s, old_s - k * s
    if old_r != 1:
        raise ValueError("Nonunit field label")
    return old_s % 617


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--stop", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    squares = {q * q % 617 for q in range(1, 617)}
    rows = sorted(squares)
    columns = [t for t in range(1, 617) if t not in squares]
    if not 1 <= args.start < args.stop <= len(rows):
        raise ValueError("Increasing second-row range")
    positive = set()
    for d in (285, 314, 362, 381, 409, 570):
        t = 1
        for _ in range(6):
            t = (t + d) % 617
            positive.add(t)
    if len(positive) != 33 or any(t in squares for t in positive):
        raise ValueError("Six endpoint supports use the actual1+j*delta convention")
    ratios = positive | {inverse(t) for t in positive}
    masks = []
    for q in rows:
        iq = inverse(q)
        mask = 0
        for j, t in enumerate(columns):
            if t * iq % 617 in ratios:
                mask |= 1 << j
        if mask.bit_count() != 66:
            raise ValueError("Literal row degree")
        masks.append(mask)
    records = []
    tested = [0, 0, 0]
    retained = [0, 0, 0]
    for i in range(args.start, args.stop):
        tested[0] += 1
        ci = masks[0] & masks[i]
        if ci.bit_count() < 4:
            continue
        retained[0] += 1
        for j in range(i + 1, len(rows)):
            tested[1] += 1
            cj = ci & masks[j]
            if cj.bit_count() < 4:
                continue
            retained[1] += 1
            for k in range(j + 1, len(rows)):
                tested[2] += 1
                ck = cj & masks[k]
                if ck.bit_count() >= 4:
                    retained[2] += 1
                    records.append({"A": [1, rows[i], rows[j], rows[k]],
                                    "C": [t for h, t in enumerate(columns)
                                          if ck >> h & 1]})
    result = {"schema": "character617-ordered-quad-part-v1",
              "start": args.start, "stop": args.stop,
              "tested": tested, "retained": retained, "records": records}
    args.output.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
