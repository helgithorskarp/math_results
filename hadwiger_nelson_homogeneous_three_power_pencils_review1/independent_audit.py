#!/usr/bin/env python3
"""Clean-room exact audit of the homogeneous three-power pencil theorem.

This file deliberately imports no code, certificate, interface, or expected
value from the reviewed package.  Its polynomial engine is a small rational
Buchberger implementation using pure lexicographic order D>C>B>A.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path


NVAR = 4
MON_ONE = (0,) * NVAR
P_ONE = {MON_ONE: Q(1)}
U_ZERO = (0, 0)
U_ONE = (2, 0)  # (r,s) represents (r+i*sqrt(3)*s)/2.
UNITS = ((2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def padd(left, right, coefficient=Q(1)):
    out = dict(left)
    for monomial, value in right.items():
        out[monomial] = out.get(monomial, Q(0)) + coefficient * value
        if not out[monomial]:
            del out[monomial]
    return out


def pscale(coefficient, polynomial):
    coefficient = Q(coefficient)
    return {m: coefficient * c for m, c in polynomial.items() if coefficient * c}


def pmul(left, right):
    out = {}
    for m, a in left.items():
        for n, b in right.items():
            monomial = tuple(x + y for x, y in zip(m, n))
            out[monomial] = out.get(monomial, Q(0)) + a * b
    return {m: c for m, c in out.items() if c}


def ppow(polynomial, exponent):
    out = P_ONE
    for _ in range(exponent):
        out = pmul(out, polynomial)
    return out


def pconst(value):
    return pscale(Q(value), P_ONE)


def pvar(index):
    return {tuple(int(i == index) for i in range(NVAR)): Q(1)}


def pmonomial(monomial, coefficient=Q(1)):
    return {tuple(monomial): Q(coefficient)}


def peval(polynomial, values):
    result = Q(0)
    for monomial, coefficient in polynomial.items():
        term = coefficient
        for value, exponent in zip(values, monomial):
            term *= value**exponent
        result += term
    return result


def leading(polynomial):
    monomial = max(polynomial)  # Pure lexicographic D>C>B>A.
    return monomial, polynomial[monomial]


def divides(left, right):
    """Whether monomial left divides monomial right."""
    return all(a <= b for a, b in zip(left, right))


def quotient_monomial(numerator, denominator):
    need(divides(denominator, numerator), "monomial division")
    return tuple(a - b for a, b in zip(numerator, denominator))


def vector_add(left, right, coefficient=Q(1)):
    return [padd(a, b, coefficient) for a, b in zip(left, right)]


def vector_scale_monomial(vector, monomial, coefficient=Q(1)):
    term = pmonomial(monomial, coefficient)
    return [pmul(term, p) for p in vector]


def combine(representation, generators):
    out = {}
    for coefficient, generator in zip(representation, generators):
        out = padd(out, pmul(coefficient, generator))
    return out


def normal_form(polynomial, basis, representation=None):
    """Divide by basis; optionally track an original-generator expression."""
    pending = dict(polynomial)
    remainder = {}
    tracked = None if representation is None else list(representation)
    while pending:
        monomial, coefficient = leading(pending)
        for divisor, divisor_rep in basis:
            dm, dc = leading(divisor)
            if divides(dm, monomial):
                shift = quotient_monomial(monomial, dm)
                factor = coefficient / dc
                pending = padd(pending, pmul(pmonomial(shift, factor), divisor), -1)
                if tracked is not None:
                    tracked = vector_add(
                        tracked,
                        vector_scale_monomial(divisor_rep, shift, factor),
                        -1,
                    )
                break
        else:
            remainder[monomial] = coefficient
            del pending[monomial]
    return remainder, tracked


def buchberger(generators):
    """Exact Buchberger with representation tracking and no pair criteria."""
    basis = []
    for index, generator in enumerate(generators):
        need(generator, "zero defining equation")
        _, coefficient = leading(generator)
        representation = [{} for _ in generators]
        representation[index] = pconst(Q(1, 1) / coefficient)
        basis.append((pscale(Q(1, 1) / coefficient, generator), representation))

    pairs = [(i, j) for j in range(len(basis)) for i in range(j)]
    processed = 0
    while processed < len(pairs):
        i, j = pairs[processed]
        processed += 1
        left, left_rep = basis[i]
        right, right_rep = basis[j]
        lm_left, lc_left = leading(left)
        lm_right, lc_right = leading(right)
        common = tuple(max(a, b) for a, b in zip(lm_left, lm_right))
        shift_left = quotient_monomial(common, lm_left)
        shift_right = quotient_monomial(common, lm_right)
        first = pmul(pmonomial(shift_left, Q(1, 1) / lc_left), left)
        second = pmul(pmonomial(shift_right, Q(1, 1) / lc_right), right)
        s_polynomial = padd(first, second, -1)
        s_rep = vector_add(
            vector_scale_monomial(left_rep, shift_left, Q(1, 1) / lc_left),
            vector_scale_monomial(right_rep, shift_right, Q(1, 1) / lc_right),
            -1,
        )
        remainder, remainder_rep = normal_form(s_polynomial, basis, s_rep)
        need(combine(remainder_rep, generators) == remainder, "tracked S-polynomial")
        if remainder:
            _, coefficient = leading(remainder)
            remainder = pscale(Q(1, 1) / coefficient, remainder)
            remainder_rep = [
                pscale(Q(1, 1) / coefficient, p) for p in remainder_rep
            ]
            new_index = len(basis)
            basis.append((remainder, remainder_rep))
            pairs.extend((i, new_index) for i in range(new_index))

    # Every pair, including every pair created by a new remainder, was reduced
    # in the loop.  Zero remainders were checked through their tracked
    # original-generator expressions, and nonzero remainders created all later
    # pairs.  This is a direct execution of Buchberger's criterion.
    for polynomial, representation in basis:
        need(combine(representation, generators) == polynomial, "basis provenance")
    return basis, processed


def cadd(left, right):
    return padd(left[0], right[0]), padd(left[1], right[1])


def cscale(coefficient, value):
    return pscale(coefficient, value[0]), pscale(coefficient, value[1])


def cmul(left, right):
    return (
        padd(pmul(left[0], right[0]), pmul(left[1], right[1]), -3),
        padd(pmul(left[0], right[1]), pmul(left[1], right[0])),
    )


def cnorm(value):
    return padd(pmul(value[0], value[0]), pmul(value[1], value[1]), 3)


def equations(signs):
    """Four norm equations after U+V=1; independent direct construction."""
    d, c, b, a = map(pvar, range(4))
    u = (a, b)
    v = (padd(P_ONE, a, -1), pscale(-1, b))
    w = (c, d)
    omega = (pconst(Q(1, 2)), pconst(Q(1, 2)))
    omega2 = (pconst(Q(-1, 2)), pconst(Q(1, 2)))
    epsilon, sigma, tau, kappa, lam = signs
    forms = (
        cadd(u, w),
        cadd(v, cscale(epsilon, w)),
        cadd(cadd(u, cscale(sigma, cmul(omega, v))), cscale(tau, cmul(omega2, w))),
        cadd(cadd(u, cscale(kappa, cmul(omega2, v))), cscale(lam, cmul(omega, w))),
    )
    norms = tuple(map(cnorm, (u, v, w)))
    return [padd(cnorm(form), P_ONE, -1) for form in forms], norms


def polynomial_json(polynomial):
    return [
        [list(monomial), str(coefficient)]
        for monomial, coefficient in sorted(polynomial.items(), reverse=True)
    ]


def radial_audit():
    cases = []
    basis_size = Counter()
    basis_terms = 0
    pair_checks = 0
    for signs in product((-1, 1), repeat=5):
        generators, norms = equations(signs)
        basis, processed = buchberger(generators)
        pair_checks += processed
        polynomials = [row[0] for row in basis]
        basis_size[len(polynomials)] += 1
        basis_terms += sum(map(len, polynomials))
        delta = P_ONE
        for i, j in ((0, 1), (0, 2), (1, 2)):
            delta = pmul(delta, padd(norms[i], norms[j], -1))
        delta_remainder, _ = normal_form(delta, basis)
        if not delta_remainder:
            classification = "equal_radius"
        else:
            classification = "exceptional_radii"
            for radius in norms:
                target = delta
                for root in (1, 3, 7):
                    target = pmul(
                        target, padd(pscale(4, radius), pconst(root), -1)
                    )
                remainder, _ = normal_form(target, basis)
                need(not remainder, "exceptional-radius consequence")
        cases.append(
            {
                "signs": signs,
                "classification": classification,
                "basis": [polynomial_json(p) for p in polynomials],
            }
        )
    classifications = Counter(case["classification"] for case in cases)
    need(classifications == {"equal_radius": 20, "exceptional_radii": 12}, "case classification")
    return {
        "sign_cases": len(cases),
        "equal_radius_cases": classifications["equal_radius"],
        "exceptional_radius_cases": classifications["exceptional_radii"],
        "buchberger_pairs_processed": pair_checks,
        "basis_size_histogram": dict(sorted(basis_size.items())),
        "basis_terms": basis_terms,
        "lex_bases_sha256": digest(cases),
        "classification_sha256": digest(
            [[case["signs"], case["classification"]] for case in cases]
        ),
    }


def uadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def umul(left, right):
    # Numerators are over 2; a product is again a unit numerator over 2.
    r, s = left
    t, u = right
    x = r * t - 3 * s * u
    y = r * u + s * t
    need(x % 2 == 0 and y % 2 == 0, "unit multiplication parity")
    return x // 2, y // 2


def uneg(value):
    return -value[0], -value[1]


def unorm(value):
    r, s = value
    need((r * r + 3 * s * s) % 4 == 0, "unit norm parity")
    return (r * r + 3 * s * s) // 4


def canonical_row(row):
    return min(tuple(umul(unit, coefficient) for coefficient in row) for unit in UNITS)


def gf4_mul(left, right):
    # Bits are coefficients of 1,t modulo t^2+t+1 over F2.
    a, b = left & 1, left >> 1
    c, d = right & 1, right >> 1
    return (a * c ^ b * d) | ((a * d ^ b * c ^ b * d) << 1)


def gf4_inverse(value):
    need(value in (1, 2, 3), "GF4 inverse domain")
    return next(x for x in (1, 2, 3) if gf4_mul(value, x) == 1)


def residue(value):
    r, s = value
    need((r - s) % 2 == 0, "Eisenstein coordinate parity")
    return (((r - s) // 2) & 1) | ((s & 1) << 1)


def projective(vector):
    pivot = next(value for value in vector if value)
    inverse = gf4_inverse(pivot)
    return tuple(gf4_mul(inverse, value) for value in vector)


def dot(normal, point):
    value = 0
    for a, b in zip(normal, point):
        value ^= gf4_mul(a, b)
    return value


def system_orbit_key(system):
    images = []
    for alpha, beta in product(UNITS, repeat=2):
        image = tuple(
            sorted(
                canonical_row((row[0], umul(alpha, row[1]), umul(beta, row[2])))
                for row in system
            )
        )
        images.append(image)
    return min(images)


def sign_template(signs):
    epsilon, sigma, tau, kappa, lam = signs
    one, omega, omega2 = U_ONE, (1, 1), (-1, 1)
    signed = lambda sign, value: value if sign == 1 else uneg(value)
    rows = (
        (one, one, U_ZERO),
        (one, U_ZERO, one),
        (U_ZERO, one, signed(epsilon, one)),
        (one, signed(sigma, omega), signed(tau, omega2)),
        (one, signed(kappa, omega2), signed(lam, omega)),
    )
    return tuple(sorted(canonical_row(row) for row in rows))


def finite_normalization_audit():
    rows = sorted(
        {
            canonical_row(row)
            for row in product((U_ZERO,) + UNITS, repeat=3)
            if sum(coefficient != U_ZERO for coefficient in row) >= 2
        }
    )
    need(len(rows) == 54, "54 projective unit-coefficient rows")
    buckets = defaultdict(list)
    for row in rows:
        buckets[projective(tuple(residue(coefficient) for coefficient in row))].append(row)
    normals = sorted(buckets)
    need(len(normals) == 18, "18 realized projective normals")
    points = list(product(range(4), repeat=3))
    masks = {
        normal: sum(1 << i for i, point in enumerate(points) if dot(normal, point) == 0)
        for normal in normals
    }
    full_mask = (1 << len(points)) - 1
    pencils = [
        pencil
        for pencil in combinations(normals, 5)
        if (masks[pencil[0]] | masks[pencil[1]] | masks[pencil[2]] | masks[pencil[3]] | masks[pencil[4]]) == full_mask
    ]
    need(len(pencils) == 9, "nine full nonmonomial pencils")
    lift_systems = []
    for pencil in pencils:
        need(sorted(len(buckets[n]) for n in pencil) == [2, 2, 2, 4, 4], "lift bucket sizes")
        for lift in product(*(buckets[n] for n in pencil)):
            lift_systems.append(tuple(sorted(lift)))
    need(len(lift_systems) == 1152 and len(set(lift_systems)) == 1152, "all lifted systems")
    orbits = Counter(system_orbit_key(system) for system in lift_systems)
    need(len(orbits) == 32 and set(orbits.values()) == {36}, "32 diagonal-unit orbits")
    template_keys = {tuple(signs): system_orbit_key(sign_template(signs)) for signs in product((-1, 1), repeat=5)}
    need(len(set(template_keys.values())) == 32, "sign templates are distinct orbits")
    need(set(template_keys.values()) == set(orbits), "sign templates exhaust lift orbits")
    return {
        "unit_rows": len(rows),
        "projective_normals": len(normals),
        "three_variable_pencils": len(pencils),
        "three_variable_lifts": len(lift_systems),
        "diagonal_unit_images_checked": len(lift_systems) * 36,
        "normalized_sign_orbits": len(orbits),
        "lifts_per_sign_orbit": 36,
        "normalization_sha256": digest(
            {
                "pencils": pencils,
                "orbits": sorted((key, value) for key, value in orbits.items()),
                "templates": sorted(template_keys.items()),
            }
        ),
        "pencils": pencils,
    }


def unit_form_audit():
    survivors = []
    checked = 0
    omega, omega2 = (1, 1), (-1, 1)
    for signs in product((-1, 1), repeat=5):
        epsilon, sigma, tau, kappa, lam = signs
        signed = lambda sign, value: value if sign == 1 else uneg(value)
        for u, v, w in product(UNITS, repeat=3):
            if uadd(u, v) != U_ONE:
                continue
            checked += 1
            forms = (
                uadd(u, w),
                uadd(v, signed(epsilon, w)),
                uadd(
                    uadd(u, signed(sigma, umul(omega, v))),
                    signed(tau, umul(omega2, w)),
                ),
                uadd(
                    uadd(u, signed(kappa, umul(omega2, v))),
                    signed(lam, umul(omega, w)),
                ),
            )
            if all(unorm(value) == 1 for value in forms):
                survivors.append((signs, u, v, w))
    need(checked == 384 and not survivors, "all-unit boundary")
    return {"all_unit_cases": checked, "all_unit_survivors": 0}


def a5_interface_audit(pencils, residual_path):
    residual = json.loads(Path(residual_path).read_text())
    residual_digest = digest(residual)
    need(
        residual_digest == "42132ed90f7696d9cf7c17e7b47588ca717bb71b633141e29412a1b55b55e97d",
        "h4195 residual hash",
    )
    all_a5 = []
    for support in combinations(range(4), 3):
        for pencil in pencils:
            embedded = []
            for normal in pencil:
                vector = [0] * 4
                for position, value in zip(support, normal):
                    vector[position] = value
                embedded.append([vector, 0])
            all_a5.append(sorted(embedded))
    all_a5.sort()
    need(len(all_a5) == 36 and len({digest(row) for row in all_a5}) == 36, "36 A5 pencils")
    selected = []
    for index, pencil in enumerate(residual["remaining_pencil_signatures"]):
        support = {j for normal, constant in pencil for j, value in enumerate(normal) if value}
        if all(constant == 0 for normal, constant in pencil) and len(support) == 3:
            selected.append([index, pencil])
    need(len(selected) == 24, "24 h4195 residual pencils")
    need(all(pencil in all_a5 for _, pencil in selected), "residual pencils in general family")
    return {
        "all_a5_pencils": len(all_a5),
        "all_a5_lifts": len(all_a5) * 128,
        "residual_pencils": len(selected),
        "residual_lifts": len(selected) * 128,
        "residual_indices": [index for index, _ in selected],
        "residual_sha256": residual_digest,
        "interface_sha256": digest({"all": all_a5, "selected": selected}),
    }


def run(residual_path):
    radial = radial_audit()
    normalization = finite_normalization_audit()
    all_unit = unit_form_audit()
    a5 = a5_interface_audit(normalization.pop("pencils"), residual_path)
    return {
        "status": "PASS",
        "polynomial": radial,
        "normalization": normalization,
        "unit_boundary": all_unit,
        "a5_interface": a5,
        "physical_three_power_concurrences": 0,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--residual", type=Path, required=True)
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.residual)
    if args.check_expected:
        expected = json.loads(Path(__file__).resolve().with_name("EXPECTED.json").read_text())
        need(json.loads(json.dumps(result)) == expected, "EXPECTED.json mismatch")
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
