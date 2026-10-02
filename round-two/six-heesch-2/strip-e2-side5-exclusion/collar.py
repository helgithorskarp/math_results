"""Exact all-k inventories along the finite-guided lower endpoint branches."""
from datetime import datetime,timezone
import json
from pathlib import Path
import resource
import signal
import time

import matrices as F
import strip_contact_reader as R
from known_e1 import known_bad

H=Path(__file__).resolve().parent
I=F.IDENTITY
G=((1,0,0,1),(0,5),(-1,2))
B=((-1,0,0,-1),(0,2),(0,1))
S=((2,-3,1,-2),(0,2),(0,1))
D=((-1,0,0,-1),(0,4),(0,1))
PLANS=(
    ('root', (I,G), ((0,2),(0,1)), (B,S)),
    ('halfturn_dead', (I,G,B), ((0,3),(-1,2)), ()),
    ('angle_forces_D', (I,G,S), ((0,4),(0,1)), (D,)),
)


def main():
    (H/'generated').mkdir(exist_ok=True)
    start=time.monotonic();ops=[0]
    def guard():
        ops[0]+=1
        if F.deps.paused() or time.monotonic()-start>=43 or ops[0]>100000:
            raise RuntimeError('Operational/time/work guard; incomplete, no negative')
    def alarm(a,b):raise RuntimeError('45s signal guard; incomplete, no negative')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    receipts=[json.loads((H/'generated'/f'core-{mode}.json').read_text())
              for mode in ['normal','optimized']]
    if not all(r['complete'] for r in receipts) or receipts[0]['mathematics_sha256']!=receipts[1]['mathematics_sha256']:
        raise ValueError('This pass Q cut is not checked')
    F.known_bad=known_bad
    out=[]
    for name,fixed,point,expected in PLANS:
        guard();supplier=F.finite_suppliers(point,fixed)
        if not supplier['finite']:raise RuntimeError('Growing source heights; no all-k force')
        if R.freeze(supplier)!=R.freeze(R.supplier_atlas(point,fixed,guard)):
            raise ValueError('Supplier reducers differ')
        atlas=R.freeze(supplier['atlas'])
        predicates=[F.G.both(F.G.point_membership(h,point),
            *(F.G.neg(F.G.intersection(F.G.relative(f,h))) for f in fixed),
            *(F.G.neg(known_bad(F.G.relative(f,h))) for f in fixed)) for h in atlas]
        demand=F.G.both(F.G.neg(F.G.either(*(F.G.point_membership(f,point) for f in fixed))),
            F.G.either(*(F.G.point_membership(f,(F.G.sub(point[0],(0,u)),F.G.sub(point[1],(0,v))))
                        for f in fixed[:2] for u,v in F.G.UV_DIRS)))
        part=F.G.partition(predicates+[demand])
        if part!=R.splitter(predicates+[demand]):raise ValueError('Partitions differ')
        samples=[]
        for k in part['representatives']:
            if not F.G.evaluate(demand,k):raise ValueError('Demand is not an original unfilled pair-halo cell')
            actual={h for h,p in zip(atlas,predicates) if F.G.evaluate(p,k)}
            want={(m,(0,F.G.value(a,k)),(0,F.G.value(b,k))) for m,a,b in expected}
            literal={(m,(0,F.G.value(a,k)),(0,F.G.value(b,k))) for m,a,b in actual}
            samples.append({'k':k,'eligible':sorted(actual),'expected':expected,
                            'agrees':literal==want})
        record={'name':name,'fixed':fixed,'point':point,'complete_suppliers':supplier,
            'eligibility':predicates,'demand':demand,'partition':part,
            'samples':samples,'uniform_expected':all(s['agrees'] for s in samples)}
        out.append(record)
        print(json.dumps({'name':name,'raw_suppliers':len(atlas),'partition':part,
                          'uniform_expected':record['uniform_expected'],'samples':samples},sort_keys=True),flush=True)
        if not record['uniform_expected']:break
    # Complete literal10-cell collar under the forced S,D prefix.
    checks=[]
    if all(r['uniform_expected'] for r in out) and len(out)==3:
        fixed=(I,G,S,D)
        points=(((0,-1),(0,0)),((0,-2),(0,-1)),((0,-2),(0,0)),
            ((0,-2),(0,1)),((0,-1),(0,1)),((0,4),(0,3)),
            ((0,4),(0,4)),((0,5),(0,3)),((0,6),(0,3)),
            ((0,7),(-1,3)))
        records=[]
        for p in points:
            guard();s=F.finite_suppliers(p,fixed)
            checks.append({'point':p,'finite':s['finite'],
                'atlas':s.get('atlas'), 'growing_example':s.get('example')})
            if not s['finite']:raise RuntimeError('Growing source family; no rejection')
            if R.freeze(s)!=R.freeze(R.supplier_atlas(p,fixed,guard)):
                raise ValueError('Collar supplier reducers differ')
            records.append((p,s))
        atlas=sorted(set().union(*(set(s['atlas']) for p,s in records)))
        if len(atlas)<=128:
            F.FIXED=fixed;F.POINTS=tuple(p for p,s in records)
            result=F.matrices(atlas,guard,True)
            collar={'fixed':fixed,'points':F.POINTS,'supplier_records':[s for p,s in records],
                'atlas':atlas,'known_E1':result}
            print(json.dumps({'collar_suppliers':len(atlas),'all_k_rejected':result['complete_rejection'],
                'universal_rejected':result['proof']['rejected'],
                'samples':[(s['k'],s['proof']['rejected'],s['proof']['visited']) for s in result['samples']]}),flush=True)
        else:collar={'status':'128-affine-pose guard, no rejection','atlas_length':len(atlas)}
    else:collar=None
    math={'uniform_steps':out,'finite_width_checks':checks,'collar':collar}
    mode='normal' if __debug__ else 'optimized'
    result={'agent':'six-heesch-2','role':'researcher','evidence':math,
        'mathematics_sha256':R.sha(math),'seconds':round(time.monotonic()-start,3),
        'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'scope':'All-k force/exclusion only at uniform_expected stages; collar '
            'only when complete_rejection holds; no global Heesch conclusion.',
        'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated'/f'collar-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({'mathematics_sha256':result['mathematics_sha256'],
        'seconds':result['seconds'],'max_rss_kib':result['max_rss_kib']}),flush=True)


if __name__=='__main__':main()
