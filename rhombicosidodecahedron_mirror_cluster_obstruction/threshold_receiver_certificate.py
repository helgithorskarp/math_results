#!/usr/bin/env python3
"""Exact finite hypotheses for THRESHOLD_RECEIVER_PROOF.md.

Python3.11+ stdlib. Exact Q(phi)/Fraction interval arithmetic, fixed1e12
root grid and complete128parameter grid on each of four circle quarters.
No private diagnostic files, sampled continuum premise or solver input.
"""
import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

from verify import PHI,QPhi,ZERO,act,dot,matmul,require,symmetry_group,vertices
from torque_certificate import cross,determinant,subtract
from cell_certificate import decode,encode,geometry
from global_cap_certificate import canonical,circle_map,expect_rejection,order,representatives
from linear_roll_certificate import exact_hull,project
from adaptive_receiver_certificate import root_bounds,verify_root,rational_strings
import actual_torque_hull_certificate as parent
import winning_receiver_certificate as winning

WINNING_SHA='f2796de9c7123917dbd845c651179216ca595545c30e6a7cdb48ea7bf6312ba3'
GLOBAL_SHA='69efa7e7cc4fbc359ce5481fc7eaa82c9779a51d56464597232e520663667fa8'
BETA=(19-8*PHI)/29



def active_balance(n,V):
    N=dot(n,n);c=min(q for v in V if (q:=dot(v,n))>0)
    beta=(19-8*PHI)/29
    require(c*c/N==beta,'wrong selected beta normal')
    active=sorted([v for v in V if dot(v,n)==c],key=order)
    y=tuple(q*c/N for q in n)
    balances=[]
    for a,b,cvertex in combinations(active,3):
        den=determinant(a,b,cvertex)
        if den==ZERO:
            continue
        weights=(determinant(y,b,cvertex)/den,
                 determinant(a,y,cvertex)/den,
                 determinant(a,b,y)/den)
        if min(weights)>0:
            require(sum(weights,ZERO)==QPhi(1),'balance weight sum')
            require(tuple(sum((w*v[j] for w,v in zip(weights,(a,b,cvertex))),ZERO)
                          for j in range(3))==y,'full positive original balance')
            balances.append((a,b,cvertex,weights))
    require(balances,'actual positive three-original-vertex balance missing')
    a,b,cvertex,weights=balances[0]
    return {'minimum_signed_chart_height':c.encode(),'squared_normal_norm':N.encode(),
            'positive_active_vertices':[encode(v) for v in active],
            'positive_three_vertex_balance':{'vertices':[encode(v) for v in (a,b,cvertex)],
                'weights':[w.encode() for w in weights],'nearest_point':encode(y)},
            'active_count':len(active)}


def hull_data(n,V):
    S={project(v,n) for v in V};H=exact_hull(S,n)
    C=tuple(sum((cross(p,q)[i] for p,q in zip(H,H[1:]+H[:1])),ZERO)/2 for i in range(3))
    area=dot(C,n)
    require(area>0,'positive full physical area branch')
    normals=[cross(subtract(q,p),n) for p,q in zip(H,H[1:]+H[:1])]
    require(all(all(dot(m,subtract(p,v))>=0 for v in V) for m,p in zip(normals,H)),
            'every original vertex must satisfy every full-hull support')
    rho2=7+8*PHI-(19-8*PHI)/29
    circle={p for p in S if dot(p,p)==rho2}
    require(len(S)==60 and len(H)==16 and len(circle)==8,
            'complete beta shadow: sixty original projections, sixteen corners, eight circle points')
    return S,H,normals,C,area*area/dot(n,n),circle


