"""Search-free checks of contact rectangles, notch intervals and local DAG.

Shared affine/height kernels remain a trust boundary. Endpoint partitions and
integer sweep reconstruction are separate, with unit-edge and materialized
point-alignment geometry audits. This is not independent peer review.
"""

import deps
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,importlib.util,json
from pathlib import Path
import resource,signal,time

import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import supplier_systems,IDENTITY
from strip_notch_intervals import translated_supplier_forbidden

HERE=Path(__file__).absolute().parent;DATA=HERE/'strip-contact-domain'
OPS=deps.OPS
spec=importlib.util.spec_from_file_location('separate_unit_edge_geometry',HERE.parent/'strip-t5/exact.py')
E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)


def freeze(x):
    if isinstance(x,dict):return {k:freeze(v) for k,v in x.items()}
    return tuple(freeze(v) for v in x) if isinstance(x,(tuple,list)) else x
def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def splitter(rows):
    atoms=set();stack=list(rows)
    while stack:
        r=stack.pop()
        if type(r) is bool:continue
        if r[0] in ['and','or','not']:stack.extend(r[1:])
        else:atoms.add(tuple(r))
    cuts={6};period=1
    for kind,A,B,*rest in atoms:
        if kind=='mod':require(rest==[3],'Unexpected modulus');period=3
        elif kind=='ge':
            cut=(-B+A-1)//A if A>0 else B//(-A)+1
            if cut>6:cuts.add(cut)
        elif kind=='eq':
            root,rem=divmod(-B,A)
            if rem==0 and root>=6:cuts.update((root,root+1))
        else:raise ValueError('Unknown atomic predicate')
    intervals=[];reps=[];cuts=sorted(cuts)
    for j,lo in enumerate(cuts):
        hi=cuts[j+1]-1 if j+1<len(cuts) else None
        sample=[lo+(r-lo)%period for r in range(period)]
        sample=[k for k in sample if hi is None or k<=hi]
        intervals.append({'lo':lo,'hi':hi,'representatives':sample});reps.extend(sample)
    return {'minimum':6,'period':period,'cuts':cuts,'intervals':intervals,
            'representatives':reps,'atomic_predicates':len(atoms)}


def endpoint_partition(systems):
    rows=[]
    for s in systems:
        e={tuple(s['lo']),tuple(s['hi'])}
        for lo,hi,active in s['forbidden']:e.update((tuple(lo),tuple(hi)));rows.append(active)
        e=sorted(e)
        for x in e:
            for y in e:
                if x!=y:rows.append(G.atom('ge',G.sub(x,y)))
    return splitter(rows)


def free_height_cells(s,k):
    # Difference events count forbidden intervals; no producer coverage test.
    endpoint={tuple(s['lo']),tuple(s['hi'])};events={}
    for lo,hi,active in s['forbidden']:
        lo,hi=tuple(lo),tuple(hi);endpoint.update((lo,hi))
        if G.evaluate(active,k):events[lo]=events.get(lo,0)+1;events[hi]=events.get(hi,0)-1
    ordered=sorted(endpoint,key=lambda x:(G.value(x,k),x));level=0;out=[]
    for j,lo in enumerate(ordered[:-1]):
        level+=events.get(lo,0);hi=ordered[j+1]
        if G.value(lo,k)==G.value(hi,k):continue
        if G.value(s['lo'],k)<=G.value(lo,k)<G.value(s['hi'],k) and level==0:out.append((lo,hi))
    return out


def supplier_atlas(point,fixed,guard):
    systems=supplier_systems(point,fixed);part=endpoint_partition(systems);classes=[]
    for interval in part['intervals']:
        k=interval['representatives'][0];atlas=set()
        for s in systems:
            guard()
            for lo,hi in free_height_cells(s,k):
                A,B=G.sub(hi,lo)
                width=B if A==0 else (max(A*interval['lo']+B,A*interval['hi']+B)
                                      if interval['hi'] is not None else None)
                require(width is not None and 0<width<=32,'Unbounded supplier family')
                a,b,c,d=s['matrix'];u=s['column']
                for j in range(width):
                    v=G.add(lo,G.constant(j))
                    atlas.add((s['matrix'],G.sub(G.sub(point[0],G.constant(a*u)),G.scale(b,v)),
                               G.sub(G.sub(point[1],G.constant(c*u)),G.scale(d,v))))
        classes.append({**interval,'atlas':sorted(atlas)})
    return {'finite':True,'partition':part,'classes':classes,
            'atlas':sorted(set().union(*(set(c['atlas']) for c in classes)))}


