#!/usr/bin/env python3
"""Exact finite hypotheses for the larger RID receiving caps in PROOF.md.

Replay the hash-pinned prior geometric certificate; then derive new tangent
upper bounds, sign stability, extended polar budgets and quadratic roll gates.
No floating-point decisions, solver, sampled passage search or private data.
"""
import argparse
from fractions import Fraction as Q
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_dependency():
    record = json.loads((HERE / 'DEPENDENCIES.json').read_text())
    directory = (HERE / record['directory']).resolve()
    require(set(record['sha256']) == {'field.py', 'verify.py', 'expected.json', 'PROOF.md'},
            'dependency fingerprint list differs')
    for name, expected in record['sha256'].items():
        require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected,
                'dependency source changed: ' + name)
    # The prior verifier imports its own field.py. Check its hash before import.
    require('field' not in sys.modules, 'unexpected preloaded arithmetic module')
    sys.path.insert(0, str(directory))
    spec = spec_from_file_location('rid_brightness_dependency', directory / 'verify.py')
    base = module_from_spec(spec)
    spec.loader.exec_module(base)
    replay = json.dumps(base.verify(), indent=2, sort_keys=True) + '\n'
    require(replay == (directory / 'expected.json').read_text(),
            'prior geometric certificate no longer regenerates')
    return base, record


def tangent_constants(base, C):
    F, PHI, ZERO, dot = base.F, base.PHI, base.ZERO, base.dot
    require(len(C) == 31, 'incomplete physical area generators')
    D = [c for c in C if c[2] == ZERO]
    E = [c for c in C if c[2] != ZERO]
    require(len(D) == 6 and len(E) == 25, 'wrong tangent/nonzero partition')
    signed = tuple(sum((c[j] * c[2].sign() for c in E), ZERO) for j in range(3))
    A0 = 12 + 28 * PHI
    require(signed == (ZERO, ZERO, A0), 'axial signed sum changed')
    corners = []
    for signs in product((-1, 1), repeat=len(D)):
        x = tuple(sum((s * c[j] for s, c in zip(signs, D)), ZERO) for j in range(3))
        corners.append(x)
    require(len(corners) == 64, 'tangent endpoint combinations omitted')
    maximum = max(dot(x, x) for x in corners)
    require(maximum == 96 + 128 * PHI and maximum < F(Q(35, 2)**2),
            'tangent circumradius certificate fails')
    maximizers = sorted(set(x for x in corners if dot(x, x) == maximum), key=base.key)
    require(len(maximizers) == 4, 'wrong number of maximum tangent corners')
    threshold = min(c[2] * c[2] / dot(c, c) for c in E)
    require(threshold == (2 - PHI) / 4 and threshold > F(Q(1, 4)**2),
            'nonzero-generator sign stability does not reach chord 1/4')
    return dict(tangent_endpoint_combinations=64,
                tangent_maximizers=[base.encode(x) for x in maximizers],
                tangent_circumradius_squared=maximum.encode(),
                nonzero_generator_count=25, tangent_generator_count=6,
                sign_stability_threshold_squared=threshold.encode(),
                local_sign_stability_chord='1/4',
                tangent_circumradius_upper='35/2',
                unit_edge_tangent_circumradius_squared=(maximum / 16).encode(),
                unit_edge_tangent_circumradius_upper='35/8')


