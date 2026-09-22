#!/usr/bin/env python3
"""Exact finite corroboration of PROOF.md, not a proof of its quantifiers.

Python 3.11+, standard library. No downloaded inputs or floating arithmetic.
All checks stay enabled under python -O.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
from math import comb, factorial
from pathlib import Path
import json
import random


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


def rref(a):
    a = [list(map(F, row)) for row in a]
    if not a:
        return a, []
    pivots = []
    row = 0
    for j in range(len(a[0])):
        p = next((i for i in range(row, len(a)) if a[i][j]), None)
        if p is None:
            continue
        a[row], a[p] = a[p], a[row]
        v = a[row][j]
        a[row] = [x/v for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][j]:
                v = a[i][j]
                a[i] = [x-v*y for x, y in zip(a[i], a[row])]
        pivots.append(j)
        row += 1
        if row == len(a):
            break
    return a, pivots


def rank(a):
    return len(rref(a)[1])


def nullspace(a):
    b, pivots = rref(a)
    out = []
    for j in range(len(a[0])):
        if j not in pivots:
            v = [F(0)]*len(a[0])
            v[j] = 1
            for i, p in enumerate(pivots):
                v[p] = -b[i][j]
            out.append(v)
    return out


def inverse(a):
    n = len(a)
    b, p = rref([list(row)+[F(i == j) for j in range(n)]
                 for i, row in enumerate(a)])
    need(p[:n] == list(range(n)), "singular matrix")
    return [row[n:] for row in b]


def determinant(a):
    a = [list(map(F, row)) for row in a]
    out = F(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return F(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            out = -out
        v = a[j][j]
        out *= v
        for i in range(j+1, len(a)):
            q = a[i][j]/v
            a[i] = [x-q*y for x, y in zip(a[i], a[j])]
    return out


def binom(a, m):
    out = F(1)
    for j in range(m):
        out *= F(a-j, j+1)
    return out


def rising(a, m):
    out = F(1)
    for j in range(m):
        out *= a+j
    return out


def bcoef(d, m):
    need(d >= 2 and m >= 1, "invalid dimension or moment degree")
    return ((-1)**(m-1)*rising(F(d, 2)+1, m-1)
            / (factorial(m-1)*2*m*(2*m-1)))


@lru_cache(None)
def exponents(d, degree):
    if d == 1:
        return ((degree,),)
    return tuple((j,)+e for j in range(degree+1)
                 for e in exponents(d-1, degree-j))


def monomial(e, v):
    out = F(1)
    for a, x in zip(e, v):
        out *= x**a
    return out


def poly_mul(p, q):
    out = {}
    for a, x in p.items():
        for b, y in q.items():
            e = tuple(i+j for i, j in zip(a, b))
            out[e] = out.get(e, F(0))+x*y
    return {e: x for e, x in out.items() if x}


def linear(v):
    d = len(v)
    return {tuple(int(i == j) for i in range(d)): F(v[j])
            for j in range(d) if v[j]}


def poly_eval(p, v):
    return sum((x*monomial(e, v) for e, x in p.items()), F(0))


def moment_table(atoms, degree):
    return {e: sum((w*monomial(e, u) for u, w in atoms), F(0))
            for e in exponents(len(atoms[0][0]), degree)}


def jet(atoms, degree):
    """Atoms encode antipodal PAIRS, with the total mass of the pair."""
    d = len(atoms[0][0])
    c = bcoef(d, degree//2)
    return {e: c*factorial(degree)*v
            / product_factorials(e) for e, v in moment_table(atoms, degree).items()}


def product_factorials(e):
    out = 1
    for j in e:
        out *= factorial(j)
    return out


def decode_jet(t):
    need(bool(t), "empty jet")
    e0 = next(iter(t))
    d, degree = len(e0), sum(e0)
    need(degree >= 2 and degree % 2 == 0, "jet degree is not positive even")
    need(set(t) == set(exponents(d, degree)), "incomplete jet")
    return {e: v*product_factorials(e)/(bcoef(d, degree//2)*factorial(degree))
            for e, v in t.items()}


def functional(moments, p):
    return sum((x*moments[e] for e, x in p.items()), F(0))


def separator(lines, target, skip=None):
    """Product hyperplane proof in Section 4; skip=target index isolates it."""
    d = len(target)
    remaining = [i for i in range(len(lines)) if i != skip]
    for ix in combinations(remaining, d-1):
        v = nullspace([lines[i] for i in ix])
        if len(v) == 1 and dot(v[0], target):
            p = linear(v[0])
            break
    else:
        raise ValueError("no separating hyperplane")
    for i in remaining:
        if i in ix:
            continue
        s = lines[i]
        v = [dot(s, s)*z-dot(s, target)*a for a, z in zip(s, target)]
        need(dot(v, target) != 0, "target lies on a covered line")
        p = poly_mul(p, linear(v))
    return p


def reconstruct_with_lines(top, previous, lines):
    """Check an exact candidate-line certificate and recover polar outer products.

    Line discovery (solving a real projective polynomial system) is not
    implemented. This checker validates a supplied rational line list.
    The theorem assumes input jets of a genuine symmetric convex body.
    """
    d, r = len(lines[0]), len(lines)
    k = r-d+2
    need(d >= 2 and k >= 2 and rank(lines) == d, "nonspanning line certificate")
    for i, u in enumerate(lines):
        need(dot(u, u)>0, "zero line")
        for v in lines[:i]:
            need(rank([u, v]) == 2, "repeated projective line")
    need(sum(next(iter(top))) == 2*k, "wrong top degree")
    need(sum(next(iter(previous))) == 2*k-2, "wrong previous degree")
    high, low = decode_jet(top), decode_jet(previous)
    basis = exponents(d, k)
    evaluation = [[monomial(e, u) for e in basis] for u in lines]
    need(rank(evaluation) == r, "bad evaluation rank")
    gram = [[high[tuple(x+y for x, y in zip(a, b))] for b in basis] for a in basis]
    need(rank(gram) == r, "bad moment rank")
    ker = nullspace(gram)
    need(all(dot(row, v) == 0 for row in evaluation for v in ker),
         "candidate lines do not annihilate the kernel")
    reconstructed, outer = [], []
    for j, v in enumerate(lines):
        q = separator(lines, v, skip=j)
        need(all(poly_eval(q, u) == 0 for i, u in enumerate(lines) if i != j),
             "interpolation failed")
        q2 = poly_mul(q, q)
        a = linear([x/dot(v, v) for x in v])
        den = functional(low, q2)
        need(den > 0, "missing or nonpositive atom")
        alpha2 = functional(high, poly_mul(poly_mul(a, a), q2))/den
        need(alpha2 > 0, "nonpositive squared radius")
        mass = den/(alpha2**(k-1)*poly_eval(q, v)**2)
        outer.append([[alpha2*x*y for y in v] for x in v])
        reconstructed.append((v, alpha2, mass))
    # Entrywise reconstruction of both entire moment tensors, without roots.
    for degree, moments in [(2*k, high), (2*k-2, low)]:
        for e, value in moments.items():
            got = sum(w*a2**(degree//2)*monomial(e, v)
                      for v, a2, w in reconstructed)
            need(got == value, "reconstructed moment mismatch")
    return outer, len(basis), len(ker)


def hull(points):
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    points = sorted(set(points))
    halves = []
    for seq in (points, points[::-1]):
        h = []
        for p in seq:
            while len(h)>1 and cross(h[-2], h[-1], p)<=0:
                h.pop()
            h.append(p)
        halves.append(h[:-1])
    return halves[0]+halves[1]


def polygon_prism(d, pairs):
    points = []
    for j in range(pairs):
        t = F(j, pairs)
        v = ((1-t*t)/(1+t*t), 2*t/(1+t*t))
        points.extend([v, tuple(-x for x in v)])
    vertices = hull(points)
    need(len(vertices) == 2*pairs, "circle hull lost a vertex")
    area2 = sum(p[0]*q[1]-p[1]*q[0]
                for p, q in zip(vertices, vertices[1:]+vertices[:1]))
    area = area2/2
    sides = [F(j+2, j+1) for j in range(d-2)]
    box = F(1)
    for a in sides:
        box *= 2*a
    atoms = []
    for p, q in list(zip(vertices, vertices[1:]+vertices[:1]))[:pairs]:
        normal = (q[1]-p[1], p[0]-q[0])
        support = dot(normal, p)
        need(support > 0, "bad polygon orientation")
        u = tuple(z/support for z in normal)+(F(0),)*(d-2)
        atoms.append((u, 2*support*box))
    for j, a in enumerate(sides):
        u = tuple(F(i == j+2)/a for i in range(d))
        atoms.append((u, area*box))
    need(sum(w for _, w in atoms) == d*area*box, "cone measure mass")
    return atoms, area*box


def encode(x):
    if isinstance(x, F):
        return str(x)
    raise TypeError(type(x).__name__)


def run():
    counts = Counter()
    records = []
    rng = random.Random(6092206)
    for d in range(2, 21):
        for m in range(1, 21):
            explicit = (binom(F(2-d, 2), m)
                        + F(d-1, 2*m-1)*binom(F(-d, 2), m-1))/d
            b = bcoef(d, m)
            need(b == explicit, "kernel expansion normalization")
            sphere = rising(F(1, 2), m)/rising(F(d, 2), m)
            need(d*b*sphere == binom(F(1, 2), m), "ellipsoid volume expansion")
            counts['kernel_coefficients'] += 1
            counts['ball_moment_identities'] += 1
            records.append([d, m, b])

    # Independent local second-derivative expansion versus determinant formula.
    triples = [(F(0), F(1)), (F(3, 4), F(5, 4)),
               (F(-4, 3), F(5, 3)), (F(5, 12), F(13, 12))]
    for d in range(2, 9):
        n = d-1
        for t, f in triples:
            lower = [[F(rng.randrange(-2, 3)) if j <= i else F(0)
                      for j in range(n)] for i in range(n)]
            q = mm(lower, transpose(lower))
            q = [[x+int(i == j) for j, x in enumerate(row)] for i, row in enumerate(q)]
            h = F(3, 2)
            g = [F(rng.randrange(-2, 3), 3) for _ in range(n)]
            w = [F(rng.randrange(-2, 3), 5) for _ in range(n)]
            ht = [[-(g[i]*w[j]+w[i]*g[j]+t*q[i][j])/h
                   for j in range(n)] for i in range(n)]
            fp, fpp = t/f, 1/f**3
            qh = [[f*(q[i][j]-h*int(i == j))
                   + fp*(g[i]*w[j]+w[i]*g[j])+h*fpp*w[i]*w[j]
                   + h*fp*ht[i][j]+h*f*int(i == j)
                   for j in range(n)] for i in range(n)]
            detq = determinant(q)
            invq = inverse(q)
            contraction = detq*sum(w[i]*invq[i][j]*w[j]
                                   for i in range(n) for j in range(n))
            lhs = h*f*determinant(qh)
            rhs = h*f**(2-d)*detq+h*h*f**(-d)*contraction
            need(lhs == rhs, "rank-one support determinant")
            need(sum(detq*invq[i][j]*(h*ht[i][j]+2*g[i]*w[j])
                     for i in range(n) for j in range(n)) == -(d-1)*t*detq,
                 "contracted spherical identity")
            counts['local_curvature_checks'] += 1
            records.append([d, t, lhs])

    # Exact volumes of [-1,1] x B plus an axial Firey segment, from fibers.
    for d in range(3, 16, 2):
        j = (d-3)//2
        for t, f in triples[:2]+[(F(4, 3), F(5, 3)), (F(12, 5), F(13, 5))]:
            s0, u0 = 1/f, t/f
            integral = sum(F((-1)**q*comb(j, q), 2*q+3)*u0**(2*q+3)
                           for q in range(j+1))
            direct = f*s0**(d-1)+F(d-1, d)*(1-s0**d)+(d-1)*t*integral
            jd = sum(F((-1)**q*comb(j, q), 2*q+1)*u0**(2*q+1)
                     for q in range(j+1))
            phi = f**(2-d)+(d-1)*t*jd
            need(direct == (phi+d-1)/d, "definition-level axial prism volume")
            counts['direct_prism_volumes'] += 1
            records.append([d, t, direct])

    last = None
    for d in range(2, 6):
        for pairs in range(2, 5):
            atoms, volume = polygon_prism(d, pairs)
            # Nonsymmetric coordinate representation via an invertible shear.
            transform = [[F(i == j)+F(1, 3)*int(j == i+1)
                          for j in range(d)] for i in range(d)]
            transform[0][0] = 2
            determinant_t = determinant(transform)
            it = transpose(inverse(transform))
            changed = [(tuple(dot(row, u) for row in it), determinant_t*w)
                       for u, w in atoms]
            for version, data in enumerate([atoms, changed]):
                r, k = len(data), len(data)-d+2
                scales = [F(i+2, i+1) for i in range(r)]
                lines = [tuple(x/a for x in u) for (u, _), a in zip(data, scales)]
                top, previous = jet(data, 2*k), jet(data, 2*k-2)
                out, size, kernel = reconstruct_with_lines(top, previous, lines)
                expected = [[[x*y for y in u] for x in u] for u, _ in data]
                need(out == expected, "polar endpoint reconstruction")
                counts['realizable_polytope_fixtures'] += 1
                counts['polar_pairs_reconstructed'] += r
                counts['kernel_dimensions_checked'] += 1
                records.append([d, r, version, size, kernel, out])
                # Construct separators for off-support points, including zeros
                # in coordinates; do not infer a universal variety from samples.
                for _ in range(3):
                    z = tuple(F(rng.randrange(-3, 4)) for _ in range(d))
                    if not dot(z, z) or any(rank([z, v]) == 1 for v in lines):
                        continue
                    p = separator(lines, z)
                    need(all(poly_eval(p, v) == 0 for v in lines), "separator zero")
                    need(poly_eval(p, z) != 0, "separator nonzero")
                    counts['off_support_separators'] += 1
                last = top, previous, lines
            for degree in [2*pairs-2, 2*pairs]:
                before = moment_table(atoms, degree)
                after = moment_table(changed, degree)
                for _ in range(3):
                    v = [F(rng.randrange(-2, 3)) for _ in range(d)]
                    tv = [dot(row, v) for row in transform]
                    def directional(table, vec):
                        return sum(F(factorial(degree), product_factorials(e))*a*monomial(e, vec)
                                   for e, a in table.items())
                    need(directional(after, tv) == determinant_t*directional(before, v),
                         "affine moment covariance")
                    counts['affine_covariance_checks'] += 1

    # Nonproduct facet configurations: crosspolytopes and their affine images.
    for d in (3, 4):
        atoms = [(tuple(map(F, (1,)+s)), F(2, factorial(d-1)))
                 for s in product((-1, 1), repeat=d-1)]
        transform = [[F(i == j)+F(1, 2)*int(j == i+1)
                      for j in range(d)] for i in range(d)]
        it = transpose(inverse(transform))
        changed = [(tuple(dot(row, u) for row in it), w) for u, w in atoms]
        for data in (atoms, changed):
            k = len(data)-d+2
            lines = [tuple(x/F(i+2, i+1) for x in u) for i, (u, _) in enumerate(data)]
            out, size, kernel = reconstruct_with_lines(jet(data, 2*k), jet(data, 2*k-2), lines)
            need(out == [[[x*y for y in u] for x in u] for u, _ in data],
                 "crosspolytope reconstruction")
            counts['realizable_polytope_fixtures'] += 1
            counts['polar_pairs_reconstructed'] += len(data)
            counts['kernel_dimensions_checked'] += 1
            records.append(['crosspolytope', d, size, kernel, out])

    def sphere_monomial(e):
        if any(j % 2 for j in e):
            return F(0)
        value = F(1)
        for j in e:
            value *= rising(F(1, 2), j//2)
        return value/rising(F(len(e), 2), sum(e)//2)
    for d in range(2, 5):
        for k in (2, 3):
            basis = exponents(d, k)
            gram = [[sphere_monomial(tuple(x+y for x, y in zip(a, b)))
                     for b in basis] for a in basis]
            need(rank(gram) == len(basis), "smooth ball Gram form not positive definite")
            counts['smooth_full_rank_controls'] += 1
    # C = unit disk x [-1,1] in R^3. Divide nu_C by pi: equator mass 4,
    # antipodal z-axis mass 2. Singular degree-two Gram, but infinite support.
    for k, expected_rank in [(2, 4), (3, 5)]:
        basis = exponents(3, k)
        def cylinder_moment(e):
            return ((4*sphere_monomial(e[:2]) if e[2] == 0 else F(0))
                    + (F(2) if e[0] == e[1] == 0 else F(0)))
        gram = [[cylinder_moment(tuple(x+y for x, y in zip(a, b)))
                 for b in basis] for a in basis]
        need(rank(gram) == expected_rank, "nonpolytope singular-Gram boundary")
        counts['cylinder_rank_controls'] += 1
        records.append(['cylinder', k, expected_rank])

    # Exact frequency cancellation underlying EVERY sharpness product family.
    for d in range(2, 10):
        for k in range(2, 21):
            for degree in range(2*k):
                surviving = [q for q in range(-degree, degree+1, 2) if q % (2*k) == 0]
                need(all(q == 0 for q in surviving), "premature angular frequency")
                counts['sharpness_frequency_checks'] += 1
            need(2*k % (2*k) == 0, "top angular frequency absent")

    # Scale-critical one-term ambiguity on an actual four-dimensional box.
    atoms, _ = polygon_prism(4, 2)
    dilated = [(tuple(x/3 for x in u), 3**4*w) for u, w in atoms]
    need(jet(atoms, 4) == jet(dilated, 4), "critical fourth term not invariant")
    need(jet(atoms, 2) != jet(dilated, 2), "quadratic term lost scale")
    counts['critical_scale_examples'] = 1

    # Adversarial certificate inputs and wrong coefficient normalization.
    top, prev, lines = last
    def reject(call):
        try:
            call()
        except (ValueError, KeyError):
            counts['rejected_corruptions'] += 1
        else:
            raise ValueError("corruption accepted")
    reject(lambda: reconstruct_with_lines(top, prev, lines[:-1]+[lines[0]]))
    reject(lambda: reconstruct_with_lines(top, prev, [tuple(F(0) for _ in lines[0])]+lines[1:]))
    # Negating the entire even moment form is definitely invalid. A change
    # to one pure-power entry can instead be valid data for a different atom.
    damaged = {e: -v for e, v in top.items()}
    reject(lambda: reconstruct_with_lines(damaged, prev, lines))
    reject(lambda: decode_jet({}))
    reject(lambda: bcoef(1, 2))
    reject(lambda: decode_jet({(1, 0): F(1)}))
    summary = dict(sorted(counts.items()))
    summary['record_sha256'] = sha256(json.dumps(records, default=encode,
        separators=(',', ':')).encode()).hexdigest()
    expected_path = Path(__file__).with_name('expected.json')
    if expected_path.exists():
        need(summary == json.loads(expected_path.read_text()), "expected summary mismatch")
    return summary


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
