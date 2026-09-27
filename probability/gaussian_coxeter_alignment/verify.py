#!/usr/bin/env python3
"""Exact finite controls; the uniform analytic theorem is in PROOF.md."""
import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import permutations, product, combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


@dataclass(frozen=True)
class Q:
    """a+b sqrt(2), with exact sign and arithmetic."""
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))

    def __add__(self, x):
        x = coerce(x)
        return Q(self.a+x.a, self.b+x.b)

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b)

    def __sub__(self, x):
        return self + -coerce(x)

    def __rsub__(self, x):
        return coerce(x) + -self

    def __mul__(self, x):
        x = coerce(x)
        return Q(self.a*x.a+2*self.b*x.b, self.a*x.b+self.b*x.a)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = coerce(x)
        den = x.a*x.a-2*x.b*x.b
        require(den != 0, 'division by zero')
        return self * Q(x.a/den, -x.b/den)

    def __rtruediv__(self, x):
        return coerce(x)/self

    def sign(self):
        if self.b == 0:
            return (self.a > 0)-(self.a < 0)
        if self.a == 0:
            return (self.b > 0)-(self.b < 0)
        if (self.a > 0) == (self.b > 0):
            return 1 if self.a > 0 else -1
        d = self.a*self.a-2*self.b*self.b
        require(d != 0, 'rational sqrt(2) contradiction')
        return (1 if self.a > 0 else -1)*(1 if d > 0 else -1)

    def record(self):
        return [str(self.a), str(self.b)]


def coerce(x):
    return x if isinstance(x, Q) else Q(x)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def scale(c, x):
    return tuple(c*a for a in x)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def d2(x, y):
    return dot(sub(x, y), sub(x, y))


def parity(p):
    return (-1)**sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))


def determinant(g):
    p, s = g
    return parity(p)*s[0]*s[1]*s[2]


def act(g, x):
    p, s = g
    return tuple(s[i]*x[p[i]] for i in range(3))


