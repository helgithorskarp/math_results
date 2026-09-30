#!/usr/bin/env python3
"""Exact global projection-area bounds and an all-source receiver cap.

Python3.11+, standard library. All proof decisions use Q(sqrt(5))/Fraction.
The continuous area, frame/roll, and torque bridges are in global_area_proof.md.
"""
import argparse,json
from fractions import Fraction as F
from collections import deque
from verify import (Q5,S,PHI,ZERO,vec,vertices,dot,cross,sub,add,mul,
                    project,convex_hull_2d)
from orientation_certificate import (build_cells,check_reflections,CHAMBER,
                                     determinant)
from stable_certificate import projected_extremes,orbit,canonical_ray,WALLS
from stable_data import VERTEX_CERTIFICATES

CAP=F(1,20000000)
PROBE_MIX=F(1,1000)
MINIMUM_NODE=9
MAXIMUM_NODE=2
QMIN=(3503950+1491850*S)/31581
QSECOND=(236425+105595*S)/2178
QMAX=(350+150*S)/3
I=tuple(vec(int(i==j) for j in range(3)) for i in range(3))


def serial(v):return list(map(str,v))


def mm(A,B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(3)),ZERO)
                       for j in range(3)) for i in range(3))


def mv(A,v):return tuple(dot(row,v) for row in A)


def transpose(A):return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))


def reflection(w):
    return tuple(tuple(I[i][j]-2*w[i]*w[j]/dot(w,w)
                       for j in range(3)) for i in range(3))


def direct_area_sq(V,u):
    """Coordinate shoelace and its Euclidean Jacobian, allowing all ties."""
    e1=vec((-u[1],u[0],0)) if u[0]!=ZERO or u[1]!=ZERO else vec((1,0,0))
    e2=cross(u,e1)
    assert dot(e1,u)==ZERO and dot(e2,u)==ZERO and dot(e1,e2)==ZERO
    points=convex_hull_2d([(dot(v,e1),dot(v,e2)) for v in V])
    a=sum((points[j][0]*points[(j+1)%len(points)][1]
           -points[j][1]*points[(j+1)%len(points)][0]
           for j in range(len(points))),ZERO)/2
    assert a.sign()>0
    return a*a/(dot(e1,e1)*dot(e2,e2))


def root_gap_greater(big,small,d):
    """Exact positive-branch test for sqrt(big)-sqrt(small)>d>0."""
    assert d>0 and small.sign()>=0
    left=big-small-d*d
    assert left.sign()>0 and left*left>4*d*d*small


