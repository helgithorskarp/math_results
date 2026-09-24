"""Checks for the critical cube--crosspolytope boundary crossover.

The finite sections use exact rational arithmetic from the adjacent affine
section package.  Saddle and Bessel-series evaluations use 80-digit Decimal
arithmetic and are corroboration for the proof in PROOF.md.
"""

from decimal import Decimal as D, getcontext
from importlib.util import module_from_spec, spec_from_file_location
from json import dumps
from math import comb, factorial
from pathlib import Path


getcontext().prec = 80
ONE = D(1)
TWO = D(2)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def decimal_power(base, exponent):
    return ONE if exponent == 0 else base ** exponent


def interval_integral(a, power):
    """Integral of x^power exp(a*x) over [-1,1]."""
    answer = D(0)
    for index in range(300):
        if (power + index) % 2:
            continue
        term = (TWO * decimal_power(a, index)
                / D(factorial(index) * (power + index + 1)))
        answer += term
        if index > 50 and abs(term) < D("1e-90"):
            return answer
    raise ArithmeticError("interval series did not terminate")


def cube_data(theta):
    """Tilt, cumulants, and central density correction for a cube slice."""
    if theta == 0:
        a = D(0)
    else:
        a = TWO * theta / (ONE - theta ** 2)
        for _ in range(80):
            partition = interval_integral(a, 0)
            mean = interval_integral(a, 1) / partition
            variance = interval_integral(a, 2) / partition - mean ** 2
            if abs(mean - theta) < D("1e-72"):
                break
            a -= (mean - theta) / variance
        else:
            raise ArithmeticError("cube saddle did not converge")
    partition = interval_integral(a, 0)
    raw = [interval_integral(a, power) / partition for power in range(5)]
    mean = raw[1]
    variance = raw[2] - mean ** 2
    third = raw[3] - D(3) * mean * raw[2] + D(2) * mean ** 3
    central_fourth = (raw[4] - D(4) * mean * raw[3]
                      + D(6) * mean ** 2 * raw[2] - D(3) * mean ** 4)
    fourth = central_fourth - D(3) * variance ** 2
    edgeworth_mean = (fourth / (D(8) * variance ** 2)
                      - D(5) * third ** 2 / (D(24) * variance ** 3))
    require(abs(mean - theta) < D("1e-70"), "cube saddle residual")
    return {
        "a": a,
        "partition": partition,
        "variance": variance,
        "third": third,
        "fourth": fourth,
        "edgeworth_mean": edgeworth_mean,
        "beta": partition * (-a * theta - ONE).exp(),
    }


def bessel_series(z):
    """Phi, its first two derivatives, and integral_0^1 t Phi'(tz) dt."""
    phi = D(0)
    first = D(0)
    second = D(0)
    integral = D(0)
    for order in range(300):
        denominator = D(factorial(order) ** 2)
        term = decimal_power(z, order) / denominator
        phi += term
        if order:
            derivative_term = D(order) * decimal_power(z, order - 1) / denominator
            first += derivative_term
            integral += derivative_term / D(order + 1)
        if order >= 2:
            second += (D(order * (order - 1))
                       * decimal_power(z, order - 2) / denominator)
        if order > 50 and abs(term) < D("1e-90"):
            return phi, first, second, integral
    raise ArithmeticError("Bessel series did not terminate")


def crossover_data(theta, lam):
    cube = cube_data(theta)
    a = cube["a"]
    partition = cube["partition"]
    b_plus = a.exp() / partition
    b_minus = (-a).exp() / partition
    z = lam * (b_plus + b_minus)
    h = lam * (b_plus - b_minus)
    phi, first, second, integral = bessel_series(z)
    d_first = (theta * z - h) * first
    d_second = (((ONE + theta ** 2) * z - TWO * theta * h) * first
                + (theta * z - h) ** 2 * second)
    correction = (
        (z * first - z ** 2 * second) / TWO
        - cube["third"] * d_first / (TWO * cube["variance"] ** 2)
        - d_second / (TWO * cube["variance"])
        + a * lam * h * integral
    )
    absolute_correction = correction + phi * (
        cube["edgeworth_mean"] + ONE / D(12)
    )
    return {
        **cube,
        "b_plus": b_plus,
        "b_minus": b_minus,
        "z": z,
        "phi": phi,
        "psi": correction,
        "absolute_correction": absolute_correction,
    }


