#!/usr/bin/env python3
"""Exact finite hypotheses for GLOBAL_CAP_PROOF.md, Python 3.11+ stdlib.

The continuous active-set, coercivity, frame and torque arguments are proved
in prose. No finite sample of rotations is treated as their replacement.
"""
import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

from verify import PHI, QPhi, ZERO, act, dot, require, symmetry_group, vertices
from torque_certificate import cross, determinant, subtract
from cell_certificate import check as check_cells, decode, encode, geometry


def order(v):
    return tuple((q.a, q.b) for q in v)


def canonical(v):
    first = next((q for q in v if q != ZERO), None)
    require(first is not None, 'zero active-set direction')
    return tuple(q/first for q in v)


def representatives(V):
    require(len(V) == 60, 'standard vertex count')
    require(all(dot(v, v) == 7+8*PHI for v in V), 'equal vertex radius')
    require(all(tuple(-q for q in v) in V for v in V), 'central symmetry')
    A = sorted({v for v in V if next(q for q in v if q != ZERO).sign() > 0},
               key=order)
    require(len(A) == 30, 'antipodal representative count')
    return A


def raw_candidates(A):
    yield from A
    for a, b in combinations(A, 2):
        for e in (-1, 1):
            yield tuple(x+e*y for x, y in zip(a, b))
    for a, b, c in combinations(A, 3):
        for e, h in product((-1, 1), repeat=2):
            yield cross(tuple(x-e*y for x, y in zip(a, b)),
                        tuple(x-h*y for x, y in zip(a, c)))


def validate_candidates(raw_count, C):
    require(raw_count == 17140, 'incomplete raw candidate enumeration')
    require(len(C) == 4681, 'incomplete distinct candidate enumeration')


def check_regions(A, G, d):
    C = set()
    raw_count = 0
    for v in raw_candidates(A):
        raw_count += 1
        C.add(canonical(v))
    validate_candidates(raw_count, C)
    regions = {}
    boundary = 0
    all_optimizers = set()
    evaluations = []
    bound = QPhi(Fraction(1, 3))
    for n in sorted(C, key=order):
        dots = [dot(n, v) for v in A]
        signs = [q.sign() for q in dots]
        if 0 in signs:
            boundary += 1
            evaluations.append('boundary')
            continue
        bits = sum((s > 0) << i for i, s in enumerate(signs))
        bits = min(bits, ((1 << 30)-1) ^ bits)
        score = min(q*q for q in dots)/dot(n, n)
        require(score <= bound, 'candidate exceeds exact diameter bound')
        evaluations.append(str(bits)+':'+','.join(score.encode()))
        if score == bound:
            all_optimizers.add(n)
        old = regions.get(bits)
        if old is None or score > old[0]:
            regions[bits] = (score, n)
    winning = {bits:n for bits,(score,n) in regions.items() if score == bound}
    beta = max(score for score,n in regions.values() if score < bound)
    directed = {act(g, d) for g in G}
    orbit = {canonical(v) for v in directed}
    require(len(directed) == 20 and len(orbit) == 10, 'threefold orbit count')
    require(all(tuple(-q for q in v) in directed for v in directed),
            'directed orbit lacks antipodes')
    require(all_optimizers == orbit and set(winning.values()) == orbit,
            'optimizers do not equal threefold orbit')
    require(len(regions) == 436 and len(winning) == 10, 'sign-region count')
    require(beta == (19-8*PHI)/29, 'second-best region bound')
    require(bound-beta > QPhi(Fraction(1, 1000)), 'strict region gap')
    counts = {}
    for score,n in regions.values():
        key = tuple(score.encode())
        counts[key] = counts.get(key, 0)+1
    return {
        'raw_candidates': raw_count, 'distinct_projective_candidates': len(C),
        'exact_candidate_dot_products': 30*len(C),
        'boundary_candidates': boundary, 'antipodal_open_sign_regions': len(regions),
        'winning_regions': len(winning), 'all_optimal_unoriented_axes': len(orbit),
        'directed_optimal_normals': len(directed),
        'max_min_axial_squared': bound.encode(),
        'second_best_region_bound': beta.encode(),
        'strict_squared_axial_gap': (bound-beta).encode(),
        'gap_greater_than_1_over_1000': True,
        'minimum_squared_shadow_diameter': (4*(7+8*PHI-bound)).encode(),
        'strict_passage_squared_scale_upper_bound': ((7+8*PHI)/(7+8*PHI-bound)).encode(),
        'score_counts': [{'score':list(k),'regions':n} for k,n in sorted(counts.items())],
        'candidate_evaluation_sha256': hashlib.sha256('\n'.join(evaluations).encode()).hexdigest(),
    }


