#!/usr/bin/env python3
"""Exact singleton/area obstruction near the twofold projection.

Standard Python 3.11+, Q(sqrt(5)) arithmetic. No solver or floating inputs.
The scalar comparison and geometric bridges are in twofold_area_proof.md.
"""
from fractions import Fraction as F
import argparse,json
from verify import (Q5,PHI,S,ZERO,vec,vertices,add,sub,mul,dot,cross,
                    convex_hull_2d)
from orientation_certificate import build_cells,clip,CORNER

ETA=F(1,100)
CAP=F(1,200)
SMALL_TRIANGLE_RADIUS=F(1,10)


def serial(v):
    return list(map(str,v))


def hull_classes(V,u):
    e1=vec((-u[1],u[0],0)) if u[0]!=ZERO or u[1]!=ZERO else vec((1,0,0))
    e2=cross(u,e1)
    mapping={}
    for j,v in enumerate(V):
        mapping.setdefault((dot(v,e1),dot(v,e2)),[]).append(j)
    return [mapping[p] for p in convex_hull_2d(mapping)]


def inside_polygon(u,p):
    for i,a in enumerate(p):
        b=p[(i+1)%len(p)]
        turn=(b[0]-a[0])*(u[1]-a[1])-(b[1]-a[1])*(u[0]-a[0])
        assert turn.sign()>=0


