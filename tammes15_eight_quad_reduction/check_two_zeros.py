#!/usr/bin/env python3
"""Exact count/angle bookkeeping and necessary cover for TWO_ZEROS.md.

CPython >=3.11, standard library. The geometric translations and strict
trigonometric comparisons are unformalized hand proofs, not code claims.
"""
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
import sys

import check as prior
import check_boundary_patch as boundary


def face_allowed(mask):
    prior.need(type(mask) is int and 0 <= mask < 16, 'four-corner mask required')
    zeros = [(mask >> i) & 1 for i in range(4)]
    # A W vertex cannot have two distinct zero-triangle neighbors.
    return all(zeros[i] or zeros[(i-1) % 4]+zeros[(i+1) % 4] <= 1
               for i in range(4))


def five_allowed(mask):
    prior.need(type(mask) is int and 0 <= mask < 16, 'four-corner mask required')
    return not any((mask >> i) & 1 and (mask >> ((i+1) % 4)) & 1
                   for i in range(4))


def allocations(r, e, maximum_all_zero):
    """Solve the three face-count equations directly in nonnegative integers."""
    solutions = []
    for a in range(maximum_all_zero+1):
        for f0, f1 in product(range(9), repeat=2):
            f2 = 8-a-f0-f1
            if f2 < 0:
                continue
            if f1+2*f2+4*a == 3*r+8 and f2+4*a == 2*e:
                solutions.append({'a': a, 'f0': f0, 'f1': f1, 'f2': f2})
    return solutions