@dataclass(frozen=True)
class Interval:
    lo:F
    hi:F
    def __post_init__(self):
        object.__setattr__(self,'lo',F(self.lo));object.__setattr__(self,'hi',F(self.hi))
        require(self.lo<=self.hi,'outward interval order')
    def __add__(self,b):return Interval(self.lo+b.lo,self.hi+b.hi)
    def __sub__(self,b):return Interval(self.lo-b.hi,self.hi-b.lo)
    def __mul__(self,b):
        values=(self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi)
        return Interval(min(values),max(values))
    def scale(self,s):
        s=F(s)
        return Interval(self.lo*s,self.hi*s) if s>=0 else Interval(self.hi*s,self.lo*s)
    def divide_positive(self,b):
        require(b.lo>0,'positive denominator branch required')
        return self*Interval(1/b.hi,1/b.lo)


_root_cache={}


def root(q):
    if q not in _root_cache:
        a,b=root_bounds(q);verify_root(q,a,b);_root_cache[q]=Interval(a,b)
    return _root_cache[q]


phi_interval=(root(QPhi(5))+Interval(1,1)).scale(F(1,2))


def field(q):return Interval(q.a,q.a)+phi_interval.scale(q.b)


def source_coordinates(H,n):
    e=(QPhi(1),ZERO,ZERO);e2=cross(n,e);N=root(dot(n,n))
    require(n[0]==ZERO,'shared orthonormal chart x axis')
    return [(field(p[0]),field(dot(p,e2)).divide_positive(N)) for p in H]


def facet_coefficients(H,n,S):
    e2=cross(n,(QPhi(1),ZERO,ZERO));N=root(dot(n,n));out=[]
    for p,q in zip(H,H[1:]+H[:1]):
        m=cross(subtract(q,p),n);M=root(dot(m,m))
        mx=field(m[0]).divide_positive(M)
        my=field(dot(m,e2)).divide_positive(N).divide_positive(M)
        h=field(dot(m,p)).divide_positive(M)
        require(h.lo>0,'positive original unit target support')
        for px,py in S:
            A=mx*px+my*py;B=my*px-mx*py
            out.append((A,B,h))
    return out


def complete_circle_parameters(grid=128):
    return [(quarter,j) for quarter in range(4) for j in range(grid+1)]


def validate_circle_parameters(samples,grid=128):
    require(grid==128 and samples==complete_circle_parameters(grid),
            'all four CLOSED quarters, endpoints and grid points required')


def validate_margin(grid=128,threshold=F(3,40),eta=F(2687,96000)):
    require(grid>0 and threshold>0 and eta>=0,'positive cover constants')
    margin=threshold-F(9,2*grid)-eta
    require(margin>F(1,100),'complete-circle/source-transport losses exceed margin')
    return margin


def circle_bound(H,n,S,grid=128,threshold=F(3,40)):
    require(grid==128,'fixed complete grid policy')
    validate_circle_parameters(complete_circle_parameters(grid),grid)
    validate_margin(grid,threshold)
    coefficients=facet_coefficients(H,n,S);records=[];mins=[]
    for quarter in range(4):
        lows=[]
        for j in range(grid+1):
            t=F(j,grid);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
            require(c*c+s*s==1,'exact rational unit-circle sample')
            for k in range(quarter):c,s=-s,c
            best=None
            for index,(A,B,h) in enumerate(coefficients):
                low=A.scale(c).lo+B.scale(s).lo-h.hi
                if best is None or low>best[0]:best=(low,index)
            require(best[0]>threshold,'no validated full-roll gap at sample')
            lows.append(best[0]);records.append((quarter,j,best[1],str(best[0])))
        mins.append(min(lows))
    raw=json.dumps(records,separators=(',',':')).encode()
    return {'quarter_count':4,'parameter_grid':grid,'complete_sample_cases':4*(grid+1),
            'full_original_receiver_facets':len(H),'original_source_corner_count':len(S),
            'evaluated_actual_facet_corner_sample_triples':len(coefficients)*4*(grid+1),
            'quarter_minimum_witness_gap_lower':[str(q) for q in mins],
            'all_witness_gaps_strictly_above':str(threshold),
            'exact_full_generated_witness_record_sha256':hashlib.sha256(raw).hexdigest(),
            'max_nearest_sample_full_circle_angle':'1/128',
            'source_support_Lipschitz_loss_upper':'9/256',
            'minimal_transport_selected_corner_error_upper':'2687/96000',
            'strict_all_winning_source_support_separation_margin_lower':'569/48000'}


