#!/usr/bin/env python3
"""Exact finite hypotheses for BETA_CAP_PROOF.md; Python3.11+ stdlib.

Two full closed-arc certificates, original circle alignments, tangent disks,
the new lower-C original contacts and all rational transport/angle bounds.
No private input, float, solver or full old parent self-test is used.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F

from verify import PHI,QPhi,ZERO,act,dot,require,symmetry_group,vertices
from cell_certificate import encode,decode
from torque_certificate import cross,subtract
from linear_roll_certificate import exact_hull,project
from global_cap_certificate import canonical,expect_rejection
from threshold_receiver_certificate import (REFS,I,BETA,Interval,source_coordinates,
    facet_coefficients,hull_data,active_balance,exact_rotations,validate_proper,threefold_source)
from contact_collar_certificate import LOW,complete_contacts,torque_hull
from adaptive_receiver_certificate import verify_root,rational_strings
import actual_torque_hull_certificate as parent
import winning_receiver_certificate as winning

GLOBAL_SHA='69efa7e7cc4fbc359ce5481fc7eaa82c9779a51d56464597232e520663667fa8'
THRESHOLD_SHA='5516794048036b35ce73b63b0fdf5eb1c01620b260b11f87dfc401e0e5ccfeac'
COLLAR_SHA='716750e5ee2e9e3ed450cfd6182bb21554551725a38dec2cc4feca02c2a071e1'
WINNING_SHA='f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3'
GRID=64
CUT=F(1,64)
GAMMA=F(1,100)
CAP=F(1,640)
BAND=F(1,600)


def arcs(grid=GRID,cut=CUT):
    require(grid==64 and cut==F(1,64),'fixed complete closed-arc policy')
    out=[]
    for q in range(4):
        start,end=(cut,F(1)) if q%2==0 else (F(0),(1-cut)/(1+cut))
        out.extend((q,j,start+(end-start)*F(j,grid),
                    start+(end-start)*F(j+1,grid)) for j in range(grid))
    return out


def validate_arcs(domain):
    require(domain==arcs() and len(domain)==256,'all four remote closed quarters, seams and intervals')
    for q in range(4):
        part=[z for z in domain if z[0]==q]
        require(len(part)==GRID and all(a[3]==b[2] for a,b in zip(part,part[1:])),
                'entire closed parameter interval, with no omitted boundary')


def weights(l,h):
    require(0<=l<h<=1,'positive nondegenerate parameter subinterval')
    return [(1-l*l,2*l,1+l*l),(1-l*h,l+h,1+l*h),(1-h*h,2*h,1+h*h)]


def verify_bernstein_identity(l,h):
    # Formal coefficient triples in the basis (A,D,H+gamma).
    W=[(a,b,-c) for a,b,c in weights(l,h)]
    for s in (F(0),F(1,2),F(1)):
        t=l+(h-l)*s
        values=(1-t*t,2*t,-1-t*t)
        require(tuple(W[0][i]*(1-s)**2+2*W[1][i]*s*(1-s)+W[2][i]*s*s
                      for i in range(3))==values,'formal quadratic Bernstein identity')
    # Both sides have degree <=2 in s; three distinct exact values prove identity.


def lower_coefficients(c,l,h,gamma=GAMMA):
    A,D,support=c
    require(gamma>0,'positive physical support threshold')
    return [A.lo*a+D.lo*b-(support.hi+gamma)*v for a,b,v in weights(l,h)]


def quarter_coefficients(coefficients,q):
    require(0<=q<4,'actual closed circle quarter')
    out=[]
    for A,D,h in coefficients:
        for _ in range(q):
            A,D=D,A.scale(-1)
        out.append((A,D,h))
    return out


def validate_coefficients(coefficients):
    require(len(coefficients)==128 and all(h.lo>0 for A,D,h in coefficients),
            'all sixteen actual unit facets times eight actual circle points')


def compact_runs(records):
    out=[]
    for q,j,k,margin in records:
        if out and out[-1][0]==q and out[-1][2]+1==j and out[-1][3]==k:
            out[-1][2]=j
        else:
            out.append([q,j,j,k])
    return out


def verify_runs(runs,coefficients,domain):
    validate_arcs(domain);validate_coefficients(coefficients)
    expanded=[]
    for q,a,b,k in runs:
        require(0<=q<4 and 0<=a<=b<GRID and 0<=k<len(coefficients),'valid compact actual witness run')
        expanded.extend((q,j,k) for j in range(a,b+1))
    require([(q,j) for q,j,k in expanded]==[(q,j) for q,j,l,h in domain],
            'complete ordered closed-arc witness coverage')
    cc=[quarter_coefficients(coefficients,q) for q in range(4)]
    for (q,j,k),(qq,jj,l,h) in zip(expanded,domain):
        require(min(lower_coefficients(cc[q][k],l,h))>0,'actual selected witness on entire closed arc')


def remote_cover(H,n,circle):
    require(len(circle)==8,'complete actual circle set')
    coordinates=source_coordinates(sorted(circle),n)
    coefficients=facet_coefficients(H,n,coordinates)
    validate_coefficients(coefficients)
    domain=arcs();validate_arcs(domain);records=[];checks=0
    cc=[quarter_coefficients(coefficients,q) for q in range(4)]
    for q,j,l,h in domain:
        verify_bernstein_identity(l,h)
        best=None
        for k,c in enumerate(cc[q]):
            low=min(lower_coefficients(c,l,h));checks+=1
            if best is None or low>best[0]:
                best=(low,k)
        require(best[0]>0,'remote roll lacks an exact entire-arc support witness')
        records.append([q,j,best[1],str(best[0])])
    runs=compact_runs(records);verify_runs(runs,coefficients,domain)
    raw=json.dumps(records,separators=(',',':')).encode()
    return {'closed_circle_quarters':4,'closed_remote_arcs':256,'subdivisions_each_quarter':64,
        'rational_parameter_cut':str(CUT),'physical_unit_support_separation_lower':str(GAMMA),
        'near_zero_or_halfturn_roll_angle_upper':'1/32',
        'all_actual_facet_circle_arc_candidates':checks,
        'formal_quadratic_identity_values_checked':256*3*3,
        'minimum_selected_Bernstein_coefficient_lower':min(F(z[3]) for z in records).__str__(),
        'complete_generated_witness_record_sha256':hashlib.sha256(raw).hexdigest(),
        'compact_witness_run_count':len(runs),'all_compact_witness_runs':runs,
        'all_selected_witness_runs_reverified':True},coefficients,records


def validate_active(n,V,active):
    h=min(dot(v,n) for v in V if dot(v,n)>0)
    require(len(active)==4 and set(active)=={v for v in V if dot(v,n)==h},
            'complete actual four-positive-original active set')


def tangent_disk(n,V):
    h=min(dot(v,n) for v in V if dot(v,n)>0)
    active=sorted(v for v in V if dot(v,n)==h);validate_active(n,V,active)
    require(h*h/dot(n,n)==BETA,'actual beta optimizer height')
    P={project(v,n) for v in active};H=exact_hull(P,n)
    require(len(H)==4,'full actual tangent quadrilateral')
    planes=[]
    for p,q in zip(H,H[1:]+H[:1]):
        m=cross(subtract(q,p),n);height=dot(m,p)
        require(height>0 and all(dot(m,v)<=height for v in P),'entire positive original tangent support')
        planes.append({'normal':encode(m),'height':height.encode(),
            'squared_origin_plane_distance':(height*height/dot(m,m)).encode()})
    radius=min(QPhi(F(p['squared_origin_plane_distance'][0]),
                    F(p['squared_origin_plane_distance'][1])) for p in planes)
    require(radius==(39+37*PHI)/29 and radius>QPhi(F(9,5)**2),
            'complete sharp tangent disk and strict rational lower')
    return {'all4original_positive_active_vertices':[encode(v) for v in active],
        'full_tangent_quadrilateral':[encode(p) for p in H],
        'all4tangent_facets':planes,'sharp_centered_disk_squared_radius':radius.encode(),
        'tangent_disk_radius_strict_lower':'9/5'}


def scalar_bounds(delta=CAP,band=BAND):
    require(delta>0 and band>0,'positive cap and nonwinning band')
    a=F(15,4)*delta
    theta=F(1,32)+F(101,100)*(a+delta)
    eta_source=F(23,50)*a+F(9,4)*a*a
    eta_target=F(9,2)*delta+F(9,4)*delta*delta
    minimum=F(57,125)-F(9,2)*delta
    a_win=F(101,300)*(F(289,500)-minimum)
    eta_win=F(289,500)*a_win+F(9,4)*a_win*a_win
    win_gap=F(51,1280)-eta_win-eta_target
    checks={
        'reference_height_exceeds57over125':BETA>QPhi(F(57,125)**2),
        'receiving_minimum_lower_is_positive':minimum>0,
        'receiving_minimum_squared_lower_exceeds_remaining_regions':minimum*minimum>F(1,7),
        'threshold_original_circle_axial_height_upper':BETA<QPhi(F(23,50)**2),
        'sqrt2_upper3over2':2<F(3,2)**2,
        'threshold_disk_lower9over5':(39+37*PHI)/29>QPhi(F(9,5)**2),
        'threshold_source_chord_multiplier':F(3,2)*F(9,2)/F(9,5)==F(15,4),
        'receiver_cap_inside_old_persistent_local_cap':delta<F(1,300),
        'all_small_normal_chords_below_one_tenth':0<delta<a<F(1,10),
        'full_near_branch_angle_below_lower_contact_bound':theta<F(1,16),
        'remote_circle_transport_margin':GAMMA-eta_source-eta_target>F(1,10000),
        'winning_c0_upper':QPhi(F(1,3))<QPhi(F(289,500)**2),
        'winning_tangent_disk_exceeds3':QPhi(F(8,3))+4*PHI>QPhi(9),
        'winning_sine_upper_below_one_twentieth':(F(289,500)-minimum)/3<F(1,20),
        'winning_acute_cosine_bound':F(399,400)>F(199,200)**2,
        'winning_chord_sine_multiplier':F(101,100)**2*F(399,400)>1,
        'winning_source_chord_below_one_tenth':a_win<F(1,10),
        'whole_reference_threefold_roll_circle_gap':F(3,40)-F(9,256)==F(51,1280),
        'winning_source_and_receiver_transport_margin':win_gap>F(1,300),
        'small_chord_to_full_angle_multiplier':F(101,100)**2*(1-F(1,400))>1,
        'nonwinning_band_F_exceeds9over20':BETA-QPhi(band)>QPhi(F(9,20)**2),
        'nonwinning_band_exceeds_remaining_regions':BETA-QPhi(band)>QPhi(F(1,7)),
        'nonwinning_band_receiver_coercivity_chord_inside_cap':F(5,6)*F(10,9)*band<delta}
    require(all(checks.values()),'unsupported cap, source/receiver transport, full angle or band bound')
    return rational_strings({'receiver_closed_unit_normal_chord_cap':delta,
        'receiving_and_source_axial_strict_lower':minimum,'threshold_source_normal_chord_upper':a,
        'full_near_branch_angle_upper':theta,
        'threshold_original_circle_source_transport_upper':eta_source,
        'whole_original_receiving_body_transport_upper':eta_target,
        'remote_actual_physical_support_gap_lower':GAMMA-eta_source-eta_target,
        'winning_source_normal_chord_upper':a_win,
        'winning_original_corner_transport_upper':eta_win,
        'reference_threefold_whole_roll_support_gap_lower':F(51,1280),
        'winning_actual_physical_support_gap_lower':win_gap,
        'nonwinning_receiver_axial_squared_slack':band,
        'nonwinning_band_receiver_normal_chord_upper':F(25,27)*band,
        'checks':checks})


def check(self_test=False):
    V=vertices();G=symmetry_group(V,return_matrices=True)
    threshold=parent.fixture('threshold_receiver_expected.json',THRESHOLD_SHA)
    collar=parent.fixture('contact_collar_expected.json',COLLAR_SHA)
    global_data=parent.fixture('global_cap_expected.json',GLOBAL_SHA)
    win=parent.fixture('winning_receiver_expected.json',WINNING_SHA)
    record,_,_=winning.active_hexagon()
    require(record==win['complete_positive_active_tangent_hexagon'],'entire winning active hexagon matches pinned parent')
    B,H0,source_info=threefold_source(V,win)
    require(source_info==threshold['threefold_original_source_corner_bounds'],
            'entire actual reference corner/preimage/height/support record matches threshold parent')
    old_covers=threshold['both_threshold_whole_circle_interval_covers']
    require(len(old_covers)==2 and all(c['quarter_count']==4 and c['parameter_grid']==128 and
            c['all_witness_gaps_strictly_above']=='3/40' and c['source_support_Lipschitz_loss_upper']=='9/256'
            and c['original_source_corner_count']==12 for c in old_covers),
            'published full reference roll covers give the pre-transport51/1280gap')
    scores=global_data['diameter_and_sign_regions']['score_counts']
    values=[QPhi(F(z['score'][0]),F(z['score'][1])) for z in scores]
    require(max(z for z in values if z not in {BETA,QPhi(F(1,3))})==QPhi(F(1,7)),
            'complete remaining signed-region maximum')
    require(sum(z['regions'] for z in scores)==436 and
            sum(z['regions'] for z,v in zip(scores,values) if v==QPhi(F(1,3)))==10 and
            sum(z['regions'] for z,v in zip(scores,values) if v==BETA)==60,
            'complete winning, threshold and remaining region counts')
    rays={canonical(act(g,n)) for n in REFS for g in G}
    pinned={canonical(decode(z['direction'])) for z in threshold['threshold_axis_classification']['all_sixty_axes_and_regions']}
    require(len(rays)==60 and rays==pinned,'every nonwinning beta projective axis from published complete classification')
    for n in REFS:
        directed={act(g,n) for g in G}
        require(len(directed)==60 and all(tuple(-q for q in r) in directed for r in directed),
                'all directed caps and normal reversals')
    axes={'body_projective_orbits':[{'representative_balance':active_balance(n,V)} for n in REFS]}
    R,C,rotation=exact_rotations(G,axes);hulls=[hull_data(n,V) for n in REFS]
    alignments=[]
    for si in range(2):
        for ti in range(2):
            D=I if si==ti else R
            source={v for v in V if project(v,REFS[si]) in hulls[si][5]}
            target={v for v in V if project(v,REFS[ti]) in hulls[ti][5]}
            require({act(D,p) for p in hulls[si][5]}==hulls[ti][5] and
                    {act(D,v) for v in source}==target,'all actual spatial and projected original circle preimages align')
            alignments.append({'source_orbit':si,'receiver_orbit':ti,
                'all8projected_and_spatial_original_circle_preimages_align':True})
    require(cross(LOW,REFS[0])==(ZERO,ZERO,ZERO) and dot(LOW,REFS[0])>0,'same directed lower receiving reference')
    low_contact,probes,T,gap=complete_contacts(LOW,V,C)
    old_low=collar['explicit_local_contact_caps'][0]
    strip=lambda records:[{k:v for k,v in r.items() if k!='original_source'} for r in records]
    require(strip(low_contact['actual_contact_records'])==
            strip(old_low['actual_shared_contact_certificate']['actual_contact_records']),
            'entire actual lower receiving contact list unchanged at C')
    low_torque=torque_hull(T,F(7,20))
    require(low_torque==old_low['complete_center_torque_hull'],'entire complete lower torque certificate unchanged')
    disks=[tangent_disk(n,V) for n in REFS]
    covers=[];saved=[]
    for n,h in zip(REFS,hulls):
        cover,coefficients,records=remote_cover(h[1],n,h[5]);covers.append(cover)
        saved.append((coefficients,records))
    bounds=scalar_bounds();rejected=0
    if self_test:
        coeff,records=saved[0];runs=compact_runs(records);domain=arcs()
        q,j,l,h=domain[0];k=records[0][2]
        corrupt=[r[:] for r in runs];corrupt[0][3]=128
        improper=tuple(decode(r) for r in rotation['improper_active_alignment_matrix'])
        n=REFS[0];height=min(dot(v,n) for v in V if dot(v,n)>0)
        active=sorted(v for v in V if dot(v,n)==height)
        def excessive_gap():
            require(min(lower_coefficients(coeff[k],l,h,F(1,4)))>0,'unsupported physical gap')
        controls=[
            lambda:validate_arcs(domain[:-1]),
            lambda:validate_arcs(domain[:192]),
            lambda:validate_arcs([domain[0]]+domain),
            lambda:validate_arcs(list(reversed(domain))),
            lambda:arcs(cut=F(0)),
            lambda:verify_runs(runs[:-1],coeff,domain),
            lambda:verify_runs(corrupt,coeff,domain),
            excessive_gap,
            lambda:validate_coefficients(coeff[:-1]),
            lambda:validate_active(n,V,active[:-1]),
            lambda:scalar_bounds(delta=F(1,625)),
            lambda:scalar_bounds(band=F(1,500)),
            lambda:validate_proper(improper),
            lambda:verify_root(QPhi(5),F(3),F(4)),
            lambda:Interval(1,0),
            lambda:Interval(1,2).divide_positive(Interval(0,1))]
        for control in controls:
            expect_rejection(control);rejected+=1
    return {'agent':'six-rupert-3','role':'researcher',
        'proof_status':'complete_unformalized_explicit_all_source_beta_caps_and_nonwinning_receiving_band',
        'global_RID':'OPEN','global_non_rupert_proved':False,
        'all_source_original_rotation_roll_translation_scale_ge_one_covered_in_new_caps':True,
        'numeric_global_all_receiver_epsilon_certified':False,
        'closed_caps_at_all60projective_or120directed_beta_axes':'1/640',
        'strict_passage_necessary_nonwinning_receiver_condition':'f(n)^2<beta-1/600',
        'strict_nonwinning_receiver_squared_diameter_lower':'(736+960phi)/29+1/150',
        'winning_receiver_below_beta_numerical_slack':'NOT_CERTIFIED',
        'all60beta_axes_exactly_match_published_classification':True,
        'complete_global_signed_regions':436,'winning_projective_regions':10,
        'nonwinning_projective_regions':426,'threshold_projective_regions':60,
        'remaining366regions_maximum':['1/7','0'],
        'all4ordered_original_circle_alignments':alignments,
        'lower_C_original_contact_certificate':low_contact,
        'lower_C_complete_torque_hull':low_torque,
        'both_exact_threshold_tangent_quadrilaterals':disks,
        'full_closed_remote_roll_certificates':covers,'all_new_rational_bounds':bounds,
        'complete_winning_positive_active_hexagon_every_entry_regenerated':True,
        'complete_reference_threefold_original_corner_record_regenerated':True,
        'published_four_closed_quarter_reference_covers_used_before_old_transport_loss':True,
        'new_malformed_controls_rejected':rejected,
        'pinned_parent_output_sha256':{'global':GLOBAL_SHA,'threshold':THRESHOLD_SHA,
                                      'contact_collar':COLLAR_SHA,'winning':WINNING_SHA},
        'full_old_parent_self_tests_replayed':False,
        'float_solver_private_or_sampled_continuum_inputs':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--self-test',action='store_true')
    args=p.parse_args();print(json.dumps(check(args.self_test),sort_keys=True,indent=2))