def validate_circle(S, circle, rho2):
    require(len(circle) == 12, 'complete twelve-point circle required')
    require(circle == {p for p in S if dot(p,p) == rho2},
            'circle must contain all and only maximum-radius projected vertices')


def circle_map(d, rho2, p, q):
    c = dot(p,q)/rho2
    t = dot(d,cross(p,q))/(dot(d,d)*rho2)
    require(c*c+dot(d,d)*t*t == QPhi(1), 'circle map is not a rotation')
    def rotate(x):
        return tuple(c*y+t*z for y,z in zip(x,cross(d,x)))
    return c,t,rotate


def require_valid_roll(d, rho2, p, q, circle):
    c,t,rotate = circle_map(d,rho2,p,q)
    require({rotate(x) for x in circle} == circle, 'invalid circle roll accepted')


def check_circle_geometry(V, G, d):
    N = dot(d,d)
    project = lambda v: tuple(x-y*dot(d,v)/N for x,y in zip(v,d))
    S = {project(v) for v in V}
    rho2 = 7+8*PHI-QPhi(Fraction(1,3))
    require(max(dot(p,p) for p in S) == rho2, 'wrong maximum projected radius')
    circle = {p for p in S if dot(p,p) == rho2}
    validate_circle(S,circle,rho2)
    gap = min(rho2-dot(p,p) for p in S if p not in circle)
    require(gap == QPhi(Fraction(4,3)), 'noncircle radius gap')
    require(rho2 > 16 and rho2 < 25, '4<rho<5')
    stabilizer = {g for g in G if act(g,d) == d}
    require(len(stabilizer) == 3, 'directed stabilizer must be C3')
    active = {v for v in V if dot(v,d) > 0 and dot(v,d)**2 == N/3}
    require(len(active) == 6, 'positive active vertex count')
    v = min(active,key=order)
    triple = {act(g,v) for g in stabilizer}
    require(len(triple) == 3 and triple <= active, 'active stress triple')
    tangents = {project(v) for v in triple}
    require(tuple(sum((p[k] for p in tangents),ZERO) for k in range(3)) == (ZERO,)*3,
            'tangent triangle does not balance')
    require(all(dot(p,p) == rho2 for p in tangents), 'tangent triangle radii')
    require(all(dot(p,q) == -rho2/2 for p in tangents for q in tangents if p != q),
            'tangent triangle not equilateral')
    p = min(circle,key=order)
    valid = set()
    bad = []
    for q in sorted(circle,key=order):
        c,t,rotate = circle_map(d,rho2,p,q)
        if {rotate(x) for x in circle} == circle:
            valid.add((c,t))
            require({rotate(x) for x in S} == S, 'circle roll fails for whole shadow')
        else:
            defect = max(min(dot(subtract(rotate(x),y),subtract(rotate(x),y))
                             for y in circle) for x in circle)
            require(defect > QPhi(Fraction(1,100)), 'invalid-roll separation')
            bad.append((q,defect))
    expected = {(QPhi(1),ZERO),(QPhi(-1),ZERO)}
    for sign in (-1,1):
        for c in (QPhi(Fraction(1,2)),QPhi(Fraction(-1,2))):
            expected.add((c,sign*(PHI-1)/2))
    require(valid == expected and len(bad) == 6, 'shadow roll group must be C6')
    return {
        'threefold_axis': encode(d), 'directed_axis_stabilizer_order': len(stabilizer),
        'active_positive_vertices': len(active),
        'active_stress_triangle': [encode(x) for x in sorted(triple,key=order)],
        'equilateral_tangent_triangle': True,
        'maximum_squared_shadow_radius': rho2.encode(), 'rho_between_4_and_5': True,
        'maximum_radius_circle_points': len(circle), 'other_squared_radius_gap': gap.encode(),
        'whole_shadow_rotation_group_order': len(valid), 'invalid_candidate_rolls': len(bad),
        'minimum_invalid_roll_defect_squared': min(z for q,z in bad).encode(),
        'invalid_roll_defect_squared_greater_than_1_over_100': True,
    }, (S,circle,rho2,p,bad[0][0])


