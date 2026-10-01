#!/usr/bin/env python3
"""Exact controls for the two-point primitive-block lemma; no search for a cover."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AXES = (2, 3, 5)
POINTS = tuple(itertools.product(*(range(q) for q in AXES)))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def make_h(kind):
    h = [[F(0) for _ in range(5)] for _ in range(3)]
    if kind == (1, 0, 0):
        pass
    elif kind == (0, 1, 0):
        h[0] = h[1] = [F(-1, 2)] + [F(1, 8)] * 4
        h[2] = [F(1)] + [F(-1, 4)] * 4
    elif kind == (0, 0, 1):
        h[0] = [F(-1), F(-1)] + [F(2, 3)] * 3
        h[1] = h[2] = [F(1, 2), F(1, 2)] + [F(-1, 3)] * 3
    elif kind == (1, 1, 0):
        h[0] = [F(-1)] + [F(1, 4)] * 4
        h[1] = [F(1)] + [F(-1, 4)] * 4
    elif kind == (1, 0, 1):
        h[0][:2] = [F(-1), F(1)]
        h[1][:2] = h[2][:2] = [F(1, 2), F(-1, 2)]
    elif kind == (0, 1, 1):
        h[0][:2] = [F(-1), F(1)]
        h[1][:2] = [F(1), F(-1)]
    elif kind == (1, 1, 1):
        h[0][:3] = [F(-1), F(0), F(1)]
        h[1][:3] = [F(0), F(1), F(-1)]
        h[2][:3] = [F(1), F(-1), F(0)]
    elif kind == (0, 0, 0):
        h = [[-a * b for b in [F(1)] + [F(-1, 4)] * 4]
             for a in [F(1), F(-1, 2), F(-1, 2)]]
    else:
        raise ValueError("unknown pair type")
    return h


def generate_certificates():
    records = []
    for kind in itertools.product(range(2), repeat=3):
        h = make_h(kind)
        w = [1 + (1 if a == 0 else -1) * h[b][c] for a, b, c in POINTS]
        nums = [int(24 * x) for x in w]
        require(all(F(n, 24) == x for n, x in zip(nums, w)), "denominator")
        records.append({"type": list(kind), "denominator": 24,
                        "weights": nums})
    return records


def validate_weight(values):
    require(len(values) == 30, "wrong weight length")
    require(all(x >= 0 for x in values), "negative weight")
    w = dict(zip(POINTS, values))
    for axis, q in enumerate(AXES):
        other = [j for j in range(3) if j != axis]
        for fixed in itertools.product(*(range(AXES[j]) for j in other)):
            total = sum(w[x] for x in POINTS
                        if all(x[j] == value for j, value in zip(other, fixed)))
            require(total == q, "wrong line sum")
    # Independently check every residue of every proper divisor via j mod 30.
    by_j = [w[(j % 2, j % 3, j % 5)] for j in range(30)]
    for d in divisors(30)[:-1]:
        for a in range(d):
            require(sum(by_j[a::d]) == 30 // d, "wrong proper-period moment")
    return w


def pair_charge(x, y):
    changed = tuple(i for i in range(3) if x[i] != y[i])
    return 2 if changed == (0,) else 1 if changed == (1,) else 0


def normalized_coordinate(z, x, y, q):
    names = [x] + ([y] if y != x else [])
    names += [j for j in range(q) if j not in names]
    return names.index(z)


def primitive_checks(records):
    require(len(records) == 8, "missing primitive type")
    certs = {}
    for rec in records:
        kind = tuple(rec["type"])
        require(kind not in certs, "duplicate primitive type")
        require(rec["denominator"] == 24, "wrong denominator")
        values = [F(n, 24) for n in rec["weights"]]
        w = validate_weight(values)
        x, y = (0, 0, 0), kind
        charge = w[x] if x == y else w[x] + w[y]
        require(charge == pair_charge(x, y), "wrong pair charge")
        certs[kind] = w
    pairs = 0
    for i, x in enumerate(POINTS):
        for y in POINTS[i:]:
            kind = tuple(int(x[j] != y[j]) for j in range(3))
            w = {}
            for z in POINTS:
                nz = tuple(normalized_coordinate(z[j], x[j], y[j], AXES[j])
                           for j in range(3))
                w[z] = certs[kind][nz]
            validate_weight([w[z] for z in POINTS])
            charge = w[x] if x == y else w[x] + w[y]
            require(charge == pair_charge(x, y), "transported pair")
            pairs += 1
    return pairs


def validate_parameters(B, p, b, u, v):
    require(all(type(x) is int for x in (B, p, b)), "noninteger parameter")
    require(B >= 30 and B % 30 == 0 and b > 0, "bad base")
    cofactor = B
    for q in (2, 3, 5):
        while cofactor % q == 0:
            cofactor //= q
    require(cofactor == 1, "base has another prime")
    require(B // 30 % b == 0, "weight is not primitive-block periodic")
    require(p > 1 and all(p % d for d in range(2, isqrt(p) + 1)), "not prime")
    require(B % p != 0, "cofactor is not coprime")
    require(len(u) == B and all(len(row) == p for row in u), "wrong u shape")
    require(len(v) == b and all(len(row) == p for row in v), "wrong v shape")
    require(all(x >= 0 for row in u + v for x in row), "negative physical weight")


def linear_budget(B, p, b, u, v):
    validate_parameters(B, p, b, u, v)
    A = [sum(row) for row in u]
    base = max(A) + max(max(row) for row in u)
    binary = max(A[a] + u[(a + B // 2) % B][r] + 2 * v[a % b][r]
                 for a in range(B) for r in range(p))
    ternary = max(A[a] + u[(a + d) % B][r] + v[a % b][r]
                  for a in range(B) for r in range(p)
                  for d in (B // 3, 2 * B // 3))
    return max(base, binary, ternary)


def literal_top_budget(B, p, b, u, v, refined=True):
    """Enumerate actual top phases, independently classifying their block points."""
    T = B // 30
    best = 0
    for a in range(B):
        for c in range(B):
            charge = 0
            if a != c and a % T == c % T:
                j, k = a // T, c // T
                x = (j % 2, j % 3, j % 5)
                y = (k % 2, k % 3, k % 5)
                charge = pair_charge(x, y) if refined else 2
            for r in range(p):
                val = sum(u[a]) + u[c][r] + charge * v[a % b][r]
                best = max(best, val)
    return best


def budget_checks():
    n = 0
    for B in (30, 60, 90, 150):
        for p in (7, 11):
            for b in divisors(B // 30):
                for seed in range(3):
                    # Deterministic, explicitly finite fixtures; not a probabilistic claim.
                    u = [[((a + 1) * (r + 3) + seed * a * r) % 13
                          for r in range(p)] for a in range(B)]
                    v = [[((t + 4) * (r + 2) + seed) % 9
                          for r in range(p)] for t in range(b)]
                    fast = linear_budget(B, p, b, u, v)
                    brute = literal_top_budget(B, p, b, u, v)
                    old = literal_top_budget(B, p, b, u, v, False)
                    require(fast == brute and brute <= old, "physical phase maximum")
                    n += 1
    B, p, b = 30, 7, 1
    u = [[0] * p for _ in range(B)]
    u[0] = [3] * p
    u[6][0] = 3
    v = [[1] + [0] * (p - 1)]
    new = linear_budget(B, p, b, u, v)
    old = literal_top_budget(B, p, b, u, v, False)
    require((new, old) == (24, 26), "strict fixture changed")
    return n, {"old_distinct_point_budget": old, "new_budget": new}


def covering_checks():
    """Literal whole-period checks, including positive known-class footprints."""
    B, p, b, N = 60, 7, 2, 420
    cover = [(1, 2), (2, 4), (0, 3), (4, 6), (8, 12)]
    require(all(any(x % m == a for a, m in cover) for x in range(N)), "control cover")
    checked = 0
    for mask in range(1 << len(cover)):
        known = [cover[i] for i in range(len(cover)) if mask >> i & 1]
        used = {m for _, m in known}
        R = [d for d in divisors(N) if d >= 2 and d not in used]
        require(B in R and N in R, "known top resource")
        for seed in range(3):
            u = [[0] * p for _ in range(B)]
            v = [[((t + 1) * (r + 2) + seed) % 5 for r in range(p)] for t in range(b)]
            for x in range(N):
                if not any(x % m == a for a, m in known):
                    u[x % B][x % p] = ((x + 1) * (seed + 2)) % 7
            lifted = [u[x % B][x % p] + v[x % b][x % p] for x in range(N)]
            demand = sum(lifted) - sum(v[x % b][x % p]
                                      for a, m in known for x in range(a, N, m))
            cap = sum(max(sum(lifted[a::m]) for a in range(m))
                      for m in R if m not in (B, N))
            K = linear_budget(B, p, b, u, v)
            require(demand <= cap + K, "genuine-cover inequality failed")
            # Check the stronger actual-phase inequality, without individual maxima.
            outside = [c for c in cover if c[1] not in used]
            footprints = sum(lifted[x] for a, m in outside for x in range(a, N, m))
            for a, c, r in ((0, 0, 0), (0, B // 2, 1), (0, B // 3, 2), (0, B // 5, 3)):
                delta = (c - a) % B
                chi = 2 if delta == B // 2 else 1 if delta in (B // 3, 2 * B // 3) else 0
                actual = sum(u[a]) + u[c][r] + chi * v[a % b][r]
                require(demand <= footprints + actual, "actual-phase inequality failed")
                checked += 1
    return checked


def target_checks():
    result = []
    for B in (1440, 2160):
        p, b = 7, B // 30
        u = [[((a + 2) * (r + 3) + a // 7) % 11 for r in range(p)] for a in range(B)]
        v = [[((t + 1) * (r + 4)) % 7 for r in range(p)] for t in range(b)]
        K = linear_budget(B, p, b, u, v)
        result.append({"period": B * p, "primitive_block_step": b,
                       "binary_separation": B // 2,
                       "ternary_separations": [B // 3, 2 * B // 3],
                       "fixture_budget": K,
                       "direct_phase_candidates": B * B * p,
                       "coupled_phase_candidates": 3 * B * p})
    return result


def rejection_checks(records):
    bad = list(records[0]["weights"])
    bad[0] += 1
    rejected = 0
    for values in ([F(n, 24) for n in bad], [F(-1)] + [F(1)] * 29, [F(1)] * 29):
        try:
            validate_weight(values)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed certificate was accepted")
    u, v = [[0] * 7 for _ in range(60)], [[0] * 7 for _ in range(4)]
    try:
        linear_budget(60, 7, 4, u, v)
    except ValueError:
        rejected += 1
    else:
        raise ValueError("invalid block period was accepted")
    return rejected


def main():
    path = ROOT / "primitive_weights.json"
    records = json.loads(path.read_text())
    # Literal data, not the generator, is the proof certificate consumed here.
    primitive_pairs = primitive_checks(records)
    budget_count, strict = budget_checks()
    output = {"author": "six-covering-3", "role": "researcher",
              "primitive_singletons_and_pairs": primitive_pairs,
              "primitive_types": len(records),
              "physical_budget_equalities": budget_count,
              "genuine_cover_actual_phase_checks": covering_checks(),
              "rejected_invalid_inputs": rejection_checks(records),
              "strict_fixture": strict, "target_fixtures": target_checks(),
              "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    expected_path = ROOT / "expected.json"
    if expected_path.exists():
        require(output == json.loads(expected_path.read_text()), "expected output mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
