#!/usr/bin/env python3
"""Fresh exact named geometry and source-cover roots; leaf signs PENDING."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,itertools,json,resource,sys,time
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'round-two/six-rupert-1/pentagonal_closed_horizon_cell'))
import geometry as H
import polynomial as E
import check as C
import source_cell as S

def encB(value,root):
    z=E.B.interval(H.K.coerce(value).interval(root));return [z.lo,z.hi]
def encQ(value):return [str(value.a),str(value.b)]
def decQ(value):return S.Q(*value)
def det(A):return S.determinant(A)
def qsub(a,b):return tuple(x-y for x,y in zip(a,b))
def qcross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def geometry(args):
    start=time.monotonic();deadline=start+args.seconds
    config=json.loads((Path(__file__).resolve().parent/'configuration.json').read_text())
    dependency=ROOT/'round-two/six-rupert-1/pentagonal_closed_horizon_cell'
    for name,pin in config['local_dependency_pins'].items():
        H.require(hashlib.sha256((dependency/name).read_bytes()).hexdigest()==pin,'pinned local proof source '+name)
    forest=dict(faces=config['source_faces'],ratio=config['ratio'])
    named=H.build(deadline);root=named['root'];points=named['points']
    cert_path=ROOT/'round-two/six-rupert-1/pentagonal_closed_horizon_cell/certificate.json'
    cert=json.loads(cert_path.read_text())
    polygon=[tuple(C.decode(z)for z in p)for p in cert['polygon']]
    raw=[(H.O,*p)for p in polygon]
    constraints=[(H.Z,H.O,H.Z),(H.Z,H.Z,H.O),(H.O,-H.phi,-H.phi*H.phi)]
    constraints.extend(tuple(s*x for x in n)for s,n in zip(cert['facet_signs'],named['normals']))
    for r in raw:
        H.require(all(H.sign(H.M.dot(a,r),root)>=0 for a in constraints),'all closed63 facet/chamber inequalities')
    walls=[]
    for i,(a,b)in enumerate(zip(polygon,polygon[1:]+polygon[:1])):
        H.require(all(H.sign(C.turn(a,b,c),root)>0 for j,c in enumerate(polygon)if j not in(i,(i+1)%5)),'whole polygon side convexity')
        matching=[j for j,wall in enumerate(constraints)if H.M.dot(wall,(H.O,*a))==H.Z and H.M.dot(wall,(H.O,*b))==H.Z]
        H.require(bool(matching),'every polygon side is an actual defining wall');walls.append(matching)
    edges=config['receiver_edges'];directions=[];rows=[];facet_checks=0
    for a,b in edges:
        if time.monotonic()>=deadline:raise TimeoutError('Actual support geometry deadline; no theorem')
        selected=[q for q in named['clauses']if q['edge']==sorted((a,b))and q['direction']==(1 if a<b else-1)]
        H.require(len(selected)==1,'one actual oriented edge/horizon clause')
        clause=selected[0];d=H.M.sub(points[b],points[a]);directions.append(d)
        fields=[]
        for r in raw:
            u=clause['direction']*H.M.dot(clause['u'],r)
            v=clause['direction']*H.M.dot(clause['v'],r)
            H.require(H.sign(u,root)>=0 and H.sign(v,root)<=0 and H.sign(u-v,root)>0,'actual incident facets give a positive-height supporting normal on every closed vertex')
            facet_checks+=2
            m=H.M.cross(d,r);h=H.M.dot(m,points[a])
            normal=tuple(sum((r[j]*clause['normal_linear_coefficients'][j][i]for j in range(3)),H.Z)for i in range(3))
            k=next(i for i in range(3)if m[i]!=H.Z);factor=normal[k]/m[k]
            H.require(H.sign(factor,root)>0 and normal==tuple(factor*z for z in m),'positive exact edge-normal/facet-normal proportionality')
            H.require(H.sign(h,root)>0,'strict actual receiver height')
            fields.append(dict(m=[encB(z,root)for z in m],h=encB(h,root)))
        rows.append(dict(edge=[a,b],vertices=fields))
    cofactor={}
    for i,j in itertools.combinations(range(len(edges)),2):
        if time.monotonic()>=deadline:raise TimeoutError('Exact cofactor preparation deadline; no theorem')
        d=H.M.cross(directions[i],directions[j])
        cofactor[f'{i}:{j}']=[encB(H.M.dot(d,r),root)for r in raw]
    forest['roots']=[]
    for fno,face in enumerate(forest['faces']):
        for i in range(1,4):
            for part in range(3):forest['roots'].append(dict(face=fno,face_triangle=[face[0],face[i],face[i+1]],frustum_part=part))
    source_path=Path(args.output).with_name('source.json')
    oldargv=sys.argv
    try:
        sys.argv=['check_cayley_cell.py','--output',str(source_path)]
        S.main()
    finally:sys.argv=oldargv
    source=json.loads(source_path.read_text())
    verts=[tuple(decQ(q)for q in v)for v in source['vertices']]
    facets=[tuple(decQ(q)for q in w)for w in source['facets']];threshold=decQ(source['threshold'])
    H.require(len(forest['faces'])==12,'all source facets explicitly represented')
    turns=0
    for normal,ids in zip(facets,forest['faces']):
        H.require(len(ids)==len(set(ids))==5 and all(type(i)==int and 0<=i<20 for i in ids),'source facet literal five-cycle')
        actual={i for i,p in enumerate(verts)if S.V.dot(normal,p)==threshold}
        H.require(actual==set(ids),'source face equals all actual dodecahedral vertices on its wall')
        for i,(a,b)in enumerate(zip(ids,ids[1:]+ids[:1])):
            for c in ids:
                if c in(a,b):continue
                turn=S.V.dot(normal,qcross(qsub(verts[b],verts[a]),qsub(verts[c],verts[a])))
                H.require(turn.sign()>0,'every other source-face vertex is strictly left of each boundary edge');turns+=1
    expected=[]
    for fno,face in enumerate(forest['faces']):
        for i in range(1,4):
            for part in range(3):expected.append(dict(face=fno,face_triangle=[face[0],face[i],face[i+1]],frustum_part=part))
    H.require(expected==forest['roots'] and len(expected)==108,'every face triangle has all three frustum-root parts')
    ratio=F(forest['ratio']);H.require(ratio==F(1,64),'stated inner source polytope ratio')
    H.require((S.Q(1)-163*ratio*decQ(source['coordinate_limit'])).sign()>0,'entire inner source polytope lies strictly inside published local cube')
    H.require(time.monotonic()<deadline,'complete exact geometry finished within its guard')
    record=dict(agent='six-rupert-1',role='researcher',status='EXACT_NAMED_GEOMETRY_RECEIVER_CELL_SOURCE_QUOTIENT_AND_FRUSTUM_ROOTS_PREPARED_LEAF_SIGNS_PENDING',
                fixedpoint_scale=E.SCALE,root_interval=[str(root.lo),str(root.hi)],
                original_point_enclosures=[[encB(z,root)for z in p]for p in points],
                exact_original_points=[[H.encode(z)for z in p]for p in points],
                actual_edge_rows=rows,actual_edge_pair_cofactor_vertex_enclosures=cofactor,
                receiver_polygon=cert['polygon'],receiver_triangle_indices=[[0,1,2],[0,2,3],[0,3,4]],
                receiver_exact_side_wall_indices=walls,actual_facet_support_sign_checks=facet_checks,
                source_vertices=source['vertices'],source_facets=source['facets'],source_threshold=source['threshold'],
                source_faces=forest['faces'],source_ratio=forest['ratio'],source_root_count=108,
                exact_source_face_global_turn_checks=turns,
                complete_named_geometry_record=named['record'],complete_source_quotient_record=source,
                source_hashes=config['local_dependency_pins'],
                forest_sha256=config['expected_forest_sha256'],
                proof_status='Only exact geometry and enclosures prepared. No leaf sign or completed all-source classification claimed here.')
    out=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    Path(args.output).write_bytes(out)
    print(json.dumps(dict(status=record['status'],bytes=len(out),sha256=hashlib.sha256(out).hexdigest(),
                         elapsed_seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1)))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--seconds',type=float,default=45.)
    p.add_argument('--output',default=str(Path(__file__).resolve().parent/'.generated/geometry.json'))
    args=p.parse_args();Path(args.output).parent.mkdir(parents=True,exist_ok=True);geometry(args)
