#!/usr/bin/env python3
"""Exact closed clipping joins triangle11 to the published three-cell domain."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import local as C
H=C.H
ROOT=Path(__file__).resolve().parents[3]
PARENT=ROOT/'round-two/six-rupert-1/pentagonal_chamber_boundary_cell'

def clip(polygon,wall,root,side):
    result=[]
    def add(p):
        if not result or result[-1]!=p:result.append(p)
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        fa=side*(wall[0]+wall[1]*a[0]+wall[2]*a[1]);fb=side*(wall[0]+wall[1]*b[0]+wall[2]*b[1])
        sa,sb=H.sign(fa,root),H.sign(fb,root)
        if sa*sb<0:
            z=fa/(fa-fb);add(tuple(x+z*(y-x)for x,y in zip(a,b)))
        if sb>=0:add(b)
    if len(result)>1 and result[0]==result[-1]:result.pop()
    return result

def cyclic_equal(a,b):
    return len(a)==len(b)and any(a==b[k:]+b[:k]for k in range(len(b)))

def compute(cert,normals,root,parent_joined):
    old_quad=parent_joined['exact_quad'];encoded_zero=[H.encode(H.Z),H.encode(H.Z)]
    quad=[encoded_zero,old_quad[1],old_quad[2],old_quad[3]]
    p=[tuple(C.decode(z)for z in v)for v in quad];old=[tuple(C.decode(z)for z in v)for v in old_quad]
    triangle=[tuple(C.decode(z)for z in v)for v in cert['polygon']]
    H.require(triangle[0]==(H.Z,H.Z)and triangle[1]==old[0]and triangle[2]==old[3],'principal axis and both literal old facet42 seam endpoints')
    constraints=[(H.Z,H.O,H.Z),(H.Z,H.Z,H.O),(H.O,-H.phi,-H.phi*H.phi)]
    constraints +=[tuple(s*z for z in n)for s,n in zip(cert['facet_signs'],normals)]
    omitted=(13,45,55);comparisons=0;turns=0;walls=[]
    for v in p:
        for j,n in enumerate(constraints):
            if j not in omitted:
                H.require(H.sign(n[0]+n[1]*v[0]+n[2]*v[1],root)>=0,'all60 retained actual receiving halfspaces hold at every proposed corner');comparisons+=1
    for i,(a,b)in enumerate(zip(p,p[1:]+p[:1])):
        for j,c in enumerate(p):
            if j not in(i,(i+1)%4):H.require(H.sign(C.turn(a,b,c),root)>0,'every other corner lies strictly left of every whole-quad side');turns+=1
        walls.append([j for j,n in enumerate(constraints)if j not in omitted and n[0]+n[1]*a[0]+n[2]*a[1]==H.Z and n[0]+n[1]*b[0]+n[2]*b[1]==H.Z])
    H.require(walls==[[1],[43],[50],[0]],'all four genuine principal-axis quadrilateral side walls')
    positive=clip(p,constraints[45],root,1);negative=clip(p,constraints[45],root,-1)
    H.require(cyclic_equal(positive,triangle),'entire positive closed facet42 clip is exactly triangle11')
    H.require(cyclic_equal(negative,old),'entire negative closed facet42 clip is exactly the published three-cell quadrilateral')
    H.require(H.sign(constraints[45][0],root)>0,'new principal-axis corner is strictly outside the old receiving domain')
    area=sum((a[0]*b[1]-a[1]*b[0]for a,b in zip(p,p[1:]+p[:1])),H.Z)/2
    return dict(agent='six-rupert-1',role='researcher',status='EXACT_PRINCIPAL_AXIS_JOINED_FOUR_CELL_CLOSED_RECEIVER_QUADRILATERAL_PASSED',
                exact_quad=quad,exact_raw_chart_area=H.encode(area),actual_wall_indices=walls,halfspace_corner_checks=comparisons,global_turn_checks=turns,
                omitted_wall_constraints=list(omitted),omitted_actual_facets=[10,42,52],closed_cell_indices=[14,28,13,11],
                closed_positive_clip=cert['polygon'],closed_negative_clip=old_quad,shared_actual_facet=42,shared_wall=45,
                parent_source_commit='827f71f46694c8e9b71643819fbe41d209e18357',parent_graph_cid='bafkreighn4d3z4hjabqiagrec4s5gwst62frexvs6fbcxfdyrfr65qnaoa',
                scope='Receiver union geometry only. New all-source classification requires the complete triangle11 local and outer-source certificates; the old three-cell part is the cited published lemma.')

def main():
    cache=json.loads((Path(__file__).resolve().parent/'.generated/named_geometry.json').read_text());root=H.V.I(*[F(q)for q in cache['root_interval']])
    cert=json.loads((Path(__file__).resolve().parent/'local_certificate.json').read_text());normals=[tuple(C.decode(z)for z in v)for v in cache['outward_facet_normals']]
    parent_path=PARENT/'joined_receiver.json';parent=json.loads(parent_path.read_text());record=compute(cert,normals,root,parent)
    record['parent_joined_receiver_sha256']=hashlib.sha256(parent_path.read_bytes()).hexdigest()
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode();(Path(__file__).resolve().parent/'.generated/joined.json').write_bytes(raw)
    print(json.dumps(dict(status=record['status'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),parent_sha256=record['parent_joined_receiver_sha256'])))

if __name__=='__main__':main()