def raw_regions():
    targets=list(G.COLS);closed=[(c+du,G.add(l,G.constant(dv)),G.add(h,G.constant(dv)))
                                for du,dv in [(0,0),*G.UV_DIRS] for c,l,h in G.COLS]
    def boxes(m,r,target):
        A,B,C,D=m;answer=set();s=B//3
        for c,l,h in G.COLS:
            for d,L,H in target:
                n=d-A*c-r
                if n%B:continue
                v=n//B
                if s>0:x0,x1=G.sub(G.constant(v),h),G.add(G.sub(G.constant(v),l),G.constant(1))
                else:x0,x1=G.sub(l,G.constant(v)),G.add(G.sub(h,G.constant(v)),G.constant(1))
                offset=G.constant(C*c+D*v)
                answer.add((x0,x1,G.sub(L,offset),G.add(G.sub(H,offset),G.constant(1))))
        return tuple(sorted(answer))
    def intervals(m,a,target):
        A,B,C,D=m;out=set()
        for c,l,h in G.COLS:
            if D<0:l,h=G.scale(-1,h),G.scale(-1,l)
            for d,L,H in target:
                if d-A*c==a:out.add((G.sub(G.sub(L,G.constant(C*c)),h),
                                    G.add(G.sub(G.sub(H,G.constant(C*c)),l),G.constant(1))))
        return tuple(sorted(out))
    systems=[]
    for m in G.MATRICES:
        if m[1]:
            for r in range(3):systems.append({'type':'nonparallel','matrix':m,'residue':r,
                                            'root':boxes(m,r,targets),'closed':boxes(m,r,closed)})
        else:
            for a in sorted({d-m[0]*c for c,_,_ in targets for d,_,_ in closed}):
                systems.append({'type':'parallel','matrix':m,'a':a,
                                'root':intervals(m,a,targets),'closed':intervals(m,a,closed)})
    return systems


def scan_boxes(s,k):
    sets=[s['root'],s['closed']];axes=2 if s['type']=='nonparallel' else 1
    e=[sorted({q for ss in sets for box in ss for q in box[2*j:2*j+2]},
              key=lambda x:(G.value(x,k),x)) for j in range(axes)]
    out=[]
    strips=list(zip(e[0],e[0][1:])) if axes==2 else [(None,None)]
    for x0,x1 in strips:
        if axes==2 and G.value(x0,k)==G.value(x1,k):continue
        active=[ss if axes==1 else [b for b in ss if G.value(b[0],k)<=G.value(x0,k)<G.value(b[1],k)] for ss in sets]
        ys=e[-1];events=[{},{}]
        for j,ss in enumerate(active):
            for box in ss:
                lo,hi=box[-2:];events[j][lo]=events[j].get(lo,0)+1;events[j][hi]=events[j].get(hi,0)-1
        root_count=closed_count=0
        for y0,y1 in zip(ys,ys[1:]):
            root_count+=events[0].get(y0,0);closed_count+=events[1].get(y0,0)
            if G.value(y0,k)<G.value(y1,k) and root_count==0 and closed_count>0:
                out.append((y0,y1) if axes==1 else (x0,x1,y0,y1))
    return out


