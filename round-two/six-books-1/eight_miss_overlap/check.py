"""Direct labeled-set controls, six-books-1, researcher. No host census."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def build():
    a, w = set(range(10)), {8, 9}
    z = a - w
    five = [set(s) for s in combinations(range(10), 5) if set(s) & w]
    need(len(five) == 196, "five-set choices")
    types = Counter()
    for u, v in product(five, repeat=2):
        common = u & v & z
        r = len(common)
        if r > 2:
            continue
        p, q, c = len(u & w), len(v & w), len(u & v & w)
        d = ((u | v) & z) | (u & v & w)
        x = a - d
        need(len(x) == p + q + r - c <= r + 2, "avoidance-set identity")
        types[p, q, r, c, len(x)] += 1
        if r == 2:
            triples = [set(s) for s in combinations(sorted(x), 3)]
            need(all(len(s & t) >= 2 for s, t in product(triples, repeat=2)), "two-triple contradiction")
        if r == 1 and len(x) == 3:
            need((u | v) & w == w and len(list(combinations(sorted(x), 3))) == 1,
                 "forced neighbor equality")
    triples4 = [set(s) for s in combinations(range(4), 3)]
    intersections = Counter(len(s & t) for s, t in product(triples4, repeat=2))
    return {"five_set_choices": len(five), "ordered_input_pairs": len(five) ** 2,
            "type_records": [list(k) + [count] for k, count in sorted(types.items())],
            "parent_retained_pairs": sum(types.values()),
            "overlap_two_excluded": sum(count for key, count in types.items() if key[2] == 2),
            "overlap_one_equality_excluded": sum(count for key, count in types.items() if key[2] == 1 and key[4] < 3),
            "retained_templates": sum(count for key, count in types.items() if key[2] == 0 or (key[2] == 1 and key[4] == 3)),
            "four_point_triple_intersections": {str(k): n for k, n in sorted(intersections.items())}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = build()
    path = HERE / "expected.json"
    if args.write:
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    else:
        need(record == json.loads(path.read_text()), "compact type table mismatch")
    print(json.dumps({"status": "PASS", "retained_templates": record["retained_templates"],
                      "expected_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
