#!/usr/bin/env python3
"""Exact arithmetic controls for UNIFORM_FRONTIER.md; no Gaussian sign test.

Python >=3.11, standard library. No assertions or floating-point premises.
The budget planner's conclusions require the uniform beta bound to be proved
elsewhere. Running this audit does not verify that analytic input.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def positive_int(value: int) -> int:
    require(type(value) is int and value > 0, "positive integer required")
    return value


def budget(k: int) -> dict:
    """Exact dimensions and error constants; does not compute B_k."""
    positive_int(k)
    return {
        "k": k,
        "atoms": k**6,
        "radius": 2*k,
        "variance": 1,
        "beta_degree": 65536*k**8-2,
        "largest_power": 65536*k**8,
        "moment_error": str(F(2, 3*k)),
        "total_error_strictly_less_than": str(F(14, 3*k)),
        "uniform_beta_sign_verified": False,
    }


def plan(epsilon: F) -> dict:
    """Sufficient budget IF every beta on the entire K_k has the given bound."""
    require(type(epsilon) is F and 0 < epsilon <= 1,
            "epsilon must be a Fraction in (0,1]")
    ratio = 10/epsilon
    k = (ratio.numerator+ratio.denominator-1)//ratio.denominator
    result = budget(k)
    result.update(
        epsilon=str(epsilon),
        required_uniform_beta_lower=str(-epsilon/2),
        conditional_defect_upper=str(epsilon/2+F(14, 3*k)),
    )
    require(epsilon/2+F(14, 3*k) < epsilon, "budget must leave a reserve")
    return result


# Bivariate rational polynomials in (N,u), for a coefficientwise identity
# rather than interpolation or a finite test of the universal formula.
def add(*polys: dict) -> dict:
    result = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            result[exponent] = result.get(exponent, F(0))+coefficient
    return {e: c for e, c in result.items() if c}


def scale(poly: dict, coefficient: F | int) -> dict:
    return {e: c*coefficient for e, c in poly.items() if c*coefficient}


def mul(a: dict, b: dict) -> dict:
    result = {}
    for (i,j), c in a.items():
        for (k,l), d in b.items():
            e = i+k, j+l
            result[e] = result.get(e, F(0))+c*d
    return {e: c for e, c in result.items() if c}


def audit() -> dict:
    one = {(0,0): F(1)}
    n = {(1,0): F(1)}
    u = {(0,1): F(1)}
    one_minus_u = add(one, scale(u, -1))
    ej = mul(n, u)
    ej2 = add(mul(ej, one_minus_u), mul(ej, ej))
    n2, n3 = add(n, scale(one, 2)), add(n, scale(one, 3))
    lhs = add(ej2, scale(ej, 3), scale(one, 2),
              scale(mul(mul(u, add(ej, one)), n3), -2),
              mul(mul(u,u), mul(n2,n3)))
    rhs = scale(add(one, mul(add(n,scale(one,-3)),mul(u,one_minus_u))), 2)
    require(lhs == rhs, "Durrmeyer second-moment polynomial mismatch")

    # Universal schedule identity after writing k=1+z, z>=0.
    # 16k^2-8k-8 = 8(k-1)(2k+1) = 24z+16z^2.
    schedule_poly = add(scale(mul(add(one,n), add(one,n)),16),
                        scale(add(one,n),-8),scale(one,-8))
    require(schedule_poly == {(1,0): F(24), (2,0): F(16)},
            "schedule positivity polynomial mismatch")

    # Gaussian exponential moments bounded using 2<pi<4, with only
    # rational squared comparisons. These are the three cube coefficients.
    require(F(4,2) < 2**2, "first exponential moment bound")
    require(2 <= 2**2, "second exponential moment bound")
    require(F(9*4,2) < 2**6, "third exponential moment bound")
    require(F(8**3,3*256) == F(2,3), "localization constant")
    require(4+F(2,3) == F(14,3) < 5, "combined error constant")
    require(1-F(14,30) > F(1,2), "strict witness reserve")
    require(F(1,2)+F(14,30) == F(29,30) < 1, "tolerance reserve")

    # Independent finite controls by summing the binomial law and the
    # separate beta raw moments, including N=0 and the endpoints u=0,1.
    kernel_controls = 0
    for degree in range(13):
        for t in [F(i,16) for i in range(17)]:
            total = F(0)
            mass = F(0)
            for j in range(degree+1):
                weight = comb(degree,j)*t**j*(1-t)**(degree-j)
                mean = F(j+1,degree+2)
                square = F((j+1)*(j+2),(degree+2)*(degree+3))
                total += weight*(square-2*t*mean+t*t)
                mass += weight
            formula = F(2,(degree+2)*(degree+3))*(1+(degree-3)*t*(1-t))
            require(mass == 1 and total == formula, "direct kernel control")
            require(0 <= total <= F(1,degree+2), "second-moment bound")
            kernel_controls += 1

    # Exact scalar controls, explicitly NOT Gaussian hinge gaps.
    # H=+/-u(1-u) and H=0 include a zero boundary and a negative control.
    beta_controls = 0
    previous_negative_defect = F(0)
    for degree in range(33):
        negative_defect = F(0)
        for j in range(degree+1):
            mean = F(j+1,degree+2)
            square = F((j+1)*(j+2),(degree+2)*(degree+3))
            value = mean-square
            direct = F((j+1)*(degree-j+1),(degree+2)*(degree+3))
            require(value == direct and value > 0, "beta scalar control")
            negative_defect = max(negative_defect, value)
            beta_controls += 1
        require(previous_negative_defect <= negative_defect <= F(1,4),
                "negative scalar defect monotonicity")
        require(F(1,4)-negative_defect <= F(1,degree+2),
                "scalar approximation control")
        previous_negative_defect = negative_defect

    plans = [plan(F(1)), plan(F(1,10)), plan(F(1,100))]
    k_controls = 0
    for k in [1,2,3,10,100,10000,10**20]:
        b = budget(k)
        require(F(1,256*k**4)**2 == F(1,b["largest_power"]),
                "schedule square-root normalization")
        require(F(1,256*k**4)*(8*k)**3/3 == F(2,3*k),
                "schedule error normalization")
        k_controls += 1

    bad = [lambda v=v: budget(v) for v in [0,-1,True,F(2),1.0]]
    bad += [lambda v=v: plan(v) for v in [F(0),F(-1),F(2),1,0.5]]
    for operation in bad:
        try:
            operation()
        except ValueError:
            pass
        else:
            raise ValueError("malformed input was accepted")

    return {
        "status": "UNIFORM_MOMENT_FRONTIER_ARITHMETIC_PASS",
        "exact_polynomial_identities": 2,
        "direct_kernel_controls": kernel_controls,
        "scalar_beta_controls": beta_controls,
        "schedule_controls": k_controls,
        "input_rejections": len(bad),
        "zero_hinge_control": {"all_beta_values": 0,"defect":0},
        "toy_controls_are_gaussian_claims": False,
        "uniform_beta_sign_verified": False,
        "plans": plans,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = audit()
    blob = (json.dumps(result,sort_keys=True,indent=2)+"\n").encode()
    if args.check:
        expected = Path(__file__).with_name("FRONTIER_EXPECTED.json").read_bytes()
        require(blob == expected, "expected arithmetic record differs")
    print(result["status"], hashlib.sha256(blob).hexdigest())
    if not args.check:
        print(blob.decode(),end="")


if __name__ == "__main__":
    main()
