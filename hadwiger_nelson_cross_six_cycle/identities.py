"""Exact symbolic checks of the proof's polynomial identities; no CAS needed."""
from fractions import Fraction as Q
from collections import defaultdict
from hashlib import sha256
import json


class P:
    """Sparse rational polynomials, with sorted variable-name monomials."""
    def __init__(self, terms=0):
        if isinstance(terms, P):
            terms = terms.terms
        if not isinstance(terms, dict):
            terms = {(): Q(terms)}
        self.terms = {m: Q(c) for m, c in terms.items() if c}

    def __add__(self, other):
        terms = defaultdict(Q, self.terms)
        for m, c in P(other).terms.items():
            terms[m] += c
        return P(dict(terms))

    __radd__ = __add__

    def __neg__(self):
        return P({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        terms = defaultdict(Q)
        for m, c in self.terms.items():
            for n, d in P(other).terms.items():
                terms[tuple(sorted(m+n))] += c*d
        return P(dict(terms))

    __rmul__ = __mul__

    def __pow__(self, n):
        if not isinstance(n, int) or n < 0:
            raise ValueError("nonnegative integral power required")
        result = P(1)
        for _ in range(n):
            result *= self
        return result


def variables(names):
    return [P({(s,): 1}) for s in names.split()]


def main():
    records = []

    def identity(name, left, right):
        if (left-right).terms:
            raise ValueError("failed polynomial identity: "+name)
        stream = json.dumps(
            [(list(m), str(c)) for m, c in sorted(P(left).terms.items())],
            separators=(',', ':'))
        records.append({"identity": name, "expanded_terms": len(P(left).terms),
                        "left_sha256": sha256(stream.encode()).hexdigest()})

    dx, dy, s = variables("dx dy s")
    identity("unit_circle_offset_norm",
             (dx-3*dy*s)**2+3*(dy+dx*s)**2,
             (dx*dx+3*dy*dy)*(1+3*s*s))
    x, y, bx, by, cx, cy, t, s = variables("x y bx by cx cy t s")
    identity("two_independent_quadratic_centres",
             (x+bx*t-cx*s)**2+(y+by*t-cy*s)**2,
             x*x+y*y+(bx*bx+by*by)*t*t+(cx*cx+cy*cy)*s*s
             +2*(x*bx+y*by)*t-2*(x*cx+y*cy)*s
             -2*(bx*cx+by*cy)*t*s)
    identity("orthogonality_determinant",
             (bx*bx+by*by)*(cx*cx+cy*cy),
             (bx*cx+by*cy)**2+(bx*cy-by*cx)**2)
    c, cb, u, T, J, S = variables("c cb u T J S")
    identity("cross_edge_minimal_polynomial_reduction",
             c*u*u-S*u+cb,
             c*(u*u-T*u+J)+(c*T-S)*u+(cb-c*J))
    r = variables("r0 r1 r2")
    s = variables("s0 s1 s2")
    t, = variables("t")
    R, S = sum(r), sum(s)
    f = [S-s[i]-2*t*r[i] for i in range(3)]
    g = [R-r[i]-2*t*s[i] for i in range(3)]
    identity("six_cycle_sum_fixed", sum(f), 2*(S-t*R))
    identity("six_cycle_sum_moving", sum(g), 2*(R-t*S))
    identity("six_cycle_centroid_elimination", (1-t*t)*R,
             Q(1, 2)*(sum(g)+t*sum(f)))
    for i in range(3):
        identity("six_cycle_angle_elimination_"+str(i),
                 (1-4*t*t)*r[i], R-2*t*S-g[i]+2*t*f[i])
    a, b = variables("a b")
    identity("collinear_six_cycle_rational_parameter",
             a*a+a*b+b*b,
             Q(1, 2)*(a*a+b*b+(-a-b)**2))
    print(json.dumps({"identities_checked": len(records), "records": records,
                      "all_expansions_match": True,
                      "uniform_theorem_requires_PROOF_md": True}, indent=2))


if __name__ == '__main__':
    main()
