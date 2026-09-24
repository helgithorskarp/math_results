"""Reproducible checks for affine cube--crosspolytope section asymptotics.

The finite section identities are exact rational arithmetic.  The saddle,
cumulant-tensor, and finite-asymptotic checks use 80-digit Decimal arithmetic;
they corroborate, but do not replace, the proof in PROOF.md.
"""

from decimal import Decimal as D, getcontext
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


getcontext().prec = 80
ONE = D(1)
TWO = D(2)
PI = D("3.141592653589793238462643383279502884197169399375105820974944592307816406286")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decimal_power(base, exponent):
    return ONE if exponent == 0 else base ** exponent


def product(values):
    answer = ONE
    for value in values:
        answer *= value
    return answer


def inside_integral(a, power):
    """Integral of x^power exp(a*x) over [-1,1], by an entire series."""
    answer = D(0)
    for index in range(300):
        if (power + index) % 2:
            continue
        term = (TWO * decimal_power(a, index)
                / D(factorial(index) * (power + index + 1)))
        answer += term
        if index > 40 and abs(term) < D("1e-90"):
            return answer
    raise ArithmeticError("inside-integral series did not terminate")


def raw_integral(a, r, y_power, g_power):
    """Unnormalized integral of y^p g(y)^q exp(a*y-r*g(y))."""
    answer = inside_integral(a, y_power) if g_power == 0 else D(0)
    for sign in (1, -1):
        rate = r - D(sign) * a
        require(rate > 0, "saddle outside its natural domain")
        tail = sum(
            D(comb(y_power, index) * factorial(index + g_power)
              * sign ** y_power)
            / decimal_power(rate, index + g_power + 1)
            for index in range(y_power + 1)
        )
        answer += (D(sign) * a).exp() * tail
    return answer


def centered_moments(a, r, max_order):
    partition = raw_integral(a, r, 0, 0)
    theta = raw_integral(a, r, 1, 0) / partition
    rho = raw_integral(a, r, 0, 1) / partition
    moments = {}
    for y_power in range(max_order + 1):
        for g_power in range(max_order + 1 - y_power):
            moments[y_power, g_power] = sum(
                D(comb(y_power, i) * comb(g_power, j))
                * decimal_power(-theta, y_power - i)
                * decimal_power(-rho, g_power - j)
                * raw_integral(a, r, i, j) / partition
                for i in range(y_power + 1)
                for j in range(g_power + 1)
            )
    return partition, theta, rho, moments


def solve_saddle(theta, rho):
    """Damped Newton solution of grad log Z=(theta,rho)."""
    r = ((ONE + 4 / rho).sqrt() - ONE) / TWO
    a = theta * r / (ONE + abs(theta) + rho)
    for iteration in range(80):
        partition, found_theta, found_rho, moments = centered_moments(a, r, 2)
        first = found_theta - theta
        second = found_rho - rho
        if max(abs(first), abs(second)) < D("1e-70"):
            return a, r, partition, found_theta, found_rho, iteration
        variance_y = moments[2, 0]
        covariance = moments[1, 1]
        variance_g = moments[0, 2]
        determinant = variance_y * variance_g - covariance ** 2
        delta_a = (-variance_g * first + covariance * second) / determinant
        delta_r = (-covariance * first + variance_y * second) / determinant
        step = ONE
        old_residual = abs(first) + abs(second)
        while r + step * delta_r <= abs(a + step * delta_a) + D("1e-30"):
            step /= 2
        while step > D("1e-40"):
            _, next_theta, next_rho, _ = centered_moments(
                a + step * delta_a, r + step * delta_r, 2
            )
            if abs(next_theta - theta) + abs(next_rho - rho) < old_residual:
                break
            step /= 2
        require(step > D("1e-40"), "Newton line search failed")
        a += step * delta_a
        r += step * delta_r
    raise ArithmeticError("Newton iteration did not converge")


def recursive_cumulants(moments):
    """Centered joint cumulants through order six."""
    answer = {}
    for total in range(1, 7):
        for y_power in range(total + 1):
            g_power = total - y_power
            value = moments[y_power, g_power]
            if y_power:
                for i in range(1, y_power + 1):
                    for j in range(g_power + 1):
                        if (i, j) != (y_power, g_power):
                            value -= (
                                D(comb(y_power - 1, i - 1) * comb(g_power, j))
                                * answer[i, j] * moments[y_power - i, g_power - j]
                            )
            else:
                for j in range(1, g_power):
                    value -= (D(comb(g_power - 1, j - 1)) * answer[0, j]
                              * moments[0, g_power - j])
            answer[y_power, g_power] = value
    return answer


def pairings(indices):
    if not indices:
        return [()]
    first = indices[0]
    return [
        ((first, indices[index]),) + rest
        for index in range(1, len(indices))
        for rest in pairings(indices[1:index] + indices[index + 1:])
    ]


PAIRINGS_FOUR = pairings(tuple(range(4)))
PAIRINGS_SIX = pairings(tuple(range(6)))