def rank(rows):
    a = [[coerce(x) for x in row] for row in rows]
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c].sign()), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        den = a[r][c]
        a[r] = [x/den for x in a[r]]
        for i in range(r+1, len(a)):
            z = a[i][c]
            if z.sign():
                a[i] = [x-z*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def loss_counts(xs, ys):
    out = {'zero': 0, 'strict': 0, 'expanding': 0}
    for i, j in combinations(range(len(xs)), 2):
        v = (d2(xs[i], xs[j])-d2(ys[i], ys[j])).sign()
        out['zero' if v == 0 else 'strict' if v > 0 else 'expanding'] += 1
    return out


def geometry(W, H):
    a = (Q(1, 2), Q(1, 1), Q(1))
    normals = [(Q(0, F(1, 2)), Q(0, F(-1, 2)), Q()),
               (Q(), Q(0, F(1, 2)), Q(0, F(-1, 2))),
               (Q(), Q(), Q(1))]
    for n in normals:
        require(dot(a, n) == Q(1) and dot(n, n) == Q(1), 'unit wall')
    require(rank(normals) == 3, 'simple roots independent')
    S = dot(a, a)
    require(S == Q(13, 6), 'radius squared')
    m = 2-S
    R, c = Q(3), 1+4/S
    V = [act(h, a) for h in H]
    require(len(set(V)) == 24, 'free rotational orbit')
    require(len({act(w, a) for w in W}) == 48, 'free full orbit')
    require(all(dot(v, v) == S for v in V), 'norm invariance')
    require(all(sum(v[j] for v in V) == Q() for j in range(3)), 'zero centre')
    require(rank(V) == 3, 'full core span')
    require((c-1).sign() > 0 and (R-c).sign() > 0, 'radial order')
    neighbors = {i: [] for i in range(24)}
    for i, u in enumerate(V):
        for j, v in enumerate(V):
            t = dot(u, v)
            require((t-m).sign() >= 0, 'minimum dot product')
            if t == m:
                neighbors[i].append(j)
    require(all(len(v) == 3 for v in neighbors.values()), 'three tight anchors')
    seen, todo = {0}, [0]
    while todo:
        for j in neighbors[todo.pop()]:
            if j not in seen:
                seen.add(j)
                todo.append(j)
    require(len(seen) == 24, 'connected incompatibility graph')
    xs = V + [scale(-R, v) for v in V]
    ys = V + [scale(c, v) for v in V]
    require(len(set(xs)) == len(set(ys)) == 48, 'distinct endpoints')
    counts = loss_counts(xs, ys)
    require(counts == {'zero': 348, 'strict': 780, 'expanding': 0}, 'all pairs')
    for i, v in enumerate(V):
        anchors = [V[j] for j in neighbors[i]]
        require(rank([sub(anchors[1], anchors[0]), sub(anchors[2], anchors[0])]) == 2,
                'anchors are not collinear')
        for u in anchors:
            require(dot(u, v) == m, 'anchor plane')
            require(d2(u, scale(-R, v)) == d2(u, scale(c, v)), 'tight root pair')
        reflected = sub(scale(-R, v), scale(2*(-R*S-m)/S, v))
        require(reflected == scale(c, v), 'exact reflection across anchor plane')
        for j in neighbors[i]:
            gap = d2(scale(-R, v), scale(c, V[j]))-d2(scale(c, v), scale(c, V[j]))
            require(gap == 2*(R+c)*(c-1)*m and gap.sign() < 0, 'mixed choices forbidden')
    paired = [tuple(xs[i])+tuple(ys[i]) for i in range(48)]
    paired_rank = rank([sub(z, paired[0]) for z in paired[1:]])
    require(paired_rank == 6, 'paired affine rank')
    # Increasing c violates the tight cross constraints, even by 1/100.
    corrupt = V + [scale(c+F(1, 100), v) for v in V]
    rejected = loss_counts(xs, corrupt)
    require(rejected['expanding'] == 72, 'corrupted target not rejected')
    # An alternative common-reflection rematching also contracts. Preserve
    # this positive control: labelled indecomposability does not exclude it.
    r = ((0, 1, 2), (1, 1, -1))
    rematched = V + [scale(-c, act(r, v)) for v in V]
    rematched_counts = loss_counts(xs, rematched)
    require(rematched_counts['expanding'] == 0, 'rematching control')
    return dict(group_order=len(W), rotation_order=len(H), sites=48,
                S=S.record(), minimum_dot=m.record(), R=R.record(), c=c.record(),
                pair_counts=counts, tight_cross_pairs=72, anchor_rank=2,
                incompatibility_edges=sum(map(len, neighbors.values()))//2,
                incompatibility_connected_vertices=len(seen), paired_affine_rank=paired_rank,
                binary_solutions_from_connected_graph=2,
                corrupted_target_expanding_pairs=rejected['expanding'],
                tested_common_reflection_expanding_pairs=rematched_counts['expanding'])


def exp_ratio(x, a):
    # gamma_s(x-a)/gamma_s(x), s=1/(2 log 2); x,a integral.
    e = 2*dot(x, a)-dot(a, a)
    require(isinstance(e, int), 'integer Gaussian exponent')
    return F(2)**e


def character_control(W, H):
    a, b, x = (3, 2, 1), (6, 4, 2), (4, 2, 1)
    observations = [act(w, x) for w in W]
    require(len(set(observations)) == 48, 'observation multiplicities')
    r = ((0, 1, 2), (1, 1, -1))
    alpha = F(1, 3)

    def orbit(z, p, sign):
        cloud = [act(h, p) for h in H]
        if sign == -1:
            cloud = [act(r, v) for v in cloud]
        return sum(exp_ratio(z, v) for v in cloud)/len(H)

    def cd(z, p):
        terms = [(determinant(w), exp_ratio(z, act(w, p))) for w in W]
        return (sum(t for _, t in terms)/len(W),
                sum(s*t for s, t in terms)/len(W))

    fs, gs, theta_values = [], [], []
    for z in observations:
        ca, da = cd(z, a)
        cb, db = cd(z, b)
        C0 = alpha*ca+(1-alpha)*cb
        B = alpha*da-(1-alpha)*db
        D = alpha*da+(1-alpha)*db
        f = alpha*orbit(z, a, 1)+(1-alpha)*orbit(z, b, -1)
        g = alpha*orbit(z, a, 1)+(1-alpha)*orbit(z, b, 1)
        require(f == C0+B and g == C0+D, 'character identity')
        require(D and abs(B) < abs(D), 'strict common alternating sign')
        theta = (1+B/D)/2
        require(0 < theta < 1, 'stochastic coefficient')
        rz = act(r, z)
        gr = alpha*orbit(rz, a, 1)+(1-alpha)*orbit(rz, b, 1)
        require(f == theta*g+(1-theta)*gr, 'paired kernel identity')
        theta_values.append(theta)
        fs.append(f)
        gs.append(g)
    require(len(set(theta_values)) == 1, 'orbit-constant coefficient')
    levels = sorted(set([F(0)]+fs+gs))
    gaps = [sum(max(y-q, 0) for y in gs)-sum(max(y-q, 0) for y in fs)
            for q in levels]
    require(all(g >= 0 for g in gaps) and any(g > 0 for g in gaps), 'all orbit hinges')
    require(sum(fs) == sum(gs), 'equal orbit sums')
    _, da = cd(x, a)
    require(da > 0, 'interior positive alternant')
    matrix = [[F(2)**(2*u*v)-F(2)**(-2*u*v) for v in a] for u in x]
    det_sinh = sum(parity(p)*product3(matrix[i][p[i]] for i in range(3))
                   for p in permutations(range(3)))
    require(da == F(2)**(-dot(a, a))*det_sinh/48, 'independent sinh determinant')
    require(cd((3, 3, 1), a)[1] == 0, 'wall cancellation')
    require(cd(act(r, x), a)[1] == -da, 'reflection covariance')
    return dict(observation_points=48, source_density_values=len(set(fs)),
                aligned_density_values=len(set(gs)), tested_hinge_breakpoints=len(levels),
                strict_breakpoints=sum(g > 0 for g in gaps), equal_total=True,
                interior_alternant_positive=True, wall_alternant_zero=True,
                sinh_determinant_identity=True,
                exact_field='rational powers of two')


def product3(values):
    answer = F(1)
    for value in values:
        answer *= value
    return answer


def compute():
    W = [(p, s) for p in permutations(range(3)) for s in product((-1, 1), repeat=3)]
    H = [w for w in W if determinant(w) == 1]
    for p, s in W:
        # Closure checked as actual signed-coordinate matrices.
        for q, t in W:
            composite = (tuple(q[p[i]] for i in range(3)),
                         tuple(s[i]*t[p[i]] for i in range(3)))
            require(composite in W, 'group closure')
            require(determinant(composite) == determinant((p, s))*determinant((q, t)),
                    'determinant character')
    require(Q(-1, 1).sign() == 1 and Q(1, -1).sign() == -1
            and Q(-2, 1).sign() == -1 and Q(2, -1).sign() == 1,
            'quadratic-field signs')
    return dict(status='COXETER_ALIGNMENT_EXACT_CONTROLS_PASS',
                arithmetic='fractions.Fraction and exact Q(sqrt(2)); no floats',
                geometry=geometry(W, H), gaussian_character=character_control(W, H),
                trust_boundary='Finite author controls, not independent review or proof of the analytic kernel input')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='compare complete output to EXPECTED.json')
    args = ap.parse_args()
    result = compute()
    if args.check:
        expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())
        require(result == expected, 'expected record mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
