#!/usr/bin/env python3
"""Exact finite hypotheses for all-source RID fivefold closed-fit rigidity.

Replay the hash-pinned complete original hull/brightness certificate, identify
the second polar orbit, derive the contact ring and its moments from originals,
and verify every positive-root/normal/roll inequality used in PROOF.md.
No floating arithmetic, sampled passage search, solver or private dataset.
"""
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_dependency():
    record = json.loads((HERE/'DEPENDENCIES.json').read_text())
    directory = (HERE/record['directory']).resolve()
    require(set(record['sha256']) == {'field.py', 'verify.py', 'expected.json', 'PROOF.md'},
            'dependency fingerprint list differs')
    for name, expected in record['sha256'].items():
        require(hashlib.sha256((directory/name).read_bytes()).hexdigest() == expected,
                'dependency source changed: '+name)
    require('field' not in sys.modules, 'unexpected preloaded arithmetic module')
    sys.path.insert(0, str(directory))
    spec = spec_from_file_location('rid_brightness_dependency', directory/'verify.py')
    base = module_from_spec(spec)
    spec.loader.exec_module(base)
    require(Path(sys.modules['field'].__file__).resolve() == directory/'field.py',
            'arithmetic import did not use the verified source')
    output = json.dumps(base.verify(), indent=2, sort_keys=True)+'\n'
    require(output == (directory/'expected.json').read_text(),
            'prior original hull/brightness certificate did not replay')
    return base, record


def project(base, v, w):
    return tuple(v[i]-w[i]*base.dot(w, v)/base.dot(w, w) for i in range(3))


def contact_geometry(base, V, ring, w):
    F, PHI, ZERO, ONE, dot = base.F, base.PHI, base.ZERO, base.ONE, base.dot
    require(len(ring) == len(set(ring)) == 10 and all(v in V for v in ring),
            'ten distinct actual contact originals required')
    s = dot(w, w)
    p2 = (7-4*PHI)/5
    D2 = (28+44*PHI)/5
    require(s == PHI+2 and min(dot(w, v)**2/s for v in V) == p2,
            'receiving minimum height differs')
    require(set(ring) == {v for v in V if dot(w, v)**2/s == p2},
            'contact ring is not the complete minimum-height set')
    require({dot(w, v) for v in ring} == {PHI-1, 1-PHI},
            'contact heights do not have the required two signs')
    require(all(dot(project(base, v, w), project(base, v, w)) == D2 for v in ring),
            'contact projected radii differ')
    require(all(dot(v, v) == D2+p2 == 7+8*PHI for v in V),
            'common original radii differ')
    q = {v:project(base, v, w) for v in ring}
    signed_sum = tuple(sum((dot(w, v).sign()*q[v][i] for v in ring), ZERO)
                       for i in range(3))
    require(signed_sum == (ZERO, ZERO, ZERO), 'signed projected contact sum is not zero')
    Pi = tuple(tuple(F(int(i == j))-w[i]*w[j]/s for j in range(3)) for i in range(3))
    qcov = tuple(tuple(sum((q[v][i]*q[v][j] for v in ring), ZERO)
                       for j in range(3)) for i in range(3))
    require(qcov == tuple(tuple(5*D2*Pi[i][j] for j in range(3)) for i in range(3)),
            'projected contact covariance is not isotropic')
    covariance = tuple(tuple(sum((v[i]*v[j] for v in ring), ZERO)
                             for j in range(3)) for i in range(3))
    require(covariance == tuple(tuple(5*D2*Pi[i][j]+10*p2*w[i]*w[j]/s
                                     for j in range(3)) for i in range(3)),
            'full contact covariance differs')
    require(D2 > 2*p2 > ZERO, 'contact covariance eigenvalue order fails')
    require(any(dot(a, base.cross(b, c)) != ZERO for a, b, c in combinations(ring, 3)),
            'contact originals do not span three-space')
    gaps = [dot(q[v], base.sub(q[v], project(base, t, w)))
            for v in ring for t in V if t != v]
    m = (4+2*PHI)/5
    require(len(gaps) == 590 and min(gaps) == m and m > F(Q(7, 5)),
            'complete singleton radial support gap fails')
    inner_gap = min(D2-dot(project(base, v, w), project(base, v, w))
                    for v in V if v not in ring)
    require(inner_gap == (-4+8*PHI)/5 and inner_gap > F(Q(7, 4)),
            'other original squared projected radius gap fails')
    raw, hull_size = base.direct_shadow_raw(V, w)
    require(hull_size == 10 and raw*raw/s == 940+1520*PHI,
            'independent original projected hull has wrong area or corners')
    return dict(contact_originals=10, projected_hull_corners=hull_size,
                minimum_height_squared=p2.encode(), projected_ring_radius_squared=D2.encode(),
                radial_support_comparisons=len(gaps), singleton_radial_support_gap=m.encode(),
                other_original_squared_radius_gap=inner_gap.encode(),
                signed_contact_sum='zero', projected_contact_covariance='5 D^2 Pi',
                full_contact_covariance='5 D^2 Pi + 10 p^2 e e^t',
                contact_span_dimension=3), Pi


