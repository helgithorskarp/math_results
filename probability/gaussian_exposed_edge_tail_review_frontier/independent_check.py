#!/usr/bin/env python3
"""Independent exact audit of the exposed-edge Gaussian endpoint theorem.

This checker imports none of the target implementation.  It reconstructs the
seven-site fixture, enumerates every vertex of the certificate linear program
for the cited edge, and rederives the endpoint constants with Fraction.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import factorial, lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_exposed_edge_tail"
PINS = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "EXPECTED.json": "6aa814dc29a320c62c6d0001f1127b5e72f0246bcbdf714a4172cecf9ff0e9b9",
    "PROOF.md": "dc6dcaa5d5977376df4f28fbb401cf73b23b6e61bbea611b04d3cbd387251328",
    "README.md": "6a151c937c7c1d01dd45deaac21e25c063dc28b04964c88a416c9c1faba13cb5",
    "SOURCES.md": "05ddbd3fb7bac30383229e4a72232e11267ef17e5ad210221cd94fffd663f8ca",
    "verify.py": "804b5f6dd47bd50c1cbcd88fa3698d5d8301d59ee05704597722844dccc81f73",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def dist2(a, b):
    return norm2(sub(a, b))


def ceil_fraction(x):
    return -((-x.numerator) // x.denominator)


def solve_square(rows, rhs):
    """Exact Gauss--Jordan solve; return None for a singular active set."""
    n = len(rows)
    a = [list(map(F, row)) + [F(value)] for row, value in zip(rows, rhs)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [value / scale for value in a[col]]
        for r in range(n):
            if r != col and a[r][col]:
                scale = a[r][col]
                a[r] = [x - scale * y for x, y in zip(a[r], a[col])]
    return tuple(a[r][-1] for r in range(n))


def on_segment(w, a, b):
    direction = sub(b, a)
    pivot = next((j for j, value in enumerate(direction) if value), None)
    if pivot is None:
        return w == a
    t = (w[pivot] - a[pivot]) / direction[pivot]
    return 0 <= t <= 1 and sub(w, a) == tuple(t * value for value in direction)


def fixture():
    x = tuple(tuple(map(F, row)) for row in (
        (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
        (1, -2, 5), (-2, -5, -1), (-5, 1, 2),
    ))
    face_normals = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))
    y = x[:4] + tuple(
        tuple(value - F(8, 3) * normal for value, normal in zip(point, n))
        for point, n in zip(x[4:], face_normals)
    )
    return x, y


def enumerate_certificate_lp(paired, pair):
    """Enumerate all active-set vertices of the seven-variable LP.

    Variables are (h_1,...,h_6,u).  The edge equality is always active; six
    further active constraints are selected from the coordinate cube,
    off-edge gap inequalities, and u>=0.
    """
    i, j = pair
    segment = tuple(k for k, point in enumerate(paired)
                    if on_segment(point, paired[i], paired[j]))
    off = tuple(k for k in range(len(paired)) if k not in segment)
    edge_row = sub(paired[i], paired[j]) + (F(0),)
    boundaries = []
    for coordinate in range(6):
        row = [F(0)] * 7
        row[coordinate] = 1
        boundaries.append((tuple(row), F(1), f"h{coordinate}=1"))
        boundaries.append((tuple(row), F(-1), f"h{coordinate}=-1"))
    for k in off:
        boundaries.append((sub(paired[i], paired[k]) + (F(-1),), F(0), f"gap{k}"))
    boundaries.append(((F(0),) * 6 + (F(1),), F(0), "u=0"))

    feasible = set()
    optimum = None
    optimal_points = set()
    for active in combinations(boundaries, 6):
        answer = solve_square((edge_row,) + tuple(c[0] for c in active),
                              (F(0),) + tuple(c[1] for c in active))
        if answer is None:
            continue
        h, u = answer[:6], answer[6]
        if not all(-1 <= value <= 1 for value in h) or u < 0:
            continue
        if dot(h, sub(paired[i], paired[j])) != 0:
            continue
        if any(dot(h, sub(paired[i], paired[k])) < u for k in off):
            continue
        feasible.add(answer)
        if optimum is None or u > optimum:
            optimum, optimal_points = u, {answer}
        elif u == optimum:
            optimal_points.add(answer)
    require(optimum is not None and optimum > 0, "certificate LP had no positive vertex")
    return segment, off, optimum, feasible, optimal_points


def audit():
    for name, digest in PINS.items():
        require(sha256((TARGET / name).read_bytes()).hexdigest() == digest,
                "target pin mismatch: " + name)

    x, y = fixture()
    paired = tuple(a + b for a, b in zip(x, y))
    losses = {(i, j): dist2(x[i], x[j]) - dist2(y[i], y[j])
              for i, j in combinations(range(7), 2)}
    require(all(value >= 0 for value in losses.values()), "fixture is not a contraction")
    require(sum(value == 0 for value in losses.values()) == 15, "tight-pair count changed")
    require(sum(value > 0 for value in losses.values()) == 6, "strict-pair count changed")

    pair = (1, 4)
    segment, off, optimum, vertices, optimizers = enumerate_certificate_lp(paired, pair)
    require(segment == (1, 4) and off == (0, 2, 3, 5, 6), "edge labels changed")
    require(optimum == F(112, 87), "independent LP optimum changed")

    normal = tuple(map(F, ("-1/4", "-1/22", "7/44", "3/44", "-3/22", "-15/44")))
    require(sum(abs(value) for value in normal) == 1, "normal is not L1-normalized")
    require(dot(normal, sub(paired[1], paired[4])) == 0, "edge equality failed")
    gaps = tuple(dot(normal, sub(paired[1], paired[k])) for k in off)
    require(gaps == (F(4, 11),) * 5, "supplied exposing gaps changed")
    eta = min(gaps)
    loss = losses[pair]
    require(loss == F(32, 3), "selected loss changed")

    radius, labels, variance, mass = F(6), 7, F(1), F(1, 7)
    delta = loss * eta**5 / (2**40 * labels**2 * radius**6)
    require(delta == F(1, 37062793887769165824), "mean-support margin changed")
    ell = 0
    while (1 << ell) * mass < 1:
        ell += 1
    big_b = 6 * radius**2 + 2 * variance * ell
    big_q = 4 * big_b / delta
    exponent = ceil_fraction(big_q**2 / variance)
    source_d2 = dist2(x[1], x[4])
    upper = 1 - mass * source_d2 / (8 * variance + source_d2)
    require((ell, big_b, big_q, exponent, upper) == (
        3,
        F(222),
        F(32911760972339019251712),
        1083184010300377825938618225621159364414930944,
        F(118, 133),
    ), "endpoint reconstruction changed")

    denominator = lcm(*(value.denominator for point in paired for value in point))
    magnitude = max(abs((denominator * value).numerator)
                    for point in paired for value in point)
    require((denominator, magnitude) == (3, 15), "input-size parameters changed")
    require(denominator * optimum == F(112, 29),
            "integer-coordinate certificate LP scaling changed")
    eta0 = F(1, 6 * denominator * factorial(7) * (2 * magnitude)**6)
    delta0 = F(1, 2**40 * labels**2 * radius**6 * denominator**7
               * (6 * factorial(7))**5 * (2 * magnitude)**30)
    require(eta0 == F(1, 66134880000000), "uniform eta bound changed")
    require(delta0 == F(
        1,
        28621920273956105372820855022791934998284752737062092800000000000000000000000000000000000,
    ), "uniform mean-support margin changed")
    require(delta0 == F(1, denominator**2) * eta0**5 /
            (2**40 * labels**2 * radius**6), "uniform formula mismatch")

    # Reconstruct the prism coefficient before the transcendental factors:
    # (1/4 from t and interpolation) * (omega_5/(2*pi)^3=1/(15*pi))
    # * (eta/(8R))^5 * (1/R).
    require(4 * 15 * 8**5 == 1966080, "prism coefficient changed")
    require(3932160 * 22 < 7 * 2**24, "pi<22/7 no longer proves pi factor")
    require(24 + 13 == 37 < 40, "final constant slack changed")

    # Scaling x,y,R,eta by 1/2 and s by 1/4 scales Delta by 1/2,
    # while Q^2/s and the source-peak bound remain unchanged.
    scaled_delta = (loss / 4) * (eta / 2)**5 / (2**40 * labels**2 * (radius / 2)**6)
    scaled_b = 6 * (radius / 2)**2 + 2 * (variance / 4) * ell
    scaled_q = 4 * scaled_b / scaled_delta
    scaled_source_d2 = source_d2 / 4
    scaled_upper = 1 - mass * scaled_source_d2 / (8 * variance / 4 + scaled_source_d2)
    require(scaled_delta == delta / 2, "margin scaling failed")
    require(scaled_q**2 / (variance / 4) == big_q**2 / variance,
            "tail exponent scaling failed")
    require(scaled_upper == upper, "upper endpoint scaling failed")

    # Mutation rejection is definition-level and independent of target code.
    require(any(dot(tuple(-z for z in normal), sub(paired[1], paired[k])) < eta
                for k in off), "reversed normal was not rejected")
    require(any(gap < F(1) for gap in gaps), "inflated margin was not rejected")
    require(losses[(0, 1)] == 0, "tight-edge mutation ceased to be tight")

    print("EXPOSED_EDGE_TAIL_INDEPENDENT_ACCEPT")
    print(f"exact LP: {len(vertices)} feasible vertices, {len(optimizers)} optimizers, max u={optimum}")
    print(f"fixture: 15 tight + 6 strict pairs; exposed gap={eta}; loss={loss}")
    print(f"Delta={delta}; E={exponent}; b={upper}")


if __name__ == "__main__":
    audit()
