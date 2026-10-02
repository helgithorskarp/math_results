"""Exact rectangle description of raw contacts of the literal T_k, k>=6.

This is a contact-domain reduction, not an E1/E2 support or Heesch bound.
Affine endpoints are (coefficient of k, constant), intervals are half-open.
"""

import deps
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import resource
import signal
import time

from strip_columns import MATRICES, UV_DIRS, require
from strip_parametric_geometry import COLS, add, sub, scale, constant, value, atom, partition

HERE = Path(__file__).absolute().parent
OPS=deps.OPS


def halo_columns_unmerged():
    return tuple((c+du,add(lo,constant(dv)),add(hi,constant(dv)))
                 for du,dv in ((0,0),)+UV_DIRS for c,lo,hi in COLS)


def nonparallel_rectangles(matrix, residue, target):
    alpha,beta,gamma,delta = matrix
    require(abs(beta)==3 and residue in range(3), 'Invalid residue system')
    sign = 1 if beta>0 else -1
    rectangles = set()
    for c,lo,hi in COLS:
        for d,L,H in target:
            n=d-alpha*c-residue
            if n%3:
                continue
            C=n//beta
            if sign==1:
                first,last=sub(constant(C),hi),sub(constant(C),lo)
            else:
                first,last=sub(lo,constant(C)),sub(hi,constant(C))
            zlo=sub(L,constant(gamma*c+delta*C))
            zhi=sub(H,constant(gamma*c+delta*C))
            rectangles.add((first,add(last,constant(1)),zlo,add(zhi,constant(1))))
    return tuple(sorted(rectangles))


def parallel_intervals(matrix, translation, target):
    alpha,beta,gamma,delta=matrix
    require(beta==0 and abs(delta)==1, 'Invalid parallel system')
    result=set()
    for c,lo,hi in COLS:
        image_lo,image_hi=(lo,hi) if delta==1 else (scale(-1,hi),scale(-1,lo))
        for d,L,H in target:
            if d-alpha*c!=translation:
                continue
            first=sub(sub(L,constant(gamma*c)),image_hi)
            last=sub(sub(H,constant(gamma*c)),image_lo)
            result.add((first,add(last,constant(1))))
    return tuple(sorted(result))


def systems():
    closed=halo_columns_unmerged(); result=[]
    for matrix in MATRICES:
        if matrix[1]:
            for r in range(3):
                result.append({'matrix':matrix,'type':'nonparallel','residue':r,
                    'root':nonparallel_rectangles(matrix,r,COLS),
                    'closed':nonparallel_rectangles(matrix,r,closed)})
        else:
            translations=sorted({d-matrix[0]*c for c,_,_ in COLS for d,_,_ in closed})
            for a in translations:
                result.append({'matrix':matrix,'type':'parallel','a':a,
                    'root':parallel_intervals(matrix,a,COLS),
                    'closed':parallel_intervals(matrix,a,closed)})
    return result


def boundaries(system, axis):
    offset=2*axis
    return sorted({q for rectangle in system['root']+system['closed']
                   for q in rectangle[offset:offset+2]})


def order_atoms(all_systems):
    rows=[]
    for s in all_systems:
        for axis in range(2 if s['type']=='nonparallel' else 1):
            e=boundaries(s,axis)
            for i,x in enumerate(e):
                for y in e[:i]:
                    rows.extend((atom('ge',sub(x,y)),atom('ge',sub(y,x))))
    return rows


def ordered_boundaries(system, axis, k):
    # Structural tie-breaking is constant throughout the parameter class.
    return sorted(boundaries(system,axis),key=lambda x:(value(x,k),x))


def inside(point, rectangles, k):
    return any(all(value(r[2*j],k)<=x<value(r[2*j+1],k)
                   for j,x in enumerate(point)) for r in rectangles)


