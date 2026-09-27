#!/usr/bin/env python3
"""Exact controls for positive moment reconstruction; see PROOF.md.

CPython >=3.11, standard library only. No numerical integration, floating
signs, external solver or Python assert is used for a proof obligation.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
import json
from math import comb, factorial, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def trim(a):
    need(all(type(x) in (int, F) for x in a), 'exact rational coefficients required')
    a = list(map(F, a))
    while len(a) > 1 and not a[-1]:
        a.pop()
    return a


def add(a, b):
    return trim([(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([x*c for x in a])


def mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return trim(c)


def affine(a, offset, slope):
    answer = [F(0)]
    power = [F(1)]
    for x in a:
        answer = add(answer, scale(power, x))
        power = mul(power, [offset, slope])
    return answer


def val(a, t):
    answer = F(0)
    for x in reversed(a):
        answer = answer*t+x
    return answer


def integral(a):
    """Integral on [0,1]."""
    return sum((x/F(i+1) for i, x in enumerate(a)), F(0))


def sphere_integral(a):
    """Integral on [-1,1] with measure dt/2."""
    return sum((a[i]/F(i+1) for i in range(0, len(a), 2)), F(0))


@lru_cache(None)
def legendre(j):
    need(type(j) is int and j >= 0, 'Legendre degree')
    if j == 0:
        return (F(1),)
    if j == 1:
        return (F(0), F(1))
    return tuple(scale(add(scale([F(0)]+list(legendre(j-1)), 2*j-1),
                           scale(legendre(j-2), -(j-1))), F(1, j)))


def shifted(j):
    return [F((-1)**(j+r)*comb(j,r)*comb(j+r,r)) for r in range(j+1)]


@lru_cache(None)
def kernel(p):
    need(type(p) is int and p >= 2, 'integer kernel parameter at least two')
    t0, t1 = [F(1)], [F(0), F(1)]
    for _ in range(2, p+1):
        t0, t1 = t1, add(scale([F(0)]+t1, 2), scale(t0, -1))
    numerator = add([F(1)], scale(t1, -1))
    quotient, previous = [], F(0)
    for a in numerator[:-1]:
        previous += a
        quotient.append(previous)
    need(mul(quotient, [F(1), F(-1)]) == numerator, 'Chebyshev division')
    need(val(quotient, F(1)) == p*p, 'endpoint derivative')
    K = mul(quotient, quotient)
    I = sphere_integral(K)
    need(I >= p*p, 'endpoint evaluation norm')
    weights = tuple(F(2*j+1)*sphere_integral(mul(K, legendre(j)))/I
                    for j in range(2*p-1))
    need(weights[0] == 1, 'normalization')
    expanded = [F(0)]
    for j, weight in enumerate(weights):
        expanded = add(expanded, scale(legendre(j), weight))
    need(scale(K, 1/I) == expanded, 'Legendre kernel expansion')
    chord = affine(K, F(1), F(-2))
    chord_integral = sum((v/F(2*r+3)*2 for r, v in enumerate(chord)), F(0))
    cost = min(F(6, p), F(22, 7)*chord_integral/I)
    need(0 < cost <= F(6, p), 'positive angular cost')
    return tuple(K), I, weights, cost


def reconstruct(p, moments):
    _, _, weights, _ = kernel(p)
    need(len(moments) == len(weights), 'wrong moment count')
    need(all(type(x) in (int, F) for x in moments), 'exact rational moments required')
    out = [F(0)]
    for j, w in enumerate(weights):
        coeff = shifted(j)
        h = sum((c*moments[r] for r, c in enumerate(coeff)), F(0))
        out = add(out, scale(coeff, w*h))
    return out


def propagate(p, radii):
    _, _, weights, _ = kernel(p)
    need(len(radii) == len(weights)
         and all(type(x) in (int, F) and x >= 0 for x in radii),
         'invalid moment radii')
    return sum((abs(w)*sum((abs(c)*radii[r] for r, c in enumerate(shifted(j))), F(0))
                for j, w in enumerate(weights)), F(0))


def moment_errors(p, q, epsilon):
    need(type(q) is int and q >= 2, 'cubature half degree')
    need(type(epsilon) in (F, int) and epsilon >= 0, 'exact radius ratio')
    return [(F((r+2)*epsilon, 2)**q)/(4*(r+2)**2*factorial(q))
            for r in range(2*p-1)]


def width(p, q, epsilon):
    return propagate(p, moment_errors(p, q, epsilon))


def safe_degree(p, epsilon, bits):
    kernel(p)
    need(type(bits) is int and bits >= 0, 'nonnegative integer error bits')
    need(type(epsilon) in (F, int) and epsilon >= 0, 'exact radius ratio')
    M = 2*p-2
    return max(2, (3*(M+2)*epsilon).__ceil__(), bits+3*M+2*M.bit_length())


def select_degree(p, epsilon, bits):
    lo = max(2, (p*epsilon).__ceil__())
    start = lo
    hi = safe_degree(p, epsilon, bits)
    goal = F(1, 1 << bits)
    need(width(p, hi, epsilon) <= goal, 'safe schedule failed')
    while lo < hi:
        mid = (lo+hi)//2
        if width(p, mid, epsilon) <= goal:
            hi = mid
        else:
            lo = mid+1
    need(width(p, lo, epsilon) <= goal, 'selected schedule failed')
    need(lo == start or width(p, lo-1, epsilon) > goal, 'predecessor check')
    return lo


def bernstein(a, left=F(0), right=F(1)):
    need(type(left) in (int,F) and type(right) in (int,F)
         and 0 <= left < right <= 1, 'invalid interval')
    a = affine(a, left, right-left)
    n = len(a)-1
    return [sum((a[j]*F(comb(k,j), comb(n,j)) for j in range(k+1)), F(0))
            for k in range(n+1)]


def certify_lower(a, left, right, bound, max_depth=12):
    """Sound sufficient test; failure is inconclusive, never a counterexample."""
    need(type(max_depth) is int and max_depth >= 0, 'subdivision depth')
    need(type(bound) in (int,F), 'exact lower bound')
    pending = [(bernstein(a, left, right), 0)]
    leaves = 0
    while pending:
        row, depth = pending.pop()
        if min(row) >= bound:
            leaves += 1
            continue
        if depth == max_depth or max(row) < bound:
            return None
        rows = [row]
        while len(rows[-1]) > 1:
            rows.append([(x+y)/2 for x, y in zip(rows[-1], rows[-1][1:])])
        pending.append(([r[0] for r in rows], depth+1))
        pending.append(([r[-1] for r in reversed(rows)], depth+1))
    return leaves


def azimuth_coefficients(K):
    """Independent bivariate expansion in t=omega_3,w=nu_3.

    Use E cos(phi)^(2r)=binom(2r,r)/4^r, and expand
    (t w+sqrt(1-t^2)sqrt(1-w^2)cos(phi))^n directly.
    """
    out = {}
    for n, kn in enumerate(K):
        for r in range(n//2+1):
            base = kn*comb(n, 2*r)*F(comb(2*r, r), 4**r)
            for i in range(r+1):
                for j in range(r+1):
                    key = (n-2*r+2*i, n-2*r+2*j)
                    out[key] = out.get(key, F(0))+base*(-1)**(i+j)*comb(r,i)*comb(r,j)
    return {k: v for k, v in out.items() if v}


def exact_controls():
    azimuth_entries = 0
    for p in range(2, 7):
        K, I, weights, _ = kernel(p)
        direct = azimuth_coefficients(K)
        spectral = {}
        for j, w in enumerate(weights):
            for a, x in enumerate(legendre(j)):
                for b, y in enumerate(legendre(j)):
                    spectral[a,b] = spectral.get((a,b), F(0))+I*w*x*y
        spectral = {k: v for k, v in spectral.items() if v}
        need(direct == spectral, 'azimuth/addition normalization mismatch')
        azimuth_entries += len(direct)
        for j in range(2*p-1):
            need(affine(legendre(j), -1, 2) == shifted(j), 'shifted coefficients')
            need(sum(map(abs, shifted(j))) == val(legendre(j), F(3)), 'absolute sum')
        constant = [F(1, r+1) for r in range(2*p-1)]
        need(reconstruct(p, constant) == [F(1)], 'constant preservation')
        moments = [F(1, r+2)-F(1, r+3) for r in range(2*p-1)]
        need(certify_lower(reconstruct(p, moments), F(0), F(1), F(0)) is not None,
             'positive average failed a positive polynomial control')
    ratios = 0
    for p in range(2, 7):
        for epsilon in [F(1,64), F(1,2), F(3)]:
            for q in range(2, 12):
                M = 2*p-2
                v = width(p,q,epsilon)
                coarse = F((M+1)**2*6**M, 16*factorial(q))*(p*epsilon)**q
                need(v <= coarse, 'coarse error budget')
                need(width(p,q+1,epsilon) <= p*epsilon*v/(q+1), 'degree ratio')
                ratios += 1
    need(F(4,3)+2*F(24,23)**2+2 < 6, 'kernel moment constant')
    need(certify_lower([0,1,-1], F(1,4), F(3,4), F(3,16)) is not None,
         'sharp interval lower bound')
    need(certify_lower([F(13,50),-1,1], F(0), F(1), F(1,100)) == 2,
         'subdivision coverage')
    need(certify_lower([F(-1,2),1,-1], F(1,4), F(3,4), F(0)) is None,
         'damaged polynomial accepted')
    rejected = 1
    for call in [lambda:kernel(1), lambda:kernel(F(3)),
                 lambda:width(3,1,F(1)), lambda:width(3,2,F(-1)),
                 lambda:reconstruct(3,[F(1)]),
                 lambda:reconstruct(3,[0.5]*5),
                 lambda:propagate(3,[F(-1)]*5),
                 lambda:propagate(3,[0.0]*5),
                 lambda:bernstein([0,1],F(1),F(0))]:
        try:
            call()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed input accepted')
    return {'azimuth_entries':azimuth_entries,'remainder_comparisons':ratios,
            'rejected_damaged_or_malformed_inputs':rejected}


def exp_negative(x, bits=220):
    """Positive exp(x) series, geometric tail, then outward reciprocal."""
    need(x >= 0, 'negative exponential argument')
    if not x:
        return F(1), F(1)
    total = term = F(1)
    n = 0
    while True:
        n += 1
        term *= x/n
        total += term
        ratio = x/(n+2)
        if ratio < 1:
            tail = term*x/(n+1)/(1-ratio)
            lo, hi = 1/(total+tail), 1/total
            if hi-lo <= F(1,1 << bits):
                return lo, hi


def sqrt_bounds(n, bits=180):
    k = isqrt(n << (2*bits))
    return F(k,1 << bits), F(k+1,1 << bits)


def scaled_interval(interval, c):
    a,b = interval
    return (a*c,b*c) if c >= 0 else (b*c,a*c)


def interval_sum(terms):
    terms = list(terms)
    return sum((a for a,b in terms),F(0)), sum((b for a,b in terms),F(0))


def gauss_moment(m, a, t, q=None):
    """Two equal atoms +/-a -> +/-ta, embedded in R3; normalize by d."""
    d = 2*a*a*(1-t*t)
    need(d > 0, 'positive control loss')
    numerator = []
    for k in range(m+1):
        z = 2*a*a*k*(m-k)/m
        mass = F(comb(m,k),2**m)
        if q is None:
            ylo,yhi = exp_negative(t*t*z)
            xlo,xhi = exp_negative(z)
            numerator.append(((ylo-xhi)*mass,(yhi-xlo)*mass))
        else:
            v = sum((((-t*t*z)**j-(-z)**j)/factorial(j) for j in range(q+1)),F(0))
            numerator.append((v*mass,v*mass))
    lo,hi = interval_sum(numerator)
    rootlo,roothi = sqrt_bounds(m)
    factors = [1/(m*m*(m-1)*d*rootlo),1/(m*m*(m-1)*d*roothi)]
    products = [v*f for v in (lo,hi) for f in factors]
    return min(products),max(products)


def compact(interval, bits=64):
    lo,hi = interval
    S = 1 << bits
    return [str(F((lo*S).__floor__(),S)), str(F((hi*S).__ceil__(),S))]


def gaussian_controls():
    answer = []
    p, q, a = 4, 8, F(1,4)
    for t in [F(0),F(1,2),F((1 << 30)-1,1 << 30),F((1 << 60)-1,1 << 60)]:
        intervals = [gauss_moment(m,a,t) for m in range(2,2*p+1)]
        approximations = [gauss_moment(m,a,t,q) for m in range(2,2*p+1)]
        errors = moment_errors(p,q,a*a)
        rejected_zero_remainder = False
        for (lo,hi),(blo,bhi),err in zip(intervals,approximations,errors):
            # q even: the exact value lies above its Taylor part.
            need(lo >= blo and hi <= bhi+err, 'paired Taylor interval')
            if lo > bhi:
                rejected_zero_remainder = True
        need(rejected_zero_remainder, 'omitted remainder escaped detection')
        mids = [(lo+hi)/2 for lo,hi in intervals]
        radii = [(hi-lo)/2 for lo,hi in intervals]
        polynomial = reconstruct(p,mids)
        error = propagate(p,radii)
        need(certify_lower(polynomial,F(0),F(1),error) is not None,
             'Gaussian positive reconstruction control')
        points = []
        for u in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
            # Definition-level sum, independent of polynomial expansion.
            direct = interval_sum(scaled_interval(interval_sum(
                scaled_interval(intervals[r],c) for r,c in enumerate(shifted(j))),
                w*val(shifted(j),u))
                for j,w in enumerate(kernel(p)[2]))
            v = val(polynomial,u)
            need(v-error <= direct[0] <= direct[1] <= v+error,
                 'moment interval propagation')
            points.append({'u':str(u),'normalized_J':compact(direct)})
        answer.append({'t':str(t),'loss':str(2*a*a*(1-t*t)),
                       'zero_remainder_rejected':rejected_zero_remainder,
                       'normalized_moment_radius_upper':compact((F(0),error))[1],
                       'normalized_J_points':points})
    return {'kernel_parameter':p,'moment_degree':2*p-2,'Taylor_degree':q,
            'exponential_bits':220,'radical_bits':180,'controls':answer,
            'scope':'Known two-atom positive class; normalization and loss-retention controls, not a new Gaussian sign.'}


def calculate():
    controls = exact_controls()
    kernels = []
    for p in [2,3,4,8,16]:
        K,I,weights,cost = kernel(p)
        kernels.append({'p':p,'degree':2*p-2,'I':str(I),'angular_cost_upper':str(cost),
                        'operator_sha256':sha256('|'.join(map(str,weights)).encode()).hexdigest()})
    schedules = []
    for p,epsilon,bits in [(4,F(1,64),12),(8,F(1,2),10),(16,F(1,2),10),
                           (8,F(4),10),(16,F(9),10)]:
        q = select_degree(p,epsilon,bits)
        schedules.append({'p':p,'moment_degree':2*p-2,'epsilon':str(epsilon),
                           'error_bits':bits,'selected_q':q,
                           'safe_q':safe_degree(p,epsilon,bits),
                           'atom_budget':2*comb(2*q+3,3)-1,
                           'relative_reconstruction_error_upper':compact((0,width(p,q,epsilon)))[1]})
    return {'status':'JACKSON_GAUSSIAN_CERTIFICATION_PASS','controls':controls,
            'kernels':kernels,'cubature_schedules':schedules,
            'gaussian_controls':gaussian_controls(),
            'scope':'Exact finite controls for uniform reconstruction. No universal positive margin, full Gaussian comparison, or KP consequence.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=HERE/'EXPECTED.json')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    result = calculate()
    encoded = (json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if args.write_expected:
        args.expected.write_bytes(encoded)
    else:
        need(json.loads(args.expected.read_text()) == result, 'expected record mismatch')
    print(result['status'])
    print('record_sha256',sha256(encoded).hexdigest())


if __name__ == '__main__':
    main()