def local_hypotheses(base, V, h):
    F, PHI, ZERO, ONE, dot = base.F, base.PHI, base.ZERO, base.ONE, base.dot
    require(0 < h < 1, 'invalid full-frame radius')
    a, b, c = PHI**3, PHI**2, 2 + PHI
    R2 = 7 + 8 * PHI
    points = set()
    for sx, sy in product((-1, 1), repeat=2):
        points.update(((sx*a, F(sy)), (F(sx), sy*a), (sx*b, sy*c)))
    gaps = []
    for p in sorted(points, key=base.key):
        cluster = [v for v in V if v[:2] == p]
        require(len(cluster) in (1, 2), 'local cluster multiplicity changed')
        require({v[2] for v in cluster} == ({ZERO} if len(cluster) == 1 else {-ONE, ONE}),
                'local paired or singleton heights changed')
        for v in V:
            if v[:2] != p:
                gaps.append(dot(p, base.sub(p, v[:2])))
    require(len(gaps) == 700 and min(gaps) == ONE, 'local radial gap changed')
    require(a > ONE and 0 < b <= c < a*b and a*a+2 == R2 == b*b+c*c,
            'local theorem algebraic parameters fail')
    require(R2 < 20 and 80*h + 40*h*h < 1,
            'local radial support upper bound fails')
    require(4*R2*h + 2*R2*h*h < ONE, 'local radial support advantage fails')
    require(F(1-h*h) > (a*a+1)*h*h, 'paired axial signs can change')
    coefficient = a*a*b*b-c*c
    require(coefficient > ZERO and
            coefficient**2*(1-h*h) > (a*a+1)*h*h*(c*c-b*b)**2,
            'positive quadratic stress gate fails')
    return dict(local_full_frame_radius=str(h), local_radial_gap_comparisons=len(gaps),
                local_minimum_radial_gap='1',
                rational_local_support_upper=str(80*h+40*h*h))


def cap_gates(base, V, delta=Q(1, 270)):
    F, PHI, ZERO, ONE, dot = base.F, base.PHI, base.ZERO, base.ONE, base.dot
    A0, A1sq, R2 = 12+28*PHI, 940+1520*PHI, 7+8*PHI
    budget = Q(1, 15)
    initial = Q(1, 16)
    require(0 < delta <= Q(1, 4), 'invalid receiving cap')
    require(50 < A0 < Q(115, 2) and A0+budget < 58 and A1sq > 58**2,
            'extended polar budget reaches the second level')
    require(2*budget/50 < initial**2, 'extended polar initial localization fails')
    require(Q(999, 1000)**2 < 1-initial**2/4,
            'tangent square-root lower bound fails')
    require(14*Q(999, 1000)-Q(115, 2)*initial/2 > 12,
            'extended source coercivity is not above twelve')
    receiver_excess = Q(35, 2)*delta
    source = receiver_excess/12
    require(receiver_excess <= budget, 'cap exceeds the extended area budget')
    require(R2*(source**2+2*delta) < ONE,
            'a non-equatorial original can maximize the required support')
    root = Q(1, 150)
    require(source**2+delta**2 < root**2, 'quadratic support positive-root gate fails')
    relative_roll = root+source**2/2
    frame = source+relative_roll
    require(frame < Q(1, 81) and delta < Q(1, 81),
            'full-frame reduction exceeds the verified local radius')
    epsilon = Q(1, 20)
    require(R2 < 25 and 5*relative_roll < epsilon,
            'equatorial pair cannot be matched within the proper-isometry gate')
    b, c = PHI**2, 2+PHI
    require(8*5*epsilon <= 2 and 2*5*epsilon <= Q(1, 2),
            'squared-distance or determinant error allowance changed')
    require(4*(c*c-b*b) > 2 and 4*b*b > 2 and 4*b*c > Q(1, 2),
            'proper circle pair gaps fail')
    qplus, qminus = (b, c), (b, -c)
    circle = [qplus, qminus, base.neg(qplus), base.neg(qminus)]
    require(set(v[:2] for v in V if v[2] == ZERO) == set(circle),
            'height-zero original set changed')
    require(all(v[2] == ZERO or v[2]*v[2] >= ONE for v in V),
            'non-equatorial squared-radius gap fails')
    survivors = [(p, q) for p in circle for q in circle if p != q and
                 dot(base.sub(p, q), base.sub(p, q)) == 4*c*c and
                 p[0]*q[1]-p[1]*q[0] < ZERO]
    require(set(survivors) == {(qplus, qminus), (base.neg(qplus), base.neg(qminus))},
            'extra proper pair correspondence survived')
    require(12*delta <= budget, 'receiving area-gap localization budget fails')
    return dict(receiver_chord_radius=str(delta), local_receiver_area_upper_slope='35/2',
                extended_global_area_budget=str(budget), initial_polar_source_chord_upper=str(initial),
                global_linear_source_coercivity_lower='12',
                receiver_area_excess_upper=str(receiver_excess), source_chord_upper=str(source),
                equatorial_support_root_upper=str(root), relative_roll_operator_upper=str(relative_roll),
                full_source_frame_operator_upper=str(frame),
                proper_pair_survivors=len(survivors), pair_matching_absolute_error_upper=str(epsilon),
                global_receiver_area_gap=str(12*delta),
                unit_edge_global_area_budget=str(budget/4),
                unit_edge_global_source_coercivity_lower='3',
                unit_edge_global_receiver_area_gap=str(3*delta))


