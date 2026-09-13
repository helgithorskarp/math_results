#!/usr/bin/env python3
"""Independent exact check of the three-vector radius-rigidity claim.

This reconstruction does not read the author's certificate or import its code.
It forms the 32 systems directly in Q[a,b,c,d], computes a fresh lexicographic
Groebner basis with SymPy, and checks the claimed radius consequences by exact
normal-form reduction.
"""

from itertools import combinations, product
import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


a, b, c, d = sp.symbols("a b c d")
VARIABLES = (d, c, b, a)
EISENSTEIN_UNITS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
HERE = Path(__file__).resolve().parent


def add(x, y):
    return (sp.expand(x[0] + y[0]), sp.expand(x[1] + y[1]))


def scale(k, x):
    return (sp.expand(k * x[0]), sp.expand(k * x[1]))


def multiply(x, y):
    # x[0] + i*sqrt(3)*x[1], and likewise for y.
    return (
        sp.expand(x[0] * y[0] - 3 * x[1] * y[1]),
        sp.expand(x[0] * y[1] + x[1] * y[0]),
    )


def squared_modulus(x):
    return sp.expand(x[0] ** 2 + 3 * x[1] ** 2)


def system(signs):
    epsilon, sigma, tau, kappa, lam = signs
    U = (a, b)
    V = (1 - a, -b)
    W = (c, d)
    omega = (sp.Rational(1, 2), sp.Rational(1, 2))
    omega2 = (sp.Rational(-1, 2), sp.Rational(1, 2))
    forms = (
        add(U, W),
        add(V, scale(epsilon, W)),
        add(add(U, scale(sigma, multiply(omega, V))), scale(tau, multiply(omega2, W))),
        add(add(U, scale(kappa, multiply(omega2, V))), scale(lam, multiply(omega, W))),
    )
    equations = [sp.expand(squared_modulus(x) - 1) for x in forms]
    radii = tuple(map(squared_modulus, (U, V, W)))
    return equations, radii


def reduce_zero(groebner, polynomial):
    return sp.Poly(groebner.reduce(sp.expand(polynomial))[1], *VARIABLES, domain=sp.QQ).is_zero


def eisenstein_add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def eisenstein_multiply(x, y):
    # Here x=(m,n) denotes m+n*omega, with omega^2=omega-1.
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0] + x[1] * y[1])


def eisenstein_norm(x):
    return x[0] ** 2 + x[0] * x[1] + x[1] ** 2


def canonical_row(row):
    return min(tuple(eisenstein_multiply(unit, entry) for entry in row) for unit in EISENSTEIN_UNITS)


def f4_multiply(x, y):
    out = 0
    while y:
        if y & 1:
            out ^= x
        y >>= 1
        x <<= 1
        if x & 4:
            x ^= 7
    return out


def f4_projectivize(row):
    pivot = next(x for x in row if x)
    inverse = next(x for x in (1, 2, 3) if f4_multiply(pivot, x) == 1)
    return tuple(f4_multiply(x, inverse) for x in row)


def residue(x):
    return (x[0] & 1) + 2 * (x[1] & 1)


def template_rows(signs):
    epsilon, sigma, tau, kappa, lam = signs
    one, zero = (1, 0), (0, 0)
    omega, omega2 = (0, 1), (-1, 1)
    return tuple(sorted(map(canonical_row, (
        (one, one, zero),
        (one, zero, one),
        (zero, one, (epsilon, 0)),
        (one, eisenstein_multiply((sigma, 0), omega), eisenstein_multiply((tau, 0), omega2)),
        (one, eisenstein_multiply((kappa, 0), omega2), eisenstein_multiply((lam, 0), omega)),
    ))))


def finite_normalization_audit():
    entries = ((0, 0),) + EISENSTEIN_UNITS
    rows = sorted({canonical_row(row) for row in product(entries, repeat=3)
                   if sum(x != (0, 0) for x in row) >= 2})
    if len(rows) != 54:
        raise AssertionError(len(rows))
    buckets = {}
    for row in rows:
        normal = f4_projectivize(tuple(map(residue, row)))
        buckets.setdefault(normal, []).append(row)
    if len(buckets) != 18:
        raise AssertionError(len(buckets))
    vectors = list(product(range(4), repeat=3))
    hyperplanes = {
        normal: {v for v in vectors if f4_multiply(normal[0], v[0]) ^
                 f4_multiply(normal[1], v[1]) ^ f4_multiply(normal[2], v[2]) == 0}
        for normal in buckets
    }
    pencils = [selection for selection in combinations(sorted(buckets), 5)
               if set().union(*(hyperplanes[n] for n in selection)) == set(vectors)]
    if len(pencils) != 9:
        raise AssertionError(len(pencils))
    templates = {template_rows(signs): signs for signs in product((-1, 1), repeat=5)}
    if len(templates) != 32:
        raise AssertionError("templates collide")
    sign_counts = {signs: 0 for signs in templates.values()}
    gauge_checks = 0
    lifts = 0
    for pencil in pencils:
        if sorted(len(buckets[x]) for x in pencil) != [2, 2, 2, 4, 4]:
            raise AssertionError("bucket sizes")
        for lift in product(*(buckets[x] for x in pencil)):
            found = set()
            for alpha, beta in product(EISENSTEIN_UNITS, repeat=2):
                gauge_checks += 1
                transformed = tuple(sorted(canonical_row(
                    (row[0], eisenstein_multiply(alpha, row[1]), eisenstein_multiply(beta, row[2]))
                ) for row in lift))
                if transformed in templates:
                    found.add(templates[transformed])
            if len(found) != 1:
                raise AssertionError((lift, found))
            sign_counts[found.pop()] += 1
            lifts += 1
    if lifts != 1152 or gauge_checks != 41472 or set(sign_counts.values()) != {36}:
        raise AssertionError((lifts, gauge_checks, sign_counts))
    return pencils, {
        "projective_pencils": len(pencils), "unit_lifts": lifts,
        "normalized_sign_cases": len(sign_counts), "lifts_per_case": 36,
        "diagonal_gauges_checked": gauge_checks,
    }


