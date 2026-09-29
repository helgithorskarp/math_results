#!/usr/bin/env python3
"""Exact five-cell certificate for fixed-projection RID rigidity.

All arithmetic is in Q(phi); Python 3.11+ standard library. See CELL_PROOF.md
for the geometric bridge and the varying-target critical-orbit reduction.
"""
import argparse
import copy
import json
from itertools import product
from math import factorial
from pathlib import Path

from verify import (PHI, QPhi, ZERO, act, dot, matmul, require,
                    symmetry_group, vertices)
from torque_certificate import cross, determinant, subtract


EXPONENTS = sorted(set(tuple(r.count(i) for i in range(3))
                       for r in product(range(3), repeat=3)))


def encode(v):
    return [q.encode() for q in v]


def decode(v):
    require(len(v) == 3, 'a vector must have three coordinates')
    require(all(len(q) == 2 for q in v), 'a field element needs two rationals')
    return tuple(QPhi(*q) for q in v)


def geometry():
    one = QPhi(1)
    A = (ZERO, ZERO, one)
    B = (ZERO, one/PHI**2, one)
    C = (one/PHI, ZERO, one)
    D = (one/(PHI*(PHI+2)), one/(PHI+2), one)
    E = (one/PHI**2, one/PHI**4, one)
    F = (one/PHI**2, ZERO, one)
    H = tuple((a+d)/2 for a, d in zip(A, D))
    # B,D,E,C in this order on the outer side; F on A,C; H on A,D.
    for p in (D, E):
        require(PHI*p[0]+PHI**2*p[1] == one, 'outer side condition')
        require(p[0] > 0 and p[1] > 0, 'outer side interior condition')
    require(B[0] < D[0] < E[0] < C[0], 'outer side ordering')
    require(F[1] == ZERO and A[0] < F[0] < C[0], 'F on open A,C side')
    require(H == tuple((a+d)/2 for a, d in zip(A, D)), 'H midpoint')
    cells = [(A, B, D), (A, H, E), (H, D, E), (A, E, F), (F, E, C)]
    bad_indices = [0, 0, 1, 0, None]
    for U in cells:
        require(determinant(*U).sign() != 0, 'parameter triangle degenerate')
        require(all(u[2] == one and u[0] >= 0 and u[1] >= 0
                    and PHI*u[0]+PHI**2*u[1] <= one for u in U),
                'ray outside chamber')
        require(all(dot(u, u) < QPhi(25)/16 for u in U), 'ray norm >=5/4')
        require(all(dot(subtract(u, w), subtract(u, w)) < 1
                    for u, w in product(U, repeat=2)), 'cell diameter >=1')
    require(D == tuple(q/(1+3*PHI) for q in (one, PHI, 1+3*PHI)),
            'critical direction identity')
    return cells, bad_indices, A, D


def check_symmetry(V, A, D):
    G = symmetry_group(V, return_matrices=True)
    require(len(G) == 60, 'proper symmetry group order')
    signed = G | {tuple(tuple(-q for q in row) for row in g) for g in G}
    require(len(signed) == 120, 'full signed symmetry order')
    normals = [(QPhi(1), ZERO, ZERO), (ZERO, QPhi(1), ZERO),
               (-PHI, -PHI**2, QPhi(1))]
    I = tuple(tuple(QPhi(int(i == j)) for j in range(3)) for i in range(3))
    interior = tuple(map(QPhi, (1, 1, 5)))
    for h in normals:
        reflection = tuple(tuple(I[i][j]-2*h[i]*h[j]/dot(h, h)
                                 for j in range(3)) for i in range(3))
        require(reflection in signed, 'chamber reflection absent from symmetry group')
        require(matmul(reflection, reflection) == I, 'reflection not involution')
        require(determinant(*reflection) == QPhi(-1), 'reflection determinant')
        require({act(reflection, v) for v in V} == V, 'reflection changes solid')
        require(dot(interior, h) > 0, 'maximization chamber argument fails')
    critical = {act(g, D) for g in G}
    mirrors = {act(g, A) for g in signed}
    require(len(critical) == 60 and len(mirrors) == 30, 'axis orbit counts')
    require(all(tuple(-q for q in u) in critical for u in critical),
            'critical orbit not antipodally paired')
    return {'proper_rotations': len(G), 'signed_symmetries': len(signed),
            'mirror_directed_normals': len(mirrors), 'mirror_unoriented_axes': len(mirrors)//2,
            'critical_directed_normals': len(critical), 'critical_unoriented_axes': len(critical)//2,
            'three_chamber_reflections_verified': True}


