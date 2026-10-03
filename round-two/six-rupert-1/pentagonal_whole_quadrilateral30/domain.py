"""Exact whole quadrilateral30 and nonredundancy audit; no fit conclusion."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, resource, time
import local as C
H=C.H
HERE=Path(__file__).resolve().parent

def run(args):
    start=time.monotonic(); deadline=start+20
    work=Path(args.work);cfg=json.loads((HERE/'configuration.json').read_text())
    target=(HERE/'target.json').read_bytes()
    H.require(hashlib.sha256(target).hexdigest()==cfg['target_sha256'],'literal entire closed target')
    t=json.loads(target);cell=dict(polygon=t['exact_polygon'],signs=t['exact_facet_signs'])
    polygon=[tuple(C.decode(z)for z in p)for p in cell['polygon']]
    H.require(len(polygon)==4 and len(cell['signs'])==60,'four literal corners and sixty original facet signs')
    model_raw=(work/'named_geometry.json').read_bytes();model_pin=cfg['expected_fresh_named_geometry_sha256']
    data=C.verified_cache(model_raw,model_pin)
    root,normals,points=data['root'],data['normals'],data['points']
    fixture=(HERE/'prior_regions.json').read_bytes();H.require(hashlib.sha256(fixture).hexdigest()==cfg['prior_regions_sha256'],'literal prior region bytes')
    fixture=json.loads(fixture);parent=dict(polygon=fixture['parent_polygon'],facet_signs=fixture['parent_phase'])
    old=[tuple(C.decode(z)for z in p)for p in parent['polygon']]
    changes=[i for i,(a,b)in enumerate(zip(cell['signs'],parent['facet_signs']))if a!=b]
    H.require(changes==[58],'single actual facet58 change')
    constraints=[(H.Z,H.O,H.Z),(H.Z,H.Z,H.O),(H.O,-H.phi,-H.phi*H.phi)]
    constraints += [tuple(sign*z for z in n)for sign,n in zip(cell['signs'],normals)]
    checks=0;turns=0;walls=[]
    for p in polygon:
        for n in constraints:
            H.require(H.sign(H.M.dot(n,(H.O,*p)),root)>=0,'all defining halfspaces at every closed corner');checks+=1
    for i,(a,b)in enumerate(zip(polygon,polygon[1:]+polygon[:1])):
        for j,p in enumerate(polygon):
            if j not in(i,(i+1)%4):H.require(H.sign(C.turn(a,b,p),root)>0,'all strict global turns');turns+=1
        wall=[j for j,n in enumerate(constraints)if H.M.dot(n,(H.O,*a))==H.Z and H.M.dot(n,(H.O,*b))==H.Z]
        H.require(bool(wall),'each entire side is an actual defining wall');walls.append(wall)
    area=sum((a[0]*b[1]-a[1]*b[0]for a,b in zip(polygon,polygon[1:]+polygon[:1])),H.Z)/2
    H.require(H.sign(area,root)>0,'positive exact area')
    seams=[]
    for i,(a,b)in enumerate(zip(polygon,polygon[1:]+polygon[:1])):
        for j,(u,v)in enumerate(zip(old,old[1:]+old[:1])):
            if a==v and b==u:seams.append(dict(new_side=i,public29_side=j))
    H.require(seams==[dict(new_side=3,public29_side=1)]and walls[3]==[61],'entire literal reversed facet58 side')
    center=tuple(sum((p[j]for p in polygon),H.Z)/4 for j in range(2))
    for j,n in enumerate(constraints):H.require(H.sign(H.M.dot(n,(H.O,*center)),root)>0,'interior center is strict in all defining halfspaces')
    encoded_prior=fixture['polygons']
    H.require(len(encoded_prior)==10,'ten literal prior regions representing the thirteen proved cells')
    prior=[[tuple(C.decode(z)for z in p)for p in poly]for poly in encoded_prior]
    rejections=[];raw=(H.O,*center)
    for g in H.M.group():
        H.require(time.monotonic()<deadline,'bounded signed-image audit')
        r=tuple(sum((H.K.coerce(H.V.Q(g[j][i].a,g[j][i].b))*raw[j]for j in range(3)),H.Z)for i in range(3))
        sign=H.sign(r[0],root);indices=[]
        for poly in prior:
            if sign==0:indices.append(-1);continue
            values=[]
            for a,b in zip(poly,poly[1:]+poly[:1]):
                ds,dt=b[0]-a[0],b[1]-a[1]
                values.append(sign*H.sign(ds*r[2]-dt*r[1]+(dt*a[0]-ds*a[1])*r[0],root))
            H.require(min(values)<0,'quadrilateral30 interior center outside every signed actualG image of each old region')
            indices.append(next(i for i,z in enumerate(values)if z<0))
        rejections.append(indices)
    record=dict(agent='six-rupert-1',role='researcher',status='EXACT_WHOLE_CLOSED_QUADRILATERAL30_DOMAIN_AND_SIGNED_PRIOR_NONREDUNDANCY_PASSED_FIT_OPEN',receiver_cell_index=30,named_target='standard same-handed pentagonal hexecontahedron',exact_polygon=cell['polygon'],exact_facet_signs=cell['signs'],phase=''.join('+'if s>0 else '-'for s in cell['signs']),exact_side_wall_indices=walls,closed_halfspace_corner_checks=checks,strict_global_turn_checks=turns,exact_raw_chart_area=H.encode(area),changes_from_public29=changes,entire_reversed_public29_seam=seams[0],exact_barycenter=[H.encode(z)for z in center],actual_proper_group_elements=len(rejections),signed_receiving_image_cases=len(rejections)*len(prior),literal_prior_regions=len(prior),image_rejection_side_indices=rejections,literal_target_sha256=hashlib.sha256(target).hexdigest(),named_model_fresh_this_mode_sha256=model_pin,parent_public_certificate_sha256=fixture['parent_certificate_sha256'],mathematical_scope='Both polygon/halfspace inclusions prove the entire closed quadrilateral. Its strict interior center is outside every signed/projective actualG image of the ten published literal regions constituting thirteen cells. No local collar, source entry, fit or global non-Rupert conclusion.',resources=dict(guard_seconds=20,threads=1,maximum_intensive_jobs=1,no_escalation=True))
    H.require(time.monotonic()<deadline,'complete target audit within guard')
    out=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:H.require(out==args.compare.read_bytes(),'whole ordinary/optimized audit agrees')
    args.output.write_bytes(out)
    print(json.dumps(dict(status=record['status'],walls=walls,halfspace_checks=checks,global_turns=turns,prior_image_cases=len(rejections)*len(prior),bytes=len(out),sha256=hashlib.sha256(out).hexdigest(),elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--compare',type=Path);run(p.parse_args())