def incidence_checks():
    graph_rows, checked = [], 0
    for r, expected_edges, expected_masks in [(0,[0,1],2),(1,[1,2],6),(2,[4],3)]:
        n, m, total = r+2, 11-2*r, 3*r+8
        pairs = tuple(combinations(range(n), 2))
        admitted = []
        for mask in range(1 << len(pairs)):
            checked += 1
            edges = frozenset(pair for i,pair in enumerate(pairs) if (mask >> i) & 1)
            b = total-2*len(edges)
            if boundary.zero_graph_allowed(n,edges) and 0 <= b <= m:
                admitted.append(edges)
        prior.need(sorted({len(e) for e in admitted}) == expected_edges,
                   'zero-graph edge classification')
        prior.need(len(admitted) == expected_masks, 'zero-graph mask count')
        if r == 2:
            prior.need(all(sorted(sum(v in edge for edge in edges) for v in range(n))
                           == [2]*4 for edges in admitted), 'four-cycle classification')
        graph_rows.append({'n3':r,'zero_vertices':n,'masks_checked':1 << len(pairs),
                           'capacity_admitted_masks':len(admitted),
                           'admitted_internal_edge_counts':expected_edges})
    prior.need(checked == 74, 'bounded zero-graph mask total')

    masks = [mask for mask in range(16) if face_allowed(mask)]
    prior.need(masks == [0,1,2,3,4,6,8,9,12,15], 'cyclic zero-corner masks')
    five_masks = [mask for mask in range(16) if five_allowed(mask)]
    prior.need(five_masks == [0,1,2,4,5,8,10], 'ordinary-five corner masks')

    rows = []
    reasons = {(0,0,0):'alpha forced to 3pi/7',
               (0,1,0):'free-Q angle lower bound exceeds upper bound',
               (1,1,0):'negative f0',
               (1,2,0):'adjacent-zero pair sum too small',
               (2,4,0):'negative f1',
               (2,4,1):'free Q needs at least two unattached fours'}
    for row in graph_rows:
        r = row['n3']
        max_a = int(r == 2)
        for e in row['admitted_internal_edge_counts']:
            closed = []
            for a in range(max_a+1):
                b = 3*r+8-2*e
                record = {'n3':r,'internal_edges':e,'all_zero_Q':a,'boundary_edges':b,
                          'unattached_fours':11-2*r-b,'ordinary_fives':r+2,
                          'f0':8-(3*r+8)+2*e-a,
                          'f1':3*r+8-4*e+4*a,'f2':2*e-4*a,
                          'exclusion':reasons[(r,e,a)]}
                rows.append(record)
                if min(record[k] for k in ['f0','f1','f2']) >= 0:
                    closed.append({'a':a,**{k:record[k] for k in ['f0','f1','f2']}})
            direct = allocations(r,e,max_a)
            prior.need(sorted(closed,key=lambda t:t['a']) == direct,
                       'independent integer face-count solutions')
    prior.need(len(rows) == 6, 'complete incidence branch table')
    six_pairs = tuple(combinations(range(6),2))
    six_histogram = {}
    for mask in range(1 << len(six_pairs)):
        edges = frozenset(pair for i,pair in enumerate(six_pairs) if (mask >> i) & 1)
        if boundary.zero_graph_allowed(6,edges):
            six_histogram[len(edges)] = six_histogram.get(len(edges),0)+1
    prior.need(max(six_histogram) == 7 and sum(six_histogram.values()) == 5314,
               'six-vertex zero-triangle graph bound')
    mixed_r = 5
    mixed_degree_sum,mixed_capacity = 3*mixed_r+4,14-2*mixed_r
    required = (mixed_degree_sum-mixed_capacity+1)//2
    prior.need(required == 8 and required > max(six_histogram),
               'mixed-distribution terminal profile contradiction')
    five_pairs = tuple(combinations(range(5),2))
    frontier_counts = {'five-cycle':0,'four-cycle with pendant edge':0}
    frontier_masks = set()
    for mask in range(1 << len(five_pairs)):
        edges = frozenset(pair for i,pair in enumerate(five_pairs) if (mask >> i) & 1)
        if len(edges) == 5 and boundary.zero_graph_allowed(5,edges):
            frontier_masks.add(edges)
            degrees = sorted(sum(v in edge for edge in edges) for v in range(5))
            if degrees == [2]*5:
                frontier_counts['five-cycle'] += 1
            elif degrees == [1,2,2,2,3]:
                frontier_counts['four-cycle with pendant edge'] += 1
            else:
                raise ValueError('unexpected mixed n3=4 zero-graph degree sequence')
    prior.need(frontier_counts == {'five-cycle':12,'four-cycle with pendant edge':60},
               'mixed n3=4 complete zero-graph types')
    templates = [((0,1),(1,2),(2,3),(3,4),(4,0)),
                 ((0,1),(1,2),(2,3),(3,0),(0,4))]
    relabeled = set()
    for template in templates:
        for p in permutations(range(5)):
            relabeled.add(prior.normalized_edges((p[a],p[b]) for a,b in template))
    prior.need(frontier_masks == relabeled, 'entry-level independent zero-graph templates')
    return {'zero_graph_masks_checked':checked,'zero_graphs':graph_rows,
            'cyclic_zero_masks_checked':16,'allowed_zero_corner_masks':masks,
            'allowed_ordinary_five_corner_masks':five_masks,
            'maximum_ordinary_fives_in_Q':2,
            'face_count_cases':rows,
            'all_zero_Q_at_most_one_for_n3_two_is_a_written_rotation_argument':True,
            'six_vertex_masks_checked':1 << len(six_pairs),
            'six_vertex_admitted_masks':sum(six_histogram.values()),
            'six_vertex_edge_histogram':six_histogram,'six_vertex_max_edges':max(six_histogram),
            'mixed_n3_five_degree_sum':mixed_degree_sum,
            'mixed_n3_five_boundary_capacity':mixed_capacity,
            'mixed_n3_five_required_edges':required,
            'mixed_n3_four_masks_checked':1 << len(five_pairs),
            'mixed_n3_four_zero_graph_types':frontier_counts,
            'mixed_n3_four_internal_edges':5,'mixed_n3_four_boundary_edges':6}


def lin(*coefficients):
    prior.need(len(coefficients) == 4, 'linear angle form dimensions')
    return tuple(F(a) for a in coefficients)


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def scale(k,a):
    return tuple(F(k)*x for x in a)