def check_threefold_chamber(G, d):
    cells,bad,A,D = geometry()
    B = cells[0][1]
    require(canonical(B) in {canonical(act(g,d)) for g in G}, 'B not threefold')
    signed = G | {tuple(tuple(-q for q in row) for row in g) for g in G}
    orbit = {act(g,B) for g in signed}
    walls = [(QPhi(1),ZERO,ZERO),(ZERO,QPhi(1),ZERO),(-PHI,-PHI**2,QPhi(1))]
    require(len(orbit) == 20, 'signed threefold orbit count')
    separation = []
    for v in orbit:
        if v == B:
            continue
        negative = [dot(v,h)**2/(dot(v,v)*dot(h,h)) for h in walls if dot(v,h) < 0]
        require(negative and max(negative) > QPhi(Fraction(1,10000)),
                'other threefold orbit point too close to chamber')
        separation.append(max(negative))
    ymax = max(u[1] for U in cells[1:] for u in U)
    require(ymax == D[1] and B[1]-ymax > QPhi(Fraction(1,10)), 'ABD chart separation')
    require(B[1] > QPhi(Fraction(3,10)) and dot(B,B) < QPhi(Fraction(25,16)),
            'B chart bounds')
    return {
        'chamber_threefold_ray': encode(B), 'signed_directed_threefold_orbit': len(orbit),
        'minimum_squared_negative_wall_separation': min(separation).encode(),
        'negative_wall_distance_greater_than_1_over_100': True,
        'chart_gap_to_other_cells': (B[1]-ymax).encode(),
        'chart_gap_greater_than_1_over_10': True,
    }


def check_threefold_torque():
    B = geometry()[0][0][1]
    record = json.loads(Path(__file__).with_name('cell_probes.json').read_text())[0]
    require(record['cell'] == 0 and record['sign'] == 1, 'ABD contact sign')
    T = [cross(decode(p['vertex']),cross(decode(p['edge']),B))
         for p in record['probes']]
    require(len(T) == 4, 'four ABD torque columns required')
    stresses = [(-1)**j*determinant(*(T[k] for k in range(4) if k != j))
                for j in range(4)]
    require(all(q > 0 for q in stresses), 'positive center torque stress')
    require(tuple(sum((stresses[j]*T[j][k] for j in range(4)),ZERO)
                  for k in range(3)) == (ZERO,)*3, 'center torque equilibrium')
    squared_distances = []
    for j in range(4):
        a,b,c = [T[k] for k in range(4) if k != j]
        normal = cross(subtract(b,a),subtract(c,a))
        require(dot(normal,normal) > 0, 'degenerate center torque facet')
        distance2 = determinant(a,b,c)**2/dot(normal,normal)
        require(distance2 > QPhi(Fraction(1,100)), 'center torque ball radius')
        squared_distances.append(distance2)
    return {
        'center_torque_stresses_positive': True,
        'center_facet_squared_distances': [q.encode() for q in squared_distances],
        'center_minimum_squared_facet_distance': min(squared_distances).encode(),
        'center_torque_ball_radius_greater_than_1_over_10': True,
    }


