"""Conditional pair obstruction for the affine32 strip atlas."""
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import time

import strip_parametric_geometry as G
from strip_columns import require
H=Path(__file__).absolute().parent
OPS=Path(os.environ["DISCOVERY_RESEARCH_TEAM_ROOT"]) if os.environ.get("DISCOVERY_RESEARCH_TEAM_ROOT") else None
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def data(record):
    D=tuple(G.pose(p) for p in record['poses'])+(
        ((-1,0,-1,1),(0,-5),(0,-3)),((-1,0,-1,1),(0,-5),(0,-2)))
    I=((1,0,0,1),(0,0),(0,0));M=D[-1]
    require(G.inverse(M)==D[-2] and all(G.inverse(g) in D for g in D),'Atlas inverse closure fails')
    pool=tuple(sorted(set(D+tuple(G.compose(M,g) for g in D))))
    points=tuple(((0,u),(1,v)) for u,v in ((-8,-3),(-5,-1),(-4,-2),(-2,0),(3,2),(4,2)))
    points+=(((0,-7),(0,-3)),((0,-1),(0,-1)))
    return D,(I,M),pool,points
def build(D,fixed,pool,points,guard=lambda:None):
    coverage=[];eligible=[];conflicts={};demands=[]
    for g in pool:
        guard();coverage.append([G.point_membership(g,p) for p in points])
        eligible.append(G.both(*(G.neg(G.conflict(f,g,D)) for f in fixed)))
    for i,g in enumerate(pool):
        guard()
        for j,h in enumerate(pool[:i]):conflicts[i,j]=G.conflict(g,h,D)
    for p in points:
        interior=G.either(*(G.point_membership(f,p) for f in fixed))
        neighbor=G.either(*(G.point_membership(f,(G.sub(p[0],G.constant(du)),
            G.sub(p[1],G.constant(dv)))) for f in fixed for du,dv in G.UV_DIRS))
        demands.append(G.both(G.neg(interior),neighbor))
    fs=[f for row in coverage for f in row]+eligible+demands+list(conflicts.values())
    return coverage,eligible,conflicts,demands,fs
def matrix(k,coverage,eligible,conflicts):
    n=len(coverage);cover=[sum(1<<j for j,f in enumerate(row) if G.evaluate(f,k)) for row in coverage]
    clash=[1<<i for i in range(n)]
    for (i,j),f in conflicts.items():
        if G.evaluate(f,k):clash[i]|=1<<j;clash[j]|=1<<i
    av=sum(1<<i for i in range(n) if cover[i] and G.evaluate(eligible[i],k))
    return {'cover':cover,'conflicts':clash,'available':av}
def reject(m,guard):
    npoints=8;full=(1<<npoints)-1;cover=m['cover'];clash=m['conflicts'];failed={};count=[0]
    at=[sum(1<<i for i,c in enumerate(cover) if c>>j&1) for j in range(npoints)]
    def visit(av,rem):
        guard();count[0]+=1;require(count[0]<=100000,'100000-node guard; no negative')
        if not rem:return False
        if (av,rem) in failed:return True
        j=min((j for j in range(npoints) if rem>>j&1),key=lambda j:(at[j]&av).bit_count())
        choices=at[j]&av
        while choices:
            bit=choices&-choices;choices^=bit;i=bit.bit_length()-1
            if not visit(av&~clash[i],rem&~cover[i]):return False
        failed[av,rem]=j;return True
    good=visit(m['available'],full)
    return {'rejected':good,'root':[hex(m['available']),hex(full)],'visited':count[0],
            'nodes':[[hex(a),hex(r),j] for (a,r),j in sorted(failed.items())] if good else []}
def main():
    start=time.monotonic();mode='normal' if __debug__ else 'optimized'
    record=json.loads((H/'strip-parametric/atlas.json').read_text());result={'agent':'six-heesch-2','role':'researcher','complete':False}
    def guard():
        if OPS is not None and any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json')):raise RuntimeError('Pause barrier')
        if time.monotonic()-start>=43:raise RuntimeError('43s guard; incomplete, no negative')
    def alarm(signum,frame):raise RuntimeError('45s guard; incomplete, no negative')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    try:
        D,fixed,pool,points=data(record);cov,elig,conflicts,demands,fs=build(D,fixed,pool,points,guard)
        split=G.partition(fs,6);samples=[]
        for k in split['representatives']:
            guard();require(all(G.evaluate(f,k) for f in demands),'Demand outside union halo')
            samples.append({'k':k,'matrix':matrix(k,cov,elig,conflicts)})
        n=len(pool);relax={'cover':[0]*n,'conflicts':[(1<<n)-1]*n,'available':0}
        for row in samples:
            m=row['matrix'];relax['available']|=m['available']
            for i in range(n):relax['cover'][i]|=m['cover'][i];relax['conflicts'][i]&=m['conflicts'][i]
        proof=reject(relax,guard)
        result.update(complete=proof['rejected'],atlas_sha256=sha(record),partition=split,
            domain_size=len(D),pool_size=len(pool),demands=points,samples=samples,
            conservative_universal_matrix=relax,universal_rejection=proof,
            source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (Path(__file__).absolute(),H/'strip_parametric_geometry.py',H/'strip_columns.py')},
            scope='All k>=6 conditional affine32 mutual pair-cover obstruction for M=(-1,0,-1,1;-5,-2); no all-k E2 necessity asserted')
    finally:
        signal.alarm(0);result.update(checked_utc=datetime.now(timezone.utc).isoformat(),
            seconds=round(time.monotonic()-start,3),max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (H/f'strip-parametric/pair-certificate-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result.get(k) for k in ('agent','role','complete','domain_size','pool_size','seconds','max_rss_kib')}|
        {'cuts':result.get('partition',{}).get('cuts'),'period':result.get('partition',{}).get('period'),
         'DAG_nodes':len(result.get('universal_rejection',{}).get('nodes',[]))},sort_keys=True))

if __name__=='__main__':main()
