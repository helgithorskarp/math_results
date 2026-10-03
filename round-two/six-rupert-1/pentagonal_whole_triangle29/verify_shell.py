#!/usr/bin/env python3
"""Exact midpoint cover and outward tensor signs from fresh pinned geometry.

One guarded batch is not an all-source theorem. Every leaf must pass and
the freshly replayed current whole-triangle local proof is also required.
"""
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
# source_cell.py is the pinned complete proper-source copy in this packet.
import source_cell as S
B=E.B

def require(test,message):
    if not test:raise ValueError(message)
def qdecode(encoded):return S.Q(*encoded)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),E.ZERO)
def cross(a,b):return(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def bdecode(encoded):return B(*encoded)
def raw_hash(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def tree_cover(forest,geometry):
    require(forest['status']=='LITERAL_CLOSED_SOURCE_FOREST'and forest['pending']==0 and not forest['failed_leaves'],'full candidate covers every declared root')
    require(forest['ratio']==geometry['source_ratio']and 0<F(forest['ratio'])<1 and forest['faces']==geometry['source_faces']and len(forest['roots'])==108,'same exact outer-shell source domain')
    require(forest['receiver_triangle_indices']==geometry['receiver_triangle_indices'],'same complete closed receiver triangulation')
    tries=[{}for _ in range(108)]
    for index,leaf in enumerate(forest['leaves']):
        root=leaf['root'];path=leaf['path']
        require(type(root)==int and 0<=root<108 and type(path)==str and len(path)%3==0 and leaf['depth']==len(path)//3,'literal root and midpoint path')
        node=tries[root]
        for k in range(0,len(path),3):
            token=path[k:k+3]
            require(all(c in'0123'for c in token[:2])and token[2]in'01','literal split edge and child')
            a,b,child=map(int,token);require(a<b,'two distinct ordered tetrahedral vertices')
            require('leaf'not in node,'no leaf ancestor')
            require('edge'not in node or node['edge']==(a,b),'siblings use exactly the same splitting edge')
            node['edge']=(a,b);node=node.setdefault('children',{}).setdefault(child,{})
        require(not node,'no duplicate or leaf ancestor of another leaf');node['leaf']=index
    verts=[tuple(qdecode(q)for q in v)for v in geometry['source_vertices']]
    ratio=F(forest['ratio']);tets={};internals=0
    def visit(node,tet):
        nonlocal internals
        if'leaf'in node:
            require(set(node)=={'leaf'},'terminal leaf is terminal');tets[node['leaf']]=tet;return
        require(set(node)=={'edge','children'}and set(node['children'])=={0,1},'both closed midpoint children exist, no covering hole')
        internals+=1;a,b=node['edge'];mid=tuple((x+y)/2 for x,y in zip(tet[a],tet[b]))
        first=list(tet);first[b]=mid;second=list(tet);second[a]=mid
        visit(node['children'][0],tuple(first));visit(node['children'][1],tuple(second))
    expected=[]
    for face_no,face in enumerate(geometry['source_faces']):
        for i in range(1,4):
            for part in range(3):expected.append(dict(face=face_no,face_triangle=[face[0],face[i],face[i+1]],frustum_part=part))
    require(expected==forest['roots'],'all exact source frustum roots occur in their canonical order')
    for node,root in zip(tries,expected):
        A,C1,C2=(verts[i]for i in root['face_triangle'])
        aA=tuple(ratio*z for z in A);aB=tuple(ratio*z for z in C1);aC=tuple(ratio*z for z in C2)
        tet=[(aA,aB,aC,C2),(aA,aB,C1,C2),(aA,A,C1,C2)][root['frustum_part']]
        visit(node,tet)
    require(set(tets)==set(range(len(forest['leaves'])))and len(tets)-internals==108,'complete exact forest identity')
    return tets,internals

def receiver_barycentric_vertices(stress,geometry,vertex_count):
    require(type(stress['receiver_triangle'])==int and 0<=stress['receiver_triangle']<len(geometry['receiver_triangle_indices']),'one actual receiver fan triangle')
    triangle=geometry['receiver_triangle_indices'][stress['receiver_triangle']]
    require(len(triangle)==3 and len(set(triangle))==3 and all(type(i)==int and 0<=i<vertex_count for i in triangle),'three literal actual receiving fan vertices')
    vertices=[tuple(F(int(i==j))for j in range(vertex_count))for i in triangle]
    path=stress.get('receiver_path',str(stress['receiver_triangle']))
    require(type(path)==str and path[:1]==str(stress['receiver_triangle'])and len(path)in(1,2)and all(j in'0123'for j in path[1:]),'whole closed fan or one literal midpoint child')
    if len(path)==2:
        a,b,c=vertices
        midpoint=lambda u,v:tuple((x+y)/2 for x,y in zip(u,v))
        ab,bc,ca=midpoint(a,b),midpoint(b,c),midpoint(c,a)
        vertices=[(a,ab,ca),(ab,b,bc),(ca,bc,c),(ab,bc,ca)][int(path[1])]
    require(all(all(z>=0 for z in v)and sum(v)==1 for v in vertices),'actual receiving vertices are exact convex combinations')
    return vertices

def stress_coefficients(stress,tet,geometry,rows,pairs,points,root):
    edges=stress['edges'];indices=[rows[tuple(edge)][0]for edge in edges]
    require(len(indices)==len(set(indices))==3,'three distinct actual support edges')
    moving=stress['moving_originals'];orientation=stress['cofactor_orientation']
    require(type(orientation)==int and orientation in(-1,1)and len(moving)==3 and all(type(p)==int and 0<=p<92 for p in moving),'proper literal stress orientation and moving-original indices')
    def pair(i,j):
        if i<j:return pairs[f'{i}:{j}']
        return [-v for v in pairs[f'{j}:{i}']]
    i,j,k=indices;weights=[pair(j,k),pair(k,i),pair(i,j)]
    if orientation<0:weights=[[-v for v in w]for w in weights]
    minimum_weight=min(v.lo for w in weights for v in w)
    require(minimum_weight>0,'affine cofactor weights positive on every exact closed receiver vertex')
    vertex_count=len(weights[0])
    receiver_vertices=receiver_barycentric_vertices(stress,geometry,vertex_count)
    affine=lambda values,beta:sum((v.ratio(b)for v,b in zip(values,beta)if b),E.ZERO)
    piece_weights=[[affine(w,beta)for beta in receiver_vertices]for w in weights]
    def qb(z):return E.B.interval(H.K.coerce(H.V.Q(z.a,z.b)).interval(root))
    c=[tuple(qb(z)for z in v)for v in tet]
    source_pairs=list(itertools.combinations_with_replacement(range(4),2))
    dotpairs=[dot(c[a],c[b])for a,b in source_pairs]
    gaps=[]
    for edge_no,point_no in enumerate(moving):
        P=points[point_no];transformed=[]
        for (a,b),cd in zip(source_pairs,dotpairs):
            u,v=c[a],c[b];pu,pv=dot(P,u),dot(P,v)
            rotational=cross(tuple(x+y for x,y in zip(u,v)),P)
            transformed.append(tuple((E.ONE-cd)*p+x*pv+y*pu+z for p,x,y,z in zip(P,u,v,rotational)))
        original_row=rows[tuple(edges[edge_no])][1]
        require(len(original_row)==vertex_count,'every actual support has the same complete receiving vertex inventory')
        values=[]
        for beta in receiver_vertices:
            m=tuple(affine([row[0][j]for row in original_row],beta)for j in range(3))
            h=affine([row[1]for row in original_row],beta)
            values.append([h*(E.ONE+cd)-dot(m,T)for cd,T in zip(dotpairs,transformed)])
        gaps.append(values)
    coefficients=[]
    for a,b in itertools.combinations_with_replacement(range(3),2):
        for source in range(10):
            value=sum((piece_weights[i][a]*gaps[i][b][source]+piece_weights[i][b]*gaps[i][a][source]for i in range(3)),E.ZERO).ratio(F(1,2))
            coefficients.append(value)
    require(len(coefficients)==60,'all60 closed tensor Bernstein coefficients')
    return minimum_weight,coefficients

def verify_stress(stress,tet,geometry,rows,pairs,points,root):
    minimum_weight,coefficients=stress_coefficients(stress,tet,geometry,rows,pairs,points,root)
    require(max(v.hi for v in coefficients)<0,'ALL60 closed tensor Bernstein coefficients strictly negative')
    encoded=[[v.lo,v.hi]for v in coefficients]
    return dict(receiver_triangle=stress['receiver_triangle'],receiver_path=stress.get('receiver_path',str(stress['receiver_triangle'])),edges=stress['edges'],moving_originals=stress['moving_originals'],
                cofactor_orientation=stress['cofactor_orientation'],minimum_positive_vertex_weight=str(F(minimum_weight,E.SCALE)),
                coefficient_count=60,coefficient_hash=raw_hash(encoded),
                coefficient_integer_intervals=encoded,
                minimum_lower_coefficient=str(F(min(v.lo for v in coefficients),E.SCALE)),
                maximum_upper_coefficient=str(F(max(v.hi for v in coefficients),E.SCALE)))

def receiver_stress_cover(leaf,geometry):
    require(leaf['kind']=='three_support_stress'and geometry['receiver_triangle_indices']==[[0,1,2]],'one entire literal closed triangle29')
    stresses=leaf['receiver_stresses']
    paths=[s.get('receiver_path',str(s['receiver_triangle']))for s in stresses]
    require(paths==sorted(set(paths)),'literal ordered distinct closed receiving pieces')
    for stress in stresses:
        receiver_barycentric_vertices(stress,geometry,3)
    for fan in ('0',):
        actual=[path for path in paths if path[:1]==fan]
        require(actual==[fan]or actual==[fan+str(j)for j in range(4)],'whole closed fan or ALL four closed midpoint children, no hole/ancestor')
    return leaf['receiver_stresses']

def run(args):
    started=time.monotonic();deadline=started+args.seconds
    geometry_path=Path(args.geometry);geometry_bytes=geometry_path.read_bytes()
    require(hashlib.sha256(geometry_bytes).hexdigest()==args.geometry_sha,'fresh exact geometry cache fingerprint')
    geometry=json.loads(geometry_bytes);forest_path=Path(args.forest)
    require(hashlib.sha256(forest_path.read_bytes()).hexdigest()==geometry['forest_sha256'],'exact same discovered candidate input')
    forest=json.loads(forest_path.read_text());tets,internals=tree_cover(forest,geometry)
    require(geometry['fixedpoint_scale']==E.SCALE,'same explicit outward fixed-point arithmetic')
    root=H.V.I(*[F(s)for s in geometry['root_interval']])
    rows={tuple(row['edge']):(i,[(tuple(bdecode(z)for z in v['m']),bdecode(v['h']))for v in row['vertices']])for i,row in enumerate(geometry['actual_edge_rows'])}
    pairs={k:[bdecode(z)for z in v]for k,v in geometry['actual_edge_pair_cofactor_vertex_enclosures'].items()}
    points=[tuple(bdecode(z)for z in p)for p in geometry['original_point_enclosures']]
    require(len(points)==92,'all92 original enclosures')
    stop=min(len(forest['leaves']),args.start+args.count)
    require(type(args.start)==int and 0<=args.start<stop,'nonempty declared exact leaf range')
    records=[]
    for index in range(args.start,stop):
        if time.monotonic()>=deadline:break
        leaf=forest['leaves'][index]
        checks=[verify_stress(s,tets[index],geometry,rows,pairs,points,root)for s in receiver_stress_cover(leaf,geometry)]
        record=dict(index=index,root=leaf['root'],path=leaf['path'],kind=leaf['kind'],exact_checks=checks)
        records.append(record)
    complete=len(records)==stop-args.start
    record=dict(agent='six-rupert-1',role='researcher',status='DECLARED_EXACT_LEAF_RANGE_PASSED'if complete else'GUARD_INCOMPLETE_EXACT_LEAF_RANGE',
                geometry_sha256=args.geometry_sha,forest_sha256=geometry['forest_sha256'],
                exact_cover_roots=108,exact_midpoint_internal_nodes=internals,exact_cover_leaves=len(tets),
                source_ratio=geometry['source_ratio'],start=args.start,requested_stop=stop,completed_stop=args.start+len(records),
                coefficient_checks=sum(sum(c['coefficient_count']for c in r.get('exact_checks',[]))for r in records),
                exact_leaf_records=records,
                mathematical_scope='Only this declared exact leaf range has coefficient proof. Whole-source classification requires every range and the freshly replayed whole-triangle local proof.')
    raw=(json.dumps(record,indent=2,sort_keys=True)+'\n').encode()
    if args.compare:require(raw==Path(args.compare).read_bytes(),'whole exact range record agrees byte for byte')
    Path(args.output).write_bytes(raw)
    print(json.dumps(dict(status=record['status'],start=record['start'],completed_stop=record['completed_stop'],coefficient_checks=record['coefficient_checks'],
                         bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),elapsed_seconds=time.monotonic()-started,
                         peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,threads=1)))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--forest',default=str(Path(__file__).resolve().parent/'.generated/forest.json'))
    p.add_argument('--geometry',default=str(Path(__file__).resolve().parent/'.generated/geometry.json'));p.add_argument('--geometry-sha',required=True)
    p.add_argument('--start',type=int,default=0);p.add_argument('--count',type=int,default=200)
    p.add_argument('--seconds',type=float,default=45.);p.add_argument('--compare')
    p.add_argument('--output',default=str(Path(__file__).resolve().parent/'.generated/leaves_0.json'))
    run(p.parse_args())