def orbit_and_roll(base, V, ring, w, C, G):
    F, PHI, ZERO, ONE = base.F, base.PHI, base.ZERO, base.ONE
    s = base.dot(w, w)
    axes = {base.ray(base.cross(c, d)) for c, d in combinations(C, 2)
            if base.cross(c, d) != (ZERO, ZERO, ZERO)}
    require(len(axes) == 121, 'complete polar normal set differs')
    second = {r for r in axes if base.brightness_raw(C, r)**2/base.dot(r, r)
              == 940+1520*PHI}
    orbit = {base.act(g, w) for g in G}
    require(len(orbit) == 12 and len(second) == 6 and
            {base.ray(n) for n in orbit} == second,
            'second polar level is not the complete proper fivefold orbit')
    I = ((ONE, ZERO, ZERO), (ZERO, ONE, ZERO), (ZERO, ZERO, ONE))
    W = ((ZERO, -ONE, PHI), (ONE, ZERO, ZERO), (-PHI, ZERO, ZERO))
    T = tuple(tuple((PHI-1)*I[i][j]/2+(2-PHI)*w[i]*w[j]/2+W[i][j]/2
                    for j in range(3)) for i in range(3))
    arithmetic = sys.modules['field']
    require(T in G and base.act(T, w) == w and arithmetic.determinant(T) == ONE,
            'proper fivefold stabilizer generator fails')
    powers = [I]
    for _ in range(4): powers.append(arithmetic.matmul(T, powers[-1]))
    require(len(set(powers)) == 5 and arithmetic.matmul(T, powers[-1]) == I,
            'proper stabilizer does not have order five')
    anchor = ring[0]
    images = {tuple(sigma*x for x in project(base, base.act(t, anchor), w))
              for sigma, t in product((-1, 1), powers)}
    require(len(images) == 10 and images == {project(base, v, w) for v in ring},
            'proper fivefold turns plus antipodal planar sign do not exhaust the ring')
    require(all(base.dot(n, n) == s for n in orbit), 'directed orbit normals not equal length')
    D2 = (28+44*PHI)/5
    q = project(base, anchor, w)
    require(base.dot(q, project(base, base.act(T, anchor), w))/D2 == (PHI-1)/2,
            'stabilizer does not turn the contact plane through 72 degrees')
    require(max(base.dot(q, t)/D2 for t in images if t != q) == PHI/2,
            'regular decagon nearest-neighbor angle is not 36 degrees')
    return dict(projective_fivefold_axes=6, directed_fivefold_axes=12,
                complete_second_axis_sha256=base.digest(
                    [base.encode(r) for r in sorted(second, key=base.key)]),
                proper_roll_lifts=10, planar_proper_ring_symmetry='C10',
                proper_body_group_order=len(G))


