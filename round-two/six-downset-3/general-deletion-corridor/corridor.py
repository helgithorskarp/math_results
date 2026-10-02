"""Exact scalar identities for the written universal six-order reduction."""
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True,
                            separators=(',', ':')).encode()).hexdigest()


def bound(k):
    require(type(k) is int and k >= 3, 'Integer k>=3')
    return (6*k-7+isqrt(28*k*k-36*k+17))//2


def scalars(q, k):
    require(type(q) is int and type(k) is int and k >= 3 and q >= max(4, k),
            'Quantified domain: integers k>=3,q>=max(4,k)')
    N = (q*q+13*q+16)//2-k
    s = 3*q+4
    h = F(1, 3*q+5)
    alpha = F(q*(q+1), 2)+3*(q+1)*h
    e = F(q*q+(13-6*k)*q+2*k*k-10*k+14, 2)
    B0 = F(q*q+(7-6*k)*q+2*k*k-12*k+8, 2)
    gap = F(N-s)
    a0 = F((2*k+1)*q+k)-F(2*k, q)
    rr = 3+F(2, q)
    d = F(N-2*s)+rr
    ww = (s-rr)/(q-1)
    az = (k-1)*(ww-1)
    aw = 1+k*(ww-1)
    Q0 = e-(k*az*az+(q-k)*aw*aw)/gap-4*q*(k-1)**2/d
    aggregate = e-a0*a0/(q*gap)-F(k*(q-k), q)*ww*ww/gap
    aggregate -= 4*q*(k-1)**2/d
    S = alpha-2*k*h
    D4 = S-2*h*(a0/gap+F(4*q*(1-k), d))
    require(gap > 0 and d > 0 and a0 > 2*k*q and Q0 == aggregate,
            'Positive denominators and exact strengthened scalar identity')
    return {'N': N, 's': s, 'h': h, 'alpha': alpha, 'e': e, 'B0': B0,
            'gap': gap, 'a0': a0, 'd': d, 'ww': ww, 'az': az, 'aw': aw,
            'Q0': Q0, 'D4': D4, 'S': S}


def region(q, k):
    # This is a threshold reduction, not a complete feasibility classifier.
    values = scalars(q, k)
    b = bound(k)
    if q <= b-6:
        return 'excluded_all_real_ansatz_by_written_theorem'
    if q >= b+1:
        require(values['B0'] > 0, 'Strict credited constructive tail')
        return 'constructively_feasible_by_imported_9195'
    return 'six_order_threshold_corridor_no_sufficiency_claim'


def mul(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def add(*terms):
    out = [0]*max(map(len, terms))
    for term in terms:
        for i, x in enumerate(term):
            out[i] += x
    return out


def check_positive_cubic(candidate):
    actual = add(mul([0, 0, 16], [1, 6]),
                 mul([16, -32, 16], [7, 6]),
                 [-x for x in mul([-9, 5], mul([7, 6], [1, 6]))])
    require(candidate == actual == [175, 269, 20, 12] and
            all(x > 0 for x in candidate), 'Exact positive cubic identity')
    return actual


def check_tail_root(k, candidate):
    require(scalars(candidate, k)['B0'] <= 0 <
            scalars(candidate+1, k)['B0'], 'Strict admissible upper root floor')


def algebra():
    # These are polynomial coefficient equalities, not sampled fits.
    DB = [17, -36, 28]
    sqrt_difference = add(DB, [-x for x in mul([-2, 5], [-2, 5])])
    require(sqrt_difference == mul([-13, 3], [-1, 1]) == [13, -16, 3],
            'DB-(5k-2)^2=(3k-13)(k-1)')
    root_upper = add(mul([7, 6], [7, 6]), [-x for x in DB])
    require(root_upper == [32, 120, 8], 'rB<6k identity')
    cubic = check_positive_cubic([175, 269, 20, 12])
    L4 = F(128, 31)+F(72, 25)
    require(L4-7 == F(7, 775), 'Positive k4 margin')
    require(321 > 17*17, 'Strict k4 square-root lower bound')
    # Monomials (R degree,k degree):
    # 2e(R-6,k)-2(19k-18-3R) = 2B0(R,k).
    reduced = {(2, 0): 1, (1, 1): -6, (1, 0): -12+13+6,
               (0, 2): 2, (0, 1): 36-10-38, (0, 0): 36-78+14+36}
    require(reduced == {(2, 0): 1, (1, 1): -6, (1, 0): 7,
                        (0, 2): 2, (0, 1): -12, (0, 0): 8},
            'Root substitution identity for all R,k')
    # k3 has b=11 and only q4,5 below b-5 in the admissible domain.
    require(bound(3) == 11 and scalars(4, 3)['e'] == -1,
            'Sole finite exception domain')
    # Square discriminant k8 is an actual strict-tail endpoint.
    require(bound(8) == 40 and scalars(40, 8)['B0'] == 0,
            'Perfect-square strict endpoint')
    return {'sqrt_difference_coefficients': sqrt_difference,
            'root_upper_coefficients': root_upper,
            'positive_cubic_coefficients': cubic,
            'root_substitution_coefficients': [reduced[a] for a in sorted(reduced)],
            'k4_margin': str(L4-7), 'k3_b': 11, 'k3_q4_e': '-1',
            'strict_square_endpoint': {'k': 8, 'q': 40, 'B0': '0'},
            'coverage': 'Written universal argument; finite algebra is not an all-k sweep'}
