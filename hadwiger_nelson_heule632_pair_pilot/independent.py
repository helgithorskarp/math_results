"""Definition-level geometry and CNF, with no producer import."""
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
RAD=(1,3,5,15,11,33,55,165)


def check(ok,why):
    if not ok:raise ValueError(why)


def point(row):
    check(len(row)==2 and all(len(a)==8 for a in row),'point shape')
    out=[]
    for a in row:
        axis={}
        for rad,c in zip(RAD,a):
            v=96*Fraction(c);check(v.denominator==1,'integral coordinate scale')
            if v:axis[rad]=int(v)
        out.append(axis)
    return out


def norm(p,q):
    coeff={r:0 for r in RAD}
    for a,b in zip(p,q):
        delta={r:a.get(r,0)-b.get(r,0) for r in a.keys()|b.keys()}
        terms=[(r,c) for r,c in sorted(delta.items()) if c]
        for r,c in terms:coeff[1]+=r*c*c
        for (r,c),(s,d) in combinations(terms,2):
            g=gcd(r,s);coeff[r*s//(g*g)]+=2*c*d*g
    return tuple(coeff[r] for r in RAD)


def geometry():
    plan=json.loads((HERE/'plan.json').read_text())
    for path,digest in plan['input_files'].items():check(sha256((REPO/path).read_bytes()).hexdigest()==digest,('input identity',path))
    old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    labels=[v for v in sorted(map(int,old['coordinates'])) if '510' in old['provenance'][v]]
    fresh=json.loads((REPO/'hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json').read_text())
    points=[point(old['coordinates'][str(v)]) for v in labels]+[point(row['coordinates']) for row in fresh]
    check(len(labels)==510 and len(points)==632,'support sizes')
    check(len({tuple(tuple(sorted(a.items())) for a in p) for p in points})==632,'distinct points')
    edges=[]
    for u in range(632):
        for v in range(u+1,632):
            if norm(points[u],points[v])==(9216,0,0,0,0,0,0,0):edges.append((u,v))
    check(len(edges)==3112,'complete exact graph')
    large={v for v in range(510) if all(all(r%5 for r in a) for a in points[v])}
    return points,edges,large


def formula(vertices,edges,k):
    vertices=sorted(vertices);number={v:i for i,v in enumerate(vertices)}
    relevant=[(u,v) for u,v in sorted(edges) if u in number and v in number]
    clauses=[]
    for i in range(len(vertices)):
        names=list(range(k*i+1,k*i+k+1));clauses.append(names)
        clauses.extend([[-a,-b] for a,b in combinations(names,2)])
    for u,v in relevant:
        clauses.extend([[-(k*number[u]+c),-(k*number[v]+c)] for c in range(1,k+1)])
    adjacent={v:set() for v in vertices}
    for u,v in relevant:adjacent[u].add(v);adjacent[v].add(u)
    triangle=[]
    for u in vertices:
        for v,w in combinations(sorted(x for x in adjacent[u] if x>u),2):
            if w in adjacent[v]:triangle=[u,v,w];break
        if triangle:break
    clauses.extend([[k*number[v]+c+1] for c,v in enumerate(triangle)])
    raw=(f'p cnf {len(vertices)*k} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
    return clauses,raw,vertices,triangle


def selection(edges,large):
    prior=json.loads((REPO/'hadwiger_nelson_heule632_transport/result.json').read_text())
    free=set(range(510))-set(prior['valid_old_singleton_cuts']);check(len(free)==488,'pair domain')
    adj={v:set() for v in range(632)}
    for u,v in edges:adj[u].add(v);adj[v].add(u)
    nl=len(free&large);ns=len(free-large)
    counts={'LL':nl*(nl-1)//2,'LS':nl*ns,'SS':ns*(ns-1)//2}
    choices={}
    for kind in ('LL','LS','SS'):
        used=set();rows=[]
        for i in range(8):
            candidates=[]
            for u,v in combinations(sorted(free-used),2):
                actual='LL' if u in large and v in large else 'SS' if u not in large and v not in large else 'LS'
                if actual==kind:candidates.append((len(adj[u])+len(adj[v])-int(v in adj[u]),u,v))
            loss,u,v=min(candidates);used|={u,v}
            _,raw,_,tri=formula(set(range(632))-{u,v},edges,4)
            rows.append({'omitted':[u,v],'stratum':kind,'lost_edges':loss,'unit_edges':3112-loss,'cnf_sha256':sha256(raw).hexdigest(),'cnf_bytes':len(raw),'triangle':tri})
        choices[kind]=rows
    selected=[dict(index=3*i+j,**choices[kind][i]) for i in range(8) for j,kind in enumerate(('LL','LS','SS'))]
    return {'vertices':632,'edges':len(edges),'pair_domain':sum(counts.values()),'stratum_sizes':counts,'selected':selected,
            'edge_sha256':sha256(''.join(f'{u},{v}\n' for u,v in edges).encode('ascii')).hexdigest()}


def colouring(text,omitted,edges,k):
    check(len(text)==632 and set(text)<=set('.'+''.join(map(str,range(k)))),'colour string')
    check([v for v,c in enumerate(text) if c=='.']==omitted,'omission set')
    count=0
    for u,v in edges:
        if text[u]!='.' and text[v]!='.':check(text[u]!=text[v],'strict unit edge');count+=1
    return count