def tangent_geometry(base, C, w):
    F, PHI, ZERO = base.F, base.PHI, base.ZERO
    s = base.dot(w, w)
    raw = base.brightness_raw(C, w)
    D = [c for c in C if base.dot(c, w) == ZERO]
    E = [c for c in C if base.dot(c, w) != ZERO]
    require(len(D) == 5 and len(E) == 26, 'fivefold area-generator partition differs')
    signed = tuple(sum((base.dot(c, w).sign()*c[i] for c in E), ZERO) for i in range(3))
    require(raw == 30+50*PHI and
            all(signed[i]*s == raw*w[i] for i in range(3)),
            'nonzero signed area-vector sum is not A1 e')
    distances = []
    for c in D:
        r = base.cross(w, c)
        value = base.brightness_raw(D, r)
        distances.append(value*value/base.dot(r, r))
    rho2 = 48+64*PHI
    require(min(distances) == rho2 and rho2 > 144,
            'complete tangent inradius is not greater than twelve')
    endpoints = [tuple(sum((sign*c[i] for sign, c in zip(signs, D)), ZERO)
                       for i in range(3)) for signs in product((-1, 1), repeat=5)]
    maximum = max(base.dot(v, v) for v in endpoints)
    require(len(endpoints) == 32 and maximum == 64+64*PHI and maximum < 169,
            'complete tangent circumradius is not below thirteen')
    stability = min(base.dot(c, w)**2/(s*base.dot(c, c)) for c in E)
    require(stability > F(Q(1, 100)**2), 'receiving signs not stable to chord 1/100')
    return dict(tangent_generator_count=len(D), nonzero_area_generator_count=len(E),
                tangent_inradius_squared=rho2.encode(), tangent_inradius_lower='12',
                tangent_endpoint_combinations=len(endpoints),
                tangent_circumradius_squared=maximum.encode(), tangent_circumradius_upper='13',
                normalized_nonzero_dot_squared_minimum=stability.encode(),
                receiving_sign_stability_chord='1/100')


def local_gates(base, h=Q(1, 60)):
    F, PHI = base.F, base.PHI
    p2, D2, R2 = (7-4*PHI)/5, (28+44*PHI)/5, 7+8*PHI
    m = (4+2*PHI)/5
    require(0 < h < 1 and 80*h+40*h*h < Q(7, 5),
            'local radial support upper bound fails')
    require(4*R2*h+2*R2*h*h < m, 'local singleton support advantage fails')
    require(p2*(1-h*h) > D2*h*h, 'contact axial signs can change')
    require(D2 > 2*p2 > 0, 'local moment eigenvalue order fails')
    return dict(local_full_frame_radius=str(h),
                rational_local_radial_error_upper=str(80*h+40*h*h),
                contact_sign_condition='p^2(1-h^2) > D^2 h^2')


def cap_gates(base, delta=Q(1, 1500)):
    F, PHI, ZERO, ONE = base.F, base.PHI, base.ZERO, base.ONE
    A0, A1sq, A2sq = 12+28*PHI, 940+1520*PHI, 960+1536*PHI
    rho2, rho5sq = F('288/5', '464/5'), 48+64*PHI
    p2, D2, R2 = (7-4*PHI)/5, (28+44*PHI)/5, 7+8*PHI
    require(0 < delta <= Q(1, 100), 'receiving cap outside sign-stability interval')
    require(F(Q(81, 250)**2) < p2 < F(Q(1, 3)**2),
            'positive receiver height root bounds fail')
    require(F(Q(22, 5)**2) < D2 < R2 < F(20) < F(Q(9, 2)**2),
            'positive original/projected radius bounds fail')
    eta = 13*delta
    upper = Q(175, 3)+eta
    require(F(58**2) < A1sq < F(Q(175, 3)**2) and
            upper < Q(117, 2) and F(Q(117, 2)**2) < A2sq,
            'area budget does not separate the third polar level')
    # Any original centered closed fit has f(source)>=f(receiver).
    lower_f = Q(321, 1000)
    require(Q(81, 250)-Q(9, 2)*delta >= lower_f,
            'receiving minimum-height budget is too weak')
    rstar = Q(11, 125)
    require(2+PHI < F(Q(29, 8)) and lower_f > Q(29, 8)*rstar,
            'twofold equatorial originals do not force r>rstar')
    rmax2 = ONE-A0*A0/(upper*upper)
    require(0 < rstar*rstar < rmax2 < rho2/(A0*A0+rho2),
            'twofold tangent lower function is not increasing on its whole interval')
    comparison = upper*upper-A0*A0*(1-rstar*rstar)-rho2*rstar*rstar
    margin = 4*A0*A0*rho2*rstar*rstar*(1-rstar*rstar)-comparison*comparison
    require(comparison > ZERO and margin > ZERO,
            'twofold area/radius contradiction positive-root certificate fails')
    # Remaining polar maximum is at the complete fivefold orbit.
    require(2*eta/58 < Q(1, 30)**2,
            'fivefold polar initial chord not below 1/30')
    require(rho5sq > 12**2 and Q(999, 1000)**2 < 1-Q(1, 30)**2/4 and
            12*Q(999, 1000)-Q(59, 60) > 11,
            'fivefold global tangent coercivity not above eleven')
    source = eta/11
    # Generic drift first forces the supporting original into the true ring.
    require(3*source+20*source*source+40*delta < Q(7, 4),
            'outside-ring original can pass the original support test')
    # A ring original has |height|=p; shortest transport drift is
    # <=p*d + D*d^2/2. All root bounds are positive and independently checked.
    square_error = 3*(source+delta)+20*source*source+Q(81, 4)*delta*delta
    root = Q(1, 15)
    require(square_error < root*root, 'ring support matching positive-root gate fails')
    source_point_drift = source/3+Q(9, 4)*source*source
    roll = Q(5, 22)*(root+source_point_drift)
    full = source+roll
    require(full < Q(1, 60) and delta < Q(1, 60),
            'arbitrary proper roll reduction exceeds the local frame radius')
    return dict(receiver_chord_radius=str(delta), receiver_area_excess_upper=str(eta),
                receiver_area_rational_upper=str(upper), receiver_minimum_height_lower=str(lower_f),
                twofold_source_tangent_lower=str(rstar),
                twofold_source_tangent_squared_upper=rmax2.encode(),
                twofold_positive_root_comparison=comparison.encode(),
                twofold_positive_squared_margin=margin.encode(),
                fivefold_initial_source_chord_upper='1/30',
                fivefold_linear_coercivity_lower='11', source_chord_upper=str(source),
                ring_support_squared_error_upper=str(square_error),
                ring_support_error_root_upper=str(root),
                source_original_transport_error_upper=str(source_point_drift),
                proper_roll_operator_upper=str(roll), full_source_frame_operator_upper=str(full))


