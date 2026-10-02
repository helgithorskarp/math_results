"""Search-free reader; shared symbolic kernel, independent materialized audit.

No producer or search is imported. Reconstruct the exact breakpoint partition,
all finite matrices, their conservative relaxation, and every DAG branch.
"""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import importlib.util
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
spec=importlib.util.spec_from_file_location('parametric_materialized_exact',H.parent/'strip-t5/exact.py')
E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
def read(p):return json.loads(p.read_text())
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def rebuild(record,guard):
    ps=[G.pose(row) for row in record['poses']]
    qs=[(tuple(row['u']),tuple(row['v'])) for row in record['halo_demands']]
    require(len(ps)==30 and len(qs)==7 and len(set(ps))==30,'Wrong literal atlas')
    identity=((1,0,0,1),(0,0),(0,0));cov=[];bad={};root=[];halo=[]
    for g in ps:
        guard();cov.append([G.point_membership(g,q) for q in qs]);root.append(G.intersection(g))
    for i in range(30):
        guard()
        for j in range(i):bad[i,j]=G.conflict(ps[i],ps[j],ps)
    for q in qs:
        adjacent=[G.point_membership(identity,(G.sub(q[0],G.constant(du)),
            G.sub(q[1],G.constant(dv)))) for du,dv in G.UV_DIRS]
        halo.append(G.both(G.neg(G.point_membership(identity,q)),G.either(*adjacent)))
    fs=[f for row in cov for f in row]+root+halo+list(bad.values())
    atoms=G.atoms(fs);cuts={6};period=1
    for a in atoms:
        kind,slope,offset,*mod=a
        if kind=='mod':require(mod==[3],'Unexpected period');period=3
        elif kind=='ge':
            change=(-offset+slope-1)//slope if slope>0 else (-offset)//slope+1
            if change>6:cuts.add(change)
        elif kind=='eq':
            point,remainder=divmod(-offset,slope)
            if remainder==0 and point>=6:cuts.update((point,point+1))
        else:raise ValueError('Unknown atom')
    ordered=sorted(cuts);intervals=[];reps=[]
    for index,lo in enumerate(ordered):
        hi=ordered[index+1]-1 if index+1<len(ordered) else None
        samples=[lo+((r-lo)%period) for r in range(period)]
        samples=[k for k in samples if hi is None or k<=hi]
        reps.extend(samples);intervals.append({'lo':lo,'hi':hi,'representatives':samples})
    split={'minimum':6,'period':period,'cuts':ordered,'intervals':intervals,
           'representatives':reps,'atomic_predicates':len(atoms)}
    matrices=[]
    for k in reps:
        guard();require(all(G.evaluate(f,k) for f in halo),'Required point is not open halo')
        cover=[sum(1<<j for j,f in enumerate(row) if G.evaluate(f,k)) for row in cov]
        conflicts=[1<<i for i in range(30)]
        for (i,j),f in bad.items():
            if G.evaluate(f,k):conflicts[i]|=1<<j;conflicts[j]|=1<<i
        available=sum(1<<i for i in range(30) if cover[i] and not G.evaluate(root[i],k))
        matrices.append({'k':k,'matrix':{'cover':cover,'conflicts':conflicts,'available':available}})
    relaxation={'cover':[0]*30,'conflicts':[(1<<30)-1]*30,'available':0}
    for row in matrices:
        m=row['matrix'];relaxation['available']|=m['available']
        for i in range(30):
            relaxation['cover'][i]|=m['cover'][i]
            relaxation['conflicts'][i]&=m['conflicts'][i]
    return ps,qs,split,matrices,relaxation

def axial(g,k):
    (a,b,c,d),u,v=g;x,y=G.value(u,k),G.value(v,k)
    m=(a-2*c,2*a+b-4*c-2*d,c,2*c+d)
    require(m in E.matrices(),'Nonrigid atlas motion')
    return m+(x-2*y,y)
