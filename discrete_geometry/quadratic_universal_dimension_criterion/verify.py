#!/usr/bin/env python3
"""Exact algebra checks; not a proof of the external projection theorem."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


# Small formal polynomial ring: nine coefficient variables and x,y,z.
N = 12
ZERO = (0,) * N


def clean(p):
    return {m: c for m, c in p.items() if c}


def add(p, q):
    out = dict(p)
    for m, c in q.items():
        out[m] = out.get(m, 0) + c
    return clean(out)


def scale(p, c):
    return clean({m: c * v for m, v in p.items()})


def mul(p, q):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            key = tuple(x + y for x, y in zip(m, n))
            out[key] = out.get(key, 0) + c * d
    return clean(out)


def diff(p, v):
    out = {}
    for m, c in p.items():
        if m[v]:
            n = list(m)
            n[v] -= 1
            out[tuple(n)] = c * m[v]
    return out


def variable(k):
    m = list(ZERO)
    m[k] = 1
    return {tuple(m): 1}


def coefficient(p, v, power):
    out = {}
    for m, c in p.items():
        if m[v] == power:
            n = list(m)
            n[v] = 0
            out[tuple(n)] = c
    return out


def symbolic_jacobians():
    v = [variable(k) for k in range(N)]
    a, b, c, d, e, f, g, h, i, x, y, z = v
    terms = [mul(a, mul(x, x)), mul(b, mul(y, y)), mul(c, mul(z, z)),
             mul(d, mul(x, y)), mul(e, mul(x, z)), mul(f, mul(y, z)),
             mul(g, x), mul(h, y), mul(i, z)]
    q = {}
    for t in terms:
        q = add(q, t)

    def minus(p, r):
        return add(p, scale(r, -1))

    de2af = minus(mul(d, e), scale(mul(a, f), 2))
    df2be = minus(mul(d, f), scale(mul(b, e), 2))
    dc2ef = minus(scale(mul(c, d), 2), mul(e, f))
    formulas = [
        add(add(mul(df2be, y), mul(dc2ef, z)), minus(mul(d, i), mul(e, h))),
        add(add(mul(de2af, x), mul(dc2ef, z)), minus(mul(d, i), mul(f, g))),
        add(add(mul(de2af, x), scale(mul(df2be, y), -1)),
            minus(mul(e, h), mul(f, g))),
    ]
    monomials = []
    for pin in range(3):
        u, w = [9 + k for k in range(3) if k != pin]
        l = coefficient(q, 9 + pin, 1)
        r = coefficient(q, 9 + pin, 0)
        direct = minus(mul(diff(l, u), diff(r, w)),
                       mul(diff(l, w), diff(r, u)))
        require(direct == formulas[pin], 'formal Jacobian mismatch')
        monomials.append(len(direct))
    return monomials


def params(coeff):
    require(len(coeff) == 9, 'expected nine rational coefficients')
    require(all(isinstance(x, (int, F)) and not isinstance(x, bool)
                for x in coeff), 'exact rational coefficients required')
    return tuple(map(F, coeff))


def matrix(coeff):
    a, b, c, d, e, f, g, h, i = params(coeff)
    return [[2*a, d, e], [d, 2*b, f], [e, f, 2*c]], [g, h, i]


def rank(rows):
    m = [list(map(F, row)) for row in rows]
    r = 0
    for j in range(len(m[0])):
        pivot = next((k for k in range(r, len(m)) if m[k][j]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        z = m[r][j]
        m[r] = [x / z for x in m[r]]
        for k in range(r + 1, len(m)):
            z = m[k][j]
            m[k] = [x - z*y for x, y in zip(m[k], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def jacobians(coeff):
    a, b, c, d, e, f, g, h, i = params(coeff)
    return ((d*f-2*b*e, 2*c*d-e*f, d*i-e*h),
            (d*e-2*a*f, 2*c*d-e*f, d*i-f*g),
            (d*e-2*a*f, 2*b*e-d*f, e*h-f*g))


def line_certificate(coeff, axis):
    """Return None or fixed coordinates of an exactly constant line."""
    m, l = matrix(coeff)
    require(axis in (0, 1, 2), 'invalid axis')
    if m[axis][axis]:
        return None
    other = [k for k in range(3) if k != axis]
    pivot = next((k for k in other if m[axis][k]), None)
    if pivot is None and l[axis]:
        return None
    point = [F(0)] * 3
    if pivot is not None:
        point[pivot] = -l[axis] / m[axis][pivot]
    return tuple(point)


def line_is_constant(coeff, axis, point):
    m, l = matrix(coeff)
    return m[axis][axis] == 0 and l[axis] + sum(
        m[axis][k]*point[k] for k in range(3) if k != axis) == 0


def evaluate(coeff, p):
    a, b, c, d, e, f, g, h, i = params(coeff)
    x, y, z = p
    return a*x*x+b*y*y+c*z*z+d*x*y+e*x*z+f*y*z+g*x+h*y+i*z


def grid_check():
    counts = dict(coefficient_vectors=0, all_variables=0,
                  all_variable_zero_jacobians=0, coordinate_condition=0,
                  both_conditions=0, constant_line_certificates=0,
                  direct_line_evaluations=0)
    for coeff in product((-1, 0, 1), repeat=9):
        counts['coefficient_vectors'] += 1
        m, l = matrix(coeff)
        all_variables = all(any(m[k]) or l[k] for k in range(3))
        zero_j = not any(any(row) for row in jacobians(coeff))
        if all_variables:
            counts['all_variables'] += 1
            # Independent matrix formulation of the additive alternative.
            no_mixed_terms = all(m[k][t] == 0 for k in range(3)
                                 for t in range(3) if k != t)
            matrix_additive = no_mixed_terms or (
                rank(m) == 1 and rank([row + [v] for row, v in zip(m, l)]) == 1)
            require(zero_j == matrix_additive, 'rank alternative disagrees')
            counts['all_variable_zero_jacobians'] += int(zero_j)
        condition_l = True
        for axis in range(3):
            point = line_certificate(coeff, axis)
            if point is None:
                continue
            condition_l = False
            require(line_is_constant(coeff, axis, point), 'invalid constant line')
            counts['constant_line_certificates'] += 1
            values = []
            for t in (-2, -1, 0, 1, 2):
                p = list(point)
                p[axis] = F(t)
                values.append(evaluate(coeff, p))
            require(len(set(values)) == 1, 'direct restriction is not constant')
            counts['direct_line_evaluations'] += len(values)
        counts['coordinate_condition'] += int(condition_l)
        counts['both_conditions'] += int(condition_l and not zero_j)
    return counts


def digit_check():
    digits = set(range(9))
    require({x+y+z for x in digits for y in digits for z in digits}
            == set(range(25)), 'digit sum not exact')
    require(9**3 == 27**2 and 25 < 27, 'dimension integer inequalities fail')
    # Independent level-two Minkowski-sum equality, entry by entry.
    prefixes = {27*x+y for x in digits for y in digits}
    pairs = {x+y for x in prefixes for y in prefixes}
    triples = {x+y for x in pairs for y in prefixes}
    expected = {27*x+y for x in range(25) for y in range(25)}
    require(triples == expected, 'level-two no-carry identity fails')
    return dict(base=27, input_digits=9, triple_sum_digits=25,
                level_two_input_points=len(prefixes),
                level_two_sum_points=len(triples),
                input_dimension='2/3', image_dimension_upper='log(25)/log(27)')


def controls():
    tests = [
        ('x(y+z)', (0,0,0,1,1,0,0,0,0), False, True),
        ('sum of squares', (1,1,1,0,0,0,0,0,0), True, False),
        ('square of sum', (1,1,1,2,2,2,0,0,0), True, False),
        ('squares plus xy', (1,1,1,1,0,0,0,0,0), True, True),
        ('x2+y2+xy+z', (1,1,0,1,0,0,0,0,1), True, True),
        ('constant', (0,)*9, False, False),
        ('shifted rational collapse', (0,1,1,F(2,3),0,0,F(5,7),0,0),
         False, True),
    ]
    out = []
    for name, c, l, r in tests:
        got_l = all(line_certificate(c, k) is None for k in range(3))
        got_r = any(any(row) for row in jacobians(c))
        require((got_l, got_r) == (l, r), 'fixture mismatch: '+name)
        out.append(dict(name=name, line_condition=l, rank_condition=r))
    rejected = 0
    for bad in [(0,)*8, (0,)*8+(0.0,), (0,)*8+(True,)]:
        try:
            params(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed coefficient accepted')
    c = tests[-1][1]
    p = list(line_certificate(c, 0))
    p[1] += 1
    require(not line_is_constant(c, 0, p), 'mutated line accepted')
    rejected += 1
    try:
        line_certificate((0,)*9, 3)
    except ValueError:
        rejected += 1
    else:
        raise ValueError('invalid axis accepted')
    return out, rejected


def main():
    fixtures, rejected = controls()
    payload = dict(status='VERIFIED',
                   formal_jacobian_monomials=symbolic_jacobians(),
                   algebra_grid=grid_check(), cantor=digit_check(),
                   fixtures=fixtures, rejected_controls=rejected,
                   trust_boundary='Written proof plus Frostman and Ren-Wang; no numerical dimension inference')
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    out = dict(payload, evidence_sha256=digest)
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        require(out == json.loads(expected.read_text()), 'expected output mismatch')
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