def raw_check(record,guard):
    systems=raw_regions();rows=[]
    for s in systems:
        for j in range(2 if s['type']=='nonparallel' else 1):
            e={q for box in s['root']+s['closed'] for q in box[2*j:2*j+2]}
            rows.extend(G.atom('ge',G.sub(x,y)) for x in e for y in e if x!=y)
    part=splitter(rows);require(part==record['partition'],'Changed raw partition')
    require(len(record['classes'])==len(part['intervals']),'Missing raw parameter class')
    for cls,interval in zip(record['classes'],part['intervals']):
        require(all(cls[x]==interval[x] for x in ['lo','hi','representatives']),'Wrong raw class')
        require(len(cls['systems'])==len(systems),'Missing raw residue/translation system')
        polynomial=[0,0,0];selected=[]
        for s,saved in zip(systems,cls['systems']):
            guard()
            for key in s:require(freeze(s[key])==freeze(saved[key]),'Changed raw rectangle geometry')
            cells=scan_boxes(s,interval['representatives'][0]);require(freeze(cells)==freeze(saved['selected']),'Wrong selected contact rectangles')
            selected.append(cells)
            for cell in cells:
                A,B=G.sub(cell[1],cell[0])
                if len(cell)==2:polynomial[0]+=B;polynomial[1]+=A
                else:
                    C,D=G.sub(cell[3],cell[2]);require(A*C==0 and (A==0 and B==1 or C==0 and D==1),'Not a unit-width contact strip')
                    polynomial[0]+=B*D;polynomial[1]+=A*D+B*C;polynomial[2]+=A*C
        require(polynomial==cls['cardinality']==[184,96,0],'Wrong exact cardinal polynomial')
    return systems,selected


def raw_material(k,systems,selected,guard):
    tile=literal(k);raw=E.raw_contacts(tile);root=set(tile);normalized={}
    for m in E.matrices():
        t=E.affine(tile,m+(0,0));x,y=min(t);key=tuple((u-x,v-y) for u,v in t)
        require(key not in normalized,'Ambiguous D6 frame');normalized[key]=(m,x,y)
    require(len(normalized)==12,'Incomplete orientations')
    inventory=set()
    for t in raw:
        x,y=min(t);m,u,v=normalized[tuple((a-x,b-y) for a,b in t)];a,b,c,d=m
        inventory.add((a+2*c,b+2*d-2*a-4*c,c,d-2*c,x-u+2*(y-v),y-v))
    rebuilt=set()
    for s,cells in zip(systems,selected):
        for cell in cells:
            guard()
            if s['type']=='parallel':
                rebuilt.update(s['matrix']+(s['a'],b) for b in range(G.value(cell[0],k),G.value(cell[1],k)))
            else:
                sign=s['matrix'][1]//3
                for t in range(G.value(cell[0],k),G.value(cell[1],k)):
                    rebuilt.update(s['matrix']+(3*t+s['residue'],s['matrix'][3]*sign*t+z)
                                   for z in range(G.value(cell[2],k),G.value(cell[3],k)))
    require(rebuilt==inventory and len(raw)==96*k+184,'Unit-edge contact inventory disagrees')
    return len(raw)


