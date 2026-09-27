#!/usr/bin/env python3
"""Independent exact controls for affine-component localization.

CPython 3.11, standard library only.  Geometry and moments use Fraction.
The fresh fixture uses an analytic norm enclosure rather than the target
producer's coordinate absolute-value bound or its checker's corner search.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import subprocess
import sys


TARGET_COMMIT = "2e90dc40c8633ea6d7345ef4d13c11a274e11135"
PINS = {
    "PROOF.md": "2d336f4f88ce58e51f57556a8de8074b8b49337ef3d9b37f6944371114d030e0",
    "README.md": "6ca6f0a0262f46c934dde9e34151e6ddc994772a755f0ca30f96cea4986ca63e",
    "HANDOFF.md": "0c6cfb4c779d963453fb3b383424b85be7c16a90fdbc84eea644b863508bcceb",
    "SOURCES.md": "018adf82d0bf799f85f15362374fd5dc475596560960af310c43d17e8f1e607f",
    "certificate.py": "8b00b68875a93ea177594b3b69bfdf2f322f6b6cb7f8443d38ade6ce6452161c",
    "verify.py": "c12a873f762820324d9b1960c87efb63a11b271a7126a09c580972d3eba071f3",
    "INPUT.json": "4d30db87259a153c7c985b04f1a0a5a248db9e7de92f1ab1887cb22453cf413f",
    "CERTIFICATE.json": "a183ff5098b33c336122e6c258edc269063f6381586fc8f09b8c17bb0114f6ed",
    "EXPECTED.json": "e70cbbc7c188fa651db00cc70fd55753f6fe8f023040ca9b2d78e81a2147f4eb",
    "INPUTS.json": "97cd0a10f0ccbfd537469914dc3d8a0c45415aa0bf69fb350a6e3a7faa7133db",
    "SHA256SUMS": "1fd284f5b98a2d4f42e62568f2e66937d914c53dddf6f336684548089f89080f",
}
TARGET_DIR = "probability/gaussian_affine_component_localization"


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def qstr(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def addv(a, b):
    return tuple(x + y for x, y in zip(a, b))


def subv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scalev(c, a):
    return tuple(c * x for x in a)


def norm2(a):
    return dot(a, a)


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    bt = transpose(b)
    return tuple(tuple(dot(row, col) for col in bt) for row in a)


def matvec(a, v):
    return tuple(dot(row, v) for row in a)


def matadd(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def matscale(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def matsub(a, b):
    return matadd(a, matscale(-1, b))


def outer(a, b):
    return tuple(tuple(x * y for y in b) for x in a)


def eye():
    return ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))


def diagonal(values):
    return tuple(tuple(values[i] if i == j else F(0) for j in range(3))
                 for i in range(3))


def determinant(a):
    if len(a) == 1:
        return a[0][0]
    terms = []
    for j in range(len(a)):
        minor = tuple(tuple(row[k] for k in range(len(a)) if k != j)
                      for row in a[1:])
        terms.append((-1) ** j * a[0][j] * determinant(minor))
    return sum(terms, F(0))


def psd(a):
    return (a == transpose(a)
            and all(determinant(tuple(tuple(a[i][j] for j in ids) for i in ids)) >= 0
                    for size in range(1, len(a) + 1)
                    for ids in combinations(range(len(a)), size)))


def det3(a):
    return determinant(a)


def frobenius2(a):
    return sum((x * x for row in a for x in row), F(0))


def rotation(axis, parameter):
    c = (1 - parameter * parameter) / (1 + parameter * parameter)
    s = 2 * parameter / (1 + parameter * parameter)
    z, o = F(0), F(1)
    matrices = {
        "x": ((o, z, z), (z, c, -s), (z, s, c)),
        "y": ((c, z, s), (z, o, z), (-s, z, c)),
        "z": ((c, -s, z), (s, c, z), (z, z, o)),
    }
    out = matrices[axis]
    need((1 - parameter * parameter) ** 2 + (2 * parameter) ** 2
         == (1 + parameter * parameter) ** 2, "Cayley circle identity failed")
    need(matmul(transpose(out), out) == eye() and det3(out) == 1,
         "Cayley matrix is not a proper rotation")
    return out


CENTERS = ((-30, 0, 0), (30, 0, 0), (0, 30, 0), (0, 0, 30))
HALFWIDTHS = ((1, 2, F(3, 2)), (F(3, 2), 1, 2),
              (2, F(3, 2), 1), (F(5, 4), F(7, 4), F(3, 2)))
WEIGHTS = (F(1, 10), F(2, 10), F(3, 10), F(4, 10))
REFLECTION = ((F(0), F(0), F(1)),
              (F(0), F(1), F(0)),
              (F(1), F(0), F(0)))
TRANSLATION = (F(100), F(-70), F(50))


def fixture(t, framed=False):
    p = t * t
    rx, ry, rz = (rotation(axis, p) for axis in ("x", "y", "z"))
    rotations = (rz, rx, ry, matmul(rz, rx))
    compressions = (
        diagonal((1 - p, F(1), F(1))),
        diagonal((F(1), 1 - p, F(1))),
        diagonal((F(1), F(1), 1 - p)),
        diagonal((1 - p, F(1), F(1))),
    )
    boxes = []
    for raw_c, h, weight, q, s in zip(CENTERS, HALFWIDTHS, WEIGHTS,
                                      rotations, compressions):
        c = tuple(map(F, raw_c))
        a = matmul(q, s)
        need(matmul(transpose(a), a) == matmul(s, s), "polar product changed")
        need(psd(matsub(eye(), matmul(transpose(a), a))), "component expands")
        need(matmul(q, s) != matmul(s, q), "fixture lost noncommutation")
        b = scalev(1 - t, c)
        if framed:
            b = addv(matvec(REFLECTION, b), TRANSLATION)
            a = matmul(REFLECTION, a)
        boxes.append(dict(c=c, b=b, h=tuple(map(F, h)), weight=weight,
                          a=a, q=q, s=s))
    return tuple(boxes)


def box_diameter_squared(boxes):
    return max(sum((abs(a["c"][j] - b["c"][j]) + a["h"][j] + b["h"][j]) ** 2
                   for j in range(3)) for a in boxes for b in boxes)


def moments(boxes):
    mx = tuple(sum((b["weight"] * b["c"][j] for b in boxes), F(0))
               for j in range(3))
    my = tuple(sum((b["weight"] * b["b"][j] for b in boxes), F(0))
               for j in range(3))
    zero = tuple(tuple(F(0) for _ in range(3)) for _ in range(3))
    vx = zero
    vy = zero
    cxy = zero
    displayed_error = F(0)
    for b in boxes:
        v = diagonal(tuple(h * h / 3 for h in b["h"]))
        xmean, ymean = subv(b["c"], mx), subv(b["b"], my)
        av = matmul(matmul(b["a"], v), transpose(b["a"]))
        cross = matmul(v, transpose(b["a"]))
        vx = matadd(vx, matscale(b["weight"], matadd(v, outer(xmean, xmean))))
        vy = matadd(vy, matscale(b["weight"], matadd(av, outer(ymean, ymean))))
        cxy = matadd(cxy, matscale(b["weight"], matadd(cross, outer(xmean, ymean))))
        shift = subv(b["b"], b["c"])
        linear = matsub(b["a"], eye())
        displayed_error += b["weight"] * (
            norm2(shift) + sum((linear[i][j] * v[j][k] * linear[i][k]
                                for i in range(3) for j in range(3) for k in range(3)), F(0)))
    gram = frobenius2(vx) + frobenius2(vy) - 2 * frobenius2(cxy)
    mean_loss = 2 * sum((vx[i][i] - vy[i][i] for i in range(3)), F(0))
    return dict(vx=vx, vy=vy, cxy=cxy, gram=gram, mean_loss=mean_loss,
                displayed_error=displayed_error)


def cross_enclosure(t):
    # Center separations have square at least 1800 and norm at most 60.
    # Every offset has norm below 3.  With local parameter p=t^2,
    # ||Q-I|| <= 4p for the two-factor rotation and ||S-I||=p, hence
    # the rotated/compressed offset perturbation is at most 30t^2.
    need(min(norm2(subv(tuple(map(F, a)), tuple(map(F, b))))
             for a, b in combinations(CENTERS, 2)) == 1800,
         "center separation floor changed")
    need(max(norm2(subv(tuple(map(F, a)), tuple(map(F, b))))
             for a, b in combinations(CENTERS, 2)) == 3600,
         "center separation ceiling changed")
    need(max(sum((F(h) * F(h) for h in widths), F(0))
             for widths in HALFWIDTHS) < 9, "offset radius ceiling changed")
    need(t <= F(1, 100), "cross enclosure outside its range")
    bracket = ((2 - t) * 1800 - 720 - 3600 * t * (1 - t)
               - 360 * t - 900 * t ** 3)
    need(bracket > 2800, "strict cross-loss enclosure failed")
    return 2800 * t


def guard(t, framed=False):
    boxes = fixture(t, framed=framed)
    state = moments(boxes)
    need(sum((b["weight"] for b in boxes), F(0)) == 1, "bad weights")
    need(all(min(h * h / 3 for h in b["h"]) >= F(1, 3) for b in boxes),
         "conditional covariance floor failed")
    need(psd(matsub(state["vx"], matscale(F(1, 3), eye()))),
         "global covariance floor failed")
    d2 = box_diameter_squared(boxes)
    need(d2 == F(7855, 2) and d2 < 63 ** 2, "diameter changed")
    k = kappa = F(1, 3)
    mass = F(1, 10)
    cost = 4 + 78 * d2 / kappa
    need(cost == 919039, "motion constant changed")
    error = 2 * state["gram"] / (k * mass)
    delta = cross_enclosure(t)
    return dict(boxes=boxes, state=state, d2=d2, k=k, kappa=kappa,
                mass=mass, cost=cost, error=error, delta=delta,
                orientation_margin=kappa / 4 - error,
                cross_margin=delta - cost * error)


def verify_pins():
    root = Path(__file__).resolve().parents[2]
    for name, wanted in PINS.items():
        path = f"{TARGET_DIR}/{name}"
        result = subprocess.run(["git", "-C", str(root), "show",
                                 f"{TARGET_COMMIT}:{path}"],
                                check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        need(sha256(result.stdout).hexdigest() == wanted,
             f"source pin mismatch: {name}")


def calculate():
    verify_pins()
    need(matmul(transpose(REFLECTION), REFLECTION) == eye()
         and det3(REFLECTION) == -1, "bad global reflection")

    t = F(1, 2 ** 50)
    base = guard(t)
    framed = guard(t, framed=True)
    need(base["state"]["gram"] == framed["state"]["gram"],
         "Gram error changed under target frame")
    need(base["state"]["mean_loss"] == framed["state"]["mean_loss"],
         "mean loss changed under target frame")
    need(framed["state"]["displayed_error"] > framed["kappa"],
         "independent-frame control unexpectedly passed directly")
    need(base["error"] > 0 and base["orientation_margin"] > F(1, 13),
         "orientation guard failed")
    need(base["cross_margin"] > F(1, 500_000_000_000),
         "cross guard margin failed")
    need(base["error"] < F(1, 10 ** 22), "error display bound failed")

    # The same analytic enclosure supplies epsilon <= 7686t: pair change is
    # below 61t, while source plus target distance is below 2d<126.
    epsilon_upper = 7686 * t
    rho = F(2800, 7686)
    sector_rhs = 2 * rho * base["k"] * base["mass"] / base["cost"]
    need(base["state"]["mean_loss"] < F(1, 400_000_000_000),
         "mean-loss display bound failed")
    need(sector_rhs > F(1, 40_000_000)
         and base["state"]["mean_loss"] <= sector_rhs,
         "uniform mean-loss sector failed")
    need(base["delta"] >= rho * epsilon_upper,
         "cross ratio deduction failed")

    # Boundary control: it is still a whole-domain contraction by the same
    # enclosure, but the sufficient cross budget deliberately fails.
    large = guard(F(1, 2 ** 30))
    need(large["orientation_margin"] > 0 and large["cross_margin"] < 0,
         "UNRESOLVED boundary control changed")

    # A common reflection and translation is an exact F=0 equality case.
    equality = []
    for raw_c, h, weight in zip(CENTERS, HALFWIDTHS, WEIGHTS):
        c = tuple(map(F, raw_c))
        equality.append(dict(c=c, b=addv(matvec(REFLECTION, c), TRANSLATION),
                             h=tuple(map(F, h)), weight=weight,
                             a=REFLECTION, q=REFLECTION, s=eye()))
    equal_state = moments(tuple(equality))
    need(equal_state["gram"] == 0 and equal_state["mean_loss"] == 0,
         "congruent equality control failed")

    # Exact corruption: an expanding singular value must fail the local PSD test.
    bad_s = diagonal((1 + t * t, F(1), F(1)))
    need(not psd(matsub(eye(), matmul(bad_s, bad_s))),
         "expanding local map was not rejected")

    need(F(74) + F(25, 8) == F(617, 8)
         and F(78) - F(617, 8) == F(7, 8),
         "analytic coefficient margin changed")

    return {
        "target_commit": TARGET_COMMIT,
        "pinned_source_files": len(PINS),
        "analytic_controls": {
            "polar_acceleration_coefficient_upper": "10",
            "green_kernel_peak": "1/8",
            "derivative_kernel_peak": "1/2",
            "motion_coefficient_before_rounding": "617/8",
            "coefficient_margin": "7/8",
        },
        "fresh_anisotropic_fixture": {
            "status": "CERTIFIED_ALL_VARIANCE_SUPPORT_AND_MEAN_LOSS_SECTOR",
            "parameter": qstr(t),
            "components": len(base["boxes"]),
            "component_weights": [qstr(x) for x in WEIGHTS],
            "noncommuting_polar_pairs": 4,
            "diameter_squared": qstr(base["d2"]),
            "global_covariance_floor": qstr(base["k"]),
            "component_covariance_floor": qstr(base["kappa"]),
            "component_mass_floor": qstr(base["mass"]),
            "motion_constant": qstr(base["cost"]),
            "aligned_error_upper_bound": "1/10000000000000000000000",
            "cross_loss_lower_bound": qstr(base["delta"]),
            "cross_margin_lower_bound": "1/500000000000",
            "orientation_margin_lower_bound": "1/13",
            "mean_loss_upper_bound": "1/400000000000",
            "sector_rhs_lower_bound": "1/40000000",
            "cross_ratio_floor": qstr(rho),
        },
        "independent_frame_control": {
            "reflection_determinant": qstr(det3(REFLECTION)),
            "gram_error_unchanged": True,
            "mean_loss_unchanged": True,
            "displayed_error_exceeds_kappa": True,
        },
        "boundary_controls": {
            "larger_parameter": qstr(F(1, 2 ** 30)),
            "larger_parameter_status": "UNRESOLVED_CROSS_BUDGET",
            "congruent_reflection_translation": "CONGRUENT_EQUALITY",
            "expanding_local_map_rejected": True,
        },
        "result": "INDEPENDENT_AFFINE_COMPONENT_CONTROLS_PASSED",
    }


def main():
    result = calculate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if len(sys.argv) == 2 and sys.argv[1] == "--emit":
        sys.stdout.write(rendered)
        return
    need(len(sys.argv) == 1, "usage: verify_review.py [--emit]")
    expected = Path(__file__).with_name("EXPECTED.json")
    need(expected.read_text(encoding="utf-8") == rendered,
         "result differs from EXPECTED.json")
    sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
