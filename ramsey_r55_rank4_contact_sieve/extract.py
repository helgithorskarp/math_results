"""Search actual physical pairs; no saved verdict is a certificate."""
from itertools import combinations
import json
import sys
from model import classify, physical


def clique(rows, mask, size):
    if size == 0:
        return []
    while mask.bit_count() >= size:
        bit = mask & -mask
        mask ^= bit
        u = bit.bit_length()-1
        rest = clique(rows, mask & rows[u], size-1)
        if rest is not None:
            return [u]+rest
    return None


def extract(data):
    status = classify(data)
    if not status.get("baseline") or status.get("keep"):
        raise ValueError("requires a newly rejected member of the retained baseline")
    graph = physical(data)
    bits = int(graph["red_hex"], 16)
    rows = [0]*43
    for k, (i, j) in enumerate(combinations(range(43), 2)):
        if (bits >> k) & 1:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
    mask = 2**43-1
    for color, contacts in [("red", rows), ("blue", [mask ^ x ^ (1 << i) for i, x in enumerate(rows)])]:
        result = clique(contacts, mask, 5)
        if result is not None:
            return graph, {"color": color, "vertices": result}
    raise ArithmeticError("no physical five found: contradiction to the contact sieve")


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    graph, cert = extract(data)
    print(json.dumps({"graph": graph, "certificate": cert}, sort_keys=True))
