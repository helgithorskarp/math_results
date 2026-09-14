"""Exact fixed-phase contact inventory for M + eta^3 M + v M."""

from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sys

DEPENDENCY = Path(__file__).resolve().parent.parent / "hadwiger_nelson_independent_moser_sum_collisions"
sys.path.insert(0, str(DEPENDENCY))

import arithmetic as K  # noqa: E402
from family import (  # noqa: E402
    ONE,
    ZERO,
    add,
    inv,
    mul,
    norm,
    product,
    require,
    scale,
    sign,
    spindle,
    sub,
)
from local import f_local  # noqa: E402


def fixed_case():
    """Return the complete exact exceptional inventory at u=eta^3."""
    M = spindle()
    eta = M[4]
    u = mul(mul(eta, eta), eta)
    require(norm(u) == ONE, "u is unit")
    B = sorted({add(a, mul(u, b)) for a, b in product(M, repeat=2)})
    require(len(B) == 49, "the M+eta^3 M representation must be injective")
    for point in B + M:
        K.residue(point)

    Db = K.differences(B)
    Dm = K.differences(M)
    db = [a for a in Db if a != ZERO]
    dm = [b for b in Dm if b != ZERO]
    Na = {a: norm(a) for a in db}
    Nb = {b: norm(b) for b in dm}
    shapes = {}
    for an, bn in product(set(Na.values()), set(Nb.values())):
        S = sub(add(an, bn), ONE)
        if S == ZERO:
            shapes[an, bn] = ("trace_zero", None)
            continue
        va = f_local(an)[0]
        vb = f_local(bn)[0]
        require(va % 2 == vb % 2 == 0, "norm valuation parity")
        valuation = f_local(S)[0] - (va + vb) // 2
        if valuation >= -1:
            shapes[an, bn] = ("trace_ge_minus1", None)
            continue
        delta = sub(scale(mul(an, bn), 4), mul(S, S))
        if sign(delta) <= 0:
            shapes[an, bn] = ("nonpositive_delta", None)
            continue
        ss = scale(delta, F(1, 3))
        if K.sqrt_real(ss) is not None:
            shapes[an, bn] = ("base_field_root", None)
            continue
        shapes[an, bn] = ("event", (S, ss, valuation))

    inverse_a = {a: inv(a) for a in db}
    inverse_b = {b: inv(b) for b in dm}
    groups = {}
    stats = Counter()
    for a, b in product(db, dm):
        kind, extra = shapes[Na[a], Nb[b]]
        stats[kind] += 1
        if kind != "event":
            continue
        S, ss, valuation = extra
        ci = mul(K.conj(inverse_a[a]), inverse_b[b])
        T = scale(mul(S, ci), -1)
        J = mul(mul(a, K.conj(b)), ci)
        key = (T, J)
        row = groups.setdefault(
            key,
            {
                "ss": ss,
                "witness": (a, b),
                "directions": [],
                "trace_valuation": valuation,
            },
        )
        require(row["ss"] == ss, "radicand must be constant on a contact group")
        require(row["trace_valuation"] == valuation, "valuation must be constant on a contact group")
        row["directions"].append((a, b))

    baseline = set()
    for i, a in enumerate(B):
        for j, b in enumerate(M):
            for ii in range(i + 1, len(B)):
                if norm(sub(a, B[ii])) == ONE:
                    baseline.add((7 * i + j, 7 * ii + j))
            for jj in range(j + 1, 7):
                if norm(sub(b, M[jj])) == ONE:
                    baseline.add((7 * i + j, 7 * i + jj))
    return u, B, Db, Dm, sorted(groups.items()), sorted(baseline), dict(stats)


def serial_element(z):
    return [str(x) for x in z]


def serial_inventory(u, groups):
    return {
        "u": serial_element(u),
        "groups": [
            {
                "key": [serial_element(z) for z in key],
                "ss": serial_element(group["ss"]),
                "trace_valuation": group["trace_valuation"],
                "directions": [
                    [serial_element(a), serial_element(b)] for a, b in group["directions"]
                ],
            }
            for key, group in groups
        ],
    }
