"""Exploratory known-row joins; ordinary-Y degrees are inferred, never tagged."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse, json, time
from derive import known, canonical, sha, guard, SCOPE

ENDPOINTS=tuple(range(9,16))
PAIRS=tuple(combinations(range(16),2))
POOLS={n:tuple(m for m in range(64) if m.bit_count()==n) for n in range(7)}

def data(item):
    r,rows,c,sy,beta,D=item
    red,degrees,_=known(r,rows,sy)
    if tuple(degrees[11:])!=tuple(D):raise ValueError('variable degree input binding')
    q=tuple(degrees[i]-red[i].bit_count() for i in range(16))
    limits={(i,j):(3 if red[i]>>j&1 else degrees[i]+degrees[j]-14)-(red[i]&red[j]).bit_count() for i,j in PAIRS}
    return red,degrees,q,limits

def ep(frame):
    index,intersection,t0,t1,t2,s0,s1=frame
    return (15,51 if intersection==2 else 23,s0,s1,t0,t1,t2)

def internal_y_degrees(frame):
    masks=ep(frame)
    return tuple(4-sum((m>>j)&1 for m in masks[2:]) for j in range(6))

def domain_endpoints(xs):
    start=time.monotonic();answer=[]
    for index,item in enumerate(xs):
        _,_,_,limit=data(item)
        def allowed(i,j,a,b):return (a&b).bit_count()<=limit[min(i,j),max(i,j)]
        for intersection,b in ((2,51),(3,23)):
            choices=[tuple(m for m in POOLS[(3,2,3)[t]] if allowed(9,13+t,15,m) and allowed(10,13+t,b,m)) for t in range(3)]
            for ts in product(*choices):
                if ts[0]|ts[1]|ts[2]!=63:continue
                if any(not allowed(13+i,13+j,ts[i],ts[j]) for i,j in combinations(range(3),2)):continue
                sy=[tuple(m for m in POOLS[2] if all(allowed(9+z,11+s,(15,b)[z],m) for z in range(2))
                          and all(allowed(11+s,13+t,m,ts[t]) for t in range(3))) for s in range(2)]
                for p,q in product(*sy):
                    if not allowed(11,12,p,q):continue
                    frame=(index,intersection,*ts,p,q)
                    h=internal_y_degrees(frame)
                    if min(h)<0:continue
                    if sum(h)!=12:raise ValueError('six-edge internal-Y bridge')
                    answer.append(frame)
        guard(start)
    guard(start);answer.sort()
    return answer,time.monotonic()-start

def domain_rows(xs,frames):
    start=time.monotonic();bases=[data(x) for x in xs];answer=[];raw_products=0
    for index,frame in enumerate(frames):
        _,_,q,limit=bases[frame[0]];endpoints=ep(frame)
        rows=tuple(tuple(m for m in POOLS[q[3+i]] if all((m&endpoints[e]).bit_count()<=limit[3+i,9+e] for e in range(7))) for i in range(6))
        if all(rows):
            answer.append((index,rows))
            n=1
            for pool in rows:n*=len(pool)
            raw_products+=n
        if index%128==0:guard(start)
    guard(start)
    return answer,time.monotonic()-start,raw_products

def partial(xs,frame,rows):
    red,degrees,q,limit=data(xs[frame[0]])
    masks=(0,63,0,*rows,*ep(frame))
    if len(masks)!=16 or tuple(m.bit_count() for m in masks)!=q:raise ValueError('all known row ranks')
    red=red+[0]*6
    for i,m in enumerate(masks):
        red[i]|=m<<16
        for j in range(6):
            if m>>j&1:red[16+j]|=1<<i
    h=internal_y_degrees(frame)
    DY=tuple(5+((masks[9]>>j)&1)+((masks[10]>>j)&1)+sum((m>>j)&1 for m in rows) for j in range(6))
    if tuple(red[16+j].bit_count()+h[j] for j in range(6))!=DY:raise ValueError('actual ordinary-Y degree bridge')
    if sum(degrees)+sum(DY)!=216:raise ValueError('actual108-edge degree-sum bridge')
    return red,tuple(degrees)+DY,h,q

def closure(red,degrees,h,q):
    # Only assigned red edges are present. No unknown internal-Q edge is used.
    for i,j in combinations(range(22),2):
        if red[i]>>j&1:
            pages=red[i]&red[j]
            if pages.bit_count()>=4:
                return ('known_red_book',i,j,tuple(k for k in range(22) if pages>>k&1)[:4])
    # For a known K--Q pair, minimize over every possible red Q-neighborhood
    # of the ordinary-Y point with its actual internal degree.
    for i in range(16):
        for j in range(6):
            edge=bool(red[i]>>(16+j)&1)
            common=(red[i]&red[16+j]&65535).bit_count()
            lower=common+max(0,q[i]+h[j]-(6 if edge else 5))
            cap=3 if edge else degrees[i]+degrees[16+j]-14
            if lower>cap:return ('colored_minimum','red' if edge else 'blue',i,16+j,lower,cap)
    return ('unresolved',)

def domain_joins(xs,frames,row_records):
    start=time.monotonic();bases=[data(x) for x in xs];answer=[];counts=Counter();nodes=0;full_pair_joins=0
    for frame_index,options in row_records:
        frame=frames[frame_index];endpoints=ep(frame);_,_,_,limit=bases[frame[0]]
        h=internal_y_degrees(frame)
        column_lower=tuple(5-z for z in h)
        chosen=[];column_counts=[0]*6
        future=[]
        for depth in range(7):
            future.append(tuple(sum(any(m>>j&1 for m in options[k]) for k in range(depth,6)) for j in range(6)))
        def recurse(depth):
            nonlocal nodes,full_pair_joins
            nodes+=1
            if nodes%1024==0:guard(start)
            if any(column_counts[j]+future[depth][j]<column_lower[j] for j in range(6)):return
            if depth==6:
                full_pair_joins+=1
                red,D,inside,q=partial(xs,frame,tuple(chosen))
                why=closure(red,D,inside,q)
                counts[why[0]]+=1
                answer.append((frame_index,tuple(chosen),tuple(D[16:]),why))
                return
            for m in options[depth]:
                if any((m&chosen[k]).bit_count()>limit[3+k,3+depth] for k in range(depth)):continue
                chosen.append(m)
                for j in range(6):column_counts[j]+=(m>>j)&1
                recurse(depth+1)
                for j in range(6):column_counts[j]-=(m>>j)&1
                chosen.pop()
        recurse(0);guard(start)
    guard(start);answer.sort()
    return answer,time.monotonic()-start,dict(sorted(counts.items())),nodes,full_pair_joins

def load(path):
    d=json.loads(path.read_text())
    if not d['complete'] or sha(d['domain'])!=d['domain_sha256']:raise ValueError('complete parent domain binding')
    return d

def main():
    p=argparse.ArgumentParser();p.add_argument('--core',type=int,choices=(0,1),required=True)
    p.add_argument('--stage',choices=('endpoints','rows','joins'),required=True);p.add_argument('--scratch',type=Path,required=True)
    a=p.parse_args();state=Path('/scratch/research-team-sol61-six-20260929/state')
    if any((state/n).exists() for n in ('PAUSED','PAUSED.json')):raise RuntimeError('pause barrier')
    parent=load(a.scratch/f'projection16-r{a.core}.json');xs=parent['domain']
    d={'schema':'cross-edge-only-'+a.stage+'-v1','scope':SCOPE,'core':a.core,'parent_X_sha256':parent['domain_sha256']}
    if a.stage=='endpoints':domain,elapsed=domain_endpoints(xs)
    else:
        y=load(a.scratch/f'endpoints-r{a.core}.json');frames=y['domain'];d['parent_endpoints_sha256']=y['domain_sha256']
        if a.stage=='rows':domain,elapsed,raw_products=domain_rows(xs,frames);d['raw_row_products']=raw_products
        else:
            rows=load(a.scratch/f'rows-r{a.core}.json');d['parent_rows_sha256']=rows['domain_sha256']
            domain,elapsed,closures,nodes,full=domain_joins(xs,frames,rows['domain'])
            d.update({'closures':closures,'backtracking_nodes':nodes,'complete_row_joins':full})
    d.update({'complete':True,'count':len(domain),'domain_sha256':sha(domain),'elapsed_seconds':elapsed,'domain':domain})
    (a.scratch/f'{a.stage}-r{a.core}.json').write_text(canonical(d)+'\n')
    print(canonical({k:v for k,v in d.items() if k!='domain'}))

if __name__=='__main__':main()
