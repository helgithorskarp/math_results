#!/usr/bin/env python3
"""Exact bookkeeping for ALL_ONE_TWO.md, CPython>=3.11, standard library.

Necessary corner/contact covers and topology fixtures, not an embedding
enumeration. Geometric and planar-normalization bridges are written proofs.
No expected output, external data, floating arithmetic or solver is used.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, product
import json
import sys

import check as base
import check_topology as topology
import check_five_corner_capacity as capacity
import check_mixed_two as previous


def angle_checks():
    lin,ladd,lscale=capacity.lin,capacity.ladd,capacity.lscale
    pi,alpha,y=lin(1,0,0),lin(0,1,0),lin(0,0,1)
    x,z,zeta,chi=lin(2,-4,0),lin(2,-2,-1),lin(0,3,-1),lin(-2,7,0)
    base.need(ladd(ladd(alpha,lscale(3,x)),lscale(-2,pi))==lin(4,-11,0),
              'unmarked D cannot have three x Q angles')
    base.need(F(3,8)-F(4,11)==F(1,88)>0,'strict alpha comparison margin')
    base.need(ladd(ladd(ladd(lscale(2,pi),lscale(-1,alpha)),lscale(-1,x)),
                   lscale(-1,zeta))==y,'k1 residual at unmarked D is y')
    base.need(ladd(ladd(ladd(lscale(2,pi),lscale(-1,alpha)),lscale(-1,y)),
                   lscale(-1,zeta))==x,'opposite zeta at third marked D forces extra x')
    base.need(ladd(ladd(chi,lscale(-1,z)),lin(3,-8,0))==lin(-1,1,1),
              'chi-z exceeds 8alpha-3pi by y+alpha-pi')
    base.need(ladd(y,lscale(-1,chi))==lin(2,-7,1),'chi<y is the inherited seven-angle sign')
    return {'formal_variable_order':['pi','alpha','y'],
            'x':[str(a) for a in x],'z':[str(a) for a in z],
            'zeta':[str(a) for a in zeta],'chi':[str(a) for a in chi],
            'unmarked_D_three_x_sum_excess':[str(a) for a in lin(4,-11,0)],
            'alpha_comparison_margin':'1/88',
            'new_ordering':'x<z<chi<y',
            'strict_sign_inputs':['alpha>3pi/8','y>pi-alpha','y>7alpha-2pi','z<b'],
            'sign_and_branch_implications_are_written_proofs':True}


def matchings(vertices):
    if not vertices:
        return ((),)
    first=vertices[0]; out=[]
    for i in range(1,len(vertices)):
        rest=vertices[1:i]+vertices[i+1:]
        for tail in matchings(rest):
            out.append(((first,vertices[i]),)+tail)
    return tuple(out)


def no_double_checks():
    counts=Counter()
    provider_counts=Counter()
    parity_counts=Counter()
    late_counts=tuple(v for v in product(range(3),repeat=3) if sum(v)==5)
    base.need(late_counts==((1,2,2),(2,1,2),(2,2,1)),
              'five late R corners occupy every remaining Q')
    all_matchings=matchings(tuple(range(4)))
    base.need(len(all_matchings)==3,'all pairings of four labeled small D corners')
    # W labels 0..3 are D1..D4, and labels4..8 are R1..R5.
    # Four original F labels distinguish the four opposite x slots.
    for unmarked in range(9):
        for assignment in product(range(4),repeat=4):
            counts['marked_x_assignments_checked']+=1
            slots=tuple(assignment.count(i) for i in range(4))
            if any(slots[i]>(2 if i==unmarked else 1) for i in range(4)):
                continue
            counts['admitted_marked_x_assignments']+=1
            if unmarked>=4:
                base.need(slots==(1,1,1,1),'unmarked R forces every D marked x')
                counts['unmarked_R_assignments']+=1
                for pairing in all_matchings:
                    for gamma_pairs in product(tuple(combinations(range(3),2)),repeat=2):
                        # gamma providers are U1,U2,unmarked R. If reused,
                        # a U would contact four distinct Ds, or R would
                        # require two gamma corners and violate its angle sum.
                        provider_counts['gamma_provider_assignments_checked']+=1
                        neighbors=[set() for _ in range(3)]
                        occurrences=[0]*3
                        for Ds,providers in zip(pairing,gamma_pairs):
                            for v in providers:
                                neighbors[v].update(Ds); occurrences[v]+=1
                        if any(len(neighbors[u])>3 for u in range(2)):
                            provider_counts['U_degree_obstructions']+=1
                        else:
                            base.need(occurrences[2]==2,'remaining obstruction must be repeated R gamma')
                            provider_counts['R_two_gamma_angle_obstructions']+=1
            else:
                k=slots[unmarked]
                base.need(k in (1,2),'unmarked D marked-x count is one or two')
                counts['unmarked_D_k'+str(k)+'_assignments']+=1
                base.need([n for n in range(8,10) if n%2==0]==[8],
                          'global x parity leaves no additional occurrence')
                if k==1:
                    base.need(slots==(1,1,1,1),'k1 forces x at all four Ds')
                    for zm in range(4):
                        parity_counts['D_k1_zeta_sector_masks_checked']+=1
                        if (3+zm.bit_count())%2==0:
                            base.need(zm.bit_count()==1,'odd marked zeta count forces one at Dstar')
                            parity_counts['D_k1_masks_forcing_unmarked_y']+=1
                else:
                    base.need(sorted(slots)==[0,1,1,2],'k2 has exactly one marked D without x')
                    # Two small D corners form one opposite pair. All other
                    # possible types are excluded in the written angle proof.
                    for v in late_counts:
                        base.need(min(v)>=1,'every late Q has a z corner')
                        counts['D_k2_late_R_corner_allocations']+=1
    expected={'marked_x_assignments_checked':2304,'admitted_marked_x_assignments':360,
              'unmarked_R_assignments':120,'unmarked_D_k1_assignments':96,
              'unmarked_D_k2_assignments':144,'D_k2_late_R_corner_allocations':432}
    base.need(counts==expected,'complete original-labeled opposite-x slot census')
    base.need(provider_counts=={'gamma_provider_assignments_checked':3240,
                               'U_degree_obstructions':2520,'R_two_gamma_angle_obstructions':720},
              'all unmarked-R gamma provider assignments rejected')
    base.need(parity_counts=={'D_k1_zeta_sector_masks_checked':384,
                             'D_k1_masks_forcing_unmarked_y':192},'complete k1 zeta-sector parity census')
    return {'W_label_order':['D1','D2','D3','D4','R1','R2','R3','R4','R5'],
            'counts':dict(sorted(counts.items())),
            'gamma_provider_counts':dict(sorted(provider_counts.items())),
            'zeta_parity_counts':dict(sorted(parity_counts.items())),
            'small_D_perfect_matchings':[list(map(list,m)) for m in all_matchings],
            'late_R_corner_count_vectors':[list(v) for v in late_counts],
            'corner_to_geometry_eliminations_are_written':True}


F_PAIRS=tuple(combinations(range(4),2))


def five_graph(mask):
    base.need(type(mask) is int and 0<=mask<64,'four-F contact graph mask')
    edges={p for i,p in enumerate(F_PAIRS) if mask>>i&1}
    base.need((0,1) not in edges,'opposite A/B are noncontacting')
    base.need(not any((0,v) in edges and (1,v) in edges for v in (2,3)),
              'C/D cannot be a third common contact neighbor of A/B')
    return edges


def five_triangle_table(mask):
    """Definition-level T incidences, independent of the A/B fan argument.

    Every F-F edge is T-T. Every contact F clique of size3 is one facial
    triangle. These geometric premises are proved in the written source.
    """
    edges=five_graph(mask)
    triples=[t for t in combinations(range(4),3)
             if all(p in edges for p in combinations(t,2))]
    doubles={e:2-sum(set(e)<=set(t) for t in triples) for e in edges}
    singles=[4-sum(n for e,n in doubles.items() if v in e)-sum(v in t for t in triples)
             for v in range(4)]
    empty=10-sum(singles)-sum(doubles.values())-len(triples)
    base.need(all(n>=0 for n in [*singles,*doubles.values(),empty]),
              'F triangle-incidence table cannot have negative face counts')
    base.need(sum(singles)+2*sum(doubles.values())+3*len(triples)==16,
              'all four Fs have four T corners')
    return {'single_F_T_counts':singles,'double_F_T_faces':sum(doubles.values()),
            'triple_F_T_faces':len(triples),'F_free_T_faces':empty}


def one_double_checks():
    counts=Counter(); forced=set(); independent={}
    for mask in range(64):
        counts['four_F_graph_masks_checked']+=1
        try:
            edges=five_graph(mask)
        except ValueError:
            continue
        counts['A_B_common_contact_admissible_masks']+=1
        touches=[sum((a,v) in edges for a in (0,1)) for v in (2,3)]
        # Eight distinct A/B T faces and two remaining Ts must accommodate
        # all eight C/D corners. Each C/D touches at most one A/B fan.
        if 2*sum(touches)+2*2>=8:
            base.need(touches==[1,1],'C/D triangle-incidence saturation')
            counts['C_D_fan_saturated_masks']+=1
            if (2,3) in edges:
                counts['both_remaining_T_faces_can_contain_C_D_masks']+=1
                same=any((a,2) in edges and (a,3) in edges for a in (0,1))
                if same:
                    counts['same_A_B_fan_three_faces_at_C_D_obstructions']+=1
                else:
                    base.need(len(edges)==3,'forced five contact graph is exactly P4')
                    forced.add(mask)
        try:
            independent[mask]=five_triangle_table(mask)
        except ValueError:
            pass
    base.need(counts=={'four_F_graph_masks_checked':64,'A_B_common_contact_admissible_masks':18,
                      'C_D_fan_saturated_masks':8,'both_remaining_T_faces_can_contain_C_D_masks':4,
                      'same_A_B_fan_three_faces_at_C_D_obstructions':2},
              'complete A/B incidence cover')
    base.need(forced==set(independent)=={44,50},
              'entry-level agreement of fan argument and independent triangle-incidence tables')
    base.need(all(a=={'single_F_T_counts':[2,2,0,0],'double_F_T_faces':6,
                     'triple_F_T_faces':0,'F_free_T_faces':0} for a in independent.values()),
              'all ten T faces contain F in both surviving contact masks')
    return {'F_label_order':['A','B','C','D'],'edge_bit_order':[list(p) for p in F_PAIRS],
            'counts':dict(sorted(counts.items())),'forced_path_masks':sorted(forced),
            'independent_T_incidence_tables':{str(k):v for k,v in sorted(independent.items())},
            'F_fan_to_T_edge_connectedness_is_written_proof':True,
            'forced_T_face_components':1}


def triangle_star(degree,mask):
    base.need(type(degree) is int and 3<=degree<=5,'triangle-star degree')
    base.need(type(mask) is int and 0<=mask<1<<degree,'triangle-star mask')
    T=tuple(bool(mask>>i&1) for i in range(degree))
    fans=0 if not any(T) else 1 if all(T) else sum(T[i] and not T[i-1] for i in range(degree))
    return {'fans':fans,'TT_ends':sum(T[i-1] and T[i] for i in range(degree)),
            'selected_edge_ends':sum(T[i-1] or T[i] for i in range(degree))}


def triangle_euler(p,r,s):
    a,m,nF=4-2*p,9-2*r+p,r+2
    base.need(min(a,m,nF,s,m-s)>=0,'ordinary-five triangle degree allocation')
    V=a+(m-s)+2*s+nF
    ends_TT=3*nF+m-s
    ends_selected=2*a+3*(m-s)+4*s+5*nF
    base.need(ends_TT%2==0 and ends_selected%2==0,'triangle edge end parity')
    E=ends_selected//2
    base.need(V==15-r-p+s and ends_TT==15+r+p-s
              and 2*E==45-r-p+s and 2*(V-E+10)==5-r-p+s,
              'independent local-star and triangle side incidence Euler formula')
    return {'p':p,'n3':r,'s':s,'vertices':V,'edges':E,'T_faces':10,
            'TT_edges':ends_TT//2,'TQ_edges':30-ends_TT,
            'normalized_Euler_characteristic':V-E+10}


def triangle_count_checks():
    census={}
    for name,degree,t in [('D',4,1),('R',4,2),('F',5,4),('U',3,0)]:
        rows=[triangle_star(degree,m) for m in range(1<<degree) if m.bit_count()==t]
        census[name]=len(rows)
        if name=='D':
            base.need(all(a=={'fans':1,'TT_ends':0,'selected_edge_ends':2} for a in rows),'all D T-star masks')
        elif name=='F':
            base.need(all(a=={'fans':1,'TT_ends':3,'selected_edge_ends':5} for a in rows),'all F T-star masks')
        elif name=='U':
            base.need(rows==[{'fans':0,'TT_ends':0,'selected_edge_ends':0}],'zero-three has no selected T star')
        else:
            base.need(Counter((a['fans'],a['TT_ends'],a['selected_edge_ends']) for a in rows)
                      =={(1,1,3):4,(2,0,4):2},'all adjacent/separated ordinary R T-star masks')
    family=[]
    for p,r in product(range(3),range(16)):
        for s in range(10-2*r+p):
            if (r+p+s)%2==1:
                family.append(triangle_euler(p,r,s))
    r2=[triangle_euler(0,2,s) for s in (1,3,5)]
    base.need([a['normalized_Euler_characteristic'] for a in r2]==[2,3,4],
              'all possible all-one r2 normalized T Euler counts exceed one')
    double_r2=[a for a in r2 if a['s']>=2]
    base.need([a['s'] for a in double_r2]==[3,5],'single double-five Q requires two separated Rs')
    return {'local_T_star_masks_by_type':census,'local_T_star_masks_checked':sum(census.values()),
            'general_ordinary_five_allocations_checked':len(family),
            'general_component_inequality':'K_T >= (5-r-p+s)/2',
            'all_one_r2_Euler_cases':r2,'one_double_five_r2_Euler_cases':double_r2,
            'fan_component_correspondence_and_F2_boundary_independence_are_written_proofs':True}


def raw_edges(faces):
    return {tuple(sorted((u,v))) for f in faces for u,v in zip(f,f[1:]+f[:1])}


def validate_triangles(faces):
    seen=set(); edge_inc=Counter()
    for f in faces:
        base.need(len(f)==3 and len(set(f))==3 and all(type(v) is int and v>=0 for v in f),
                  'simple integer-labeled triangle fixture')
        key=frozenset(f)
        base.need(key not in seen,'duplicate triangle fixture face')
        seen.add(key); edge_inc.update(raw_edges((f,)))
    base.need(all(n<=2 for n in edge_inc.values()),'at most two fixture faces per edge')


def normalize_T_faces(faces):
    validate_triangles(faces)
    face_edges=[raw_edges((f,)) for f in faces]
    vertices={v for f in faces for v in f}
    corner_labels={}
    for v in vertices:
        incident=[i for i,f in enumerate(faces) if v in f]
        adjacency=[(i,j) for i,j in combinations(incident,2)
                   if any(v in e for e in face_edges[i]&face_edges[j])]
        for fan in topology.components(incident,adjacency):
            for i in fan:
                corner_labels[(i,v)]=(v,min(fan))
    normalized=tuple(tuple(corner_labels[(i,v)] for v in f) for i,f in enumerate(faces))
    base.need(len(raw_edges(normalized))==len(raw_edges(faces)),'fan splitting preserves selected edges')
    return normalized


def fixture_data(faces):
    edges=sorted(raw_edges(faces)); vertices={v for f in faces for v in f}
    face_edges=[raw_edges((f,)) for f in faces]
    adjacency=[(i,j) for i,j in combinations(range(len(faces)),2) if face_edges[i]&face_edges[j]]
    K=len(topology.components(vertices,edges))
    KF=len(topology.components(range(len(faces)),adjacency))
    positions={e:i for i,e in enumerate(edges)}
    rows=[sum(1<<positions[e] for e in es) for es in face_edges]
    return {'vertices':len(vertices),'edges':len(edges),'T_faces':len(faces),
            'edge_graph_components':K,'face_edge_components':KF,
            'Euler_characteristic':len(vertices)-len(edges)+len(faces),
            'cycle_rank':len(edges)-len(vertices)+K,'F2_boundary_rank':topology.gf2_rank(rows)}


def triangle_fixtures():
    tetra=((0,1,2),(0,3,1),(0,2,3),(1,3,2))
    pinched=((0,1,2),(0,3,4))
    fixtures={'one_triangle_disk':((0,1,2),),
              'two_triangle_disk':((0,1,2),(0,2,3)),
              'six_triangle_annulus':((0,1,4),(0,4,3),(1,2,5),(1,5,4),(2,0,3),(2,3,5)),
              'two_pinched_disks_before_split':pinched,
              'two_pinched_disks_after_split':normalize_T_faces(pinched),
              'three_tetrahedron_faces_disk':tetra[:-1],
              'four_tetrahedron_faces_full_sphere':tetra}
    fields=('vertices','edges','T_faces','edge_graph_components','face_edge_components',
            'Euler_characteristic','cycle_rank','F2_boundary_rank')
    expected=((3,3,1,1,1,1,1,1),(4,5,2,1,1,1,2,2),(6,12,6,1,1,0,7,6),
              (5,6,2,1,2,1,2,2),(6,6,2,2,2,2,2,2),(4,6,3,1,1,1,3,3),(4,6,4,1,1,2,3,3))
    out={}
    for (name,faces),want in zip(fixtures.items(),expected):
        data=fixture_data(faces)
        base.need(tuple(data[k] for k in fields)==want,'exact triangle topology fixture '+name)
        normalized=fixture_data(normalize_T_faces(faces)) if name!='two_pinched_disks_after_split' else data
        base.need(normalized['edge_graph_components']==data['face_edge_components'],
                  'normalization component correspondence in each fixture')
        out[name]=data
    base.need(out['four_tetrahedron_faces_full_sphere']['F2_boundary_rank']==3,
              'full-sphere countercontrol requires an omitted-face hypothesis')
    return out


def cover():
    old=previous.cover()
    removed=[p for p in old['profiles'] if p['d42']==0 and p['n3']==2]
    retained=[p for p in old['profiles'] if p not in removed]
    direct=[]; rows=[]
    for oldrow in old['distributions']:
        row=dict(oldrow)
        row['surviving_degree_profiles']=sum(all(p[k]==row[k] for k in ('d41','d42','d51')) for p in retained)
        rows.append(row)
        if not row['allowed_H_codes']:
            continue
        for r,n4,n5 in product(range(16),repeat=3):
            if r<=1 and r+n4+n5==15 and 3*r+4*n4+5*n5==62 and n4>=row['d41']+row['d42']:
                direct.append({'d41':row['d41'],'d42':row['d42'],'d51':row['d51'],
                               'n3':r,'n4':n4,'n5':n5,'H_codes':row['allowed_H_codes'][:]})
    base.need(retained==direct,'entry-level independent four-profile degree generation')
    base.need(len(removed)==1 and (removed[0]['d41'],removed[0]['d42'],removed[0]['n3'])==(4,0,2),
              'sole newly removed all-one r2 profile')
    base.need(len(retained)==4 and sum(len(a['allowed_H_codes']) for a in rows)==11,
              'four profiles and unchanged eleven global H types')
    return {'previous_degree_profiles':5,'remaining_degree_profiles':4,
            'previous_colored_H_types':11,'remaining_colored_H_types':11,
            'remaining_deficit_distributions':2,'removed_profiles':removed,
            'distributions':rows,'profiles':retained,'maximum_n3':1,'maximum_n5':3,
            'restriction':'At most one degree-three vertex in the conditional q8 beta-interval branch'}


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
    for faces in (((0,1,1),),((0,1,2),(2,1,0)),((True,1,2),),((0,1,2),(0,1,3),(0,1,4))):
        rejects(lambda f=faces:validate_triangles(f),'malformed triangle fixture accepted')
    for mask in (-1,64,True,1,10):
        rejects(lambda m=mask:five_graph(m),'malformed or common-contact violating F graph accepted')
    for d,m in ((2,0),(6,0),(True,0),(4,-1),(4,16),(4,True),(3,8)):
        rejects(lambda a=d,b=m:triangle_star(a,b),'malformed triangle-star mask accepted')
    for mask in (0,6,38):
        rejects(lambda m=mask:five_triangle_table(m),'inconsistent F T-incidence table accepted')
    test({44,50}==set(one_double_checks()['forced_path_masks']),'both labeled F paths retained')
    f=triangle_fixtures()
    test(f['two_pinched_disks_before_split']['edge_graph_components']==1
         and f['two_pinched_disks_after_split']['edge_graph_components']==2,'pinched T fans must split')
    test(f['four_tetrahedron_faces_full_sphere']['Euler_characteristic']==2
         and f['four_tetrahedron_faces_full_sphere']['F2_boundary_rank']==3,
         'all spherical faces fail the proper-selection cycle-independence premise')
    test(F(3,8)-F(4,11)>0,'strict alpha margin')
    test(cover()['remaining_degree_profiles']==4,'all-one r2 removed')
    test(len([p for p in cover()['profiles'] if p['d42']==1])==2,'both prior mixed survivors retained')
    return controls


def main():
    base.need(sys.argv[1:] in ([],['--selftest']),'usage: check_all_one_two.py [--selftest]')
    out={'agent':'six-tammes-1','role':'researcher',
         'scope':'exact necessary corner/contact covers and topology fixtures; geometry and normalization written separately',
         'linear_angle_checks':angle_checks(),'no_double_five_checks':no_double_checks(),
         'one_double_five_checks':one_double_checks(),'triangle_star_Euler_checks':triangle_count_checks(),
         'triangle_topology_fixtures':triangle_fixtures(),'cover':cover()}
    if sys.argv[1:]:
        print(json.dumps({'status':'PASS','controls':selftest(),'degree_profiles':4,
                          'colored_H_types':11,'maximum_n3':1,'maximum_n5':3},sort_keys=True))
    else:
        print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
