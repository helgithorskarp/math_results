#!/usr/bin/env python3
"""Optional exact identities in QQ[r,x]; SymPy 1.14.0.

Checks k=1,...,9 symbolically in r. It does not replace the uniform proof.
"""
import json
import sympy as sp

r, x = sp.symbols("r x")


def choose_polynomial(top, degree):
    return sp.prod(top - j for j in range(degree)) / sp.factorial(degree)


checks = 0
for k in range(1, 10):
    q = sum(choose_polynomial(r - 1 + j, j) * choose_polynomial(x + j, j)
            for j in range(k))
    interpolation = sum(
        choose_polynomial(r - 1, h - 1)
        * sp.prod(x + j for j in range(1, k + 1) if j != h)
        / (sp.factorial(h - 1) * sp.factorial(k - h))
        for h in range(1, k + 1))
    if not sp.Poly(sp.expand(q - interpolation), r, x, domain=sp.QQ).is_zero:
        raise AssertionError(("interpolation", k))
    checks += 1
    for h in range(1, k + 1):
        expected = (-1) ** (h - 1) * choose_polynomial(r - 1, h - 1)
        if not sp.Poly(sp.expand(q.subs(x, -h) - expected), r, domain=sp.QQ).is_zero:
            raise AssertionError(("sign identity", k, h))
        checks += 1

print(json.dumps({"all_checks_passed": True, "domain": "QQ[r,x]",
                  "k_range": [1, 9], "identity_checks": checks,
                  "sympy_version": sp.__version__}, sort_keys=True, indent=2))
