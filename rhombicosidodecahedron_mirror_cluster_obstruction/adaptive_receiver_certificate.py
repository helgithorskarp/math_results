#!/usr/bin/env python3
"""Exact finite and radical hypotheses for ADAPTIVE_RECEIVER_PROOF.md.

Python 3.11+ standard library. All radicals are enclosed on a fixed rational
grid of denominator 10^12 by exact Q(phi) sign comparisons. No floating point.
Continuous source elimination and convex patch coverage are proved in prose.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from verify import PHI,QPhi,ZERO,dot,vertices,require
from torque_certificate import cross,subtract,determinant
from cell_certificate import geometry,encode,decode
from global_cap_certificate import expect_rejection
from linear_roll_certificate import check as check_previous

DEN=10**12


def verify_root(q,lo,hi):
    require(0<=lo<=hi and QPhi(lo*lo)<=q<=QPhi(hi*hi), 'invalid root enclosure')


def root_bounds(q):
    require(q>=0, 'negative root argument')
    if q==ZERO:
        return F(0),F(0)
    lo,hi=0,DEN
    while QPhi(F(hi*hi,DEN*DEN))<q:
        hi*=2
    while hi-lo>1:
        m=(lo+hi)//2
        z=QPhi(F(m*m,DEN*DEN))
        if z==q:
            return F(m,DEN),F(m,DEN)
        if z<q:
            lo=m
        else:
            hi=m
    a,b=F(lo,DEN),F(hi,DEN)
    verify_root(q,a,b)
    return a,b


def regenerate_probes(V,U):
    edges=[]
    distances=[]
    for p,q in combinations(sorted(V),2):
        e=subtract(q,p)
        s2=dot(e,e)
        require(s2>=QPhi(4), 'shorter pair than standard edge')
        distances.append(','.join(s2.encode()))
        if s2==QPhi(4):
            edges.append((p,q))
    require(len(edges)==120, 'complete standard edge count')
    require(all(sum(v in e for e in edges)==4 for v in V), 'standard vertex degree')
    probes=[]
    decisions=[]
    tested=0
    for p,q in edges:
        for e in (subtract(q,p),subtract(p,q)):
            gaps=[dot(cross(e,u),subtract(p,w)) for u in U for w in sorted(V)]
            tested+=len(gaps)
            good=all(g>=0 for g in gaps)
            decisions.append('1' if good else '0')
            if good:
                probes.extend([(p,e),(q,e)])
    require(len(probes)==36 and tested==43200, 'persistent probe enumeration')
    return probes,{'vertex_pair_distances':len(distances),
                   'nearest_neighbor_edges':len(edges),'tested_corner_support_gaps':tested,
                   'qualified_oriented_edges':len(probes)//2,
                   'candidate_decision_sha256':hashlib.sha256(''.join(decisions).encode()).hexdigest()}


def validate_probes(V,U,probes):
    require(V==vertices() and len(probes)==36 and len(set(probes))==36,
            'complete distinct persistent probes required')
    for v,e in probes:
        require(v in V and dot(e,e)==QPhi(4), 'invalid endpoint/edge')
        require(tuple(x+y for x,y in zip(v,e)) in V or subtract(v,e) in V,
                'edge lacks second original endpoint')
        for u in U:
            require(all(dot(cross(e,u),subtract(v,w))>=0 for w in V),
                    'persistent support fails on an original vertex')


def center_torque_facets(probes,B):
    T=sorted({cross(v,cross(e,B)) for v,e in probes})
    require(len(T)==18, 'complete center torque set')
    # The previously used tetrahedron is a subset, with a full positive stress.
    prior=json.loads(Path(__file__).with_name('cell_probes.json').read_text())[0]
    P=[(decode(p['vertex']),decode(p['edge'])) for p in prior['probes']]
    require(all(p in probes for p in P), 'prior interior tetrahedron missing')
    W=[cross(v,cross(e,B)) for v,e in P]
    lam=[(-1)**j*determinant(*(W[k] for k in range(4) if k!=j)) for j in range(4)]
    require(all(q>0 for q in lam), 'origin interior stress is not positive')
    require(all(sum((lam[j]*W[j][k] for j in range(4)),ZERO)==ZERO
                for k in range(3)), 'origin interior stress does not balance')
    facets=set()
    tests=triples=0
    for a,b,c in combinations(T,3):
        triples+=1
        n=cross(subtract(b,a),subtract(c,a))
        require(dot(n,n)>0, 'unexpected degenerate torque triple')
        h=dot(n,a)
        gaps=[dot(n,t)-h for t in T]
        tests+=len(gaps)
        if all(g<=0 for g in gaps):
            require(h>0, 'facet contradicts interior origin')
            facets.add(tuple(q/h for q in n))
        elif all(g>=0 for g in gaps):
            require(h<0, 'facet contradicts interior origin')
            facets.add(tuple(q/h for q in n))
    require(triples==816 and tests==14688 and len(facets)==15,
            'incomplete facet enumeration')
    validate_facets(T,facets)
    return T,facets,{'center_distinct_torques':len(T),'torque_triples':triples,
                    'torque_triple_support_comparisons':tests,'center_facet_planes':len(facets),
                    'sharp_center_squared_ball_radius':(2-PHI).encode(),
                    'sharp_center_ball_radius':(PHI-1).encode(),
                    'prior_positive_interior_stress_rechecked':True}


def validate_facets(T,facets):
    require(len(T)==18 and len(facets)==15, 'incomplete torque/facet set')
    for n in facets:
        require(all(dot(n,t)<=QPhi(1) for t in T), 'invalid torque support facet')
        require(sum(dot(n,t)==QPhi(1) for t in T)>=3, 'facet lacks three contacts')
        require(QPhi(1)/dot(n,n)>=2-PHI, 'torque ball radius overestimated')
    require((PHI,ZERO,ZERO) in facets, 'sharp x facet missing')
    require(sum(dot((PHI,ZERO,ZERO),t)==QPhi(1) for t in T)==4,
            'sharp facet needs all four torque contacts')
    require((PHI-1)**2==2-PHI, 'golden-ratio radius identity')


def check_roll_branch(threshold=F(77,1000)):
    k=F(12909,10000)
    h=F(42361,10000)
    sqrt3=F(433,250)
    endpoint=k/2-h*(1-sqrt3/2)
    r0=F(1,10)
    at_r0=k*r0*F(99,100)-h*r0*r0/2
    checks={
        'long_derivative_lower':k*k<F(5,3),
        'long_support_upper':1+2*PHI<QPhi(h),
        'sqrt_three_lower':sqrt3*sqrt3<3,
        'pi_over_six_gap_above_threshold':endpoint>threshold,
        'one_tenth_roll_chord_gap_above_threshold':at_r0>threshold,
        'half_roll_cosine_above_ninety_nine_hundredths':1-r0*r0/4>F(99,100)**2,
        'near_identity_gap_per_chord_above_one':F(5,4)*F(99,100)-F(17,4)/20>1,
        'coarse_derivative_lower':F(5,4)**2<F(5,3),
        'coarse_support_upper':1+2*PHI<QPhi(F(17,4)),
        'angle_over_chord_bound_to_one_tenth':F(101,100)**2*(1-F(1,400))>1,
    }
    require(threshold>0 and all(checks.values()), 'roll branch threshold not certified')
    return {'one_sided_error_threshold':str(threshold),
            'roll_chord_per_error_upper':'1',
            'pi_over_six_support_gap_lower':str(endpoint),
            'one_tenth_chord_support_gap_lower':str(at_r0),
            'near_identity_support_slope_lower':'41/40','checks':checks}


def check_cap_constants(delta=F(1,200)):
    R=F(9,2)
    gamma=F(101,100)
    source=F(23,10)*delta
    eta=F(297,20)*delta
    theta=F(37,2)*delta
    B=geometry()[0][0][1]
    beta=(19-8*PHI)/29
    checks={
        'vertex_radius_between_four_and_nine_over_two':QPhi(16)<7+8*PHI<QPhi(R*R),
        'c0_between_four_over_seven_and_three_over_five':F(4,7)**2<F(1,3)<F(3,5)**2,
        'nonoptimal_region_bound_between_four_over_twentyfive_and_one_over_four':
            QPhi(F(4,25))<beta<QPhi(F(1,4)),
        'receiver_axial_value_above_one_half':F(4,7)-R*delta>F(1,2),
        'source_deficit_below_one_fifth':F(3,5)-F(2,5)==F(1,5),
        'source_chord_coefficient_valid':gamma/2*R<F(23,10),
        'source_chord_from_sine_valid':F(2,1)/F(199,100)<gamma*gamma,
        'roll_branch_error_threshold':eta<=F(77,1000),
        'factor_chords_below_one_tenth':max(source,delta,eta)<F(1,10),
        'full_angle_coefficient_valid':gamma*(F(23,10)+1+F(297,20))<F(37,2),
        'sum_of_factor_angles_below_one':theta<1,
        'receiver_cap_keeps_its_chamber_center':delta<F(1,100),
        'center_chart_norm_below_five_over_four':dot(B,B)<QPhi(F(25,16)),
        'chart_normal_z_lower':F(4,5)-delta>F(79,100),
        'chart_error_below_three_delta':F(9,4)/F(79,100)<3,
        'receiver_stays_in_closed_ABD':3*delta<F(1,10),
        'center_chart_norm_below_twentyseven_over_twentyfive':dot(B,B)<QPhi(F(27,25)**2),
        'perturbed_chart_norm_below_ten_over_nine':F(27,25)+3*delta<F(10,9),
        'support_remainder_coefficient_at_most_ten':2*R*F(10,9)<=10,
        'sharp_center_ball_above_three_over_five':PHI-1>QPhi(F(3,5)),
        'torque_ball_perturbation_coefficient':2*R*3==27,
        'actual_torque_ball_positive':F(3,5)-27*delta>0,
        'torque_remainder_margin_positive':F(3,5)-27*delta-5*theta>0,
    }
    require(delta>0 and all(checks.values()), 'receiver cap constants not certified')
    return {'receiver_normal_chord_radius':str(delta),
            'source_normal_chord_upper':str(source),
            'one_sided_shadow_error_upper':str(eta),
            'full_relative_angle_upper':str(theta),
            'center_ball_radius_lower':'3/5',
            'actual_ball_radius_lower':str(F(3,5)-27*delta),
            'support_remainder_coefficient_upper':'10',
            'strict_torque_margin_lower':str(F(3,5)-27*delta-5*theta),
            'checks':checks}


def point_enclosures(u,B,V):
    N=dot(u,u)
    N0=dot(B,B)
    p=dot(u,B)
    require(N>0 and p>0, 'invalid directed normal branch')
    s2=(N*N0-p*p)/(N*N0)
    require(ZERO<=s2<QPhi(1), 'invalid squared normal sine')
    cl,ch=root_bounds(1-s2)
    # Stable exact identity for the chord; no subtraction of near-unit roots.
    dl=root_bounds(2*s2/(1+ch))[0]
    dh=root_bounds(2*s2/(1+cl))[1]
    require(all(dot(u,v).sign()==dot(B,v).sign()!=0 for v in V),
            'receiver corners do not share a strict axial sign region')
    axial=min(dot(u,v)**2/N for v in V)
    require(axial>(19-8*PHI)/29, 'receiver corner does not clear the region gap')
    require(axial<=QPhi(F(1,3)), 'inherited global axial maximum contradicted')
    return {'u':encode(u),'normal_chord':(dl,dh),'axial_value':root_bounds(axial),
            'chart_norm':root_bounds(N),
            'chart_displacement':root_bounds(dot(subtract(u,B),subtract(u,B))),
            'squared_axial_value':axial.encode(),
            'all_sixty_axial_signs_match_center':True,
            'squared_axial_value_exceeds_nonoptimal_region_bound':True}


def example_corners(k=163):
    A,B,D=geometry()[0][0]
    L=(ZERO,B[1]-QPhi(F(1,k)),QPhi(1))
    C=tuple(F(39,40)*b+F(1,40)*d for b,d in zip(B,D))
    return (B,L,C)


def check_patch(corners=None):
    default=corners is None
    if default:
        corners=example_corners()
    require(len(corners)==3 and len(set(corners))==3, 'complete distinct triangle corners required')
    A,B,D=geometry()[0][0]
    require(dot(cross(subtract(corners[1],corners[0]),
                      subtract(corners[2],corners[0])),
                cross(subtract(corners[1],corners[0]),
                      subtract(corners[2],corners[0])))>0,
            'receiver triangle has zero area')
    barycentric=[]
    for u in corners:
        require(u[2]==QPhi(1), 'receiver corner outside unit-z chart')
        wD=u[0]/D[0]
        wB=(u[1]-wD*D[1])/B[1]
        wA=1-wB-wD
        require(min(wA,wB,wD)>=0, 'receiver corner outside closed ABD')
        barycentric.append([q.encode() for q in (wA,wB,wD)])
    data=[point_enclosures(u,B,vertices()) for u in corners]
    f_lower=min(p['axial_value'][0] for p in data)
    delta=max(p['normal_chord'][1] for p in data)
    chart=max(p['chart_norm'][1] for p in data)
    drift=max(p['chart_displacement'][1] for p in data)
    R=root_bounds(7+8*PHI)[1]
    c0=root_bounds(QPhi(F(1,3)))[1]
    a=F(101,200)*(c0-f_lower)
    eta=R*(a+delta)
    theta=F(101,100)*(a+delta+eta)
    center=root_bounds(2-PHI)[0]
    margin=center-R*chart*theta-2*R*drift
    checks={'shared_axial_sign_region':all(p['all_sixty_axial_signs_match_center'] for p in data),
            'positive_axial_lower':f_lower>0,
            'axial_lower_clears_region_gap':QPhi(f_lower*f_lower)>(19-8*PHI)/29,
            'nonnegative_source_deficit_bound':a>=0,
            'normal_cap_cone_coefficient_positive':1-delta*delta/2>0,
            'roll_branch_error_threshold':eta<=F(77,1000),
            'all_factor_chords_below_one_tenth':max(a,delta,eta)<F(1,10),
            'sum_of_factor_angles_below_one':theta<1,
            'strict_torque_margin_positive':margin>0}
    require(all(checks.values()), 'adaptive receiver triangle criterion fails')
    outside=data[1]['normal_chord'][0]>F(1,190)
    if default:
        require(outside and margin>F(1,10), 'stated triangle comparison/margin fails')
    return {'complete_closed_projective_triangle_excludes_all_sources':True,
            'corners':data,'corner_barycentric_coordinates_in_ABD':barycentric,
            'all_patch_axial_value_lower':f_lower,'all_patch_normal_chord_upper':delta,
            'all_patch_chart_norm_upper':chart,'all_patch_chart_displacement_upper':drift,
            'source_normal_chord_upper':a,'one_sided_shadow_error_upper':eta,
            'full_relative_angle_upper':theta,'sharp_center_ball_radius_lower':center,
            'strict_torque_margin_lower':margin,
            'second_corner_outside_chord_cap_radius_one_over_190':outside,
            'checks':checks}


def rational_strings(x):
    if isinstance(x,F):
        return str(x)
    if isinstance(x,dict):
        return {k:rational_strings(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):
        return [rational_strings(v) for v in x]
    return x


def check(self_test=False):
    previous=check_previous(self_test)
    path=Path(__file__).with_name('linear_roll_expected.json')
    require(previous==json.loads(path.read_text()), 'inherited complete roll output changed')
    V=vertices()
    U=geometry()[0][0]
    B=U[1]
    probes,enumeration=regenerate_probes(V,U)
    validate_probes(V,U,probes)
    T,facets,torque=center_torque_facets(probes,B)
    roll=check_roll_branch()
    cap=check_cap_constants()
    patch=check_patch()
    if self_test:
        expect_rejection(lambda:validate_probes(V,U,probes[:-1]))
        bad=list(probes)
        v,e=bad[0]
        bad[0]=(v,tuple(-q for q in e))
        expect_rejection(lambda:validate_probes(V,U,bad))
        expect_rejection(lambda:validate_facets(T,facets-{(PHI,ZERO,ZERO)}))
        bad_facets=set(facets)
        q=next(iter(sorted(bad_facets)))
        bad_facets.remove(q)
        bad_facets.add(tuple(-x for x in q))
        expect_rejection(lambda:validate_facets(T,bad_facets))
        expect_rejection(lambda:check_roll_branch(F(2,25)))
        expect_rejection(lambda:check_cap_constants(F(1,150)))
        expect_rejection(lambda:root_bounds(QPhi(-1)))
        expect_rejection(lambda:verify_root(QPhi(2),F(3,2),F(8,5)))
        expect_rejection(lambda:check_patch(example_corners()[:-1]))
        expect_rejection(lambda:check_patch(example_corners(150)))
    return rational_strings({
        'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_analytic_theorem_with_exact_finite_hypotheses',
        'global_non_rupert_proved':False,
        'arbitrary_source_orientation_roll_translation_scale_ge_one':True,
        'closed_receiver_cap_chord_radius':'1/200',
        'all_source_receiver_caps':10,'radius_improvement_over_previous_cap':35,
        'adaptive_receiver_region_and_whole_triangle_criterion_proved':True,
        'persistent_probe_enumeration':enumeration,
        'all_selected_endpoint_corner_support_checks':36*3*60,
        'persistent_probes':[{'vertex':encode(v),'edge':encode(e)} for v,e in probes],
        'center_torque_hull':torque,
        'complete_center_facet_normals':[encode(n) for n in sorted(facets)],
        'concavity_roll_branch':roll,'cap_constants':cap,'example_receiver_triangle':patch,
        'radical_enclosure_grid_denominator':DEN,
        'new_malformed_controls_rejected':10 if self_test else 0,
        'inherited_malformed_controls_replayed':12 if self_test else 0,
        'inherited_linear_roll_expected_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'inherited_linear_roll_graph':'bafkreih2r7gsrai6kr32c2vapf5v5debgmkr2ri3n2uysvdtmfgxp3mbtm',
        'inherited_cell_graph':'bafkreiakgi4vli7xoy5vmho5xsga7iistawcm7yhebl2flwkzu62hvewmq'})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),indent=2,sort_keys=True))
