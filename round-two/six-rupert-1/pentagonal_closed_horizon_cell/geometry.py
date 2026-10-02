#!/usr/bin/env python3
"""Exact named-solid horizon reduction with closed degeneracies retained.

Reused exact named-model generator. No global containment decision is made.
All92 originals and60 actual pentagonal facets are rebuilt before use.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
            'NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json,resource,sys,time
ROOT=Path(__file__).resolve().parents[3]
MODEL_DIR=Path(__file__).resolve().parents[1]/'pentagonal_minimum_diameter'
PINS={'verify.py':'12c94ea3ab9d7bc42e2086dbb5fbb9154306d6fd7095a8be4b25bb44fefd5339',
      'model.py':'aa8512eed3abe60c8d897f725f7015ffb22617cf0287c3f0533ed23805c8084c',
      'model.json':'e1ce268370de64b35be62bd14ed36b63fe48dc240e5a73a80b5fe5136a2eec8e'}
for name,pin in PINS.items():
    if hashlib.sha256((MODEL_DIR/name).read_bytes()).hexdigest()!=pin:
        raise ValueError('pinned named model changed: '+name)
spec=importlib.util.spec_from_file_location('verify',MODEL_DIR/'verify.py')
V=importlib.util.module_from_spec(spec);sys.modules['verify']=V;spec.loader.exec_module(V)
spec=importlib.util.spec_from_file_location('horizon_named_model',MODEL_DIR/'model.py')
M=importlib.util.module_from_spec(spec);sys.modules[spec.name]=M;spec.loader.exec_module(M)
K,Z,O,phi=M.K,M.K(),M.K.coerce(1),M.K.coerce(V.PHI)

def require(test,message):
    if not test:raise ValueError(message)

def sign(value,root):
    value=K.coerce(value)
    if value==Z:return 0
    enclosure=value.interval(root)
    if enclosure.lo>0:return 1
    if enclosure.hi<0:return -1
    raise ValueError('undecided algebraic sign; no mathematical conclusion')

def encode(value):
    return [[str(q.a),str(q.b)] for q in K.coerce(value).c]

def build(deadline=float('inf')):
    started=time.monotonic();root,enclosed,scale=V.named_parameters()
    X=M.X
    parameters=(O,phi*(3-X.square()),5-phi+2*phi*X-3*X.square(),
                ((14*phi-27)*X.square()+(10*phi-6)*X+32-12*phi)/31,
                (X.square()-2)/phi)
    require(X*parameters[4]==O,'positive root reciprocal identity')
    for p,interval in zip(parameters,enclosed):
        bound=p.interval(root)
        require(bound.lo>0 and bound.lo<=interval.hi and interval.lo<=bound.hi,'named positive parameter branch')
    formal=V.vertices(V.group())
    evaluated=[tuple(sum((K.coerce(c)*p for c,p in zip(coordinate,parameters)),Z)
                     for coordinate in point) for point in formal]
    positive=set()
    for point in evaluated:
        for value in point:
            direction=sign(value,root)
            if direction:positive.add(value if direction>0 else -value)
    require(len(positive)==20,'exact literal coordinate palette')
    palette=sorted(positive,key=lambda z:z.interval(root).lo)
    require(all(palette[i].interval(root).hi<palette[i+1].interval(root).lo for i in range(19)),
            'exact positive palette ordering')
    literal=json.loads((MODEL_DIR/'model.json').read_text())
    points=[tuple(Z if c==0 else palette[abs(c)-1]*(1 if c>0 else -1) for c in row)
            for row in literal['vertices']]
    require(len(points)==len(set(points))==92 and set(points)==set(evaluated),'exact92 named originals')
    faces=literal['faces'];normals=[];slacks=[];edges={};strict=0;coplanar=0
    for fno,face in enumerate(faces):
        if time.monotonic()>=deadline:raise TimeoutError('named facet audit deadline incomplete')
        require(len(face)==len(set(face))==5 and all(type(k)==int and 0<=k<92 for k in face),'literal pentagon')
        n=M.cross(M.sub(points[face[1]],points[face[0]]),M.sub(points[face[2]],points[face[0]]))
        height=M.dot(n,points[face[0]]);require(height!=Z,'nonzero facet height')
        n=tuple(a/height for a in n);row=[]
        orientation=None
        for first,second in zip(face,face[1:]+face[:1]):
            for third in face:
                if third in (first,second):continue
                turn=sign(M.dot(n,M.cross(M.sub(points[second],points[first]),M.sub(points[third],points[first]))),root)
                require(turn!=0 and (orientation is None or orientation==turn),'strictly convex facet cycle')
                orientation=turn
            edges.setdefault(tuple(sorted((first,second))),[]).append(fno)
        for index,p in enumerate(points):
            gap=1-M.dot(n,p)
            if index in face:require(gap==Z,'exact original facet coplanarity');coplanar+=1
            else:require(sign(gap,root)>0,'strict original facet support');strict+=1
            row.append(gap)
        normals.append(n);slacks.append(row)
    require(len(faces)==60 and len(edges)==150 and all(len(fs)==2 for fs in edges.values()),'complete closed150-edge incidence')
    require(92-150+60==2,'Euler incidence identity')
    reached={0};todo=[0]
    while todo:
        f=todo.pop()
        for adjacent in edges.values():
            if f in adjacent:
                other=next(g for g in adjacent if g!=f)
                if other not in reached:reached.add(other);todo.append(other)
    require(len(reached)==60,'connected closed facet adjacency')
    clauses=[];normal_identities=0;height_identities=0
    basis=tuple(tuple(O if i==j else Z for i in range(3)) for j in range(3))
    for (a,b),adjacent in sorted(edges.items()):
        if time.monotonic()>=deadline:raise TimeoutError('horizon-edge audit deadline incomplete')
        u,v=(normals[f] for f in adjacent);d=M.sub(points[b],points[a]);cross=M.cross(u,v)
        coordinate=next(i for i in range(3) if d[i]!=Z)
        kappa=cross[coordinate]/d[coordinate]
        require(kappa!=Z and cross==tuple(kappa*x for x in d),'two actual facet normals cross parallel actual edge')
        if sign(kappa,root)<0:u,v=v,u;adjacent=adjacent[::-1];kappa=-kappa
        require(sign(kappa,root)>0,'strictly positive horizon orientation coefficient')
        require(all(M.dot(n,p)==O for n in (u,v) for p in (points[a],points[b])),'both original endpoints on both incident facets')
        coefficients=[]
        for r in basis:
            ur,vr=M.dot(u,r),M.dot(v,r)
            normal=tuple(ur*z-vr*y for y,z in zip(u,v))
            require(normal==tuple(kappa*x for x in M.cross(d,r)),'exact common-linear horizon normal identity')
            normal_identities+=1
            require(M.dot(normal,points[a])==ur-vr and M.dot(normal,points[b])==ur-vr,'exact common-linear horizon height identities')
            height_identities+=2
            coefficients.append(normal)
        for direction in (1,-1):
            clauses.append(dict(edge=[a,b],incident_faces=adjacent,direction=direction,
                                u=u,v=v,normal_linear_coefficients=tuple(tuple(direction*x for x in row) for row in coefficients),
                                height_linear_coefficients=tuple(direction*(x-y) for x,y in zip(u,v))))
    require(len(clauses)==300,'all directed actual horizon clauses')
    digest=lambda value:hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    inventory=[dict(edge=c['edge'],incident_faces=c['incident_faces'],direction=c['direction'],
                    u=list(map(encode,c['u'])),v=list(map(encode,c['v'])),
                    normal_coefficients=[list(map(encode,row)) for row in c['normal_linear_coefficients']],
                    height_coefficients=list(map(encode,c['height_linear_coefficients']))) for c in clauses]
    record=dict(agent='six-rupert-1',role='researcher',status='EXACT_COMPLETE_DIRECTED_HORIZON_IDENTITIES_PASSED_FEASIBILITY_OPEN',
                point_count=92,facet_count=60,edge_count=150,directed_horizon_clauses=300,
                source_inequalities_per_active_clause=92,potential_source_inequalities=27600,
                strict_facet_original_comparisons=strict,exact_coplanar_original_comparisons=coplanar,
                strictly_convex_pentagon_turn_comparisons=900,
                horizon_common_linear_vector_identities=normal_identities,
                horizon_endpoint_height_identities=height_identities,
                complete_clause_inventory_sha256=digest(inventory),
                exact_named_point_inventory_sha256=digest([list(map(encode,p)) for p in points]),
                source_dependencies=PINS,
                algebraic_field='Q(phi)[x], phi^2=phi+1, x^3=2x+phi; unique positive root x in(17/10,18/10)',
                active_horizon_clause='direction*(u dot r)>=0, direction*(v dot r)<=0, direction*((u-v) dot r)>0',
                actual_normal='direction*((u dot r)*v-(v dot r)*u); normalized incident outward facets have height1',
                unit_fit_polynomial='(1+c dot c)*h - m dot ((1-c dot c)*P+2*c*(c dot P)+2*c cross P) - m_y*alpha - m_z*beta',
                translation='actual b=pi_r(alpha*e_y+beta*e_z)/(1+c dot c); r_x=1, arbitrary actual b is represented',
                scope='Complete named-solid projection/horizon formulation including grazing facet and collapsed-edge boundaries. It does not decide feasibility, source containment, or global Rupert property.',
                proof_decisions='Exact quotient identities and rational interval signs. Finite-to-continuum normal-cone/support/Cayley arguments are written separately, unformalized and independently unreviewed.')
    return dict(root=root,points=points,normals=normals,facet_slacks=slacks,clauses=clauses,record=record,
                elapsed_seconds=time.monotonic()-started)

def clause_at(clause,raw,root):
    raw=tuple(K.coerce(x) for x in raw);direction=clause['direction']
    ur=direction*M.dot(clause['u'],raw);vr=direction*M.dot(clause['v'],raw)
    if sign(ur,root)<0 or sign(vr,root)>0 or sign(ur-vr,root)<=0:return None
    m=tuple(sum((raw[j]*clause['normal_linear_coefficients'][j][i] for j in range(3)),Z) for i in range(3))
    h=sum((raw[j]*clause['height_linear_coefficients'][j] for j in range(3)),Z)
    require(h==ur-vr and sign(h,root)>0,'actual active support has positive physical height')
    return m,h

def transformed(point,c):
    c=tuple(K.coerce(x) for x in c)
    if all(x==Z for x in c):return tuple(point)
    d=M.dot(c,c);cp=M.dot(c,point);cross=M.cross(c,point)
    return tuple((1-d)*p+2*q*cp+2*z for p,q,z in zip(point,c,cross))

def gap(m,h,point,c,alpha=0,beta=0,scale=1):
    c=tuple(K.coerce(x) for x in c)
    denominator=O if all(x==Z for x in c) else 1+M.dot(c,c)
    value=denominator*h-K.coerce(scale)*M.dot(m,transformed(point,c))
    if alpha:value-=m[1]*K.coerce(alpha)
    if beta:value-=m[2]*K.coerce(beta)
    return value
