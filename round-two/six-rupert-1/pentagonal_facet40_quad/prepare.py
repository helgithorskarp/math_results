#!/usr/bin/env python3
"""Prepare exact outer-source proposal data from the freshly reconstructed named solid.

This stage is not a complete all-source certificate.  Its cache is
linked to the completed fresh local run, and every selected original support
is checked again, without importing centrality or an equality inventory.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,resource,sys,time
import local as C
H,E=C.H,C.E
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
PARENT=ROOT/'round-two/six-rupert-1/pentagonal_principal_axis_cell'
import source_cell as S
import receiver_union as J

def encB(value,root):
    z=E.B.interval(H.K.coerce(value).interval(root));return [z.lo,z.hi]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=float,default=40.)
    parser.add_argument('--output',type=Path,default=HERE/'.generated/geometry.json');args=parser.parse_args()
    start=time.monotonic();deadline=start+args.seconds
    config=json.loads((HERE/'configuration.json').read_text())
    dependency=ROOT/'round-two/six-rupert-1/pentagonal_closed_horizon_cell'
    for name,pin in config['local_dependency_pins'].items():H.require(hashlib.sha256((dependency/name).read_bytes()).hexdigest()==pin,'pinned exact model/polynomial source '+name)
    for name,pin in config['own_local_pins'].items():H.require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==pin,'pinned current local proof '+name)
    for name,pin in config['parent_source_pins'].items():H.require(hashlib.sha256((PARENT/name).read_bytes()).hexdigest()==pin,'pinned previous entire receiver theorem '+name)
    local_path=HERE/'.generated/local.json'
    H.require(hashlib.sha256(local_path.read_bytes()).hexdigest()==config['expected_local_record_sha256'],'completed whole fresh local proof record')
    local=json.loads(local_path.read_text());cert=json.loads((HERE/'local_certificate.json').read_text())
    H.require(hashlib.sha256(json.dumps(cert,sort_keys=True).encode()).hexdigest()==local['certificate_sha256'],'same complete receiver/contact certificate')
    cache_path=HERE/'.generated/named_geometry.json'
    H.require(hashlib.sha256(cache_path.read_bytes()).hexdigest()==config['expected_fresh_named_geometry_sha256'],'same completed fresh actual named-geometry cache')
    cache=json.loads(cache_path.read_text())
    H.require(cache['record']==local['complete_named_geometry_record'],'exact cache comes from the completed actual-model rebuild')
    root=H.V.I(*[F(q)for q in cache['root_interval']])
    points=[tuple(C.decode(z)for z in p)for p in cache['exact_original_points']]
    polygon=[tuple(C.decode(z)for z in p)for p in cert['polygon']]
    raw=[(H.O,*p)for p in polygon]
    edges=sorted({tuple(c[:2])for d in cert['duals']for c in d['contacts']})
    rows=[];directions=[];comparisons=0
    for a,b in edges:
        d=H.M.sub(points[b],points[a]);directions.append(d);fields=[]
        for r in raw:
            if time.monotonic()>=deadline:raise TimeoutError('actual whole-quadrilateral outer support preparation incomplete')
            m=H.M.cross(d,r);h=H.M.dot(m,points[a])
            H.require(H.sign(h,root)>0,'strict positive original receiver support height')
            H.require(H.M.dot(m,r)==H.Z and H.M.dot(m,d)==H.Z,'actual support/edge perpendicular identities')
            for p in points:
                H.require(H.sign(h-H.M.dot(m,p),root)>=0,'all92 original points satisfy every closed-corner supporting plane');comparisons+=1
            fields.append(dict(m=[encB(z,root)for z in m],h=encB(h,root)))
        rows.append(dict(edge=[a,b],vertices=fields))
    pairs={}
    for i,j in itertools.combinations(range(len(edges)),2):
        cross=H.M.cross(directions[i],directions[j])
        pairs[f'{i}:{j}']=[encB(H.M.dot(cross,r),root)for r in raw]
    source_path=HERE/'.generated/source.json';oldargv=sys.argv
    try:sys.argv=['source_cell.py','--output',str(source_path)];S.main()
    finally:sys.argv=oldargv
    source=json.loads(source_path.read_text());vertices=[tuple(S.Q(*q)for q in v)for v in source['vertices']]
    facets=[tuple(S.Q(*q)for q in v)for v in source['facets']];threshold=S.Q(*source['threshold'])
    faces=config['source_faces'];turns=0
    H.require(len(faces)==len(facets)==12,'all twelve source faces')
    for normal,ids in zip(facets,faces):
        H.require(len(ids)==len(set(ids))==5 and all(type(i)==int and 0<=i<20 for i in ids),'literal source-face five-cycle')
        H.require({i for i,p in enumerate(vertices)if S.V.dot(normal,p)==threshold}==set(ids),'source face includes every actual incident vertex')
        for a,b in zip(ids,ids[1:]+ids[:1]):
            for c in ids:
                if c in(a,b):continue
                u=tuple(x-y for x,y in zip(vertices[b],vertices[a]));v=tuple(x-y for x,y in zip(vertices[c],vertices[a]))
                cross=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
                H.require(S.V.dot(normal,cross).sign()>0,'strict complete source-face orientation');turns+=1
    ratio=F(config['ratio']);H.require(0<ratio<1,'actual proper-source core ratio');rho=F(local['closed_relative_cayley_euclidean_radius'])
    H.require((S.Q(rho*rho)-ratio*ratio*S.Q(*source['covering_cayley_radius_squared'])).sign()>0,'entire inner source polytope lies strictly inside the newly proved Euclidean collar')
    forest_sha=config['expected_forest_sha256']
    parent_joined=json.loads((PARENT/'joined_receiver.json').read_text())
    joined=J.compute(cert,[tuple(C.decode(z)for z in v)for v in cache['outward_facet_normals']],root,parent_joined)
    joined['parent_joined_receiver_sha256']=hashlib.sha256((PARENT/'joined_receiver.json').read_bytes()).hexdigest()
    H.require(joined==json.loads((HERE/'receiver_union.json').read_text()),'whole declared literal closed receiving union with partial shared seam')
    record=dict(agent='six-rupert-1',role='researcher',status='EXACT_OUTER_PROPOSAL_GEOMETRY_PREPARED_ALL_SOURCE_LEAF_SIGNS_PENDING',fixedpoint_scale=E.SCALE,
                root_interval=cache['root_interval'],original_point_enclosures=[[encB(z,root)for z in p]for p in points],
                exact_original_points=cache['exact_original_points'],receiver_polygon=cert['polygon'],receiver_triangle_indices=[[0,1,2],[0,2,3]],
                actual_edge_rows=rows,actual_edge_pair_cofactor_vertex_enclosures=pairs,
                source_vertices=source['vertices'],source_facets=source['facets'],source_threshold=source['threshold'],
                source_faces=faces,source_ratio=str(ratio),source_root_count=108,forest_sha256=forest_sha,
                complete_named_geometry_record=cache['record'],complete_source_quotient_record=source,
                outward_facet_normals=cache['outward_facet_normals'],exact_receiver_union=joined,
                receiver_exact_side_wall_indices=local['closed_cell_geometry']['exact_polygon_edge_wall_indices'],
                exact_parent_boundary=dict(parent_cells=[14,28,13,11],current_cell=20,changed_actual_facet=40,shared_wall=43,current_vertex_indices=[2,3],parent_vertex_indices=[1,2],parent_source_commit=joined['parent_source_commit']),
                local_dependency_pins=config['local_dependency_pins'],own_local_source_pins=config['own_local_pins'],parent_source_pins=config['parent_source_pins'],
                local_whole_record_sha256=hashlib.sha256(local_path.read_bytes()).hexdigest(),
                actual_original_support_comparisons=comparisons,source_face_global_turn_checks=turns,
                proof_status='Exact supports and inner-core link only. Every outer-source leaf remains pending until a full closed cover and all signs pass.')
    H.require(time.monotonic()<deadline,'complete exact support/source preparation finished inside its guard')
    path=args.output;raw_bytes=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode();path.write_bytes(raw_bytes)
    print(json.dumps(dict(status=record['status'],edges=len(edges),original_support_comparisons=comparisons,source_ratio=str(ratio),bytes=len(raw_bytes),sha256=hashlib.sha256(raw_bytes).hexdigest(),elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))

if __name__=='__main__':main()
