"""Search-free lower-endpoint replay with separate axial footprint checks."""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import resource
import signal
import time

import deps
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
from known_e1 import EXCLUDED,known_bad
from collar import I,G as LOWER,B,S,D,PLANS

H=Path(__file__).resolve().parent
POINTS=(((0,-1),(0,0)),((0,-2),(0,-1)),((0,-2),(0,0)),
    ((0,-2),(0,1)),((0,-1),(0,1)),((0,4),(0,3)),
    ((0,4),(0,4)),((0,5),(0,3)),((0,6),(0,3)),((0,7),(-1,3)))
FIXED=(I,LOWER,S,D)


def formulas(fixed,points,atlas):
    cov=[[G.point_membership(h,p) for p in points] for h in atlas]
    eligible=[G.both(*(G.both(G.neg(G.intersection(G.relative(f,h))),
        G.neg(known_bad(G.relative(f,h)))) for f in fixed)) for h in atlas]
    clashes={(i,j):G.either(G.intersection(G.relative(a,b)),
        known_bad(G.relative(a,b))) for j,b in enumerate(atlas) for i,a in enumerate(atlas[:j])}
    demands=[G.both(G.neg(G.either(*(G.point_membership(f,p) for f in fixed))),
        G.either(*(G.point_membership(f,(G.sub(p[0],(0,u)),G.sub(p[1],(0,v))))
            for f in fixed[:2] for u,v in G.UV_DIRS))) for p in points]
    rows=[v for row in cov for v in row]+eligible+list(clashes.values())+demands
    return cov,eligible,clashes,demands,R.splitter(rows)


def symbolic_matrix(k,cov,eligible,clashes):
    c=[sum(1<<j for j,p in enumerate(row) if G.evaluate(p,k)) for row in cov]
    n=len(c);con=[1<<i for i in range(n)]
    for (i,j),p in clashes.items():
        if G.evaluate(p,k):con[i]|=1<<j;con[j]|=1<<i
    av=sum(1<<i for i,p in enumerate(eligible) if c[i] and G.evaluate(p,k))
    return {'cover':c,'conflicts':con,'available':av}


def axial_matrix(k,fixed,points,atlas,guard):
    E=R.E;tile=R.literal(k)
    frames=[R.axial(h,k) for h in atlas]
    fframes=[R.axial(f,k) for f in fixed]
    shapes=[set(E.affine(tile,h)) for h in frames]
    fshapes=[set(E.affine(tile,f)) for f in fframes]
    literal_points=[(G.value(u,k)-2*G.value(v,k),G.value(v,k)) for u,v in points]
    excluded={R.axial(q,k) for g in EXCLUDED for q in (g,G.inverse(g))}
    def bad(rel,A,B):
        suspect=rel in excluded
        if rel[:4]==(1,0,0,1):
            u,v=rel[4]+2*rel[5],rel[5]
            if u==-6:u,v=-u,-v
            suspect|=u==6 and v not in [3-k,4-k]
            if u==-5:u,v=-u,-v
            suspect|=u==5 and 3<=v<=k+1
        return suspect and E.touching(A,B)
    c=[sum(1<<j for j,p in enumerate(literal_points) if p in A) for A in shapes]
    n=len(atlas);con=[1<<i for i in range(n)];av=0
    for i,(frame,A) in enumerate(zip(frames,shapes)):
        guard()
        if c[i] and all(not A&B and not bad(E.compose(E.inverse(f),frame),B,A)
                        for f,B in zip(fframes,fshapes)):av|=1<<i
        for j,(other,B) in enumerate(zip(frames[:i],shapes[:i])):
            if A&B or bad(E.compose(E.inverse(other),frame),B,A):
                con[i]|=1<<j;con[j]|=1<<i
    occupied=set().union(*fshapes)
    original_halo=E.halo(fshapes[0]|fshapes[1])-occupied
    require(set(literal_points)<=original_halo,'A collar demand is not in original pair halo')
    require(all(not(a&b) for i,a in enumerate(fshapes) for b in fshapes[:i]),
            'Forced prefix is not a packing')
    return {'cover':c,'conflicts':con,'available':av}


def check_steps(steps,guard):
    require(len(steps)==len(PLANS),'Missing forced step')
    results=[]
    for saved,(name,fixed,point,expected) in zip(steps,PLANS):
        guard()
        require(saved['name']==name and R.freeze(saved['fixed'])==fixed and
            R.freeze(saved['point'])==point,'Wrong literal force input')
        suppliers=R.supplier_atlas(point,fixed,guard)
        require(R.freeze(suppliers)==R.freeze(saved['complete_suppliers']),
                'Changed complete force inventory')
        atlas=R.freeze(suppliers['atlas'])
        cov,elig,clash,demands,part=formulas(fixed,(point,),atlas)
        # Saved force partitions do not include unused pairwise clashes.
        forcepart=R.splitter(elig+demands)
        for k in forcepart['representatives']:
            require(all(G.evaluate(p,k) for p in demands),'Wrong force demand')
            found={R.axial(h,k) for h,p in zip(atlas,elig) if G.evaluate(p,k)}
            require(found=={R.axial(h,k) for h in expected},'Missing force/exclusion')
        results.append({'name':name,'raw_suppliers':len(atlas),
                        'partition':forcepart,'expected':expected})
    return results


