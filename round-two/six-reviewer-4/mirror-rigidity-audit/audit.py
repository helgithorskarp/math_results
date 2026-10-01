"""Independent physical J74 mirror audit, reviewer six-reviewer-4.

Ordered integer-pair arithmetic; no researcher module, hull finder or solver.
All untrusted data are rechecked against an independently constructed body.
The continuum argument and explicit constant propagation are in REVIEW.md.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
from geometry import S, construct, as_fields, fdot as dot, fcross as cross, need

HERE = Path(__file__).resolve().parent
ZERO = (S(), S(), S())
R2 = S(11, 4, 4)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def scale(t, a):
    return tuple(t*x for x in a)


def absolute(x):
    return x if x >= 0 else -x


def ceiling(x):
    need(x >= 0, 'nonnegative ceiling input')
    high = 1
    while S(high) < x:
        high *= 2
    low = 0
    while low < high:
        mid = (low+high)//2
        if S(mid) < x:
            low = mid+1
        else:
            high = mid
    return low


def norm1(v):
    return sum((absolute(x) for x in v), S())


def scalar(text):
    m = re.fullmatch(r'\(([-0-9/]+)\)\+\(([-0-9/]+)\)sqrt5', text)
    need(m is not None, 'literal ordered quadratic-field scalar')
    return pair([m[1], m[2]])


def pair(xs):
    need(len(xs) == 2 and all(isinstance(x, str) for x in xs), 'two rational strings')
    a, b = map(Fraction, xs)
    return S(a.numerator*b.denominator, b.numerator*a.denominator,
             a.denominator*b.denominator)


def vec(xs):
    need(len(xs) == 3, 'three physical coordinates')
    return tuple(scalar(x) for x in xs)


def axes():
    phi = S(1, 1, 2)
    return [(S(1), S(), S()), (S(), S(1), S())]+[
        scale(1/(2*phi), (S(1), e*phi, d*(1+phi)))
        for e in (-1, 1) for d in (-1, 1)]


def project(v, m):
    return sub(v, scale(dot(v, m), m))


def det(a):
    return dot(a[0], cross(a[1], a[2]))


def inverse(a):
    determinant = det(a)
    need(determinant != 0, 'nonsingular common triple')
    out = []
    for i in range(3):
        row = []
        for j in range(3):
            minor = [[a[r][c] for c in range(3) if c != i]
                     for r in range(3) if r != j]
            row.append(((-1)**(i+j)) *
                       (minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0])/determinant)
        out.append(row)
    need(all(sum((out[i][k]*a[k][j] for k in range(3)), S()) == S(i == j)
             for i in range(3) for j in range(3)), 'literal inverse product')
    return out


def matvec(a, v):
    return tuple(dot(row, v) for row in a)


def unique_indices(xs, size=60):
    need(all(type(i) is int and 0 <= i < size for i in xs)
         and len(set(xs)) == len(xs), 'distinct valid original indices')
    return xs


def tangent_basis(m):
    e = next(project(v, m) for v in [(S(1), S(), S()),
                                    (S(), S(1), S()), (S(), S(), S(1))]
             if dot(project(v, m), project(v, m)) > 0)
    return e, cross(m, e)


def polar_cycle(rays, m):
    need(len(set(rays)) == len(rays) and len(rays) >= 3, 'distinct nontrivial polar cycle')
    e, f = tangent_basis(m)
    positive_axis_crossings = 0
    margins = []
    for a, b in zip(rays, rays[1:]+rays[:1]):
        margin = dot(m, cross(a, b))
        need(margin > 0, 'each directed cone width lies strictly between zero and pi')
        margins.append(margin)
        ya, yb = dot(f, a), dot(f, b)
        # Each positive-axis crossing belongs to a unique half-open arc.
        if ya <= 0 < yb:
            need(dot(e, a)*yb-dot(e, b)*ya > 0, 'actual positive-axis crossing')
            positive_axis_crossings += 1
    need(positive_axis_crossings == 1, 'exactly one full winding, including walls and wrap')
    return min(margins)


def boundary_record(record, vertices, m):
    corners = unique_indices(record['corner_original_indices'])
    need(len(corners) == 12, 'twelve complete strict convex corners')
    declared = set(unique_indices(record['boundary_original_indices']))
    actual = set()
    corner_preimages = set()
    gamma2 = S(3, -1, 8)
    supports = interior = 0
    distance_minimum = None
    for a, b in zip(corners, corners[1:]+corners[:1]):
        edge = sub(vertices[b], vertices[a])
        inward = cross(m, edge)
        need(dot(inward, inward) > 0, 'nonzero projected polygon edge')
        need(all(dot(inward, sub(vertices[i], vertices[a])) > 0
                 for i in corners if i not in (a, b)), 'strict convex cyclic polygon')
        for i, v in enumerate(vertices):
            value = dot(inward, sub(v, vertices[a]))
            need(value >= 0, 'all actual originals inside complete supporting polygon')
            supports += 1
            if value == 0:
                actual.add(i)
            if i not in declared:
                need(value > 0, 'every omitted original strictly interior')
                distance2 = value*value/dot(inward, inward)
                need(distance2 >= gamma2, 'physical squared supporting-line clearance')
                interior += 1
                distance_minimum = distance2 if distance_minimum is None else min(distance_minimum, distance2)
        corner_preimages.update(i for i, v in enumerate(vertices)
                                if project(v, m) == project(vertices[a], m))
    need(actual == declared and len(actual) == 28 and len(corner_preimages) == 20,
         'complete twenty corner preimages plus eight edge-interior originals')
    need(distance_minimum == gamma2, 'sharp physical clearance')
    reflected = [sub(vertices[i], scale(2*dot(vertices[i], m), m)) for i in actual]
    need(set(reflected) == {vertices[i] for i in actual}, 'all twenty-eight actual prototype reflections')
    equator = [vertices[i] for i in actual if dot(vertices[i], m) == 0]
    need(any(det([sub(equator[j], equator[0]), sub(equator[k], equator[0]),
                  sub(vertices[i], equator[0])]) != 0
             for j, k in combinations(range(1, len(equator)), 2) for i in actual),
         'full spatial affine dimension of prototype')
    full_body_reflection = all(sub(v, scale(2*dot(v, m), m)) in vertices for v in vertices)
    return {'axis': record['axis'], 'boundary': sorted(actual), 'supports': supports,
            'interior_distances': interior, 'full_body_reflection': full_body_reflection}


def profile(record, vertices, m, boundary):
    need(record['axis'] in (0, 1, 2) and dot(m, m) == 1, 'marked representative and physical unit normal')
    qix = unique_indices(record['equatorial_original_indices'])
    need(set(qix) == {i for i, v in enumerate(vertices) if dot(v, m) == 0}
         and len(qix) == 4, 'all actual equatorial originals')
    beta = [pair(p) for p in record['equatorial_weights']]
    need(len(beta) == 4 and min(beta) > 0 and sum(beta, S()) == 1, 'positive singleton stress')
    need(tuple(sum((b*vertices[i][j] for b, i in zip(beta, qix)), S())
               for j in range(3)) == ZERO, 'literal singleton barycenter')
    e, f = tangent_basis(m)
    need(any(dot(m, cross(vertices[i], vertices[j])) != 0 for i, j in combinations(qix, 2)),
         'actual positive stress spans physical plane')
    moment = [[sum((b*vertices[i][j]*vertices[i][k] for b, i in zip(beta, qix)), S())
               for k in range(3)] for j in range(3)]
    A = [[S(j == k)-m[j]*m[k]-moment[j][k]/R2 for k in range(3)] for j in range(3)]
    need(sum((moment[j][j] for j in range(3)), S()) == R2, 'physical common moment trace')
    planar_det = (S(1)-sum((A[j][k]*A[k][j] for j in range(3) for k in range(3)), S()))/2
    need(planar_det > 0, 'positive planar bilinear determinant')
    def ray(xs):
        v = vec(xs)
        need(dot(m, v) == 0 and norm1(v) == 1, 'physical normalized tangent ray')
        return v
    rays = [ray(xs) for xs in record['receiver_wall_rays']]
    winding_margin = polar_cycle(rays, m)
    need(len(record['fans']) == len(rays) and
         [x['interval'] for x in record['fans']] == [[i, (i+1) % len(rays)] for i in range(len(rays))],
         'every literal closed arc exactly covered')
    fans = []
    for ix, fan in enumerate(record['fans']):
        need(len(fan['original_edges']) == 16 and
             len({tuple(x) for x in fan['original_edges']}) == 16, 'sixteen distinct actual directed edges')
        ds = [rays[i] for i in fan['interval']]
        rows = []
        h_inv_max = S()
        support_checks = 0
        for edge in fan['original_edges']:
            a, b = unique_indices(edge)
            need(a in boundary and b in boundary, 'actual prototype endpoint contacts')
            delta = sub(vertices[b], vertices[a])
            need(dot(delta, delta) == 1, 'literal original unit edge')
            h = dot(cross(delta, m), vertices[a])
            need(h > 0, 'positive fixed support normalization')
            h_inv_max = max(h_inv_max, 1/h)
            for d in [ZERO, *ds]:
                u = add(m, scale(S(1, 0, 100), d))
                normal = cross(delta, u)
                need(dot(normal, u) == dot(normal, delta) == 0
                     and dot(normal, vertices[a]) > 0, 'actual support normal perpendicular to edge and receiver')
                for v in vertices:
                    need(dot(normal, sub(vertices[a], v)) >= 0, 'literal original oriented support determinant')
                    support_checks += 1
            m0 = scale(1/h, cross(delta, m))
            for source in edge:
                need(dot(m0, vertices[source]) == 1, 'actual base contact')
                rows.append({'source': source, 'normal': m0, 'torque': cross(vertices[source], m0),
                             'k': dot(delta, m)/h})
        common = []
        for i, b in zip(qix, beta):
            rr = [row for row in rows if row['source'] == i]
            need(len(rr) == 2 and dot(m, cross(rr[0]['normal'], rr[1]['normal'])) != 0,
                 'two independent actual support lines at singleton')
            difference = sub(rr[0]['normal'], rr[1]['normal'])
            radial = scale(1/R2, vertices[i])
            theta = dot(sub(radial, rr[1]['normal']), difference)/dot(difference, difference)
            need(0 < theta < 1 and
                 add(scale(theta, rr[0]['normal']), scale(1-theta, rr[1]['normal'])) == radial,
                 'positive exact radial decomposition')
            common += [(rr[0], b*theta), (rr[1], b*(1-theta))]
        weights = [w for _, w in common]
        need(min(weights) > 0 and sum(weights, S()) == 1, 'all common weights positive and normalized')
        need(all(sum((w*row[key][j] for row, w in common), S()) == 0
                 for key in ['normal', 'torque'] for j in range(3)), 'physical common balances')
        need(all(project(row['torque'], m) == ZERO for row, _ in common), 'common rows independent of tilt')
        stress = [[sum((w*vertices[row['source']][j]*row['normal'][k] for row, w in common), S())
                   for k in range(3)] for j in range(3)]
        need(stress == [[x/R2 for x in row] for row in moment], 'all physical common moment entries')
        linear = [(dot(row['torque'], m), dot(row['normal'], e), dot(row['normal'], f))
                  for row, _ in common]
        # Maximal determinant differs from the producer's first-nonzero triple.
        triple = max(combinations(range(8), 3), key=lambda t: absolute(det([linear[i] for i in t])))
        inv = inverse([linear[i] for i in triple])
        K0 = ceiling(3*max(sum((absolute(inv[i][j]) for i in range(3)), S())
                          for j in range(3))/min(weights))
        aa = [ray(xs) for xs in fan['critical_tilt_rays']]
        need(dot(m, cross(*aa)) != 0 and
             all(dot(row['torque'], a) <= 0 for row in rows for a in aa), 'all physical critical inequalities')
        facets = []
        for j in range(2):
            options = [-dot(row['torque'], aa[j]) for row in rows
                       if dot(row['torque'], aa[1-j]) == 0]
            need(options and max(options) > 0, 'actual complete critical cone facet')
            facets.append(max(options))
        corners = [dot(a, matvec(A, b)) for a in aa for b in aa]
        need(min(corners) > S(1, 0, 20), 'all acute bilinear corners')
        B = tuple(sum((w*row['k']*vertices[row['source']][j] for row, w in common), S())
                  for j in range(3))
        Kc = sum((w*row['k'] for row, w in common), S())
        fans.append({'fan': ix, 'supports': support_checks, 'corners': list(map(str, corners)),
                     'B': list(map(str, B)), 'Kc': str(Kc), 'N': ceiling(h_inv_max),
                     'coercivity_K0': K0, 'facet_inverse': ceiling(1/min(facets)),
                     'B_norm_upper': ceiling(norm1(B)), 'Kc_abs_upper': ceiling(absolute(Kc)),
                     'chosen_maximal_det_triple': list(triple)})
    return {'axis': record['axis'], 'fans': fans, 'moment': [[str(x) for x in row] for row in moment],
            'planar_det': str(planar_det), 'winding_inverse': ceiling(1/winding_margin)}


def constants(profiles):
    fans = [f for p in profiles for f in p['fans']]
    N = max(f['N'] for f in fans)
    K0 = max(f['coercivity_K0'] for f in fans)
    A0 = 18*K0*N
    B0 = 4*A0+2
    J0 = (4*A0+9)*N*max(f['facet_inverse'] for f in fans)
    E0 = A0+2*J0
    C0 = (E0+9)//10+40*J0
    X = max(f['B_norm_upper'] for f in fans)
    Y = max(f['Kc_abs_upper'] for f in fans)
    H = 2*C0+1+2*X+5*B0*X+B0+B0*B0*(1+X)+4*Y*B0
    # Also fits every actual support triangle and the credited prototype cap.
    D0 = max(4, 2*K0*N, 2*E0, 2*J0, 40*H, 10000,
             200*max(p['winding_inverse'] for p in profiles))
    need(D0 >= 40*H and D0 >= 2*E0 and D0 >= 2*K0*N, 'literal perturbation absorption')
    return {'N': N, 'K0': K0, 'A0': A0, 'B0': B0, 'J0': J0, 'E0': E0,
            'C0': C0, 'X': X, 'Y': Y, 'H': H, 'D0': D0,
            'kappa_upper': '1/'+str(D0), 'local_input_r_eta_upper': '1/'+str(4*D0),
            'bilinear_coefficient_lower': '1/40',
            'scope': 'Both receiver tangent r and relative Cayley vector w bounded; not an all-source receiving radius.'}


def run(inputs, controls=True):
    vertices = [as_fields(v, 20) for v in construct()[0]]
    need(len(vertices) == len(set(vertices)) == 60 and all(dot(v, v) == R2 for v in vertices),
         'independent common-sphere model')
    shadow_gap = S(3, -1, 8)-4*R2*S(2, 0, 29)**2
    need(shadow_gap == S(2171, -969, 6728) and shadow_gap > 0
         and 2171**2-5*969**2 == 18436,
         'enlarged closed shadow-reduction cap')
    mm = axes()
    boundary = [boundary_record(record, vertices, m)
                for record, m in zip(inputs['boundary_profiles'], mm)]
    need(len(boundary) == 6 and [x['axis'] for x in boundary] == list(range(6)),
         'all marked shadow prototypes')
    need([x['full_body_reflection'] for x in boundary] == [True, True, False, False, False, False],
         'mixed reflection is only a prototype symmetry')
    motion_matches = 0
    receiver_counts = [0]*6
    distinct_motions = set()
    for motion in inputs['motions']:
        a, b = motion['source_axis'], motion['receiver_axis']
        columns = [vec(x) for x in motion['proper_matrix_columns']]
        matrix = list(zip(*columns))
        marked_matrix = (b, tuple(columns))
        need(marked_matrix not in distinct_motions, 'distinct proper catalogue matrices for each receiver')
        distinct_motions.add(marked_matrix)
        need(all(dot(columns[i], columns[j]) == S(i == j) for i in range(3) for j in range(3))
             and det(matrix) == 1, 'actual proper original catalogue motion')
        need(matvec(matrix, mm[a]) == scale(motion['direction'], mm[b]), 'marked normal transport')
        source = {matvec(matrix, vertices[i]) for i in boundary[a]['boundary']}
        target = {vertices[i] for i in boundary[b]['boundary']}
        need(source == target, 'all actual spatial boundary preimages transported')
        motion_matches += len(source)
        receiver_counts[b] += 1
    need(motion_matches == 616 and receiver_counts == [2, 4, 4, 4, 4, 4],
         'complete credited twenty-two catalogue transports')
    profiles = [profile(record, vertices, mm[j], set(boundary[j]['boundary']))
                for j, record in enumerate(inputs['profiles'])]
    need(len(profiles) == 3 and [len(p['fans']) for p in profiles] == [18, 12, 16],
         'all forty-six closed physical cones')
    rejected = 0
    if controls:
        damaged = []
        z = copy.deepcopy(inputs['profiles'][0]); z['fans'].pop(); damaged.append(z)
        z = copy.deepcopy(inputs['profiles'][0]); z['equatorial_weights'][0] = ['-1', '0']; damaged.append(z)
        z = copy.deepcopy(inputs['profiles'][0])
        z['fans'][0]['critical_tilt_rays'][0] = [str(-scalar(x)) for x in z['fans'][0]['critical_tilt_rays'][0]]
        damaged.append(z)
        z = copy.deepcopy(inputs['profiles'][0]); z['fans'][0]['original_edges'][0][1] = z['fans'][0]['original_edges'][0][0]
        damaged.append(z)
        for z in damaged:
            try:
                profile(z, vertices, mm[0], set(boundary[0]['boundary']))
            except ValueError:
                rejected += 1
            else:
                raise ValueError('damaged contact hypothesis accepted')
        z = copy.deepcopy(inputs['boundary_profiles'][0])
        corner_preimages = {i for i, v in enumerate(vertices)
                            if any(project(v, mm[0]) == project(vertices[j], mm[0])
                                   for j in z['corner_original_indices'])}
        z['boundary_original_indices'] = sorted(corner_preimages)
        try:
            boundary_record(z, vertices, mm[0])
        except ValueError:
            rejected += 1
        else:
            raise ValueError('edge-interior preimages incorrectly omitted')
    return {'actual_reviewer': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
            'original_vertices': 60, 'boundary_supports': sum(x['supports'] for x in boundary),
            'boundary_interior_distances': sum(x['interior_distances'] for x in boundary),
            'prototype_reflections': 168, 'catalogue_boundary_matches': motion_matches,
            'closed_cones': 46, 'all_original_contact_supports': sum(f['supports'] for p in profiles for f in p['fans']),
            'bilinear_corner_checks': 184, 'negative_controls_rejected': rejected,
            'closed_shadow_reduction_chord_radius': '2/29',
            'enlarged_squared_support_gap': str(shadow_gap),
            'constants': constants(profiles), 'profiles': profiles}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = run(json.loads((HERE/'inputs.json').read_text()))
    if args.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        need(result == json.loads((HERE/'expected.json').read_text()), 'complete independently expected record')
        print('PASS')