def check_constants(delta=Fraction(1,2000000)):
    require(delta == Fraction(1,2000000), 'unsupported receiver cap radius')
    eta = 190*delta
    e_upper = Fraction(1,32)
    q_lower = Fraction(999,1000)
    checks = {
        'source_stays_in_optimal_sign_region': 50*delta < Fraction(1,1000),
        'source_f_greater_than_one_half': Fraction(1,3)-50*delta > Fraction(1,4),
        'sqrt_two_times_twenty_five_less_than_thirty_six': 2*25**2 < 36**2,
        'circle_points_are_forced': 10*eta < Fraction(1,10),
        'circle_error_upper': 1900*delta < e_upper**2,
        'invalid_rolls_are_excluded': 2*e_upper < Fraction(1,10),
        'receiver_stays_in_threefold_chamber': delta < Fraction(1,100),
        'chart_error_less_than_three_delta': Fraction(9,4)/Fraction(79,100) < 3,
        'receiver_stays_in_ABD': 3*delta < Fraction(1,10),
        'ABD_barycentric_margin': 1-10*delta > q_lower,
        'torque_remainder_margin': Fraction(25,252) < Fraction(1,10)-30*delta,
        'full_relative_angle_is_excluded': 148*delta+e_upper/2 < Fraction(1,63),
    }
    require(all(checks.values()), 'a rational proof error bound failed')
    return {
        'receiver_normal_chord_radius': str(delta),
        'source_normal_chord_error_upper': str(36*delta),
        'one_sided_shadow_error_upper': str(eta),
        'circle_point_error_upper': str(e_upper),
        'ABD_barycentric_q_lower': str(q_lower),
        'center_torque_ball_radius_lower': '1/10',
        'torque_column_perturbation_upper': str(30*delta),
        'perturbed_torque_ball_radius_lower': str(Fraction(1,10)-30*delta),
        'local_exclusion_angle_lower': '1/63',
        'full_relative_angle_upper': str(148*delta+e_upper/2),
        'rational_error_checks': checks,
    }


def expect_rejection(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('malformed control was accepted')


def check(self_test=False):
    V = vertices()
    A = representatives(V)
    G = symmetry_group(V,return_matrices=True)
    require(len(G) == 60, 'proper symmetry group order')
    d = (ZERO,QPhi(1),-PHI**2)
    regions = check_regions(A,G,d)
    circle, fixture = check_circle_geometry(V,G,d)
    chamber = check_threefold_chamber(G,d)
    torque = check_threefold_torque()
    constants = check_constants()
    inherited = check_cells()
    expected_cells = json.loads(Path(__file__).with_name('cell_expected.json').read_text())
    require(json.loads(json.dumps(inherited)) == expected_cells,
            'inherited cell certificate changed')
    if self_test:
        expect_rejection(lambda: representatives(V-{next(iter(V))}))
        expect_rejection(lambda: validate_candidates(17139,set(range(4681))))
        expect_rejection(lambda: validate_candidates(17140,set(range(4680))))
        S,C,rho2,p,badq = fixture
        expect_rejection(lambda: validate_circle(S,C-{next(iter(C))},rho2))
        expect_rejection(lambda: require_valid_roll(d,rho2,p,badq,C))
        expect_rejection(lambda: check_constants(Fraction(1,1000000)))
    return {
        'agent':'six-rupert-3', 'role':'researcher',
        'proof_status':'unformalized_analytic_theorem_with_exact_finite_hypotheses',
        'global_non_rupert_proved':False,
        'all_source_receiver_caps':10, 'arbitrary_translation_and_source_roll':True,
        'diameter_and_sign_regions':regions, 'threefold_shadow':circle,
        'threefold_local_chamber':chamber, 'threefold_local_torque':torque,
        'quantitative_constants':constants,
        'inherited_cell_expected_sha256': hashlib.sha256(
            Path(__file__).with_name('cell_expected.json').read_bytes()).hexdigest(),
        'active_set_dependency_graph':'bafkreifyedsqxvx6zpxnj2jpg6bjzladxq3ufn7ef4ekjs6a42nvgfvxaa',
        'local_cell_dependency_graph':'bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args = parser.parse_args()
    print(json.dumps(check(args.self_test),indent=2,sort_keys=True))
