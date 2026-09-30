"""Separate full Bernstein audit by six-tammes-1; researcher, no reviewer.

Expand the affine substitution first, then convert the two monomial
axes to Bernstein form. Compare every coefficient with the production
transform, including all five original-Q divisors and the two margins.
CPython >=3.11, standard library only.
"""
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path
import hashlib
import json
import check as production


def require(ok, text):
    if not ok:
        raise ValueError(text)


def polynomial(rows):
    d = {}
    for i, j, a in rows:
        require((i, j) not in d and a != 0, 'audit canonical terms')
        d[i, j] = a
    return d


def linear_combination(items):
    d = defaultdict(int)
    for coefficient, p in items:
        for key, value in p.items():
            d[key] += coefficient*value
    return {key: value for key, value in d.items() if value}


def product(p, q):
    d = defaultdict(int)
    for a, x in p.items():
        for b, y in q.items():
            d[a[0]+b[0], a[1]+b[1]] += x*y
    return {key: value for key, value in d.items() if value}


def c_times(p):
    return {(i+1, j): a for (i, j), a in p.items()}


def reference(p):
    n = max(i for i, j in p)
    m = max(j for i, j in p)
    a, dc = F(1, 2), F(1, 10)
    b, dt = F(5, 11), F(50, 253)
    # First expand p(a+dc*u,b+dt*v) in ordinary powers.
    after_c = [[sum(p.get((i, j), 0)*comb(i, k)*a**(i-k)*dc**k
                     for i in range(k, n+1)) for j in range(m+1)]
               for k in range(n+1)]
    powers = [[sum(after_c[k][j]*comb(j, l)*b**(j-l)*dt**l
                   for j in range(l, m+1)) for l in range(m+1)]
              for k in range(n+1)]
    # Then convert powers to degree-(n,m) Bernstein coefficients.
    converted_c = [[sum(powers[k][l]*F(comb(i, k), comb(n, k))
                        for k in range(i+1)) for l in range(m+1)]
                   for i in range(n+1)]
    return tuple(tuple(sum(converted_c[i][l]*F(comb(j, l), comb(m, l))
                           for l in range(j+1)) for j in range(m+1))
                 for i in range(n+1))


def jobs(certificate):
    points = {}
    out = {}
    for name, obj in certificate['points'].items():
        nums = tuple(polynomial(p) for p in obj['numerators'])
        den = polynomial(obj['denominator'])
        points[name] = nums, den
        out['point_denominator_'+name] = den
    for name, a, b in (('B', 'U', 'X'), ('C', 'U', 'Z'), ('Y', 'B', 'C'),
                        ('N', 'J', 'Y'), ('O', 'Y', 'M')):
        x, dx = points[a]
        y, dy = points[b]
        ordinary_dot = linear_combination([(1, product(u, v)) for u, v in zip(x, y)])
        sx = linear_combination([(1, p) for p in x])
        sy = linear_combination([(1, p) for p in y])
        out['Q_divisor_'+name] = linear_combination([
            (1, product(dx, dy)), (1, ordinary_dot),
            (-1, c_times(ordinary_dot)), (1, c_times(product(sx, sy)))])
    num = polynomial(certificate['NO_inner_product']['numerator'])
    den = polynomial(certificate['NO_inner_product']['denominator'])
    out['NO_denominator'] = den
    out['NO_cosine_excess_over_one_twentieth'] = linear_combination([
        (20, num), (-20, c_times(den)), (-1, den)])
    out['NO_distinctness_over_one_thousandth'] = linear_combination([
        (999, den), (-1000, num)])
    return out


def counts():
    # Independent raw corner-budget enumeration, not delta-first generation.
    raw = []
    kept = []
    for a in range(14):
        for b in range(14-a):
            for t5 in range(5):
                if a+2*(13-a-b)+t5 != 24:
                    continue
                delta = 4-t5
                raw.append((delta, a, b))
                if delta > 2 or a+b < delta+1:
                    continue
                if (delta, a, b) in ((0, 0, 3), (1, 1, 2)):
                    continue
                kept.append((delta, a, b))
    actual = sorted((r['five_deficit'], r['one_T_fours'], r['zero_T_fours'])
                    for r in production.bookkeeping()['r1_necessary_profiles_on_open_half_three_fifths'])
    require(sorted(kept) == actual, 'full-entry raw count cover')
    # Build the second-T choices independently from their consumed opposite
    # triangle incidences. Two separate uses of D cannot be the same face.
    labelled = []
    for zero in ('B', 'C', 'D'):
        for choice in range(4):
            xr, sz = bool(choice & 1), bool(choice & 2)
            consumed = ([] if xr else ['B', 'D'])+([] if sz else ['D', 'C'])
            if zero in consumed or consumed.count('D') > 1:
                continue
            labelled.append((zero, xr, sz))
    expected = production.bookkeeping()['delta2_a2_b1_second_triangle_prefixes']
    require(sorted(labelled) == sorted(expected['labelled']), 'full-entry second-T prefix cover')
    return {'raw_corner_budget_rows': len(raw), 'seven_rows': sorted(kept),
            'five_labelled_second_triangle_prefixes': sorted(labelled)}


def main():
    certificate = json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    tables = []
    for name, p in sorted(jobs(certificate).items()):
        independent = reference(p)
        actual = production.bernstein(p)
        require(independent == actual, 'all-entry Bernstein comparison: '+name)
        entries = [x for row in independent for x in row]
        require(min(entries) > 0, 'independent strict positive table: '+name)
        digest = hashlib.sha256(json.dumps([[str(v) for v in row] for row in independent],
                                          separators=(',', ':')).encode()).hexdigest()
        tables.append({'name': name, 'coefficients': len(entries), 'sha256': digest})
    require(len(tables) == 21, 'all 21 sign tables audited')
    print(json.dumps({'agent': 'six-tammes-1', 'role': 'researcher',
                      'status': 'SEPARATE_ALGORITHM_SAME_AUTHOR_AUDIT',
                      'tables': tables, 'coefficients_compared': sum(x['coefficients'] for x in tables),
                      'bookkeeping': counts(),
                      'scope': 'Entrywise sign-table and count audit; geometry and independent mathematical review remain outside this audit.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
