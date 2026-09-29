#!/usr/bin/env python3
"""Exact algebra and admissible controls, not a uniform-error proof.

Python 3.11+, standard library only. Polynomial coefficients are Fraction.
No floating point is used. The analytic proof is in PROOF.md.
"""

from fractions import Fraction as F


def add(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, F(0)) + value
        if not out[key]:
            del out[key]
    return out


def scale(a, value):
    return {key: value * coefficient for key, coefficient in a.items()
            if value * coefficient}


def mul(a, b, keep):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x + y for x, y in zip(ka, kb))
            if keep(key):
                out[key] = out.get(key, F(0)) + va * vb
    return {key: value for key, value in out.items() if value}


def power(a, n, keep):
    result = {tuple(0 for _ in next(iter(a))): F(1)}
    for _ in range(n):
        result = mul(result, a, keep)
    return result


def basis(n, index):
    key = [0] * n
    key[index] = 1
    return {tuple(key): F(1)}


def check_inverse_distance():
    # Independent implicit check: f^2*((1-delta-x)^2+y^2)=1 through
    # total degree two fixes the positive inverse-square-root branch.
    keep = lambda key: sum(key) <= 2
    one = {(0, 0, 0): F(1)}
    delta, x, y = (basis(3, k) for k in range(3))
    a_minus_x = add(one, scale(add(delta, x), F(-1)))
    squared_distance = add(power(a_minus_x, 2, keep), power(y, 2, keep))
    f = add(one, add(delta, x))
    f = add(f, power(delta, 2, keep))
    f = add(f, scale(mul(delta, x, keep), F(2)))
    f = add(f, power(x, 2, keep))
    f = add(f, scale(power(y, 2, keep), F(-1, 2)))
    assert mul(power(f, 2, keep), squared_distance, keep) == one
    # x^2-y^2/2 = (|zeta|^2+3 Re(zeta^2))/4.
    assert F(1, 4) + F(3, 4) == 1
    assert F(1, 4) - F(3, 4) == F(-1, 2)
    # Coefficients from e1(zeta)=-8c8/9, e2(zeta)=7c7/9.
    assert F(1, 8) * F(-8, 9) == F(-1, 9)
    assert F(3, 32) * F(64, 81) == F(2, 27)
    assert F(3, 32) * F(-14, 9) == F(-7, 48)
    print("PASS inverse-distance expansion and Newton coefficient identities")


def omega_mul(a, b):
    # Q(omega), omega^2+omega+1=0, represented by u+v omega.
    u, v = a
    x, y = b
    return (u*x-v*y, u*y+v*x-v*y)


def omega_power(n):
    result = (F(1), F(0))
    for _ in range(n):
        result = omega_mul(result, (F(0), F(1)))
    return result


def omega_conjugate(a):
    u, v = a
    return (u-v, -v)


def check_cube_constraint():
    assert omega_power(9) == (F(1), F(0))
    assert omega_power(8) == omega_power(2)
    assert omega_power(7) == omega_power(1)
    for n in (7, 8):
        u, v = omega_power(n)
        x, y = omega_conjugate((u, v))
        assert v+y == 0
        assert (u+x)/2 == F(-1, 2)
    assert F(9)/F(3, 2) == 6
    assert 1-F(6, 9) == F(1, 3)
    assert F(1, 9)-F(7, 48) == F(-5, 144)
    assert F(1, 32)-F(5, 144)*F(9, 14) == F(1, 112)
    print("PASS cube-root averaging and local coercivity constants 1/3, 1/112")


