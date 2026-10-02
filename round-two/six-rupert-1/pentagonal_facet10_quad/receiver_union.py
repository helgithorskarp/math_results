#!/usr/bin/env python3
"""Check the literal closed union with its strict partial-wall intersection.

The source classification on the old quadrilateral is an explicit cited
parent theorem. This module supplies only receiver-domain geometry.
"""
from pathlib import Path
import argparse,hashlib,json
import local as C
H=C.H
ROOT=Path(__file__).resolve().parents[3]
PARENT=ROOT/'round-two/six-rupert-1/pentagonal_facet40_quad'
HERE=Path(__file__).resolve().parent

def parent_image_exclusions(point,old,root):
    raw=(H.O,*point);excluded=[]
    group=H.M.group();H.require(len(group)==60,'all actual proper receiving-body images')
    for g in group:
        u=tuple(sum((H.K.coerce(H.V.Q(g[j][i].a,g[j][i].b))*raw[j]for j in range(3)),H.Z)for i in range(3))
        sign=H.sign(u[0],root)
        if sign==0:excluded.append(-1);continue
        sides=[]
        for a,b in zip(old,old[1:]+old[:1]):
            ds,dt=b[0]-a[0],b[1]-a[1]
            value=ds*u[2]-dt*u[1]+(dt*a[0]-ds*a[1])*u[0]
            sides.append(sign*H.sign(value,root))
        H.require(min(sides)<0,'new receiver lies outside every signed/projective parent body image')
        excluded.append(next(i for i,v in enumerate(sides)if v<0))
    return excluded

def compute(certificate,normals,root,parent):
    H.require(parent['closed_cell_indices']==[14,28,13,11,20],'entire cited five-cell closed parent union')
    old0=[tuple(C.decode(z)for z in p)for p in parent['exact_parent_quad']]
    old20=[tuple(C.decode(z)for z in p)for p in parent['exact_added_quad']]
    new=[tuple(C.decode(z)for z in p)for p in certificate['polygon']]
    H.require(all(len(p)==4 for p in (old0,old20,new)),'three whole closed quadrilaterals')
    checks=0
    for poly in (old0,old20,new):
        for i,(a,b)in enumerate(zip(poly,poly[1:]+poly[:1])):
            for j,c in enumerate(poly):
                if j not in(i,(i+1)%4):
                    H.require(H.sign(C.turn(a,b,c),root)>0,'strict globally convex cyclic ring');checks+=1
    evaluate=lambda facet,p:H.M.dot(tuple(certificate['facet_signs'][facet]*z for z in normals[facet]),(H.O,*p))
    H.require([H.sign(evaluate(10,p),root)for p in old20]==[-1,0,0,-1],'old20 opposite closed actual facet10 side')
    H.require([H.sign(evaluate(10,p),root)for p in new]==[1,1,0,0],'new full actual facet10 side')
    H.require(new[2]==old20[2]and new[3]==old20[1],'whole facet10 seam reversed literal endpoints')
    H.require([H.sign(evaluate(40,p),root)for p in old0]==[-1,0,0,-1],'old0 opposite closed actual facet40 side')
    H.require([H.sign(evaluate(40,p),root)for p in new]==[1,0,0,1],'new full actual facet40 side')
    H.require(new[1]==old0[2],'partial facet40 seam retains old vertex')
    a,b=old0[1],old0[2];d=H.M.sub(b,a);coordinate=next(j for j,z in enumerate(d)if z!=H.Z)
    z=(new[2][coordinate]-a[coordinate])/d[coordinate]
    H.require(new[2]==tuple(x+z*y for x,y in zip(a,d))and H.sign(z,root)>0 and H.sign(1-z,root)>0,'other facet40 endpoint strictly inside old side')
    barycenter=tuple(sum((p[j]for p in new),H.Z)/4 for j in range(2))
    H.require(H.sign(evaluate(10,barycenter),root)>0 and H.sign(evaluate(40,barycenter),root)>0,'strict raw union enlargement')
    exclusions=[parent_image_exclusions(barycenter,p,root)for p in (old0,old20)]
    return dict(agent='six-rupert-1',role='researcher',status='EXACT_CLOSED_FACET10_AND40_THREE_QUADRILATERAL_RECEIVER_UNION_PASSED',
        parent_cells=[14,28,13,11,20],closed_cell_indices=[14,28,13,11,20,34],
        exact_previous_quadrilaterals=[parent['exact_parent_quad'],parent['exact_added_quad']],exact_added_quad=certificate['polygon'],
        new_fan_triangle_indices=[[0,1,2],[0,2,3]],
        shared_segments=[dict(actual_facet=10,wall=13,parent_quad=1,parent_side_indices=[1,2],new_side_indices=[2,3],exact_segment=[certificate['polygon'][2],certificate['polygon'][3]]),
                         dict(actual_facet=40,wall=43,parent_quad=0,parent_side_indices=[1,2],new_side_indices=[1,2],exact_segment=[certificate['polygon'][1],certificate['polygon'][2]],strict_old_side_parameter=H.encode(z))],
        global_turn_checks=checks,exact_new_quad_barycenter=[H.encode(q)for q in barycenter],signed_parent_receiving_image_cases=120,
        new_barycenter_parent_image_rejection_side_indices=exclusions,
        parent_source_commit='4f89c33fb8e4828f97f4b68481e15a15db51faa4',parent_graph_cid='bafkreiexvt7tzreqsjsovespasoghudhedvtumsnoe7pp7evvkyqguu3za',
        scope='Omega=old four-cell quadrilateral UNION entire closed quad20 UNION entire closed quad34. Intersection with the parent is exactly the two adjacent closed facet10/40 segments. No convex hull or unknown adjacent19 claim.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'.generated/receiver_union.json');args=p.parse_args()
    cache=json.loads((HERE/'.generated/named_geometry.json').read_text())
    from fractions import Fraction as F
    root=H.V.I(*[F(q)for q in cache['root_interval']])
    cert=json.loads((HERE/'local_certificate.json').read_text())
    parent=json.loads((PARENT/'receiver_union.json').read_text())
    result=compute(cert,[tuple(C.decode(z)for z in n)for n in cache['outward_facet_normals']],root,parent)
    result['parent_receiver_union_sha256']=hashlib.sha256((PARENT/'receiver_union.json').read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],new_closed_cells=result['closed_cell_indices'],shared_actual_facets=[10,40])))
if __name__=='__main__':main()
