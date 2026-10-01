"""Independent exact checks by six-reviewer-1, mathematical reviewer.

No campaign code, certificates or native solvers are imported. The written
analytic and topological bridges are audited in REVIEW.md, not formalized here.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from math import gcd
import argparse
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class A:
    """Exact c + ncoef*n + jcoef*j; multiplication is only by scalars."""
    c: F = F(0)
    n: F = F(0)
    j: F = F(0)

    def __add__(self, other):
        other = affine(other)
        return A(self.c + other.c, self.n + other.n, self.j + other.j)

    __radd__ = __add__

    def __neg__(self):
        return A(-self.c, -self.n, -self.j)

    def __sub__(self, other):
        return self + (-affine(other))

    def __rsub__(self, other):
        return affine(other) + (-self)

    def __mul__(self, scalar):
        scalar = F(scalar)
        return A(self.c * scalar, self.n * scalar, self.j * scalar)

    __rmul__ = __mul__

    def at(self, width, index=0):
        return self.c + self.n * width + self.j * index

    def record(self):
        return [str(self.c), str(self.n), str(self.j)]


def affine(x):
    return x if isinstance(x, A) else A(F(x))


def point(q, r):
    return affine(q), affine(r)


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def minus(a, b):
    return tuple(x - y for x, y in zip(a, b))


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def norm(v):
    return v[0]**2 + v[0]*v[1] + v[1]**2


# Literal matrices, rather than the author's iterated rotation routines.
ROTATIONS = (
    ((1, 0), (0, 1)), ((0, -1), (1, 1)),
    ((-1, -1), (1, 0)), ((-1, 0), (0, -1)),
    ((0, 1), (-1, -1)), ((1, 1), (-1, 0)),
)
J = ((1, 1), (0, -1))


def product(m, p):
    return tuple(tuple(sum(m[i][l]*p[l][k] for l in range(2))
                       for k in range(2)) for i in range(2))


def matrix(h, k):
    return product(ROTATIONS[k], J) if h else ROTATIONS[k]


def apply(m, p):
    return tuple(m[i][0]*p[0] + m[i][1]*p[1] for i in range(2))


N, INDEX = A(n=F(1)), A(j=F(1))
ZERO = point(0, 0)
VERTICES = (point(0, -1), point(N, -1), point(N-1, 1), point(0, 1))
PRIMITIVES = ((1, 0), (-1, 2), (-1, 0), (0, -1))
FACTORS = (N, affine(1), N-1, affine(2))


def planes(h, k, translation=ZERO):
    m = matrix(h, k)
    return [(tuple((1-2*h)*x for x in apply(m, v)),
             plus(apply(m, a), translation))
            for v, a in zip(PRIMITIVES, VERTICES)]


def direction_audit():
    directions = set()
    factors = []
    for h in (0, 1):
        for k in range(6):
            m = matrix(h, k)
            require(det(m[0], m[1]) == 1-2*h, 'matrix handedness')
            for v in ((1, 0), (0, 1), (1, 1)):
                require(norm(apply(m, v)) == norm(v), 'metric isometry')
            for i, (v, factor) in enumerate(zip(PRIMITIVES, FACTORS)):
                edge = minus(apply(m, VERTICES[(i+1)%4]), apply(m, VERTICES[i]))
                mv = apply(m, v)
                require(edge == tuple(factor*x for x in mv), 'affine edge identity')
                require(factor.j == 0 and factor.n >= 0 and factor.at(8) > 0,
                        'uniform positive side factor')
                u = tuple((1-2*h)*x for x in mv)
                require(gcd(*u) == 1 and norm(u) in (1, 3), 'primitive norm')
                directions.add(u)
                factors.append(factor.record())
    magnitudes = sorted({abs(det(u, v)) for u in directions for v in directions})
    require(len(directions) == 12 and magnitudes == [0, 1, 2, 3], 'direction completeness')
    return {'orientations': 12, 'affine_edge_identities': len(factors),
            'directions': [list(v) for v in sorted(directions)],
            'determinant_magnitudes': magnitudes}


def fillers(required_upper_sign=-1):
    b, c = VERTICES[1:3]
    corners = [(b, -1, (-1, 2)), (c, +1, (1, -2))]
    targets = [(b, +1, (1, -2)), (c, required_upper_sign, (-1, 2))]
    rows = []
    for endpoint, sign, ray in targets:
        found = []
        for proto, state, flat in corners:
            for h in (0, 1):
                for k in range(6):
                    m = matrix(h, k)
                    if state == sign and apply(m, (-1, 0)) == (-1, 0) and apply(m, flat) == ray:
                        found.append((h, k, minus(endpoint, apply(m, proto))))
        rows.append(found)
    expected = [[(0, 0, point(1, -2))], [(0, 0, point(-1, 2))]]
    require(rows == expected, 'endpoint filler uniqueness/translation/state')
    return {'corner_orientation_cases': 48,
            'lower': [0, 0, 1, -2], 'upper': [0, 0, -1, 2]}


# Port families retain their symbolic index and all n>=8, not sampled widths.
PORTS = [('bottom', -1, point(INDEX, -1), point(INDEX+1, -1), N-1),
         ('top', +1, point(N-1-INDEX, 1), point(N-2-INDEX, 1), N-2),
         ('left', +1, point(0, 1-INDEX), point(0, -INDEX), affine(1))]
ROOT_PORTS = [('+', +1, point(0, 1), point(0, 0)),
              ('-', -1, point(0, -1), point(1, -1))]


def providers():
    answer = []
    for root_name, root_sign, root_start, root_end in ROOT_PORTS:
        for name, sign, start, end, upper in PORTS:
            if sign != -root_sign:
                continue
            for h in (0, 1):
                for k in range(6):
                    m = matrix(h, k)
                    s, e = apply(m, start), apply(m, end)
                    if h:
                        s, e = e, s  # restore physical counterclockwise order
                    if minus(e, s) != minus(root_start, root_end):
                        continue
                    translation = minus(root_end, s)
                    require(plus(e, translation) == root_start, 'second endpoint match')
                    answer.append((root_name, name, h, k, translation, upper))
    require([(r[0],r[1],r[2],r[3]) for r in answer] ==
            [('+','bottom',0,1), ('+','bottom',1,4),
             ('-','top',0,0), ('-','top',1,3),
             ('-','left',0,5), ('-','left',1,4)], 'complete charged providers')
    return answer


def endpoint_lower_bound(slack, lower, upper, margin):
    require(lower.j == upper.j == 0 and (upper-lower).n >= 0 and
            (upper-lower).at(8) >= 0, 'parameter domain')
    result = []
    for bound in (lower, upper):
        s = A(slack.c + slack.j*bound.c, slack.n + slack.j*bound.n)
        require(s.n >= 0 and s.at(8) >= margin, 'all-width half-plane bound')
        result.append([str(s.at(8)), str(s.n)])
    return result


def obstruction():
    rows = providers()
    evidence = []
    for i, row in enumerate(rows):
        root, name, h, k, translation, upper = row
        lower = affine(1 if i == 1 else 0)
        if i == 5:
            upper = affine(0)  # a=1-j: j=1 is the forced, unblocked provider
        blocker = point(-1, 2) if root == '+' else point(1, -2)
        w = [point(F(-1,2),F(9,8)), point(F(-1,2),F(3,2)),
             point(F(5,4),-2), point(F(5,4),-2),
             point(F(3,2),-2), point(F(3,2),-2)][i]
        checks = []
        for u, anchor in planes(h, k, translation)+planes(0, 0, blocker):
            slack = det(u, minus(w, anchor))
            checks.append(endpoint_lower_bound(slack, lower, upper, F(1,8)))
        evidence.append({'family': [root, name, h, k],
                         'translation': [x.record() for x in translation],
                         'index_lower': lower.record(), 'index_upper': upper.record(),
                         'common_point': [str(x.c) for x in w], 'bounds': checks})
    p = rows[1]; q = rows[5]
    pt = tuple(A(x.c, x.n) for x in p[4])
    qt = tuple(A(x.c+x.j, x.n) for x in q[4])
    require(pt == point(-1,1) and qt == point(0,-1), 'forced provider poses')
    w = point(F(-1,2), -2)
    conflict = [endpoint_lower_bound(det(u,minus(w,a)),affine(0),affine(0),F(1,8))
                for u,a in planes(p[2],p[3],pt)+planes(q[2],q[3],qt)]
    return {'symbolic_families': evidence, 'forced_conflict': conflict,
            'primitive_halfplanes_checked': 56, 'margin': '1/8'}


def numeric_planes(width, h, k, translation):
    return [(u, tuple(x.at(width) for x in a)) for u,a in
            planes(h,k,point(*translation))]


def hull(points):
    ordered = sorted(set(points))
    if len(ordered) <= 1:
        return ordered
    halves = []
    for seq in (ordered, list(reversed(ordered))):
        part = []
        for p in seq:
            while len(part) >= 2 and det(minus(part[-1],part[-2]),minus(p,part[-1])) <= 0:
                part.pop()
            part.append(p)
        halves.append(part)
    return halves[0][:-1]+halves[1][:-1]


def intersection(all_planes):
    vertices = []
    for (u,a),(v,b) in combinations(all_planes,2):
        divisor = det(u,v)
        if not divisor:
            continue
        first, second = det(u,a), det(v,b)
        w = (F(first*v[0]-u[0]*second,divisor),
             F(first*v[1]-u[1]*second,divisor))
        if all(det(t,minus(w,p)) >= 0 for t,p in all_planes):
            vertices.append(w)
    return hull(vertices)


def check_vertex_margin(vertices, all_planes, denominator):
    k = len(vertices)
    require(3 <= k <= 8, 'positive-area extreme-vertex count')
    bary = tuple(sum(v[i] for v in vertices)/k for i in range(2))
    least = None
    for u,a in all_planes:
        slacks = [det(u,minus(w,a)) for w in vertices]
        require(all(s >= 0 for s in slacks), 'feasible vertices')
        require(sum(s == 0 for s in slacks) <= 2, 'support line extreme count')
        require(all(s == 0 or s >= F(1,3*denominator) for s in slacks), 'Cramer positive slack')
        average = det(u,minus(bary,a))
        require(average >= F(k-2,3*denominator*k) >= F(1,9*denominator), 'improved barycenter bound')
        # Squared metric distance avoids a floating sqrt(3).
        require(F(3)*average**2/(4*norm(u)) >= F(1,18*denominator)**2,
                'physical line distance')
        least = average if least is None else min(least,average)
    return least


def grid_stress():
    counts = {}
    trials = 0
    thin = 0
    # A finite regression only; the all-width/all-grid proof is in REVIEW.md.
    translations = ((0,0),(1,0),(-1,2),(1,-2),(4,0),(0,4),
                    (8,0),(2,-1),(-2,1),(7,3))
    for width in (8,19):
        for denominator in (1,33,88):
            old = numeric_planes(width,0,0,(0,0))
            for h in (0,1):
                for k in range(6):
                    for a,b in translations:
                        trials += 1
                        # Nonintegral phases, also near the tip and long sides.
                        t = (F(a*denominator+denominator-1,denominator),
                             F(b*denominator+1,denominator))
                        ps = old+numeric_planes(width,h,k,t)
                        vs = intersection(ps)
                        if len(vs) < 3:
                            thin += 1
                            continue
                        check_vertex_margin(vs,ps,denominator)
                        counts[len(vs)] = counts.get(len(vs),0)+1
    return {'pairs': trials, 'positive_area_by_vertex_count': {str(k):v for k,v in counts.items()},
            'empty_or_zero_area': thin, 'denominators': [1,33,88], 'widths': [8,19]}


def threshold(d):
    require(F(1,18*d) > F(1,1600), 'strict deformation buffer')


def controls():
    rejected = []
    def reject(name, f):
        try:
            f()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Malformed control accepted: '+name)
    reject('wrong upper intrinsic state', lambda: fillers(+1))
    reject('denominator89 licensed by new bound', lambda: threshold(89))
    reject('negative width slope', lambda: endpoint_lower_bound(A(F(100),F(-1)),affine(0),affine(0),F(1,8)))
    reject('unsupported common-point margin', lambda: endpoint_lower_bound(A(F(1,16)),affine(0),affine(0),F(1,8)))
    reject('zero-area polygon passed as positive area', lambda: check_vertex_margin([(F(0),F(0)),(F(1),F(0))],[],1))
    # Positive control: same-state inward interfaces are legal without protection.
    # O and J(O)+(1,-2) have opposite skeleton sides at the entire bottom;
    # the two bowed interfaces are separated by 2/1600 at a unit midpoint.
    require(planes(1,0,point(1,-2))[0][0] == (-1,0), 'unprotected opposite side')
    midpoint = F(1,2)
    gap = 2*F(1,100)*midpoint**2*(1-midpoint)**2
    require(gap == F(1,800), 'inward interface gap')
    return {'malformed_controls_rejected': rejected,
            'unprotected_same_inward_state_midpoint_gap': str(gap)}


def run():
    directions = direction_audit()
    endpoint = fillers()
    obstruction_evidence = obstruction()
    for d in range(1,89):
        threshold(d)
    # k-2 nonzero slacks yields the universal 1/(9d) primitive margin.
    require(all(F(k-2,3*k) >= F(1,9) for k in range(3,9)), 'barycenter vertex ratio')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'status':'EXACT_INDEPENDENT_CONTACT_ARITHMETIC_CONFIRMED',
            'directions':directions,'endpoint_fillers':endpoint,
            'three_copy_obstruction':obstruction_evidence,
            'improved_primitive_slack':'1/(9d)',
            'improved_boundary_distance':'1/(18d)',
            'sufficient_denominators':[1,88], 'worst_margin':'1/1584',
            'profile_displacement':'1/1600','grid_regression':grid_stress(),
            'controls':controls()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected',type=Path)
    args = parser.parse_args()
    result = run()
    if args.expected:
        require(result == json.loads(args.expected.read_text()), 'expected output mismatch')
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
