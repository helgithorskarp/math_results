#!/usr/bin/env python3
"""Exact H632 geometry, deterministic pair selection and direct colour CNF."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
RAD=(1,3,5,15,11,33,55,165)
INPUTS=('hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json',
        'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json',
        'hadwiger_nelson_heule632_transport/result.json')


def need(ok,why):
    if not ok:raise ValueError(why)


def point(row):
    need(len(row)==2 and all(len(axis)==8 for axis in row),'coordinate shape')
    q=[[96*Fraction(x) for x in axis] for axis in row]
    need(all(x.denominator==1 for axis in q for x in axis),'coordinate denominator')
    return tuple(tuple(int(x) for x in axis) for axis in q)


def norm(p,q):
    ans=[0]*8
    for axis in range(2):
        d=[(i,a-b) for i,(a,b) in enumerate(zip(p[axis],q[axis])) if a!=b]
        for i,a in d:
            for j,b in d:ans[i^j]+=a*b*RAD[i&j]
    return tuple(ans)


def geometry():
    old=json.loads((REPO/INPUTS[0]).read_text())
    labels=[v for v in range(553) if '510' in old['provenance'][v]]
    fresh=json.loads((REPO/INPUTS[1]).read_text())
    points=[point(old['coordinates'][str(v)]) for v in labels]+[point(row['coordinates']) for row in fresh]
    need(len(labels)==510 and len(points)==len(set(points))==632,'fixed support')
    need([r['centre_index'] for r in fresh]==sorted({r['centre_index'] for r in fresh}),'fresh order')
    edges=[(u,v) for u,v in combinations(range(632),2) if norm(points[u],points[v])==(9216,0,0,0,0,0,0,0)]
    need(len(edges)==3112,'full unit graph')
    large={v for v in range(510) if all(points[v][a][j]==0 for a in (0,1) for j in (2,3,6,7))}
    need(len(large)==375,'old large block')
    return points,edges,large


def pairs(edges,large):
    forbidden=set(json.loads((REPO/INPUTS[2]).read_text())['valid_old_singleton_cuts'])
    need(len(forbidden)==22,'known cuts')
    free=sorted(set(range(510))-forbidden);degree=[0]*632;edge_set=set(edges)
    for u,v in edges:degree[u]+=1;degree[v]+=1
    buckets={kind:[] for kind in ('LL','LS','SS')}
    for u,v in combinations(free,2):
        kind='LL' if u in large and v in large else 'SS' if u not in large and v not in large else 'LS'
        loss=degree[u]+degree[v]-int((u,v) in edge_set)
        buckets[kind].append((loss,u,v))
    chosen={}
    for kind,rows in buckets.items():
        used=set();selected=[]
        for loss,u,v in sorted(rows):
            if u in used or v in used:continue
            selected.append({'omitted':[u,v],'stratum':kind,'lost_edges':loss,'unit_edges':3112-loss})
            used.update((u,v))
            if len(selected)==8:break
        need(len(selected)==8,'eight disjoint pairs per stratum');chosen[kind]=selected
    selected=[dict(index=3*i+j,**chosen[kind][i]) for i in range(8) for j,kind in enumerate(('LL','LS','SS'))]
    return selected,{kind:len(rows) for kind,rows in buckets.items()}


def formula(vertices,edges,k):
    vertices=sorted(vertices);positions={v:i for i,v in enumerate(vertices)}
    es=sorted((u,v) for u,v in edges if u in positions and v in positions)
    need(k>=3,'palette size')
    var=lambda v,c:k*positions[v]+c+1
    clauses=[]
    for v in vertices:
        clauses.append([var(v,c) for c in range(k)])
        for a,b in combinations(range(k),2):clauses.append([-var(v,a),-var(v,b)])
    for u,v in es:
        for c in range(k):clauses.append([-var(u,c),-var(v,c)])
    adj={v:set() for v in vertices}
    for u,v in es:adj[u].add(v);adj[v].add(u)
    triangle=next(((u,v,w) for u,v in es for w in sorted(adj[u]&adj[v]) if w>v),())
    for c,v in enumerate(triangle):clauses.append([var(v,c)])
    raw=(f'p cnf {k*len(vertices)} {len(clauses)}\n'+''.join(' '.join(map(str,cl))+' 0\n' for cl in clauses)).encode('ascii')
    return clauses,raw,vertices,list(triangle)


def decode(log,vertices,k,clauses):
    values={}
    for line in log.splitlines():
        if line.startswith('v '):
            for x in map(int,line.split()[1:]):
                if x:
                    need(abs(x) not in values or values[abs(x)]==(x>0),'model consistency')
                    values[abs(x)]=x>0
    need(set(values)==set(range(1,k*len(vertices)+1)),'complete model')
    for clause in clauses:need(any(values[abs(x)]==(x>0) for x in clause),'model clause')
    answer={}
    for i,v in enumerate(vertices):
        colours=[c for c in range(k) if values[k*i+c+1]];need(len(colours)==1,'one colour per vertex');answer[v]=colours[0]
    return answer


def check_colouring(answer,vertices,edges,k):
    need(set(answer)==set(vertices),'exact retained vertices')
    need(all(type(c) is int and 0<=c<k for c in answer.values()),'colour domain')
    checks=0
    for u,v in edges:
        if u in answer and v in answer:need(answer[u]!=answer[v],'unit edge');checks+=1
    return checks


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    points,edges,large=geometry();selected,counts=pairs(edges,large);args.out.mkdir(parents=True,exist_ok=True)
    for row in selected:
        _,raw,_,triangle=formula(set(range(632))-set(row['omitted']),edges,4)
        row.update(cnf_sha256=sha256(raw).hexdigest(),cnf_bytes=len(raw),triangle=triangle)
    raw=''.join(f'{u},{v}\n' for u,v in edges).encode('ascii')
    report={'vertices':632,'edges':len(edges),'pair_domain':sum(counts.values()),'stratum_sizes':counts,'selected':selected,'edge_sha256':sha256(raw).hexdigest()}
    (args.out/'preparation.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,indent=2))
