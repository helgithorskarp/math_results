"""Search-free paired-atlas reader; independent materialized geometry audit."""
from copy import deepcopy
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
from strip_parametric_reader import E,axial,literal,sha
H=Path(__file__).absolute().parent
OPS=Path(os.environ["DISCOVERY_RESEARCH_TEAM_ROOT"]) if os.environ.get("DISCOVERY_RESEARCH_TEAM_ROOT") else None
def read(p):return json.loads(p.read_text())
def setup(record):
    atlas=[G.pose(p) for p in record['poses']]
    atlas.extend([((-1,0,-1,1),(0,-5),(0,-3)),((-1,0,-1,1),(0,-5),(0,-2))])
    fixed=[((1,0,0,1),(0,0),(0,0)),atlas[-1]]
    require(G.inverse(atlas[-1])==atlas[-2] and all(G.inverse(p) in atlas for p in atlas),'Inverse closure fails')
    pool=sorted(set(atlas+[G.compose(fixed[1],p) for p in atlas]))
    points=[((0,u),(1,v)) for u,v in ((-8,-3),(-5,-1),(-4,-2),(-2,0),(3,2),(4,2))]
    points.extend([((0,-7),(0,-3)),((0,-1),(0,-1))])
    return atlas,fixed,pool,points
def reconstruct(record,guard):
    atlas,fixed,pool,points=setup(record);cover=[];eligible=[];bad={};halo=[]
    for p in pool:
        guard();cover.append([G.point_membership(p,q) for q in points])
        eligible.append(G.both(*(G.neg(G.conflict(f,p,atlas)) for f in fixed)))
    for i in range(len(pool)):
        guard()
        for j in range(i):bad[i,j]=G.conflict(pool[i],pool[j],atlas)
    for q in points:
        inside=G.either(*(G.point_membership(f,q) for f in fixed))
        around=G.either(*(G.point_membership(f,(G.sub(q[0],G.constant(du)),
            G.sub(q[1],G.constant(dv)))) for f in fixed for du,dv in G.UV_DIRS))
        halo.append(G.both(G.neg(inside),around))
    predicates=[p for group in cover for p in group]+eligible+halo+list(bad.values())
    atomset=G.atoms(predicates);cuts={6};period=1
    for row in atomset:
        kind,A,B,*mod=row
        if kind=='mod':require(mod==[3],'Unexpected modulus');period=3
        elif kind=='ge':
            change=(-B+A-1)//A if A>0 else (-B)//A+1
            if change>6:cuts.add(change)
        elif kind=='eq':
            point,remainder=divmod(-B,A)
            if not remainder and point>=6:cuts.update((point,point+1))
        else:raise ValueError('Unknown atomic predicate')
    ordered=sorted(cuts);intervals=[];reps=[];samples=[]
    for i,lo in enumerate(ordered):
        hi=ordered[i+1]-1 if i+1<len(ordered) else None
        ks=[lo+(r-lo)%period for r in range(period)];ks=[k for k in ks if hi is None or k<=hi]
        intervals.append({'lo':lo,'hi':hi,'representatives':ks});reps.extend(ks)
    split={'minimum':6,'period':period,'cuts':ordered,'intervals':intervals,
           'representatives':reps,'atomic_predicates':len(atomset)}
    n=len(pool);relax={'cover':[0]*n,'conflicts':[(1<<n)-1]*n,'available':0}
    for k in reps:
        guard();require(all(G.evaluate(p,k) for p in halo),'Demand outside fixed union halo')
        mask=[sum(1<<j for j,p in enumerate(group) if G.evaluate(p,k)) for group in cover]
        clash=[1<<i for i in range(n)]
        for (i,j),p in bad.items():
            if G.evaluate(p,k):clash[i]|=1<<j;clash[j]|=1<<i
        avail=sum(1<<i for i in range(n) if mask[i] and G.evaluate(eligible[i],k))
        matrix={'cover':mask,'conflicts':clash,'available':avail};samples.append({'k':k,'matrix':matrix})
        relax['available']|=avail
        for i in range(n):relax['cover'][i]|=mask[i];relax['conflicts'][i]&=clash[i]
    return atlas,fixed,pool,points,split,samples,relax

def numerical(k,atlas,fixed,pool,points):
    tile=literal(k);domain={E.affine(tile,axial(p,k)) for p in atlas}
    F=[E.affine(tile,axial(f,k)) for f in fixed];motions=[axial(p,k) for p in pool]
    tiles=[E.affine(tile,g) for g in motions]
    direct=domain|{E.affine(t,axial(fixed[1],k)) for t in domain}
    require(set(tiles)==direct and len(set(tiles))==len(pool),'Incomplete materialized pool')
    occupied=set().union(*map(set,F));qs=[(G.value(u,k)-2*G.value(v,k),G.value(v,k)) for u,v in points]
    require(set(qs)<=E.halo(occupied),'Numerical demand not halo')
    mask=[sum(1<<j for j,q in enumerate(qs) if q in t) for t in tiles]
    elig=[]
    for t in tiles:
        good=occupied.isdisjoint(t)
        for f,g in zip(F,fixed):
            if E.touching(t,f) and E.affine(t,E.inverse(axial(g,k))) not in domain:good=False
        elig.append(good)
    n=len(pool);clash=[1<<i for i in range(n)]
    for i,t in enumerate(tiles):
        for j,s in enumerate(tiles[:i]):
            bad=not set(t).isdisjoint(s)
            if not bad and E.touching(t,s):
                bad=E.affine(s,E.inverse(motions[i])) not in domain or E.affine(t,E.inverse(motions[j])) not in domain
            if bad:clash[i]|=1<<j;clash[j]|=1<<i
    matrix={'cover':mask,'conflicts':clash,'available':sum(1<<i for i in range(n) if mask[i] and elig[i])}
    return matrix,domain,F

