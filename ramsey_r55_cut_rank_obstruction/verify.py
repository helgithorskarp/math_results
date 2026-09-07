"""Independent dense physical verifier. No producer, solver, catalog or assert."""
import hashlib
import json
import sys
from itertools import combinations


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rank(matrix):
    a = [list(row) for row in matrix]
    if not a:
        return 0
    r = 0
    for j in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(r + 1, len(a)):
            if a[i][j]:
                a[i] = [x ^ y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def slot_bound(a, r):
    # An independent sum over all row-space slots, with the zero slot first.
    if a <= 9:
        caps = [0] + [1] * ((1 << r) - 1)
    elif a <= 18:
        caps = [0] + [2] * ((1 << r) - 1)
    elif a == 19:
        caps = [2] * (1 << r)
    else:
        caps = [4] + [5] * ((1 << r) - 1)
    return sum(caps)


def graph(data):
    need(type(data) is dict and set(data) == {"n", "red_hex", "cut", "rank_color"}, "input fields")
    need(type(data["n"]) is int and data["n"] == 43, "input order")
    h = data["red_hex"]
    need(type(h) is str and len(h) == 226 and all(c in "0123456789abcdef" for c in h), "hex syntax")
    word = int(h, 16)
    need(word < 2**903, "hex range")
    a = data["cut"]
    need(type(a) is list and 1 <= len(a) < 43 and
         all(type(v) is int and 0 <= v < 43 for v in a) and a == sorted(set(a)), "cut syntax")
    need(data["rank_color"] in ("red", "blue"), "rank color")
    b = [v for v in range(43) if v not in a]
    if len(a) > len(b):
        a, b = b, a
    g = [[0] * 43 for _ in range(43)]
    k = 0
    for i in range(43):
        for j in range(i + 1, 43):
            g[i][j] = g[j][i] = (word // (2**k)) % 2
            k += 1
    return g, a, b


def verify(data, cert):
    g, a, b = graph(data)
    color = data["rank_color"]
    matrix = [[g[u][v] ^ int(color == "blue") for v in b] for u in a]
    r = rank(matrix)
    bound = next(k for k in range(len(a) + 1) if slot_bound(len(a), k) >= len(a))
    fields = {"input_sha256", "cut", "rank_color", "rank", "rank_lower_bound", "row_basis_hex", "status"}
    excluded = r < bound
    if excluded:
        fields |= {"witness_color", "witness"}
    need(type(cert) is dict and set(cert) == fields, "certificate fields")
    expected_hash = hashlib.sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    need(cert["input_sha256"] == expected_hash, "input hash")
    need(cert["cut"] == a and cert["rank_color"] == color, "cut/color mismatch")
    need(type(cert["rank"]) is int and cert["rank"] == r, "rank mismatch")
    need(type(cert["rank_lower_bound"]) is int and cert["rank_lower_bound"] == bound, "bound mismatch")
    bs = cert["row_basis_hex"]
    need(type(bs) is list and len(bs) == r, "basis size")
    nums = []
    for s in bs:
        need(type(s) is str and s.startswith("0x") and len(s) <= 13, "basis syntax")
        x = int(s, 16)
        need(0 < x < 2**len(b) and hex(x) == s, "basis range")
        nums.append(x)
    basis = [[(x >> j) & 1 for j in range(len(b))] for x in nums]
    need(rank(basis) == r and rank(matrix + basis) == r, "basis does not span the cut")
    if excluded:
        need(cert["status"] == "EXCLUDED_WITH_PHYSICAL_WITNESS", "wrong exclusion status")
        q = cert["witness"]
        need(type(q) is list and len(q) == 5 and all(type(v) is int and 0 <= v < 43 for v in q)
             and q == sorted(set(q)), "five-set syntax")
        need(cert["witness_color"] in ("red", "blue"), "witness color")
        c = int(cert["witness_color"] == "red")
        need(all(g[u][v] == c for u, v in combinations(q, 2)), "nonmonochromatic witness")
        return "VERIFIED_PHYSICAL_EXCLUSION"
    need(cert["status"] == "OUTSIDE_CUT_RANK_GATE", "wrong outside status")
    return "VERIFIED_OUTSIDE_GATE_ONLY"


if __name__ == "__main__":
    print(verify(json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))))
