"""Optional exact dense derivation; SymPy 1.14.0, same author, no native import.

Rebuilds the ENTIRE certificate and all three actual seven-slot records.
Bernstein coefficients are obtained by exact interpolation in the Bernstein
basis, rather than importing verify.py's power-to-Bernstein conversion.
"""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import sympy as s

BASE = Path(__file__).resolve().parent
r, z, u, v = s.symbols("r z u v")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2)+"\n").encode("utf-8")


def coefficients(expression, variable):
    P = s.Poly(expression, variable, domain=s.QQ)
    return [str(P.nth(i)) for i in range(max(0, P.degree())+1)]


def even_to_u(expression):
    out = 0
    for (power,), coefficient in s.Poly(expression, r, domain=s.QQ).terms():
        require(power % 2 == 0, "angular rational coefficient is not even")
        out += coefficient*u**(power//2)
    return s.Poly(out, u, domain=s.QQ)


def interpolate_bernstein(poly):
    degree = s.Poly(poly, u, domain=s.QQ).degree()
    nodes = [s.Rational(j, degree) for j in range(degree+1)]
    basis = s.Matrix([[s.binomial(degree, k)*x**k*(1-x)**(degree-k)
                       for k in range(degree+1)] for x in nodes])
    values = s.Matrix([poly.subs(u, 1+x/4) for x in nodes])
    result = basis.inv()*values
    require(all(x > 0 for x in result), "complete closed-interval positivity")
    rebuilt = sum(result[k]*s.binomial(degree, k)*v**k*(1-v)**(degree-k)
                  for k in range(degree+1))
    require(s.Poly(s.expand(rebuilt-poly.subs(u, 1+v/4)), v).is_zero,
            "whole interpolated Bernstein identity")
    return list(map(str, result))


def derive():
    p, beta, B = r+r**3, r**3, 1+2*r*r-r**4-r**6
    tau, q = (r*r-1)**2*(r*r+1), (z-p)**2+1
    gU = (z*z-p*z+1)**2
    gL = (z-beta)**2*(z*z-2*r*z+B)
    require(s.Poly(s.expand(gU-tau*q-gL), z, r).is_zero,
            "whole companion quartic")
    D3 = (z*z-p*z+1)*(z+beta)
    Q2 = z*z+2*r*z+B
    f = s.Poly(s.expand(D3**2*Q2), z, domain=s.QQ.poly_ring(r))
    h = f.diff().mul_ground(s.Rational(1, 8))
    H4, rem = h.div(s.Poly(D3, z, domain=f.domain))
    require(rem.is_zero and H4.LC() == 1, "whole derivative factorization")
    field = s.QQ.frac_field(r)
    H = s.Poly(H4.as_expr(), z, domain=field)
    inverse = s.invert(H.diff(), H)
    mass = (s.Poly(-8*D3*Q2, z, domain=field)*inverse).rem(H)
    mass2 = (mass*mass).rem(H)
    a, b, c = H.nth(3), H.nth(2), H.nth(1)
    powers = [s.Integer(4), -a, a*a-2*b, -a**3+3*a*b-3*c]
    N = s.expand(-2*f.nth(6))
    X = s.expand(N*N/2-4*f.nth(4))
    D = s.expand(X-N*N/8)
    require(s.cancel(sum(mass.nth(i)*powers[i] for i in range(4))-N) == 0,
            "whole raw mass normalization")
    eta = s.cancel(sum(mass2.nth(i)*powers[i] for i in range(4)))
    C = s.cancel((N*N-eta)/D)
    numerator, denominator = map(even_to_u, s.fraction(C))
    Delta = s.Poly(1, r, domain=s.QQ)
    for i in range(4):
        Delta = s.lcm(Delta, s.Poly(s.fraction(s.cancel(inverse.nth(i)))[1],
                                  r, domain=s.QQ))
    Delta = Delta.monic()
    invnum = [s.cancel(inverse.nth(i)*Delta.as_expr()) for i in range(4)]
    disc = s.Poly(s.discriminant(H4.as_expr(), z), r, domain=s.QQ)
    disc_quotient, rem = disc.div(Delta)
    require(rem.is_zero, "nonzero inverse-denominator specialization bridge")
    gap = s.Poly(16*denominator.as_expr()-numerator.as_expr(), u, domain=s.QQ)
    divided_gap, rem = gap.div(s.Poly(u-1, u))
    require(rem.is_zero, "whole limiting-edge gap")
    certificate = {
        "domain": "QQ[r][z], r>1 and B=1+2r^2-r^4-r^6>0",
        "critical_quartic": [coefficients(H4.nth(i), r) for i in range(5)],
        "inverse_common_denominator": coefficients(Delta.as_expr(), r),
        "inverse_numerators": [coefficients(a, r) for a in invnum],
        "discriminant": coefficients(disc.as_expr(), r),
        "discriminant_divided_by_inverse_denominator":
            coefficients(disc_quotient.as_expr(), r),
        "angular_numerator_u": coefficients(numerator.as_expr(), u),
        "angular_denominator_u": coefficients(denominator.as_expr(), u),
        "complete_bernstein_denominator": interpolate_bernstein(denominator.as_expr()),
        "complete_bernstein_divided_gap": interpolate_bernstein(divided_gap.as_expr()),
    }

    def evaluate_matrix(poly, matrix):
        out = s.zeros(7)
        for coefficient in reversed([poly.nth(i) for i in range(poly.degree()+1)]):
            out = out*matrix+coefficient*s.eye(7)
        return out

    rows = []
    for value in (s.Rational(101, 100), s.Rational(11, 10), s.Rational(10, 9)):
        literal_f = s.Poly(f.as_expr().subs(r, value), z, domain=s.QQ)
        literal_h = literal_f.diff().mul_ground(s.Rational(1, 8))
        matrix = s.zeros(7)
        for j in range(6):
            matrix[j+1, j] = 1
        for j in range(7):
            matrix[j, 6] = -literal_h.nth(j)
        derivative = evaluate_matrix(literal_h.diff(), matrix)
        inverse_matrix = derivative.inv()
        require(derivative*inverse_matrix == s.eye(7), "whole seven-slot inverse")
        mass_matrix = -8*evaluate_matrix(literal_f, matrix)*inverse_matrix
        n, x, d = [t.subs(r, value) for t in (N, X, D)]
        eta_literal = s.trace(mass_matrix*mass_matrix)
        c_literal = (n*n-eta_literal)/d
        require(s.trace(mass_matrix) == n and d > 0 and c_literal < 16
                and c_literal == C.subs(r, value), "actual seven-slot formula")
        original_powers = [s.Integer(8)]
        for k in range(1, 6):
            out = -k*literal_f.nth(8-k)
            for j in range(1, k):
                out -= literal_f.nth(8-j)*original_powers[k-j]
            original_powers.append(out)
        rows.append({"r": str(value), "B": str(B.subs(r, value)),
                     "all_original_first_five_powers": list(map(str, original_powers)),
                     "full_f_coefficients": coefficients(literal_f.as_expr(), z),
                     "full_h_coefficients": coefficients(literal_h.as_expr(), z),
                     "N": str(n), "X": str(x), "D": str(d),
                     "raw_mass_trace": str(s.trace(mass_matrix)),
                     "raw_eta": str(eta_literal), "angular_C": str(c_literal)})
    return certificate, rows


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=BASE/"CERTIFICATE.json")
    parser.add_argument("--expected", type=Path, default=BASE/"EXPECTED.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(s.__version__ == "1.14.0", "recorded CAS version is SymPy1.14.0")
    certificate, cases = derive()
    data = canonical(certificate)
    require(data == args.certificate.read_bytes(), "ENTIRE rebuilt certificate bytes")
    expected = json.loads(args.expected.read_text())
    require(canonical(cases) == canonical(expected["seven_slot_cases"]),
            "ENTIRE rebuilt actual seven-slot records")
    if args.output:
        args.output.write_bytes(data)
    print(json.dumps({"status": "whole certificate and three actual seven-slot records agree",
                      "certificate_bytes": len(data), "certificate_sha256": sha256(data).hexdigest(),
                      "sympy_version": s.__version__, "same_author": True}, sort_keys=True))


if __name__ == "__main__":
    main()
