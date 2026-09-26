#!/usr/bin/env python3
"""Exact controls for the written selector-motion proof. Standard library only.

This checks finite identities, not the universal analytic inference or an
external theorem. No source from another research packet is imported.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Poly:
    """Small sparse rational polynomials; a monomial lists its variable names."""

    def __init__(self, value=0):
        if isinstance(value, Poly):
            self.terms = dict(value.terms)
        elif isinstance(value, dict):
            self.terms = {k: F(v) for k, v in value.items() if v}
        else:
            self.terms = {(): F(value)} if value else {}

    def __add__(self, other):
        terms = dict(self.terms)
        for k, v in Poly(other).terms.items():
            terms[k] = terms.get(k, 0) + v
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + -Poly(other)

    def __rsub__(self, other):
        return Poly(other) + -self

    def __mul__(self, other):
        terms = {}
        for k, v in self.terms.items():
            for l, w in Poly(other).terms.items():
                m = tuple(sorted(k + l))
                terms[m] = terms.get(m, 0) + v * w
        return Poly(terms)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'invalid power')
        answer = Poly(1)
        for _ in range(exponent):
            answer = answer * self
        return answer

    def __eq__(self, other):
        return self.terms == Poly(other).terms

    def diff(self, name):
        terms = {}
        for k, v in self.terms.items():
            power = k.count(name)
            if power:
                remaining = list(k)
                remaining.remove(name)
                terms[tuple(remaining)] = power * v
        return Poly(terms)

    def sub(self, values):
        total = Poly()
        for k, v in self.terms.items():
            term = Poly(v)
            for name in k:
                term *= values.get(name, variable(name))
            total += term
        return total


def variable(name):
    return Poly({(name,): 1})


def equal(left, right, message):
    require(left == right, message)


EDGES = tuple(combinations(range(4), 2))
H = tuple(variable('h' + str(i)) for i in range(4))
LAM = tuple(variable('lambda' + str(i)) for i in range(4))
C = variable('c')
CHI = variable('chi')


def tournament(mask):
    return tuple((a, b) if mask & (1 << e) else (b, a)
                 for e, (a, b) in enumerate(EDGES))


def gram(a, b, exceptional):
    kind_a, i = a
    kind_b, j = b
    base = H[i] - C if i == j else -C
    if kind_a == kind_b == 'v':
        return base
    if kind_a == kind_b == 'r':
        return base + (CHI if i != j and {i, j} == set(exceptional) else 0)
    return base * LAM[i if kind_a == 'r' else j]


def label_vector(label):
    if len(label) == 1:
        return {('v', label[0]): F(1)}
    tail, head = label
    return {('v', head): F(1), ('r', tail): F(1)}


def distance_form(left, right, exceptional):
    coeff = label_vector(left)
    for key, value in label_vector(right).items():
        coeff[key] = coeff.get(key, 0) - value
    return sum((x * y * gram(a, b, exceptional)
                for a, x in coeff.items() for b, y in coeff.items()), Poly())


def endpoint_distance(left, right, sign):
    """Independent endpoint expansion using only the physical four-vector Gram."""
    coeff = [0] * 4
    for factor, label in ((1, left), (-1, right)):
        if len(label) == 1:
            coeff[label[0]] += factor
        else:
            a, b = label
            coeff[b] += factor
            coeff[a] += factor * sign
    return sum((coeff[i] * coeff[j] * (H[i] - C if i == j else -C)
                for i in range(4) for j in range(4)), Poly())


def expected_form(left, right, exceptional):
    if len(left) == len(right) == 1:
        return endpoint_distance(left, right, 1)
    if len(left) == 1:
        left, right = right, left
    a, b = left
    if len(right) == 1:
        m = right[0]
        base = endpoint_distance((b,), (m,), 1)
        return base + H[a] - C - 2 * H[a] * LAM[a] * (m == a)
    e, f = right
    base = endpoint_distance((b,), (f,), 1)
    if a == e:
        return base
    return (base + H[a] + H[e]
            - 2 * H[a] * LAM[a] * (f == a)
            - 2 * H[e] * LAM[e] * (b == e)
            - (2 * CHI if {a, e} == set(exceptional) else 0))


def check_tournaments():
    counts = Counter()
    exceptional_pairs = 0
    audited_pairs = 0
    control_count = 0
    for mask in range(64):
        arcs = tournament(mask)
        degree = Counter(a for a, _ in arcs)
        if any(degree[j] == 0 for j in range(4)):
            counts['prior_sink_motion'] += 1
            continue
        counts['new_sinkless_motion'] += 1
        eligible = [a for a in range(4) if degree[a] == 1]
        require(eligible, 'sinkless tournament lacks the required vertex')
        i = min(eligible)
        k = next(b for a, b in arcs if a == i)
        labels = tuple((a,) for a in range(4)) + arcs
        require(len(labels) == 10, 'wrong label count')
        for left, right in combinations(labels, 2):
            form = distance_form(left, right, (i, k))
            equal(form, expected_form(left, right, (i, k)),
                  'distance identity failed: ' + str((mask, left, right)))
            for sign in (-1, 1):
                values = {'lambda' + str(j): sign for j in range(4)}
                values['chi'] = 0
                equal(form.sub(values), endpoint_distance(left, right, sign),
                      'endpoint mismatch')
            audited_pairs += 1
            if form.diff('chi') != 0:
                equal(form.diff('chi'), -2, 'exceptional Gram coefficient')
                equal(form.diff('lambda' + str(k)), -2 * H[k],
                      'exceptional distance lacks its reserve')
                for a in range(4):
                    if a != k:
                        equal(form.diff('lambda' + str(a)), 0,
                              'unexpected exceptional coefficient')
                exceptional_pairs += 1
            else:
                # Every remaining varying coefficient is 0 or -2h_a.
                for a in range(4):
                    coefficient = form.diff('lambda' + str(a))
                    require(coefficient == 0 or coefficient == -2 * H[a],
                            'unpaid nonexceptional distance')
        # A full-family tight distance has chi but no compensating lambda.
        r = next(a for a in range(4) if a not in (i, k))
        bad = distance_form((i, r), (k, r), (i, k))
        equal(bad.diff('chi'), -2, 'rejection control lost its hump')
        for a in range(4):
            equal(bad.diff('lambda' + str(a)), 0, 'control unexpectedly paid')
        control_count += 1
    require(dict(counts) == {'prior_sink_motion': 32, 'new_sinkless_motion': 32},
            'selector coverage changed')
    return {'selector_counts': dict(sorted(counts.items())),
            'formal_label_pair_identities': audited_pairs,
            'exceptional_pairs_with_contraction_reserve': exceptional_pairs,
            'full_family_motion_rejection_controls': control_count}


def check_polynomials():
    t, q, A, B, L, Q, z = map(variable, ('t', 'q', 'A', 'B', 'L', 'Q', 'z'))
    identities = []

    def check(name, left, right):
        equal(left, right, name)
        identities.append(name)

    check('Moebius norm', (t + q)**2 + (1 - q**2) * (1 - t**2),
          (1 + q*t)**2)
    check('Moebius mixed Gram', t * (t + q) + 1 - t**2, 1 + q*t)
    f, g = 1 - t**2, 1 + q*t
    n = f.diff('t') * g - f * g.diff('t')
    check('quotient first derivative numerator', n, -(q*t**2 + 2*t + q))
    check('quotient second derivative numerator',
          n.diff('t') * g - 2*n * g.diff('t'), -2*(1-q**2))
    check('endpoint derivative numerator', n.sub({'t': 1}), -2*(1+q))
    check('exceptional delta identity after multiplying by L',
          L*Q + (A*B-L)*(Q+A*B), A*B*(Q+A*B-L))
    check('normal-norm h_k', L+B**2+(A*B-L), B*(A+B))
    check('hyperbolic margin factorization',
          B*(A+B)-A*B*(1-z)**2, B**2+A*B*z*(2-z))
    # (2 cosh(d)-2)e^-d=(1-e^-d)^2, with z=e^-d.
    check('exponential margin identity', (1+z**2)-2*z, (1-z)**2)
    # Verify the formal calculator is not simply accepting every identity.
    require((t+q)**2 != (t-q)**2, 'polynomial rejection control failed')
    return identities


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F())


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def fixture(a, b, d):
    a, b, d = F(a), F(b), F(d)
    require(min(a, b, d) > 0, 'invalid shape')
    z = -1/a
    x = -(1+1/a**2)/b
    y = -(1+1/a**2+x**2)/d
    return ((F(0), F(0), a), (b, F(0), z), (x, d, z), (x, y, z))


def projection(v, a, b):
    aa, ab, bb = dot(a, a), dot(a, b), dot(b, b)
    det = aa*bb-ab**2
    require(det > 0, 'dependent complementary vectors')
    va, vb = dot(v, a), dot(v, b)
    x, y = (bb*va-ab*vb)/det, (aa*vb-ab*va)/det
    return tuple(x*ai+y*bi for ai, bi in zip(a, b))


def check_fixtures():
    regular = tuple(tuple(map(F, row)) for row in
                    ((1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)))
    shapes = {'regular': regular, 'asymmetric_1_2_3': fixture(1,2,3),
              'thin_1_over_5_3_7_over_2': fixture(F(1,5),3,F(7,2))}
    records = []
    projection_checks = 0
    endpoint_checks = 0
    for name, v in shapes.items():
        for a, b in EDGES:
            equal(dot(v[a], v[b]), -1, 'fixture is not orthocentric')
        h = tuple(dot(x, x)+1 for x in v)
        equal(sum(1/x for x in h), 1, 'kernel normalization')
        for coordinate in range(3):
            equal(sum(v[i][coordinate]/h[i] for i in range(4)), 0,
                  'positive kernel vector')
        for i in range(4):
            for k in range(4):
                if i == k:
                    continue
                r, l = [a for a in range(4) if a not in (i,k)]
                p = projection(v[i], v[r], v[l])
                equal(p, projection(v[k], v[r], v[l]), 'common projection')
                L = dot(p,p)
                ni, nk = sub(v[i],p), sub(v[k],p)
                a2, b2 = dot(ni,ni), dot(nk,nk)
                require(min(L,a2,b2) > 0, 'degenerate normal geometry')
                equal(dot(ni,nk), -(L+1), 'normal orientation')
                equal(a2*b2, (L+1)**2, 'AB=L+c squared')
                equal(h[k], b2+L+1, 'h_k=B^2+AB')
                projection_checks += 1
        labels = tuple((i,) for i in range(4)) + tuple(
            (i,j) for i in range(4) for j in range(4) if i!=j)
        for left, right in combinations(labels, 2):
            def point(label, sign):
                if len(label) == 1:
                    return v[label[0]]
                a,b = label
                return tuple(v[b][c]+sign*v[a][c] for c in range(3))
            d0 = sub(point(left,-1),point(right,-1))
            d1 = sub(point(left,1),point(right,1))
            require(dot(d0,d0)-dot(d1,d1) >= 0, 'endpoint is not a contraction')
            endpoint_checks += 1
        records.append({'name': name,
                        'vertices': [[str(x) for x in row] for row in v],
                        'h': [str(x) for x in h]})
    return {'fixtures': records, 'ordered_projection_checks': projection_checks,
            'direct_coordinate_endpoint_pairs': endpoint_checks}


def check_common_target_and_radii():
    # An asymmetric exact split including a zero edge and deterministic edges.
    p = (F(1,3), F(0), F(1), F(2,5), F(4,7), F(3,4))
    edge_mass = (F(2), F(3), F(0), F(5), F(7), F(11))
    weights = []
    for mask in range(64):
        w = F(1)
        for e in range(6):
            w *= p[e] if mask & (1<<e) else 1-p[e]
        weights.append(w)
    equal(sum(weights), 1, 'selector probabilities')
    for e in range(6):
        marginal = sum(w for mask,w in enumerate(weights) if mask & (1<<e))
        equal(marginal*edge_mass[e], p[e]*edge_mass[e], 'source split')
        equal(sum(w*edge_mass[e] for w in weights), edge_mass[e], 'fixed target')
    # Max/min radius selection is checked for every possible ordering/tie pattern.
    cases = 0
    for left in range(4):
        for right in range(4):
            for squared_distance in map(F, (0, F(1,2), 1, 2, 4, 8, 9, 16)):
                inside_left = squared_distance <= left**2
                inside_right = squared_distance <= right**2
                equal(inside_left or inside_right,
                      squared_distance <= max(left,right)**2, 'union max rule')
                equal(inside_left and inside_right,
                      squared_distance <= min(left,right)**2, 'intersection min rule')
                cases += 1
    return {'exact_common_target_marginals': 6, 'radius_order_controls': cases}


def result():
    return {'status': 'exact finite controls passed; universal proof is in PROOF.md',
            'polynomial_identities': check_polynomials(),
            'tournaments': check_tournaments(), 'geometry': check_fixtures(),
            'mixture_and_radius_controls': check_common_target_and_radii(),
            'scope': 'No Gaussian integration, solver, sampled-path sign inference, '
                     'or independent peer review is claimed.'}


def main():
    if sys.argv[1:] not in ([], ['--emit']):
        raise SystemExit('Usage: python3 verify.py [--emit]')
    answer = result()
    if sys.argv[1:] == ['--emit']:
        print(json.dumps(answer, indent=2, sort_keys=True))
        return
    expected_path = Path(__file__).with_name('EXPECTED.json')
    expected = json.loads(expected_path.read_text())
    require(answer == expected, 'EXPECTED.json differs from exact recomputation')
    print('PASS: 32 new sinkless motions + 32 prior sink motions cover all selectors.')
    print('PASS: 1440 formal distance pairs, 36 projection checks, 360 endpoint pairs.')
    print('PASS: exact identities, common-target/radius controls, full-map rejection.')


if __name__ == '__main__':
    main()
