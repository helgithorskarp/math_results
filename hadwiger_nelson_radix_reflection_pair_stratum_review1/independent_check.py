#!/usr/bin/env python3
"""Independent checker for the h4191 A5 reflection-pair stratum.

The checker imports no h4191 module.  It reconstructs the A5 norm-curve
inventory from the earlier reviewer h4181 source, derives reflection-normal
forms through the digit action, obtains every algebraic chart from an
independent real-coordinate formula using FLINT's multivariate resultant and
a reviewer-written quotient-Euclid implementation, and checks
the submitted colour words against all actual label pairs.  The optional
frontier input checks the conditional residual subtraction.  A representative
physical quartic is rebuilt in a separate exact Cartesian extension.
"""

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations, product
import json
import math
from pathlib import Path
import sys
import time

import sympy as S
from flint import fmpq, fmpq_poly as FQPoly, fmpz_mpoly_ctx, fmpz_poly as FZPoly


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_radix_reflection_pair_stratum"
INVENTORY_SOURCE = (
    ROOT
    / "hadwiger_nelson_radix_two_coordinate_pencils_review1"
    / "independent_check.py"
)
INVENTORY_SOURCE_SHA256 = (
    "5a3804b9e39e55686fd2ffa377f7bc60323b46c33c45f88f16076fe529a3de23"
)
CURVE_INVENTORY_SHA256 = (
    "85c286422c01bcb6ebb244186032bc607984471bc2b705ef7247084dd7c33db9"
)
FRONTIER_CANONICAL_SHA256 = (
    "5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3"
)
PRIME = 1_000_003

