#!/usr/bin/env python3
"""Exact controls for the degree budget; no Gaussian sign or integral evaluator."""

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path

from paired_cubature import budget as cubature_budget
from rational_frontier import rational, require


def budget(k):
    old = cubature_budget(k)
    degree = 2048*k**5-3
    atoms = old["atoms"]
    return {
        "k": k, "atoms": atoms, "beta_degree": degree,
        "largest_power": degree+2,
        "previous_largest_power": old["largest_power"],
        "coordinate_denominator": old["coordinate_denominator"],
        "weight_denominator": old["weight_denominator"],
        "compact_beta_error_bound": str(F(27, 64*k)),
        "global_compact_beta_error_bound": str(F(203, 64*k)),
        "global_rational_beta_error_bound": str(F(973, 256*k)),
        "nonpoint_pair_loss_floor": str(F(1, 2048*k**6*atoms**2)),
        "moment_error_denominator": f"({degree+1})*3^({degree})",
        "indices_outside_reviewed_sign_strip": degree-6,
    }


def plan(epsilon):
    epsilon = rational(epsilon)
    require(0 < epsilon <= 1, "tolerance must be in (0,1]")
    value = 8/epsilon
    k = (value.numerator+value.denominator-1)//value.denominator
    bound = epsilon/2 + F(973, 256*k)
    require(bound <= F(1997, 2048)*epsilon < epsilon, "consumer tolerance")
    return {"epsilon": str(epsilon), "required_uniform_beta_lower_bound":
            str(-epsilon/2), "unrestricted_defect_upper_bound": str(bound),
            "budget": budget(k)}


def beta_root(a, b):
    """Exact E sqrt(V), including the two deterministic kernel endpoints."""
    require(type(a) is int and type(b) is int and a >= 0 and b >= 0
            and a+b >= 2, "beta kernel parameters")
    if a == 0:
        return F(0)
    if b == 0:
        return F(1)
    value = F(1)
    for j in range(b):
        value *= F(2*(a+j), 2*(a+j)+1)
    return value


def beta_root_by_integration(a, b):
    """A second exact calculation: integrate the expanded beta density."""
    require(type(a) is int and type(b) is int and a >= 1 and b >= 1,
            "positive beta parameters for density integration")
    normalizer = F(factorial(a+b-1), factorial(a-1)*factorial(b-1))
    return normalizer*sum((-1)**j*comb(b-1, j)*F(2, 2*a+2*j+1)
                          for j in range(b))


def kernel(degree, u, omit_endpoints=False, wrong_shift=False):
    require(type(degree) is int and degree >= 0, "nonnegative beta degree")
    u = rational(u)
    require(0 <= u <= 1, "threshold in [0,1]")
    n = degree+2
    mass = mean = square = root = F(0)
    for j in range(n+1):
        if omit_endpoints and j in (0, n):
            continue
        weight = comb(n, j)*u**j*(1-u)**(n-j)
        mass += weight
        a, b = (j+1, n-j+1) if wrong_shift else (j, n-j)
        mean += weight*F(a, a+b)
        square += weight*F(a*(a+1), (a+b)*(a+b+1))
        root += weight*beta_root(a, b)
    return mass, mean, square, root


def verify_kernel(degree, u, values):
    n = degree+2
    mass, mean, square, root = values
    require(mass == 1, "kernel endpoint mass lost")
    require(mean == u, "kernel fails to preserve threshold")
    require(square-u*u == F(2, n+1)*u*(1-u), "kernel variance mismatch")
    require(0 <= root <= 1, "invalid square-root moment")


def risk_certificate(degree):
    """Certify the entire threshold interval for this finite degree.

    With u=t^2, the exact square-root risk is a rational polynomial in t.
    Nonnegative Bernstein coefficients certify its upper bound on [0,1].
    """
    n = degree+2
    d = 2*n+2
    power = [F(0)]*(d+1)
    power[0] = F(2, n+1)
    power[2] = -2
    for j in range(n+1):
        factor = 2*comb(n, j)*beta_root(j, n-j)
        for l in range(n-j+1):
            power[2*(j+l)+1] += factor*comb(n-j, l)*(-1)**l
    bernstein = [sum(power[i]*F(comb(j, i), comb(d, i)) for i in range(j+1))
                 for j in range(d+1)]
    require(min(bernstein) >= 0, "finite whole-interval risk certificate")
    # Check this polynomial against the probability definition, not just its
    # coefficient construction. These points do not replace the certificate.
    for t in (F(0), F(1, 7), F(1, 2), F(5, 6), F(1)):
        values = kernel(degree, t*t)
        risk = values[1]+t*t-2*t*values[3]
        direct = F(2, n+1)-risk
        from_power = sum(v*t**i for i, v in enumerate(power))
        from_bernstein = sum(v*comb(d, i)*t**i*(1-t)**(d-i)
                             for i, v in enumerate(bernstein))
        require(direct == from_power == from_bernstein, "risk representations differ")
    return {"degree": degree, "polynomial_degree": d,
            "minimum_bernstein_coefficient": str(min(bernstein)),
            "coefficient_sha256": sha256(
                json.dumps(list(map(str, bernstein)), separators=(",", ":")).encode()
            ).hexdigest()}


