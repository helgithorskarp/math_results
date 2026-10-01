#!/usr/bin/env python3
"""Optional exact CAS derivation of CERTIFICATE.json; not needed by verify.py."""
import argparse
import json
from pathlib import Path
import sympy as S


def main():
    if S.__version__ != '1.14.0':
        raise ValueError('Use SymPy1.14.0 for the recorded optional derivation')
    n, X, z = S.symbols('n X z')
    N, s, m = X-n-1, X/2-n, X-2*n-2
    e = n*(n-1)/2
    c = n*(n*n-3*n+4)/4
    C2 = n*X/4-n*(n*n-3*n+4)/2
    C4 = (3*n*n-2*n)*X/16-(n**4+n*(n-2)**4)/8
    V = N*(C2+c)-e*e
    a = (2*n+5)/n**2
    HL = m+a*a*C2/2-a**4*C4/8
    DL = e*HL+N*a*C2
    HH = m+2*a*a*C2
    E = (N-s)*HH+m*(s-m)
    P = S.cancel(65536*n**12*(DL*DL-V*E))
    P = S.Poly(P, X, n, domain=S.QQ)
    if P.degree(X) != 3:
        raise ValueError('unexpected degree')
    cs = [S.Poly(P.as_expr(), X).coeff_monomial(X**k) for k in range(4)]
    arrays = [[str(t) for t in reversed(S.Poly(cn, n).all_coeffs())] for cn in cs]
    tests = {'c0': cs[0], 'c2': cs[2], 'c3_lower': cs[3]-8192*n**12,
             'c1_lower': cs[1]+8192*n**17}
    positive = {name: [str(t) for t in reversed(S.Poly(poly.subs(n, z+8), z).all_coeffs())]
                for name, poly in tests.items()}
    if any(int(t) <= 0 for row in positive.values() for t in row):
        raise ValueError('positive shifted certificate fails')
    cert = {'agent': 'six-downset-3', 'role': 'researcher',
            'domain': 'QQ[n,X], X later specialized to2^n, integern>=6; powers in all arrays ascending.',
            'identity': 'P=65536*n^12*(D_lower^2-V*E), E=(N-s)*HH+m*(s-m).',
            'denominator_constant': '65536', 'denominator_n_power': 12,
            'coefficient_arrays': arrays, 'shift': 8,
            'positive_shifted_coefficients': positive}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = json.dumps(cert, indent=2)+'\n'
    if args.output:
        args.output.write_text(raw)
    print(raw, end='')


if __name__ == '__main__':
    main()
