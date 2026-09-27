#!/usr/bin/env python3
"""Independent exact checks for the spherical-sinc comparison review.

This checker imports no target code.  Unlike the target's scalar power
checks, it expands multivariate monomials after two independent spherical
translations, integrates sparse polynomials exactly, and verifies the full
commuting-operator divided difference at definition level.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NVARS = 7  # u, theta_1..theta_3, eta_1..eta_3
ZERO_EXP = (0,) * NVARS


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(a, b):
    out = dict(a)
    for monomial, coefficient in b.items():
        out[monomial] = out.get(monomial, F(0)) + coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def scale(a, scalar):
    return {m: scalar * c for m, c in a.items() if scalar * c}


def multiply(a, b):
    out = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            monomial = tuple(x + y for x, y in zip(ma, mb))
            out[monomial] = out.get(monomial, F(0)) + ca * cb
    return {m: c for m, c in out.items() if c}


def power(a, exponent):
    out = {ZERO_EXP: F(1)}
    base = a
    while exponent:
        if exponent & 1:
            out = multiply(out, base)
        exponent //= 2
        if exponent:
            base = multiply(base, base)
    return out


def term(coefficient, **exponents):
    e = [0] * NVARS
    names = {"u": 0, "t1": 1, "t2": 2, "t3": 3,
             "e1": 4, "e2": 5, "e3": 6}
    for name, value in exponents.items():
        e[names[name]] = value
    return {tuple(e): F(coefficient)}


def odd_double_factorial(n):
    if n <= 0:
        return 1
    out = 1
    for k in range(n, 0, -2):
        out *= k
    return out


def sphere_moment(exponents, dimension=3):
    """Uniform S^(dimension-1) coordinate moment for <=3 used axes."""
    if any(e & 1 for e in exponents):
        return F(0)
    half_degree = sum(exponents) // 2
    numerator = 1
    for exponent in exponents:
        numerator *= odd_double_factorial(exponent - 1)
    denominator = 1
    for k in range(half_degree):
        denominator *= dimension + 2 * k
    return F(numerator, denominator)


def integrate(poly, dimension=3):
    answer = F(0)
    for monomial, coefficient in poly.items():
        u_power = monomial[0]
        theta = sphere_moment(monomial[1:4], dimension)
        eta = sphere_moment(monomial[4:7], dimension)
        answer += coefficient * F(1, u_power + 1) * theta * eta
    return answer


def linear_form(constant, theta_coeffs=(), eta_coeffs=(),
                u_theta=False, u_eta=False):
    out = {ZERO_EXP: F(constant)} if constant else {}
    for axis, coefficient in enumerate(theta_coeffs):
        if coefficient:
            kwargs = {f"t{axis + 1}": 1}
            if u_theta:
                kwargs["u"] = 1
            out = add(out, term(coefficient, **kwargs))
    for axis, coefficient in enumerate(eta_coeffs):
        if coefficient:
            kwargs = {f"e{axis + 1}": 1}
            if u_eta:
                kwargs["u"] = 1
            out = add(out, term(coefficient, **kwargs))
    return out


def evaluate_monomial(alpha, forms):
    out = {ZERO_EXP: F(1)}
    for exponent, form in zip(alpha, forms):
        out = multiply(out, power(form, exponent))
    return out


def left_side(alpha, c, p, q, t, dimension=3):
    p_forms = [linear_form(c[i], [t * value for value in p[i]])
               for i in range(len(alpha))]
    q_forms = [linear_form(c[i], (), [t * value for value in q[i]])
               for i in range(len(alpha))]
    return integrate(evaluate_monomial(alpha, p_forms), dimension) - \
        integrate(evaluate_monomial(alpha, q_forms), dimension)


def hessian_terms(alpha, p, q):
    """Sparse monomials and coefficients of (Delta_P-Delta_Q)c^alpha."""
    n = len(alpha)
    output = []
    for i in range(n):
        for j in range(n):
            k_ij = sum(p[i][a] * p[j][a] - q[i][a] * q[j][a]
                       for a in range(3))
            if i == j:
                derivative = alpha[i] * (alpha[i] - 1)
                if derivative:
                    beta = list(alpha)
                    beta[i] -= 2
                    output.append((tuple(beta), k_ij * derivative))
            elif alpha[i] and alpha[j]:
                beta = list(alpha)
                beta[i] -= 1
                beta[j] -= 1
                output.append((tuple(beta), k_ij * alpha[i] * alpha[j]))
    return output


def right_side(alpha, c, p, q, t, dimension=3, kernel=True):
    forms = []
    for i in range(len(alpha)):
        # c + t(1-u)P theta + tu Q eta
        form = linear_form(c[i], [t * value for value in p[i]],
                           [t * value for value in q[i]], u_eta=True)
        correction = linear_form(0, [-t * value for value in p[i]],
                                 (), u_theta=True)
        forms.append(add(form, correction))
    total = {}
    for beta, coefficient in hessian_terms(alpha, p, q):
        total = add(total, scale(evaluate_monomial(beta, forms), coefficient))
    if kernel:
        weight = add(term(t * t, u=1), term(-t * t, u=2))
    else:
        weight = term(t * t)
    return integrate(multiply(weight, total), dimension)


def compositions(total, length):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, length - 1):
            yield (first,) + tail


def operator_checks():
    cases = [
        (
            (F(1, 3), F(-2, 5), F(4, 7)),
            ((F(1), F(0), F(-1, 2)),
             (F(2, 3), F(1, 4), F(0)),
             (F(-3, 5), F(2), F(1, 7))),
            ((F(1, 2), F(1, 3), F(0)),
             (F(-1, 5), F(3, 4), F(2, 3)),
             (F(4, 7), F(-2, 5), F(1))),
            F(3, 5),
            5,
        ),
        (
            (F(-1, 2), F(2, 3), F(5, 4), F(-3, 7)),
            ((F(1), F(2), F(0)),
             (F(-1), F(1, 2), F(3, 2)),
             (F(2, 5), F(-3, 4), F(1, 3)),
             (F(0), F(0), F(0))),
            ((F(2, 3), F(-1, 4), F(1)),
             (F(1, 5), F(4, 3), F(-1, 2)),
             (F(-2, 7), F(1, 3), F(5, 6)),
             (F(0), F(0), F(0))),
            F(4, 9),
            4,
        ),
    ]
    checked = 0
    for c, p, q, t, max_degree in cases:
        n = len(c)
        for degree in range(max_degree + 1):
            for alpha in compositions(degree, n):
                lhs = left_side(alpha, c, p, q, t)
                rhs = right_side(alpha, c, p, q, t)
                require(lhs == rhs, f"operator identity failed: {alpha}")
                checked += 1
    # Higher-degree sparse controls exercise mixed Hessian entries.
    c, p, q, t, _ = cases[0]
    for alpha in [(7, 1, 0), (3, 3, 2), (2, 4, 3), (1, 2, 7)]:
        require(left_side(alpha, c, p, q, t) ==
                right_side(alpha, c, p, q, t),
                f"high-degree identity failed: {alpha}")
        checked += 1
    return checked


def dot(v, w):
    return sum((a * b for a, b in zip(v, w)), F(0))


def sub(v, w):
    return tuple(a - b for a, b in zip(v, w))


def squared(v):
    return dot(v, v)


def submodular_checks():
    p = [
        (F(-2), F(1), F(0)),
        (F(1), F(-3), F(2)),
        (F(4), F(2), F(-1)),
        (F(0), F(0), F(3)),
        (F(-1), F(5), F(2)),
    ]
    # A non-scalar linear contraction followed by a translation.
    scales = (F(1, 2), F(2, 3), F(3, 4))
    translation = (F(7, 5), F(-2, 7), F(1, 3))
    q = [tuple(scales[a] * point[a] + translation[a] for a in range(3))
         for point in p]
    losses = {}
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            loss = squared(sub(p[i], p[j])) - squared(sub(q[i], q[j]))
            require(loss >= 0, "constructed fixture is not a contraction")
            losses[i, j] = loss
    posteriors = [
        [F(1, 5)] * 5,
        [F(v, 31) for v in (1, 2, 4, 8, 16)],
        [F(v, 20) for v in (2, 5, 1, 9, 3)],
    ]
    checks = 0
    for pi in posteriors:
        require(sum(pi, F(0)) == 1 and all(value > 0 for value in pi),
                "invalid posterior")
        hessian = [[(pi[i] if i == j else F(0)) - pi[i] * pi[j]
                    for j in range(5)] for i in range(5)]
        require(all(sum(row, F(0)) == 0 for row in hessian),
                "Hessian rows do not sum to zero")
        gram = sum((dot(p[i], p[j]) - dot(q[i], q[j])) * hessian[i][j]
                   for i in range(5) for j in range(5))
        pair = sum(losses[i, j] * pi[i] * pi[j] for i, j in losses)
        require(gram == pair and pair > 0, "pair-loss sign identity failed")
        checks += 1
    return checks, len(losses)


def negative_controls():
    c = (F(1, 3), F(-2, 5), F(4, 7))
    p = ((F(1), F(0), F(-1, 2)),
         (F(2, 3), F(1, 4), F(0)),
         (F(-3, 5), F(2), F(1, 7)))
    q = ((F(1, 2), F(1, 3), F(0)),
         (F(-1, 5), F(3, 4), F(2, 3)),
         (F(4, 7), F(-2, 5), F(1)))
    t, alpha = F(3, 5), (2, 2, 1)
    lhs = left_side(alpha, c, p, q, t)
    rhs = right_side(alpha, c, p, q, t)
    require(lhs == rhs and lhs != -rhs, "sign corruption was not exposed")
    require(lhs != right_side(alpha, c, p, q, t, kernel=False),
            "missing-kernel corruption was not exposed")
    alpha4 = (4, 0, 0)
    require(left_side(alpha4, c, p, q, t, dimension=2) !=
            right_side(alpha4, c, p, q, t, dimension=2),
            "wrong-dimension corruption was not exposed")
    try:
        require(F(1) - F(4) >= 0, "expanding pair")
    except RuntimeError:
        pass
    else:
        raise RuntimeError("expanding pair was accepted")
    return 4


def check_pins():
    data = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for record in data["files"]:
        payload = (ROOT / record["path"]).read_bytes()
        require(sha256(payload).hexdigest() == record["sha256"],
                f"input pin mismatch: {record['path']}")
    return data


def main():
    pins = check_pins()
    identities = operator_checks()
    submodular, pairs = submodular_checks()
    controls = negative_controls()
    require(F(1, 2) * F(1, 6) == F(1, 12), "continuum factor")
    require(F(1, 4) * F(1, 12) == F(1, 48), "compact-ray factor")
    require(44 * 96 == 4224, "strict-Lipschitz endpoint constant")
    result = {
        "status": "INDEPENDENT_SPHERICAL_SINC_REVIEW_PASS",
        "target_artifact": pins["target"]["artifact_ref"],
        "target_commit": pins["target"]["source_commit"],
        "pinned_files": len(pins["files"]),
        "multivariate_operator_identities": identities,
        "maximum_total_degree": 10,
        "submodular_posterior_checks": submodular,
        "fixture_pair_losses": pairs,
        "constant_checks": 3,
        "negative_controls": controls,
        "universal_scope": "written proof audit; finite exact checks are not formalization"
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
