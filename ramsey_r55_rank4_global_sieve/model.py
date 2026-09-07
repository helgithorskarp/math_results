"""All rank-four factors and all 443 physical within-side coordinates."""
from collections import Counter
from itertools import combinations
import json
import re
import sys

PAIRS = list(combinations(range(43), 2))
INTERNAL = [(i, j) for i, j in PAIRS if (i < 20) == (j < 20)]


def rank(vectors):
    basis = {}
    for value in vectors:
        x = value
        while x:
            p = x.bit_length()-1
            if p in basis:
                x ^= basis[p]
            else:
                basis[p] = x
                break
    return len(basis)


def dot(x, y):
    return (x & y).bit_count() & 1


def factors(data):
    if not isinstance(data, dict) or set(data) != {"rows", "columns", "internal_hex"}:
        raise ValueError("exact factor fields required")
    a, b = data["rows"], data["columns"]
    for arr, size in [(a, 20), (b, 23)]:
        if not isinstance(arr, list) or len(arr) != size or any(type(x) is not int or not 0 <= x < 16 for x in arr):
            raise ValueError("invalid label list")
        if rank(arr) != 4:
            raise ValueError("factors must both span F2^4")
    h = data["internal_hex"]
    if not isinstance(h, str) or re.fullmatch(r"[0-9a-f]{111}", h) is None or int(h, 16) >= 2**443:
        raise ValueError("exact 443-bit internal encoding required")
    return a, b, int(h, 16)


def affine_removed(a, b):
    ca, cb = Counter(a), Counter(b)
    if set(ca) != set(range(1, 16)) or set(cb) != set(range(1, 16)):
        return False
    if sorted(ca.values()) != [1]*10+[2]*5 or sorted(cb.values()) != [1]*7+[2]*8:
        return False
    doubled = {x for x in cb if cb[x] == 2}
    return any(doubled == {y for y in range(16) if dot(w, y)} for w in range(1, 16))


def classify(data):
    a, b, _ = factors(data)
    ca, cb = Counter(a), Counter(b)
    blue_rank = rank([sum((1-dot(x, y)) << j for j, y in enumerate(b)) for x in a])
    if ca[0] and cb[0]:
        return {"baseline": False, "reason": "previous_zero_pair"}
    if blue_rank < 4:
        return {"baseline": False, "reason": "previous_complement_rank"}
    if affine_removed(a, b):
        return {"baseline": False, "reason": "previous_affine_family"}
    for violated, reason in [(ca[0] > 1 or cb[0] > 2, "zero_multiplicity"),
                             (max(ca.values()) > 4, "row_class"),
                             (max(cb.values()) > 5, "column_class")]:
        if violated:
            return {"baseline": True, "keep": False, "reason": reason}
    return {"baseline": True, "keep": True, "reason": "survives_necessary_filter"}


def physical(data):
    a, b, bits = factors(data)
    red = 0
    t = 0
    for k, (i, j) in enumerate(PAIRS):
        if i < 20 <= j:
            value = dot(a[i], b[j-20])
        else:
            value = (bits >> t) & 1
            t += 1
        red |= value << k
    return {"n": 43, "red_hex": format(red, "0226x")}


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps({"classification": classify(data), "graph": physical(data)}, sort_keys=True))
