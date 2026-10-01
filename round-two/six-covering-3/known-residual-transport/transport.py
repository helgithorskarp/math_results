"""Sharp known-residual primitive transport budgets, with exact integer checks.

Author six-covering-3, researcher, 2026-10-01. Necessary budgets only.
Dependencies are the explicitly cited sibling publications; no solver required.
"""

from itertools import product
import json
from math import gcd
from pathlib import Path
import subprocess
import sys

PRIOR = Path(__file__).resolve().parent.parent / "four-top-block-dp"
sys.path.insert(0, str(PRIOR))
from budget import (CHARGE, balanced_vertices, footprints, local_table, require,
                    sharp_function, subset_dp, validate)
from reproduce import encode as old_encode


MASS = tuple(6 - CHARGE[63 ^ mask] for mask in range(64))
DELTA = tuple(tuple(MASS[u] - MASS[u & ~h] for h in range(64)) for u in range(64))


def sharp_nonnegative(mask):
    require(type(mask) is int and 0 <= mask < 64, "invalid residual point mask")
    return tuple(value + 1 for value in sharp_function(63 ^ mask))


def validate_masks(T, C, masks):
    require(len(masks) == T and all(len(row) == C for row in masks), "wrong known-mask dimensions")
    require(all(type(m) is int and 0 <= m < 64 for row in masks for m in row),
            "invalid known point mask")


def literal_charge(C, ds, rs, mask, js, weights, residual_masks):
    value = 0
    for z in range(C):
        points = 0
        for i, d in enumerate(ds):
            if mask & (1 << i) and z % d == rs[i]:
                points |= 1 << js[i]
        value += DELTA[residual_masks[z]][points] * weights[z]
    return value


def profile35(weights, residual_masks):
    """Four lookup tables for the O(1) local C35 inclusion-exclusion formula."""
    require(len(weights) == len(residual_masks) == 35, "invalid C35 profile")
    point = [[DELTA[residual_masks[z]][h] * weights[z] for z in range(35)]
             for h in range(64)]
    base = [sum(row) for row in point]
    rows = [[sum(row[z] for z in range(r, 35, 5)) for r in range(5)] for row in point]
    cols = [[sum(row[z] for z in range(r, 35, 7)) for r in range(7)] for row in point]
    return base, rows, cols, point


def profile_charge35(rs, mask, js, profile):
    r5, r7, s = rs[1:]
    base, rows, cols, point = profile
    a = (1 << js[0]) if mask & 1 else 0
    r = a | ((1 << js[1]) if mask & 2 else 0)
    c = a | ((1 << js[2]) if mask & 4 else 0)
    both = r | c
    e = a
    if s % 5 == r5 and mask & 2:
        e |= 1 << js[1]
    if s % 7 == r7 and mask & 4:
        e |= 1 << js[2]
    f = e | ((1 << js[3]) if mask & 8 else 0)
    cross = next(z for z in range(35) if z % 5 == r5 and z % 7 == r7)
    return (base[a] + rows[r][r5] - rows[a][r5] + cols[c][r7] - cols[a][r7]
            + point[both][cross] - point[r][cross] - point[c][cross] + point[a][cross]
            + point[f][s] - point[e][s])


def exact_budget(B, C, b, u, v, masks, fixed=None, work_limit=5000000):
    """Literal reference DP. The work cap is operational, never an exclusion."""
    T, ds, fixed = validate(B, C, b, u, v, fixed)
    validate_masks(T, C, masks)
    choices = tuple((fixed[d][1],) if d in fixed else range(d) for d in ds)
    jobs = T * (7 ** len(ds) - 1)
    for rs in choices:
        jobs *= len(rs)
    require(jobs <= work_limit, "reference work cap; no conclusion about covers")
    footprints_u = footprints(C, ds, u)
    best = None
    for rs in product(*choices):
        tables = []
        for q in range(T):
            def periodic(C, ds, rs, mask, js, weights):
                return literal_charge(C, ds, rs, mask, js, weights, masks[q])
            tables.append(local_table(B, C, b, ds, rs, q, footprints_u, v, fixed, periodic))
        value = subset_dp(tables, len(ds))
        best = value if best is None else max(best, value)
    return best


