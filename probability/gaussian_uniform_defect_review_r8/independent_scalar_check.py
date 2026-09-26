"""Independent exact scalar audit: Euler powers, polygons, Simpson error.

Does not import the reviewed checker or read its certificate. No floating
point, Gamma Taylor series, Machin identity, or numerical root finder.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import isqrt
import json

BITS, SQUARES, PANELS = 128, 48, 64
SCALE = 1 << BITS


def require(condition, label):
    if not condition:
        raise ValueError(label)


def ceil_fraction(x):
    return -((-x.numerator)//x.denominator)


def sqrt_interval(lo, hi=None):
    lo, hi = Q(lo), Q(lo if hi is None else hi)
    require(0 <= lo <= hi, 'sqrt domain')
    a = isqrt(lo.numerator*SCALE*SCALE//lo.denominator)
    b = isqrt(hi.numerator*SCALE*SCALE//hi.denominator) + 1
    result = Q(a, SCALE), Q(b, SCALE)
    require(result[0]**2 <= lo <= hi <= result[1]**2, 'sqrt coverage')
    return result


def polygon_pi():
    sine = cosine = sqrt_interval(Q(1, 2))
    sides = 4
    while sides < 2048:
        c = sqrt_interval((1+cosine[0])/2, (1+cosine[1])/2)
        sine = sine[0]/(2*c[1]), sine[1]/(2*c[0])
        cosine = c
        sides *= 2
    bracket = sides*sine[0], sides*sine[1]/cosine[0]
    require(3 < bracket[0] < bracket[1] < 4, 'polygon pi range')
    return bracket


@lru_cache(None)
def exp_minus(x):
    x = Q(x)
    require(0 <= x <= 2, 'Euler exponential domain')
    if not x:
        return Q(1), Q(1)
    n = 1 << SQUARES
    a = (SCALE*(1-x/n)).__floor__()
    b = ceil_fraction(SCALE/(1+x/n))
    for _ in range(SQUARES):
        a = a*a//SCALE
        b = (b*b+SCALE-1)//SCALE
    require(0 < a <= b <= SCALE, 'Euler enclosure order')
    return Q(a, SCALE), Q(b, SCALE)


def gamma_cdf(x, pi):
    x = Q(x)
    require(0 <= x <= Q(6, 5), 'CDF range')
    if not x:
        return Q(0), Q(0)
    total = [Q(0), Q(0)]
    for j in range(PANELS+1):
        u = Q(j, PANELS)
        multiplier = 1 if j in (0, PANELS) else (4 if j % 2 else 2)
        a, b = exp_minus(x*u*u)
        total[0] += multiplier*u*u*a
        total[1] += multiplier*u*u*b
    error = Q(481, 180*PANELS**4)
    integral = max(Q(0), total[0]/(3*PANELS)-error), total[1]/(3*PANELS)+error
    sx, sp = sqrt_interval(x), sqrt_interval(*pi)
    result = 4*x*sx[0]*integral[0]/sp[1], 4*x*sx[1]*integral[1]/sp[0]
    require(0 <= result[0] <= result[1] <= 1, 'CDF enclosure order')
    return result


def difference(t, q, w, pi):
    exponential = exp_minus(t)
    cdf = gamma_cdf(t+q, pi)
    return 1-exponential[1]-w*cdf[1], 1-exponential[0]-w*cdf[0]


def rounded(interval, digits=9):
    factor = 10**digits
    return [str(Q((interval[0]*factor).__floor__(), factor)),
            str(Q(ceil_fraction(interval[1]*factor), factor))]


def derivative_polynomial_audit():
    # Derivatives of p(v)*exp(-x*v^2) send p to p'-2*x*v*p.
    p = {(0, 2): Q(1)}
    for _ in range(4):
        out = {}
        for (xpower, vpower), coefficient in p.items():
            if vpower:
                key = (xpower, vpower-1)
                out[key] = out.get(key, 0)+vpower*coefficient
            key = (xpower+1, vpower+1)
            out[key] = out.get(key, 0)-2*coefficient
        p = {key: value for key, value in out.items() if value}
    require(p == {(1, 0): -24, (2, 2): 156, (3, 4): -112, (4, 6): 16},
            'fourth derivative polynomial')
    x = Q(6, 5)
    bound = 24*x+156*x*x+112*x**3+16*x**4
    require(bound < 481, 'Simpson derivative bound')
    return str(bound)


def run():
    q, w, c = Q(17, 50), Q(57, 50), Q(7, 50)
    left, right = Q(17, 20), Q(43, 50)
    pi = polygon_pi()
    e = exp_minus(2*q)
    derivative_left = pi[0]-4*w*w*e[1]*(left+q)
    derivative_right = 4*w*w*e[0]*(right+q)-pi[1]
    require(derivative_left > 0 and derivative_right > 0, 'coarse root bracket')
    fq = gamma_cdf(q, pi)
    d0 = -w*fq[1], -w*fq[0]
    require(d0[0] > -c, 'negative-side envelope')
    at_left = difference(left, q, w, pi)
    require(at_left[1] < -Q(1, 2500), 'fixed-point upper envelope')
    # d'(t*)=0, t* in [left,right], and |d''|<4 on that interval.
    curvature = 1+Q(4, 3)*w*(Q(6, 5)+Q(1, 2))
    require(curvature < 4, 'curvature bound')
    maximum_upper = at_left[1]+2*(right-left)**2
    require(maximum_upper < -Q(1, 5000), 'global critical upper bound')
    require(w-1 == c, 'infinite endpoint')
    false_shift = difference(left, Q(1, 3), w, pi)
    require(false_shift[0] > 0, 'nearby false envelope witness')
    require(exp_minus(0) == (1, 1) and gamma_cdf(0, pi) == (0, 0), 'endpoint controls')
    return {
        'status': 'INDEPENDENT_SCALAR_ENVELOPE_PASS',
        'method': 'Euler power bounds; inscribed/circumscribed polygons; composite Simpson with explicit fourth derivative bound',
        'dyadic_bits': BITS, 'Euler_squarings': SQUARES, 'Simpson_panels': PANELS,
        'polygon_sides': 2048, 'pi_enclosure': rounded(pi),
        'critical_bracket': [str(left), str(right)],
        'derivative_sign_margins': [rounded((a, a)) for a in (derivative_left, derivative_right)],
        'd_zero_enclosure': rounded(d0), 'd_at_17_over_20': rounded(at_left),
        'global_critical_upper_bound': '-1/5000', 'absolute_error_bound': str(c),
        'fourth_derivative_bound': derivative_polynomial_audit(),
        'second_derivative_majorant': str(curvature),
        'false_shift_1_over_3_at_17_over_20': rounded(false_shift),
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