def negative_controls(base, V, ring, w):
    cases = [lambda:contact_geometry(base, V, ring[:-1], w),
             lambda:contact_geometry(base, V, ring[:-1]+[ring[0]], w),
             lambda:cap_gates(base, Q(1, 1000)),
             lambda:local_gates(base, Q(1, 50))]
    rejected = 0
    for case in cases:
        try:
            case()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed or out-of-budget control accepted')
    require(rejected == 4, 'negative controls incomplete')
    return rejected


def verify():
    base, dependency = load_dependency()
    V = base.vertices()
    w = (base.ZERO, base.PHI, base.ONE)
    s = base.dot(w, w)
    p2 = (7-4*base.PHI)/5
    ring = [v for v in V if base.dot(w, v)**2/s == p2]
    contacts, Pi = contact_geometry(base, V, ring, w)
    planes, _ = base.complete_facets(V)
    C, face_records, _ = base.area_generators(V, planes)
    previous = json.loads(((HERE/dependency['directory'])/'expected.json').read_text())
    require(base.digest(face_records) == previous['facet_record_sha256'],
            'fresh physical facet vectors disagree with the replayed originals')
    G = base.proper_group(V)
    orbit = orbit_and_roll(base, V, ring, w, C, G)
    tangent = tangent_geometry(base, C, w)
    local = local_gates(base)
    cap = cap_gates(base)
    return dict(agent='six-rupert-3', role='researcher',
                proof_status='written_geometric_proof_with_exact_finite_hypotheses',
                global_RID_Rupert_status='unresolved', arithmetic='Q(phi), exact rational signs',
                dependency_commit=dependency['source_commit'], dependency_graph=dependency['graph_ref'],
                dependency_replay='every byte of prior expected.json regenerated',
                reference_axis=base.encode(w),
                physical_projection_matrix=[base.encode(row) for row in Pi],
                closed_fit_classification='lambda=1, t=0, B1=sigma B2 g; sigma=+/-1, g in proper G',
                source_roll_premise='arbitrary proper roll; bound derived from actual originals',
                malformed_controls_rejected=negative_controls(base, V, ring, w),
                **contacts, **orbit, **tangent, **local, **cap)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    output = json.dumps(verify(), indent=2, sort_keys=True)+'\n'
    if not args.emit:
        require(output == (HERE/'expected.json').read_text(), 'regenerated new expected record differs')
    print(output, end='')


if __name__ == '__main__':
    main()
