"""Exact finite collars and the S-branch forced-neighbor certificate."""
from datetime import datetime,timezone
import json
from pathlib import Path
import resource
import signal
import time

import deps
import reader as V
import strip_contact_reader as R
import strip_local_pair_certificate as C
import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import IDENTITY,finite_suppliers
import supplier_trees as T

HERE=Path(__file__).absolute().parent
g=((1,0,0,1),(0,6),(-1,4))
r=((-1,0,0,-1),(0,5),(0,3))
s=((-1,0,-1,1),(0,7),(0,5))
a=((-1,3,0,1),(-3,2),(0,2))
j=((1,-3,0,-1),(0,0),(1,1))
m=((1,0,1,-1),(0,-4),(1,-2))
POINTS=(((0,3),(1,2)),((0,-2),(1,0)),((0,-3),(1,-2)),((0,1),(0,0)))


def finite(entry,guard):
    fixed=(IDENTITY,R.freeze(entry['pose']));points=R.freeze(entry['points'])
    suppliers=[finite_suppliers(p,fixed) for p in points]
    require(all(x['finite'] for x in suppliers),'Growing supplier family retained')
    atlas=sorted(set().union(*(set(x['atlas']) for x in suppliers)))
    require(len(atlas)<=128,'128-pose guard; no rejection')
    partition,samples,universal=C.matrices(fixed,atlas,points,guard)
    proof=C.cover_certificate(universal,len(points),guard)
    require(proof['rejected'],'Conservative collar has a cover; no exclusion')
    return {'agent':'six-heesch-2','role':'researcher','case':entry['name'],'method':'finite',
            'fixed':fixed,'points':points,'supplier_records':suppliers,'atlas':atlas,
            'partition':partition,'samples':samples,'universal':universal,'proof':proof,'complete':True}


def transport(candidate,fixed,entries):
    for index,anchor in enumerate(fixed):
        relative=G.relative(anchor,candidate)
        for entry in entries:
            pose=R.freeze(entry['pose'])
            for inverse,target in ((False,pose),(True,G.inverse(pose))):
                if relative==target:
                    return {'candidate':candidate,'anchor_index':index,'case':entry['name'],'inverse':inverse}
    raise ValueError('No proved literal contact excludes this supplier')


def chain(entries,guard):
    fixed=(IDENTITY,g,r,s);expected=(a,j,m,None);models=tuple(R.freeze(e['pose']) for e in entries)
    def bad(relative):
        return G.both(G.touching(relative),G.either(G.allowed(relative,models),
                                                   G.allowed(G.inverse(relative),models)))
    stages=[]
    for point,chosen in zip(POINTS,expected):
        guard();suppliers=finite_suppliers(point,fixed)
        require(suppliers['finite'],'Growing chain supplier family retained')
        atlas=R.freeze(suppliers['atlas'])
        eligible=[G.both(G.point_membership(c,point),
                         *[G.neg(G.intersection(G.relative(f,c))) for f in fixed],
                         *[G.neg(bad(G.relative(f,c))) for f in fixed]) for c in atlas]
        demanded=G.both(V.in_halo(point,fixed[:2]),
                       G.neg(G.either(*(G.point_membership(f,point) for f in fixed))))
        partition=G.partition(eligible+[demanded]);samples=[]
        for k in partition['representatives']:
            guard();require(G.evaluate(demanded,k),'Not an original unfilled pair-halo demand')
            allowed=[c for c,row in zip(atlas,eligible) if G.evaluate(row,k)]
            require(set(allowed)==({chosen} if chosen is not None else set()),'Chain is not uniformly forced')
            samples.append({'k':k,'eligible':allowed})
        mappings=[transport(c,fixed,entries) for c in atlas if c!=chosen]
        stages.append({'fixed':fixed,'point':point,'supplier_record':suppliers,'partition':partition,
                       'samples':samples,'expected':chosen,'mappings':mappings})
        if chosen is not None:fixed=(*fixed,chosen)
    return {'agent':'six-heesch-2','role':'researcher','stages':stages,'complete':True,
            'scope':'S cannot occur in a registered E2 halo cover of (I;6,4-k), for all k>=6'}


def main():
    start=time.monotonic();calls=0
    def guard():
        nonlocal calls
        calls+=1
        if deps.paused() or time.monotonic()-start>=43 or calls>100000:
            raise RuntimeError('Operational/43s/100000-operation guard; incomplete work inconclusive')
    def alarm(x,y):raise RuntimeError('45s signal guard; incomplete work inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    inputs=json.loads((HERE/'inputs.json').read_text());entries=inputs['cases']
    mode='normal' if __debug__ else 'optimized';folder=HERE/'generated'/mode;folder.mkdir(parents=True,exist_ok=True)
    hashes=[]
    for entry in entries:
        guard()
        if entry['method']=='finite':record=finite(entry,guard)
        else:
            fixed=(IDENTITY,R.freeze(entry['pose']))
            record={'agent':'six-heesch-2','role':'researcher','case':entry['name'],'method':'tree',
                    'fixed':fixed,'points':entry['points'],
                    'tree':T.build(T.freeze_plan(entry['plan']),fixed,guard),'complete':True}
        (folder/f"{entry['name']}.json").write_text(json.dumps(record,indent=1)+'\n')
        hashes.append([entry['name'],R.sha(record)])
    stages=chain(entries,guard)
    (folder/'chain.json').write_text(json.dumps(stages,indent=1)+'\n')
    math={'case_hashes':hashes,'chain_sha256':R.sha(stages)}
    signal.alarm(0)
    out={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':math,
         'mathematics_sha256':R.sha(math),'seconds':round(time.monotonic()-start,3),
         'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'checked_utc':datetime.now(timezone.utc).isoformat()}
    (folder/'generator-summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='evidence'}),flush=True)


if __name__=='__main__':main()
