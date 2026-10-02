"""Complete all-k notch suppliers and a necessary E1 side-contact restriction.

Point alignment enumerates suppliers independently of the raw-contact atlas.
Every candidate covering N has a unique source column and source height v.
Forbidden v/b intervals are exact column-overlap conditions.
"""

import deps
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import resource,signal,time

from strip_columns import MATRICES,require,literal_cells
from strip_parametric_geometry import COLS,add,sub,scale,constant,value,atom,both,evaluate,partition

HERE=Path(__file__).absolute().parent
OPS=deps.OPS
N=((0,-1),(1,-1))


def notch_forbidden(matrix, source_column):
    alpha,beta,gamma,delta=matrix
    rows=[]
    for c,lo,hi in COLS:
        for d,L,H in COLS:
            if beta:
                n=d+1-alpha*(c-source_column)
                if n%beta:continue
                C=n//beta
                image_v=add(N[1],constant(gamma*(c-source_column)+delta*C))
                active=both(atom('ge',sub(image_v,L)),atom('ge',sub(H,image_v)))
                rows.append((sub(lo,constant(C)),add(sub(hi,constant(C)),constant(1)),active))
            elif d==-1+alpha*(c-source_column):
                offset=add(N[1],constant(gamma*(c-source_column)))
                if delta==1:
                    first=add(sub(offset,H),lo);last=add(sub(offset,L),hi)
                else:
                    first=add(sub(L,offset),lo);last=add(sub(H,offset),hi)
                rows.append((first,add(last,constant(1)),True))
    return tuple(rows)


def parameter_partition(systems):
    atoms=[]
    for s in systems:
        endpoints={s['lo'],s['hi']}
        for lo,hi,active in s['forbidden']:
            endpoints.update((lo,hi));atoms.append(active)
        e=sorted(endpoints)
        for j,x in enumerate(e):
            for y in e[:j]:atoms.extend((atom('ge',sub(x,y)),atom('ge',sub(y,x))))
    return partition(atoms)


def allowed_intervals(s,k):
    endpoint={s['lo'],s['hi']}
    for lo,hi,_ in s['forbidden']:endpoint.update((lo,hi))
    e=sorted(endpoint,key=lambda x:(value(x,k),x));out=[]
    for lo,hi in zip(e,e[1:]):
        if value(lo,k)==value(hi,k):continue
        v=value(lo,k)
        if not value(s['lo'],k)<=v<value(s['hi'],k):continue
        if any(evaluate(active,k) and value(a,k)<=v<value(b,k) for a,b,active in s['forbidden']):continue
        out.append((lo,hi))
    return out


def all_notch_suppliers():
    systems=[{'matrix':m,'column':c,'lo':lo,'hi':add(hi,constant(1)),
              'forbidden':notch_forbidden(m,c)} for m in MATRICES for c,lo,hi in COLS]
    part=parameter_partition(systems);classes=[]
    for interval in part['intervals']:
        require(len(interval['representatives'])==1,'Unexpected period')
        k=interval['representatives'][0];atlas=[]
        for s in systems:
            for lo,hi in allowed_intervals(s,k):
                require(sub(hi,lo)==(0,1),'Supplier family is not a single affine pose')
                alpha,beta,gamma,delta=s['matrix'];c=s['column']
                atlas.append((s['matrix'],sub(constant(-1-alpha*c),scale(beta,lo)),
                              sub(sub(N[1],constant(gamma*c)),scale(delta,lo))))
        require(len(set(atlas))==len(atlas),'Duplicate notch supplier')
        classes.append({**interval,'atlas':sorted(atlas)})
    return systems,part,classes


