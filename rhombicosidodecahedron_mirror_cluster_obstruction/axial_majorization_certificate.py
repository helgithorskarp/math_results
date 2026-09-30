#!/usr/bin/env python3
"""Exact finite hypotheses of AXIAL_MAJORIZATION_PROOF.md; Python3.11+ stdlib.

Only threshold-original sources into winning receivers are excluded here.
The global receiving gap remains1/100. No floating computation or solver.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'axial_majorization_inputs.json'


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_inputs():
    raw = MANIFEST.read_bytes()
    manifest = json.loads(raw)
    rows = manifest['files']
    demand(len(rows) == 44 and len({r['file'] for r in rows}) == 44,
           'complete distinct44published mathematical inputs')
    for row in rows:
        name = row['file']
        demand(Path(name).name == name and name.endswith(('.py', '.json')),
               'ordinary same-directory mathematical input')
        content = (HERE / name).read_bytes()
        demand(len(content) == row['bytes'] and
               hashlib.sha256(content).hexdigest() == row['sha256'],
               'published mathematical input byte mismatch: ' + name)
    return manifest, hashlib.sha256(raw).hexdigest()


INPUTS, INPUTS_SHA = pinned_inputs()
from verify import PHI, QPhi, ZERO, act, dot, require, symmetry_group, vertices
from torque_certificate import cross, subtract
from cell_certificate import encode, geometry
from linear_roll_certificate import project
from threshold_receiver_certificate import BETA, REFS, root as inherited_root

Q = F(21, 50)
PAIR_MAX = QPhi(F(68, 3)) + 32*PHI
SUM_SQUARED = (44 + 12*PHI)/29
ROOT_RECORDS = {}


def exact_root(name, value):
    """Regenerate and explicitly validate the positive fixed1e12 grid bracket."""
    interval = inherited_root(value)
    a, b = interval.lo, interval.hi
    demand(a >= 0 and a <= b and b-a <= F(1, 10**12) and
           QPhi(a*a) <= value <= QPhi(b*b), 'positive outward root bracket')
    ROOT_RECORDS[name] = dict(radicand=value.encode(), lower=str(a), upper=str(b))
    return a, b


def validate_body(V):
    demand(V == vertices() and len(V) == 60, 'complete standard original vertices')
    demand(all(tuple(-a for a in v) in V and dot(v, v) == 7+8*PHI for v in V),
           'antipodal equal-radius original body')


def tangent_facets(n, P, expected_count, expected_radius_squared):
    """Test every possible pair against every tangent point, retaining all edges."""
    demand(len(P) == expected_count and len(set(P)) == expected_count,
           'complete distinct active tangent points')
    facets = {}
    comparisons = 0
    for i, j in combinations(range(len(P)), 2):
        m = cross(n, subtract(P[j], P[i]))
        h = dot(m, P[i])
        demand(dot(m, m) > ZERO, 'nondegenerate tangent pair')
        gaps = [dot(m, p)-h for p in P]
        comparisons += len(P)
        if all(g <= ZERO for g in gaps) or all(g >= ZERO for g in gaps):
            demand(h != ZERO, 'tangent origin strictly inside all edge supports')
            mu = tuple(x/h for x in m)
            demand(all(dot(mu, p) <= QPhi(1) for p in P), 'actual tangent support')
            demand(sum(dot(mu, p) == QPhi(1) for p in P) == 2,
                   'exact tangent facet endpoints')
            facets[mu] = dict(pair=[i, j], radius_squared=(QPhi(1)/dot(mu, mu)).encode())
    demand(len(facets) == expected_count, 'all tangent polygon facets')
    radii = [QPhi(1)/dot(mu, mu) for mu in facets]
    demand(min(radii) == expected_radius_squared and min(radii) > ZERO,
           'sharp centered tangent disk')
    return dict(possible_pairs=len(P)*(len(P)-1)//2, comparisons=comparisons,
                sharp_radius_squared=expected_radius_squared.encode(),
                facets=[dict(normal=encode(mu), **row) for mu, row in sorted(facets.items())])


def winning_geometry(V, selected=None, claimed_pair_max=PAIR_MAX):
    validate_body(V)
    B = geometry()[0][0][1]
    N = dot(B, B)
    ordered = sorted(V)
    heights = [dot(v, B)**2/N for v in ordered]
    demand(min(heights) == QPhi(F(1, 3)), 'winning regional reference height')
    active = sorted(v for v in V if dot(v, B) > ZERO and 3*dot(v, B)**2 == N)
    if selected is not None:
        demand(selected == active, 'all six positive winning originals')
    demand(len(active) == 6 and all(dot(v, B) == PHI-1 for v in active),
           'complete common signed winning heights')
    signed = set(active) | {tuple(-x for x in v) for v in active}
    others = V-signed
    demand(len(signed) == 12 and len(others) == 48 and
           min(dot(v, B)**2/N for v in others) == QPhi(F(5, 3)),
           'complete12active and48nonactive original partition')
    P = [project(v, B) for v in active]
    demand(all(sum((p[a] for p in P), ZERO) == ZERO for a in range(3)),
           'exact six-original tangent balance')
    facets = tangent_facets(B, P, 6, QPhi(F(8, 3))+4*PHI)
    pairs = []
    complements = []
    for i, j in combinations(range(6), 2):
        s = tuple(P[i][a]+P[j][a] for a in range(3))
        complement = [k for k in range(6) if k not in (i, j)]
        t = tuple(sum((P[k][a] for k in complement), ZERO) for a in range(3))
        demand(t == tuple(-x for x in s), 'every four-sum is the negative complement pair')
        sq = dot(s, s)
        pairs.append(dict(pair=[i, j], squared_tangent_sum=sq.encode()))
        complements.append(dict(four=complement, squared_tangent_sum=dot(t, t).encode()))
    demand(max(dot(tuple(P[i][a]+P[j][a] for a in range(3)),
                   tuple(P[i][a]+P[j][a] for a in range(3)))
               for i, j in combinations(range(6), 2)) == claimed_pair_max == PAIR_MAX,
           'exact full fifteen-pair maximum')
    return dict(raw_reference=encode(B), normal_norm_squared=N.encode(),
                all60_original_squared_heights=[x.encode() for x in heights],
                positive_original_indices=[ordered.index(v) for v in active],
                all_six_tangents=[encode(p) for p in P], positive_tangent_sum_zero=True,
                nonactive_original_count=48, nonactive_minimum_squared_height=QPhi(F(5, 3)).encode(),
                tangent_disk=facets, all15_tangent_complement_pairs=pairs,
                all15_four_original_complements=complements,
                maximum_squared_four_tangent_sum=PAIR_MAX.encode()), B


def threshold_geometry(n, V, selected=None, claimed_sum=SUM_SQUARED):
    validate_body(V)
    ordered = sorted(V)
    N = dot(n, n)
    heights = [dot(v, n)**2/N for v in ordered]
    demand(min(heights) == BETA, 'threshold regional reference height')
    c = min(dot(v, n) for v in V if dot(v, n) > ZERO)
    active = sorted(v for v in V if dot(v, n) == c)
    if selected is not None:
        demand(selected == active, 'all four positive threshold originals')
    demand(len(active) == 4 and c*c/N == BETA, 'complete positive threshold contacts')
    signed = sorted(set(active) | {tuple(-x for x in v) for v in active})
    demand(len(signed) == 8, 'four distinct antipodal source pairs')
    P = [project(v, n) for v in active]
    facets = tangent_facets(n, P, 4, (39+37*PHI)/29)
    S = tuple(sum((v[a] for v in active), ZERO) for a in range(3))
    demand(dot(S, n) == 4*c, 'sum of all four positive axial reference heights')
    tangent_sum = project(S, n)
    demand(dot(tangent_sum, tangent_sum) == claimed_sum == SUM_SQUARED,
           'exact four-positive tangent sum')
    projected = {project(v, n) for v in V}
    circle = {p for p in projected if dot(p, p) == 7+8*PHI-BETA}
    source_circle = [project(v, n) for v in signed]
    demand(len(projected) == 60 and len(circle) == 8 and set(source_circle) == circle,
           'all eight original maximum-circle preimages uniquely identified')
    pairs = []
    for i, j in combinations(range(8), 2):
        delta = subtract(source_circle[i], source_circle[j])
        sq = dot(delta, delta)
        demand(sq > QPhi(F(3, 2)**2), 'every reference circle pair exceeds3over2')
        pairs.append(dict(pair=[i, j], squared_distance=sq.encode()))
    return dict(raw_reference=encode(n), normal_norm_squared=N.encode(),
                all60_original_squared_heights=[x.encode() for x in heights],
                positive_original_indices=[ordered.index(v) for v in active],
                signed_circle_original_indices=[ordered.index(v) for v in signed],
                all_four_tangents=[encode(p) for p in P], tangent_disk=facets,
                four_original_sum=encode(S), four_tangent_sum=encode(tangent_sum),
                four_tangent_sum_squared=SUM_SQUARED.encode(),
                unique_original_projections=60, all28_source_circle_pairs=pairs)


def scalar_certificate(q=Q, candidate=F(3, 8), retain_curvature=True):
    demand(F(2, 5) < q < F(9, 20) and 0 < candidate < 1, 'supported positive parameter domain')
    cL, cU = exact_root('threshold_height', BETA)
    c0L, c0U = exact_root('winning_height', QPhi(F(1, 3)))
    rtL, rtU = exact_root('threshold_disk_radius', (39+37*PHI)/29)
    rwL, rwU = exact_root('winning_disk_radius', QPhi(F(8, 3))+4*PHI)
    sL, sU = exact_root('threshold_four_tangent_sum_norm', SUM_SQUARED)
    wL, wU = exact_root('winning_complement_pair_norm', PAIR_MAX)
    sineT = (cU-q)/rtL
    sineW = (c0U-q)/rwL
    demand(0 < sineT < 1 and 0 < sineW < 1, 'positive small regional tangent bounds')
    zTL, zTU = exact_root('threshold_cosine_at_tangent_bound', QPhi(1-sineT*sineT))
    zWL, zWU = exact_root('winning_cosine_at_tangent_bound', QPhi(1-sineW*sineW))
    chordT = F(1001, 1000)*sineT
    chordW = F(1001, 1000)*sineW
    eta = cU*chordT+F(9, 4)*chordT*chordT
    loss = BETA-QPhi(q*q)+QPhi(9*eta)
    heightU = 4*cU*(zTU if retain_curvature else 1)+sU*sineT
    heightL = 4*c0L*zWL-wU*sineW
    gap = heightL-heightU
    gates = dict(
        receiver_height_square_above_other_region_maximum=QPhi(q*q)>QPhi(F(1, 7)),
        threshold_reference_height_exceeds_q=cL>q,
        winning_reference_height_exceeds_q=c0L>q,
        all_original_radii_below9over2=7+8*PHI<QPhi(F(9, 2)**2),
        threshold_normal_chord_conversion=F(1001, 1000)**2*(1+zTL)>2,
        winning_normal_chord_conversion=F(1001, 1000)**2*(1+zWL)>2,
        threshold_normal_chord_below21over1000=chordT<F(21, 1000),
        winning_normal_chord_below53over1000=chordW<F(53, 1000),
        all_threshold_positive_original_signs_persist=cL-F(9, 2)*chordT>0,
        all_winning_positive_original_signs_persist=c0L*zWL-F(9, 2)*chordW>0,
        all48_winning_nonactive_original_heights_exceed_one=F(5, 4)-F(9, 2)*chordW>1,
        exact_winning_nonactive_reference_height_exceeds5over4=QPhi(F(5, 3))>QPhi(F(5, 4)**2),
        all_actual_source_circle_candidate_heights_below_one=BETA+QPhi(9*eta)<QPhi(1),
        all_actual_source_circle_candidate_distances_below_bound=loss<QPhi(candidate*candidate),
        all_eight_radial_candidates_distinct=F(3, 2)-2*eta>2*candidate,
        curved_threshold_sum_strictly_increasing=sU*sU*(1-sineT*sineT)>(4*cU*sineT)**2,
        four_height_sum_gap_exceeds_one14000=gap>F(1, 14000),
        explicit_one31_squared_height_band_above_q_squared=BETA-QPhi(F(1, 31))>QPhi(q*q),
    )
    demand(all(gates.values()), 'unsupported axial-majorization scalar gates')
    return dict(q=str(q), all18_scalar_gates=gates,
                outward_threshold_tangent_norm_bound=str(sineT),
                outward_winning_tangent_norm_bound=str(sineW),
                threshold_normal_chord_bound=str(chordT), winning_normal_chord_bound=str(chordW),
                original_source_circle_transport_bound=str(eta), candidate_distance_bound=str(candidate),
                candidate_squared_distance_bound=loss.encode(),
                threshold_four_original_height_sum_upper=str(heightU),
                winning_four_smallest_original_height_sum_lower=str(heightL),
                strict_four_height_sum_gap=str(gap), certified_gap_lower='1/14000',
                source_cosine_term_retained=retain_curvature,
                receiving_squared_height_gap=(BETA-QPhi(q*q)).encode(),
                old25epsilonover27_chord_bound_used=False)


def orbit_certificate(V, B):
    G = symmetry_group(V, return_matrices=True)
    ordered = sorted(V)
    def signs(n):
        values = [dot(v, n).sign() for v in ordered]
        demand(0 not in values, 'strict actual original signed region')
        return sum((s > 0) << i for i, s in enumerate(values))
    records = []
    all_keys = set()
    for name, n, expected in [('winning', B, 20), ('threshold_low', REFS[0], 60),
                              ('threshold_high', REFS[1], 60)]:
        directions = {act(g, n) for g in G}
        demand(len(directions) == expected and
               all(tuple(-x for x in a) in directions for a in directions),
               'complete actual directed proper reference orbit')
        keys = {signs(a) for a in directions}
        demand(len(keys) == expected and not all_keys.intersection(keys),
               'distinct directed reference signed regions')
        all_keys.update(keys)
        mask = (1 << 60)-1
        projective = {min(k, mask ^ k) for k in keys}
        demand(len(projective) == expected//2, 'exact signed reversal pairing')
        raw = json.dumps([encode(a) for a in sorted(directions)], separators=(',', ':')).encode()
        records.append(dict(reference=name, directed_original_normal_count=expected,
                            projective_signed_region_count=expected//2,
                            complete_directed_reference_orbit_sha256=hashlib.sha256(raw).hexdigest()))
    return dict(actual_proper_body_rotations=len(G), all140_directed_signed_regions_distinct=True,
                original_reference_orbits=records)


def rejection(name, call, rows):
    try:
        call()
    except ValueError:
        rows.append(name)
        return
    raise ValueError('malformed control accepted: '+name)


def check(self_test=False):
    ROOT_RECORDS.clear()
    V = vertices()
    validate_body(V)
    winning, B = winning_geometry(V)
    threshold = [threshold_geometry(n, V) for n in REFS]
    scalar = scalar_certificate()
    roots = dict(ROOT_RECORDS)
    orbits = orbit_certificate(V, B)
    rejected = []
    if self_test:
        activeW = [sorted(V)[i] for i in winning['positive_original_indices']]
        activeT = [sorted(V)[i] for i in threshold[0]['positive_original_indices']]
        rejection('missing_original_vertex', lambda:validate_body(V-{min(V)}), rejected)
        rejection('missing_positive_winning_original', lambda:winning_geometry(V, selected=activeW[:-1]), rejected)
        rejection('missing_positive_threshold_original', lambda:threshold_geometry(REFS[0], V, selected=activeT[:-1]), rejected)
        rejection('false_complement_pair_maximum', lambda:winning_geometry(V, claimed_pair_max=PAIR_MAX-QPhi(1)), rejected)
        rejection('false_four_positive_tangent_sum', lambda:threshold_geometry(REFS[0], V, claimed_sum=SUM_SQUARED+QPhi(1)), rejected)
        rejection('unsupported_smaller_receiving_height', lambda:scalar_certificate(q=F(419, 1000)), rejected)
        rejection('unsafe_radial_candidate_distance', lambda:scalar_certificate(candidate=F(1, 100)), rejected)
        rejection('discarded_source_cosine_curvature', lambda:scalar_certificate(retain_curvature=False), rejected)
        rejection('invalid_parameter_domain', lambda:scalar_certificate(q=F(0)), rejected)
        demand(len(rejected) == 9, 'all nine malformed controls rejected')
    return dict(agent='six-rupert-3', role='researcher',
                proof_status='complete_written_unformalized_author_checked_source_branch_exclusion',
                independently_reviewed=False, global_RID_status='OPEN',
                global_receiving_squared_height_gap='1/100 unchanged',
                stronger_GLOBAL_gap_proved=False,
                branch='all threshold signed-region original sources into winning receivers f(n)>=21/50',
                closed_containment_excluded_for_all_proper_Q_planar_t_lambda_at_least_one=True,
                explicit_source_branch_squared_height_band='f(n)^2>=beta-1/31',
                phi_positive_root=True, beta=BETA.encode(), body_radius_squared=(7+8*PHI).encode(),
                all60_original_vertices=[encode(v) for v in sorted(V)],
                full_winning_original_geometry=winning, both_threshold_original_geometries=threshold,
                exact_scalar_bounds=scalar, all_positive_outward_root_enclosures=roots,
                directed_proper_gauge_checks=orbits, malformed_controls_rejected=rejected,
                published44_input_pins_checked=True, input_manifest_sha256=INPUTS_SHA,
                published_global_spectrum_436_regions_reenumerated=False,
                global_all_four_source_receiver_branches_discharged_here=False,
                continuous_radial_matching_and_majorization_proof='AXIAL_MAJORIZATION_PROOF.md')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--emit', action='store_true', help='emit regenerated exact fields for comparison')
    args = parser.parse_args()
    result = check(args.self_test)
    raw = (json.dumps(result, sort_keys=True, indent=2)+'\n').encode()
    if args.emit:
        print(raw.decode(), end='')
    else:
        demand(args.self_test, 'published replay requires all malformed controls')
        demand(raw == (HERE/'axial_majorization_expected.json').read_bytes(),
               'every expected certificate byte must match')
        print(json.dumps(dict(status='verified_every_expected_byte', bytes=len(raw),
                              sha256=hashlib.sha256(raw).hexdigest(),
                              scalar_gates=len(result['exact_scalar_bounds']['all18_scalar_gates']),
                              malformed_controls_rejected=len(result['malformed_controls_rejected']),
                              source_branch_only=True, global_receiving_gap='1/100'), sort_keys=True))


if __name__ == '__main__':
    main()