def angle_checks():
    # Formal linear variables pi, alpha, y, S. No numerical trigonometry.
    pi,alpha,y,S = (lin(*(int(i == j) for i in range(4))) for j in range(4))
    x,A0 = add(scale(2,pi),scale(-4,alpha)),add(scale(2,pi),scale(-2,alpha))
    no_edge_residual = add(add(scale(3,A0),scale(2,x)),scale(-4,pi))
    prior.need(no_edge_residual == lin(6,-14,0,0), 'noncontact-zero angle identity')
    forced_ratio = -no_edge_residual[0]/no_edge_residual[1]
    ratio_gap = forced_ratio-F(2,5)
    prior.need(forced_ratio == F(3,7) and ratio_gap == F(1,35),
               'noncontact-zero rational contradiction')

    one_zero_O = add(scale(2,add(A0,scale(-1,y))),x)
    one_zero_S = add(scale(6,pi),scale(-1,one_zero_O))
    prior.need(one_zero_O == lin(6,-8,-2,0) and one_zero_S == lin(0,8,2,0),
               'one-degree-three angle identities')
    pair_gap = add(scale(12,alpha),scale(-1,one_zero_S))
    prior.need(pair_gap == scale(2,add(scale(2,alpha),scale(-1,y))),
               'one-degree-three strict gap factor')

    contact_O = add(scale(4,pi),scale(-1,S))
    free_sum = add(add(scale(5,A0),scale(2,x)),scale(-1,contact_O))
    prior.need(free_sum == lin(10,-18,0,1), 'contact-zero free-Q angle identity')
    lower = add(lin(*free_sum[:3],0),scale(6*free_sum[3],alpha))
    prior.need(lower == lin(10,-12,0,0), 'contact-zero lower-bound substitution')
    lower_pi = lower[0]+lower[1]*F(2,5)
    pi_gap = lower_pi-5
    radical_gap = F(14,9)**2-2
    prior.need(lower_pi == F(26,5) and pi_gap == F(1,5) and radical_gap == F(34,81),
               'strict rational comparison margins')

    c,z = prior.variable(0),prior.variable(1)
    numerator = 1+c**2*z-c*(1+z)
    prior.need(not (numerator-(1-c)*(1-c*z)).terms,
               'adjacent-angle derivative numerator factorization')
    return {'linear_variable_order':['pi','alpha','y','S'],
            'n3_zero_noncontact_residual':[str(a) for a in no_edge_residual],
            'forced_alpha_over_pi':str(forced_ratio),'alpha_ratio_gap':str(ratio_gap),
            'n3_one_opposite_sum':[str(a) for a in one_zero_O],
            'n3_one_adjacent_zero_sum':[str(a) for a in one_zero_S],
            'n3_one_strict_gap_factor':'2(2alpha-y)>0',
            'n3_zero_contact_free_Q_sum':[str(a) for a in free_sum],
            'free_Q_sum_lower_pi_coefficient':str(lower_pi),
            'free_Q_sum_upper_pi_coefficient':'5','free_Q_sum_pi_gap':str(pi_gap),
            'square_margin_for_sqrt2_lt_14_over_9':str(radical_gap),
            'derivative_numerator_identity':'1+c^2 z-c(1+z)=(1-c)(1-c z)',
            'strict_trigonometric_inequalities_are_written_hand_proofs':True}


def legal(labels,edges):
    return labels.count('4/2') <= 1 and boundary.legal(labels,edges)


