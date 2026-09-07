"""Read a physical graph/cut, decide gate membership, extract a literal bad five."""
import hashlib
import json
import sys
from itertools import combinations

from model import lower_bound


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def parse(data):
    if type(data) is not dict or set(data) != {"n", "red_hex", "cut", "rank_color"}:
        raise ValueError("wrong input fields")
    if type(data["n"]) is not int or data["n"] != 43:
        raise ValueError("order must be 43")
    h = data["red_hex"]
    if (type(h) is not str or len(h) != 226 or any(c not in "0123456789abcdef" for c in h)
            or int(h, 16) >= 1 << 903):
        raise ValueError("red_hex must be canonical 903-bit physical adjacency")
    cut = data["cut"]
    if (type(cut) is not list or not 1 <= len(cut) <= 42 or
            any(type(v) is not int or not 0 <= v < 43 for v in cut) or cut != sorted(set(cut))):
        raise ValueError("invalid cut")
    if data["rank_color"] not in ("red", "blue"):
        raise ValueError("invalid rank color")
    other = [v for v in range(43) if v not in cut]
    if len(cut) > len(other):
        cut, other = other, cut
    adj = [0] * 43
    packed = int(h, 16)
    for i, (u, v) in enumerate(combinations(range(43), 2)):
        if (packed >> i) & 1:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return adj, cut, other


def basis(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return [pivots[p] for p in sorted(pivots, reverse=True)]


def clique(adj, candidates, size, prefix=()):
    if not size:
        return list(prefix)
    while candidates.bit_count() >= size:
        bit = candidates & -candidates
        candidates ^= bit
        v = bit.bit_length() - 1
        found = clique(adj, candidates & adj[v], size - 1, prefix + (v,))
        if found is not None:
            return found
    return None


def extract(data):
    adj, a, b = parse(data)
    reverse = data["rank_color"] == "blue"
    rows = [sum(((((adj[u] >> v) & 1) ^ reverse) << j) for j, v in enumerate(b)) for u in a]
    bs = basis(rows)
    bound = lower_bound(len(a))
    out = {"input_sha256": digest(data), "cut": a, "rank_color": data["rank_color"],
           "rank": len(bs), "rank_lower_bound": bound, "row_basis_hex": [hex(x) for x in bs]}
    if len(bs) >= bound:
        return dict(out, status="OUTSIDE_CUT_RANK_GATE")
    mask = (1 << 43) - 1
    for color, colored in (("red", adj), ("blue", [mask ^ row ^ (1 << i) for i, row in enumerate(adj)])):
        found = clique(colored, mask, 5)
        if found is not None:
            return dict(out, status="EXCLUDED_WITH_PHYSICAL_WITNESS", witness_color=color, witness=found)
    raise RuntimeError("low-cut-rank graph without a bad five: theorem/implementation failure")


if __name__ == "__main__":
    print(json.dumps(extract(json.load(open(sys.argv[1]))), indent=2, sort_keys=True))