def dag(proof,matrix):
    require(proof['rejected'] and proof['root']==[hex(matrix['available']),hex(255)],'Wrong rejection root')
    nodes=[(int(a,16),int(r,16),j) for a,r,j in proof['nodes']]
    require(len({(a,r) for a,r,j in nodes})==len(nodes),'Duplicate state')
    cov=matrix['cover'];clash=matrix['conflicts'];initial=matrix['available']
    suppliers=[sum(1<<i for i,c in enumerate(cov) if c>>j&1) for j in range(8)];valid=set()
    for available,remaining,j in sorted(nodes,key=lambda row:(row[1].bit_count(),row)):
        require(available>=0 and not available&~initial and 0<remaining<=255 and
                type(j) is int and 0<=j<8 and remaining>>j&1,'Invalid proof state')
        choices=available&suppliers[j]
        while choices:
            bit=choices&-choices;choices^=bit;i=bit.bit_length()-1
            require((available&~clash[i],remaining&~cov[i]) in valid,'Missing exhaustive child')
        valid.add((available,remaining))
    require((initial,255) in valid,'Root not certified')
    return len(nodes)
def verify(cert,record,split,samples,relax):
    require(cert['complete'] and cert['atlas_sha256']==sha(record),'Changed atlas input')
    require(cert['partition']==split and cert['samples']==samples and
            cert['conservative_universal_matrix']==relax,'Changed exact reconstruction')
    return dag(cert['universal_rejection'],relax)

def main():
    start=time.monotonic();mode='normal' if __debug__ else 'optimized'
    record=read(H/'strip-parametric/atlas.json');cert=read(H/'strip-parametric/pair-certificate-normal.json')
    other=read(H/'strip-parametric/pair-certificate-optimized.json')
    for k in ('complete','atlas_sha256','partition','domain_size','pool_size','demands','samples','conservative_universal_matrix','universal_rejection','source_hashes'):
        require(cert[k]==other[k],'Producer modes disagree')
    for name,digest in cert['source_hashes'].items():require(hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,'Producer source changed')
    def guard():
        if OPS is not None and any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json')):raise RuntimeError('Pause barrier')
        if time.monotonic()-start>=43:raise RuntimeError('43s guard; incomplete, no negative')
    def alarm(signum,frame):raise RuntimeError('45s guard; incomplete, no negative')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    try:
        atlas,fixed,pool,points,split,samples,relax=reconstruct(record,guard)
        nodes=verify(cert,record,split,samples,relax)
        for row in samples:
            guard();matrix,domain,F=numerical(row['k'],atlas,fixed,pool,points)
            require(matrix==row['matrix'],'Symbolic/numerical mismatch')
        damages=[]
        missing=deepcopy(cert);missing['partition']['cuts'].remove(10);damages.append(missing)
        altered=deepcopy(cert);altered['conservative_universal_matrix']['available']^=1;damages.append(altered)
        broken=deepcopy(cert);broken['universal_rejection']['nodes'].pop(0);damages.append(broken)
        count=0
        for bad in damages:
            try:verify(bad,record,split,samples,relax)
            except ValueError:count+=1
            else:raise ValueError('Damaged certificate accepted')
        evidence={'complete':True,'atlas_sha256':sha(record),'domain_size':len(atlas),'pool_size':len(pool),
            'breakpoints':split['cuts'],'period':split['period'],'representatives':split['representatives'],
            'atomic_predicates':split['atomic_predicates'],'DAG_nodes':nodes,'damaged_controls':count,
            'matrix_sha256':sha(relax),'source_hashes':{str(p.relative_to(H.parent)):hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (Path(__file__).absolute(),H/'strip_parametric_reader.py',H/'strip_parametric_geometry.py',H/'strip_columns.py',H.parent/'strip-t5/exact.py')},
            'proof_status':'Search-free reader; shared symbolic kernel plus separate materialized geometry; author checked, unformalized, independently unreviewed',
            'scope':'Conditional all-k pair obstruction, k>=6; no all-k E2 inclusion is established'}
        out={'agent':'six-heesch-2','role':'researcher','checked_utc':datetime.now(timezone.utc).isoformat(),
            'evidence':evidence,'evidence_sha256':sha(evidence),'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        (H/f'strip-parametric/pair-reader-{mode}.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
    finally:signal.alarm(0)

if __name__=='__main__':main()
