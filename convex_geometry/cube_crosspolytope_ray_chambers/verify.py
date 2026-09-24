"""Exact verifier for the global ray-chamber Legendre-kernel expansion."""

from fractions import Fraction as F
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def falling(value, length):
    answer = 1
    for offset in range(length):
        answer *= value - offset
    return answer


def rising(value, length):
    answer = 1
    for offset in range(length):
        answer *= value + offset
    return answer


def add_term(polynomial, key, value):
    polynomial[key] = polynomial.get(key, F(0)) + value
    if not polynomial[key]:
        del polynomial[key]


def kernel_terms(dimension):
    """H_d(A,s)=sum c[p,q] A^p s^q for s>=0."""
    require(type(dimension) is int and dimension >= 1, "kernel dimension")
    return {
        (dimension - 1 - degree, degree): F(
            falling(dimension - 1, degree) * rising(dimension, degree),
            factorial(dimension - 1) * factorial(degree) ** 2,
        )
        for degree in range(dimension)
    }


def transform_terms(polynomial):
    """Coefficient action induced by one signed tail-replacement operator."""
    transformed = {}
    for (a_power, slack_power), coefficient in polynomial.items():
        for moment in range(a_power + 1):
            weight = (
                coefficient
                * comb(a_power, moment)
                * (F(1, 2 ** (moment + 1)) - 1)
                * F(
                    factorial(moment) * factorial(slack_power),
                    factorial(moment + slack_power + 1),
                )
            )
            add_term(
                transformed,
                (a_power - moment, slack_power + moment + 1),
                weight,
            )
    return transformed


def correction_terms(size, order):
    """Terms of binom(N,r) T^r H_(N-r), without their shifts."""
    require(type(size) is int and 2 <= size and 0 <= order < size,
            "correction order")
    polynomial = kernel_terms(size - order)
    for _ in range(order):
        polynomial = transform_terms(polynomial)
    return {
        key: F(comb(size, order)) * coefficient
        for key, coefficient in polynomial.items()
    }


def chamber_section(size, base, slack):
    """Global A_N from the truncated-power chamber formula."""
    base, slack = F(base), F(slack)
    require(base > 0 and slack >= 0, "section parameters")
    answer = F(0)
    for order in range(size):
        if slack < 2 * order:
            break
        for (a_power, slack_power), coefficient in correction_terms(
            size, order
        ).items():
            answer += (
                coefficient
                * (base + 2 * order) ** a_power
                * (slack - 2 * order) ** slack_power
            )
    return answer


def legendre_value(degree, value):
    """Exact three-term recurrence for P_degree(value)."""
    value = F(value)
    previous = F(1)
    if degree == 0:
        return previous
    current = value
    for order in range(1, degree):
        previous, current = (
            current,
            F(2 * order + 1, order + 1) * value * current
            - F(order, order + 1) * previous,
        )
    return current


def legendre_kernel(dimension, base, slack):
    base, slack = F(base), F(slack)
    return (
        base ** (dimension - 1)
        / factorial(dimension - 1)
        * legendre_value(dimension - 1, F(1) + F(2) * slack / base)
    )


def load_exact_section():
    path = (Path(__file__).resolve().parent.parent
            / "affine_cube_crosspolytope_sections" / "exact_section.py")
    specification = spec_from_file_location("chamber_exact_section", path)
    require(specification is not None and specification.loader is not None,
            "exact-section import")
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def direct_section(module, size, margin, slack, sign=1):
    margin, slack = F(margin), F(slack)
    theta = F(sign) * (1 + margin)
    return module.section(
        size,
        margin * size + slack,
        theta * size,
    )


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    exact = load_exact_section()

    structural_checks = 0
    coefficient_counts = {}
    for size in range(2, 21):
        coefficient_counts[str(size)] = []
        for order in range(size):
            terms = correction_terms(size, order)
            coefficient_counts[str(size)].append(len(terms))
            require(all(a_power + slack_power == size - 1
                        for a_power, slack_power in terms),
                    "homogeneous chamber degree")
            require(all(slack_power >= order
                        for _, slack_power in terms),
                    "knot vanishing order")
            leading = terms.get((size - order - 1, order), F(0))
            predicted = F(
                comb(size, order) * (-1) ** order,
                2 ** order * factorial(order)
                * factorial(size - order - 1),
            )
            require(leading == predicted, "exact derivative jump")
            structural_checks += 1

    expected_n3 = (
        {(2, 0): F(1, 2), (1, 1): F(3), (0, 2): F(3)},
        {(1, 1): F(-3, 2), (0, 2): F(-21, 8)},
        {(0, 2): F(3, 8)},
    )
    require(tuple(correction_terms(3, order) for order in range(3))
            == expected_n3, "explicit N=3 spline")

    legendre_checks = 0
    for dimension in range(1, 13):
        terms = kernel_terms(dimension)
        for base in (F(1), F(3, 2), F(4)):
            for slack in (F(0), F(1, 3), F(1), F(2)):
                polynomial = sum(
                    coefficient * base ** a_power * slack ** slack_power
                    for (a_power, slack_power), coefficient in terms.items()
                )
                require(polynomial == legendre_kernel(
                    dimension, base, slack
                ), "Legendre kernel identity")
                legendre_checks += 1

    exact_checks = 0
    for size in range(2, 9):
        deltas = {
            F(0), F(1), F(2), F(5, 2), F(4), F(9, 2), F(6), F(15, 2),
            F(2 * (size - 1)), F(2 * (size - 1) + 1), F(2 * size + 3),
        }
        for margin in (F(1, 2), F(1), F(2)):
            base = margin * size
            for slack in sorted(deltas):
                predicted = chamber_section(size, base, slack)
                require(predicted == direct_section(
                    exact, size, margin, slack
                ), "global affine chamber identity")
                exact_checks += 1

        for slack in sorted(deltas):
            require(
                direct_section(exact, size, F(1), slack, 1)
                == direct_section(exact, size, F(1), slack, -1),
                "global reflection identity",
            )

    # On the first chamber the global formula specializes to the Legendre law.
    first_chamber_checks = 0
    for size in range(2, 13):
        for base in (F(1), F(3), F(7, 2)):
            for slack in (F(0), F(1, 2), F(2)):
                require(
                    chamber_section(size, base, slack)
                    == legendre_kernel(size, base, slack),
                    "first chamber specialization",
                )
                first_chamber_checks += 1

    sample_size = 5
    sample_base = F(5)
    sample_rows = []
    for slack in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12):
        section = chamber_section(sample_size, sample_base, F(slack))
        normalized = section * F(factorial(sample_size - 1),
                                 sample_size ** (sample_size - 1))
        sample_rows.append({
            "slack": slack,
            "active_correction_orders": min(slack // 2, sample_size - 1) + 1,
            "A_N": fraction_text(section),
            "D_N_minus_1": fraction_text(normalized),
        })

    output = {
        "status": "GLOBAL_RAY_CHAMBER_CLASSIFICATION_VERIFIED",
        "exact_affine_engine_checks": exact_checks,
        "legendre_kernel_checks": legendre_checks,
        "first_chamber_specializations": first_chamber_checks,
        "homogeneity_vanishing_jump_checks": structural_checks,
        "explicit_N3_spline": True,
        "global_reflection_sizes": 7,
        "coefficient_count_pattern_N10": coefficient_counts["10"],
        "sample_N5_margin1": sample_rows,
        "scope": (
            "Exact rational global chamber formula compared with the "
            "independent all-strata engine; PROOF.md establishes every "
            "dimension, radius, chamber, and knot smoothness statement."
        ),
    }
    print(dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
