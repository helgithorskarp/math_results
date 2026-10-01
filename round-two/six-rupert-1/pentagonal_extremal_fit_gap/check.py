#!/usr/bin/env python3
"""Exact balanced-edge certificate and quantified global passage gap.

Standard library only. Every sign is exact algebra or a strict outward
rational interval gate. An unfinished computation establishes no claim.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'pentagonal_area_spectrum'
HASHES={
    'check.py':'64f847094441915167ce42601fe418d9332b39474bedf63f075c76cbfdccd534',
    'polygons.json':'9cf8972b021a148625d037adfe17c86d0ee45fd61811c0737d73ed71ceec79ec',
    'expected.json':'0368f8a13f76e5e3e745735dab9d0dd4df954c59c98a0f0e783359220c06cf9d',
}
for name,digest in HASHES.items():
    if hashlib.sha256((PARENT/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('parent source changed: '+name)
spec=importlib.util.spec_from_file_location('pentagonal_area_parent',PARENT/'check.py')
A=importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)
M,V=A.M,A.V
ZERO=M.K()
I=V.I
RHO=F(1,500)
KAPPA=1-RHO*RHO/2
DUAL_RADIUS=F(201,200)
TRANSPORT=F(11,10)
DECREMENT=F(1,10**6)


def det(a,b):return a[0]*b[1]-a[1]*b[0]
def idot(a,b):return sum((x*y for x,y in zip(a,b)),I(0,0))
def isub(a,b):return tuple(x-y for x,y in zip(a,b))


def frames(root,points,areas,poly):
    v=M.cross(areas[0],areas[58])
    q=tuple(M.K.coerce(x) for x in (V.ONE,-V.PHI,-V.ONE/V.PHI))
    es=(v[1],-v[0],ZERO)
    fs=M.cross(v,es)
    B=M.dot(es,es)
    T=M.dot(v,v)
    V.require(A.field_sign(B,root)>0 and A.field_sign(T,root)>0 and
              M.dot(v,es)==ZERO and M.dot(es,fs)==ZERO and
              M.dot(fs,fs)==B*T,'source orthogonal frame failed')
    er=tuple(M.K.coerce(x) for x in (V.PHI,V.ONE,V.Z))
    fr=tuple(M.K.coerce(x) for x in (V.ONE/(2*V.PHI),-V.ONE/2,V.H/2))
    h=M.K.coerce(V.H)
    V.require(M.dot(er,er)==M.dot(fr,fr)==h and M.dot(er,fr)==ZERO and
              M.dot(er,q)==M.dot(fr,q)==ZERO and
              M.cross(q,er)==tuple(2*x for x in fr),'receiver orthogonal frame failed')
    source=[(M.dot(es,p),M.dot(fs,p)) for p in points]
    coords=[(M.dot(er,p),M.dot(fr,p)) for p in points]
    cycle=poly['maximum']['ccw_literal_vertex_indices']
    normals=[]
    rhs=[]
    for i,j in zip(cycle,cycle[1:]+cycle[:1]):
        n=(coords[j][1]-coords[i][1],coords[i][0]-coords[j][0])
        r=M.dot(n,coords[i])
        V.require(A.field_sign(r,root)>0,'receiver offset is nonpositive')
        normals.append(n);rhs.append(r)
    phi=M.K.coerce(V.PHI);x=M.X
    a=((14*phi-27)*x.square()+(10*phi-6)*x+32-12*phi)*F(1,31)
    radius2=a.square()*h
    for p in points:
        V.require(A.field_sign(radius2-M.dot(p,p),root)>=0,'original body leaves radius ball')
    return source,normals,rhs,V.qi(V.H).sqrt()/B.interval(root).sqrt(),T.interval(root).sqrt(),(a*h).interval(root)


def row_point(row,root,source,normals,rhs,factor,sqrtT,scaled_radius):
    V.require(isinstance(row,dict) and set(row)=={'receiving_edges','source_vertices'},'dual row grammar')
    edges,vertices=row['receiving_edges'],row['source_vertices']
    V.require(isinstance(edges,list) and len(edges) in (2,3) and len(set(edges))==len(edges) and
              all(type(i) is int and 0<=i<20 for i in edges) and
              isinstance(vertices,list) and len(vertices)==len(edges) and
              all(type(i) is int and 0<=i<92 for i in vertices),'dual indices invalid')
    ns=[normals[i] for i in edges]
    if len(ns)==2:
        V.require(all(x+y==ZERO for x,y in zip(*ns)),'pair normals are not exact opposites')
        weights=[M.K.coerce(1),M.K.coerce(1)]
    else:
        weights=[det(ns[1],ns[2]),det(ns[2],ns[0]),det(ns[0],ns[1])]
        signs=[A.field_sign(w,root) for w in weights]
        V.require(signs==[1,1,1] or signs==[-1,-1,-1],'triple weights are not strictly balanced positive')
        if signs[0]<0:weights=[-w for w in weights]
    V.require(all(sum((w*n[k] for w,n in zip(weights,ns)),ZERO)==ZERO for k in range(2)),
              'weights do not cancel arbitrary translation')
    denominator=sum((w*rhs[i] for w,i in zip(weights,edges)),ZERO)
    den=denominator.interval(root)
    V.require(den.lo>0,'dual normalization is not positive')
    c0=c1=d0=d1=ZERO
    length_sum=I(0,0)
    for w,n,j in zip(weights,ns,vertices):
        u,z=source[j]
        c0+=w*n[0]*u;c1+=w*n[1]*z
        d0+=w*n[1]*u;d1-=w*n[0]*z
        length_sum+=w.interval(root)*M.dot(n,n).interval(root).sqrt()
    point=(factor*(c0.interval(root)+c1.interval(root)/sqrtT)/den,
           factor*(d0.interval(root)+d1.interval(root)/sqrtT)/den)
    constant=scaled_radius*length_sum/den
    V.require(constant.lo>0 and constant.hi<TRANSPORT,'dual tilt transport bound failed')
    return point,constant


def circle_check(points):
    V.require(len(points)>=3,'dual polygon is too small')
    count=0
    for i,a in enumerate(points):
        b=points[(i+1)%len(points)]
        edge=isub(b,a)
        length2=idot(edge,edge)
        offset=det(a,b)
        V.require(length2.lo>0 and offset.lo>0,'dual edge/origin degeneracy')
        V.require((offset.square()-DUAL_RADIUS**2*length2).lo>0,'dual polygon fails its disk radius')
        V.require(det(isub(a,points[i-1]),edge).lo>0,'dual polygon turn is not strictly counterclockwise')
        probe=(edge[1],-edge[0])
        for j,c in enumerate(points):
            if j in (i,(i+1)%len(points)):continue
            V.require(idot(probe,isub(a,c)).lo>0,'dual polygon convex support failed')
            count+=1
    return count


def certificate_check(data,root,frame_data):
    V.require(isinstance(data,dict) and set(data)=={'source_facet_pair','receiving_axis','receiving_cycle_source','dual_polygon_rows'} and
              data['source_facet_pair']==[0,58] and data['receiving_axis']==['1','-phi','-1/phi'] and
              data['receiving_cycle_source']=='../pentagonal_area_spectrum/polygons.json',
              'certificate scope changed')
    rows=data['dual_polygon_rows']
    V.require(isinstance(rows,list) and len(rows)==38,'dual polygon row count changed')
    points=[];bounds=[]
    for row in rows:
        p,c=row_point(row,root,*frame_data)
        points.append(p);bounds.append(c)
    count=circle_check(points)
    V.require(DUAL_RADIUS-1-2*TRANSPORT*RHO==F(3,5000),'pair cap scalar margin changed')
    return points,{'balanced_dual_rows':len(rows),
                   'pair_rows':sum(len(r['receiving_edges'])==2 for r in rows),
                   'triple_rows':sum(len(r['receiving_edges'])==3 for r in rows),
                   'dual_circle_strict_support_checks':count,
                   'dual_circle_disk_edge_gates':len(rows),
                   'dual_circle_strict_turns':len(rows),
                   'disk_radius':str(DUAL_RADIUS),'tilt_transport_bound':str(TRANSPORT),
                   'source_and_receiver_chord_cap':str(RHO),
                   'pair_exclusion_margin':str(DUAL_RADIUS-1-2*TRANSPORT*RHO),
                   'frozen_scale_ceiling':str(1/DUAL_RADIUS)}


def global_gates(root,charts):
    minimum=charts[57]
    maximum=next(c for c in charts[37]['corners'] if c['choices']==(1,-1))
    minimum_count=maximum_count=tied_count=0
    for chart in charts:
        if chart['index']!=58:
            margin=KAPPA*KAPPA*chart['support2']*minimum['norm2']-minimum['support2']*chart['norm2']
            V.require(A.field_sign(margin,root)>0,'nonminimum facet does not clear localization sphere')
            minimum_count+=1
        for corner in chart['corners']:
            difference=maximum['norm2']-corner['norm2']
            if difference==ZERO:tied_count+=1
            else:
                V.require(A.field_sign(KAPPA*KAPPA*maximum['norm2']-corner['norm2'],root)>0,
                          'nonmaximum cube image does not clear localization threshold')
                maximum_count+=1
    m=minimum['support'].interval(root)/minimum['norm2'].interval(root).sqrt()
    big=maximum['norm2'].interval(root).sqrt()
    upper=(big/m).sqrt()
    ceiling=upper-DECREMENT
    V.require(ceiling.lo>1,'global ceiling is not above the identity scale')
    source_margin=m/KAPPA-big/ceiling.square()
    receiver_margin=ceiling.square()*m-KAPPA*big
    V.require(source_margin.lo>F(1,20000000) and receiver_margin.lo>F(1,20000000),
              'global scale does not force both extremal neighborhoods with the stated margin')
    decimal=F(1012389033,10**9)
    V.require(ceiling.hi<decimal,'advertised global decimal upper bound failed')
    return {'nonminimum_chart_localization_gates':minimum_count,
            'nonmaximum_cube_image_localization_gates':maximum_count,
            'maximum_cube_image_ties':tied_count,
            'radial_localization_cosine':str(KAPPA),
            'exact_area_ratio_decrement':str(DECREMENT),
            'source_area_localization_margin_exceeds':'1/20000000',
            'receiver_area_localization_margin_exceeds':'1/20000000',
            'global_passage_scale_decimal_ceiling':str(decimal)}


def negative_controls(root,frame_data,rows,points):
    cases=[]
    bad={'receiving_edges':[3,14],'source_vertices':[15,12]}
    cases.append(('unbalanced_translation_pair',lambda:row_point(bad,root,*frame_data)))
    bad_boolean=json.loads(json.dumps(rows[0]));bad_boolean['source_vertices'][0]=True
    cases.append(('boolean_source_index',lambda:row_point(bad_boolean,root,*frame_data)))
    cases.append(('reversed_dual_boundary',lambda:circle_check(list(reversed(points)))))
    cases.append(('missing_essential_dual_point',lambda:circle_check(points[1:])))
    rejected=[]
    for name,run in cases:
        try:run()
        except ValueError:rejected.append(name)
        else:raise ValueError('damaged certificate accepted: '+name)
    print(json.dumps({'negative_controls_rejected':rejected},sort_keys=True),file=sys.stderr)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--negative-controls',action='store_true')
    parser.add_argument('--discovery',action='store_true',help='skip expected fixture comparison during author derivation only')
    args=parser.parse_args()
    root,scale,mats,points,areas=A.build_geometry()
    poly=json.loads((PARENT/'polygons.json').read_text())
    charts=A.enumerate_charts(areas,root)
    parent_expected=json.loads((PARENT/'expected.json').read_text())
    inherited=A.audit_extrema(root,scale,mats,areas,A.permutation_group(areas),charts)
    inherited.update(A.audit_polygons(root,points,areas,charts,poly))
    V.require(all(parent_expected[k]==value for k,value in inherited.items()),'parent finite premise mismatch')
    frame_data=frames(root,points,areas,poly)
    data=json.loads((HERE/'certificate.json').read_text())
    dual_points,out=certificate_check(data,root,frame_data)
    out.update(global_gates(root,charts))
    out.update({'agent':'six-rupert-1','role':'researcher','full_rupert_problem':'OPEN',
                'proof_status':'author-checked finite premises for PROOF.md; unformalized and independently unreviewed',
                'floating_point_proof_decisions':0,'parent_sha256':HASHES,
                'parent_regenerated_extremum_and_polygon_record_fields':len(inherited),
                'original_vertices_rechecked_in_radius_ball':92,
                'all_rolls_and_actual_translations':'retained via positive exactly balanced original-edge weights',
                'closed_scale_at_least_one_extremal_pair_caps':'EXCLUDED',
                'nieuwland_supremum':'strictly below sqrt(Amax/Amin)-1/1000000'})
    if not args.discovery:
        V.require(out==json.loads((HERE/'expected.json').read_text()),'complete output differs from expected.json')
    if args.negative_controls:negative_controls(root,frame_data,data['dual_polygon_rows'],dual_points)
    if args.emit or args.discovery:print(json.dumps(out,indent=2,sort_keys=True))
    else:print('PASS: all-roll extremal-pair caps and quantified global Nieuwland gap; full Rupert OPEN')


if __name__=='__main__':main()
