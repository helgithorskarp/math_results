"""Independent exact J74 contact/path audit; six-reviewer-4.

All coordinates are independently constructed. Radial exposure finds candidates;
complete supporting directed edges prove the silhouette, without author hull
code. Contact weights and motions are untrusted compact inputs. Continuum and
path arguments are ordinary written proofs, not inferred from finite examples.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from geometry import S, construct, as_fields, fdot as dot, fcross as cross, need

HERE = Path(__file__).resolve().parent
ZERO = (S(), S(), S())
R2 = S(11, 4, 4)


def field(pair):
    need(isinstance(pair, list) and len(pair) == 2 and
         all(type(x) is str for x in pair), 'two rational coefficient strings')
    a, b = map(Fraction, pair)
    return S(a.numerator*b.denominator, b.numerator*a.denominator,
             a.denominator*b.denominator)


def vector(x):
    return tuple(x)


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def scale(t, v):
    return tuple(t*x for x in v)


def outer(v):
    return [[x*y for y in v] for x in v]


def matvec(a, v):
    return tuple(dot(r, v) for r in a)


def det(a):
    return dot(a[0], cross(a[1], a[2]))


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[dot(r, c) for c in zip(*b)] for r in a]


def moment(points, weights):
    return [[sum((w*p[i]*p[j] for w, p in zip(weights, points)), S())
             for j in range(3)] for i in range(3)]


def normals():
    phi = S(1, 1, 2)
    return [(S(1), S(), S()), (S(), S(1), S())]+[
        scale(1/(2*phi), (S(1), e*phi, d*(1+phi)))
        for e in (-1, 1) for d in (-1, 1)]


def silhouette(vertices, m):
    projected = [sub(v, scale(dot(v, m), m)) for v in vertices]
    classes = {}
    for i, p in enumerate(projected):
        classes.setdefault(p, []).append(i)
    # This criterion alone does not assert hull completeness. All supporting
    # edges and all60 points are checked independently immediately below.
    corners = sorted(p for p in classes if all(
        dot(p, sub(p, w)) > 0 for w in classes if w != p))
    need(len(corners) == 12, 'twelve radially exposed candidates')
    successor = {}
    for p in corners:
        possible = []
        for q in corners:
            if p == q:
                continue
            inward = cross(m, sub(q, p))
            if (all(dot(inward, sub(w, p)) >= 0 for w in projected) and
                    all(dot(inward, sub(w, p)) > 0 for w in corners if w not in (p, q))):
                possible.append(q)
        need(len(possible) == 1, 'one full-original supporting successor')
        successor[p] = possible[0]
    cycle, p = [], corners[0]
    while p not in cycle:
        cycle.append(p)
        p = successor[p]
    need(p == cycle[0] and len(cycle) == 12, 'complete strict supporting twelve-cycle')
    singletons, pairs, contact, gaps = {}, {}, set(), []
    for p in corners:
        ix = tuple(classes[p])
        height = [dot(vertices[i], m) for i in ix]
        if len(ix) == 1:
            need(height == [S()] and dot(p, p) == R2, 'equatorial singleton original')
            singletons[ix[0]] = p
        else:
            need(len(ix) == 2 and set(height) == {S(1, 0, 2), S(-1, 0, 2)} and
                 dot(p, p) == R2-S(1, 0, 4), 'complete original mirror pair')
            pairs[ix] = p
        contact.update(ix)
        gaps.extend(dot(p, sub(p, vertices[i])) for i in range(60) if i not in ix)
    need((len(singletons), len(pairs), len(contact), len(gaps)) == (4, 8, 20, 700),
         'complete contact classes and radial comparisons')
    need(min(gaps) == S(1, 0, 4), 'sharp complete radial gap one quarter')
    return {'normal': m, 'corners': corners, 'cycle': cycle, 'singletons': singletons,
            'pairs': pairs, 'contacts': contact, 'gaps': gaps}


def weights(record, view):
    need(set(record) == {'axis', 'singletons', 'pairs'}, 'complete stress record fields')
    singles = record['singletons']; pairs = record['pairs']
    need(len(singles) == 4 and len(pairs) == 8, 'all twelve contact weights')
    need(all(type(r['vertex']) is int for r in singles), 'integer original vertex indices')
    si = [r['vertex'] for r in singles]
    pi = [tuple(r['vertices']) for r in pairs]
    need(len(set(si)) == 4 and set(si) == set(view['singletons']), 'complete physical singleton assignment')
    need(len(set(pi)) == 8 and set(pi) == set(view['pairs']), 'complete physical paired assignment')
    beta = [field(r['weight']) for r in singles]
    alpha = [field(r['weight']) for r in pairs]
    need(min(beta+alpha) > S(1, 0, 100), 'strict positive stress weights')
    qs = [view['singletons'][i] for i in si]; ps = [view['pairs'][i] for i in pi]
    need(sum(beta, S()) == 1, 'normalized singleton weights')
    need(all(sum((w*q[i] for w, q in zip(beta, qs)), S()) == 0 for i in range(3)),
         'balanced singleton barycenter')
    M = moment(qs, beta)
    need(M == moment(ps, alpha), 'entrywise physical second-moment equality')
    m = view['normal']
    need(matvec(M, m) == ZERO and sum((M[i][i] for i in range(3)), S()) == R2,
         'plane kernel and physical trace')
    P = [[S(int(i == j))-m[i]*m[j] for j in range(3)] for i in range(3)]
    T = [[M[i][j]-P[i][j]/2 for j in range(3)] for i in range(3)]
    tr = sum((T[i][i] for i in range(3)), S())
    det2 = (tr*tr-sum((T[i][j]*T[j][i] for i in range(3) for j in range(3)), S()))/2
    need(matvec(T, m) == ZERO and tr > 0 and det2 > 0,
         'strict uniform moment lower bound M greater than P/2')
    e = next(e for e in [(S(1), S(), S()), (S(), S(1), S()), (S(), S(), S(1))]
             if dot(cross(m, e), cross(m, e)) > 0)
    u = cross(m, e); v = cross(m, u)
    forms = [(dot(p, u)**2, 2*dot(p, u)*dot(p, v), dot(p, v)**2) for p in ps]
    gram = moment(forms, [S(1)]*8)
    need(det(gram) > 0, 'paired quadratic forms span Sym of plane')
    view.update({'qs': qs, 'ps': ps, 'beta': beta, 'alpha': alpha, 'M': M, 'P': P})
    return {'axis': record['axis'], 'moment_matrix': [[repr(x) for x in r] for r in M],
            'moment_lower_bound': '1/2', 'lower_bound_planar_determinant': repr(det2),
            'dyad_gram_determinant': repr(det(gram)), 'minimum_weight': repr(min(beta+alpha))}


def motions(data, views, vertices):
    need(len(data) == 22, 'complete twenty-two motion records')
    count = [[0]*6 for _ in range(6)]; signatures = set(); matches = comparisons = 0
    identity = [[S(int(i == j)) for j in range(3)] for i in range(3)]
    for item in data:
        i, j = item['source'], item['receiver']
        need(type(i) is type(j) is int and 0 <= i < 6 and 0 <= j < 6, 'proper motion axis indices')
        need(len(item['matrix']) == 3 and all(len(r) == 3 for r in item['matrix']), 'full physical motion matrix')
        Q = [[field(x) for x in r] for r in item['matrix']]
        signature = (i, j, tuple(x for r in Q for x in r))
        need(signature not in signatures, 'unique proper motion record'); signatures.add(signature)
        need(multiply(Q, transpose(Q)) == identity and det(Q) == 1, 'orthogonal proper motion')
        a, b = views[i], views[j]
        moved = {matvec(Q, vertices[k]) for k in a['contacts']}
        target = {vertices[k] for k in b['contacts']}
        need(moved == target and len(moved) == 20, 'twenty shared actual spatial contacts')
        need(matvec(Q, a['normal']) in (b['normal'], scale(-1, b['normal'])), 'proper normal lift')
        for p, q in zip(b['cycle'], b['cycle'][1:]+b['cycle'][:1]):
            inward = cross(b['normal'], sub(q, p))
            need(all(dot(inward, sub(matvec(Q, w), p)) >= 0 for w in vertices),
                 'full moved-original shadow containment')
            comparisons += 60
        count[i][j] += 1; matches += 20
    need(count == [[2, 0, 0, 0, 0, 0], [0, 4, 0, 0, 0, 0]]+[[0, 0, 1, 1, 1, 1]]*4,
         'all proper configuration types covered')
    return {'configuration_count_matrix': count, 'spatial_contact_matches': matches,
            'full_moved_original_support_comparisons': comparisons}


def rotation(axis, t):
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    i, j = (axis+1)%3, (axis+2)%3
    R = [[S(int(a == b)) for b in range(3)] for a in range(3)]
    R[i][i] = R[j][j] = c; R[i][j] = -s; R[j][i] = s
    return R


def literal_controls(views):
    pair_checks = singleton_checks = 0
    for view in views:
        m, P, M = view['normal'], view['P'], view['M']
        for index in range(4):
            A = rotation(index%3, S(1+index, 0, 1600))
            B = rotation((index+1)%3, S(-1-index, 0, 1700))
            L1, L2 = multiply(P, A), multiply(P, B)
            n1, n2 = matvec(transpose(A), m), matvec(transpose(B), m)
            z1, z2 = dot(n1, m), dot(n2, m)
            u1, u2 = sub(n1, scale(z1, m)), sub(n2, scale(z2, m))
            t = scale(S(index-1, 0, 1000000), matvec(P, (S(1), S(1), S())))
            lam = 1+S(index, 0, 1000000)
            for p in view['ps']:
                source = max(dot(s, s) for s in [add(scale(lam, matvec(L1, add(p, scale(sign/2, m)))), t)
                                                 for sign in (S(1), S(-1))])
                target = max(dot(s, s) for s in [matvec(L2, add(p, scale(sign/2, m)))
                                                 for sign in (S(1), S(-1))])
                abs1 = dot(t, matvec(L1, m))-lam*z1*dot(p, u1)
                abs2 = dot(p, u2)
                formula1 = lam*lam*(R2-dot(p, u1)**2-z1*z1/4)+2*lam*dot(t, matvec(L1, p))+dot(t, t)+lam*(abs1 if abs1 >= 0 else -abs1)
                formula2 = R2-dot(p, u2)**2-z2*z2/4+z2*(abs2 if abs2 >= 0 else -abs2)
                need(source == formula1 and target == formula2, 'literal paired maximum-norm identities')
                pair_checks += 2
            residual = S(); main = S()
            for q, beta in zip(view['qs'], view['beta']):
                s, w = add(scale(lam, matvec(L1, q)), t), matvec(L2, q)
                residual += beta*(dot(sub(s, w), sub(s, w))-dot(w, w)+dot(s, s))
                d = sub(scale(lam, matvec(L1, q)), w); main += beta*dot(d, d)
            D = dot(u1, matvec(M, u1))-dot(u2, matvec(M, u2))
            need(residual == main+2*dot(t, t)+(lam*lam-1)*(R2-dot(u1, matvec(M, u1)))-D,
                 'literal aggregate singleton slack identity')
            singleton_checks += 1
    # These deliberately arbitrary frames are algebra controls, not fits.
    return {'arbitrary_frame_examples': 24, 'paired_norm_identities': pair_checks,
            'singleton_slack_identities': singleton_checks}


def constants():
    eta = Fraction(1, 100)
    need(R2 < 5 and S(0, 1) < S(9, 0, 4), 'exact radius rational upper bounds')
    need(1/(1-eta*eta) < Fraction(101, 100) and
         1/(1-eta*eta) < Fraction(101, 100)**2, 'scale and denominator bounds')
    translation = Fraction(45, 4)*Fraction(101, 100)**2
    need(translation < 12, 'uniform quadratic translation coefficient')
    error = 20*eta+10*eta*eta/(1-eta*eta)+54*eta*eta
    need(error < Fraction(1, 4), 'full-class support advantage at one hundredth')
    return {'necessary_constraint_radius': '1/100', 'translation_bound': '12 eta^2',
            'support_error_upper_bound': str(error), 'positive_support_margin': str(Fraction(1, 4)-error)}


def build(inputs):
    need(inputs.get('actual_reviewer') == 'six-reviewer-4' and
         inputs.get('role') == 'independent mathematical reviewer', 'actual reviewer attribution')
    need(S(9, -4) > 0 and S(2, -1) < 0 and S(0, 1)*S(0, 1) == 5,
         'ordered field independent controls')
    raw, _ = construct(); vertices = [as_fields(v, 20) for v in raw]
    need(len(set(vertices)) == 60 and all(dot(v, v) == R2 for v in vertices), 'complete equal-radius model')
    records = inputs['records']
    need(len(records) == 6 and [r['axis'] for r in records] == list(range(6)), 'complete six-axis stress coverage')
    ns = normals(); need(all(dot(m, m) == 1 for m in ns), 'all minimum normals unit')
    views = [silhouette(vertices, m) for m in ns]
    stresses = [weights(r, v) for r, v in zip(records, views)]
    motion_result = motions(inputs['motions'], views, vertices)
    return {'actual_reviewer': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'status': 'PASS', 'vertices': 60, 'six_exact_stresses': stresses,
            'radial_comparisons': sum(len(v['gaps']) for v in views),
            'static_support_comparisons': 6*12*60, 'configuration_motions': motion_result,
            'literal_controls': literal_controls(views), 'proved_constant_checks': constants()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=HERE/'inputs.json')
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = build(json.loads(args.inputs.read_text()))
    if not args.emit:
        need(result == json.loads((HERE/'expected.json').read_text()), 'complete independent expected-record agreement')
    print(json.dumps(result if args.emit else {k: v for k, v in result.items() if k != 'six_exact_stresses'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