def literal(k):
    cells={(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):
        for x in (-2*r-1,-2*r-2):
            for y in (r+1,r+2):cells.add((x,y))
    return tuple(sorted(cells))

def materialized(k,ps,qs):
    tile=literal(k);motions=[axial(g,k) for g in ps];tiles=[E.affine(tile,g) for g in motions]
    domain=set(tiles);root=set(tile);points=[(G.value(u,k)-2*G.value(v,k),G.value(v,k)) for u,v in qs]
    require(set(points)<=E.halo(tile),'Materialized point outside halo')
    require(len(domain)==30 and all(E.frame(tile,t)==g for t,g in zip(tiles,motions)),
            'Ambiguous representative frame')
    cover=[sum(1<<j for j,q in enumerate(points) if q in t) for t in tiles]
    available=sum(1<<i for i,t in enumerate(tiles) if cover[i] and root.isdisjoint(t))
    conflicts=[1<<i for i in range(30)]
    for i,t in enumerate(tiles):
        for j,s in enumerate(tiles[:i]):
            bad=not set(t).isdisjoint(s)
            if not bad and E.touching(t,s):
                bad=E.affine(s,E.inverse(motions[i])) not in domain or E.affine(t,E.inverse(motions[j])) not in domain
            if bad:conflicts[i]|=1<<j;conflicts[j]|=1<<i
    return {'cover':cover,'conflicts':conflicts,'available':available},tiles

def check_dag(proof,matrix):
    require(proof['rejected'] and not proof.get('incomplete',False),'Not a rejection')
    cov=matrix['cover'];clash=matrix['conflicts'];start=matrix['available']
    require(proof['root']==[hex(start),hex(127)],'Changed DAG root')
    nodes=[(int(a,16),int(r,16),j) for a,r,j in proof['nodes']]
    require(len({(a,r) for a,r,j in nodes})==len(nodes),'Repeated state')
    at=[sum(1<<i for i,c in enumerate(cov) if c>>j&1) for j in range(7)];valid=set()
    for available,remaining,j in sorted(nodes,key=lambda x:(x[1].bit_count(),x)):
        require(available>=0 and not available&~start and 0<remaining<=127 and
                type(j) is int and 0<=j<7 and remaining>>j&1,'Invalid DAG state')
        choices=at[j]&available
        while choices:
            bit=choices&-choices;choices^=bit;i=bit.bit_length()-1
            child=available&~clash[i],remaining&~cov[i]
            require(child in valid,'Missing exhaustive child')
        valid.add((available,remaining))
    require((start,127) in valid,'No complete root rejection')
    return len(nodes)

def verify_package(cert,atlas_sha,split,matrices,relaxation):
    require(cert['complete'] and cert['atlas_sha256']==atlas_sha,'Atlas binding changed')
    require(cert['partition']==split and cert['samples']==matrices,'Breakpoint partition or matrices changed')
    require(cert['conservative_universal_matrix']==relaxation,'Invalid conservative relaxation')
    return check_dag(cert['universal_rejection'],relaxation)

def main():
    start=time.monotonic();mode='normal' if __debug__ else 'optimized'
    record=read(H/'strip-parametric/atlas.json');cert=read(H/'strip-parametric/certificate-normal.json')
    other=read(H/'strip-parametric/certificate-optimized.json')
    for key in ('complete','atlas_sha256','partition','samples','conservative_universal_matrix','universal_rejection','source_hashes'):
        require(cert[key]==other[key],'Producer modes disagree')
    for name,digest in cert['source_hashes'].items():
        require(hashlib.sha256((H/name).read_bytes()).hexdigest()==digest,'Producer source changed')
    def guard():
        if OPS is not None and any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json')):raise RuntimeError('Pause barrier')
        if time.monotonic()-start>=43:raise RuntimeError('43s guard; incomplete, no negative')
    def alarm(signum,frame):raise RuntimeError('45s guard; incomplete, no negative')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    try:
        ps,qs,split,matrices,relaxation=rebuild(record,guard)
        atlas_sha=sha(record);nodes=verify_package(cert,atlas_sha,split,matrices,relaxation)
        for row in matrices:
            guard();actual,tiles=materialized(row['k'],ps,qs)
            require(actual==row['matrix'],'Symbolic geometry disagrees with materialized sets')
        damages=[]
        missing=deepcopy(cert);missing['partition']['cuts'].remove(7);damages.append(missing)
        altered=deepcopy(cert);altered['conservative_universal_matrix']['cover'][0]^=1;damages.append(altered)
        broken=deepcopy(cert);broken['universal_rejection']['nodes'].pop(0);damages.append(broken)
        rejected=0
        for bad in damages:
            try:verify_package(bad,atlas_sha,split,matrices,relaxation)
            except ValueError:rejected+=1
            else:raise ValueError('Damaged certificate accepted')
        evidence={'complete':True,'atlas_sha256':atlas_sha,'breakpoints':split['cuts'],'period':split['period'],
            'representatives':split['representatives'],'atomic_predicates':split['atomic_predicates'],
            'DAG_nodes':nodes,'damaged_controls':rejected,'matrix_sha256':sha(relaxation),
            'source_hashes':{str(p.relative_to(H.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (Path(__file__).absolute(),H/'strip_parametric_geometry.py',H/'strip_columns.py',H.parent/'strip-t5/exact.py')},
            'proof_status':'Search-free reader, shared symbolic kernel and separate materialized geometry audit; author checked, unformalized, independently unreviewed',
            'scope':'Conditional all k>=6 root obstruction for literal affine30 atlas; no all-k necessity or global Heesch upper established'}
        out={'agent':'six-heesch-2','role':'researcher','checked_utc':datetime.now(timezone.utc).isoformat(),
            'evidence':evidence,'evidence_sha256':sha(evidence),'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
        (H/f'strip-parametric/reader-{mode}.json').write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps(out,sort_keys=True),flush=True)
    finally:signal.alarm(0)

if __name__=='__main__':main()