def cover():
    baseline = boundary.cover()
    rows, profiles = [], []
    for before in baseline['distributions']:
        d41,d42,d51 = before['d41'],before['d42'],before['d51']
        labels = ['4/1']*d41+['4/2']*d42+['5/1']*d51
        pairs = tuple(combinations(range(len(labels)),2))
        codes,signatures = set(),set()
        for mask in range(1 << len(pairs)):
            edges = frozenset(e for i,e in enumerate(pairs) if (mask >> i) & 1)
            if legal(labels,edges):
                codes.add(prior.code(labels,edges))
                signatures.add(prior.signature(labels,edges))
        independent = prior.component_cover(labels) if d51 == 0 and d42 <= 1 else set()
        prior.need(signatures == independent and len(codes) == len(signatures),
                   'independent colored component cover')
        prior.need(sorted(codes) == (before['allowed_H_codes'] if d42 <= 1 else []),
                   'entry-level prior H cover comparison')
        added = []
        if codes:
            # Independent direct generation from 15 vertices and degree sum 62.
            for n3,n4,n5 in product(range(16),repeat=3):
                if (n3+n4+n5 == 15 and 3*n3+4*n4+5*n5 == 62 and n4 >= d41+d42
                        and not (d42 == 1 and n3 == 5)):
                    added.append({'d41':d41,'d42':d42,'d51':d51,
                                  'n3':n3,'n4':n4,'n5':n5,'H_codes':sorted(codes)})
        profiles.extend(added)
        rows.append({'d41':d41,'d42':d42,'d51':d51,'allowed_H_codes':sorted(codes),
                     'surviving_degree_profiles':len(added)})
    def retained_profile(p):
        return p['d42'] <= 1 and not (p['d42'] == 1 and p['n3'] == 5)
    retained = [deepcopy(p) for p in baseline['profiles'] if retained_profile(p)]
    prior.need(profiles == retained, 'entry-level direct degree-sum cover comparison')
    removed = [p for p in baseline['profiles'] if not retained_profile(p)]
    prior.need([p['n3'] for p in removed if p['d42'] == 2] == [0,1,2]
               and [p['n3'] for p in removed if p['d42'] == 1] == [5],
               'removed zero-triangle profiles')
    prior.need(len(profiles) == 10 and sum(len(r['allowed_H_codes']) for r in rows) == 11
               and sum(bool(r['allowed_H_codes']) for r in rows) == 2, 'cover totals')
    return {'previous_degree_profiles':14,'remaining_degree_profiles':10,
            'previous_colored_H_types':13,'remaining_colored_H_types':11,
            'remaining_deficit_distributions':2,
            'restriction':'All degree fives ordinary; two zero-triangle fours impossible; mixed profile n3=5 impossible',
            'removed_profiles':removed,'distributions':rows,'profiles':profiles}


def selftest():
    controls = 0
    def test(condition,message):
        nonlocal controls
        prior.need(condition,message)
        controls += 1
    test(not face_allowed(5), 'opposite zeros without all-zero face rejected')
    test(not face_allowed(7), 'three-zero face rejected')
    test(face_allowed(15), 'four-zero face retained in local rule')
    test(not five_allowed(3), 'adjacent ordinary fives rejected')
    test(five_allowed(5), 'opposite ordinary fives retained')
    for mask in [-1,16,True]:
        try:
            face_allowed(mask)
        except ValueError:
            controls += 1
        else:
            raise ValueError('malformed corner mask accepted')
    test(allocations(1,1,0) == [], 'negative free-face count rejected')
    test(allocations(2,4,1) == [{'a':1,'f0':1,'f1':2,'f2':4}],
         'all-zero Q forced by complete face equations')
    for edges in [frozenset(),frozenset([(0,1)])]:
        labels = ['4/2','4/2']
        test(boundary.legal(labels,edges), 'two-zero H type existed in prior stage')
        test(not legal(labels,edges), 'two-zero H type now excluded')
    test(legal(['4/1']*4,prior.normalized_edges(((0,1),(1,2),(2,3),(3,0)))),
         'all-one-deficit four-cycle retained')
    test(legal(['4/1','4/1','4/2'],prior.normalized_edges(((0,2),(1,2)))),
         'mixed all-four path retained')
    k23 = frozenset((a,b) for a in (0,1) for b in (2,3,4))
    test(not boundary.zero_graph_allowed(6,k23), 'six-vertex common-neighbor obstruction')
    example = prior.normalized_edges(((0,1),(1,2),(2,3),(3,4),(4,0),(5,0),(5,2)))
    test(boundary.zero_graph_allowed(6,example), 'seven-edge six-vertex graph is admitted')
    return controls


def main():
    prior.need(sys.argv[1:] in ([],['--selftest']), 'usage: check_two_zeros.py [--selftest]')
    incidence,angles,remaining = incidence_checks(),angle_checks(),cover()
    if sys.argv[1:]:
        print(json.dumps({'status':'PASS','controls':selftest(),'degree_profiles':10,
                          'colored_H_types':11,'zero_graph_masks':74},sort_keys=True))
    else:
        print(json.dumps({'agent':'six-tammes-1','role':'researcher',
                          'scope':'exact incidence/angle arithmetic and necessary cover; written geometry separate',
                          'incidence_checks':incidence,'angle_checks':angles,
                          'cover':remaining},indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