def all_unit_audit():
    considered = 0
    survivors = []
    omega, omega2 = (0, 1), (-1, 1)
    for signs in product((-1, 1), repeat=5):
        epsilon, sigma, tau, kappa, lam = signs
        for U, V, W in product(EISENSTEIN_UNITS, repeat=3):
            if eisenstein_add(U, V) != (1, 0):
                continue
            considered += 1
            forms = (
                eisenstein_add(U, W),
                eisenstein_add(V, eisenstein_multiply((epsilon, 0), W)),
                eisenstein_add(eisenstein_add(U, eisenstein_multiply((sigma, 0), eisenstein_multiply(omega, V))),
                                eisenstein_multiply((tau, 0), eisenstein_multiply(omega2, W))),
                eisenstein_add(eisenstein_add(U, eisenstein_multiply((kappa, 0), eisenstein_multiply(omega2, V))),
                                eisenstein_multiply((lam, 0), eisenstein_multiply(omega, W))),
            )
            if all(eisenstein_norm(x) == 1 for x in forms):
                survivors.append((signs, U, V, W))
    if considered != 384 or survivors:
        raise AssertionError((considered, survivors))
    return {"unit_boundary_cases": considered, "unit_boundary_survivors": 0}


def residual_audit(pencils, residual_path):
    residual = json.loads(Path(residual_path).read_text())
    canonical_digest = hashlib.sha256(
        json.dumps(residual, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if canonical_digest != "42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d":
        raise AssertionError(canonical_digest)
    embedded = set()
    for support in combinations(range(4), 3):
        for pencil in pencils:
            lifted = []
            for normal in pencil:
                vector = [0] * 4
                for index, value in zip(support, normal):
                    vector[index] = value
                lifted.append((tuple(vector), 0))
            embedded.add(tuple(sorted(lifted)))
    selected = []
    for index, pencil in enumerate(residual["remaining_pencil_signatures"]):
        canonical = tuple(sorted((tuple(normal), constant) for normal, constant in pencil))
        support = {i for normal, _ in canonical for i, value in enumerate(normal) if value}
        if all(constant == 0 for _, constant in canonical) and len(support) == 3:
            if canonical not in embedded:
                raise AssertionError((index, canonical))
            selected.append(index)
    if len(embedded) != 36 or len(selected) != 24:
        raise AssertionError((len(embedded), len(selected)))
    return {"a5_three_position_pencils": len(embedded), "h4195_residual_pencils": len(selected),
            "h4195_residual_indices_sha256": hashlib.sha256(json.dumps(selected).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-digest", default="")
    parser.add_argument("--residual", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    transcript = []
    counts = {"equal": 0, "exceptional": 0}
    for signs in product((-1, 1), repeat=5):
        equations, (u, v, w) = system(signs)
        basis = sp.groebner(equations, *VARIABLES, order="grevlex", domain=sp.QQ)
        delta = sp.expand((u - v) * (u - w) * (v - w))
        if reduce_zero(basis, delta):
            classification = "equal"
            consequences = [True]
        else:
            polynomial = lambda t: (4 * t - 1) * (4 * t - 3) * (4 * t - 7)
            consequences = [reduce_zero(basis, delta * polynomial(t)) for t in (u, v, w)]
            if not all(consequences):
                raise AssertionError(f"unproved radius claim for signs={signs}: {consequences}")
            classification = "exceptional"
        counts[classification] += 1
        transcript.append({
            "signs": list(signs),
            "classification": classification,
            "basis_size": len(basis.polys),
            "basis_digest": hashlib.sha256(
                "\n".join(str(p.as_expr()) for p in basis.polys).encode()
            ).hexdigest(),
        })
    if counts != {"equal": 20, "exceptional": 12}:
        raise AssertionError(counts)
    digest = hashlib.sha256(
        json.dumps(transcript, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    if args.expected_digest and digest != args.expected_digest:
        raise AssertionError((digest, args.expected_digest))
    pencils, normalization = finite_normalization_audit()
    result = {"status": "PASS", "radius_cases": counts, "groebner_transcript_sha256": digest,
              **normalization, **all_unit_audit()}
    if args.residual:
        result.update(residual_audit(pencils, args.residual))
    if args.check_expected:
        expected = HERE / ("EXPECTED_WITH_RESIDUAL.json" if args.residual else "EXPECTED.json")
        if result != json.loads(expected.read_text()):
            raise AssertionError("expected output mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
