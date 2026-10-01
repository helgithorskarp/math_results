#!/usr/bin/env python3
"""Exact six-contact certificate for the written minimum-neighborhood proof.

Python 3.11+, standard library only. Rational arithmetic in
Q(phi)[x]/(phi^2-phi-1, x^3-2*x-phi), positive real named root.
No floating-point or external LP solver is a proof dependency.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse
import copy
import hashlib
import json
import sys

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'pentagonal_area_spectrum'
PARENT_HASHES={
    'check.py':'64f847094441915167ce42601fe418d9332b39474bedf63f075c76cbfdccd534',
    'polygons.json':'9cf8972b021a148625d037adfe17c86d0ee45fd61811c0737d73ed71ceec79ec',
    'expected.json':'0368f8a13f76e5e3e745735dab9d0dd4df954c59c98a0f0e783359220c06cf9d',
}
for name,digest in PARENT_HASHES.items():
    if hashlib.sha256((PARENT/name).read_bytes()).hexdigest()!=digest:
        raise ValueError('area-spectrum dependency changed: '+name)
sys.path.insert(0,str(PARENT))
import check as A
M,V,Z=A.M,A.V,A.ZERO
ONE=M.K.coerce(1)
RHO=F(1,1000000)
THETA=F(1,10000)


def inverse(rows):
    n=len(rows)
    V.require(all(len(row)==n for row in rows),'inverse is not square')
    a=[list(row)+[M.K.coerce(int(i==j)) for j in range(n)]
       for i,row in enumerate(rows)]
    for i in range(n):
        at=next((j for j in range(i,n) if a[j][i]!=Z),None)
        V.require(at is not None,'contact rank is deficient')
        a[i],a[at]=a[at],a[i]
        pivot=a[i][i].inv()
        a[i]=[x*pivot for x in a[i]]
        for j in range(n):
            if j==i:
                continue
            s=a[j][i]
            a[j]=[x-s*y for x,y in zip(a[j],a[i])]
    out=[row[n:] for row in a]
    for i in range(n):
        for j in range(n):
            want=M.K.coerce(int(i==j))
            V.require(sum((rows[i][k]*out[k][j] for k in range(n)),Z)==want,
                      'right inverse product failed')
            V.require(sum((out[i][k]*rows[k][j] for k in range(n)),Z)==want,
                      'left inverse product failed')
    return out


def validate_input(data,cycle):
    V.require(type(data) is dict and set(data)=={'format','contacts'},
              'unexpected certificate fields')
    V.require(type(data['format']) is int and data['format']==1,'format version')
    rows=data['contacts']
    V.require(type(rows) is list and len(rows)==6,'exactly six contacts required')
    for row in rows:
        V.require(type(row) is dict and set(row)=={'edge','vertex'},'contact fields')
        i,j=row['edge'],row['vertex']
        V.require(type(i) is int and 0<=i<len(cycle),'edge index')
        V.require(type(j) is int and 0<=j<92,'vertex index')
        V.require(j in (cycle[i],cycle[(i+1)%len(cycle)]),'contact is not an endpoint')
    V.require(len({(r['edge'],r['vertex']) for r in rows})==6,'repeated contact')
    return rows


def contact_rows(rows,cycle,points,N,e,f,root):
    G=[]
    gaps=0
    edges={}
    for row in rows:
        at=row['edge']
        i,j=cycle[at],cycle[(at+1)%len(cycle)]
        d=M.sub(points[j],points[i])
        normal=M.cross(d,N)
        support=M.dot(normal,points[i])
        V.require(A.field_sign(support,root)>0,'outward support not positive')
        V.require(A.field_sign(M.dot(d,d),root)>0,'zero original edge')
        V.require(A.field_sign(ONE-M.dot(d,d),root)>0,'edge length not below one')
        for k,p in enumerate(points):
            gap=support-M.dot(normal,p)
            if k in (i,j):
                V.require(gap==Z,'endpoint is off the supporting plane')
            else:
                V.require(A.field_sign(gap-F(1,2000),root)>0,
                          'receiver support is not strict by 1/2000')
                gaps+=1
        edges[at]=(i,j)
        G.append(list(M.cross(points[row['vertex']],normal))+
                 [M.dot(normal,e),M.dot(normal,f)])
    return G,edges,gaps


def audit(data,geometry):
    root,scale,mats,points,areas=geometry
    cycle=json.loads((PARENT/'polygons.json').read_text())['minimum']['ccw_literal_vertex_indices']
    rows=validate_input(data,cycle)
    raw=M.cross(areas[0],areas[58])
    V.require(A.field_sign(raw[0],root)>0,'normal chart sign')
    N=tuple(c/raw[0] for c in raw)
    V.require(N[0]==ONE,'normal chart normalization')
    e=(N[1],-N[0],Z)
    f=M.cross(N,e)
    V.require(M.dot(N,e)==Z and M.dot(N,f)==Z and M.dot(e,f)==Z,
              'fixed translation frame is not orthogonal')
    for label,vector in (('N',N),('e',e),('f',f)):
        norm2=M.dot(vector,vector)
        V.require(A.field_sign(norm2,root)>0,'zero frame vector: '+label)
        V.require(A.field_sign(4-norm2,root)>0,'frame norm not below two: '+label)
    for point in points:
        V.require(A.field_sign(4-M.dot(point,point),root)>0,'body radius not below two')
    # Replay the exact parent silhouette support/turn checks. Global extremizer
    # classification and equality rigidity remain published prerequisites.
    parent_polygon=A.audit_polygon(points,raw,cycle,root)[0]
    G,edges,gaps=contact_rows(rows,cycle,points,N,e,f,root)
    H=inverse(G[:5])
    unnormalized=[-sum((G[5][k]*H[k][i] for k in range(5)),Z)
                  for i in range(5)]+[ONE]
    total=sum(unnormalized,Z)
    V.require(A.field_sign(total,root)>0,'weight sum is not positive')
    weights=[w/total for w in unnormalized]
    for w in weights:
        V.require(A.field_sign(w-F(3,40),root)>0,'weight is not above 3/40')
    V.require(sum(weights,Z)==ONE,'weights do not sum to one')
    for k in range(5):
        V.require(sum((w*g[k] for w,g in zip(weights,G)),Z)==Z,
                  'translation/torque balance failed')
    for row in H:
        bound=F(0)
        for entry in row:
            interval=entry.interval(root)
            bound+=max(abs(interval.lo),abs(interval.hi))
        V.require(bound<101,'inverse row norm not below 101')
    V.require(F(101)*F(37,3)<1250,'positive-span constant')
    support_margin=F(1,2000)-8*RHO
    span_margin=F(1,1250)-20*RHO
    rotation_margin=span_margin/2-2*THETA
    V.require(support_margin==F(123,250000)>0,'support perturbation margin')
    V.require(span_margin==F(39,50000)>0,'row perturbation margin')
    V.require(rotation_margin==F(19,100000)>0,'finite rotation remainder margin')
    out={
        'agent':'six-rupert-1','role':'researcher',
        'status':'COMPLETE_EXACT_FINITE_PREMISES_UNFORMALIZED_BRIDGES',
        'coefficient_domain':'Q(phi)[x]/(phi^2-phi-1,x^3-2*x-phi), positive named root',
        'contact_rows':6,'persistent_original_edges':len(edges),
        'persistent_edge_indices':sorted(edges),
        'nonendpoint_support_checks_including_repeated_edge':gaps,
        'distinct_nonendpoint_support_checks':90*len(edges),
        'body_radius_checks':92,'inverse_product_checks':50,
        'exact_balanced_coordinates':5,'weight_lower_bound':'3/40',
        'inverse_infinity_norm_upper_bound':'101',
        'positive_span_lower_constant':'1/1250',
        'local_receiver_chord':str(RHO),'local_relative_rotation_angle':str(THETA),
        'support_perturbation_margin':str(support_margin),
        'span_perturbation_margin':str(span_margin),
        'finite_rotation_margin':str(rotation_margin),
        'all_source_receiving_collar_radius':'EXISTS_POSITIVE_UNQUANTIFIED',
        'minimum_projective_receiving_axes':30,
        'full_rupert_status':'OPEN',
        'parent_polygon_audit':parent_polygon,
        'parent_sha256':PARENT_HASHES,
    }
    return out


def negative_controls(original,geometry):
    cycle=json.loads((PARENT/'polygons.json').read_text())['minimum']['ccw_literal_vertex_indices']
    bad=[]
    a=copy.deepcopy(original);a['contacts'][0]['vertex']=True;bad.append(('boolean_vertex',a))
    a=copy.deepcopy(original);a['contacts'][0]['vertex']=0;bad.append(('noncontact_vertex',a))
    a=copy.deepcopy(original);a['contacts'][5]=dict(a['contacts'][0]);bad.append(('repeated_contact',a))
    a=copy.deepcopy(original);a['contacts'].pop();bad.append(('missing_contact',a))
    a=copy.deepcopy(original);a['contacts'][5]={'edge':2,'vertex':cycle[2]};bad.append(('collapsed_facet_contact',a))
    rejected=[]
    for label,data in bad:
        try:
            audit(data,geometry)
        except (ValueError,ZeroDivisionError):
            rejected.append(label)
        else:
            raise ValueError('damaged control was accepted: '+label)
    return rejected


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--negative-controls',action='store_true')
    parser.add_argument('--discovery',action='store_true',
                        help='author fixture generation only; mathematical gates still run')
    args=parser.parse_args()
    data=json.loads((HERE/'certificate.json').read_text())
    geometry=A.build_geometry()
    out=audit(data,geometry)
    if not args.discovery:
        V.require(out==json.loads((HERE/'expected.json').read_text()),'expected record changed')
    if args.negative_controls:
        out=dict(out,negative_controls_rejected=negative_controls(data,geometry))
    if args.emit:
        print(json.dumps(out,sort_keys=True,indent=2))
    else:
        print('PASS: six positive spanning contacts; local box and qualitative all-source collar premises.')


if __name__=='__main__':
    main()