def check(rho=CAP,reverse_hull_cell=None,omit_hull_cell=None,
          drop_cell=None,claimed_minimum_node=MINIMUM_NODE):
    V=vertices();assert len(V)==62 and set(V)=={mul(-1,v) for v in V}
    # Each of the62 supplied points is an actual3D vertex; this is also
    # used when ruling out an additional body rotation from a failed permutation.
    radial=[dot(v,sub(v,w)) for j,v in enumerate(V) for k,w in enumerate(V) if j!=k]
    assert len(radial)==3782 and all(x.sign()>0 for x in radial)
    assert check_reflections(V)==3
    cells,_=build_cells()
    if drop_cell is not None:cells.pop(drop_cell)
    nodes=sorted(set(u for p in cells for u in p))
    assert len(cells)==12 and len(nodes)==14
    M=nodes[MINIMUM_NODE]
    assert M==vec(((3*S-5)/6,(S-1)/6,1))
    assert dot(M,M)==(28-8*S)/9
    assert nodes[MAXIMUM_NODE]==vec((0,PHI**-2,1))
    area_at={};C=[];reports=[]
    supports=turns_count=direct_checks=0
    for k,p in enumerate(cells):
        center=mul(Q5(F(1,len(p))),tuple(sum((u[j] for u in p),ZERO) for j in range(3)))
        hull=projected_extremes(V,center)
        if reverse_hull_cell==k:hull.reverse()
        if omit_hull_cell==k:hull.pop()
        for j,a in enumerate(hull):
            b=hull[(j+1)%len(hull)]
            edge=sub(V[b],V[a]);offsets=[]
            for u in p:
                normal=cross(edge,u)
                offsets.append(dot(normal,V[a]))
                assert all(dot(normal,sub(V[a],v)).sign()>=0 for v in V)
                supports+=len(V)
            assert all(x.sign()>=0 for x in offsets) and any(x.sign()>0 for x in offsets)
            before=sub(V[a],V[hull[(j-1)%len(hull)]])
            after=sub(V[b],V[a])
            turns=[dot(u,cross(before,after)) for u in p]
            assert all(x.sign()>=0 for x in turns) and any(x.sign()>0 for x in turns)
            turns_count+=len(turns)
        coeff=mul(Q5(F(1,2)),tuple(sum((cross(V[hull[j]],V[hull[(j+1)%len(hull)]])[r]
                                       for j in range(len(hull))),ZERO) for r in range(3)))
        C.append(coeff)
        assert dot(coeff,center).sign()>0
        assert dot(coeff,center)**2/dot(center,center)==direct_area_sq(V,center)
        direct_checks+=1
        for u in p:
            a=dot(coeff,u);assert a.sign()>0
            squared=a*a/dot(u,u)
            assert squared==direct_area_sq(V,u)
            direct_checks+=1
            if u in area_at:assert area_at[u]==squared
            area_at[u]=squared
        reports.append({'cell':k,'corner_indices':[nodes.index(u) for u in p],
                        'hull':hull,'area_vector':serial(coeff)})
    assert set(area_at)==set(nodes)
    best=min(area_at.values())
    assert best==QMIN and area_at[nodes[claimed_minimum_node]]==best
    assert [j for j,u in enumerate(nodes) if area_at[u]==best]==[MINIMUM_NODE]
    second=min(q for q in area_at.values() if q!=best)
    assert second==QSECOND
    root_gap_greater(second,best,F(1,100))
    grad_max=max(dot(c,c) for c in C)
    assert grad_max==QMAX and grad_max<Q5(256)
    assert area_at[nodes[MAXIMUM_NODE]]==grad_max
    maximum_cells=[j for j,c in enumerate(C) if dot(c,c)==grad_max]
    assert maximum_cells==[0]
    assert canonical_ray(C[0])==canonical_ray(nodes[MAXIMUM_NODE])
    assert QMAX<QMIN*F(507,500)**4

    # Global area coercivity: chamber chord radius2/5 about M, and
    # incident-cell corners within1/5. Squares are compared on positive dots.
    for u in CHAMBER:
        p=dot(M,u);assert p.sign()>0
        assert p*p>F(529,625)*dot(M,M)*dot(u,u)
    incident=[k for k,p in enumerate(cells) if M in p]
    assert incident==[4,7,9]
    for k in incident:
        for u in cells[k]:
            p=dot(M,u);assert p.sign()>0
            assert p*p>F(2401,2500)*dot(M,M)*dot(u,u)

    # Complete proper group from two products of the verified wall reflections.
    wall_matrices=[reflection(w) for w in WALLS]
    generators=[mm(wall_matrices[0],wall_matrices[1]),
                mm(wall_matrices[1],wall_matrices[2])]
    for g in generators:
        assert mm(g,transpose(g))==I and determinant(*g)==Q5(1)
        assert {mv(g,v) for v in V}==set(V)
    group={I};pending=deque([I])
    while pending:
        g=pending.popleft()
        for a in generators:
            h=mm(a,g)
            if h not in group:
                group.add(h);pending.append(h)
                assert len(group)<=120
    assert len(group)==60
    for g in group:
        assert transpose(g) in group
        assert {mv(g,v) for v in V}==set(V)
    minorbit={mv(g,M) for g in group}
    assert len(minorbit)==60 and mul(-1,M) in minorbit
    minaxes={canonical_ray(u) for u in minorbit}
    assert len(minaxes)==30 and minaxes==orbit(M)
    assert sum(mv(g,M)==M for g in group)==1
    maxorbit={mv(g,nodes[MAXIMUM_NODE]) for g in group}
    assert len(maxorbit)==20 and mul(-1,nodes[MAXIMUM_NODE]) in maxorbit
    threefold=mm(wall_matrices[0],wall_matrices[2])
    assert threefold in group and threefold!=I
    assert mm(mm(threefold,threefold),threefold)==I
    assert mv(threefold,nodes[MAXIMUM_NODE])==nodes[MAXIMUM_NODE]

    # All62 original projections, not just the silhouette's visible corners.
    projections=[project(v,M) for v in V]
    projected_radii=[dot(p,p) for p in projections]
    top=max(projected_radii);second_radius=max(x for x in projected_radii if x<top)
    top_indices=[j for j,x in enumerate(projected_radii) if x==top]
    assert top==(155+65*S)/58 and top>Q5(4)
    assert top_indices==[4,57] and projections[4]==mul(-1,projections[57])
    assert second_radius==Q5(5)
    root_gap_greater(top,second_radius,F(1,1000))
    minimal_hull=projected_extremes(V,M)
    assert len(minimal_hull)==16
    J=tuple(tuple(2*M[i]*M[j]/dot(M,M)-I[i][j] for j in range(3)) for i in range(3))
    assert mm(J,J)==I and determinant(*J)==Q5(1)
    assert {mv(J,v) for v in V}!=set(V)
    # Two maximal-radius points give exactly C2 planar rotations; together
    # with the area orbit and J's failed body permutation this proves G is full.
    sep=min(sum(((J[i][j]-g[i][j])**2 for i in range(3) for j in range(3)),ZERO)
            for g in group)
    assert sep.sign()>0 and sep>Q5(8*rho*rho)

    # Explicitly perturb the inherited four weak supports into strict supports.
    _,sign,contacts,chords=next(x for x in VERTEX_CERTIFICATES if x[0]==MINIMUM_NODE)
    assert sign==-1 and len(contacts)==len(chords)==4
    E=[];T=[];all_gaps=[];probe_reports=[]
    for (a,b,j),(c,d) in zip(contacts,chords):
        e=add(sub(V[b],V[a]),mul(Q5(PROBE_MIX),sub(V[d],V[c])))
        normal=cross(e,M)
        assert dot(e,e)<Q5(25)
        gaps=[dot(normal,sub(V[j],v)) for k,v in enumerate(V) if k!=j]
        assert all(x.sign()>0 for x in gaps)
        E.append(e);T.append(cross(V[j],normal));all_gaps.extend(gaps)
        probe_reports.append({'contact':[a,b,j],'exposing_chord':[c,d],
                              'mixed_edge':serial(e),'minimum_exposure_gap':str(min(gaps))})
    weights=[sign*((-1)**j)*determinant(*(T[k] for k in range(4) if k!=j)) for j in range(4)]
    assert all(w.sign()>0 for w in weights)
    assert tuple(sum((weights[j]*T[j][k] for j in range(4)),ZERO) for k in range(3))==vec((0,0,0))
    facet_distances=[]
    for omit in range(4):
        a,b,c=[T[j] for j in range(4) if j!=omit]
        normal=cross(sub(b,a),sub(c,a))
        assert dot(normal,normal).sign()>0
        squared=dot(normal,a)**2/dot(normal,normal)
        assert squared>Q5(F(81,2500))
        facet_distances.append(squared)
    exposure=min(all_gaps)
    assert exposure==(-11+5*S)/3600
    assert exposure-75*rho>Q5(F(1,25000))

    # Complete rational cap chain; no rounded transcendental comparisons.
    assert 0<rho<=F(1,100)
    assert max(dot(v,v) for v in V)<Q5(F(25,4))
    assert dot(M,M)<Q5(F(121,100))
    assert F(10,11)-rho>F(4,5)
    assert F(21,8)<3 and F(11,10)+3*rho<F(6,5)
    eta=1603*rho
    assert eta<F(1,1000) and 640*rho<1
    target=F(9,1000)-641*rho
    assert target>0 and eta<target*target
    torque_margin=F(9,50)-38*rho-F(15,2)*F(9,500)
    assert torque_margin>F(1,25)

    return {
        'agent':'six-rupert-1','role':'researcher',
        'status':'exact finite hypotheses for global area and all-source closed classification',
        'arithmetic':'Q(sqrt(5))/Fraction; standard Python3.11+',
        'global_Rupert_property':'unresolved',
        'whole_closed_cells':len(cells),'distinct_chamber_corners':len(nodes),
        'whole_cell_support_comparisons':supports,'whole_cell_turn_comparisons':turns_count,
        'shoelace_Jacobian_area_comparisons':direct_checks,
        'cell_certificates':reports,
        'corner_areas':[{'index':j,'ray':serial(u),'physical_area_squared':str(area_at[u])}
                        for j,u in enumerate(nodes)],
        'global_minimum_area_squared':str(best),'minimum_chamber_node':MINIMUM_NODE,
        'minimum_directed_orbit_size':len(minorbit),'minimum_unoriented_axes':len(minaxes),
        'second_corner_area_squared':str(second),'corner_area_gap_lower':'1/100',
        'global_maximum_area_squared':str(grad_max),'maximum_chamber_node':MAXIMUM_NODE,
        'maximum_directed_orbit_size':len(maxorbit),'maximum_unoriented_axes':len(maxorbit)//2,
        'maximum_gradient_cells':maximum_cells,'area_Lipschitz_upper':16,
        'global_pass_scale_bound':'lambda^4 <= qmax/qmin < (507/500)^4; strict for strict containment',
        'global_normal_distance_per_area_excess':40,
        'source_chord_per_receiver_chord':640,
        'proper_body_group_size':len(group),'proper_group_generators':[[serial(row) for row in g] for g in generators],
        'body_vertex_permutation_checks':len(group)*len(V),
        'all_3D_vertex_radial_exposure_comparisons':len(radial),
        'all_3D_vertex_radial_exposure_minimum':str(min(radial)),
        'minimal_shadow_hull':minimal_hull,'minimal_shadow_max_radius_vertex_indices':top_indices,
        'minimal_shadow_max_radius_squared':str(top),'minimal_shadow_second_radius_squared':str(second_radius),
        'minimal_shadow_rotation_group':'C2; identity and planar half-turn',
        'receiver_halfturn_is_body_symmetry':False,'receiver_halfturn_Frobenius_separation_squared':str(sep),
        'strict_probe_mix':str(PROBE_MIX),'strict_probes':probe_reports,
        'strict_probe_vertex_exposure_comparisons':len(all_gaps),'strict_probe_exposure_minimum':str(exposure),
        'torque_positive_cofactors':list(map(str,weights)),
        'torque_facet_squared_distances':list(map(str,facet_distances)),
        'torque_ball_radius_lower':'9/50',
        'receiver_cap_chord_radius':str(rho),'source_orientation_restriction':'none',
        'transport_shadow_error_upper':str(eta),'roll_chord_squared_upper':str(eta),
        'gauged_full_relative_angle_upper_radians':'9/500',
        'receiver_probe_exposure_margin':str(exposure-75*rho),
        'torque_remainder_margin':str(torque_margin),
        'closed_containment_classification':'lambda=1, t=0, Q in G union J_n G',
        'closed_relative_rotations_per_receiver':120,
        'strict_passages_in_receiver_caps':'excluded for every source orientation, roll, translation and scale>=1',
        'solver_or_floating_point_proof_decisions':0,
    }


def negative_tests():
    controls=[('incomplete cell cover',{'drop_cell':0}),
              ('reversed hull',{'reverse_hull_cell':0}),
              ('missing hull corner',{'omit_hull_cell':0}),
              ('false fivefold minimum',{'claimed_minimum_node':13}),
              ('unsupported cap1/1000000',{'rho':F(1,1000000)})]
    rejected=[]
    for name,args in controls:
        try:check(**args)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('malformed hypotheses accepted: '+name)
    return rejected


if __name__=='__main__':
    if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=check()
    if args.self_test:result['malformed_controls_rejected']=negative_tests()
    print(json.dumps(result,indent=2))