def translated_supplier_forbidden(g, a_shift=6):
    """b is variable in g_b+b. Return b-intervals of overlap with root."""
    (alpha,beta,gamma,delta),a,b=g;a=add(a,constant(a_shift));rows=[]
    for c,lo,hi in COLS:
        for d,L,H in COLS:
            if beta:
                numerator=sub(constant(d-alpha*c),a)
                require(numerator[0]%beta==0,'Nonconstant divisibility case')
                if numerator[1]%beta:continue
                v=(numerator[0]//beta,numerator[1]//beta)
                active=both(atom('ge',sub(v,lo)),atom('ge',sub(hi,v)))
                offset=add(add(constant(gamma*c),scale(delta,v)),b)
                first=sub(L,offset);last=sub(H,offset)
            else:
                active=atom('eq',add(a,constant(alpha*c-d)))
                min_v,max_v=(lo,hi) if delta==1 else (scale(-1,hi),scale(-1,lo))
                first=sub(sub(sub(L,constant(gamma*c)),b),max_v)
                last=sub(sub(sub(H,constant(gamma*c)),b),min_v)
            rows.append((first,add(last,constant(1)),active))
    return tuple(rows)


def side_restriction(atlas):
    # Exact raw domain: I;(6,b), 3-k <= b <= 3.
    systems=[{'supplier':g,'lo':(-1,3),'hi':(0,4),
              'forbidden':translated_supplier_forbidden(g)} for g in atlas]
    part=parameter_partition(systems);classes=[]
    for interval in part['intervals']:
        k=interval['representatives'][0]
        classes.append({**interval,'surviving_supplier_intervals':[
            {'supplier':s['supplier'],'allowed_b':allowed_intervals(s,k)} for s in systems]})
    return systems,part,classes


def material_suppliers(k):
    tile=literal_cells(k);point=(-1,k-1);out=set()
    for m in MATRICES:
        a,b,c,d=m
        for x,y in tile:
            u,v=point[0]-a*x-b*y,point[1]-c*x-d*y
            image={(a*i+b*j+u,c*i+d*j+v) for i,j in tile}
            if not tile&image:out.add((m,(u,v)))
    return out


def main():
    start=time.monotonic()
    def guard():
        require(not deps.paused(),
                'Operational pause barrier; unfinished result inconclusive')
        require(time.monotonic()-start<43,'43s guard; unfinished result inconclusive')
    def alarm(signum,frame):raise RuntimeError('45s guard; unfinished result inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    systems,part,classes=all_notch_suppliers();guard()
    require(len(classes)==1 and len(classes[0]['atlas'])==9,'Expected one all-k nine-supplier atlas not proved')
    side_systems,side_part,side_classes=side_restriction(classes[0]['atlas']);guard()
    samples=[]
    for k in [6,7,8,9,12,20]:
        guard();atlas=classes[0]['atlas']
        generated={(m,(value(a,k),value(b,k))) for m,a,b in atlas}
        require(generated==material_suppliers(k),'Materialized notch inventory disagrees')
        tile=literal_cells(k);side=next(x for x in side_classes if x['lo']<=k and (x['hi'] is None or k<=x['hi']))
        permissible=set()
        for row in side['surviving_supplier_intervals']:
            permissible.update(v for lo,hi in row['allowed_b'] for v in range(value(lo,k),value(hi,k)))
        found=set()
        for b0 in range(3-k,4):
            for m,(u,v) in generated:
                a,b,c,d=m
                new={(a*x+b*y+u+6,c*x+d*y+v+b0) for x,y in tile}
                if not tile&new:found.add(b0)
        require(found==permissible,'Materialized side-filter disagrees')
        samples.append({'k':k,'notch_suppliers':len(generated),'permissible_side_shifts':sorted(found)})
    signal.alarm(0)
    result={'agent':'six-heesch-2','role':'researcher','scope':'All k>=6 notch suppliers and necessary E1 side condition only; no full E2 inclusion',
            'notch_partition':part,'notch_systems':systems,'notch_classes':classes,
            'side_partition':side_part,'side_systems':side_systems,'side_classes':side_classes,'samples':samples,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'seconds':round(time.monotonic()-start,3),'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    mode='normal' if __debug__ else 'optimized'
    (HERE/'strip-contact-domain'/f'notch-intervals-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['scope','notch_partition','notch_classes','side_partition','side_classes','samples','seconds','max_rss_kib']},sort_keys=True),flush=True)


if __name__=='__main__':main()
