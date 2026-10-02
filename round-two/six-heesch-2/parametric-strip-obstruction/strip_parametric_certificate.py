"""Finite breakpoint reduction and conservative universal seven-cell DAG."""
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

def formulas(record,guard=lambda:None):
    atlas=tuple(G.pose(row) for row in record['poses'])
    points=tuple((tuple(row['u']),tuple(row['v'])) for row in record['halo_demands'])
    identity=((1,0,0,1),(0,0),(0,0));coverage=[];conflicts={};roots=[];demands=[]
    for g in atlas:
        guard();require(g[0] in G.MATRICES,'Wrong atlas matrix')
        coverage.append([G.point_membership(g,p) for p in points])
        roots.append(G.intersection(g))
    for point in points:
        root=G.point_membership(identity,point)
        neighbor=G.either(*(G.point_membership(identity,(G.sub(point[0],G.constant(du)),
            G.sub(point[1],G.constant(dv)))) for du,dv in G.UV_DIRS))
        demands.append(G.both(G.neg(root),neighbor))
    for i,g in enumerate(atlas):
        guard()
        for j,h in enumerate(atlas[:i]):conflicts[i,j]=G.conflict(g,h,atlas)
    rows=[r for group in coverage for r in group]+list(conflicts.values())+roots+demands
    return atlas,points,coverage,conflicts,roots,demands,rows

def matrix_at(k,coverage,conflicts,roots):
    n=len(coverage);cover=[sum(1<<j for j,r in enumerate(row) if G.evaluate(r,k)) for row in coverage]
    clash=[1<<i for i in range(n)]
    available=sum(1<<i for i in range(n) if cover[i] and not G.evaluate(roots[i],k))
    for (i,j),row in conflicts.items():
        if G.evaluate(row,k):clash[i]|=1<<j;clash[j]|=1<<i
    return {'cover':cover,'conflicts':clash,'available':available}

def rejection(cover,conflicts,available,guard=lambda:None):
    failed={};counter=[0]
    at=[sum(1<<i for i,c in enumerate(cover) if c>>j&1) for j in range(7)]
    def visit(av,remaining):
        guard();counter[0]+=1;require(counter[0]<=100000,'100000-node guard; incomplete, no negative')
        if not remaining:return False
        if (av,remaining) in failed:return True
        j=min((j for j in range(7) if remaining>>j&1),key=lambda j:(at[j]&av).bit_count())
        choices=at[j]&av
        while choices:
            bit=choices&-choices;choices^=bit;i=bit.bit_length()-1
            if not visit(av&~conflicts[i],remaining&~cover[i]):return False
        failed[av,remaining]=j;return True
    complete=visit(available,127)
    return {'rejected':complete,'visited':counter[0],'root':[hex(available),hex(127)],
            'nodes':[[hex(a),hex(r),j] for (a,r),j in sorted(failed.items())] if complete else []}

def main():
    start=time.monotonic();path=H/'strip-parametric/atlas.json';record=json.loads(path.read_text())
    mode='normal' if __debug__ else 'optimized';result={'agent':'six-heesch-2','role':'researcher','complete':False}
    def guard():
        if OPS is not None and any((OPS/n).exists() for n in ('PAUSED','PAUSED.json','HANDOVER.json')):raise RuntimeError('Pause barrier')
        if time.monotonic()-start>=43:raise RuntimeError('43s guard; incomplete, no negative')
    def alarm(signum,frame):raise RuntimeError('45s guard; incomplete, no negative')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    try:
        atlas,points,coverage,conflicts,roots,demands,rows=formulas(record,guard)
        require(len(atlas)==30 and len(points)==7,'Changed atlas size')
        split=G.partition(rows,6);samples=[]
        for k in split['representatives']:
            guard();require(all(G.evaluate(r,k) for r in demands),'A required point is outside the open root halo')
            samples.append({'k':k,'matrix':matrix_at(k,coverage,conflicts,roots)})
        union_cover=[0]*30;universal_conflicts=[(1<<30)-1]*30;union_available=0
        for row in samples:
            m=row['matrix'];union_available|=m['available']
            for i in range(30):union_cover[i]|=m['cover'][i];universal_conflicts[i]&=m['conflicts'][i]
        relaxation={'cover':union_cover,'conflicts':universal_conflicts,'available':union_available}
        proof=rejection(**relaxation,guard=guard)
        individual=[]
        if not proof['rejected']:
            for row in samples:
                guard();individual.append({'k':row['k'],'proof':rejection(**row['matrix'],guard=guard)})
        complete=proof['rejected'] or all(r['proof']['rejected'] for r in individual)
        result.update(complete=complete,atlas_sha256=sha(record),partition=split,samples=samples,
            conservative_universal_matrix=relaxation,universal_rejection=proof,individual_rejections=individual,
            source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                (Path(__file__).absolute(),H/'strip_parametric_geometry.py',H/'strip_columns.py')},
            claim='Conditional: all k>=6 lack a mutually atlas-admissible complete root surround. The atlas is an explicit definition. No all-k necessity or unconditional global Heesch upper is proved.',
            proof_status='Private author checked, unformalized, independently unreviewed; no finite-five or uniform global Heesch upper')
    finally:
        signal.alarm(0);result.update(checked_utc=datetime.now(timezone.utc).isoformat(),
            seconds=round(time.monotonic()-start,3),max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        (H/f'strip-parametric/certificate-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('agent','role','complete','seconds','max_rss_kib')}|
        {'cuts':result.get('partition',{}).get('cuts'),'period':result.get('partition',{}).get('period'),
         'samples':len(result.get('samples',[])),'universal_DAG_nodes':len(result.get('universal_rejection',{}).get('nodes',[]))},sort_keys=True))

if __name__=='__main__':main()