def check_limiting_cone(V, cells, A, D, loop_input=None):
    """Exact full edge-contact cone on the open triangle A,D,E."""
    if loop_input is None:
        loop_input = json.loads(Path(__file__).with_name('limit_silhouette.json').read_text())
    loop = list(map(decode, loop_input))
    require(len(loop) == 16 and len(set(loop)) == 16, '16 distinct silhouette vertices')
    require(all(v in V for v in loop), 'silhouette vertex absent')
    require(all(loop[(j+8)%16] == tuple(-q for q in v) for j,v in enumerate(loop)),
            'silhouette not antipodally ordered')
    E = cells[2][2]
    U = (A, D, E)
    center = tuple(sum((u[k] for u in U), ZERO)/3 for k in range(3))
    axis = (QPhi(1), PHI, 1-PHI)
    require(dot(axis, D) == ZERO and dot(axis, axis) > 0, 'limiting axis not nonzero tangent')
    comparisons = zero_dots = negative_dots = 0
    for j,v in enumerate(loop):
        nxt = loop[(j+1)%16]
        d = subtract(nxt, v)
        prev_d = subtract(v, loop[j-1])
        require(dot(d,d) == QPhi(4), 'silhouette edge length is not two')
        turn = cross(prev_d,d)
        require(all(dot(turn,u) >= 0 for u in U) and dot(turn,center) > 0,
                'silhouette turn is not strictly convex in open cell')
        for u in U:
            m = cross(d,u)
            for w in V:
                require(dot(m,subtract(v,w)) >= 0, 'silhouette edge not supporting')
                comparisons += 1
        mcenter = cross(d,center)
        require(all(dot(mcenter,subtract(v,w)) > 0 for w in V if w not in (v,nxt)),
                'open-cell edge has additional supporting preimages')
        mD = cross(d,D)
        require(dot(mD,mD) > 0, 'vanishing edge probe at D would require extra limit analysis')
        for endpoint in (v,nxt):
            value = dot(axis,cross(endpoint,mD))
            require(value <= 0, 'limiting contact cone not separated')
            zero_dots += value == ZERO
            negative_dots += value < 0
    require(negative_dots > 0, 'separator has no strict inequality')
    return {'open_cell_rays': list(map(encode,U)), 'silhouette_vertices': len(loop),
            'support_comparisons_at_corners': comparisons,
            'full_contact_cone_generators_before_antipodal_deduplication': 32,
            'all_edge_probes_have_nonzero_D_limits': True,
            'limiting_separator': encode(axis),
            'limiting_separator_zero_dot_products': zero_dots,
            'limiting_separator_negative_dot_products': negative_dots,
            'uniform_positive_first_order_contact_margin_through_this_cell': False}


def cofactor_coefficients(T, omitted, sign):
    """Coefficient expansion by determinant trilinearity, not interpolation."""
    kept = [j for j in range(4) if j != omitted]
    result = {e: ZERO for e in EXPONENTS}
    for r in product(range(3), repeat=3):
        exponent = tuple(r.count(i) for i in range(3))
        term = determinant(*(T[j][k] for j, k in zip(kept, r)))
        result[exponent] += sign*(-1)**omitted*term
    return result