I=tuple(tuple(QPhi(int(i==j)) for j in range(3)) for i in range(3))
REFS=((ZERO,QPhi(1),-3-3*PHI),(ZERO,QPhi(1),(3*PHI-1)/11))


def validate_proper(M):
    require(matmul(M,tuple(zip(*M)))==I and determinant(*M)==QPhi(1),
            'orthogonal determinant-positive full spatial rotation required')


def region_key(n,A):
    signs=[dot(v,n).sign() for v in A]
    require(0 not in signs,'strict signed region required')
    bits=sum((s>0)<<i for i,s in enumerate(signs))
    return min(bits,((1<<30)-1)^bits)


def validate_axis_set(axes,G,n):
    require(len(axes)==30 and axes=={canonical(act(g,n)) for g in G},
            'complete thirty-axis actual proper-body orbit required')


def threshold_axes(V,G,global_data):
    A=representatives(V);orbits=[];all_axes=set();records=[];keys=set()
    for n in REFS:
        axes={canonical(act(g,n)) for g in G};validate_axis_set(axes,G,n)
        require(not axes&all_axes,'two threshold body orbits must be disjoint')
        all_axes.update(axes)
        directed={act(g,n) for g in G}
        require(len(directed)==60 and {tuple(-q for q in k) for k in directed}==directed,
                'all directed normals and their reversals covered by actual body rotations')
        require(sum(act(g,n)==n for g in G)==1 and
                sum(canonical(act(g,n))==canonical(n) for g in G)==2,
                'exact directed and projective stabilizers')
        for k in sorted(axes,key=order):
            key=region_key(k,A);require(key not in keys,'distinct threshold strict signed regions')
            keys.add(key);balance=active_balance(k,V)
            require(balance['active_count']==4,'complete four-positive-original-active beta stratum')
            records.append({'region_sign_bits':key,'direction':encode(k),'balance':balance})
        orbits.append({'representative':encode(n),'projective_axes':30,
                       'proper_directed_orbit':60,'signed_directed_orbit':60,
                       'proper_directed_stabilizer':1,'proper_projective_stabilizer':2,
                       'representative_balance':active_balance(n,V)})
    counts=global_data['diameter_and_sign_regions']['score_counts']
    require(sum(r['regions'] for r in counts if r['score']==BETA.encode())==60,
            'pinned complete global spectrum must have exactly sixty beta regional maxima')
    require(len(all_axes)==len(keys)==60,'all nonwinning beta regions individually identified')
    records.sort(key=lambda r:r['region_sign_bits'])
    raw=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    return {'complete_threshold_projective_axes':60,'body_projective_orbits':orbits,
            'all_sixty_axes_and_regions':[{'direction':r['direction'],
                                         'region_sign_bits':r['region_sign_bits']} for r in records],
            'all_sixty_original_positive_balance_records_sha256':hashlib.sha256(raw).hexdigest(),
            'actual_positive_balances_verified':60,'active_count_distribution':{'4':60},
            'completeness_uses_pinned_global_spectrum_and_written_regional_uniqueness':True}


def validate_hull(n,V,S,H):
    require(S=={project(v,n) for v in V} and len(S)==60,'all original projected vertices required')
    require(H==exact_hull(S,n) and len(H)==16,'complete correctly oriented actual sixteen-corner hull')


def validate_circle(S,circle):
    rho2=7+8*PHI-BETA
    require(len(circle)==8 and circle=={p for p in S if dot(p,p)==rho2} and
            max(dot(p,p) for p in S)==rho2,'complete actual eight-point maximum circle required')