def direct_double_series(theta, lam, data):
    """Independent (p,q)-sum for Phi and Psi."""
    leading = D(0)
    correction = D(0)
    for total in range(120):
        last_weight = D(0)
        for plus in range(total + 1):
            minus = total - plus
            weight = (
                decimal_power(lam, total)
                * decimal_power(data["b_plus"], plus)
                * decimal_power(data["b_minus"], minus)
                / D(factorial(total) * factorial(plus) * factorial(minus))
            )
            displacement = theta * D(total) - D(plus) + D(minus)
            relative = (
                D(total) - D(total ** 2) / TWO
                - data["third"] * displacement
                / (TWO * data["variance"] ** 2)
                - displacement ** 2 / (TWO * data["variance"])
            )
            if total:
                relative += (data["a"] * D(plus - minus) * lam
                             / D(total + 1))
            leading += weight
            correction += weight * relative
            last_weight = weight
        if total > 60 and abs(last_weight) < D("1e-80"):
            return leading, correction
    raise ArithmeticError("double series did not terminate")


def load_exact_section():
    path = (Path(__file__).resolve().parent.parent
            / "affine_cube_crosspolytope_sections" / "exact_section.py")
    specification = spec_from_file_location("boundary_exact_section", path)
    require(specification is not None and specification.loader is not None,
            "exact-section import")
    module = module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def exact_ratio(module, size, theta, lam):
    total = module.F(str(theta)) * size
    radius = module.F(str(lam)) / size
    full = module.section(size, radius, total)
    boundary = module.section(size, 0, total)
    require(boundary > 0, "zero cube reference section")
    return D(full.numerator) / D(full.denominator) / (
        D(boundary.numerator) / D(boundary.denominator)
    )


def text(value, digits=18):
    return f"{value:.{digits}f}"


def main():
    exact = load_exact_section()
    parameters = (
        (D(0), D(1)),
        (D(0), D(2)),
        (D("0.5"), D(1)),
        (D("0.5"), D(2)),
    )
    samples = []
    for theta, lam in parameters:
        data = crossover_data(theta, lam)
        double_phi, double_psi = direct_double_series(theta, lam, data)
        require(abs(data["phi"] - double_phi) < D("1e-70"),
                "Bessel and double leading series")
        require(abs(data["psi"] - double_psi) < D("1e-68"),
                "operator and double correction series")
        rows = []
        for size in (6, 8, 10, 12, 14):
            ratio = exact_ratio(exact, size, theta, lam)
            scaled = D(size) * (ratio - data["phi"])
            rows.append({
                "N": size,
                "ratio": text(ratio),
                "N_times_leading_residual": text(scaled),
                "correction_residual": text(scaled - data["psi"]),
            })
        require(abs(D(rows[-1]["ratio"]) - data["phi"])
                < abs(D(rows[0]["ratio"]) - data["phi"]),
                "exact ratios did not approach the Bessel limit")
        require(abs(D(rows[-1]["correction_residual"])) < D("1.0"),
                "first-correction corroboration outside tolerance")
        samples.append({
            "theta": str(theta),
            "lambda": str(lam),
            "cube_tilt_a": text(data["a"]),
            "cube_variance": text(data["variance"]),
            "bessel_argument_z": text(data["z"]),
            "Phi": text(data["phi"]),
            "Psi": text(data["psi"]),
            "absolute_N_inverse_coefficient": text(
                data["absolute_correction"]
            ),
            "finite_exact_sections": rows,
        })

    for size in (4, 6, 8):
        for lam in (D(1), D(2)):
            positive = exact_ratio(exact, size, D("0.5"), lam)
            negative = exact_ratio(exact, size, D("-0.5"), lam)
            require(positive == negative, "exact reflection identity")
    for lam in (D(1), D(2)):
        positive = crossover_data(D("0.5"), lam)
        negative = crossover_data(D("-0.5"), lam)
        require(abs(positive["a"] + negative["a"]) < D("1e-70"),
                "reflected cube tilt")
        for key in ("phi", "psi", "absolute_correction"):
            require(abs(positive[key] - negative[key]) < D("1e-68"),
                    f"reflected crossover datum {key}")
    zero = crossover_data(D("0.5"), D(0))
    require(zero["phi"] == 1 and zero["psi"] == 0,
            "zero-thickness specialization")

    output = {
        "status": "BOUNDARY_BESSEL_CROSSOVER_VERIFIED",
        "series_agreement_bound": "1e-68",
        "exact_reflection_checks": 6,
        "asymptotic_reflection_checks": 2,
        "zero_thickness": {"Phi": "1", "Psi": "0"},
        "samples": samples,
        "scope": (
            "Exact rational finite sections plus independent 80-digit Bessel "
            "and tail-label series; PROOF.md establishes the uniform expansion."
        ),
    }
    print(dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
