"""Rational whole certificate entries, with no downset or matrix allocation."""
from fractions import Fraction as F
import pins
from literal import table
from variance import scalar_record, require

EDGES = {(1, 2): 1, (1, 4): 1, (2, 5): -1, (3, 4): -1}


def parameters(q, k, variance_only=False):
    require(type(q) is int and type(k) is int and k >= 5 and q >= max(4, k),
            'literal integer k>=5,q>=max(4,k)')
    r = scalar_record(q, k)
    if (q, k) == (24, 6) and not variance_only:
        r.update(kappa='1/4096', t='5',
                 certified_nonempty_and_projected_cap_floor='1/1048576',
                 mechanism='complete23-orbit exceptional point')
    else:
        require(F(r['strict_scalar_margin']) > 0,
                'variance sufficient premise fails; no negative matrix conclusion')
        r['mechanism'] = 'whole constant-row variance and generic lower repair'
    r['s'] = 3*q+4
    r['alpha'] = str(F(q*(q+1), 2)+F(3*(q+1), 3*q+5))
    return r


def certificate(q, k):
    p = parameters(q, k)
    N, s, h = p['N'], p['s'], F(1, 3*q+5)
    kappa, t = F(p['kappa']), F(p['t'])
    w = table(q)

    def typ(A):
        return (A & 7).bit_count(), (A >> 3).bit_count()

    def member(A):
        require(type(A) is int and A >= 0 and A.bit_length() <= q+3,
                'original member bitmask outside ground set')
        a, b = typ(A)
        require(a+b <= 2 or a+b == 3 and a >= 2, 'outside original downset')
        require(not (A & 7 == 6 and b == 1 and (A >> 3).bit_length() <= k),
                'deleted triangle supplied as surviving member')

    def weight(A, B):
        a, d = w[tuple(sorted((typ(A), typ(B))))]
        return a+kappa*d-1

    def row(A):
        a, b = typ(A)
        full = F(1) if a == 0 else h if a < 3 else -3*(q+1)*h
        if A & 6:
            removed = F(-k)
        else:
            outside = A >> 3
            hits = 0
            while outside:
                bit = outside & -outside
                hits += int(bit.bit_length() <= k)
                outside -= bit
            base, slope = w[tuple(sorted((typ(A), (2, 1))))]
            removed = -hits+(k-hits)*(base+kappa*slope-1)
        repair = 2 if A == 1 else -1 if A in (3, 5) else 0
        return kappa*full-removed+t*repair

    total = kappa*F(p['alpha'])-2*k*kappa*h+k*(s-k)

    def entry(A, B):
        member(A)
        member(B)
        if A == B == 0:
            L = 1+total
        elif A == 0 or B == 0:
            L = 1-row(A or B)
        else:
            C = F(s-1) if A == B else F(-1) if A & B else weight(A, B)
            L = 1+C+t*EDGES.get(tuple(sorted((A, B))), 0)
        return (L-s*int(A == B))/(N-s)

    return p, entry


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('q', type=int)
    parser.add_argument('k', type=int)
    parser.add_argument('--a', type=int, default=0)
    parser.add_argument('--b', type=int, default=0)
    args = parser.parse_args()
    p, entry = certificate(args.q, args.k)
    print(json.dumps({'parameters': p, 'entry_masks': [args.a, args.b],
                      'M_entry': str(entry(args.a, args.b))}, indent=2))
