#!/usr/bin/env python3
"""Exact mixed-neighbour support and transported positive witnesses."""
from hashlib import sha256
import importlib.util
from itertools import combinations,product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
N=514

def load(path):return json.loads(path.read_text())
def need(ok,message):
    if not ok:raise ValueError(message)
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def inputs():
    for name,digest in load(HERE/'manifest.json').items():need(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    C=module('centre_arithmetic',REPO/'hadwiger_nelson_heule510_completion_frontier/census.py')
    H,labels,union,ambient,_=C.inputs()
    large=[i for i,p in enumerate(H) if all(p[a][k]==0 for a in(0,1) for k in(2,3,6,7))];L=set(large)
    pool=load(REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json')
    chosen=[r for r in pool if set(r['neighbors']) & L and set(r['neighbors'])-L]
    need([r['centre_index'] for r in chosen]==[170,436,1239,1527],'complete mixed-neighbour selection')
    pts=H+[C.parse_point(r['coordinates']) for r in chosen]
    need(len(set(pts))==N and all(p not in union and p not in ambient for p in pts[510:]),'new support')
    need(all((96*x).denominator==1 for p in pts for a in p for x in a),'coordinate scale')
    ints=[tuple(tuple(int(96*x) for x in a) for a in p) for p in pts]
    edges=[(u,v) for u,v in combinations(range(N),2) if C.dist(ints[u],ints[v])==(96**2,)+(0,)*7]
    adj=[set() for _ in pts]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    R=module('old_witness_decoder',REPO/'hadwiger_nelson_heule517_large4_review1/independent_check.py')
    old=load(REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json')
    groups=R.witness_data(REPO,old,labels,L,set(range(517))-L)
    source=[(name,i,row,c) for name,rs in groups.items() for i,(row,c) in enumerate(rs)]
    source += [('whole',i,r,r['colouring']) for i,r in enumerate(load(REPO/'hadwiger_nelson_heule517_whole_decision/certificate.json')['rows'])]
    need(len(source)==963,'source colourings')
    return dict(points=pts,edges=edges,adj=adj,large=large,small=sorted(set(range(N))-L),source=source,chosen=chosen)

def check(c,edges):
    need(len(c)==N and set(c)<=set('.0123'),'colour domain')
    need(all(c[u]=='.' or c[v]=='.' or c[u]!=c[v] for u,v in edges),'monochromatic edge')
    return [i for i,x in enumerate(c) if x=='.']

def extend(c,adj,order):
    c=list(c)
    for v in order:
        if c[v]=='.':
            available=set('0123')-{c[u] for u in adj[v]}
            if available:c[v]=min(available)
    return ''.join(c)

def transport(data):
    tails=sorted((''.join(t) for t in product('0123.',repeat=4)),key=lambda s:(s.count('.'),tuple('0123.'.index(x) for x in s)))
    newedges=[e for e in data['edges'] if e[1]>=510];rows=[]
    for source_index,(_,_,row,old_c) in enumerate(data['source']):
        base=old_c[:510]
        for tail in tails:
            c=base+tail
            if all(c[u]=='.' or c[v]=='.' or c[u]!=c[v] for u,v in newedges):break
        else:raise ValueError('empty extension unavailable')
        final=extend(c,data['adj'],data['large']+[v for v in data['small'] if v<510])
        D=check(final,data['edges']);need(D,'unexpected full four-colouring')
        fills=[[v,final[v]] for v in range(510) if final[v]!=base[v]]
        rows.append(dict(kind='transport',source_index=source_index,tail=tail,fills=fills,D=D,colouring=final))
    return rows

def minimal(rows):
    out=[]
    for row in sorted(rows,key=lambda r:(len(r['D']),r['D'])):
        if not any(set(q['D'])<=set(row['D']) for q in out):out.append(row)
    return out

def master(rows):
    P=module('threshold_encoder',REPO/'hadwiger_nelson_heule517_family_pilot/engine.py')
    n,c=P.atleast(N,6);c += [[-v-1 for v in r['D']] for r in rows];return n,c

def graph_cnf(vertices,edges,k=4):
    pos={v:i for i,v in enumerate(vertices)};c=[[k*i+j+1 for j in range(k)] for i in range(len(vertices))]
    c += [[-k*pos[u]-j-1,-k*pos[v]-j-1] for u,v in edges if u in pos and v in pos for j in range(k)]
    if 0 in pos:c.append([k*pos[0]+1])
    return k*len(vertices),c

def activated(edges):
    offset=4*N+1;c=[[-offset-v]+[4*v+j+1 for j in range(4)] for v in range(N)]
    c += [[-4*u-j-1,-4*v-j-1] for u,v in edges for j in range(4)];c.append([-offset,1]);return 5*N,c

def raw(n,c):return (f'p cnf {n} {len(c)}\n'+''.join(' '.join(map(str,x))+' 0\n' for x in c)).encode()