def check(eta=ETA,reverse_hull_cell=None,omit_hull_cell=None):
    V=vertices()
    assert len(V)==62
    assert set(V)=={vec((-v[0],v[1],v[2])) for v in V}
    assert set(V)=={vec((v[0],-v[1],v[2])) for v in V}
    assert set(V)=={vec((v[0],v[1],-v[2])) for v in V}
    Hc=hull_classes(V,CORNER)
    assert len(Hc)==12 and all(len(c)==1 for c in Hc)
    H=[c[0] for c in Hc]
    assert all(V[j][2]==ZERO for j in H)
    large_x,large_y=(5+3*S)/6,(5+S)/6
    small_x,small_y=(15+S)/22,(25+9*S)/22
    assert large_x/large_y==PHI
    assert small_y/small_x==PHI**2
    expected={vec((sign*S,0,0)) for sign in (-1,1)}
    expected|={vec((0,sign*S,0)) for sign in (-1,1)}
    for x,y in [(large_x,large_y),(small_x,small_y)]:
        expected|={vec((sx*x,sy*y,0)) for sx in (-1,1) for sy in (-1,1)}
    assert {V[j] for j in H}==expected

    R2=max(dot(v,v) for v in V)
    assert R2==(25+10*S)/9
    radial_gaps=[]
    radial_comparisons=0
    for j in H:
        gaps=[dot(V[j],sub(V[j],v)) for k,v in enumerate(V) if k!=j]
        assert all(g.sign()>0 for g in gaps)
        radial_comparisons+=len(gaps)
        radial_gaps.append({'vertex':j,'minimum_gap':str(min(gaps))})
    radial_min=min(dot(V[j],sub(V[j],v)) for j in H for k,v in enumerate(V) if k!=j)
    assert radial_min==(135-35*S)/242
    exposure_error=R2*(4*eta+2*eta**2)
    assert radial_min>exposure_error

    polygons,_=build_cells()
    incident=[k for k,p in enumerate(polygons) if CORNER in p]
    assert incident==[1,5]
    area_coefficients={}
    support_comparisons=0
    turn_comparisons=0
    cell_reports=[]
    for k in incident:
        p=polygons[k]
        u=mul(Q5(1)/len(p),tuple(sum((q[i] for q in p),ZERO) for i in range(3)))
        hc=hull_classes(V,u)
        assert all(len(c)==1 for c in hc)
        h=[c[0] for c in hc]
        assert len(h)==16
        if reverse_hull_cell==k:h.reverse()
        if omit_hull_cell==k:h.pop()
        for i,a in enumerate(h):
            b=h[(i+1)%len(h)]
            e=sub(V[b],V[a])
            offsets=[]
            for q in p:
                n=cross(e,q)
                offsets.append(dot(n,V[a]))
                assert all(dot(n,sub(V[a],v)).sign()>=0 for v in V)
                support_comparisons+=len(V)
            assert all(x.sign()>=0 for x in offsets) and any(x.sign()>0 for x in offsets)
            before=sub(V[a],V[h[(i-1)%len(h)]])
            after=sub(V[b],V[a])
            turns=[dot(q,cross(before,after)) for q in p]
            assert all(x.sign()>=0 for x in turns) and any(x.sign()>0 for x in turns)
            turn_comparisons+=len(turns)
        area=mul(Q5(F(1,2)),tuple(sum((cross(V[h[i]],V[h[(i+1)%len(h)]])[j]
                                      for i in range(len(h))),ZERO) for j in range(3)))
        area_coefficients[k]=area
        cell_reports.append({'cell':k,'polygon':[serial(q) for q in p],
                             'hull':h,'oriented_area_coefficient':serial(area)})
    C0=area_coefficients[1][2]
    Cx=area_coefficients[5][0]
    c=(5-S)/2
    assert c==3-PHI
    assert area_coefficients[1]==vec((0,c*Cx,C0))
    assert area_coefficients[5]==vec((Cx,0,C0))
    assert C0==(160+150*S)/33 and Cx==(5+15*S)/33
    assert C0.sign()>0 and Cx.sign()>0

    # Whole-triangle cover for the area formula, including all its boundaries.
    rho=SMALL_TRIANGLE_RADIUS
    T=[CORNER,vec((rho,0,1)),vec((0,rho,1))]
    divider=vec((1,-c,0))
    triangle_corners=[]
    for k,side in [(1,-1),(5,1)]:
        clipped=clip(T,divider,side)
        for q in clipped:inside_polygon(q,polygons[k])
        triangle_corners.append({'cell':k,'corners':[serial(q) for q in clipped]})

    # Four-case scalar lemma uses only these exact coefficient comparisons.
    q=1/PHI**2
    assert PHI>1/c and PHI**2>c
    assert PHI**2<Q5(3)
    assert (PHI**2+1)/c==PHI**2
    assert 1-c*q>ZERO and c-1/PHI>ZERO
    assert 3*(1-c*q)>1+q
    assert 3*(c-1/PHI)>1+1/PHI
    assert 1-2*eta>0 and 1-eta**2>F(1,4)
    assert 4*eta<=rho
    area_margin=Cx-6*eta*C0
    assert area_margin.sign()>0
    if eta==ETA:
        assert 2*CAP==eta
        assert area_margin==(-23+30*S)/165

    return {
        'agent':'six-rupert-1','role':'researcher',
        'status':'exact hypotheses for a twofold singleton/area strict obstruction',
        'orthonormal_frame_operator_radius':str(eta),
        'receiver_cap_chord_radius':str(CAP),
        'full_relative_angle_cap_radians':str(CAP),
        'A_extreme_vertex_indices':H,
        'singleton_radial_exposure_comparisons':radial_comparisons,
        'radial_exposure_minimum':str(radial_min),
        'frame_support_error_bound':str(exposure_error),
        'strict_exposure_margin':str(radial_min-exposure_error),
        'per_vertex_radial_gaps':radial_gaps,
        'incident_cell_certificates':cell_reports,
        'whole_polygon_support_comparisons':support_comparisons,
        'whole_polygon_turn_comparisons':turn_comparisons,
        'small_triangle_cover':triangle_corners,
        'unit_normal_area_formula':'C0*z+Cx*max(|x|,c*|y|)',
        'area_constants':{'C0':str(C0),'Cx':str(Cx),'c':str(c)},
        'scalar_increment_bound':'dx+dy < 3*(M1-M2)',
        'strict_area_comparison_margin':str(area_margin),
        'geometric_consequence':'explicit strict caps at all 15 twofold axes',
        'combined_consequence':'with prior stable/E caps, some uniform positive strict full-relative-angle gap exists for every receiver',
        'numerical_global_angle_gap_computed':False,
        'global_Rupert_property':'unresolved',
        'solver_or_floating_point_decisions':0,
    }


if __name__=='__main__':
    if not __debug__:raise RuntimeError('verification requires assertions; do not use python -O')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    result=check()
    if args.self_test:
        controls=[('unsupported frame radius1/50',{'eta':F(1,50)}),
                  ('reversed hull',{'reverse_hull_cell':1}),
                  ('missing hull corner',{'omit_hull_cell':5})]
        rejected=[]
        for name,kwargs in controls:
            try:check(**kwargs)
            except AssertionError:rejected.append(name)
            else:raise RuntimeError('malformed control accepted: '+name)
        result['malformed_controls_rejected']=rejected
    print(json.dumps(result,indent=2))
