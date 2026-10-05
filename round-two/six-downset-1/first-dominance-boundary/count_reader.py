"""Exact root/endpoint certificate guards; no large original allocation."""
from fractions import Fraction as F
import counts


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(text):
    require(type(text) is str and len(text) <= 8192, 'bounded rational certificate')
    value = F(text)
    require(str(value) == text, 'canonical root certificate rational')
    return value


def validate(record, n, values):
    require(record['n'] == n and record['counts'] == list(values)
            and record['large_original_constructed'] is False,
            'root certificate original-count scope')
    q = 2**(n-1)
    seed = counts.scalars(q, list(values))
    require(q >= 200*seed['h'] and record['N'] == seed['N'],
            'root certificate theorem domain')
    lo, hi = map(rational, record['gamma_interval'])
    require(0 < lo < hi < 6*seed['h']
            and hi-lo <= F(6*seed['h'], 2**56), 'whole gamma isolation interval')
    signs = [counts.shift(q, values, theta)['sigma'] for theta in (lo, hi)]
    require(signs[0] > 0 > signs[1]
            and signs == list(map(rational, record['gamma_endpoint_sigma'])),
            'both complete gamma endpoint signs')
    tlo, thi = 2*seed['s']-hi, 2*seed['s']-lo
    require(list(map(rational, record['top_FIRST_interval'])) == [tlo, thi]
            and 2*q < tlo < thi < 2*seed['s'], 'whole original FIRST top interval')
    dlo = counts.positive_bounds(seed, tlo)[0]
    dhi = counts.positive_bounds(seed, thi)[1]
    ulo, uhi = counts.positive_bounds(seed, F(seed['N']))
    require(list(map(rational, record['delta_FIRST_interval'])) == [dlo, dhi]
            and list(map(rational, record['delta_upper_interval'])) == [ulo, uhi]
            and F(q,200) < dlo < dhi < ulo < uhi,
            'complete radical FIRST-upper ordering')
    require(list(map(rational, record['exact_cap_interval'])) ==
            [6*seed['L']+lo, 6*seed['L']+hi], 'whole cap/gamma identity')
    baseline = counts.shift(q, values, F(0))
    require(record['baseline'] == {k:str(baseline[k]) for k in ('w','z','g','sigma')},
            'whole theta-zero Schur baseline')
    require(record['root_bisections'] == 56 and record['radical_bits'] == 72
            and record['positive_order_verified'] is True,
            'root precision and completed-order scope')
    return True
