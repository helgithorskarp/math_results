#!/usr/bin/env python3
"""Exact centre reconstruction from a complete modular triple superset."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import lcm, comb
from pathlib import Path
import subprocess
import time

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
RAD=[1,3,5,15,11,33,55,165]
ZERO=(0,)*8
ONE=(1,)+(0,)*7


def require(ok, detail):
    if not ok: raise ValueError(detail)


def mul(a,b):
    r=[0]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:r[i^j]+=x*y*RAD[i&j]
    return tuple(r)


def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,k):return tuple(x*k for x in a)


def inverse(a,bit=4):
    require(a!=ZERO,'division by zero')
    if bit==0:
        require(all(x==0 for x in a[1:]),'rational norm')
        return (1/F(a[0]),)+(F(0),)*7
    conjugate=tuple(-x if i&bit else x for i,x in enumerate(a))
    norm=mul(a,conjugate)
    require(all(x==0 for i,x in enumerate(norm) if i&bit),'tower norm')
    return mul(conjugate,inverse(norm,bit//2))


def dist(a,b):
    x,y=sub(a[0],b[0]),sub(a[1],b[1])
    return add(mul(x,x),mul(y,y))


def parse_point(row):return tuple(tuple(F(c) for c in axis) for axis in row)
def dump_point(p):return [[str(c) for c in axis] for axis in p]


def inputs():
    manifest=json.loads((HERE/'manifest.json').read_text())
    for name,digest in manifest['inputs'].items():
        require(sha256((REPO/name).read_bytes()).hexdigest()==digest,('input hash',name))
    old=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json').read_text())
    union=[parse_point(old['coordinates'][str(v)]) for v in old['vertices']]
    labels=[v for v in old['vertices'] if '510' in old['provenance'][v]]
    H=[union[v] for v in labels]
    aligned=json.loads((REPO/'hadwiger_nelson_parts509_heule_union_minimum/aligned_510.json').read_text())
    require(set(H)=={parse_point(row) for row in aligned['aligned_H']},'aligned Heule source agreement')
    require(len(H)==len(set(H))==510 and len(set(union))==553,'source cardinalities')
    scaled=[]
    for point in H:
        row=[96*c for axis in point for c in axis]
        require(all(c.denominator==1 and abs(c)<=144 for c in row),'filter input coefficient bound')
        scaled.append([int(c) for c in row])
    # Parked1111 is only a comparison set, not an enumerated search family.
    pool=json.loads((REPO/'hadwiger_nelson_parts509_swap_closure/completion_points.json').read_text())['points']
    Aextra=[]
    for row in pool:
        q=parse_point([row['x'],row['y']])
        if all(q[a][i]==0 for a in (0,1) for i in (2,3,6,7)) and len(row['neighbors'])>=4:Aextra.append(q)
    ambient=set(union[:509]+Aextra)
    require(len(Aextra)==602 and len(ambient)==1111,'parked ambient definition')
    return H,labels,set(union),ambient,scaled


def circumcentre(a,b,c):
    u=(sub(b[0],a[0]),sub(b[1],a[1])); v=(sub(c[0],a[0]),sub(c[1],a[1]))
    det=sub(mul(u[0],v[1]),mul(u[1],v[0]))
    if det==ZERO:return None
    s=add(mul(u[0],u[0]),mul(u[1],u[1])); t=add(mul(v[0],v[0]),mul(v[1],v[1]))
    inv=scale(inverse(det),F(1,2))
    return (add(a[0],mul(sub(mul(s,v[1]),mul(t,u[1])),inv)),
            add(a[1],mul(sub(mul(t,u[0]),mul(s,v[0])),inv)))


def neighbours(q,H):
    denominator=lcm(96,*(c.denominator for axis in q for c in axis))
    Q=tuple(tuple(int(c*denominator) for c in axis) for axis in q)
    HS=[tuple(tuple(int(c*denominator) for c in axis) for axis in p) for p in H]
    unit=(denominator**2,)+(0,)*7
    return [v for v,p in enumerate(HS) if dist(p,Q)==unit]


def run(work,filter_binary):
    work.mkdir(parents=True,exist_ok=False)
    start=time.monotonic(); H,labels,union,ambient,scaled=inputs()
    raw='510 96\n'+''.join(' '.join(map(str,row))+'\n' for row in scaled)
    (work/'points.txt').write_text(raw)
    (work/'H_labels.json').write_text(json.dumps(labels)+'\n')
    begin=time.monotonic()
    r=subprocess.run([str(filter_binary.resolve()),str(work/'points.txt'),str(work/'survivors.tsv')],capture_output=True,text=True,check=True)
    filtering=json.loads(r.stdout); require(filtering['triples']==comb(510,3),'full triple count')
    (work/'filter.json').write_text(json.dumps(filtering,indent=2)+'\n')
    filter_seconds=time.monotonic()-begin
    pair_centres={}; centres=[]; centre_ids={}; rejected=[]; visited=0
    for line in (work/'survivors.tsv').read_text().splitlines():
        triple=tuple(map(int,line.split())); i,j,k=triple; visited+=1
        if any(k in centres[c]['neighbors'] for c in pair_centres.get((i,j),[])):continue
        q=circumcentre(H[i],H[j],H[k])
        if q is None or dist(H[i],q)!=ONE:
            rejected.append(list(triple));continue
        require(q not in centre_ids,'duplicate centre escaped incidence coverage')
        ns=neighbours(q,H); require(set(triple)<=set(ns),'centre unit radius')
        index=len(centres); centre_ids[q]=index
        centres.append({'coordinates':dump_point(q),'neighbors':ns,'witness':list(triple)})
        for pair in combinations(ns,2):pair_centres.setdefault(pair,[]).append(index)
        if index%250==0:print(json.dumps({'centres':len(centres),'survivors_visited':visited,'seconds':time.monotonic()-start}),flush=True)
    require(visited==filtering['second_survivors'],'survivor coverage')
    # Stable geometric ordering, independent of the first witness triple.
    centres.sort(key=lambda c:parse_point(c['coordinates']))
    (work/'centres.json').write_text(json.dumps(centres,separators=(',',':'))+'\n')
    (work/'rejected.json').write_text(json.dumps(rejected)+'\n')
    full_hist=Counter(); external_hist=Counter(); outside_union_hist=Counter(); fresh_hist=Counter(); fresh=[]
    Hset=set(H)
    for index,row in enumerate(centres):
        q=parse_point(row['coordinates']); degree=len(row['neighbors']);full_hist[degree]+=1
        if q not in Hset:external_hist[degree]+=1
        if q not in union:outside_union_hist[degree]+=1
        if q not in ambient and q not in union:
            fresh_hist[degree]+=1
            if degree>=4:fresh.append({'centre_index':index,**row,'degree':degree})
    accounted=sum(comb(len(row['neighbors']),3) for row in centres)
    require(accounted+len(rejected)==visited,'triple multiplicity coverage')
    summary={'vertices':510,'unit_edges':sum(dist(H[i],H[j])==ONE for i,j in combinations(range(510),2)),
             'centres':len(centres),'full_degree_histogram':dict(sorted(full_hist.items())),
             'external_degree_histogram':dict(sorted(external_hist.items())),
             'outside_closed553_histogram':dict(sorted(outside_union_hist.items())),
             'outside_both553_and1111_histogram':dict(sorted(fresh_hist.items())),
             'fresh_degree_at_least_four':len(fresh),'unit_circle_triples':accounted,'modular_rejections':len(rejected),
             'filter':filtering,'filter_seconds':filter_seconds,'seconds':time.monotonic()-start,
             'centres_sha256':sha256((work/'centres.json').read_bytes()).hexdigest(),
             'survivors_sha256':sha256((work/'survivors.tsv').read_bytes()).hexdigest()}
    (work/'fresh_candidates.json').write_text(json.dumps(fresh,separators=(',',':'))+'\n')
    (work/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--work',type=Path,required=True);ap.add_argument('--filter',type=Path,required=True)
    args=ap.parse_args();run(args.work,args.filter)