def literal(k):
    out={(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):out.update({(-2*r-1,r+1),(-2*r-1,r+2),(-2*r-2,r+1),(-2*r-2,r+2)})
    return tuple(sorted(out))


def axial(g,k):
    (a,b,c,d),u,v=g;x,y=G.value(u,k),G.value(v,k)
    m=(a-2*c,2*a+b-4*c-2*d,c,2*c+d);require(m in E.matrices(),'Nonrigid pose')
    return m+(x-2*y,y)


def notch_material(k,atlas):
    tile=literal(k);root=set(tile);N=(1-2*k,k-1);suppliers=set()
    for m in E.matrices():
        rotated=E.affine(tile,m+(0,0))
        for x,y in rotated:
            g=m+(N[0]-x,N[1]-y)
            if root.isdisjoint(E.affine(tile,g)):suppliers.add(g)
    require(suppliers=={axial(g,k) for g in atlas},'Materialized point-alignment inventory disagrees')
    possible=[]
    for b in range(3-k,4):
        side=(1,0,0,1,6-2*b,b)
        if any(root.isdisjoint(E.affine(E.affine(tile,h),side)) for h in suppliers):possible.append(b)
    require(possible==[3-k,4-k],'Materialized side supplier filter disagrees')
    return {'k':k,'notch_suppliers':len(suppliers),'side_shifts':possible}


def dag_check(proof,matrix,demands):
    require(proof['rejected'],'Not a negative certificate');cov=matrix['cover'];con=matrix['conflicts'];n=len(cov)
    require(proof['root']==[hex(matrix['available']),hex((1<<demands)-1)],'Changed DAG root')
    nodes=[(int(A,16),int(R,16),j) for A,R,j in proof['nodes']]
    require(len({(A,R) for A,R,j in nodes})==len(nodes),'Duplicate DAG state');valid=set()
    for A,R,j in sorted(nodes,key=lambda x:(x[1].bit_count(),x)):
        require(A>=0 and A>>n==0 and 0<R<1<<demands and 0<=j<demands and R>>j&1,'Invalid DAG state')
        for i in range(n):
            if A>>i&1 and cov[i]>>j&1:
                child=(A&~con[i],R&~cov[i]);require(child in valid,'Missing exhaustive supplier branch')
        valid.add((A,R))
    require((matrix['available'],(1<<demands)-1) in valid,'Uncertified root')
    return len(nodes)


def local_check(record,guard,material=True):
    fixed=freeze(record['fixed']);points=freeze(record['points']);atlas=set()
    for p,saved in zip(points,record['supplier_records']):
        fresh=supplier_atlas(p,fixed,guard);require(freeze(fresh)==freeze(saved),'Changed complete point-supplier reduction')
        atlas.update(fresh['atlas'])
    atlas=sorted(atlas);require(freeze(atlas)==freeze(record['atlas']),'Incomplete supplier atlas')
    require(len(points)==len(record['supplier_records']),'Missing point supplier record')
    cov=[[G.point_membership(g,p) for p in points] for g in atlas]
    eligible=[G.both(*(G.neg(G.intersection(G.relative(f,g))) for f in fixed)) for g in atlas]
    clash={(i,j):G.intersection(G.relative(g,h)) for j,h in enumerate(atlas) for i,g in enumerate(atlas[:j])}
    halo=[]
    for p in points:
        occupied=G.either(*(G.point_membership(f,p) for f in fixed))
        near=G.either(*(G.point_membership(f,(G.sub(p[0],G.constant(u)),G.sub(p[1],G.constant(v))))
                       for f in fixed for u,v in G.UV_DIRS))
        halo.append(G.both(G.neg(occupied),near))
    part=splitter([x for row in cov for x in row]+eligible+list(clash.values())+halo)
    require(part==record['partition'],'Changed local partition');n=len(atlas)
    universal={'cover':[0]*n,'conflicts':[(1<<n)-1]*n,'available':0};samples=[]
    for k in part['representatives']:
        guard();require(all(G.evaluate(f,k) for f in halo),'Invalid halo demand')
        cover=[sum(1<<j for j,f in enumerate(row) if G.evaluate(f,k)) for row in cov];con=[1<<i for i in range(n)]
        for (i,j),f in clash.items():
            if G.evaluate(f,k):con[i]|=1<<j;con[j]|=1<<i
        av=sum(1<<i for i,f in enumerate(eligible) if cover[i] and G.evaluate(f,k))
        m={'cover':cover,'conflicts':con,'available':av};samples.append({'k':k,'matrix':m})
        if material:
            tile=literal(k);feet=[set(E.affine(tile,axial(g,k))) for g in atlas]
            occupied=set().union(*(set(E.affine(tile,axial(f,k))) for f in fixed))
            pp=[(G.value(u,k)-2*G.value(v,k),G.value(v,k)) for u,v in points]
            require(set(pp)<=E.halo(occupied),'Materialized demand outside halo')
            direct={'cover':[sum(1<<j for j,p in enumerate(pp) if p in F) for F in feet],
                    'available':sum(1<<i for i,F in enumerate(feet) if set(pp)&F and not occupied&F),
                    'conflicts':[sum(1<<j for j,H in enumerate(feet) if F&H) for F in feet]}
            require(direct==m,'Materialized local geometry disagrees')
        universal['available']|=av
        for i in range(n):universal['cover'][i]|=cover[i];universal['conflicts'][i]&=con[i]
    require(samples==record['samples'] and universal==record['universal'],'Changed conservative finite matrix')
    nodes=dag_check(record['proof'],universal,len(points));require(record['complete'],'Not a complete result')
    return {'suppliers':n,'points':len(points),'cuts':part['cuts'],'DAG_nodes':nodes,'atlas_sha256':sha(atlas)}


def main():
    start=time.monotonic()
    def guard():
        if deps.paused():
            raise RuntimeError('Operational pause barrier; unfinished reader inconclusive')
        if time.monotonic()-start>=43:
            raise RuntimeError('43s guard; unfinished reader inconclusive')
    def alarm(signum,frame):raise RuntimeError('45s guard; unfinished reader inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    raw=json.loads((DATA/'produced-normal.json').read_text());systems,selected=raw_check(raw,guard)
    samples=[{'k':k,'raw_contacts':raw_material(k,systems,selected,guard)} for k in [6,7,8,9,12]]
    notch=json.loads((DATA/'notch-intervals-normal.json').read_text())
    J=supplier_atlas(((0,-1),(1,-1)),(IDENTITY,),guard)
    require(len(J['atlas'])==9,'Wrong notch supplier count')
    require(freeze(J['classes'])==freeze(notch['notch_classes']) and J['partition']==notch['notch_partition'],
            'Changed nine-supplier classification')
    side=[{'supplier':g,'lo':(-1,3),'hi':(0,4),'forbidden':translated_supplier_forbidden(g)} for g in J['atlas']]
    side_part=endpoint_partition(side);require(side_part==notch['side_partition'],'Changed side partition')
    require(side_part['cuts']==[6],'Side case not uniform')
    expected=[{'supplier':s['supplier'],'allowed_b':free_height_cells(s,6)} for s in side]
    require(freeze(expected)==freeze(notch['side_classes'][0]['surviving_supplier_intervals']),'Wrong side restriction')
    shifts=set()
    forced_candidates=set()
    for row in expected:
        for lo,hi in row['allowed_b']:
            require(G.sub(hi,lo)==(0,1),'Non-point surviving side family');shifts.add(lo)
            if lo==(-1,4):
                m,a,b=row['supplier'];forced_candidates.add((m,G.add(a,(0,6)),G.add(b,(-1,4))))
    require(shifts=={(-1,3),(-1,4)},'Wrong all-k side shifts')
    require(forced_candidates=={((-1,0,0,-1),(0,5),(0,3)),((2,-3,1,-2),(0,5),(0,3))},
            'Wrong notch candidates for the second side shift')
    material_notch=[notch_material(k,J['atlas']) for k in [6,7,8,9,12]]
    local=json.loads((DATA/'local-angle-normal.json').read_text());verified=local_check(local,guard)
    damages=0
    for which in range(6):
        guard();a=deepcopy(raw);b=deepcopy(notch);c=deepcopy(local)
        try:
            if which==0:a['classes'][0]['systems'].pop();raw_check(a,guard)
            elif which==1:a['classes'][0]['systems'][0]['selected'][0][0][1]+=1;raw_check(a,guard)
            elif which==2:c['partition']['cuts'].pop();local_check(c,guard,False)
            elif which==3:c['universal']['available']^=1;local_check(c,guard,False)
            elif which==4:c['proof']['nodes'].pop();local_check(c,guard,False)
            else:c['supplier_records'][0]['atlas'].pop();local_check(c,guard,False)
        except ValueError:damages+=1
        else:raise ValueError('Damaged certificate accepted')
    signal.alarm(0)
    evidence={'raw_cardinality':[184,96,0],'raw_samples':samples,'notch_suppliers':9,'material_notch':material_notch,
              'E1_identity_side6_shifts':['3-k','4-k'],'angle_exclusion':verified,
              'E2_identity_side4_minus_k_forced_pose':[[-1,0,0,-1],5,3],
              'damaged_controls':damages,'trust_boundary':'Shared affine/height kernels; separate event sweeps, cuts and materialized audits; unformalized ordinary reduction; no independent review'}
    mode='normal' if __debug__ else 'optimized'
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':evidence,'evidence_sha256':sha(evidence),
            'checked_utc':datetime.now(timezone.utc).isoformat(),'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (DATA/f'verified-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)


if __name__=='__main__':main()
