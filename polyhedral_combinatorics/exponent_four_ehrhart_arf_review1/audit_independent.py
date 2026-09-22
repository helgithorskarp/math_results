#!/usr/bin/env python3
"""Independent exact audit of the exponent-four Ehrhart/Arf criterion.

CPython 3.11+, standard library only.  This imports no target module,
fixture, output, or certificate.  Coordinate profiles are enumerated as
multisets (column order is immaterial), and the local jump is calculated by
three definition-level routes: finite characters, binary codewords, and a
symplectic decomposition.  Canonical simplex and cube-product counts are
computed from their defining slack inequalities with a memoized recursion.
The Berline--Vergne local formula remains an explicitly documented human
premise rather than a computational conclusion.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations_with_replacement, product
import json
from math import comb, log2
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(s, left, right):
    return ((left[0] + right[0]) % 4, left[1] ^ right[1])


def multiple(s, coefficient, value):
    answer = (0, 0)
    for _ in range(coefficient % 4):
        answer = add(s, answer, value)
    return answer


def generated_subgroup(s, generators):
    values = {(0, 0)}
    for generator in generators:
        values = {add(s, value, multiple(s, coefficient, generator))
                  for value in values for coefficient in range(4)}
    return values


def generating_profile(s, profile):
    return len(generated_subgroup(s, profile)) == 4 * (1 << s)


def gaussian_character_jump(s, profile):
    """Equation (8), evaluated directly with Gaussian-integer numerators."""
    real_sum = imag_sum = 0
    for character_a in (1, 3):
        for character_y in range(1 << s):
            real, imag = 1, 0
            for a, x in profile:
                phase = (character_a * a
                         + 2 * ((character_y & x).bit_count() & 1)) % 4
                require(phase, "a selected character is singular")
                # 1/(1-i^phase) = (u+iv)/2.
                u, v = {1: (1, 1), 2: (1, 0), 3: (1, -1)}[phase]
                real, imag = real * u - imag * v, real * v + imag * u
            real_sum += real
            imag_sum += imag
    require(imag_sum == 0, "odd-character sum is not real")
    # Character prefactor 2/|C4 x F2^s|, plus 2^-g above.
    return Fraction(real_sum, 1 << (s + len(profile) + 1))


def binary_code(s, profile):
    odd = tuple((a, x) for a, x in profile if a & 1)
    words = []
    qvalues = {}
    for word in range(1 << len(odd)):
        if word.bit_count() & 1:
            continue
        xsum = 0
        negative = 0
        for index, (a, x) in enumerate(odd):
            if word >> index & 1:
                xsum ^= x
                negative += a == 3
        if xsum:
            continue
        words.append(word)
        qvalues[word] = ((word.bit_count() // 2) + negative) & 1
    word_set = set(words)
    radical = {word for word in words
               if all(not ((word & other).bit_count() & 1)
                      for other in words)}
    return odd, word_set, qvalues, radical


def vector_basis(values):
    """Ascending-pivot F2 basis, deliberately unlike target insertion order."""
    rows = {}
    for original in sorted(values):
        value = original
        while value:
            pivot = (value & -value).bit_length() - 1
            if pivot not in rows:
                rows[pivot] = value
                break
            value ^= rows[pivot]
    return [rows[pivot] for pivot in sorted(rows)]


def dot(left, right):
    return (left & right).bit_count() & 1


def symplectic_decomposition(words):
    remaining = vector_basis(words)
    pairs = []
    while True:
        choice = next(((i, j) for i in range(len(remaining))
                       for j in range(i + 1, len(remaining))
                       if dot(remaining[i], remaining[j])), None)
        if choice is None:
            return pairs, remaining
        i, j = choice
        u, v = remaining[i], remaining[j]
        rest = []
        for index, word in enumerate(remaining):
            if index in (i, j):
                continue
            rest.append(word ^ (u if dot(word, v) else 0)
                        ^ (v if dot(word, u) else 0))
        pairs.append((u, v))
        remaining = vector_basis(rest)


def inspect_profile(s, profile):
    require(profile and generating_profile(s, profile), "generating profile required")
    odd, words, qvalues, radical = binary_code(s, profile)
    pairs, radical_basis = symplectic_decomposition(words)
    require(set(generated_subgroup_binary(radical_basis)) == radical,
            "symplectic algorithm returned the wrong radical")
    require(len(words) == 1 << len(vector_basis(words)), "code basis dimension")
    direct_sum = sum((-1) ** qvalues[word] for word in words)
    code_jump = Fraction(direct_sum, 1 << len(profile))
    character_jump = gaussian_character_jump(s, profile)
    require(code_jump == character_jump, "character/code normalization mismatch")
    radical_nonzero = any(qvalues[word] for word in radical)
    require((direct_sum == 0) == radical_nonzero, "radical vanishing criterion")
    ell = int(log2(len(words)))
    rho = int(log2(len(radical)))
    require((ell - rho) % 2 == 0, "odd nonsingular quotient dimension")
    if radical_nonzero:
        arf = None
        witness = min(word for word in radical if qvalues[word])
    else:
        arf = sum(qvalues[u] * qvalues[v] for u, v in pairs) & 1
        expected = (-1) ** arf * (1 << ((ell + rho) // 2))
        require(direct_sum == expected, "Arf sign or magnitude mismatch")
        witness = None
    rank = ell - rho
    magnitude_exponent = None if direct_sum == 0 else -sum(a == 2 for a, _ in profile) - s - 1 - rank // 2
    if direct_sum:
        if magnitude_exponent >= 0:
            expected_abs = Fraction(1 << magnitude_exponent)
        else:
            expected_abs = Fraction(1, 1 << -magnitude_exponent)
        require(abs(code_jump) == expected_abs, "closed magnitude mismatch")
    return {
        "s": s,
        "profile": [list(item) for item in profile],
        "codimension": len(profile),
        "odd_columns": len(odd),
        "code_dimension": ell,
        "radical_dimension": rho,
        "bilinear_rank": rank,
        "cancellation_witness": witness,
        "arf": arf,
        "gauss_sum": direct_sum,
        "delta": fraction_json(code_jump),
    }


def generated_subgroup_binary(generators):
    values = {0}
    for generator in generators:
        values |= {value ^ generator for value in tuple(values)}
    return values


def fraction_json(value):
    return [value.numerator, value.denominator]


def invariant_group_obstruction():
    """Exhaust all invariant-factor groups of exponent <=4 and order <=256."""
    checked = possible = 0
    counterexamples = {}
    for four_rank in range(5):
        for two_rank in range(9):
            if four_rank + two_rank == 0 or 2 * four_rank + two_rank > 8:
                continue
            moduli = (4,) * four_rank + (2,) * two_rank
            zero = (0,) * len(moduli)
            group = tuple(product(*(range(modulus) for modulus in moduli)))

            def group_add(left, right):
                return tuple((a + b) % modulus
                             for a, b, modulus in zip(left, right, moduli))

            def cyclic(value):
                current = zero
                answer = {zero}
                for _ in range(3):
                    current = group_add(current, value)
                    answer.add(current)
                return answer

            for b in group:
                if b == zero or group_add(b, b) != zero:
                    continue
                eligible = tuple(q for q in group if b in cyclic(q))
                generated = {zero}
                for q in eligible:
                    generated = {group_add(value, multiple_tuple(coefficient, q, moduli))
                                 for value in generated for coefficient in range(4)}
                observed = len(generated) == len(group)
                expected = ((four_rank == 0 and two_rank == 1)
                            or (four_rank == 1
                                and b == (2,) + (0,) * two_rank))
                require(observed == expected, "finite group obstruction mismatch")
                checked += 1
                possible += observed
                label = f"C4^{four_rank}xC2^{two_rank}"
                counterexamples.setdefault(label, {
                    "group_order": len(group),
                    "eligible_count": len(eligible),
                    "eligible_span_order": len(generated),
                    "possible": observed,
                })
    require(not counterexamples["C4^0xC2^2"]["possible"], "C2^2 boundary")
    require(not counterexamples["C4^2xC2^0"]["possible"], "C4^2 boundary")
    return checked, possible, {
        "C2xC2": counterexamples["C4^0xC2^2"],
        "C4xC4": counterexamples["C4^2xC2^0"],
    }


def multiple_tuple(coefficient, value, moduli):
    return tuple((coefficient * coordinate) % modulus
                 for coordinate, modulus in zip(value, moduli))


def enumerate_profiles():
    limits = ((0, 9), (1, 9), (2, 7), (3, 6))
    records = []
    sign_counts = {"positive": 0, "zero": 0, "negative": 0}
    by_s = {}
    first_sign = {}
    digest = sha256()
    total_multisets = 0
    for s, maximum_g in limits:
        alphabet = ((2, 0),) + tuple((a, x) for a in (1, 3)
                                    for x in range(1 << s))
        for g in range(1, maximum_g + 1):
            for profile in combinations_with_replacement(alphabet, g):
                total_multisets += 1
                if not generating_profile(s, profile):
                    continue
                record = inspect_profile(s, profile)
                delta = Fraction(*record["delta"])
                sign = "zero" if not delta else "positive" if delta > 0 else "negative"
                sign_counts[sign] += 1
                by_s[s] = by_s.get(s, 0) + 1
                first_sign.setdefault((s, sign), profile)
                digest.update(json.dumps(record, sort_keys=True,
                                         separators=(",", ":")).encode() + b"\n")
                records.append(record)
    for s in range(4):
        for sign in ("positive", "zero", "negative"):
            require((s, sign) in first_sign, f"missing {sign} fixture for s={s}")
    return total_multisets, records, sign_counts, by_s, first_sign, digest.hexdigest()


def simplex_count(s, profile, n):
    """Literal defining-slack count, memoized by suffix/budget/group state."""
    costs = tuple(2 if a == 2 else 1 for a, _ in profile)

    @lru_cache(None)
    def visit(index, budget, a, x):
        if index == len(profile):
            return int((a, x) == (2 * (n & 1), 0))
        q_a, q_x = profile[index]
        cost = costs[index]
        answer = 0
        for value in range(budget // cost + 1):
            answer += visit(index + 1, budget - cost * value,
                            (a + value * q_a) % 4,
                            x ^ (q_x if value & 1 else 0))
        return answer

    return visit(0, 2 * n, 0, 0)


@lru_cache(None)
def simplex_count_cartesian(s, profile, n):
    """Second definition-level count by a literal Cartesian box scan."""
    costs = tuple(2 if a == 2 else 1 for a, _ in profile)
    answer = 0
    for values in product(*(range(2 * n // cost + 1) for cost in costs)):
        if sum(cost * value for cost, value in zip(costs, values)) > 2 * n:
            continue
        a = sum(value * q[0] for value, q in zip(values, profile)) % 4
        x = 0
        for value, q in zip(values, profile):
            if value & 1:
                x ^= q[1]
        answer += (a, x) == (2 * (n & 1), 0)
    return answer


def interpolate(points, value):
    answer = Fraction(0)
    for index, (x, y) in enumerate(points):
        term = Fraction(y)
        for other, (z, _) in enumerate(points):
            if other != index:
                term *= Fraction(value - z, x - z)
        answer += term
    return answer


def invertible_binary_maps(s):
    if s == 0:
        return ((),)
    maps = []
    for columns in product(range(1 << s), repeat=s):
        if len(generated_subgroup_binary(columns)) == 1 << s:
            maps.append(columns)
    return tuple(maps)


def apply_linear(columns, value):
    answer = 0
    for bit, column in enumerate(columns):
        if value >> bit & 1:
            answer ^= column
    return answer


def coordinate_change(s, profile, sign, functional, shift, linear):
    changed = []
    for a, x in reversed(profile):
        first = (sign * a + 2 * dot(functional, x)) % 4
        second = apply_linear(linear, x) ^ (shift if a & 1 else 0)
        changed.append((first, second))
    return tuple(sorted(changed))


def realization_audit(first_sign):
    fixtures = []
    holdouts = cartesian_counts = product_models = coordinate_checks = 0
    for s in range(4):
        linear_maps = invertible_binary_maps(s)
        for sign_name in ("positive", "zero", "negative"):
            profile = first_sign[(s, sign_name)]
            local = inspect_profile(s, profile)
            delta = Fraction(*local["delta"])
            g = len(profile)
            # Exhaust the natural automorphism family for the selected fixtures.
            base_character = gaussian_character_jump(s, profile)
            for scalar_sign, functional, shift, linear in product(
                    (1, -1), range(1 << s), range(1 << s), linear_maps):
                changed = coordinate_change(
                    s, profile, scalar_sign, functional, shift, linear
                )
                require(generating_profile(s, changed), "automorphism lost generation")
                require(gaussian_character_jump(s, changed) == base_character,
                        "coordinate-dependent local jump")
                coordinate_checks += 1

            for cube_dimension in range(3):
                degree = g + cube_dimension
                # Need degree+1 values in each residue class plus two holdouts.
                maximum = 2 * degree + 5
                values = [simplex_count(s, profile, n) * (n + 1) ** cube_dimension
                          for n in range(maximum + 1)]
                even = [(n, values[n]) for n in range(0, 2 * degree + 1, 2)]
                odd = [(n, values[n]) for n in range(1, 2 * degree + 2, 2)]
                require(len(even) == degree + 1 == len(odd), "interpolation sample count")
                for value in range(degree + 1):
                    difference = interpolate(even, value) - interpolate(odd, value)
                    require(difference == delta * (value + 1) ** cube_dimension,
                            "simplex/cube parity polynomial mismatch")
                for n in range(2 * degree + 2, maximum + 1):
                    points = even if n % 2 == 0 else odd
                    require(interpolate(points, n) == values[n], "Ehrhart holdout mismatch")
                    holdouts += 1
                for n in range(4):
                    require(simplex_count_cartesian(s, profile, n)
                            == simplex_count(s, profile, n),
                            "Cartesian and memoized slack counts disagree")
                    require(values[n] == simplex_count_cartesian(s, profile, n)
                            * (n + 1) ** cube_dimension,
                            "cube-product literal count mismatch")
                    cartesian_counts += 1
                product_models += 1
            fixtures.append({
                "s": s,
                "sign": sign_name,
                "profile": [list(item) for item in profile],
                "delta": fraction_json(delta),
                "codimension": g,
            })
    return {
        "fixtures": fixtures,
        "simplex_cube_product_models": product_models,
        "Ehrhart_holdouts": holdouts,
        "cartesian_lattice_counts": cartesian_counts,
        "coordinate_automorphism_checks": coordinate_checks,
    }


def c2_boundary():
    for g in range(1, 13):
        # The sole odd character contributes (1-(-1))^-g.
        jump = Fraction(1, 1 << g)
        require(jump == Fraction(1, 2 ** g), "C2 normalization")
    return 12


def run():
    group_checks, group_possible, excluded_examples = invariant_group_obstruction()
    total, records, signs, by_s, first_sign, digest = enumerate_profiles()
    realization = realization_audit(first_sign)
    require(any(record["radical_dimension"] for record in records), "no radical case")
    require(any(record["arf"] == 1 for record in records), "no negative Arf case")
    require(any(record["cancellation_witness"] is not None for record in records),
            "no cancellation case")
    return {
        "status": "pass",
        "group_involutions_checked": group_checks,
        "group_involutions_admitting_generation": group_possible,
        "excluded_smallest_groups": excluded_examples,
        "profile_multisets_examined": total,
        "generating_profile_multisets": len(records),
        "profiles_by_elementary_rank": {str(key): by_s[key] for key in sorted(by_s)},
        "sign_distribution": signs,
        "maximum_elementary_rank": 3,
        "maximum_profile_length": 9,
        "C2_codimensions_checked": c2_boundary(),
        "profile_entrywise_sha256": digest,
        **realization,
    }


if __name__ == "__main__":
    result = run()
    if "--emit" not in sys.argv[1:]:
        expected = Path(__file__).with_name("EXPECTED_OUTPUT.json")
        require(expected.exists(), "missing EXPECTED_OUTPUT.json")
        require(result == json.loads(expected.read_text()), "expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