def rebuild(collar,guard):
    require(R.freeze(collar['fixed'])==FIXED and R.freeze(collar['points'])==POINTS,
            'Wrong literal final collar')
    require(len(collar['supplier_records'])==len(POINTS),'Missing source inventory')
    rebuilt=[]
    for p,saved in zip(POINTS,collar['supplier_records']):
        guard();s=R.supplier_atlas(p,FIXED,guard)
        require(R.freeze(s)==R.freeze(saved),'Complete supplier source differs')
        rebuilt.append(s)
    atlas=tuple(sorted(set().union(*(set(R.freeze(s['atlas'])) for s in rebuilt))))
    require(atlas==R.freeze(collar['atlas']),'Wrong entire supplier atlas')
    cov,elig,clash,demands,part=formulas(FIXED,POINTS,atlas)
    saved=collar['known_E1'];require(part==saved['partition'],'Missing critical parameter cut')
    n=len(atlas);universal={'cover':[0]*n,'conflicts':[(1<<n)-1]*n,'available':0}
    matrices=[]
    for k in part['representatives']:
        guard();require(all(G.evaluate(p,k) for p in demands),'False original pair-halo demand')
        symbolic=symbolic_matrix(k,cov,elig,clash)
        direct=axial_matrix(k,FIXED,POINTS,atlas,guard)
        require(symbolic==direct,'Separate AX footprint/conflict matrix differs')
        matrices.append({'k':k,'matrix':symbolic})
        for j in range(n):
            universal['cover'][j]|=symbolic['cover'][j]
            universal['conflicts'][j]&=symbolic['conflicts'][j]
        universal['available']|=symbolic['available']
    # A supplementary far-tail material audit; the threshold splitter proves
    # the tail, rather than this isolated parameter.
    require(symbolic_matrix(40,cov,elig,clash)==axial_matrix(40,FIXED,POINTS,atlas,guard),
            'Far-tail material audit differs')
    require(universal==saved['universal'],'Wrong conservative universal matrix')
    for row,s in zip(matrices,saved['samples']):
        require(row['k']==s['k'] and row['matrix']==s['matrix'],'Wrong class matrix')
    require(len(matrices)==len(saved['samples']),'Missing parameter class')
    nodes=R.dag_check(saved['proof'],universal,len(POINTS))
    return {'partition':part,'universal':universal,'matrices':matrices,
            'DAG_nodes':nodes,'atlas_size':n,'available':universal['available'].bit_count()}


def main():
    (H/'generated').mkdir(exist_ok=True)
    start=time.monotonic();calls=[0]
    def guard():
        calls[0]+=1
        if any((R.OPS/n).exists() for n in ['PAUSED','PAUSED.json','HANDOVER.json']) or \
                time.monotonic()-start>=43 or calls[0]>100000:
            raise RuntimeError('Operational/time/work guard; no negative')
    def alarm(a,b):raise RuntimeError('45s signal guard; no negative')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    source=json.loads((H/'generated'/'collar-normal.json').read_text())['evidence']
    steps=check_steps(source['uniform_steps'],guard)
    replay=rebuild(source['collar'],guard)
    # Each damage check compares to geometry already reconstructed from source;
    # the DAG checks themselves replay every actual supplier branch.
    controls=[];saved=source['collar']['known_E1']
    for label in ['changed_matrix_available','changed_matrix_cover','changed_clash',
                  'missing_DAG_node','false_DAG_leaf','changed_DAG_root']:
        d=deepcopy(saved)
        if label=='changed_matrix_available':d['universal']['available']^=1
        elif label=='changed_matrix_cover':d['universal']['cover'][0]^=1
        elif label=='changed_clash':d['universal']['conflicts'][0]^=1
        elif label=='missing_DAG_node':d['proof']['nodes'].pop()
        elif label=='false_DAG_leaf':d['proof']['nodes']=d['proof']['nodes'][:1]
        else:d['proof']['root'][1]='0x0'
        try:
            require(d['universal']==replay['universal'],'Changed reconstructed matrix')
            R.dag_check(d['proof'],replay['universal'],len(POINTS))
        except ValueError:controls.append(label)
        else:raise ValueError('Damaged matrix or DAG accepted')
    math={'steps':steps,'replay':replay,'damaged_controls':controls,
          'separate_AX_material_parameters':replay['partition']['representatives']+[40],
          'uniform_conclusion':'(I;5,2-k) outside registered E2 for every k>=6'}
    mode='normal' if __debug__ else 'optimized'
    result={'agent':'six-heesch-2','role':'researcher','complete':True,
        'evidence':math,'mathematics_sha256':R.sha(math),
        'seconds':round(time.monotonic()-start,3),
        'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated'/f'check-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({'complete':True,'mathematics_sha256':result['mathematics_sha256'],
        'DAG_nodes':replay['DAG_nodes'],'atlas_size':replay['atlas_size'],
        'parameters':math['separate_AX_material_parameters'],'damaged_controls':controls,
        'seconds':result['seconds'],'max_rss_kib':result['max_rss_kib']},sort_keys=True),flush=True)


if __name__=='__main__':main()