def check_defect_integral():
    # Variables are (delta, t, sigma, d, v). Truncate only delta degree.
    # This checks the full rational denominator to the needed order,
    # rather than assuming it is 1 before expansion.
    keep = lambda key: key[0] <= 2
    one = {(0, 0, 0, 0, 0): F(1)}
    delta, t, sigma, d, v = (basis(5, k) for k in range(5))
    a = add(one, scale(delta, F(-1)))
    b = add(scale(delta, F(2)), scale(power(delta, 2, keep), F(-1)))
    mu = add(one, scale(mul(sigma, delta, keep), F(-1)))
    D = mul(d, delta, keep)
    R = add(scale(one, F(9, 2)),
            scale(mul(sigma, delta, keep), F(-8)))
    R = add(R, scale(delta, F(-7, 4)))
    R = add(R, scale(power(delta, 2, keep), F(-7, 8)))
    prefactor = power(add(a, mul(mul(b, mu, keep), t, keep)), 8, keep)
    denominator_base = add(a, mul(mul(b, t, keep), R, keep))
    u = add(denominator_base, scale(one, F(-1)))
    inverse_square = add(add(one, scale(u, F(-2))),
                         scale(power(u, 2, keep), F(3)))
    angular = mul(mul(mul(a, b, keep), t, keep), D, keep)
    variance = scale(mul(mul(power(b, 2, keep), power(t, 2, keep), keep),
                         v, keep), F(1, 2))
    exponent = scale(mul(add(angular, variance), inverse_square, keep), F(-8))
    # Exponent starts in delta degree two, so exp(exponent)=1+exponent.
    assert all(key[0] == 2 for key in exponent)
    integrand = mul(prefactor, add(one, exponent), keep)
    expected = dict(one)
    expected = add(expected, scale(mul(delta, t, keep), F(16)))
    expected = add(expected, scale(delta, F(-8)))
    expected = add(expected, scale(mul(power(delta, 2, keep),
                                      power(t, 2, keep), keep), F(112)))
    expected = add(expected, scale(mul(power(delta, 2, keep), t, keep), F(-120)))
    expected = add(expected, scale(power(delta, 2, keep), F(28)))
    for parameter in (sigma, d):
        expected = add(expected, scale(mul(mul(power(delta, 2, keep),
                                              parameter, keep), t, keep), F(-16)))
    expected = add(expected, scale(mul(mul(power(delta, 2, keep), v, keep),
                                      power(t, 2, keep), keep), F(-16)))
    assert integrand == expected
    integral = {}
    for key, coefficient in integrand.items():
        delta_degree, t_degree, sigma_degree, d_degree, v_degree = key
        out_key = (delta_degree, sigma_degree, d_degree, v_degree)
        integral[out_key] = integral.get(out_key, F(0)) + coefficient/F(t_degree+1)
    integral = {key: value for key, value in integral.items() if value}
    assert integral == {
        (0, 0, 0, 0): F(1),
        (2, 0, 0, 0): F(16, 3),
        (2, 1, 0, 0): F(-8),
        (2, 0, 1, 0): F(-8),
        (2, 0, 0, 1): F(-16, 3),
    }
    assert 1+F(3, 2)*F(1, 3) < F(7, 4)
    assert 1+F(3, 2)*F(1, 2) == F(7, 4)
    print("PASS integrated defect expansion and thin-family variance threshold")


def check_admissible_controls():
    # p=(z-c)^9-(a-c)^9, c>=0, a<=1. Its roots lie in the disk
    # centered at c with radius a-c, hence in |z|<=a<=1. All criticals=c.
    gamma, kappa = F(1, 4), F(1, 224)
    checked = 0
    for delta in (F(0), F(1, 10000), F(1, 1000), F(1, 100)):
        for c in (F(0), F(1, 10000), F(1, 1000), F(1, 100)):
            a = 1-delta
            mu = 1/(a-c)
            Q = 8*c*c
            margin = mu-1-gamma*delta-kappa*Q
            assert margin >= 0
            assert (margin == 0) == (delta == 0 and c == 0)
            checked += 1
    # Thin family is exactly admissible for every 0<=a<=1.
    for a in (F(0), F(1, 2), F(9, 10), F(99, 100), F(1)):
        reciprocal_moduli = [1/(a+1)]*7 + [9/(a+1)]
        mu = sum(reciprocal_moduli)/8
        variance = sum((r-mu)**2 for r in reciprocal_moduli)/8
        assert mu == 2/(a+1)
        assert variance == 7/(a+1)**2
        if a < 1:
            assert (mu-1)/(1-a) == 1/(a+1)
            assert mu > 1+F(1, 4)*(1-a)
    assert F(7, 4) == 7/(F(1)+1)**2
    print(f"PASS {checked} translated-binomial controls and five exact thin-family controls")


if __name__ == "__main__":
    check_inverse_distance()
    check_cube_constraint()
    check_defect_integral()
    check_admissible_controls()
    print("PASS exact algebra; uniform errors and existential radii require PROOF.md")
