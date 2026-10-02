"""Universal finite collar obstruction with complete point-supplier reduction.

An atlas is derived from point alignment, not assumed from finite samples.
Packing-only conflicts suffice to reject an E1 pair-halo cover when successful.
"""

import deps
import argparse
from datetime import datetime,timezone
import hashlib,json
from pathlib import Path
import resource,signal,time

import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import finite_suppliers,IDENTITY

HERE=Path(__file__).absolute().parent
OPS=deps.OPS
ANGLE=((2,-3,1,-2),(0,5),(0,3))
ANGLE_POINTS=(((-3,6),(-2,4)),((0,-3),(0,-2)),((0,-1),(1,-1)),
              ((0,-1),(0,0)),((0,4),(0,3)),((0,-2),(0,-1)))


def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def matrices(fixed,atlas,points,guard):
    coverage=[];eligible=[];clash={};demand=[]
    for h in atlas:
        guard();coverage.append([G.point_membership(h,p) for p in points])
        eligible.append(G.both(*(G.neg(G.intersection(G.relative(g,h))) for g in fixed)))
    for j,h in enumerate(atlas):
        guard()
        for i,g in enumerate(atlas[:j]):clash[i,j]=G.intersection(G.relative(g,h))
    for p in points:
        occupied=G.either(*(G.point_membership(g,p) for g in fixed))
        adjacent=G.either(*(G.point_membership(g,(G.sub(p[0],G.constant(du)),G.sub(p[1],G.constant(dv))))
                          for g in fixed for du,dv in G.UV_DIRS))
        demand.append(G.both(G.neg(occupied),adjacent))
    part=G.partition([x for row in coverage for x in row]+eligible+list(clash.values())+demand)
    n=len(atlas);universal={'cover':[0]*n,'conflicts':[(1<<n)-1]*n,'available':0};samples=[]
    for k in part['representatives']:
        guard();require(all(G.evaluate(x,k) for x in demand),'A demanded point is not in every open halo')
        cov=[sum(1<<j for j,f in enumerate(row) if G.evaluate(f,k)) for row in coverage]
        con=[1<<j for j in range(n)]
        for (i,j),f in clash.items():
            if G.evaluate(f,k):con[i]|=1<<j;con[j]|=1<<i
        av=sum(1<<j for j,f in enumerate(eligible) if cov[j] and G.evaluate(f,k))
        for j in range(n):universal['cover'][j]|=cov[j];universal['conflicts'][j]&=con[j]
        universal['available']|=av;samples.append({'k':k,'matrix':{'cover':cov,'conflicts':con,'available':av}})
    return part,samples,universal


def cover_certificate(matrix,number_of_points,guard):
    cov,con,av=matrix['cover'],matrix['conflicts'],matrix['available'];failed={};nodes=[0]
    suppliers=[sum(1<<i for i,C in enumerate(cov) if C>>j&1) for j in range(number_of_points)]
    def visit(A,R):
        guard();nodes[0]+=1;require(nodes[0]<=100000,'100000-node guard; incomplete, no rejection')
        if not R:return []
        if (A,R) in failed:return None
        j=min((j for j in range(number_of_points) if R>>j&1),key=lambda j:(suppliers[j]&A).bit_count())
        choices=suppliers[j]&A
        while choices:
            bit=choices&-choices;choices^=bit;i=bit.bit_length()-1
            answer=visit(A&~con[i],R&~cov[i])
            if answer is not None:return [i]+answer
        failed[A,R]=j;return None
    remaining=(1<<number_of_points)-1;answer=visit(av,remaining)
    return {'rejected':answer is None,'visited':nodes[0],'cover_witness':answer,
            'root':[hex(av),hex(remaining)],
            'nodes':[[hex(A),hex(R),j] for (A,R),j in sorted(failed.items())] if answer is None else []}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--case',default='angle',choices=['angle']);args=parser.parse_args()
    start=time.monotonic()
    def guard():
        require(not deps.paused(),
                'Operational pause barrier; incomplete work inconclusive')
        require(time.monotonic()-start<43,'43s guard; incomplete work inconclusive')
    def alarm(signum,frame):raise RuntimeError('45s guard; incomplete work inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    fixed=(IDENTITY,ANGLE);points=ANGLE_POINTS;sup=[]
    for p in points:
        guard();d=finite_suppliers(p,fixed);require(d['finite'],'Point has a varying height family')
        sup.append(d)
    atlas=sorted(set().union(*(set(d['atlas']) for d in sup)))
    part,samples,universal=matrices(fixed,atlas,points,guard)
    proof=cover_certificate(universal,len(points),guard);individual=[]
    if not proof['rejected']:
        for row in samples:individual.append({'k':row['k'],'proof':cover_certificate(row['matrix'],len(points),guard)})
    complete=proof['rejected'] or bool(individual) and all(x['proof']['rejected'] for x in individual)
    signal.alarm(0)
    d={'agent':'six-heesch-2','role':'researcher','case':args.case,'complete':complete,
       'scope':'All k>=6: only the literal registered fixed pair and these halo demands; a rejection excludes that pose from E1',
       'fixed':fixed,'points':points,'supplier_records':sup,'atlas':atlas,'partition':part,
       'samples':samples,'universal':universal,'proof':proof,'individual':individual,
       'source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
                         [HERE/'strip_local_pair_certificate.py',HERE/'strip_point_suppliers.py',HERE/'strip_notch_intervals.py',
                          deps.GEOMETRY/'strip_parametric_geometry.py',deps.GEOMETRY/'strip_columns.py']},
       'checked_utc':datetime.now(timezone.utc).isoformat(),'seconds':round(time.monotonic()-start,3),
       'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    mode='normal' if __debug__ else 'optimized'
    (HERE/'strip-contact-domain'/f'local-{args.case}-{mode}.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({'case':args.case,'complete':complete,'suppliers':len(atlas),'points':len(points),
                      'partition':part,'universal_nodes':len(proof['nodes']),
                      'universal_rejected':proof['rejected'],'individual':[{'k':x['k'],'rejected':x['proof']['rejected'],'nodes':len(x['proof']['nodes'])} for x in individual],
                      'seconds':d['seconds'],'max_rss_kib':d['max_rss_kib']},sort_keys=True),flush=True)


if __name__=='__main__':main()
