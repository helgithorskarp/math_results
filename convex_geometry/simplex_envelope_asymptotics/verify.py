"""Exact corroboration of the constants and volume formula, not the limit proof."""
from fractions import Fraction as F
from math import factorial
import json

from exact_section import section, sharp_constant
from geometry_check import direct_section


def require(ok, message):
    if not ok:
        raise ValueError(message)


# Q(r), with r^2=1-r. Every coefficient is a Fraction.
def q(a=0, b=0):
    return F(a), F(b)


def add(x, y):
    return x[0] + y[0], x[1] + y[1]


def mul(x, y):
    a, b = x
    c, d = y
    return a*c + b*d, a*d + b*c - b*d


def scale(x, c):
    return mul(x, q(c))


def power(x, n):
    result = q(1)
    for _ in range(n):
        result = mul(result, x)
    return result


def check_moments():
    r, inverse_r, inverse_Z = q(0, 1), q(1, 1), q(F(1, 2), F(-1, 2))
    Z = q(4, 2)
    require(mul(r, inverse_r) == q(1), "inverse r")
    require(mul(Z, inverse_Z) == q(1), "normalization")
    p0 = scale(inverse_Z, 2)
    ptail = mul(inverse_r, inverse_Z)
    require(add(p0, scale(ptail, 2)) == q(1), "mixture mass")
    require(p0 == power(r, 2) and ptail == scale(r, F(1, 2)), "mixture labels")
    moments = [mul(scale(power(inverse_r, k+1), 2*factorial(k)), inverse_Z)
               for k in (1, 2)]
    mean, second = moments
    require(mean == q(1), "cost mean")
    var_cost = add(second, q(-1))
    require(var_cost == q(1, 2), "cost variance")
    raw = add(q(F(1, 3)), add(inverse_r, add(scale(power(inverse_r, 2), 2),
                                              scale(power(inverse_r, 3), 2))))
    var_x = mul(scale(raw, 2), inverse_Z)
    require(var_x == q(F(13, 3), F(8, 3)), "coordinate variance")
    det = mul(var_x, var_cost)
    require(det == q(F(29, 3), 6), "covariance determinant")
    require(scale(ptail, 2) == r, "active fraction")
    return {name: [str(c) for c in value] for name, value in
            (("r", r), ("Z", Z), ("mean_cost", mean), ("variance_x", var_x),
             ("variance_cost", var_cost), ("determinant", det),
             ("active_fraction", scale(ptail, 2)))}


def main():
    moments = check_moments()
    rows = []
    cases = [(2, F(0)), (2, F(1, 3)), (2, F(2)), (2, F(5)),
             (3, F(0)), (3, F(1, 3)), (3, F(1)), (3, F(3)), (3, F(5)),
             (4, F(4))]
    for N, radius in cases:
        value = section(N, radius)
        require(value == direct_section(N, radius),
                f"strata/halfspace disagreement at {N},{radius}")
        if N == 2:
            require(value == 2 + radius, "line normalization")
        rows.append({"N": N, "radius": str(radius), "delta_volume": str(value)})
    constants = {str(n): str(sharp_constant(n)) for n in range(1, 13)}
    require([constants[str(n)] for n in (1, 2, 3)] == ["2", "16/3", "127/8"],
            "preceding geometric constants")
    rejected = 0
    for action in (lambda: section(1), lambda: section(True),
                   lambda: section(3, -1), lambda: sharp_constant(0)):
        try:
            action()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("malformed parameter accepted")
    print(json.dumps({
        "status": "exact corroboration passed",
        "field_basis": ["1", "r"], "moments": moments,
        "geometric_checks": rows, "sharp_constants": constants,
        "malformed_parameters_rejected": rejected,
        "scope": "Written proof establishes asymptotics and total variation; finite checks do not."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
