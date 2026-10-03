#!/usr/bin/env python3
"""Optional dense SymPy reconstruction of the ENTIRE exact record.

No import of verify.py or its arithmetic. Same-author validation, not an
independent mathematical review. The continuous proof is in PROOF.md.
"""
import hashlib
import json
from pathlib import Path

import sympy as s


def require(condition, message):
    if not condition:
        raise ValueError(message)


def coefficients(expression, z):
    p = s.Poly(s.expand(expression), z, domain=s.QQ)
    return [str(c) for c in reversed(p.all_coeffs())]


def matrix_record(a):
    return [[str(a[i, j]) for j in range(a.cols)] for i in range(a.rows)]


def main():
    require(s.__version__ == "1.14.0", "requires documented SymPy 1.14.0")
    z = s.symbols("r")
    cases = []
    for n in (7, 8):
        for k in (1, 2, 3):
            m = n-1-k
            middle = m-k*z
            cubic = s.expand(-m+middle**3+k*z**3)
            lo, hi = s.Rational(m, k+1), s.Rational(m+1, k)
            row = {"n": n, "m": m, "k": k,
                   "interval": [str(lo), str(hi)],
                   "middle": coefficients(middle, z), "cubic": coefficients(cubic, z)}
            if k == 1:
                center, factor, remainder = (s.Rational(5, 2), 15, s.Rational(105, 4)) if n == 7 else (s.Integer(3), 18, s.Integer(48))
                square = factor*(z-center)**2+remainder
                require(s.expand(cubic-square) == 0 and factor > 0 and remainder > 0,
                        "square identity")
                row["certificate"] = {"route": "positive_square", "center": str(center),
                                      "factor": str(factor), "remainder": str(remainder),
                                      "square_identity": coefficients(square, z)}
            elif k == 2:
                f = z**3-8*z**2+16*z-10 if n == 7 else z**3-10*z**2+25*z-20
                outer = s.Integer(4 if n == 7 else 5)
                require(s.expand(cubic+6*f) == 0, "whole cubic factor")
                require(s.expand(s.diff(f, z)-3*(z-lo)*(z-outer)) == 0, "derivative factor")
                require(lo < hi < outer and f.subs(z, lo) < 0, "entire interval sign")
                row["certificate"] = {"route": "decreasing_negative_cubic",
                                      "factor": coefficients(f, z),
                                      "derivative": coefficients(s.diff(f, z), z),
                                      "outer_derivative_root": str(outer),
                                      "left_value": str(f.subs(z, lo))}
            elif n == 7:
                q = 8*z**2-19*z+8
                ends = [q.subs(z, lo), q.subs(z, hi)]
                require(s.expand(cubic+3*(z-1)*q) == 0, "whole middle-zero factor")
                require(s.diff(q, z, 2) > 0 and max(ends) < 0 and lo < 1 < hi,
                        "closed quadratic interval")
                require(middle.subs(z, 1) == 0, "middle support drops")
                row["certificate"] = {"route": "only_zero_middle_root",
                                      "quadratic": coefficients(q, z),
                                      "quadratic_endpoint_values": [str(x) for x in ends],
                                      "interior_root": "1", "middle_at_root": "0"}
            else:
                require(s.factor(cubic) == -12*(z-1)**2*(2*z-5), "complete endpoint factorization")
                require(lo == 1 and hi < s.Rational(5, 2), "open interval sign")
                row["certificate"] = {"route": "positive_endpoint_square",
                                      "double_root": "1", "remaining_factor": ["-5", "2"],
                                      "remaining_factor_at_right": str(2*hi-5)}
            cases.append(row)
    v = s.Matrix([1, 1, 1, -1, -1, -1, 0, 0])
    moments = [sum(x**j for x in v) for j in range(1, 7)]
    norm = moments[1]
    p = s.eye(8)-s.ones(8)/8
    h = p*s.diag(*v)*p
    nodes = [s.Integer(-1), s.Rational(-1, 2), s.Integer(0), s.Rational(1, 2), s.Integer(1)]
    spectral_records, projections = [], []
    for lam in nodes:
        # Dense evaluation of the Lagrange polynomial at H; no sparse Fraction
        # matrix code from the portable checker is imported.
        lagrange = s.prod((z-other)/(lam-other) for other in nodes if other != lam)
        cp = s.Poly(lagrange, z, domain=s.QQ)
        proj = s.zeros(8)
        for (degree,), coef in cp.terms():
            proj += coef*h**degree
        require(proj**2 == proj and h*proj == lam*proj and proj.T == proj,
                "full projector equations")
        image = proj*v
        mass = (image.T*image)[0]
        spectral_records.append({"eigenvalue": str(lam), "rank": int(proj.trace()),
                                 "matrix": matrix_record(proj), "image": [str(x) for x in image],
                                 "raw_full_mass": str(mass), "normalized_full_mass": str(mass/norm)})
        projections.append(proj)
    require(sum(projections, s.zeros(8)) == s.eye(8), "complete ambient spectral decomposition")
    for i, a in enumerate(projections):
        for b in projections[i+1:]:
            require(a*b == s.zeros(8), "all distinct full projectors orthogonal")
    f = s.prod(z-x for x in v)
    critical = s.diff(f, z)/8
    char = h.charpoly(z).as_expr()
    require(s.expand(char-z*critical) == 0, "independent dense characteristic polynomial")
    masses = [s.Rational(row["raw_full_mass"]) for row in spectral_records]
    eta = sum(m*m for m in masses)/norm**2
    normalized_x = moments[3]/norm**2
    d = normalized_x-s.Rational(1, 8)
    c = (1-eta)/d
    require(moments == [0, 6, 0, 6, 0, 6] and masses == [0, 3, 0, 3, 0] and c == 12,
            "actual equality control")
    record = {"cases": cases,
              "small_support": [{"n": n, "cauchy_lower": str(s.Rational(1, n))} for n in range(1, 7)],
              "equality": {"profile": [str(x) for x in v], "moments_1_to_6": [str(x) for x in moments],
                           "original_polynomial": coefficients(f, z), "critical_polynomial": coefficients(critical, z),
                           "ambient_characteristic": coefficients(char, z), "ambient_H": matrix_record(h),
                           "full_projectors": spectral_records, "X": str(normalized_x),
                           "eta": str(eta), "D": str(d), "C": str(c)},
              "angular": {"level_bounds": [{"r": r, "upper": str(s.Rational(24*(r-2), r-1))} for r in range(2, 9)],
                          "strict_universal_upper": "144/7",
                          "gap_to_49_over_2": str(s.Rational(49, 2)-s.Rational(144, 7))}}
    raw = (json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False)+"\n").encode()
    require(raw == Path(__file__).with_name("expected.json").read_bytes(), "entire CAS record differs")
    print(json.dumps({"status": "verified", "whole_record_matches": True, "sympy": s.__version__,
                      "record_bytes": len(raw), "record_sha256": hashlib.sha256(raw).hexdigest(),
                      "dense_characteristic_polynomial_checked": True}))


if __name__ == "__main__":
    main()
