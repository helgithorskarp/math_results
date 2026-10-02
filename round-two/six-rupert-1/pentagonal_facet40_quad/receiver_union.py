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
PARENT=ROOT/'round-two/six-rupert-1/pentagonal_principal_axis_cell'
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
    old=[tuple(C.decode(z)for z in v)for v in parent['exact_quad']]
    new=[tuple(C.decode(z)for z in v)for v in certificate['polygon']]
    H.require(len(old)==len(new)==4,'whole parent and new closed quadrilaterals')
    H.require(parent['closed_cell_indices']==[14,28,13,11] and parent['actual_wall_indices']==[[1],[43],[50],[0]],'exact parent domain inventory')
    checks=0
    for i,(a,b) in enumerate(zip(old,old[1:]+old[:1])):
        for j,c in enumerate(old):
            if j not in(i,(i+1)%4):
                H.require(H.sign(C.turn(a,b,c),root)>0,'parent globally convex cyclic ring');checks+=1
    phase=certificate['facet_signs'];wall=tuple(-phase[40]*z for z in normals[40])
    evaluate=lambda p:H.M.dot(wall,(H.O,*p))
    H.require([H.sign(evaluate(p),root)for p in old]==[1,0,0,1],'parent wholly on old closed actual facet40 side')
    H.require([H.sign(evaluate(p),root)for p in new]==[-1,-1,0,0],'new whole quad on opposite side with exactly its full shared side')
    a,b=old[1],old[2];d=H.M.sub(b,a)
    coordinate=next(j for j,z in enumerate(d)if z!=H.Z)
    parameters=[]
    for p in (new[3],new[2]):
        z=(p[coordinate]-a[coordinate])/d[coordinate]
        H.require(p==tuple(x+z*y for x,y in zip(a,d)) and H.sign(z,root)>0 and H.sign(1-z,root)>0,'both literal seam endpoints strictly inside the parent side')
        parameters.append(z)
    H.require(H.sign(parameters[1]-parameters[0],root)>0,'actual reversed closed seam orientation')
    # The new point is outside the old quad. Both regions lie on opposite
    # sides of the same true wall, so their intersection is exactly this
    # closed segment, not a convex-hull enlargement of unknown phases.
    barycenter=tuple(sum((p[j]for p in new),H.Z)/4 for j in range(2))
    H.require(H.sign(evaluate(barycenter),root)<0,'strict raw receiving-domain enlargement')
    exclusions=parent_image_exclusions(barycenter,old,root)
    return dict(agent='six-rupert-1',role='researcher',status='EXACT_CLOSED_FACET40_PARTIAL_WALL_RECEIVER_UNION_PASSED',
        parent_cells=[14,28,13,11],closed_cell_indices=[14,28,13,11,20],
        exact_parent_quad=parent['exact_quad'],exact_added_quad=certificate['polygon'],
        new_fan_triangle_indices=[[0,1,2],[0,2,3]],shared_actual_facet=40,shared_wall=43,
        shared_parent_side_indices=[1,2],shared_new_side_indices=[2,3],
        strict_parent_side_parameters=[H.encode(z)for z in parameters],parent_global_turn_checks=checks,
        exact_new_quad_barycenter=[H.encode(z)for z in barycenter],signed_parent_receiving_image_count=60,
        new_barycenter_parent_image_rejection_side_indices=exclusions,
        exact_shared_segment=[certificate['polygon'][2],certificate['polygon'][3]],
        parent_source_commit='d89e5a0cc1417ed93aab1470cae3307bd576f9fd',
        parent_graph_cid='bafkreie6hs3pebb2adk44qgp7tchv7j5uezinsrljr6hunnaoecgkqynhy',
        scope='Omega=parent closed quadrilateral UNION added closed quadrilateral20, retaining the exact shared subsegment and all boundaries. No convex-hull region or adjacent19/34 claim.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'.generated/receiver_union.json');args=p.parse_args()
    cache=json.loads((HERE/'.generated/named_geometry.json').read_text())
    from fractions import Fraction as F
    root=H.V.I(*[F(q)for q in cache['root_interval']])
    cert=json.loads((HERE/'local_certificate.json').read_text())
    parent=json.loads((PARENT/'joined_receiver.json').read_text())
    result=compute(cert,[tuple(C.decode(z)for z in n)for n in cache['outward_facet_normals']],root,parent)
    result['parent_joined_receiver_sha256']=hashlib.sha256((PARENT/'joined_receiver.json').read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(status=result['status'],new_closed_cells=result['closed_cell_indices'],shared_actual_facet=40)))
if __name__=='__main__':main()