def actual_value(B, C, b, u, v, masks, phases):
    T, ds, _ = validate(B, C, b, u, v)
    validate_masks(T, C, masks)
    require(len(phases) == len(ds), "incomplete top phase assignment")
    require(all(type(t) is int and type(r) is int and 0 <= t < B and 0 <= r < d
                for d, (t, r) in zip(ds, phases)), "invalid actual top phase")
    ordinary = sum(u[t][z] for d, (t, r) in zip(ds, phases) for z in range(r, C, d))
    periodic = 0
    for q in range(T):
        for z in range(C):
            h = 0
            for d, (t, r) in zip(ds, phases):
                if t % T == q and z % d == r:
                    h |= 1 << (t // T)
            periodic += DELTA[masks[q][z]][h] * v[q % b][z]
    return ordinary + periodic


def coefficient_row(B, C, b, masks, phases):
    """Unfolded linear coefficients of one witnessed row of the K_U maximum.

    Preserve these original-coordinate coefficients in a cutting-plane model;
    this routine does not impose symmetry on any future weight vector.
    """
    T, ds, _ = validate(B, C, b, [[0] * C for _ in range(B)], [[0] * C for _ in range(b)])
    validate_masks(T, C, masks)
    require(len(phases) == len(ds) and all(0 <= t < B and 0 <= r < d
                for d, (t, r) in zip(ds, phases)), "invalid coefficient-row phases")
    cu, cv = [[0] * C for _ in range(B)], [[0] * C for _ in range(b)]
    for d, (t, r) in zip(ds, phases):
        for z in range(r, C, d):
            cu[t][z] += 1
    for q in range(T):
        for z in range(C):
            h = 0
            for d, (t, r) in zip(ds, phases):
                if t % T == q and z % d == r:
                    h |= 1 << (t // T)
            cv[q % b][z] += DELTA[masks[q][z]][h]
    return cu, cv


def known_data(B, C, anchors):
    """Literal known OUTSIDE union masks and multiplicities in actual CRT blocks.

    Prescribed top classes are deliberately excluded; they enter the top set H.
    """
    N, T = B * C, B // 6
    require(type(B) is int and B >= 6 and B % 6 == 0 and type(C) is int
            and C >= 1 and gcd(B, C) == 1, "invalid known-block domain")
    rest = B
    for p in (2, 3):
        while rest % p == 0:
            rest //= p
    require(rest == 1, "known B prime support must be {2,3}")
    anchors = tuple(tuple(pair) for pair in anchors)
    require(len({n for n, _ in anchors}) == len(anchors), "repeated known modulus")
    require(all(type(n) is int and type(a) is int and n > 0 and N % n == 0 and 0 <= a < n
                for n, a in anchors), "invalid known class")
    outside = [(n, a) for n, a in anchors if gcd(n, B) != B]
    inverse = pow(B, -1, C) if C > 1 else 0
    masks, multiplicities = [], []
    for q in range(T):
        mr, sr = [], []
        for z in range(C):
            mask, total = 0, 0
            for j in range(6):
                t = q + T * j
                x = t + B * (((z - t) * inverse) % C)
                k = sum(x % n == a for n, a in outside)
                total += k
                if k == 0:
                    mask |= 1 << j
            mr.append(mask)
            sr.append(total)
        masks.append(mr)
        multiplicities.append(sr)
    return masks, multiplicities


def encode(B, b, u, v, masks, fixed):
    validate(B, 35, b, u, v, fixed)
    validate_masks(B // 6, 35, masks)
    return old_encode(B, b, u, v, fixed) + " ".join(str(x) for row in masks for x in row) + "\n"


def run(exe, B, b, u, v, masks, fixed=None, quotient=True):
    fixed = {} if fixed is None else fixed
    completed = subprocess.run([str(exe)] + (["--orbits"] if quotient else []),
                               input=encode(B, b, u, v, masks, fixed), text=True,
                               capture_output=True, check=True, timeout=50)
    result = json.loads(completed.stdout)
    require((result["B"], result["C"], result["b"]) == (B, 35, b), "metadata mismatch")
    require(len(result["phases"]) == 4, "incomplete phase witness")
    phases = []
    for d, (dd, t, r) in zip((1, 5, 7, 35), result["phases"]):
        require(dd == d and 0 <= t < B and 0 <= r < d, "invalid optimizer phase")
        require(d not in fixed or (t, r) == fixed[d], "prescribed phase changed")
        phases.append((t, r))
    require(actual_value(B, 35, b, u, v, masks, phases) == result["value"],
            "literal top witness score mismatch")
    return result
