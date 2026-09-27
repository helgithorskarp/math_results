#!/usr/bin/env python3
"""Exact supporting arithmetic for the relative spherical transfer.

Standard-library Python >=3.11. The continuum estimates and spherical
margin premise are proved/stated in PROOF.md, not certified by sampling.
"""

from fractions import Fraction as F
import json


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


# Laurent monomials in (K,Kp,p,b,q,epsilon,mpp).
NV = 7


def mono(coefficient, **exponents):
    names = ["K", "Kp", "p", "b", "q", "epsilon", "mpp"]
    return {tuple(exponents.get(k, 0) for k in names): F(coefficient)}


def add(*polys):
    out = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            out[exponent] = out.get(exponent, F(0)) + coefficient
    return {k: v for k, v in out.items() if v}


def mul(p, q):
    out = {}
    for a, c in p.items():
        for b, d in q.items():
            key = tuple(x+y for x, y in zip(a, b))
            out[key] = out.get(key, F(0)) + c*d
    return {k: v for k, v in out.items() if v}


def partial(poly, variable):
    out = {}
    for exponent, coefficient in poly.items():
        if exponent[variable]:
            new = list(exponent)
            new[variable] -= 1
            out[tuple(new)] = coefficient*exponent[variable]
    return out


def radial_derivative_identity():
    integrand = mono(1, K=1, p=5, b=-1)
    # dK/dp=Kp, db/dp=1-epsilon*mpp, dp/dq=q/b.
    dp = add(mul(partial(integrand, 0), mono(1, Kp=1)),
             partial(integrand, 2),
             mul(partial(integrand, 3),
                 add(mono(1), mono(-1, epsilon=1, mpp=1))))
    result = mul(dp, mono(1, q=1, b=-1))
    expected = add(mono(1, Kp=1, q=1, p=5, b=-2),
                   mono(5, K=1, q=1, p=4, b=-2),
                   mono(-1, K=1, q=1, p=5, b=-3),
                   mono(1, K=1, q=1, p=5, b=-3, epsilon=1, mpp=1))
    require(result == expected, "formal radial derivative identity")
    return {"monomials": len(result), "status": "IDENTITY_PASS"}


def coefficient_budgets():
    a = F(5, 4)
    inverse_square_difference = 2*F(5, 2)*4
    inverse_cube_difference = 2*(F(3, 2)**2+F(3, 2)+1)*8
    require(inverse_square_difference == 20 and inverse_cube_difference == 76,
            "inverse power difference constants")
    r1 = a**5*4
    r2 = 5*a**4*4+a**5*8
    r1_error = 5*a**4*4+20
    r2_error = 5*(4*a**3*4+20)+(5*a**4*8+76)
    epsilon_error = a**5*8
    require(r1 == F(3125, 256) and r1 < 13, "R1 size")
    require(r2 == F(9375, 128) and r2 < 80, "R2 size")
    require(r1_error == F(4405, 64) and r1_error < 70, "R1 difference")
    require(r2_error == F(13757, 32) and r2_error < 440, "R2 difference")
    require(epsilon_error < 25, "epsilon coefficient")
    coefficients = [440, 4*70+80*5+25, 13*26]
    require(coefficients == [440, 705, 338], "derivative difference coefficients")
    require(all(x <= y for x, y in zip(coefficients, [800, 1600, 800])),
            "800 q^2(1+q)^2 envelope")
    # Integral q^2/sqrt(lambda^2-q^2) is pi*lambda^2/4.
    require(F(800, 32*4) == F(25, 4), "outer error pi coefficient")
    return {"R1_max": str(r1), "R2_absolute_max": str(r2),
            "R1_error_over_z": str(r1_error),
            "R2_error_over_z": str(r2_error),
            "R2_epsilon_coefficient": str(epsilon_error),
            "polynomial_coefficients_q2_q3_q4": coefficients,
            "outer_error_coefficient_of_pi": "25/4"}


def modal_budget():
    epsilon = F(1, 64)
    lam = F(1, 2)
    kappa = 1-epsilon
    require(kappa**-3 < 3, "curvature inverse cube")
    require(16**2 <= 17**2*kappa, "c sqrt(w0)<=17 epsilon")
    require(22*epsilon < 1 and 4+17*epsilon < 5, "local exponential budget")
    require(4*epsilon/lam == F(1, 8), "prefix/radius separation")
    # Direct normalization gives 180/sqrt(2); use the rational upper 256.
    require(180**2 < 2*256**2, "physical modal prefix constant")
    require(F(2*16*4**4, 4*32) == 64, "limiting modal prefix constant")
    prefix = 320*epsilon**3/lam**2
    require(prefix == F(5, 1024) and prefix < 1, "total normalized prefix budget")
    # Constant-kernel normalization in the exact spherical representation.
    require(F(1, 32)*4*F(2, 3) == F(1, 12), "J(lambda) leading D lambda^2/12")
    require(F(9, 64) > F(1, 8), "middle/high-noise range overlap")
    return {"max_epsilon": str(epsilon), "min_lambda_R": str(lam),
            "actual_prefix_constant": 256, "limit_prefix_constant": 64,
            "prefix_error_over_D_epsilon_upper": str(prefix),
            "small_lambda_J_over_D_coefficient": "1/12",
            "high_noise_overlap": True}


def two_point_calibration():
    eta = F(1, 3888)
    c2_upper = 1+450*3**9
    require(c2_upper == 8857351, "C(2) rational upper bound using e<3")
    required = 2*c2_upper/eta
    variance = 2**37
    require(variance >= 64 and variance > required,
            "one variance covers the loss-normalized spherical premise")
    require(F(c2_upper, variance) < eta/2, "error is below half the normalized margin")
    controls = []
    for j in [0, 1, 4, 16, 64, 128]:
        radius = 1-F(1, 2**j)
        loss = 2*(1-radius**2)
        lower_j = eta*loss
        error = F(c2_upper, variance)*loss
        require(loss > 0 and error < lower_j/2, "vanishing-loss calibration")
        controls.append({"target_radius": str(radius), "loss": str(loss),
                         "assumed_from_analytic_control_J_lower": str(lower_j),
                         "Gaussian_normalized_error_upper": str(error)})
    require(eta*0 == F(c2_upper, variance)*0 == 0, "isometry equality")
    return {"scope": "normalization control on an already positive two-point class",
            "spherical_parameter_interval": ["1/2", "2"],
            "analytic_J_over_D_lower": str(eta), "C2_upper": c2_upper,
            "variance_requirement_upper": str(required),
            "one_sufficient_variance": variance,
            "controls": controls, "zero_loss_equalities": True}


def main():
    result = {"schema": "relative-spherical-transfer-v1",
              "status": "EXACT_RELATIVE_TRANSFER_CHECKS_PASS",
              "formal_identity": radial_derivative_identity(),
              "coefficient_budgets": coefficient_budgets(),
              "modal_budget": modal_budget(),
              "two_point_calibration": two_point_calibration(),
              "trust_boundary": "unformalized continuum proof; general spherical margin and overlapping tail remain premises"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
