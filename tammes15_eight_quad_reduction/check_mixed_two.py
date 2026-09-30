#!/usr/bin/env python3
"""Exact bookkeeping for MIXED_TWO.md; CPython>=3.11, standard library.

This is a necessary corner/boundary cover, not an embedding enumerator.
Trigonometric branches and the geometric eliminations are written proofs.
No expected output, scratch pilot, external data or solver is an input.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
import json
import sys

import check as base
import check_topology as topology
import check_five_corner_capacity as previous


def compose(p,q):
    out,power=(F(0),),(F(1),)
    for a in p:
        out=previous.add(out,previous.scale(a,power))
        power=previous.mul(power,q)
    return out


def verify_seven_polynomial(coefficients):
    base.need(tuple(map(F,coefficients))==tuple(map(F,(-8,-8,80,16,-200,120))),
              'seventh-angle polynomial coefficients')


def polynomial_checks():
    add,mul,scale=previous.add,previous.mul,previous.scale
    c=(F(0),F(1)); one=(F(1),)
    A=add(add(one,scale(2,c)),scale(-1,mul(c,c)))
    B=add(one,scale(2,c))
    N,D=compose((-1,21,-35,7),B),compose((-7,35,-21,1),B)
    P=add(scale(2,mul(mul(c,c),N)),scale(-1,mul(A,D)))
    verify_seven_polynomial(P)
    shifted=compose(P,(F(1,2),F(1)))
    base.need(shifted==(F(5,4),F(43,2),F(-46),F(-84),F(100),F(120)),
              'exact shifted seventh-angle coefficients')
    base.need(F(43,2)-F(46,10)-F(84,100)==F(803,50)>0,
              'strict lower bound on shifted polynomial')
    base.need(sum(a*2**i for i,a in enumerate((-7,35,-21,1)))==-13,
              'seventh-angle denominator at B=2')
    base.need(3*F(11,5)**2-42*2+35==F(-862,25)<0,
              'denominator derivative upper bound')
    base.need(add((F(2),),scale(-1,A))==(F(1),F(-2),F(1)),
              'w comparison gap is (1-c)^2')
    # A different representation derives the tangent formula from (S+i)^7.
    # Here S^2=B, rather than substituting a remembered tan(7 theta) formula.
    z,S=base.variable(0),base.variable(1)
    re,im=base.Poly(1),base.Poly(0)
    for _ in range(7):
        re,im=re*S-im,re+im*S
    Bz=1+2*z
    Dz=Bz**3-21*Bz**2+35*Bz-7
    Nz=7*Bz**3-35*Bz**2+21*Bz-1
    identities=(base.reduce_square(re-S*Dz,1,Bz),
                base.reduce_square(im-Nz,1,Bz),
                previous.symbolic(P,z)-(2*z**2*Nz-(1+2*z-z**2)*Dz),
                previous.symbolic(shifted,z)-previous.symbolic(P,z+F(1,2)),
                2-(1+2*z-z**2)-(1-z)**2)
    base.need(all(not p.terms for p in identities),
              'independent sparse complex-power and shift identities')
    base.need(23**2-2*16**2==17>0,'alpha>3pi/8 exact square margin')
    return {'coefficient_order':'ascending powers of c',
            'seven_angle_positive_numerator':[str(a) for a in P],
            'shift_c':'1/2+v, 0<v<1/10',
            'shifted_coefficients':[str(a) for a in shifted],
            'strict_lower_bound':'P>5/4+(803/50)v>0',
            'D_at_B2':-13,'D_derivative_upper_bound':'-862/25',
            'independent_sparse_complex_seventh_power_verified':True,
            'w_comparison_positive_gap':'2-A=(1-c)^2',
            'alpha_3pi8_square_margin':17,
            'proved_in_written_branch_argument':['y>7alpha-2pi','rho(z)>4alpha-pi'],
            'auxiliary_sign_interval':'1/2<c<3/5'}


def linear_angle_checks():
    lin,ladd,lscale=previous.lin,previous.ladd,previous.lscale
    pi,alpha,y=lin(1,0,0),lin(0,1,0),lin(0,0,1)
    x=lin(2,-4,0); z=lin(2,-2,-1)
    zeta=lin(0,3,-1); delta=lin(-4,12,0)
    residual=lin(-2,8,0); C1=lin(2,-1,-1)
    gap_y7=lin(2,-7,1); gap_y=lin(-1,1,1)
    base.need(ladd(ladd(ladd(alpha,y),lscale(2,x)),lscale(-2,pi))==gap_y7,
              'D with y cannot have two x corners')
    base.need(ladd(x,lscale(-1,zeta))==gap_y7,'zeta<x')
    base.need(ladd(delta,lscale(-1,x))==lin(-6,16,0),'three-x Z0 residual exceeds x')
    base.need(ladd(C1,lscale(-1,zeta))==x,'k3 would force an extra x occurrence')
    base.need(ladd(residual,lscale(-2,zeta))==lscale(2,gap_y),
              'two Z0 zeta corners have too small a sum')
    base.need(ladd(C1,lscale(-1,alpha))==z,
              'each non-y D Q angle is strictly below z')
    base.need(ladd(ladd(lscale(2,x),y),alpha)==ladd(lscale(2,pi),gap_y7),
              'Z0 with two x corners cannot have a corner above y')
    base.need(residual==lscale(2,lin(-1,4,0)),
              'two w corners exceed residual Z0 angle sum')
    return {'formal_variable_order':['pi','alpha','y'],
            'x':[str(a) for a in x],'z':[str(a) for a in z],
            'zeta':[str(a) for a in zeta],'three_x_residual_delta':[str(a) for a in delta],
            'two_x_residual':[str(a) for a in residual],
            'D_alpha_y_two_x_excess':[str(a) for a in gap_y7],
            'two_x_residual_minus_two_zeta':[str(a) for a in lscale(2,gap_y)],
            'sign_bridges_are_written_geometric_proofs':True}


def no_double_five_checks():
    opposites=[]
    for targets in product(range(3),repeat=4):
        counts=tuple(targets.count(i) for i in range(3))
        if counts[0]<=1 and counts[1]<=1 and counts[2]<=3:
            opposites.append(counts)
    histogram=Counter(c[2] for c in opposites)
    base.need(len(opposites)==20 and histogram=={2:12,3:8},
              'all marked opposite-five x-slot allocations')
    lower,upper=8,4+1+1+3
    parity_candidates=[n for n in range(lower,upper+1) if n%2==0]
    base.need(parity_candidates==[8],'global x-occurrence parity forbids any extra x')
    # Three remaining Qs accommodate all six R z corners. No adjacent pair
    # of z corners is possible when z<b; at most two occur in each face.
    final_counts=[a for a in product(range(3),repeat=3) if sum(a)==6]
    base.need(final_counts==[(2,2,2)],'complete late ordinary-four corner count')
    return {'four_labeled_opposite_slots_checked':81,
            'admitted_opposite_assignments':20,
            'counts_by_marked_Z0_x_corners':dict(sorted(histogram.items())),
            'global_x_occurrence_lower_bound':lower,'global_x_occurrence_upper_bound':upper,
            'even_global_x_occurrence_candidates':parity_candidates,
            'two_D_small_opposite_pairings':['D1/D2','D1/Z0 and D2/Z0'],
            'late_Q_R_corner_count_vectors':[list(a) for a in final_counts],
            'geometric_elimination_of_both_k_values_is_written':True}


def zero_graph(mask):
    base.need(type(mask) is int and 0<=mask<8,'three-label zero graph mask')
    pairs=tuple(combinations(range(3),2))
    edges={pair for i,pair in enumerate(pairs) if mask>>i&1}
    base.need(len(edges)<=2,'zero graph cannot be a contact triangle')
    adj=[set() for _ in range(3)]
    for i,j in edges:
        adj[i].add(j); adj[j].add(i)
    return edges,adj


def labeled_boundary_checks():
    """U1,U2,Z0 labeled 0,1,2; D and adjacent R labels kept distinct.

    The separated R labels are fixed by relabeling the ordinary fours.
    Zero-neighbor subsets exclude adjacent Z pairs by the facial-triangle
    rule. The cover is only necessary, and the elimination is hand geometry.
    """
    counts=Counter()
    e1_D_patterns=Counter()
    e2_candidate_histogram=Counter()
    for s in (2,4,6):
        for mask in range(7):
            edges,adj=zero_graph(mask); e=len(edges)
            if e-s//2<0:
                continue
            b=10-2*e; h=e-s//2
            targets=[3-len(adj[0]),3-len(adj[1]),4-len(adj[2])]
            Doptions=[a for k in range(3) for a in combinations(range(3),k)
                      if not any(tuple(sorted(pair)) in edges for pair in combinations(a,2))]
            for Ds in product(Doptions,repeat=2):
                for Rs in product((None,0,1,2),repeat=6-s):
                    counts['labeled_vectors_checked']+=1
                    columns=[sum(i in a for a in Ds)+Rs.count(i) for i in range(3)]
                    if columns!=targets:
                        continue
                    tag=f's{s}e{e}'
                    counts[tag+'_column_matched']+=1
                    base.need(sum(columns)==b,'labeled zero boundary sum')
                    stubs=tuple(2-len(a) for a in Ds)+tuple(int(a is None) for a in Rs)
                    base.need(sum(stubs)==2*h,'independent W-W QQ end sum')
                    if not topology.QQ_graphs(tuple(d for d in stubs if d)):
                        counts[tag+'_nongraphical']+=1
                        continue
                    common=[len(adj[i]&adj[j])+sum(i in a and j in a for a in Ds)
                            for i,j in combinations(range(3),2)]
                    if max(common)>2:
                        counts[tag+'_common_neighbor_rejected']+=1
                        continue
                    counts[tag+'_before_five_roles']+=1
                    if s==4:
                        raise ValueError('s4 common-contact obstruction missed')
                    base.need(s==2 and e in (1,2),'double-five necessary cases exhausted')
                    if e==1:
                        base.need(h==0 and all(len(a)==2 for a in Ds)
                                  and all(a is not None for a in Rs),'e1 saturates all boundary slots')
                        if targets[2]<4:
                            counts['e1_two_single_Q_opposites_exceed_Z0_boundary']+=1
                            continue
                        base.need(edges=={(0,1)} and all(2 in a for a in Ds)
                                  and Rs.count(2)==2,'e1 forced D,D,R,R at Z0')
                        e1_D_patterns[Ds]+=1
                        counts['e1_remaining_angle_frame_models']+=1
                    else:
                        base.need(targets[2]<=3 and all(len(a)>0 for a in Ds)
                                  and tuple(sorted(d for d in stubs if d))==(1,1),
                                  'e2: connected zeros and exactly two one-stub W vertices')
                        # S fours have already supplied y in the double-five Q.
                        # Only D with one Z neighbor and unattached adjacent R
                        # have an available Z-free Q for a further y occurrence.
                        weak_D=[i for i,a in enumerate(Ds) if len(a)==1]
                        weak_R=[i for i,a in enumerate(Rs) if a is None]
                        base.need(len(weak_D)+len(weak_R)==2,'complete eligible provider set')
                        e2_candidate_histogram[len(weak_D)]+=1
                        for chosen in weak_D:
                            other_providers=[('D',i) for i in weak_D if i!=chosen]
                            other_providers += [('R',i) for i in weak_R]
                            base.need(len(other_providers)<=1,
                                      'single-five Q opposite D cannot have two distinct y providers')
                        counts['e2_insufficient_Y_for_any_required_D_opposite']+=1
    expected={'labeled_vectors_checked':48048,
              's2e1_column_matched':116,'s2e1_before_five_roles':116,
              'e1_two_single_Q_opposites_exceed_Z0_boundary':80,
              'e1_remaining_angle_frame_models':36,
              's2e2_column_matched':600,'s2e2_nongraphical':72,
              's2e2_common_neighbor_rejected':30,'s2e2_before_five_roles':498,
              'e2_insufficient_Y_for_any_required_D_opposite':498,
              's4e2_column_matched':5,'s4e2_common_neighbor_rejected':5}
    base.need(dict(counts)==expected,'complete labeled boundary census counts')
    base.need(sum(e1_D_patterns.values())==36 and len(e1_D_patterns)==4,
              'all four ordered D-zero-pair patterns in e1 angle frames')
    return {'zero_label_order':['U1','U2','Z0'],
            'separated_R_labels_fixed_by_relabeling':True,'counts':dict(sorted(counts.items())),
            'e1_distinct_D_pair_patterns':len(e1_D_patterns),
            'e2_model_histogram_by_possible_D_single_Q_opposites':dict(sorted(e2_candidate_histogram.items())),
            's6_forbidden_by_negative_W_W_QQ_edge_count':True,
            'not_an_embedding_enumeration':True}


def cyclic_frame_checks():
    counts=Counter()
    for frame in permutations(range(4)):  # D1,D2,R1,R2
        for marked_parity in range(2):
            counts['labeled_cyclic_frames']+=1
            free=[i for i in range(4) if i%2!=marked_parity]
            pairs=[(frame[i],frame[(i+1)%4]) for i in free]
            if any((i<2)!=(j<2) for i,j in pairs):
                counts['free_D_R_opposite_pair_rejected']+=1
                continue
            base.need(sorted(sum(i<2 for i in pair) for pair in pairs)==[0,2],
                      'remaining free pairs are exactly DD and RR')
            counts['free_D_D_and_R_R_angle_contradiction']+=1
    base.need(counts=={'labeled_cyclic_frames':48,'free_D_R_opposite_pair_rejected':32,
                      'free_D_D_and_R_R_angle_contradiction':16},'complete cyclic frame cover')
    return dict(sorted(counts.items()))


def five_matching(mask):
    base.need(type(mask) is int and 0<=mask<16,'K2,2 five contact mask')
    pairs=tuple(product((0,1),(2,3)))
    degrees=[0]*4
    for i,(u,v) in enumerate(pairs):
        if mask>>i&1:
            degrees[u]+=1; degrees[v]+=1
    base.need(max(degrees)<=1,'two double-five Qs force a matching of five contacts')
    return mask.bit_count()


def four_five_checks():
    histogram=Counter()
    for mask in range(16):
        try:
            count=five_matching(mask)
        except ValueError:
            continue
        histogram[count]+=1
    base.need(histogram=={0:1,1:4,2:2},'complete K2,2 matching cover')
    base.need(4*4>10+2*2,'two double-five Qs give too few T corners at four fives')
    return {'labeled_K2_2_contact_masks_checked':16,'admissible_matchings':7,
            'matchings_by_edge_count':dict(sorted(histogram.items())),
            'maximum_two_five_T_faces':4,'maximum_T_five_corners':14,
            'required_T_five_corners':16,
            'conclusion':'Exactly four ordinary fives cannot occupy two double-five Qs',
            'ordinary_five_premise_explicit_on_auxiliary_interval':True}


def cover():
    old=previous.cover()
    removed=[p for p in old['profiles'] if p['d42']==1 and p['n3']==2]
    retained=[p for p in old['profiles'] if p not in removed]
    direct=[]
    for row in old['distributions']:
        if not row['allowed_H_codes']:
            continue
        for r,n4,n5 in product(range(16),repeat=3):
            if r+n4+n5!=15 or 3*r+4*n4+5*n5!=62:
                continue
            if (r<=2 and not (row['d42']==1 and r==2)
                    and n4>=row['d41']+row['d42']):
                direct.append({'d41':row['d41'],'d42':row['d42'],'d51':row['d51'],
                               'n3':r,'n4':n4,'n5':n5,'H_codes':row['allowed_H_codes'][:]})
    base.need(retained==direct,'independent entry-level five-profile degree generation')
    base.need(len(removed)==1 and removed[0]['n4']==9 and removed[0]['n5']==4,
              'sole newly removed mixed r2 degree profile')
    rows=[]
    for oldrow in old['distributions']:
        row=dict(oldrow)
        row['surviving_degree_profiles']=sum(all(p[k]==row[k] for k in ('d41','d42','d51'))
                                              for p in retained)
        rows.append(row)
    base.need(len(retained)==5 and sum(len(row['allowed_H_codes']) for row in rows)==11,
              'five degree profiles and unchanged eleven global H types')
    return {'previous_degree_profiles':6,'remaining_degree_profiles':5,
            'previous_colored_H_types':11,'remaining_colored_H_types':11,
            'remaining_deficit_distributions':2,'removed_profiles':removed,
            'distributions':rows,'profiles':retained,
            'restriction':'mixed zero-triangle-four distribution has n3<=1',
            'auxiliary_four_five_restriction':'f2<=1 when n5=4 and all fives are ordinary'}


def selftest():
    controls=0
    def test(value,message):
        nonlocal controls
        base.need(value,message); controls+=1
    def rejects(call,message):
        nonlocal controls
        try:
            call()
        except ValueError:
            controls+=1
        else:
            raise ValueError(message)
    for mask in (-1,8,True,7):
        rejects(lambda m=mask:zero_graph(m),'invalid or triangular zero graph accepted')
    for mask in (-1,16,True,3,5,15):
        rejects(lambda m=mask:five_matching(m),'invalid or nonmatching F graph accepted')
    for bad in ((-7,-8,80,16,-200,120),(-8,-8,80,16,-200,119)):
        rejects(lambda p=bad:verify_seven_polynomial(p),'corrupted seventh-angle coefficient accepted')
    test(not topology.QQ_graphs((2,)),'lone two-stub vertex cannot form a simple QQ graph')
    test(topology.QQ_graphs((1,1))==(1,),'two one-stub vertices form exactly one QQ edge')
    test(F(803,50)>0 and F(5,4)>0,'strict seventh-angle margins')
    test(23**2>2*16**2,'strict alpha lower-bound margin')
    test(cyclic_frame_checks()['labeled_cyclic_frames']==48,'cyclic frame cover retained')
    test(no_double_five_checks()['late_Q_R_corner_count_vectors']==[[2,2,2]],
         'late ordinary-four corners require three opposite pairs')
    test(cover()['remaining_degree_profiles']==5,'new profile count')
    test(any(p['d42']==1 and p['n3']==2 for p in previous.cover()['profiles']),
         'new mixed profile was retained by the prior checker')
    return controls


def main():
    base.need(sys.argv[1:] in ([],['--selftest']),'usage: check_mixed_two.py [--selftest]')
    # Audit all local incidence masks using the preceding independently
    # written star code, not a hard-coded assumption about free Q sectors.
    local=topology.local_checks()
    out={'agent':'six-tammes-1','role':'researcher',
         'scope':'exact necessary corner/boundary cover; geometric eliminations written separately',
         'polynomial_checks':polynomial_checks(),'linear_angle_checks':linear_angle_checks(),
         'local_star_checks':local,'no_double_five_corner_checks':no_double_five_checks(),
         'labeled_boundary_checks':labeled_boundary_checks(),'cyclic_frame_checks':cyclic_frame_checks(),
         'four_five_matching_checks':four_five_checks(),'cover':cover()}
    if sys.argv[1:]:
        print(json.dumps({'status':'PASS','controls':selftest(),'degree_profiles':5,
                          'colored_H_types':11,'mixed_maximum_n3':1},sort_keys=True))
    else:
        print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
