#!/usr/bin/env python3
"""Independent exact controls for the convex normal-ray review.

Python >= 3.10, standard library only.  This deliberately imports no code
from gaussian_radial_contractions/check_convex_core.py.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from json import dumps
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_radial_contractions"
PINS = {
    "CONVEX_CORES.md": "83aa49c83c100880029bf61fb8f7db85c1537724ec9283f284a08abe8b454bab",
    "check_convex_core.py": "5ede53585ce470784b40af52e61e037fe02c882dffb7fe682067ea94232dba81",
    "convex_core_expected.json": "127554c450d29b0ceb1c53d79e2dd0ac286c5128d9c711e612204461a45332d8",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rejected(fn):
    try:
        fn()
    except ValueError:
        return 1
    raise ValueError("mutation unexpectedly passed")


def v(*coordinates):
    return tuple(F(x) for x in coordinates)


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def mul(a, x):
    return tuple(a * b for b in x)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def rational_sqrt(x):
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    require(a * a == x.numerator and b * b == x.denominator,
            "fixture did not have rational norm")
    return F(a, b)


def clip(x):
    return max(F(-1), min(F(1), x))


def describe(x, project):
    p = project(x)
    r = rational_sqrt(norm2(sub(x, p)))
    u = mul(1 / r, sub(x, p)) if r else v(0, 0, 0)
    return x, p, r, u


def profiles():
    def mirror(r):
        return r if r <= 1 else max(F(0), 2 - r)

    def inversion(r):
        return r if r <= 1 else 1 / r

    def fold(r):
        z = r % 2
        return min(z, 2 - z)

    return (lambda r: r, lambda r: F(0), mirror, inversion, fold), mirror


def core_fixtures():
    zero = v(0, 0, 0)
    # Each (base, direction) is a certified outward normal ray.  The list is
    # intentionally different from the target checker's fixture table.
    data = [
        ("box", lambda x: tuple(clip(a) for a in x), [
            (v(1, -1, 0), v(F(3, 5), F(-4, 5), 0)),
            (v(-1, -1, 1), v(F(-2, 3), F(-2, 3), F(1, 3))),
            (v(0, 1, 1), v(0, F(5, 13), F(12, 13))),
            (v(-1, 0, 0), v(-1, 0, 0)),
        ]),
        ("segment", lambda x: v(clip(x[0]), 0, 0), [
            (v(F(1, 3), 0, 0), v(0, F(5, 13), F(12, 13))),
            (v(1, 0, 0), v(F(3, 5), F(4, 5), 0)),
            (v(-1, 0, 0), v(F(-4, 5), 0, F(3, 5))),
        ]),
        ("plane", lambda x: v(x[0], x[1], 0), [
            (zero, v(0, 0, 1)),
            (v(2, -1, 0), v(0, 0, -1)),
            (v(-3, 2, 0), v(0, 0, 1)),
        ]),
        ("point", lambda x: zero, [
            (zero, v(F(3, 5), F(4, 5), 0)),
            (zero, v(F(-4, 5), 0, F(3, 5))),
            (zero, v(0, F(-5, 13), F(12, 13))),
        ]),
    ]
    radii = (F(0), F(1, 4), F(2, 3), F(1), F(5, 4), F(7, 4), F(2), F(3))
    answer = []
    for name, project, rays in data:
        points = set()
        for p, u in rays:
            require(project(p) == p and norm2(u) == 1, "bad normal-ray fixture")
            for r in radii:
                x = add(p, mul(r, u))
                require(project(x) == p, "projection fixture failed")
                points.add(x)
        answer.append((name, project, [describe(x, project) for x in sorted(points)]))
    return answer


def lift_square(a, b, rho, t, w):
    _, p, r, u = a
    _, q, s, z = b
    R, S = rho(r), rho(s)
    A, B = (1 - t) * r + t * R, (1 - t) * s + t * S
    fx = add(p, mul(A, u)) + (w * (r - R),)
    fy = add(q, mul(B, z)) + (w * (s - S),)
    return norm2(sub(fx, fy))


def split_square(a, b, rho, t, mutation=0):
    _, p, r, u = a
    _, q, s, z = b
    R, S = rho(r), rho(s)
    A, B = (1 - t) * r + t * R, (1 - t) * s + t * S
    alpha = dot(sub(p, q), u)
    beta = -dot(sub(p, q), z)
    c = dot(u, z)
    require(alpha >= 0 and beta >= 0 and 1 - c >= 0, "normal sign failed")
    result = norm2(sub(p, q)) + 2 * A * alpha + 2 * B * beta
    result += (1 - t) * (r - s) ** 2 + t * (R - S) ** 2
    result += (2 + mutation) * A * B * (1 - c)
    derivative = -2 * (r - R) * alpha - 2 * (s - S) * beta
    derivative += (R - S) ** 2 - (r - s) ** 2
    derivative -= 2 * (1 - c) * ((r - R) * B + (s - S) * A)
    require(derivative <= 0, "distance derivative became positive")
    return result


def geometric_controls(mutation=0):
    ps, mirror = profiles()
    # t=q^2/(1+q^2), sqrt(t(1-t))=q/(1+q^2).
    qw = ((F(0), F(0), F(0)), (F(1, 4), F(1, 17), F(4, 17)),
          (F(1, 2), F(1, 5), F(2, 5)), (F(1), F(1, 2), F(1, 2)),
          (F(2), F(4, 5), F(2, 5)), (None, F(1), F(0)))
    identity_checks = monotone_checks = collar_checks = 0
    per_core = {}
    for name, project, points in core_fixtures():
        for x, p, r, u in points:
            R = mirror(r)
            target = add(p, mul(R, u))
            require(project(target) == p, "normal fibre was not preserved")
            if r <= 2:
                pk = x if r <= 1 else add(p, u)
                require(target == sub(mul(2, pk), x), "collar identity failed")
                collar_checks += 1
        for a, b in combinations(points, 2):
            for rho in ps:
                last = None
                for _, t, w in qw:
                    direct = lift_square(a, b, rho, t, w)
                    split = split_square(a, b, rho, t, mutation)
                    require(direct == split, "lift decomposition failed")
                    require(last is None or direct <= last, "lift was not contracting")
                    last = direct
                    identity_checks += 1
                    monotone_checks += int(t != 0)
        per_core[name] = len(points)
    return per_core, identity_checks, monotone_checks, collar_checks


def cancellation_controls():
    checks = 0
    for f in (F(1, 20), F(1, 3), F(1), F(7, 3), F(9)):
        for h in (F(0), F(1, 10), F(1, 2), F(1), F(3), F(10)):
            conditional = f * max(F(0), 1 - h / f)
            require(conditional == max(F(0), f - h), "Gaussian cancellation failed")
            checks += 1
    # Same-ray target collisions under rho_e=(1-e)rho+e r occur at at
    # most one epsilon; verify the affine equation and avoidance exactly.
    ps, _ = profiles()
    collision_checks = 0
    for rho in ps:
        for r, s in combinations((F(1, 4), F(2, 3), F(5, 4), F(2), F(3)), 2):
            intercept = rho(r) - rho(s)
            slope = (r - s) - intercept
            require(intercept or slope, "collision equation vanished identically")
            forbidden = -intercept / slope if slope else None
            for epsilon in (F(1, 101), F(2, 101), F(3, 101), F(5, 101)):
                if epsilon != forbidden:
                    require(intercept + epsilon * slope != 0,
                            "non-forbidden perturbation collided")
                collision_checks += 1
    return checks, collision_checks


def main():
    for name, digest in PINS.items():
        require(sha256((TARGET / name).read_bytes()).hexdigest() == digest,
                f"source pin mismatch: {name}")
    cores, identities, monotone, collars = geometric_controls()
    mutations = rejected(lambda: geometric_controls(mutation=1))
    cancellations, collisions = cancellation_controls()
    print(dumps({
        "status": "CONVEX_NORMAL_RAY_INDEPENDENT_ACCEPT",
        "source_pins": len(PINS),
        "core_sites": cores,
        "exact_lift_identities": identities,
        "exact_monotonicity_steps": monotone,
        "collar_identities": collars,
        "gaussian_cancellations": cancellations,
        "perturbation_collision_controls": collisions,
        "intentional_rejections": mutations,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
