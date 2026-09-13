#!/usr/bin/env python3
"""Secondary exact SymPy audit of the field and mixed-contact identities."""

import json

import sympy as sp


def require(condition, message):
    if not condition:
        raise ValueError(message)


x = sp.symbols("x")
alpha = sp.I * sp.sqrt(3)
beta = sp.I * sp.sqrt(11)
sqrt13 = sp.sqrt(13)
u = (5 + alpha * sqrt13) / 8

base_polynomial = sp.minimal_polynomial(alpha + beta, x)
extended_polynomial = sp.minimal_polynomial(alpha + beta + sqrt13, x)
base_degree = sp.Poly(base_polynomial, x).degree()
extended_degree = sp.Poly(extended_polynomial, x).degree()
require(base_degree == 4 and extended_degree == 8, "sqrt(13) field degree")
require(sp.simplify(u**2 - sp.Rational(5, 4) * u + 1) == 0, "u polynomial")
require(sp.simplify(u * sp.conjugate(u)) == 1, "u norm")

# Check the local model in QQ[w,R]/(w^2+w+1,R^2-33).
w, root = sp.symbols("w root")
groebner = sp.groebner([w**2 + w + 1, root**2 - 33], w, root, domain=sp.QQ)


def reduce_local(expression):
    return sp.expand(groebner.reduce(sp.Poly(sp.expand(expression), w, root))[1].as_expr())


alpha2 = 1 + 2 * w
beta2 = root * alpha2 / 3
require(reduce_local(alpha2**2 + 3) == 0, "local alpha")
require(reduce_local(beta2**2 + 11) == 0, "local beta")
require(reduce_local(-alpha2 * beta2 - root) == 0, "local sqrt33")
require(reduce_local((1 + 2 * w**2) + alpha2) == 0, "local conjugation")

# Derive the explicit mixed contact directly in complex radicals.
d = alpha / 15
r = 3 * alpha / 5
omega = (-1 + alpha) / 2
contact = sp.expand(omega * ((1 - u) * d + u * r))
expected_contact = sp.expand(omega * (-sqrt13 + 2 * alpha) / 5)
require(sp.simplify(contact - expected_contact) == 0, "mixed contact formula")
require(sp.simplify(contact * sp.conjugate(contact)) == 1, "mixed contact norm")
require(sp.simplify(omega * sp.conjugate(omega)) == 1, "omega norm")

result = {
    "status": "PASS",
    "sympy": sp.__version__,
    "base_primitive_degree": base_degree,
    "extended_primitive_degree": extended_degree,
    "u_minimal_polynomial_checked": True,
    "u_norm_checked": True,
    "local_quotient_identities_checked": 4,
    "mixed_contact_identity_checked": True,
    "mixed_contact_norm_checked": True,
}
print(json.dumps(result, indent=2, sort_keys=True))