def threefold_source(V,winning_data):
    B=geometry()[0][0][1];N=dot(B,B)
    record,points,facets=winning.active_hexagon()
    require(record==winning_data['complete_positive_active_tangent_hexagon'],
            'every full six-active-tangent-hexagon entry must match the published predecessor')
    S={project(v,B) for v in V};H=exact_hull(S,B);rho2=7+8*PHI-QPhi(F(1,3))
    require(len(H)==12 and all(dot(p,p)==rho2 for p in H),'complete threefold circle dodecagon')
    preimages=[]
    for p in H:
        original=[v for v in V if project(v,B)==p]
        require(len(original)==1 and 3*dot(original[0],B)**2==N,
                'unique actual original corner preimage with squared height one third')
        preimages.append(original[0])
    normals=[cross(subtract(q,p),B) for p,q in zip(H,H[1:]+H[:1])]
    require(all(dot(m,subtract(p,v))>=0 for m,p in zip(normals,H) for v in V),
            'all 720 original source corner-edge support comparisons')
    c0=F(289,500);radius=F(9,2);chord=F(1,24);q=F(57,125)
    require(QPhi(F(1,3))<QPhi(c0*c0) and 7+8*PHI<QPhi(radius*radius),
            'exact source height and body radius rational upper bounds')
    require(QPhi(q*q)<BETA and F(101,300)*(c0-q)<chord,
            'full active-hexagon coercivity puts every winning source inside the chord bound')
    eta=c0*chord+radius*chord*chord/2
    require(eta==F(2687,96000) and validate_margin()==F(569,48000),
            'source movement and whole-circle continuum margin')
    return B,H,{'complete_center_corner_count':12,'all_original_source_support_comparisons':720,
                'actual_unique_original_corner_preimages':[encode(v) for v in preimages],
                'complete_center_hull':[encode(p) for p in H],
                'complete_positive_active_tangent_hexagon_every_entry_matches_parent':True,
                'full_active_tangent_support_comparisons':record['original_tangent_support_comparisons'],
                'source_normal_chord_upper':str(chord),'actual_corner_axial_height_squared':['1/3','0'],
                'uniform_selected_corner_transport_upper':str(eta),
                'full_circle_Lipschitz_loss_upper':'9/256',
                'strict_uniform_winning_source_separation_margin_lower':'569/48000'}


def exact_rotations(G,axes):
    a=(2*PHI-1)/5
    M=((QPhi(1),ZERO,ZERO),(ZERO,a,-2*a),(ZERO,-2*a,-a))
    H=tuple(tuple(-x for x in row) for row in M)
    L=((QPhi(1),ZERO,ZERO),(ZERO,QPhi(-1),ZERO),(ZERO,ZERO,QPhi(-1)))
    R=matmul(H,L);validate_proper(H);validate_proper(R);require(L in G,'original body half turn')
    y=[decode(o['representative_balance']['positive_three_vertex_balance']['nearest_point'])
       for o in axes['body_projective_orbits']]
    require(act(R,y[0])==y[1] and act(R,y[1])==y[0],
            'proper full spatial alignment of positive directed unit normals')
    require(determinant(*M)==QPhi(-1),'recorded active alignment is improper and cannot stand alone')
    axis=(ZERO,PHI,QPhi(-1));N=dot(axis,axis);c=PHI/2;t=(PHI-1)/2
    skew=((ZERO,-axis[2],axis[1]),(axis[2],ZERO,-axis[0]),(-axis[1],axis[0],ZERO))
    C=tuple(tuple(c*I[i][j]+(1-c)*axis[i]*axis[j]/N+t*skew[i][j]
                  for j in range(3)) for i in range(3))
    validate_proper(C);require(c*c+N*t*t==QPhi(1),'positive Rodrigues sine branch')
    powers=[I]
    for j in range(5):powers.append(matmul(C,powers[-1]))
    require(C not in G and powers[2] in G and powers[4] in G and powers[5]==R,
            'exact nonbody 36 degree rotation with squared body rotation and fifth power R')
    require({matmul(C,g) for g in G}=={matmul(H,g) for g in G},
            '36 degree turn and proper active alignment give the same left body coset')
    return R,C,{'improper_active_alignment_matrix':[encode(row) for row in M],
                'proper_positive_normal_alignment_matrix':[encode(row) for row in R],
                'proper_36_degree_rotation_matrix':[encode(row) for row in C],
                'proper_36_degree_rotation_axis':encode(axis),'cosine_36_degrees':c.encode(),
                'sine_over_axis_norm_positive':t.encode(),
                '36_degree_turn_is_not_body_symmetry':True,
                '72_degree_square_is_actual_body_symmetry':True,
                'fifth_power_equals_proper_circle_alignment':True,
                '36_degree_left_body_coset_equals_proper_alignment_coset':True}