ZERO_E = (0, 0)
DIGITS = (ZERO_E, (1, 0), (0, 1))
LABELS = tuple(product(range(3), repeat=5))
WEIGHTS = tuple((1,) + tail for tail in product(range(3), repeat=4))


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_inventory_source():
    require(
        file_sha256(INVENTORY_SOURCE) == INVENTORY_SOURCE_SHA256,
        "pinned reviewer inventory source",
    )
    spec = importlib.util.spec_from_file_location("h4191_reviewer_inventory", INVENTORY_SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R = load_inventory_source()


def primitive_integer_coefficients(poly, variable):
    """Return low-to-high primitive integral coefficients with positive lead."""
    p = S.Poly(poly, variable, domain=S.QQ)
    require(not p.is_zero, "nonzero univariate polynomial")
    values = [F(p.nth(i)) for i in range(p.degree() + 1)]
    denominator = math.lcm(*(v.denominator for v in values))
    integers = [int(v * denominator) for v in values]
    divisor = math.gcd(*integers)
    if integers[-1] < 0:
        divisor = -divisor
    return tuple(v // divisor for v in integers)


def primitive_multivariate(poly, variables):
    p = S.Poly(poly, *variables, domain=S.QQ)
    require(not p.is_zero, "nonzero multivariate polynomial")
    values = [F(v) for v in p.coeffs()]
    denominator = math.lcm(*(v.denominator for v in values))
    integers = [int(v * denominator) for v in values]
    divisor = math.gcd(*integers)
    # SymPy's lexicographically leading coefficient fixes the sign.
    if integers[0] < 0:
        divisor = -divisor
    terms = [
        (monomial, int(F(coefficient) * denominator) // divisor)
        for monomial, coefficient in p.terms()
    ]
    return S.expand(sum(c * math.prod(v ** e for v, e in zip(variables, m)) for m, c in terms))


def compose(left, right):
    return tuple(left[right[i]] for i in range(len(left)))


def reconstruct_symmetry(pair_rows):
    factors, row_by_curve = R.curve_inventory()
    require(digest(factors) == CURVE_INVENTORY_SHA256, "independent curve inventory")
    curve_by_row = {row: curve for curve, row in row_by_curve.items()}
    require(len(factors) == 2797 and len(row_by_curve) == 2796, "complete curve inventory")
    circle = factors.index(((0, 0, -1), (0, 2, 3), (2, 0, 1)))
    require(circle == 342, "radial curve ID")

    identity = tuple(range(len(factors)))
    rotation = list(identity)
    conjugation = list(identity)
    for curve, row in row_by_curve.items():
        power = (1, 0)
        rotated = []
        for coefficient in row:
            rotated.append(R.e_mul(coefficient, power))
            power = R.e_mul(power, (-1, 1))
        rotation[curve] = curve_by_row[R.canonical_row(tuple(rotated))]
        conjugation[curve] = curve_by_row[
            R.canonical_row(tuple(R.e_conj(value) for value in row))
        ]
    rotation = tuple(rotation)
    conjugation = tuple(conjugation)
    group = (
        identity,
        rotation,
        compose(rotation, rotation),
        conjugation,
        compose(rotation, conjugation),
        compose(compose(rotation, rotation), conjugation),
    )
    require(len(set(group)) == 6, "six distinct D3 actions")
    require(
        all(compose(g, h) in group for g in group for h in group),
        "closed D3 action",
    )

    require(pair_rows == sorted(pair_rows), "sorted pair rows")
    require(len({tuple(row[:2]) for row in pair_rows}) == len(pair_rows), "unique pair rows")
    normalizations = []
    real_rows = {}
    expanded = set()
    for row in pair_rows:
        require(
            len(row) == 5 and all(type(v) is int for v in row),
            "integral five-field pair row",
        )
        a, b, mask, bound, allowance = row
        require(0 <= a < b < len(factors), "valid curve pair")
        orbit = [tuple(sorted((g[a], g[b]))) for g in group]
        actual_mask = sum(1 << i for i, image in enumerate(orbit) if image == (a, b))
        require((a, b) == min(orbit), "canonical D3 pair")
        require(actual_mask == mask and mask.bit_count() == 2 and mask & 56, "reflection stabilizer mask")
        degree_a = max(i + j for i, j, _ in factors[a])
        degree_b = max(i + j for i, j, _ in factors[b])
        require(bound == degree_a * degree_b // 2 and allowance == bound // 2, "pair allowance")
        choices = [
            (index, action[a], action[b])
            for index, action in enumerate(group[:3])
            if conjugation[action[a]] == action[a]
            and conjugation[action[b]] == action[b]
        ]
        require(len(choices) == 1, "unique rotation to two reflection-fixed curves")
        index, c, d = choices[0]
        c, d = sorted((c, d))
        normalizations.append([a, b, index, c, d])
        expanded.update(orbit)
        for curve in (c, d):
            if curve in real_rows:
                continue
            source = row_by_curve[curve]
            first = next(value for value in source if value != ZERO_E)
            multiplier = R.e_conj(first)
            transformed = tuple(R.e_mul(value, multiplier) for value in source)
            require(
                all(second == 0 and first in (-1, 0, 1) for first, second in transformed),
                "real coefficient normalization",
            )
            real_rows[curve] = tuple(first for first, _ in transformed)
    require(len(real_rows) == 112, "112 real normalized curves")
    return factors, row_by_curve, curve_by_row, normalizations, real_rows, sorted(expanded)


X, D, RAD, U = S.symbols("x D r u")


def real_norm_equation(coefficients):
    """Derive |sum a_j z^j|^2-1 via z=x+i*sqrt(3)y and D=3y^2."""
    real_power = S.Integer(1)
    imag_power = S.Integer(0)
    real_total = S.Integer(0)
    imag_total = S.Integer(0)
    for coefficient in coefficients:
        real_total += coefficient * real_power
        imag_total += coefficient * imag_power
        real_power, imag_power = (
            S.expand(X * real_power - D * imag_power),
            S.expand(real_power + X * imag_power),
        )
    norm = S.expand(real_total * real_total + D * imag_total * imag_total - 1)
    trace_half = (U - RAD) / 2
    transformed = S.expand(norm.subs({X: trace_half, D: RAD - trace_half * trace_half}))
    return primitive_multivariate(transformed, (RAD, U))


MPOLY_CONTEXT = fmpz_mpoly_ctx.get(("r", "u"), "lex")


def expression_to_mpoly(expression):
    polynomial = S.Poly(expression, RAD, U, domain=S.ZZ)
    return MPOLY_CONTEXT.from_dict(
        {monomial: int(coefficient) for monomial, coefficient in polynomial.terms()}
    )


def mpoly_radial_coefficients(polynomial):
    terms = polynomial.to_dict()
    degree = max((monomial[0] for monomial in terms), default=-1)
    values = []
    for radial_degree in range(degree + 1):
        coefficients = {
            monomial[1]: int(coefficient)
            for monomial, coefficient in terms.items()
            if monomial[0] == radial_degree
        }
        top = max(coefficients, default=-1)
        values.append(FQPoly([coefficients.get(index, 0) for index in range(top + 1)]))
    return flint_trim(values)


def primitive_flint_polynomial(polynomial):
    require(polynomial, "nonzero FLINT polynomial")
    values = [F(str(polynomial[index])) for index in range(polynomial.degree() + 1)]
    denominator = math.lcm(*(value.denominator for value in values))
    integers = [int(value * denominator) for value in values]
    divisor = math.gcd(*integers)
    if integers[-1] < 0:
        divisor = -divisor
    return tuple(value // divisor for value in integers)


def flint_trim(values):
    values = list(values)
    while values and not values[-1]:
        values.pop()
    return values


def flint_inverse(value, modulus):
    common, inverse, unused = value.xgcd(modulus)
    require(common == 1, "only quotient-ring units are inverted")
    inverse %= modulus
    require(value * inverse % modulus == 1, "checked quotient inverse")
    return inverse


def flint_quotient_gcd(first, second, modulus):
    def remainder(left, right):
        left = list(left)
        inverse = flint_inverse(right[-1], modulus)
        while len(left) >= len(right):
            coefficient = left[-1] * inverse % modulus
            offset = len(left) - len(right)
            for index, value in enumerate(right):
                left[offset + index] = (left[offset + index] - coefficient * value) % modulus
            left = flint_trim(left)
        return left

    first = flint_trim(FQPoly(value) % modulus for value in first)
    second = flint_trim(FQPoly(value) % modulus for value in second)
    while second:
        first, second = second, remainder(first, second)
    require(first, "nonzero fibre gcd")
    inverse = flint_inverse(first[-1], modulus)
    return [value * inverse % modulus for value in first]


def evaluate_radial(coefficients, radius, modulus):
    result = FQPoly([])
    for coefficient in reversed(coefficients):
        result = (result * radius + coefficient) % modulus
    return result


def rational_tuple(poly):
    if not poly:
        return ("0",)
    return tuple(str(poly[index]) for index in range(poly.degree() + 1))


def key_text(key):
    return json.dumps(key, separators=(",", ":"))


def reconstruct_components(pair_rows, normalizations, real_rows, progress=False):
    equations = {
        curve: expression_to_mpoly(real_norm_equation(row))
        for curve, row in real_rows.items()
    }
    radial_coefficients = {
        curve: mpoly_radial_coefficients(equation)
        for curve, equation in equations.items()
    }
    components = {}
    coverage_keys = []
    eliminants = []
    fibre_histogram = Counter()
    started = time.monotonic()

    for position, (a, b, rotation, c, d) in enumerate(normalizations, 1):
        first = equations[c]
        second = equations[d]
        resultant = first.resultant(second, "r")
        resultant_terms = resultant.to_dict()
        require(
            resultant_terms and all(monomial[0] == 0 for monomial in resultant_terms),
            "nonzero univariate resultant",
        )
        top = max(monomial[1] for monomial in resultant_terms)
        resultant_poly = FZPoly(
            [int(resultant_terms.get((0, index), 0)) for index in range(top + 1)]
        )
        resultant_coefficients = primitive_flint_polynomial(resultant_poly)
        eliminants.append(resultant_coefficients)
        resultant_poly = FZPoly(list(resultant_coefficients))
        content, factor_terms = resultant_poly.factor()
        product_poly = FZPoly([int(content)])
        for factor, exponent in factor_terms:
            product_poly *= factor ** exponent
        require(product_poly == resultant_poly, "exact resultant factor product")
        keys = []
        for factor, exponent in factor_terms:
            q = primitive_flint_polynomial(factor)
            modulus = FQPoly(list(q))
            gcd = flint_quotient_gcd(
                radial_coefficients[c], radial_coefficients[d], modulus
            )
            degree = len(gcd) - 1
            fibre_histogram[degree] += 1
            if degree == 0:
                continue
            if degree == 1:
                radius = -gcd[0] % modulus
                # Preserve the affine trace representative u-R even when q is
                # linear; this is the certificate's canonical chart encoding.
                trace = FQPoly([0, 1]) - radius
                require(
                    not evaluate_radial(radial_coefficients[c], radius, modulus)
                    and not evaluate_radial(radial_coefficients[d], radius, modulus),
                    "direct standard-chart substitution",
                )
                key = (q, rational_tuple(trace), rational_tuple(radius))
                text = key_text(key)
                components[text] = key
                keys.append(text)
            else:
                require(len(q) == 2, "nonlinear fibre only over rational projection")
                value = fmpq(-q[0], q[1])
                fibre = FQPoly([item[0] if item else 0 for item in gcd])
                content2, terms2 = fibre.factor()
                rebuilt = FQPoly([content2])
                for factor2, exponent2 in terms2:
                    rebuilt *= factor2 ** exponent2
                require(rebuilt == fibre, "exact exceptional-fibre factor product")
                for factor2, exponent2 in terms2:
                    q2 = primitive_flint_polynomial(factor2)
                    exceptional_modulus = FQPoly(list(q2))
                    specialized_first = [FQPoly([coefficient(value)]) for coefficient in radial_coefficients[c]]
                    specialized_second = [FQPoly([coefficient(value)]) for coefficient in radial_coefficients[d]]
                    radius_variable = FQPoly([0, 1])
                    require(
                        not evaluate_radial(specialized_first, radius_variable, exceptional_modulus)
                        and not evaluate_radial(specialized_second, radius_variable, exceptional_modulus),
                        "direct exceptional-chart substitution",
                    )
                    trace = (str(value), "-1")
                    radius = ("0", "1")
                    key = (q2, trace, radius)
                    text = key_text(key)
                    components[text] = key
                    keys.append(text)
        coverage_keys.append([[a, b], sorted(set(keys))])
        if progress and position % 400 == 0:
            print(
                f"geometry {position}/{len(normalizations)} pairs, {len(components)} components, {time.monotonic()-started:.1f}s",
                file=sys.stderr,
                flush=True,
            )

    ordered_keys = sorted(components)
    ids = {text: index for index, text in enumerate(ordered_keys)}
    ordered_components = [components[text] for text in ordered_keys]
    coverage = [[pair, [ids[text] for text in keys]] for pair, keys in coverage_keys]
    return {
        "components": ordered_components,
        "coverage": coverage,
        "eliminants": eliminants,
        "fibre_degree_histogram": {str(k): v for k, v in sorted(fibre_histogram.items())},
    }


def canonical_sign(terms):
    terms = tuple(terms)
    negative = tuple((i, j, -c) for i, j, c in terms)
    return min(terms, negative)


def projection_key(factor):
    even = canonical_sign((i, j // 2, c) for i, j, c in factor if j % 2 == 0)
    odd = canonical_sign((i, j // 2, c) for i, j, c in factor if j % 2 == 1)
    return even, odd


def label_edge_inventory(factors, curve_by_row):
    projections = [projection_key(factor) for factor in factors]
    colours = [
        [sum(weight[index] * label[index] for index in range(5)) % 3 for label in LABELS]
        for weight in WEIGHTS
    ]
    bad = [set() for _ in WEIGHTS]
    base_edges = 0
    owner_counts = Counter()
    for left, right in combinations(range(243), 2):
        difference = tuple(
            (
                DIGITS[LABELS[left][index]][0] - DIGITS[LABELS[right][index]][0],
                DIGITS[LABELS[left][index]][1] - DIGITS[LABELS[right][index]][1],
            )
            for index in range(5)
        )
        row = R.canonical_row(difference)
        support = [index for index, value in enumerate(row) if value != ZERO_E]
        if len(support) == 1:
            owner = "base" if support[0] == 0 else 342
        else:
            owner = curve_by_row[row]
        owner_counts[owner] += 1
        if owner == "base":
            base_edges += 1
        for index in range(len(WEIGHTS)):
            if colours[index][left] == colours[index][right]:
                require(owner != "base", "every candidate word colours universal edges")
                bad[index].add(projections[owner])
    require(sum(owner_counts.values()) == 29403 and base_edges == 243, "all label-pair owners")
    return bad, projections, owner_counts


def is_prime(number):
    if number < 2:
        return False
    if number % 2 == 0:
        return number == 2
    divisor = 3
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2
    return True


def mod_trim(values):
    values = list(values)
    while values and values[-1] == 0:
        values.pop()
    return values


def mod_remainder(first, second, prime):
    first = mod_trim(v % prime for v in first)
    second = mod_trim(v % prime for v in second)
    require(second, "nonzero modular divisor")
    inverse = pow(second[-1], -1, prime)
    while len(first) >= len(second):
        scale = first[-1] * inverse % prime
        offset = len(first) - len(second)
        for index, value in enumerate(second):
            first[offset + index] = (first[offset + index] - scale * value) % prime
        first = mod_trim(first)
    return first


def mod_gcd_one(first, second, prime):
    first = mod_trim(first)
    second = mod_trim(second)
    while second:
        first, second = second, mod_remainder(first, second, prime)
    return len(first) == 1 and first[0] % prime != 0


class ModQuotient:
    def __init__(self, q, prime):
        require(q[-1] % prime, "component degree survives modulo prime")
        self.prime = prime
        inverse = pow(q[-1] % prime, -1, prime)
        self.q = [value * inverse % prime for value in q]
        self.degree = len(q) - 1

    def red(self, values):
        values = [value % self.prime for value in values]
        for degree in range(len(values) - 1, self.degree - 1, -1):
            coefficient = values[degree]
            if coefficient:
                for index in range(self.degree):
                    values[degree - self.degree + index] = (
                        values[degree - self.degree + index]
                        - coefficient * self.q[index]
                    ) % self.prime
        return mod_trim(values[: self.degree])

    def add(self, first, second, scale=1):
        result = list(first) + [0] * max(0, len(second) - len(first))
        for index, value in enumerate(second):
            result[index] = (result[index] + scale * value) % self.prime
        return mod_trim(result)

    def scale(self, value, scalar):
        return mod_trim((scalar * item) % self.prime for item in value)

    def mul(self, first, second):
        if not first or not second:
            return []
        result = [0] * (len(first) + len(second) - 1)
        for i, left in enumerate(first):
            for j, right in enumerate(second):
                result[i + j] += left * right
        return self.red(result)

    def rational(self, values):
        result = []
        for text in values:
            value = F(text)
            require(value.denominator % self.prime, "component denominator survives modulo prime")
            result.append(
                value.numerator
                * pow(value.denominator % self.prime, -1, self.prime)
                % self.prime
            )
        return self.red(result)


def projection_basis(algebra, trace, radius):
    inverse_two = pow(2, -1, algebra.prime)
    inverse_three = pow(3, -1, algebra.prime)
    x = algebra.scale(trace, inverse_two)
    d = algebra.scale(algebra.add(radius, algebra.mul(x, x), -1), inverse_three)
    x_powers = [[1]]
    d_powers = [[1]]
    for _ in range(8):
        x_powers.append(algebra.mul(x_powers[-1], x))
    for _ in range(4):
        d_powers.append(algebra.mul(d_powers[-1], d))
    monomials = {
        (i, j): algebra.mul(x_powers[i], d_powers[j])
        for i in range(9)
        for j in range(5)
    }
    return d, monomials


def evaluate_projection(projection, algebra, d, monomials):

    def evaluate(terms):
        result = []
        for i, j, coefficient in terms:
            result = algebra.add(result, monomials[i, j], coefficient)
        return result

    even = evaluate(projection[0])
    odd = evaluate(projection[1])
    return algebra.add(algebra.mul(even, even), algebra.mul(d, algebra.mul(odd, odd)), -1)


def check_colour_words(components, words, bad_by_word, progress=False):
    require(is_prime(PRIME), "proof modulus is prime")
    require(len(words) == len(components), "one word per component")
    require(all(type(word) is int and 0 <= word < len(WEIGHTS) for word in words), "valid word indices")
    checks = 0
    started = time.monotonic()
    for index, (component, word) in enumerate(zip(components, words), 1):
        q, trace_text, radius_text = component
        algebra = ModQuotient(q, PRIME)
        trace = algebra.rational(trace_text)
        radius = algebra.rational(radius_text)
        d, monomials = projection_basis(algebra, trace, radius)
        for projection in bad_by_word[word]:
            obstruction = evaluate_projection(projection, algebra, d, monomials)
            require(
                mod_gcd_one(algebra.q, obstruction, PRIME),
                "colour-bad actual unit event excluded on entire component",
            )
            checks += 1
        if progress and index % 400 == 0:
            print(
                f"colour {index}/{len(components)} components, {checks} projection checks, {time.monotonic()-started:.1f}s",
                file=sys.stderr,
                flush=True,
            )
    return checks


# Fraction-polynomial arithmetic for the independent physical fixture.
def ftrim(values):
    values = tuple(F(v) for v in values)
    while values and not values[-1]:
        values = values[:-1]
    return values


def fadd(first, second, scale=1):
    result = list(first) + [F(0)] * max(0, len(second) - len(first))
    for index, value in enumerate(second):
        result[index] += scale * value
    return ftrim(result)


def fmul(first, second):
    if not first or not second:
        return ()
    result = [F(0)] * (len(first) + len(second) - 1)
    for i, left in enumerate(first):
        for j, right in enumerate(second):
            result[i + j] += left * right
    return ftrim(result)


def fdivmod(first, second):
    first = list(ftrim(first))
    second = ftrim(second)
    require(second, "nonzero exact divisor")
    quotient = [F(0)] * max(0, len(first) - len(second) + 1)
    while len(first) >= len(second):
        value = first[-1] / second[-1]
        offset = len(first) - len(second)
        quotient[offset] = value
        for index, coefficient in enumerate(second):
            first[offset + index] -= value * coefficient
        first = list(ftrim(first))
    return ftrim(quotient), ftrim(first)


def fderivative(poly):
    return ftrim(index * poly[index] for index in range(1, len(poly)))


def fevaluate(poly, value):
    result = F(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def sturm_chain(poly):
    chain = [ftrim(poly), fderivative(ftrim(poly))]
    while chain[-1]:
        quotient, remainder = fdivmod(chain[-2], chain[-1])
        if not remainder:
            break
        chain.append(tuple(-value for value in remainder))
    return chain


def sign_at(poly, where):
    value = fevaluate(poly, where)
    return (value > 0) - (value < 0)


def sturm_variations(chain, where=None, positive_infinity=True):
    signs = []
    for poly in chain:
        if where is None:
            sign = (poly[-1] > 0) - (poly[-1] < 0)
            if not positive_infinity and (len(poly) - 1) % 2:
                sign = -sign
        else:
            sign = sign_at(poly, where)
        if sign:
            signs.append(sign)
    return sum(first != second for first, second in zip(signs, signs[1:]))


def sturm_interval_count(poly, left, right):
    chain = sturm_chain(poly)
    require(all(fevaluate(item, left) or item != chain[0] for item in chain), "left endpoint convention")
    require(fevaluate(poly, left) and fevaluate(poly, right), "nonroot interval endpoints")
    return sturm_variations(chain, left) - sturm_variations(chain, right)


def sturm_total_count(poly):
    chain = sturm_chain(poly)
    return sturm_variations(chain, None, False) - sturm_variations(chain, None, True)


class FractionQuotient:
    def __init__(self, q):
        self.q = ftrim(q)

    def red(self, value):
        return fdivmod(ftrim(value), self.q)[1]

    def add(self, first, second, scale=1):
        return self.red(fadd(first, second, scale))

    def scale(self, value, scalar):
        return self.red(tuple(F(scalar) * item for item in value))

    def mul(self, first, second):
        return self.red(fmul(first, second))


class Embedding:
    def __init__(self, q, interval):
        self.q = q
        self.left, self.right = map(F, interval)
        require(fevaluate(q, self.left) * fevaluate(q, self.right) < 0, "root bracket sign change")
        require(sturm_interval_count(q, self.left, self.right) == 1, "one real root in bracket")

    def interval_evaluate(self, poly):
        low = high = F(0)
        for coefficient in reversed(poly):
            products = (low * self.left, low * self.right, high * self.left, high * self.right)
            low, high = min(products) + coefficient, max(products) + coefficient
        return low, high

    def sign(self, poly):
        poly = ftrim(poly)
        if not poly:
            return 0
        for _ in range(10000):
            low, high = self.interval_evaluate(poly)
            if low > 0:
                return 1
            if high < 0:
                return -1
            middle = (self.left + self.right) / 2
            left_value = fevaluate(self.q, self.left)
            middle_value = fevaluate(self.q, middle)
            if left_value * middle_value < 0:
                self.right = middle
            else:
                self.left = middle
        raise AssertionError("interval sign failed to separate")


def irreducible_quartic_mod_prime(q, prime):
    normalized = [value % prime for value in q]
    require(normalized[-1], "quartic degree survives")
    for value in range(prime):
        if sum(coefficient * pow(value, index, prime) for index, coefficient in enumerate(normalized)) % prime == 0:
            return False
    for a in range(prime):
        for b in range(prime):
            if not mod_remainder(normalized, [b, a, 1], prime):
                return False
    return True


def check_physical_fixture(path, component_ids, coverage):
    data = json.loads(Path(path).read_text())
    require(data["schema"] == "hn-radix-reflection-pair-physical-v1", "physical schema")
    q = tuple(F(value) for value in data["q"])
    require(len(q) == 5 and irreducible_quartic_mod_prime([int(v) for v in q], 7), "quartic irreducible modulo seven")
    require(sturm_total_count(q) == 2, "exactly two real quartic embeddings")
    trace_text = tuple(data["trace"])
    radius_text = tuple(data["radius"])
    component_key = key_text((tuple(int(v) for v in q), trace_text, radius_text))
    require(component_key in component_ids, "physical fixture is a derived algebraic component")
    component_id = component_ids[component_key]
    coverage_map = {tuple(pair): ids for pair, ids in coverage}
    require(component_id in coverage_map[(27, 1257)], "fixture belongs to declared source pair")

    algebra = FractionQuotient(q)
    one = (F(1),)
    zero = ()
    trace = algebra.red(tuple(F(value) for value in trace_text))
    radius = algebra.red(tuple(F(value) for value in radius_text))
    x = algebra.scale(trace, F(1, 2))
    y_squared = algebra.scale(algebra.add(radius, algebra.mul(x, x), -1), F(1, 3))

    def ext_add(first, second, scale=1):
        return algebra.add(first[0], second[0], scale), algebra.add(first[1], second[1], scale)

    def ext_scale(value, scalar):
        return algebra.scale(value[0], scalar), algebra.scale(value[1], scalar)

    def ext_mul(first, second):
        return (
            algebra.add(algebra.mul(first[0], second[0]), algebra.mul(y_squared, algebra.mul(first[1], second[1]))),
            algebra.add(algebra.mul(first[0], second[1]), algebra.mul(first[1], second[0])),
        )

    ext_zero = (zero, zero)
    ext_one = (one, zero)

    def complex_add(first, second, scale=1):
        return ext_add(first[0], second[0], scale), ext_add(first[1], second[1], scale)

    def complex_mul(first, second):
        return (
            ext_add(ext_mul(first[0], second[0]), ext_mul(first[1], second[1]), -3),
            ext_add(ext_mul(first[0], second[1]), ext_mul(first[1], second[0])),
        )

    complex_zero = (ext_zero, ext_zero)
    complex_one = (ext_one, ext_zero)
    z = ((x, zero), (zero, one))
    omega = (ext_scale(ext_one, F(1, 2)), ext_scale(ext_one, F(1, 2)))
    digit_values = (complex_zero, complex_one, omega)
    powers = [complex_one]
    for _ in range(4):
        powers.append(complex_mul(powers[-1], z))
    coordinates = []
    for label in LABELS:
        value = complex_zero
        for index, digit in enumerate(label):
            value = complex_add(value, complex_mul(powers[index], digit_values[digit]))
        coordinates.append(value)

    embeddings = [Embedding(q, item["isolating_interval"]) for item in data["embeddings"]]
    for embedding in embeddings:
        require(embedding.sign(radius) > 0 and embedding.sign(y_squared) > 0, "physical nonreal embedding")

    def ext_zero_at(value, embedding):
        a, b = value
        if not b:
            return not a
        norm = algebra.add(algebra.mul(a, a), algebra.mul(y_squared, algebra.mul(b, b)), -1)
        if norm:
            return False
        return embedding.sign(algebra.mul(a, b)) < 0

    factors, row_by_curve = R.curve_inventory()
    curve_by_row = {row: curve for curve, row in row_by_curve.items()}
    edge_sets = [[] for _ in embeddings]
    active_sets = [set() for _ in embeddings]
    for left, right in combinations(range(243), 2):
        delta_real = ext_add(coordinates[left][0], coordinates[right][0], -1)
        delta_imag = ext_add(coordinates[left][1], coordinates[right][1], -1)
        norm = ext_add(ext_mul(delta_real, delta_real), ext_mul(delta_imag, delta_imag), 3)
        unit_test = ext_add(norm, ext_one, -1)
        difference = tuple(
            (
                DIGITS[LABELS[left][index]][0] - DIGITS[LABELS[right][index]][0],
                DIGITS[LABELS[left][index]][1] - DIGITS[LABELS[right][index]][1],
            )
            for index in range(5)
        )
        row = R.canonical_row(difference)
        support = [index for index, value in enumerate(row) if value != ZERO_E]
        owner = "base" if len(support) == 1 and support[0] == 0 else (342 if len(support) == 1 else curve_by_row[row])
        for index, embedding in enumerate(embeddings):
            require(not ext_zero_at(norm, embedding), "243 distinct physical vertices")
            if ext_zero_at(unit_test, embedding):
                edge_sets[index].append((left, right))
                if owner != "base":
                    active_sets[index].add(owner)

    good_words = []
    for weight in WEIGHTS:
        colours = [sum(a * b for a, b in zip(weight, label)) % 3 for label in LABELS]
        if all(colours[left] != colours[right] for edges in edge_sets for left, right in edges):
            good_words.append(weight)
    require(good_words, "independently found physical three-colouring")
    results = []
    for index, edges in enumerate(edge_sets):
        require(all(edge in edges for edge in ((0, 81), (0, 162), (81, 162))), "permanent triangle")
        results.append(
            {
                "vertices": 243,
                "unit_edges": len(edges),
                "active_curves": sorted(active_sets[index]),
                "edge_sha256": digest(edges),
                "chromatic_number": 3,
            }
        )
    return {
        "quartic_real_embeddings": len(embeddings),
        "physical_pair_checks_per_embedding": 29403,
        "component_id": component_id,
        "source_pair": [27, 1257],
        "first_found_colour_word": list(good_words[0]),
        "examples": results,
    }


def check_frontier(path, pair_rows, expanded):
    data = json.loads(Path(path).read_text())
    require(digest(data) == FRONTIER_CANONICAL_SHA256, "pinned h4185 frontier")
    require(set(data) >= {"remaining_exact", "remaining_six"}, "frontier modes")
    selected = sorted(
        row
        for mode in ("remaining_exact", "remaining_six")
        for row in data[mode]
        if row[2] & 56
    )
    require(selected == pair_rows, "complete reflection-stabilized selection")
    removed_exact = [row for row in data["remaining_exact"] if row[2] & 56]
    removed_six = [row for row in data["remaining_six"] if row[2] & 56]
    kept_exact = [row for row in data["remaining_exact"] if not row[2] & 56]
    kept_six = [row for row in data["remaining_six"] if not row[2] & 56]
    rotation_only = [row for row in kept_exact + kept_six if row[2].bit_count() > 1]
    require(
        rotation_only
        == [
            [318, 340, 7, 32, 10],
            [318, 341, 7, 32, 10],
            [319, 340, 7, 32, 10],
            [319, 341, 7, 32, 10],
        ],
        "four rotation-only rows retained",
    )
    return {
        "input_global_pairs": len(data["remaining_exact"]) + len(data["remaining_six"]),
        "removed_exact_five_rows": len(removed_exact),
        "removed_at_least_six_rows": len(removed_six),
        "removed_total_rows": len(selected),
        "removed_allowance": sum(row[4] for row in selected),
        "expanded_pair_exclusions": len(expanded),
        "remaining_global_pairs": len(kept_exact) + len(kept_six),
        "remaining_global_allowance": sum(row[4] for row in kept_exact + kept_six),
        "remaining_exact_five_rows": len(kept_exact),
        "remaining_exact_five_allowance": sum(row[4] for row in kept_exact),
        "remaining_at_least_six_rows": len(kept_six),
        "remaining_at_least_six_allowance": sum(row[4] for row in kept_six),
        "rotation_only_rows_retained": rotation_only,
        "trust_boundary": "exact transformation of the pinned h4185 interface; inherited orbit allowances remain conditional",
    }


def run(certificate_path, physical_path, frontier_path=None, progress=False):
    raw = Path(certificate_path).read_bytes()
    certificate = json.loads(raw)
    require(certificate["schema"] == "hn-radix-reflection-pair-stratum-v1", "certificate schema")
    require(certificate["prime"] == PRIME, "declared proof prime")
    pair_rows = certificate["pair_rows"]

    started = time.monotonic()
    factors, row_by_curve, curve_by_row, normalizations, real_rows, expanded = reconstruct_symmetry(pair_rows)
    require(digest(normalizations) == certificate["normalizations_sha256"], "normalization inventory")
    require(digest(expanded) == certificate["expanded_pair_exclusions_sha256"], "expanded exclusion inventory")
    symmetry_seconds = time.monotonic() - started

    geometry_started = time.monotonic()
    geometry = reconstruct_components(pair_rows, normalizations, real_rows, progress)
    geometry_seconds = time.monotonic() - geometry_started
    components = geometry["components"]
    coverage = geometry["coverage"]
    require(digest(components) == certificate["component_inventory_sha256"], "component inventory")
    require(digest(coverage) == certificate["cover_sha256"], "pair-to-component cover")
    require(digest(geometry["eliminants"]) == "79692a62a6048f688761be7cdc388e181687450e3662f5cf6f63748801ad0c9c", "eliminant inventory")

    edge_started = time.monotonic()
    bad_by_word, projections, owner_counts = label_edge_inventory(factors, curve_by_row)
    colour_checks = check_colour_words(
        components, certificate["colour_word_indices"], bad_by_word, progress
    )
    colour_seconds = time.monotonic() - edge_started

    component_ids = {key_text(component): index for index, component in enumerate(components)}
    physical = check_physical_fixture(physical_path, component_ids, coverage)
    frontier = check_frontier(frontier_path, pair_rows, expanded) if frontier_path else None

    result = {
        "verified": True,
        "target_certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "independent_inventory_source_sha256": INVENTORY_SOURCE_SHA256,
        "pair_systems": len(pair_rows),
        "real_coefficient_norm_curves": len(real_rows),
        "algebraic_components": len(components),
        "pair_component_incidence_slots": sum(len(ids) for pair, ids in coverage),
        "fibre_degree_histogram": geometry["fibre_degree_histogram"],
        "eliminant_inventory_sha256": digest(geometry["eliminants"]),
        "D3_expanded_pair_exclusions": len(expanded),
        "used_colour_words": len(set(certificate["colour_word_indices"])),
        "actual_label_pairs_per_word_inventory": 29403,
        "universal_edges": owner_counts["base"],
        "colour_projection_unit_checks": colour_checks,
        "all_named_physical_members_chromatic_number": 3,
        "physical_fixture": physical,
        "conditional_frontier": frontier,
        "timings_seconds": {
            "symmetry": round(symmetry_seconds, 3),
            "geometry": round(geometry_seconds, 3),
            "colour": round(colour_seconds, 3),
            "total": round(time.monotonic() - started, 3),
        },
        "record_improvement": False,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=TARGET / "certificate.json")
    parser.add_argument("--physical", type=Path, default=TARGET / "physical.json")
    parser.add_argument("--frontier", type=Path)
    parser.add_argument("--expected", type=Path, default=HERE / "EXPECTED.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    result = run(args.certificate, args.physical, args.frontier, args.progress)
    if args.check_expected:
        expected = json.loads(args.expected.read_text())
        comparison = dict(result)
        comparison.pop("timings_seconds")
        require(comparison == expected, "independent expected result")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