def check(certificate=None):
    V = vertices()
    require(len(V) == 60 and all(dot(v, v) == 7+8*PHI for v in V),
            'standard sphere-inscribed vertex input')
    require(all(tuple(-q for q in v) in V for v in V), 'central symmetry')
    require(7+8*PHI < 25, 'R<5 bound')
    require(PHI**3 > 1 and all((QPhi(sx),QPhi(sy),sz*PHI**3) in V
                              for sx,sy,sz in product((-1,1),repeat=3)),
            'box proving K contains the unit ball')
    cells, bad_indices, A, D = geometry()
    symmetry = check_symmetry(V, A, D)
    if certificate is None:
        certificate = json.loads(Path(__file__).with_name('cell_probes.json').read_text())
    require(len(certificate) == 5, 'five cell inputs required')
    outputs = []
    support_count = coefficient_count = 0
    minimum_normalized_coefficient = None
    for number, (record, U, bad) in enumerate(zip(certificate, cells, bad_indices)):
        require(record['cell'] == number and record['sign'] in (-1, 1), 'cell index/sign')
        require(len(record['probes']) == 4, 'four probes per cell required')
        T = []
        out_probes = []
        for probe in record['probes']:
            v, d = decode(probe['vertex']), decode(probe['edge'])
            require(v in V, 'support vertex absent')
            require(dot(d, d) == QPhi(4), 'edge vector length is not two')
            require(tuple(x+y for x, y in zip(v, d)) in V or subtract(v, d) in V,
                    'probe edge has no second endpoint')
            corner_torques = []
            for u in U:
                m = cross(d, u)
                require(dot(m, u) == ZERO, 'probe not perpendicular to target normal')
                for w in V:
                    require(dot(m, subtract(v, w)) >= 0, 'invalid supporting probe')
                    support_count += 1
                corner_torques.append(cross(v, m))
            T.append(corner_torques)
            out_probes.append({'vertex': encode(v), 'edge_vector': encode(d)})
        weights = []
        polynomial_weights = []
        cell_minimum = None
        for j in range(4):
            coefficients = cofactor_coefficients(T, j, record['sign'])
            require(all(q >= 0 for q in coefficients.values()), 'negative polynomial coefficient')
            for e, q in coefficients.items():
                coefficient_count += 1
                if bad is not None and e[bad] == 3:
                    continue
                multinomial = factorial(3)
                for k in e:
                    multinomial //= factorial(k)
                normalized = q/multinomial
                require(normalized > QPhi(1)/10, 'positive cubic coefficient bound failed')
                if cell_minimum is None or normalized < cell_minimum:
                    cell_minimum = normalized
                if minimum_normalized_coefficient is None or normalized < minimum_normalized_coefficient:
                    minimum_normalized_coefficient = normalized
            weights.append([coefficients[e].encode() for e in EXPONENTS])
            polynomial_weights.append(coefficients)
        # Cofactor identity checked at two exact barycentric values as a
        # cross-check; the universal identity is determinant algebra in the proof.
        for bary in [(QPhi(1)/3,)*3, (QPhi(1)/6,QPhi(1)/3,QPhi(1)/2)]:
            torque = [tuple(sum((b*t[k] for b,t in zip(bary, tj)),ZERO)
                            for k in range(3)) for tj in T]
            lambdas = [record['sign']*(-1)**j*determinant(
                *[t for k,t in enumerate(torque) if k != j]) for j in range(4)]
            expanded = [sum((q*product_value for e,q in coefficients.items()
                             for product_value in [bary[0]**e[0]*bary[1]**e[1]*bary[2]**e[2]]), ZERO)
                        for coefficients in polynomial_weights]
            require(expanded == lambdas, 'trilinear coefficient expansion cross-check')
            require(all(q > 0 for q in lambdas), 'positive stress cross-check')
            require(all(sum((q*t[k] for q,t in zip(lambdas,torque)),ZERO) == ZERO
                        for k in range(3)), 'stress identity cross-check')
        outputs.append({'cell': number, 'rays': list(map(encode, U)),
                        'exceptional_barycentric_corner': bad,
                        'support_probes': out_probes,
                        'cofactor_cubic_coefficients': weights,
                        'minimum_nonexceptional_normalized_coefficient': cell_minimum.encode()})
    # Quantitative constants for r=q/6250, M<25/2, theta<=q/100000.
    require(QPhi(25)/4/QPhi(100000) < QPhi(1)/6250, 'angle/remainder inequality')
    return {'agent': 'six-rupert-3', 'role': 'researcher',
            'claim_status': 'exact_polynomial_cell_certificate_for_analytic_local_lemma',
            'global_non_rupert_proved': False,
            'uniform_local_non_rupert_proved': False,
            'every_fixed_target_has_positive_exclusion_angle': True,
            'remaining_local_accumulation_normals_one_symmetry_orbit': True,
            'critical_normal_unnormalized': encode((QPhi(1),PHI,1+3*PHI)),
            'symmetry': symmetry, 'cell_count': len(cells),
            'support_comparisons_at_corners': support_count,
            'exact_cubic_coefficients_checked': coefficient_count,
            'cubic_monomial_exponents': EXPONENTS,
            'minimum_nonexceptional_normalized_coefficient': minimum_normalized_coefficient.encode(),
            'support_probe_bound_M': '25/2', 'torque_facet_normal_bound': '625',
            'K_contains_closed_unit_ball': True,
            'cofactor_lower_bound': 'q/10', 'torque_ball_radius_lower_bound': 'q/6250',
            'per_cell_relative_rotation_angle_maximum_radians': 'q/100000',
            'uniform_angle_away_from_critical_orbit': 'rho/200000 for 0<rho<=1/200',
            'cells': outputs,
            'limiting_contact_cone_obstruction': check_limiting_cone(V,cells,A,D)}


def self_test():
    original = json.loads(Path(__file__).with_name('cell_probes.json').read_text())
    invalids = []
    bad = copy.deepcopy(original)
    bad[0]['sign'] *= -1
    invalids.append(bad)
    bad = copy.deepcopy(original)
    bad[0]['probes'][0]['edge'] = [[str(-QPhi(*q).a), str(-QPhi(*q).b)]
                                 for q in bad[0]['probes'][0]['edge']]
    invalids.append(bad)
    invalids.append(original[:-1])
    for certificate in invalids:
        try:
            check(certificate)
        except ValueError:
            pass
        else:
            raise ValueError('malformed cell certificate accepted')
    cells, _, A, D = geometry()
    loop = json.loads(Path(__file__).with_name('limit_silhouette.json').read_text())
    try:
        check_limiting_cone(vertices(),cells,A,D,loop[::-1])
    except ValueError:
        pass
    else:
        raise ValueError('reversed silhouette accepted')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    print(json.dumps(check(), indent=2, sort_keys=True))
