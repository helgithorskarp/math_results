#!/usr/bin/env python3
"""Exact Heule517 graph, inherited witnesses and omission master."""
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
CENTRES=[327,439,671,1040,1074,1377,1383]


def require(ok,detail):
    if not ok:raise ValueError(detail)


def geometry():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input identity',name))
    path=REPO/'hadwiger_nelson_heule510_completion_frontier/census.py'
    spec=importlib.util.spec_from_file_location('exact_census_data',path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    H,labels,union,ambient,_=mod.inputs()
    pool=json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    seven=[r for r in pool if r['degree']>=7]
    require([r['centre_index'] for r in seven]==CENTRES,'whole degree stratum')
    points=H+[mod.parse_point(row['coordinates']) for row in seven]
    require(len(points)==len(set(points))==517,'graph support')
    require(all((96*c).denominator==1 for p in points for axis in p for c in axis),'integer scale')
    ints=[tuple(tuple(int(96*c) for c in axis) for axis in p) for p in points]
    edges=[(u,v) for u,v in combinations(range(517),2) if mod.dist(ints[u],ints[v])==(96**2,)+(0,)*7]
    require(len(edges)==2555 and sum(v<510 for u,v in edges)==2504,'unit graph')
    require(not any(u>=510 for u,v in edges),'added vertices independent')
    adj=[set() for _ in points]
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    return dict(points=points,labels=labels,edges=edges,adj=adj,old=old)


def check_colouring(colours,edges):
    require(len(colours)==517 and set(colours)<=set('.0123'),'colour domain')
    require(all(colours[u]=='.' or colours[v]=='.' or colours[u]!=colours[v] for u,v in edges),'monochromatic unit edge')
    return tuple(v for v,c in enumerate(colours) if c=='.')


def extend(colours,adj,order):
    colours=list(colours)
    for v in order:
        if colours[v]!='.':continue
        available=set('0123')-{colours[u] for u in adj[v]}
        if available:colours[v]=min(available)
    return ''.join(colours)


def inherited(data):
    old=data['old'];rows=[]
    sources=[('forced',u,[u],old['forced_witness'][str(u)]) for u in old['forced']]
    sources += [('family',i,row['D'],row['witness']) for i,row in enumerate(old['family'])]
    require(len(sources)==830,'source row count')
    for kind,index,deleted,colouring in sources:
        retained=sorted(set(range(553))-set(deleted))
        require(len(colouring)==len(retained) and set(colouring)<=set('0123'),'inherited row format')
        cmap=dict(zip(retained,colouring))
        base=''.join(cmap.get(v,'.') for v in data['labels'])+'.'*7
        base=extend(base,data['adj'],range(510,517))
        D=check_colouring(base,data['edges'])
        rows.append(dict(D=list(D),source=kind,index=index,extra=base[510:]))
    return rows


def decode(row,data):
    if row['source']=='native':return row['colouring']
    old=data['old']
    if row['source']=='forced':D=[row['index']];text=old['forced_witness'][str(row['index'])]
    else:
        require(row['source']=='family','source kind')
        source=old['family'][row['index']];D=source['D'];text=source['witness']
    cmap=dict(zip(sorted(set(range(553))-set(D)),text))
    return ''.join(cmap.get(v,'.') for v in data['labels'])+row['extra']


def minimal(rows):
    selected=[]
    for row in sorted(rows,key=lambda r:(len(r['D']),r['D'])):
        D=set(row['D'])
        if not any(set(s['D'])<=D for s in selected):selected.append(row)
    return selected


def atleast(n,bound):
    """Backward threshold implications: final prefix true iff enough inputs."""
    require(0<=bound<=n,'cardinality bound')
    clauses=[];variables=n;prefix={}
    for i in range(1,n+1):
        for j in range(1,min(i,bound)+1):
            variables+=1;prefix[i,j]=variables
            old=prefix.get((i-1,j))
            clauses.append([-variables]+([old] if old else [])+[i])
            if j>1:clauses.append([-variables]+([old] if old else [])+[prefix[i-1,j-1]])
    if bound:clauses.append([prefix[n,bound]])
    return variables,clauses


def master(rows):
    variables,clauses=atleast(517,9)
    clauses += [[-v-1 for v in row['D']] for row in rows]
    return variables,clauses


def dimacs(variables,clauses):
    return (f'p cnf {variables} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()


def activated(edges):
    col=lambda v,c:4*v+c+1
    clauses=[[-(2069+v)]+[col(v,c) for c in range(4)] for v in range(517)]
    clauses += [[-col(u,c),-col(v,c)] for u,v in edges for c in range(4)]
    clauses += [[-2069,1]]
    return 2585,clauses


def graph_cnf(vertices,edges,k=4):
    pos={v:i for i,v in enumerate(vertices)};col=lambda v,c:k*pos[v]+c+1
    clauses=[[col(v,c) for c in range(k)] for v in vertices]
    clauses += [[-col(u,c),-col(v,c)] for u,v in edges if u in pos and v in pos for c in range(k)]
    if 0 in pos:clauses += [[col(0,0)]]
    return k*len(vertices),clauses