def asymptotic_data(theta, rho):
    a, r, partition, found_theta, found_rho, iterations = solve_saddle(theta, rho)
    _, _, _, moments = centered_moments(a, r, 6)
    cumulants = recursive_cumulants(moments)
    variance_y = moments[2, 0]
    covariance = moments[1, 1]
    variance_g = moments[0, 2]
    determinant = variance_y * variance_g - covariance ** 2
    precision = (
        (variance_g / determinant, -covariance / determinant),
        (-covariance / determinant, variance_y / determinant),
    )

    def cumulant(indices):
        y_count = sum(index == 0 for index in indices)
        return cumulants[y_count, len(indices) - y_count]

    edgeworth_constant = D(0)
    for bits in range(16):
        indices = tuple((bits >> position) & 1 for position in range(4))
        edgeworth_constant += sum(
            cumulant(indices)
            * product(precision[indices[left]][indices[right]]
                      for left, right in pairing) / D(24)
            for pairing in PAIRINGS_FOUR
        )
    for left_bits in range(8):
        left_indices = tuple((left_bits >> position) & 1 for position in range(3))
        for right_bits in range(8):
            right_indices = tuple((right_bits >> position) & 1
                                  for position in range(3))
            indices = left_indices + right_indices
            edgeworth_constant -= sum(
                cumulant(left_indices) * cumulant(right_indices)
                * product(precision[indices[first]][indices[second]]
                          for first, second in pairing) / D(72)
                for pairing in PAIRINGS_SIX
            )
    linear_slack = sum(
        cumulant((i, j, k)) * precision[i][j] * precision[k][1] / TWO
        for i in range(2) for j in range(2) for k in range(2)
    )
    section_correction = (edgeworth_constant + linear_slack / r
                          - precision[1][1] / r ** 2)
    gamma = section_correction - D(5) / D(12)
    free_energy = partition * (-a * theta + r * rho).exp()
    beta = free_energy / ONE.exp()
    kappa = beta / (r * (TWO * PI * determinant).sqrt())
    return {
        "a": a,
        "r": r,
        "theta_residual": found_theta - theta,
        "rho_residual": found_rho - rho,
        "iterations": iterations,
        "beta": beta,
        "kappa": kappa,
        "gamma1": gamma,
    }


def load_module(name, path):
    specification = spec_from_file_location(name, path)
    require(specification is not None and specification.loader is not None,
            "module import specification")
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def text(value, digits=18):
    return f"{value:.{digits}f}"


def finite_diagnostics(module, theta, rho, data):
    rows = []
    for n in (3, 5, 7, 9, 11):
        exact_fraction = module.normalized_constant(n, str(rho), str(theta))
        exact = D(exact_fraction.numerator) / D(exact_fraction.denominator)
        leading = data["kappa"] * data["beta"] ** n / D(n).sqrt()
        rows.append({
            "n": n,
            "n_relative_residual": text(D(n) * (exact / leading - ONE)),
        })
    require(abs(D(rows[-1]["n_relative_residual"]) - data["gamma1"])
            < abs(D(rows[0]["n_relative_residual"]) - data["gamma1"]),
            "finite residual did not move toward gamma1")
    return rows


def main():
    directory = Path(__file__).resolve().parent
    affine = load_module("affine_exact_section", directory / "exact_section.py")
    central = load_module(
        "central_exact_section",
        directory.parent / "simplex_envelope_asymptotics" / "exact_section.py",
    )

    central_checks = 0
    for size in range(2, 9):
        for radius in (size, size + 1, 2 * size):
            require(affine.section(size, radius, 0) == central.section(size, radius),
                    "central exact-section specialization")
            central_checks += 1
    reflection_checks = 0
    for size in range(2, 8):
        for radius, total in ((size, 1), (2 * size, size / 2), (size + 2, -2)):
            require(affine.section(size, str(radius), str(total))
                    == affine.section(size, str(radius), str(-total)),
                    "exact affine reflection")
            reflection_checks += 1
    for size in range(2, 9):
        excess = D(size) / 2
        require(affine.stratum(size, 0, 0, str(excess), str(D(size) + excess))
                == affine.F(str(excess)) ** (size - 1) / factorial(size - 1),
                "positive pure-ray stratum")

    require(len(PAIRINGS_FOUR) == 3 and len(PAIRINGS_SIX) == 15,
            "pair-partition enumeration")
    parameters = ((D(0), D(1)), (D("0.5"), D(1)), (D("1.5"), D(1)))
    samples = []
    all_data = {}
    for theta, rho in parameters:
        data = asymptotic_data(theta, rho)
        require(max(abs(data["theta_residual"]), abs(data["rho_residual"]))
                < D("1e-68"), "saddle residual")
        all_data[theta, rho] = data
        samples.append({
            "theta": str(theta),
            "rho": str(rho),
            "a": text(data["a"]),
            "r": text(data["r"]),
            "beta": text(data["beta"]),
            "kappa": text(data["kappa"]),
            "gamma1": text(data["gamma1"]),
            "newton_iterations": data["iterations"],
            "finite_corroboration": finite_diagnostics(
                affine, theta, rho, data
            ),
        })

    central_data = all_data[D(0), D(1)]
    golden = (D(5).sqrt() - ONE) / TWO
    require(abs(central_data["r"] - golden) < D("1e-70"),
            "central saddle specialization")
    central_gamma = -D(237) / D(20) + D(284) * golden / D(15)
    require(abs(central_data["gamma1"] - central_gamma) < D("1e-68"),
            "central first-correction specialization")

    positive = all_data[D("0.5"), D(1)]
    negative = asymptotic_data(D("-0.5"), D(1))
    require(abs(positive["a"] + negative["a"]) < D("1e-68"),
            "reflected saddle a")
    for key in ("r", "beta", "kappa", "gamma1"):
        require(abs(positive[key] - negative[key]) < D("1e-68"),
                f"reflected asymptotic datum {key}")

    output = {
        "status": "AFFINE_SECTION_ASYMPTOTICS_VERIFIED",
        "exact_section_checks": {
            "central_specializations": central_checks,
            "reflection_identities": reflection_checks,
            "pure_ray_strata": 7,
        },
        "pair_partition_counts": {"order_four": 3, "order_six": 15},
        "reflection_saddle_error_bound": "1e-68",
        "samples": samples,
        "scope": (
            "Exact rational finite-section identities and 80-digit saddle/cumulant "
            "corroboration; PROOF.md establishes the locally uniform all-orders theorem."
        ),
    }
    print(dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
