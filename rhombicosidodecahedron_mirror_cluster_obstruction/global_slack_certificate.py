#!/usr/bin/env python3
"""Exact finite hypotheses for GLOBAL_SLACK_PROOF.md, Python3.11+stdlib.

Complete signed ordering-wall/cone coverage, original circle preimages and
pair distances, actual active/nonactive heights, uniform q phase/cut gates,
and rational near-circle injection bounds. No sampled continuum premise.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from functools import cmp_to_key
from itertools import combinations

from verify import QPhi,PHI,ZERO,dot,require,vertices,symmetry_group
from cell_certificate import encode,decode,geometry
from torque_certificate import cross,subtract
from linear_roll_certificate import project
from global_cap_certificate import expect_rejection
from adaptive_receiver_certificate import rational_strings
import beta_cap_certificate as beta
import winning_receiver_certificate as winning
import actual_torque_hull_certificate as hull

BETACAP_SHA='452b30d5c368a8de97c47d1b92bfe5f176452fd5fea57b8f254f183cd358c065'
EPSILON=F(1,1200)


def signed_ray(w):
    require(any(q!=ZERO for q in w),'nonzero oriented ray')
    scale=next(q for q in w if q!=ZERO)
    if scale<ZERO:
        scale=-scale
    return tuple(q/scale for q in w)


def coordinates(w,B):
    X=(QPhi(1),ZERO,ZERO)
    require(dot(X,B)==ZERO,'fixed transverse exact angular coordinate')
    return dot(w,X),dot(w,cross(B,X))


def upper_half(w,B):
    x,y=coordinates(w,B)
    require(x!=ZERO or y!=ZERO,'nonzero tangent angular coordinates')
    return 0 if y>ZERO or (y==ZERO and x>ZERO) else 1


def orientation(u,v,B):
    x,y=coordinates(u,B);a,b=coordinates(v,B)
    return x*b-y*a


def angular_sort(rays,B):
    def compare(u,v):
        hu,hv=upper_half(u,B),upper_half(v,B)
        if hu!=hv:
            return -1 if hu<hv else 1
        det=orientation(u,v,B)
        if det!=ZERO:
            return -1 if det>ZERO else 1
        require(u==v,'unremoved collinear oriented rays')
        return 0
    return sorted(rays,key=cmp_to_key(compare))


def full_wall_rays(P,B):
    require(len(P)==6 and len(set(P))==6 and all(dot(p,B)==ZERO for p in P),
            'complete actual six-point tangent plane')
    candidates=[]
    for i,j in combinations(range(6),2):
        w=cross(subtract(P[i],P[j]),B)
        require(dot(w,w)>ZERO,'nonzero actual pair-ordering wall')
        candidates += [signed_ray(w),signed_ray(tuple(-q for q in w))]
    require(len(candidates)==30,'all fifteen pair-equality lines and both directed rays')
    return angular_sort(set(candidates),B),candidates


def validate_walls(rays,P,B):
    expected,candidates=full_wall_rays(P,B)
    require(rays==expected and len(set(rays))==len(rays),'entire canonical cyclic ordering-wall set')
    require(all(signed_ray(tuple(-q for q in r)) in set(rays) for r in rays),
            'every antipodal ordering wall included')
    for u,v in zip(rays,rays[1:]+rays[:1]):
        require(orientation(u,v,B)>ZERO,'every adjacent closed cone has angle strictly below pi')
    return candidates


def validate_cell(P,B,u,v,order,lower=QPhi(1)):
    require(len(order)==6 and set(order)==set(range(6)),'complete original rank permutation')
    require(orientation(u,v,B)>ZERO,'positive closed tangent cone')
    gap_vector=subtract(P[order[2]],P[order[0]])
    for ray in (u,v):
        heights=[dot(P[i],ray) for i in order]
        require(all(a<=b for a,b in zip(heights,heights[1:])),
                'same original order holds on both closed cone boundary rays')
        gap=dot(gap_vector,ray)
        require(gap>ZERO and gap*gap>lower*lower*dot(ray,ray),
                'strict rank-three gap on each cone endpoint')
    # Linear inequalities extend to the entire positive cone.
    # g.u>c||u|| and g.v>c||v|| imply g.(au+bv)>c||au+bv||,
    # by the triangle inequality, for a,b>=0 not both zero.


def order_cones(P,B):
    rays,candidates=full_wall_rays(P,B);validate_walls(rays,P,B)
    cells=[];wall_records=[]
    for ray in rays:
        heights=sorted(dot(p,ray) for p in P)
        gap=heights[2]-heights[0]
        require(gap>ZERO,'no three original supporting points on one line')
        wall_records.append({'oriented_ray':encode(ray),
            'squared_third_minus_first_gap':(gap*gap/dot(ray,ray)).encode()})
    for i,(u,v) in enumerate(zip(rays,rays[1:]+rays[:1])):
        interior=tuple(a+b for a,b in zip(u,v))
        heights=[dot(p,interior) for p in P]
        require(len(set(heights))==6,'no omitted ordering wall inside an adjacent cone')
        order=sorted(range(6),key=lambda j:heights[j])
        validate_cell(P,B,u,v,order)
        cells.append({'from_ray':i,'to_ray':(i+1)%len(rays),'all_six_original_ranks':order,
                      'both_closed_boundary_rank_orders_and_gap_verified':True})
    sharp=min(QPhi(F(r['squared_third_minus_first_gap'][0]),
                   F(r['squared_third_minus_first_gap'][1])) for r in wall_records)
    require(sharp==(60-12*PHI)/19 and sharp>QPhi(1),'sharp full angular third-height gap')
    return {'all15original_pair_ordering_lines':15,'all30signed_wall_candidates':30,
        'distinct_oriented_wall_rays':len(rays),'all_signed_wall_candidates':[encode(r) for r in candidates],
        'complete_ordered_wall_records':wall_records,'all_closed_angular_cones':cells,
        'all_cones_strictly_below_halfturn':True,'sharp_squared_third_minus_first_gap':sharp.encode(),
        'uniform_third_minus_first_gap_strictly_above_tangent_norm':True},rays


def validate_circle(n,V,circle):
    R2=7+8*PHI
    expected={project(v,n) for v in V if dot(v,n)**2/dot(n,n)==beta.BETA}
    require(len(circle)==8 and set(circle)==expected,'all eight distinct actual original circle points')
    require(all(dot(p,p)==R2-beta.BETA for p in circle),'common actual beta circumradius')


def circle_geometry(n,V):
    circle=sorted(beta.hull_data(n,V)[5]);validate_circle(n,V,circle)
    records=[];originals=[]
    for p in circle:
        matches=[v for v in V if project(v,n)==p]
        require(len(matches)==1,'unique actual original circle preimage')
        v=matches[0]
        require(dot(v,n)**2/dot(n,n)==beta.BETA,'actual circle preimage axial height')
        originals.append({'projection':encode(p),'original_preimage':encode(v)})
    for i,j in combinations(range(8),2):
        dist=dot(subtract(circle[i],circle[j]),subtract(circle[i],circle[j]))
        require(dist>QPhi(1),'all actual circle points separated by more than one')
        records.append({'pair':[i,j],'squared_distance':dist.encode()})
    sharp=min(QPhi(F(r['squared_distance'][0]),F(r['squared_distance'][1])) for r in records)
    require(sharp==(40+32*PHI)/29,'complete actual minimum source-circle pair distance')
    return {'all8actual_original_circle_preimages':originals,'all28actual_circle_pair_distances':records,
        'minimum_squared_pair_distance':sharp.encode(),'all_source_pair_distances_strictly_above_one':True},circle


def scalar_bounds(epsilon=EPSILON,pair_lower=F(1)):
    require(epsilon>0 and pair_lower>0,'positive slack and distinct source-pair bound')
    a=F(25,27)*epsilon
    eta=F(23,50)*a+F(9,4)*a*a
    loss=epsilon+9*eta
    c0_lower=F(577,1000);z_lower=F(199,200);height_upper=F(23,50)
    radial=(c0_lower*z_lower-height_upper)/F(9,2)
    checks={
        'epsilon_below_published_nonwinning_band':epsilon<F(1,600),
        'all_receiving_and_source_height_exceed_q':beta.BETA-QPhi(epsilon)>QPhi(F(57,125)**2),
        'remaining366region_barrier':beta.BETA-QPhi(epsilon)>QPhi(F(1,7)),
        'all_height_lower_above9over20':beta.BETA-QPhi(epsilon)>QPhi(F(9,20)**2),
        'c0_lower577over1000':c0_lower*c0_lower<F(1,3),
        'beta_height_upper23over50':beta.BETA<QPhi(height_upper*height_upper),
        'sqrt2_upper3over2':2<F(3,2)**2,
        'full_threshold_disk_radius_above9over5':(39+37*PHI)/29>QPhi(F(9,5)**2),
        'source_coercivity_multiplier25over27':F(3,2)/F(9,5)*F(10,9)==F(25,27),
        'body_radius_below9over2':7+8*PHI<QPhi(F(9,2)**2),
        'winning_tangent_displacement_above1over40':radial>F(1,40),
        'actual_threshold_source_transport_below_one2000':eta<F(1,2000),
        'reference_beta_circle_radius_exceeds_four':7+8*PHI-beta.BETA>QPhi(16),
        'candidate_original_receiver_height_below_one_half':beta.BETA+QPhi(9*eta)<QPhi(F(1,2)**2),
        'candidate_height_excess_below_third_height_gap':F(10,9)*loss<F(1,40),
        'source_to_chosen_receiving_original_distance_below_one10':loss<F(1,100),
        'perturbed_actual_source_pair_distance_above_one5':pair_lower-2*eta>F(1,5),
        'all_small_source_normal_chords_below_one10':a<F(1,10),
        'nonactive_original_receiver_height_above17over16':
            F(5,4)**2<F(5,3) and F(5,4)-F(9,2)*F(1,24)==F(17,16)}
    require(all(checks.values()),'unsupported full numerical global slack/injection bounds')
    return rational_strings({'numeric_global_axial_squared_slack':epsilon,
        'threshold_source_normal_chord_upper':a,'threshold_source_circle_original_transport_upper':eta,
        'source_to_chosen_receiving_original_squared_distance_upper':loss,
        'candidate_original_receiver_height_excess_upper':F(10,9)*loss,
        'winning_tangent_norm_strict_lower':radial,'candidate_receiving_original_count_upper':4,
        'source_original_circle_points_count':8,'source_to_chosen_receiving_vertex_distance_strict_upper':'1/10',
        'perturbed_source_pair_distance_strict_lower':'1/5','checks':checks})


def check(self_test=False):
    V=vertices();R2=7+8*PHI
    win=hull.fixture('winning_receiver_expected.json',beta.WINNING_SHA)
    global_data=hull.fixture('global_cap_expected.json',beta.GLOBAL_SHA)
    cap=hull.fixture('beta_cap_expected.json',BETACAP_SHA)
    require(cap['closed_caps_at_all60projective_or120directed_beta_axes']=='1/640' and
            cap['strict_passage_necessary_nonwinning_receiver_condition']=='f(n)^2<beta-1/600' and
            cap['global_RID']=='OPEN','complete published nonwinning receiver band input')
    scores=global_data['diameter_and_sign_regions']['score_counts']
    values=[QPhi(F(z['score'][0]),F(z['score'][1])) for z in scores]
    require(sum(z['regions'] for z in scores)==436 and
            max(v for v in values if v not in {beta.BETA,QPhi(F(1,3))})==QPhi(F(1,7)),
            'complete source regional barrier and classification')
    hexagon,P,facets=winning.active_hexagon()
    require(hexagon==win['complete_positive_active_tangent_hexagon'],'every winning active hexagon entry regenerated')
    B=geometry()[0][0][1];N=dot(B,B)
    active=[decode(v) for v in hexagon['positive_original_active_vertices']]
    others=sorted(v for v in V if v not in active and tuple(-q for q in v) not in active)
    require(len(others)==48 and min(dot(v,B)**2/N for v in others)==QPhi(F(5,3)),
            'every actual nonactive receiving original and sharp height gap')
    cone_record,rays=order_cones(P,B)
    circles=[];circle_points=[]
    for n in beta.REFS:
        record,points=circle_geometry(n,V);circles.append(record);circle_points.append(points)
    disks=[beta.tangent_disk(n,V) for n in beta.REFS]
    require(disks==cap['both_exact_threshold_tangent_quadrilaterals'],
            'every actual threshold tangent quadrilateral entry regenerated')
    phase=rational_strings(winning.phase_bounds())
    U,cut=winning.cut_triangle()
    outer=rational_strings(winning.outer_geometry(U))
    G=symmetry_group(V,return_matrices=True)
    chamber=rational_strings(winning.chamber_geometry(G))
    require(phase==win['phase_bounds'] and rational_strings(cut)==win['outer_receiver_cut_triangle'] and
            outer==win['outer_triangle_geometry'] and chamber==win['whole_receiver_chamber_reduction'],
            'complete uniform q phase/cut/chamber records regenerated')
    torque=win['complete_actual_torque_facet_certificate']
    require(torque['triple_strata_certified']==840 and
            torque['classifications']=={'opposite':726,'distance':114,'degenerate':0},
            'published whole U torque theorem, not rerun')
    adaptive=hull.fixture('adaptive_receiver_expected.json',hull.ADAPTIVE_SHA)
    probes,pool,center_facets=hull.selected_probes(adaptive)
    supports=0
    for u in U:
        for v,e in probes:
            m=cross(e,u)
            for w in V:
                require(dot(m,subtract(v,w))>=ZERO,'every actual receiving support on all closed U corners')
                supports+=1
    require(supports==1800,'complete actual receiving cut-triangle support cover')
    bounds=scalar_bounds();rejected=0
    if self_test:
        first=cone_record['all_closed_angular_cones'][0]
        u,v=rays[0],rays[1];order=first['all_six_original_ranks']
        bad=order[:];bad[0],bad[-1]=bad[-1],bad[0]
        worst=min(range(len(rays)),key=lambda j:QPhi(
            F(cone_record['complete_ordered_wall_records'][j]['squared_third_minus_first_gap'][0]),
            F(cone_record['complete_ordered_wall_records'][j]['squared_third_minus_first_gap'][1])))
        worst_order=cone_record['all_closed_angular_cones'][worst]['all_six_original_ranks']
        controls=[
            lambda:validate_walls(rays[:-1],P,B),
            lambda:validate_walls(list(reversed(rays)),P,B),
            lambda:validate_walls(rays+rays[:1],P,B),
            lambda:validate_walls(rays[1:]+rays[:1],P,B),
            lambda:validate_cell(P,B,u,u,order),
            lambda:validate_cell(P,B,u,v,order[:-1]),
            lambda:validate_cell(P,B,u,v,bad),
            lambda:validate_cell(P,B,rays[worst],rays[(worst+1)%len(rays)],worst_order,QPhi(2)),
            lambda:full_wall_rays(P[:-1],B),
            lambda:full_wall_rays(P,(QPhi(1),ZERO,ZERO)),
            lambda:validate_circle(beta.REFS[0],V,circle_points[0][:-1]),
            lambda:validate_circle(beta.REFS[0],V,[(ZERO,ZERO,ZERO)]+circle_points[0][1:]),
            lambda:scalar_bounds(epsilon=F(1,1000)),
            lambda:scalar_bounds(pair_lower=F(0)),
            lambda:scalar_bounds(epsilon=F(0))]
        for control in controls:
            expect_rejection(control);rejected+=1
    return {'agent':'six-rupert-3','role':'researcher',
        'proof_status':'complete_unformalized_numeric_global_RID_receiver_slack',
        'global_RID':'OPEN','global_non_rupert_proved':False,
        'numeric_global_all_receivers_axial_squared_slack':'1/1200',
        'all_original_proper_source_rotation_full_roll_translation_scale_ge_one_covered':True,
        'strict_passage_necessary_receiver_condition':'f(n)^2<beta-1/1200',
        'strict_receiver_squared_diameter_lower':'(736+960phi)/29+1/300',
        'complete_winning_angular_order_and_third_height_gap':cone_record,
        'both_original_threshold_circle_preimages_and_pair_distances':circles,
        'all48nonactive_original_center_heights_regenerated':True,
        'sharp_nonactive_original_center_squared_height':['5/3','0'],
        'entire_winning_and_threshold_tangent_certificates_regenerated':True,
        'uniform_winning_to_winning_f_gt_q_phase_and_chart_inputs_regenerated':True,
        'new_original_cut_triangle_support_comparisons':supports,
        'winning_whole840strata_torque_theorem_inherited_not_rerun':True,
        'all_new_rational_bounds':bounds,'new_malformed_controls_rejected':rejected,
        'pinned_parent_output_sha256':{'winning':beta.WINNING_SHA,'global':beta.GLOBAL_SHA,'beta_caps':BETACAP_SHA},
        'full_old_parent_self_tests_replayed':False,
        'float_solver_private_sampled_continuum_or_compactness_input':False,
        'new_independent_review_or_formalization_asserted':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true')
    args=p.parse_args();print(json.dumps(check(args.self_test),sort_keys=True,indent=2))