def selected_rectangles(system,k):
    axes=[ordered_boundaries(system,j,k) for j in
          range(2 if system['type']=='nonparallel' else 1)]
    selected=[]
    if len(axes)==1:
        for lo,hi in zip(axes[0],axes[0][1:]):
            if value(lo,k)==value(hi,k):continue
            point=(value(lo,k),)
            if inside(point,system['closed'],k) and not inside(point,system['root'],k):
                selected.append((lo,hi))
    else:
        for lo,hi in zip(axes[0],axes[0][1:]):
            if value(lo,k)==value(hi,k):continue
            for low,high in zip(axes[1],axes[1][1:]):
                if value(low,k)==value(high,k):continue
                point=(value(lo,k),value(low,k))
                if inside(point,system['closed'],k) and not inside(point,system['root'],k):
                    selected.append((lo,hi,low,high))
    return selected


def cardinal_polynomial(rectangles):
    # Exact coefficients in increasing degree, no fitting from samples.
    out=[0,0,0]
    for r in rectangles:
        A,B=sub(r[1],r[0])
        if len(r)==2:out[0]+=B;out[1]+=A
        else:
            C,D=sub(r[3],r[2]);out[0]+=B*D;out[1]+=A*D+B*C;out[2]+=A*C
    return out


def poses(system, rectangles, k):
    m=system['matrix'];out=set()
    if system['type']=='parallel':
        for lo,hi in rectangles:
            for b in range(value(lo,k),value(hi,k)):
                out.add(m+(system['a'],b))
    else:
        sign=1 if m[1]>0 else -1
        for lo,hi,low,high in rectangles:
            for t in range(value(lo,k),value(hi,k)):
                for z in range(value(low,k),value(high,k)):
                    out.add(m+(3*t+system['residue'],m[3]*sign*t+z))
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--sample',type=int,action='append')
    args=parser.parse_args();start=time.monotonic()
    def guard():
        require(not deps.paused(),
                'Operational pause barrier')
        require(time.monotonic()-start<43,'43s work guard; unfinished reduction inconclusive')
    def alarm(signum,frame):raise RuntimeError('45s signal guard; unfinished reduction inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    all_systems=systems();part=partition(order_atoms(all_systems));guard()
    classes=[]
    for interval in part['intervals']:
        guard();require(len(interval['representatives'])==1,'Unexpected nontrivial period')
        k=interval['representatives'][0];records=[];total=[0,0,0];by_matrix={}
        for s in all_systems:
            guard();rect=selected_rectangles(s,k);poly=cardinal_polynomial(rect)
            for j,n in enumerate(poly):total[j]+=n
            m=str(s['matrix']);by_matrix.setdefault(m,[0,0,0])
            for j,n in enumerate(poly):by_matrix[m][j]+=n
            records.append({**s,'selected':rect,'cardinality':poly})
        classes.append({**interval,'systems':records,'cardinality':total,'by_matrix':by_matrix,
                        'selected_rectangles':sum(len(r['selected']) for r in records)})
    samples=[]
    for k in args.sample or [6,7,8]:
        guard();require(k>=6,'Sample outside stated domain')
        cls=next(x for x in classes if x['lo']<=k and (x['hi'] is None or k<=x['hi']))
        ps=set().union(*(poses(s,s['selected'],k) for s in cls['systems']))
        require(len(ps)==sum(n*k**j for j,n in enumerate(cls['cardinality'])), 'Non-disjoint rectangles')
        samples.append({'k':k,'poses':len(ps),'pose_sha256':hashlib.sha256(json.dumps(sorted(ps)).encode()).hexdigest()})
    guard();signal.alarm(0)
    d={'agent':'six-heesch-2','role':'researcher','scope':'All-k raw registered contact domain only; no E1/E2 inclusion or Heesch upper',
       'partition':part,'classes':classes,'samples':samples,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
       'checked_utc':datetime.now(timezone.utc).isoformat(),'seconds':round(time.monotonic()-start,3),
       'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    out=HERE/'strip-contact-domain';out.mkdir(exist_ok=True)
    mode='normal' if __debug__ else 'optimized'
    (out/f'produced-{mode}.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({'partition':part,'classes':[{k:v for k,v in x.items() if k not in ['systems','by_matrix']} for x in classes],
                      'samples':samples,'seconds':d['seconds'],'max_rss_kib':d['max_rss_kib']},sort_keys=True),flush=True)


if __name__=='__main__':main()
