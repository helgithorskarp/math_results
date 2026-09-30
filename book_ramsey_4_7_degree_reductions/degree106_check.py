#!/usr/bin/env python3
"""Exact necessary-state reductions for a 106-edge degree-seven witness.

No full witness enumeration occurs here. See degree106.md for the bridge.
Python 3.11+, standard library; deterministic, single-process arithmetic.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

PAIRS = tuple(combinations(range(7), 2))
FORMS = (
    ("P7", tuple((i, i + 1) for i in range(6))),
    ("P4+C3", ((0, 1), (1, 2), (2, 3), (4, 5), (4, 6), (5, 6))),
    ("P3+C4", ((0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (3, 6))),
    ("P2+C5", ((0, 1), (2, 3), (3, 4), (4, 5), (5, 6), (2, 6))),
)
NEGATIVE_VECTORS = (
    (-1, -2, -2, -1, 2, 2, 2),
    (22, 25, 25, 22, -35, -35, -38),
    (50, 89, 116, 143, -172, -79, -163),
    (50, 89, 116, 143, -79, -172, -163),
    (143, 89, 116, 50, -172, -79, -163),
    (143, 89, 116, 50, -79, -172, -163),
    (92, 197, 263, 314, -391, -391, -91),
    (92, 263, 197, 314, -391, -391, -91),
    (314, 197, 263, 92, -391, -391, -91),
    (314, 263, 197, 92, -391, -391, -91),
)


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def capacity(edges, sigma):
    edges = {(min(b, z), max(b, z)) for b, z in edges}
    l = [[int((min(i, j), max(i, j)) in edges) if i != j else 0
          for j in range(7)] for i in range(7)]
    h = list(map(sum, l))
    c = [[0] * 7 for _ in range(7)]
    for b in range(7):
        c[b][b] = 6 + sigma[b]
    for b, z in PAIRS:
        codegree = sum(l[b][j] * l[z][j] for j in range(7))
        c[b][z] = c[z][b] = (
            2 - codegree if l[b][z]
            else h[b] + h[z] + sigma[b] + sigma[z] - 1 - codegree)
    return h, c


def state(edges, sigma, a, defect):
    h, c = capacity(edges, sigma)
    s = [row[:] for row in c]
    for pos in defect:
        b, z = PAIRS[pos]
        s[b][z] -= 1
        s[z][b] -= 1
    cols = [6 + x for x in sigma]
    if any(s[b][z] < 0 or s[b][z] > min(cols[b], cols[z])
           for b, z in PAIRS):
        return "intersection_range", None
    u = [sum(s[b]) - 3 * cols[b] for b in range(7)]
    if any(v < -a or v > a + 2 for v in u):
        return "row_bounds", None
    base = 18 + 8 * a + 5 * sum(x * y for x, y in zip(sigma, u))
    base -= sum(sigma[b] * s[b][z] * sigma[z]
                for b in range(7) for z in range(7))
    delta = sum(v * v for v in u) - base
    if delta < 0 or delta > 8 * a or delta % 4:
        return "moment", None
    q = delta // 4
    lo = [max(0, -v) for v in u]
    hi = [min(a, a + 2 - v) for v in u]
    for mark, target in ((1, q), (0, 2 * a - q)):
        selected = [b for b in range(7) if sigma[b] == mark]
        if not (sum(lo[b] for b in selected) <= target
                <= sum(hi[b] for b in selected)):
            return "signed_incidence", None
    return "survive", (s, u, q)


def signed_rows(h, sigma, a, s, u, q):
    """Visit every multiset of exceptional rows with the necessary loads."""
    positive = [p for p in combinations(range(7), 4)
                if sum(h[b] for b in p) <= 7]
    negative = [p for p in combinations(range(7), 2)
                if sum(h[b] for b in p) <= 3]
    for ts in combinations_with_replacement(negative, a):
        tc = [sum(b in p for p in ts) for b in range(7)]
        if sum(tc[b] * sigma[b] for b in range(7)) != q:
            continue
        hc = [u[b] + tc[b] for b in range(7)]
        m = a + 2
        if any(v < 0 or v > m for v in hc):
            continue
        rem = [[s[b][z] - sum(b in p and z in p for p in ts)
                for z in range(7)] for b in range(7)]
        if any(v < 0 for row in rem for v in row):
            continue

        def visit(start, rows, counts, mat):
            need = m - len(rows)
            if any(v < 0 or v > need for v in counts):
                return
            if need == 0:
                if not any(counts):
                    yield ts, tuple(rows), mat
                return
            for j in range(start, len(positive)):
                p = positive[j]
                if any(counts[b] == 0 for b in p):
                    continue
                if any(counts[b] == need and b not in p for b in range(7)):
                    continue
                if any(mat[b][z] == 0 for b in p for z in p):
                    continue
                new = [row[:] for row in mat]
                for b in p:
                    for z in p:
                        new[b][z] -= 1
                yield from visit(j, rows + [p],
                                 [v - int(b in p) for b, v in enumerate(counts)], new)

        yield from visit(0, [], hc, rem)


def quadratic(v, mat):
    return sum(v[b] * mat[b][z] * v[z] for b in range(7) for z in range(7))


def scalar_audit():
    out = []
    for e in range(1, 9):
        t = 8 - e
        values = []
        for h in combinations_with_replacement(range(4), 7):
            if sum(h) == 2 * e:
                values.append(32 * e - 3 * sum(x * x for x in h)
                              + 6 * t - 2 * sum(h[:t]) - 126)
        out.append({"e": e, "t": t, "histograms": len(values),
                    "max_2U_upper": max(values)})
    require([r["max_2U_upper"] for r in out] == [-62, -44, -26, -12, -2, 8, 16, 16],
            "scalar bounds changed")
    return out


def three_leaf_audit():
    target = [1, 1, 1, 2, 2, 2, 3]
    counts = Counter()
    digest = sha256()
    for chosen in combinations(range(21), 6):
        edges = {PAIRS[j] for j in chosen}
        h = [sum(b in p for p in edges) for b in range(7)]
        if h != target:
            continue
        counts["L"] += 1
        for ones in combinations(range(7), 2):
            sigma = [int(b in ones) for b in range(7)]
            weight = sum(h[b] for b in ones)
            for a in range(2):
                budget = 3 - weight - a
                if budget < 0:
                    continue
                for defect in combinations_with_replacement(range(21), budget):
                    status, _ = state(edges, sigma, a, defect)
                    counts["states"] += 1
                    counts[status] += 1
                    digest.update(json.dumps([chosen, ones, a, defect, status],
                                             separators=(",", ":")).encode() + b"\n")
    require(not counts["survive"], "three-leaf necessary state survived")
    require(counts["L"] == 88 and counts["states"] == 6600,
            "three-leaf coverage differs")
    return {"counts": dict(sorted(counts.items())), "states_sha256": digest.hexdigest()}


def form_audit(name, edges):
    edges = set(edges)
    h, _ = capacity(edges, [0] * 7)
    counts = Counter()
    by_a = Counter()
    signed_by_a = Counter()
    vectors_used = Counter()
    states_hash = sha256()
    signed_records = []
    for ones in combinations(range(7), 2):
        sigma = [int(b in ones) for b in range(7)]
        weight = sum(h[b] for b in ones)
        for a in range(5):
            budget = 6 - weight - a
            if budget < 0:
                continue
            for defect in combinations_with_replacement(range(21), budget):
                status, data = state(edges, sigma, a, defect)
                counts["states"] += 1
                counts[status] += 1
                states_hash.update(json.dumps([ones, a, defect, status],
                                              separators=(",", ":")).encode() + b"\n")
                if data is None:
                    continue
                by_a[a] += 1
                require(a <= 2, "a>=3 necessary state survived")
                if name == "P2+C5":
                    require(a <= 1, "P2+C5 a>=2 state survived")
                s, u, q = data
                for ts, hs, rem in signed_rows(h, sigma, a, s, u, q):
                    signed_by_a[a] += 1
                    signed_records.append([list(ones), a, list(defect),
                                           [list(p) for p in ts], [list(p) for p in hs]])
                    if name == "P4+C3":
                        witness = next((j for j, v in enumerate(NEGATIVE_VECTORS)
                                        if quadratic(v, rem) < 0), None)
                        require(witness is not None, "triangle residual Gram has no certificate")
                        vectors_used[witness] += 1
    require(counts["states"] == 35420, "form defect-state coverage differs")
    if name == "P3+C4":
        require(not signed_by_a[2], "P3+C4 a=2 exceptional rows survived")
    if name == "P2+C5":
        require(not signed_by_a[1] and not signed_by_a[2],
                "P2+C5 negative exceptional row survived")
    signed_records.sort()
    fingerprint = sha256(json.dumps(signed_records, separators=(",", ":")).encode()).hexdigest()
    return {"name": name, "counts": dict(sorted(counts.items())),
            "necessary_states_by_a": dict(sorted(by_a.items())),
            "signed_configurations_by_a": dict(sorted(signed_by_a.items())),
            "states_sha256": states_hash.hexdigest(), "signed_sha256": fingerprint,
            "negative_vectors_used": dict(sorted(vectors_used.items()))}


def isolate_audit():
    out = []
    for name, edges in (("C6", tuple((i, 1 + i % 6) for i in range(1, 7))),
                        ("2C3", ((1, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6)))):
        sigma = [1, 1, 0, 0, 0, 0, 0]
        _, c = capacity(set(edges), sigma)
        u = [sum(c[b]) - 3 * (6 + sigma[b]) for b in range(7)]
        if name == "2C3":
            v = [0, 1, 1, 1, -1, -1, -1]
            require(quadratic(v, c) == -11, "isolated triangle certificate differs")
            out.append({"name": name, "negative_vector": v, "value": -11})
        else:
            actual = sum(v * v for v in u)
            required = 12 + 16 - 2 + 5 * sum(x * y for x, y in zip(sigma, u))
            required -= quadratic(sigma, c)
            required += 4  # forced q=1, proved in degree106.md
            require((actual, required) == (24, 20), "isolated cycle moment differs")
            out.append({"name": name, "u": u, "actual_norm2": actual,
                        "required_norm2": required, "q": 1})
    return out


def main():
    out = {"agent": "six-books-1", "role": "researcher",
           "scope": "necessary-state reduction only; no 106-edge existence decision",
           "scalar": scalar_audit(), "isolates": isolate_audit(),
           "three_leaf": three_leaf_audit(),
           "forms": [form_audit(name, edges) for name, edges in FORMS],
           "negative_vectors": NEGATIVE_VECTORS}
    target = Path(__file__).with_name("degree106_expected.json")
    if target.exists():
        require(json.loads(target.read_text()) == json.loads(json.dumps(out)),
                "expected output differs")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