def finite_threshold_comparisons(V,hulls,R):
    rho2=7+8*PHI-BETA;pairs=[]
    for si,ti in [(0,0),(0,1),(1,0),(1,1)]:
        source,target=hulls[si],hulls[ti];A=I if si==ti else R
        # R maps positive normals in both directions. Its action on the body
        # agrees as a set with the prototype's improper M by central symmetry.
        mapped={act(A,p) for p in source[5]}
        require(mapped==target[5],'all eight actual source circle points align')
        pivot=min(mapped,key=order);valid=[]
        for q in sorted(target[5],key=order):
            c,t,rotate=circle_map(REFS[ti],rho2,pivot,q)
            if {rotate(p) for p in mapped}!=target[5]:continue
            rotated={rotate(act(A,p)) for p in source[0]}
            gaps=[dot(m,subtract(p,v)) for m,p in zip(target[2],target[1]) for v in rotated]
            contained=min(gaps)>=0;equal=set(target[1])<=rotated and contained
            valid.append({'cosine':c.encode(),'scaled_axial_sine':t.encode(),
                          'source_contained_in_receiver':contained,'full_shadows_equal':equal,
                          'minimum_full_original_support_gap':min(gaps).encode(),
                          'support_comparisons':len(gaps)})
        require(len(valid)==2 and {tuple(v['cosine']) for v in valid}=={('1','0'),('-1','0')} and
                all(v['scaled_axial_sine']==['0','0'] for v in valid),
                'only zero and half-turn rolls preserve the complete threshold circle')
        require(all(v['source_contained_in_receiver']==(si<=ti) and
                    v['full_shadows_equal']==(si==ti) for v in valid),
                'exact one-way unequal closed containment classification')
        pairs.append({'source_orbit':si,'receiver_orbit':ti,
                      'all_eight_possible_circle_correspondences':8,'circle_valid_rolls':valid})
    require(hulls[0][4]<hulls[1][4],'unequal physical shadow areas')
    return pairs


def closed_orientation_cosets(G,C):
    records=[]
    for i,n in enumerate(REFS):
        N=dot(n,n);J=tuple(tuple(2*n[j]*n[k]/N-I[j][k] for k in range(3)) for j in range(3))
        validate_proper(J)
        bases=[I,J] if i==0 else [I,J,C,matmul(J,C)]
        cosets=[{matmul(b,g) for g in G} for b in bases]
        require(all(len(s)==60 for s in cosets) and
                all(not a&b for a,b in combinations(cosets,2)),
                'all stated proper orientation left cosets must be pairwise disjoint')
        records.append({'receiver_orbit':i,'disjoint_left_cosets':len(cosets),
                        'closed_containment_proper_rotations':60*len(cosets),
                        'equal_shadow_rotations':120,'unequal_closed_containment_rotations':120*i,
                        'closed_containment_scale':'1','closed_containment_translation':'0'})
    return records