def transport_controls(base):
    # Exact checks of the displayed shortest-rotation formula at nonzero tilts.
    # These are controls; the arbitrary-normal identity is proved algebraically
    # in PROOF.md and is not inferred from these finitely many examples.
    F, PHI, ZERO, ONE, dot = base.F, base.PHI, base.ZERO, base.ONE, base.dot
    params = [(ZERO, ZERO), (F(Q(1, 20)), F(Q(1, 30))),
              (PHI/30, F(Q(1, 17))), (-PHI/40, PHI/23)]
    count = 0
    for p, q in params:
        den = ONE+p*p+q*q
        x, y, z = 2*p/den, 2*q/den, (ONE-p*p-q*q)/den
        n = (x, y, z)
        require(dot(n, n) == ONE and z > ZERO, 'control normal is not unit upper hemisphere')
        H = ((ONE-x*x/(ONE+z), -x*y/(ONE+z), -x),
             (-x*y/(ONE+z), ONE-y*y/(ONE+z), -y), (x, y, z))
        require(all(dot(r, s) == F(int(i == j))
                    for i, r in enumerate(H) for j, s in enumerate(H)),
                'displayed transport is not orthogonal')
        require(dot(H[0], base.cross(H[1], H[2])) == ONE,
                'displayed transport is not proper')
        require(tuple(dot(r, n) for r in H) == (ZERO, ZERO, ONE),
                'displayed transport does not send the normal to e')
        d2 = x*x+y*y+(z-ONE)**2
        require(d2/2 == ONE-z, 'quadratic chord identity fails')
        # Equatorial block I-H has eigenvalues 0 and 1-z: trace and determinant.
        block = ((x*x/(ONE+z), x*y/(ONE+z)),
                 (x*y/(ONE+z), y*y/(ONE+z)))
        require(block[0][0]+block[1][1] == ONE-z and
                block[0][0]*block[1][1]-block[0][1]*block[1][0] == ZERO,
                'equatorial block is not the stated quadratic contraction')
        count += 1
    return count


def negative_controls(base, V, C):
    rejected = 0
    cases = [lambda: tangent_constants(base, C[:-1]),
             lambda: tangent_constants(base, [tuple(2*x for x in c) for c in C]),
             lambda: cap_gates(base, V, Q(1, 200)),
             lambda: local_hypotheses(base, V, Q(1, 80))]
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
    # Reconstruct the actual facet area vectors, rather than loading a private
    # precomputed corpus or changing the prior verifier's guards/constants.
    planes, _ = base.complete_facets(V)
    C, records, _ = base.area_generators(V, planes)
    require(base.digest(records) == json.loads(
        ((HERE/dependency['directory'])/'expected.json').read_text())['facet_record_sha256'],
        'fresh physical area vectors differ from the replayed certificate')
    tangent = tangent_constants(base, C)
    local = local_hypotheses(base, V, Q(1, 81))
    cap = cap_gates(base, V)
    return dict(agent='six-rupert-3', role='researcher',
                proof_status='written_geometric_proof_with_exact_finite_hypotheses',
                global_RID_Rupert_status='unresolved', arithmetic='Q(phi), exact rational signs',
                dependency_commit=dependency['source_commit'], dependency_graph=dependency['graph_ref'],
                dependency_replay='every byte of prior expected.json regenerated',
                exact_transport_controls=transport_controls(base),
                malformed_controls_rejected=negative_controls(base, V, C),
                **tangent, **local, **cap)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    output = json.dumps(verify(), indent=2, sort_keys=True)+'\n'
    if not args.emit:
        require(output == (HERE/'expected.json').read_text(), 'new expected record differs')
    print(output, end='')


if __name__ == '__main__':
    main()
