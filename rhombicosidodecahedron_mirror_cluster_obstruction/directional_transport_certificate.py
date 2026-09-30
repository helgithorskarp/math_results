#!/usr/bin/env python3
"""Exact hypotheses for DIRECTIONAL_TRANSPORT_PROOF.md; Python 3.11+ stdlib.

Replays the entire adaptive certificate. Regenerates long-edge height/gaps,
unique center-corner preimages, and the proper C3 plus planar-half-turn gauge.
All radical bounds use exact Q(phi) comparisons on the inherited rational grid.
The continuous transport and whole-polygon arguments are proved in prose.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from verify import PHI,QPhi,ZERO,act,dot,matmul,vertices,require
from torque_certificate import cross,subtract,determinant
from cell_certificate import geometry,encode,decode
from global_cap_certificate import circle_map,expect_rejection
from linear_roll_certificate import project,exact_hull,validate_polygon
from adaptive_receiver_certificate import (
    DEN,check as check_previous,check_roll_branch,example_corners,
    point_enclosures,root_bounds,rational_strings)

AXIS=(ZERO,QPhi(1),-PHI**2)
I=tuple(tuple(QPhi(int(i==j)) for j in range(3)) for i in range(3))


def corner_preimages(V,d):
    require(V==vertices() and d==AXIS, 'standard vertices and directed axis required')
    projected={project(v,d):v for v in sorted(V)}
    require(len(projected)==len(V)==60, 'center projection must have unique preimages')
    rho2=QPhi(F(20,3))+8*PHI
    return {p:v for p,v in projected.items() if dot(p,p)==rho2}


def validate_preimages(V,d,P):
    require(V==vertices() and d==AXIS and len(P)==12, 'complete twelve corner preimages required')
    require(P==corner_preimages(V,d), 'incorrect center corner preimage')
    require(all(v in V and project(v,d)==p and
                dot(v,d)**2/dot(d,d)==QPhi(F(1,3)) for p,v in P.items()),
            'center corner axial height is not exactly c0')


def axial_matrices(d):
    N=dot(d,d)
    X=tuple(tuple(cross(d,I[j])[i] for j in range(3)) for i in range(3))
    c=QPhi(F(-1,2))
    return (I,)+tuple(tuple(tuple(c*I[i][j]+(1-c)*d[i]*d[j]/N+
                                      sign*(PHI-1)*X[i][j]/2
                                for j in range(3)) for i in range(3))
                      for sign in (-1,1))


def validate_gauge(V,d,P,matrices):
    validate_preimages(V,d,P)
    require(len(matrices)==3 and len(set(matrices))==3 and I in matrices,
            'complete C3 body matrices required')
    require(dot(d,d)==3*PHI**2, 'Rodrigues axial normalization identity')
    S={project(v,d) for v in V}
    p=min(P)
    rho2=dot(p,p)
    rolls=set()
    records=[]
    tests=0
    for g in matrices:
        require(matmul(g,tuple(zip(*g)))==I and determinant(*zip(*g))==QPhi(1),
                'body gauge is not a proper rotation')
        require(act(g,d)==d and matmul(matmul(g,g),g)==I,
                'body gauge must fix directed axis and have order dividing three')
        require({act(g,v) for v in V}==V, 'body gauge fails on original vertex set')
        for sign in (-1,1):
            q=tuple(sign*x for x in act(g,p))
            c,t,rotate=circle_map(d,rho2,p,q)
            require(all(rotate(x)==tuple(sign*y for y in act(g,x)) for x in S),
                    'planar rotation differs from signed body action')
            require({rotate(x) for x in S}==S and {rotate(x) for x in P}==set(P),
                    'gauge fails to preserve whole shadow and corner set')
            for x,v in P.items():
                image=tuple(sign*y for y in act(g,v))
                require(P[rotate(x)]==image, 'corner preimage permutation does not commute')
            tests+=len(S)
            rolls.add((c,t))
            records.append({'body_matrix':[encode(row) for row in g],
                            'source_planar_halfturn_sign':sign,
                            'planar_cosine':c.encode(),'planar_sine_over_axis_norm':t.encode()})
    expected={(QPhi(1),ZERO),(QPhi(-1),ZERO)}
    expected.update((QPhi(c),sign*(PHI-1)/2)
                    for c in (F(1,2),F(-1,2)) for sign in (-1,1))
    require(rolls==expected and tests==360, 'signed C3 action must realize complete C6')
    return {'proper_body_matrices':3,'proper_body_vertex_permutation_checks':180,
            'signed_planar_rotation_actions':6,'projected_vertex_action_checks':tests,
            'corner_preimage_action_checks':72,'all_corner_squared_axial_heights':'1/3',
            'actions':records}


def validate_long_heights(V,d,edges,delta=F(1,2)):
    require(V==vertices() and d==AXIS and len(edges)==6,
            'complete standard long-edge height audit required')
    canonical=validate_polygon(V,d,exact_hull({project(v,d) for v in V},d))
    expected=[e for e in canonical['complete_oriented_edges']
              if QPhi(*(F(q) for q in e['squared_unit_tangential_derivative']))==QPhi(F(5,3))]
    require(edges==expected, 'long-edge list differs from regenerated outward hull')
    require(delta>0, 'positive receiver transport range required')
    klo,_=root_bounds(QPhi(F(5,3)))
    ratios=[]
    records=[]
    checks=0
    for edge in edges:
        p,m=decode(edge['p']),decode(edge['outward_normal'])
        mm=dot(m,m)
        ties=[]
        count=0
        for v in sorted(V):
            checks+=1
            gap=dot(m,subtract(p,v))
            require(gap>=0, 'negative original-vertex supporting gap')
            H2=dot(d,v)**2/dot(d,d)
            if gap==ZERO:
                require(H2<=QPhi(F(5,3)), 'long-edge tie exceeds kappa axial height')
                ties.append(H2)
            if H2>QPhi(F(5,3)):
                Hhi=root_bounds(H2)[1]
                gaplo=root_bounds(gap*gap/mm)[0]
                require(Hhi>klo and gaplo>delta*(Hhi-klo),
                        'long-edge strict gap fails to absorb excess axial height')
                ratios.append(gaplo/(Hhi-klo))
                count+=1
        require(len(ties)==4 and max(ties)==QPhi(F(5,3)), 'complete sharp tied axial heights')
        records.append({'outward_normal':edge['outward_normal'],
                        'tied_original_squared_axial_heights':[q.encode() for q in sorted(ties)],
                        'higher_height_strict_gap_comparisons':count})
    require(checks==360 and len(ratios)==216, 'incomplete long-edge height/gap coverage')
    return {'regenerated_long_edges':6,'original_vertex_height_support_checks':checks,
            'all_long_edge_original_ties':24,'maximum_tied_squared_axial_height':'5/3',
            'higher_height_strict_gap_comparisons':len(ratios),
            'receiver_normal_chord_range':delta,
            'minimum_gap_over_excess_axial_height_lower':min(ratios),'edges':records}


def check_general_constants():
    a=F(101,200)*(F(7,12)-F(2,5))
    threshold=F(77,1000)
    oldrange=F(1,50)
    checks={
        'c0_less_than_seven_over_twelve':F(1,3)<F(7,12)**2,
        'beta_greater_than_four_over_twentyfive':(19-8*PHI)/29>QPhi(F(4,25)),
        'source_chord_below_one_tenth':a<F(1,10),
        'kappa_greater_than_one':F(5,3)>1,
        'error_threshold_implies_receiver_chord_below_one_tenth':threshold<F(1,10),
        'error_threshold_implies_receiver_chord_within_height_gap_audit':threshold<F(1,2),
        'full_relative_angle_below_one':F(101,100)*(a+2*threshold)<1,
        'vertex_radius_between_four_and_nine_over_two':QPhi(16)<7+8*PHI<QPhi(F(81,4)),
        'old_adaptive_error_implies_both_chords_below_one_over_fifty':threshold/4<oldrange,
        'c0_less_than_three_over_five':F(1,3)<F(3,5)**2,
        'kappa_less_than_thirteen_over_ten':F(5,3)<F(13,10)**2,
        'source_directional_coefficient_below_R':F(3,5)+F(9,4)*oldrange<4,
        'receiver_directional_coefficient_below_R':F(13,10)+F(9,4)*oldrange<4,
    }
    require(all(checks.values()), 'directional criterion or generalization constants fail')
    return {'unconditional_winning_region_source_chord_upper':a,
            'criterion_generalizes_every_previous_adaptive_receiver':True,'checks':checks}


def check_cap_constants(delta=F(1,100)):
    R=F(9,2)
    source=F(23,10)*delta
    error=F(67,25)*delta+F(5661,400)*delta*delta
    theta=F(101,100)*(F(33,10)*delta+error)
    theta_bound=F(63,10)*delta
    B=geometry()[0][0][1]
    margin=F(3,5)-27*delta-5*theta_bound
    checks={
        'positive_radius':delta>0,
        'receiver_axial_value_above_one_half':F(4,7)-R*delta>F(1,2),
        'source_chord_coefficient_valid':F(101,200)*R<F(23,10),
        'directional_error_coefficients_valid':
            F(3,5)*F(23,10)+F(13,10)==F(67,25) and
            R/2*(F(23,10)**2+1)==F(5661,400),
        'directional_error_within_roll_branch':error<=F(77,1000),
        'factor_chords_below_one_tenth':max(source,delta,error)<F(1,10),
        'full_angle_coefficient_valid':theta<theta_bound,
        'full_angle_below_one':theta_bound<1,
        'strict_chamber_separation_allows_closed_cap':delta<=F(1,100),
        'strict_center_z_margin_allows_closed_cap':F(4,5)-delta>=F(79,100),
        'chart_error_below_three_delta':F(9,4)/F(79,100)<3,
        'receiver_stays_in_closed_ABD':3*delta<F(1,10),
        'center_chart_norm_below_twentyseven_over_twentyfive':dot(B,B)<QPhi(F(27,25)**2),
        'perturbed_chart_norm_below_ten_over_nine':F(27,25)+3*delta<F(10,9),
        'support_remainder_coefficient_at_most_ten':2*R*F(10,9)<=10,
        'sharp_center_ball_above_three_over_five':PHI-1>QPhi(F(3,5)),
        'strict_torque_margin_positive':margin>0,
    }
    require(all(checks.values()), 'directional closed receiver cap constants fail')
    return {'receiver_normal_chord_radius':delta,'source_normal_chord_upper':source,
            'directional_long_support_error_upper':error,
            'full_relative_angle_upper':theta_bound,
            'unsimplified_full_relative_angle_upper':theta,
            'strict_torque_margin_lower':margin,'checks':checks}


def larger_corners(k=60):
    A,B,D=geometry()[0][0]
    L=(ZERO,B[1]-QPhi(F(1,k)),QPhi(1))
    C=tuple(F(19,20)*b+F(1,20)*d for b,d in zip(B,D))
    return B,L,C


def check_patch(corners=None):
    default=corners is None
    if default:
        corners=larger_corners()
    require(len(corners)==3 and len(set(corners))==3, 'complete distinct receiver triangle required')
    A,B,D=geometry()[0][0]
    normal=cross(subtract(corners[1],corners[0]),subtract(corners[2],corners[0]))
    require(dot(normal,normal)>0, 'receiver triangle is degenerate')
    barycentric=[]
    for u in corners:
        require(u[2]==QPhi(1), 'receiver triangle outside unit-z chart')
        wD=u[0]/D[0]
        wB=(u[1]-wD*D[1])/B[1]
        wA=1-wB-wD
        require(min(wA,wB,wD)>=0, 'receiver triangle outside closed ABD')
        barycentric.append([q.encode() for q in (wA,wB,wD)])
    data=[point_enclosures(u,B,vertices()) for u in corners]
    f_lower=min(p['axial_value'][0] for p in data)
    delta=max(p['normal_chord'][1] for p in data)
    chart=max(p['chart_norm'][1] for p in data)
    drift=max(p['chart_displacement'][1] for p in data)
    R=root_bounds(7+8*PHI)[1]
    c0=root_bounds(QPhi(F(1,3)))[1]
    kappa=root_bounds(QPhi(F(5,3)))[1]
    a=F(101,200)*(c0-f_lower)
    error=c0*a+kappa*delta+R*(a*a+delta*delta)/2
    theta=F(101,100)*(a+delta+error)
    center=root_bounds(2-PHI)[0]
    margin=center-R*chart*theta-2*R*drift
    checks={
        'common_sixty_vertex_strict_axial_signs':all(p['all_sixty_axial_signs_match_center'] for p in data),
        'axial_lower_clears_region_gap':QPhi(f_lower*f_lower)>(19-8*PHI)/29,
        'nonnegative_source_deficit_bound':a>=0,
        'positive_normal_cap_cone_coefficient':1-delta*delta/2>0,
        'receiver_chord_within_height_gap_audit':delta<=F(1,2),
        'directional_error_within_roll_branch':error<=F(77,1000),
        'all_factor_chords_below_one_tenth':max(a,delta,error)<F(1,10),
        'sum_of_factor_angles_below_one':theta<1,
        'strict_torque_margin_positive':margin>0,
    }
    require(all(checks.values()), 'directional whole receiver triangle criterion fails')
    comparison={}
    if default:
        oldB,oldL,oldC=example_corners()
        require(oldB==B and oldL==tuple(b+F(60,163)*(l-b) for b,l in zip(B,corners[1])) and
                oldC==tuple(b+F(1,2)*(c-b) for b,c in zip(B,corners[2])),
                'previous receiver triangle is not inside the stated larger triangle')
        oldnormal=cross(subtract(oldL,B),subtract(oldC,B))
        require(normal==tuple(F(163,30)*x for x in oldnormal), 'chart triangle area ratio fails')
        require(data[1]['normal_chord'][0]>F(1,70) and margin>F(1,20),
                'stated receiver triangle extent or margin fails')
        comparison={'contains_entire_previous_receiver_triangle':True,
                    'unit_z_chart_area_ratio_to_previous_triangle':'163/30',
                    'spherical_area_ratio_claimed':False,
                    'second_corner_normal_chord_greater_than_one_over_seventy':True,
                    'strict_torque_margin_greater_than_one_over_twenty':True}
    return {'entire_closed_receiver_triangle_excludes_every_source':True,
            'corners':data,'corner_barycentric_coordinates_in_ABD':barycentric,
            'all_patch_axial_value_lower':f_lower,'all_patch_normal_chord_upper':delta,
            'all_patch_chart_norm_upper':chart,'all_patch_chart_displacement_upper':drift,
            'source_normal_chord_upper':a,'directional_long_support_error_upper':error,
            'full_relative_angle_upper':theta,'strict_torque_margin_lower':margin,
            'comparison_to_previous_triangle':comparison,'checks':checks}


def check(self_test=False):
    previous=check_previous(self_test)
    path=Path(__file__).with_name('adaptive_receiver_expected.json')
    require(previous==json.loads(path.read_text()), 'inherited complete adaptive output changed')
    V=vertices()
    H=exact_hull({project(v,AXIS) for v in V},AXIS)
    polygon=validate_polygon(V,AXIS,H)
    edges=[e for e in polygon['complete_oriented_edges']
           if QPhi(*(F(q) for q in e['squared_unit_tangential_derivative']))==QPhi(F(5,3))]
    heights=validate_long_heights(V,AXIS,edges)
    P=corner_preimages(V,AXIS)
    matrices=axial_matrices(AXIS)
    gauge=validate_gauge(V,AXIS,P,matrices)
    general=check_general_constants()
    cap=check_cap_constants()
    patch=check_patch()
    branch=check_roll_branch()
    if self_test:
        expect_rejection(lambda:validate_long_heights(V-{min(V)},AXIS,edges))
        expect_rejection(lambda:validate_long_heights(V,AXIS,edges[:-1]))
        bad=[dict(e) for e in edges]
        bad[0]['outward_normal']=encode(tuple(-q for q in decode(bad[0]['outward_normal'])))
        expect_rejection(lambda:validate_long_heights(V,AXIS,bad))
        expect_rejection(lambda:validate_long_heights(V,AXIS,edges,F(3,5)))
        expect_rejection(lambda:validate_preimages(V,AXIS,{p:v for p,v in P.items() if p!=min(P)}))
        badP=dict(P)
        badP[min(P)]=tuple(-q for q in P[min(P)])
        expect_rejection(lambda:validate_preimages(V,AXIS,badP))
        expect_rejection(lambda:validate_gauge(V,AXIS,P,matrices[:-1]))
        badM=(tuple(tuple(-q for q in row) for row in I),)+matrices[1:]
        expect_rejection(lambda:validate_gauge(V,AXIS,P,badM))
        expect_rejection(lambda:check_cap_constants(F(1,90)))
        expect_rejection(lambda:check_patch(larger_corners()[:-1]))
        expect_rejection(lambda:check_patch(larger_corners(20)))
    return rational_strings({
        'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_analytic_theorem_with_exact_finite_and_radical_hypotheses',
        'global_non_rupert_proved':False,
        'arbitrary_source_orientation_roll_translation_scale_ge_one':True,
        'closed_receiver_cap_chord_radius':'1/100','unoriented_receiver_axes':10,
        'cap_radius_improvement_over_adaptive_predecessor':2,
        'directional_receiver_and_whole_polygon_criterion_proved':True,
        'directional_error_formula':'c0*a+sqrt(5/3)*delta+(R/2)*(a*a+delta*delta)',
        'long_edge_axial_heights_and_support_gaps':heights,
        'center_corner_preimages':[{'projected_corner':encode(p),'original_vertex':encode(v)}
                                   for p,v in sorted(P.items())],
        'proper_body_and_planar_halfturn_gauge':gauge,
        'general_criterion_constants':general,'concavity_roll_branch':branch,
        'cap_constants':cap,'larger_receiver_triangle':patch,
        'radical_enclosure_grid_denominator':DEN,
        'new_malformed_controls_rejected':11 if self_test else 0,
        'inherited_malformed_controls_replayed':22 if self_test else 0,
        'inherited_adaptive_expected_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'inherited_adaptive_graph':'bafkreicsflhs33t2yft342slfzk46vnr55unjj3uf6pnmsaxmtgum6rvz4',
        'inherited_linear_roll_graph':'bafkreih2r7gsrai6kr32c2vapf5v5debgmkr2ri3n2uysvdtmfgxp3mbtm'})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),indent=2,sort_keys=True))