def check(self_test=False):
    V=vertices();A=representatives(V);G=symmetry_group(V,return_matrices=True)
    global_data=parent.fixture('global_cap_expected.json',GLOBAL_SHA)
    winning_data=parent.fixture('winning_receiver_expected.json',WINNING_SHA)
    axes=threshold_axes(V,G,global_data)
    B,H0,source=threefold_source(V,winning_data);coordinates=source_coordinates(H0,B)
    hulls=[hull_data(n,V) for n in REFS]
    for n,h in zip(REFS,hulls):validate_hull(n,V,h[0],h[1]);validate_circle(h[0],h[5])
    covers=[circle_bound(h[1],n,coordinates) for n,h in zip(REFS,hulls)]
    R,C,rotations=exact_rotations(G,axes)
    pairs=finite_threshold_comparisons(V,hulls,R);cosets=closed_orientation_cosets(G,C)
    rejected=0
    if self_test:
        controls=[lambda:representatives(set(sorted(V)[:-1])),
                  lambda:active_balance(B,V),
                  lambda:validate_axis_set(set(sorted({canonical(act(g,REFS[0])) for g in G})[:-1]),G,REFS[0]),
                  lambda:validate_proper(tuple(decode(row) for row in rotations['improper_active_alignment_matrix'])),
                  lambda:validate_hull(REFS[0],V,hulls[0][0],hulls[0][1][:-1]),
                  lambda:validate_hull(REFS[0],V,hulls[0][0],list(reversed(hulls[0][1]))),
                  lambda:validate_circle(hulls[0][0],set(sorted(hulls[0][5])[:-1])),
                  lambda:Interval(1,0),
                  lambda:Interval(1,2).divide_positive(Interval(0,1)),
                  lambda:verify_root(QPhi(5),F(3),F(4)),
                  lambda:validate_circle_parameters(complete_circle_parameters()[:387]),
                  lambda:validate_circle_parameters(complete_circle_parameters()[:-1]),
                  lambda:validate_circle_parameters([complete_circle_parameters()[0]]+complete_circle_parameters()),
                  lambda:validate_margin(grid=64),
                  lambda:circle_bound(hulls[0][1],REFS[0],coordinates,threshold=F(1,4))]
        for control in controls:expect_rejection(control);rejected+=1
    return rational_strings({'agent':'six-rupert-3','role':'researcher',
        'proof_status':'unformalized_complete_all_threshold_receiver_exclusion_and_closed_boundary_classification',
        'global_RID':'OPEN','global_non_rupert_proved':False,'beta':BETA.encode(),
        'global_necessary_receiver_condition_for_strict_passage':'f(n)^2 < beta',
        'equivalent_strict_squared_receiver_diameter_lower':((736+960*PHI)/29).encode(),
        'all_receivers_f_squared_at_least_beta_excluded_for_strict_passage':True,
        'arbitrary_source_full_proper_rotation_roll_translation_scale_ge_one':True,
        'threshold_axis_classification':axes,'threefold_original_source_corner_bounds':source,
        'both_threshold_whole_circle_interval_covers':covers,
        'both_actual_threshold_full_hulls':[[encode(p) for p in h[1]] for h in hulls],
        'both_actual_threshold_maximum_circles':[[encode(p) for p in sorted(h[5],key=order)] for h in hulls],
        'threshold_squared_physical_shadow_areas':[h[4].encode() for h in hulls],
        'new_actual_target_original_support_comparisons':1920,
        'all_full_circle_actual_facet_corner_sample_evaluations':sum(c['evaluated_actual_facet_corner_sample_triples'] for c in covers),
        'exact_proper_rotations':rotations,'finite_equal_radius_source_comparisons':pairs,
        'finite_original_support_comparisons_for_circle_valid_rolls':7680,
        'closed_threshold_orientation_classifications':cosets,
        '36_degree_turn_gives_unequal_closed_containment_with_eight_shared_circle_points':True,
        '36_degree_example_is_not_strict_interior_passage':True,
        'new_malformed_controls_rejected':rejected,'pinned_winning_expected_sha256':WINNING_SHA,
        'pinned_global_expected_sha256':GLOBAL_SHA,
        'whole_six_active_hexagon_every_parent_entry_reproduced':True,
        'full_old_global_directional_or_winning_self_tests_replayed':False,
        'float_heuristic_samples_or_private_diagnostics_are_proof_inputs':False})


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    print(json.dumps(check(args.self_test),sort_keys=True,indent=2))