def check_inputs():
    root = Path(__file__).resolve().parents[2]
    inputs = json.loads(Path(__file__).with_name("WEIGHTED_INPUTS.json").read_text())
    for path, item in inputs.items():
        require(sha256((root/path).read_bytes()).hexdigest() == item["sha256"],
                "pinned input changed: "+path)
    return len(inputs)


def audit():
    pinned = check_inputs()
    require(F(2, 3) < F(5, 6)**2, "pi>3 coefficient bound")
    require(sum(F(1, factorial(j)) for j in range(5)) > F(8, 3), "e lower bound")
    require(F(10, 9)**2*6**3/F(8, 3)**3 == F(15, 4)**2,
            "calculus maximum constant")
    require(F(80, 9) < 9 and 3+F(15, 4) == F(27, 4), "radius-2k constant")
    require(2*F(27, 4)*F(1, 32) == F(27, 64), "kernel degree constant")
    require(F(11, 4)+F(27, 64) == F(203, 64), "compact budget")
    require(F(11, 4)+F(27, 64)+F(161, 256) == F(973, 256), "rational budget")
    require(F(1, 2)+F(973, 2048) == F(1997, 2048) < 1, "detection constant")

    moment_controls = 0
    root_controls = 0
    for degree in range(33):
        n = degree+2
        for a in range(1, n):
            require(beta_root(a, n-a) == beta_root_by_integration(a, n-a),
                    "beta square-root normalization")
            root_controls += 1
        for t in (F(0), F(1, 16), F(1, 4), F(1, 2), F(3, 4), F(15, 16), F(1)):
            u = t*t
            values = kernel(degree, u)
            verify_kernel(degree, u, values)
            risk = values[1]+u-2*t*values[3]
            require(0 <= risk <= F(2, n+1), "square-root kernel risk")
            moment_controls += 1
    certificates = [risk_certificate(n) for n in range(33)]

    rows = [budget(k) for k in (1, 2, 4, 10, 100, 1000, 10**6)]
    for row in rows:
        k = row["k"]
        require(F(2, row["beta_degree"]+3) == F(1, 1024*k**5),
                "exact square-root error schedule")
        require(row["previous_largest_power"] == 65536*k**8,
                "prior degree provenance")
        require(row["largest_power"]*32*k**3 < row["previous_largest_power"],
                "degree improvement factor")

    failures = [lambda: verify_kernel(3, F(1, 4), kernel(3, F(1, 4), True)),
                lambda: verify_kernel(3, F(1, 4), kernel(3, F(1, 4), False, True))]
    failures += [lambda x=x: budget(x) for x in (0, -1, True, F(2), 1.0)]
    failures += [lambda x=x: plan(x) for x in (0, -1, F(3, 2), True, 0.5)]
    for operation in failures:
        try:
            operation()
        except ValueError:
            pass
        else:
            raise ValueError("deliberate kernel error or malformed input accepted")

    return {
        "status": "SQUARE_ROOT_DEGREE_BUDGET_CONTROLS_PASS",
        "pinned_inputs": pinned,
        "direct_kernel_moment_and_risk_controls": moment_controls,
        "beta_root_product_vs_density_integral_controls": root_controls,
        "whole_interval_risk_certificates": certificates,
        "universal_all_degree_proof": "written proof, not finite extrapolation",
        "negative_controls_rejected": len(failures),
        "budgets": rows,
        "plans": [plan(F(1)), plan(F(1, 10)), plan(F(1, 100))],
        "gaussian_sign_evaluated": False,
        "exhaustive_configuration_cover": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    blob = (json.dumps(audit(), sort_keys=True, indent=2)+"\n").encode()
    if args.check:
        require(blob == Path(__file__).with_name("WEIGHTED_EXPECTED.json").read_bytes(),
                "weighted-degree expected record mismatch")
    print("SQUARE_ROOT_DEGREE_BUDGET_CONTROLS_PASS", sha256(blob).hexdigest())
    if not args.check:
        print(blob.decode(), end="")


if __name__ == "__main__":
    main()
