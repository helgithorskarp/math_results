"""Exploratory necessary domains: specified cross leaf, only E<=108."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse, hashlib, json, time

CYCLE=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN=(40,20)
MIN=(2,2,1,1,1,1)
V14=tuple(i for i in range(16) if i not in (11,12))
MASK14=sum(1<<i for i in V14)
PAIRS14=tuple(combinations(V14,2))
PAIRS16=tuple(combinations(range(16),2))
SCOPE='specified literal one-nine leaf; root10/mark9/other neighbors10; E<=108; cross omissions'

def canonical(x):return json.dumps(x,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def guard(start):
    if time.monotonic()-start>30:raise RuntimeError('30s phase guard: incomplete domain is no exclusion')
def masks(ranks):return tuple(m for m in range(64) if m.bit_count() in ranks)

def base(r):
    red=[0]*16
    def edge(i,j):red[i]|=1<<j;red[j]|=1<<i
    for j in (1,2,*range(3,11)):edge(0,j)
    for j in (2,11,12):edge(1,j)
    for j in range(9,16):edge(2,j)
    for i,j in CYCLE:edge(i+3,j+3)
    for s in range(2):
        for i in range(6):
            if OWN[s]>>i&1:edge(s+9,i+3)
    for s,w in enumerate((6,5) if r==0 else (5,6)):
        for t in range(3):
            if w>>t&1:edge(s+9,t+13)
    for s,w in enumerate((6,3)):
        for t in range(3):
            if w>>t&1:edge(s+11,t+13)
    return tuple(red)

BASE=(base(0),base(1))
def known(r,rows,sy=(0,0)):
    red=list(BASE[r]);columns=tuple(sum(((rows[t]>>i)&1)<<t for t in range(3)) for i in range(6))
    for i in range(6):
        red[i+3]|=columns[i]<<13
        red[i+3]|=(((sy[0]>>i)&1)+2*((sy[1]>>i)&1))<<11
    for t in range(3):red[t+13]|=rows[t]<<3
    for s in range(2):red[s+11]|=sy[s]<<3
    R=tuple(w.bit_count() for w in rows)
    degrees=(10,10,9,*([10]*8),6+sy[0].bit_count(),6+sy[1].bit_count(),6+R[0],6+R[1],7+R[2])
    return red,degrees,columns

def necessary(red,degrees,vertices,pairs,outside,mask):
    q={i:degrees[i]-(red[i]&mask).bit_count() for i in vertices}
    if any(z<0 or z>outside for z in q.values()):raise ValueError('outside-rank bridge')
    for i,j in pairs:
        cap=3 if red[i]>>j&1 else degrees[i]+degrees[j]-14
        if (red[i]&red[j]&mask).bit_count()+max(0,q[i]+q[j]-outside)>cap:return False
    return True

def domain14(r):
    start=time.monotonic();answer=[];candidates=0
    sx=(6,5) if r==0 else (5,6)
    for rows in product(masks((3,4,5)),masks((3,4,5)),masks((2,3,4))):
        candidates+=1
        red,degrees,c=known(r,rows)
        if any(c[i].bit_count()<MIN[i] for i in range(6)):continue
        # Ordinary SX--T red bounds use Q ranks4 and3 for T0/T2.
        if any((rows[t]&OWN[s]).bit_count()>1 for t in (0,2) for s in range(2) if sx[s]>>t&1):continue
        if necessary(red,degrees,V14,PAIRS14,8,MASK14):answer.append((r,rows,c,tuple(degrees[t] for t in (13,14,15))))
        if candidates%256==0:guard(start)
    guard(start);answer.sort()
    return {'schema':'cross-edge-only-projection14-v1','scope':SCOPE,'core':r,
            'complete':True,'row_rank_filtered_domain':candidates,'count':len(answer),
            'degrees_T_histogram':sorted(Counter(item[3] for item in answer).items()),
            'domain_sha256':sha(answer),'elapsed_seconds':time.monotonic()-start,'domain':answer}

def sy_options(k):
    choices=tuple(tuple(w for w in range(4) if w.bit_count()<=2-z) for z in k)
    answer=[]
    for columns in product(*choices):
        # The blue SY pair requires an ordinary-X union of at least5.
        if sum(w!=0 for w in columns)<5:continue
        sy=tuple(sum(((columns[i]>>s)&1)<<i for i in range(6)) for s in range(2))
        beta=tuple(2-k[i]-columns[i].bit_count() for i in range(6))
        answer.append((sy,beta))
    return answer

def domain16(r,input14):
    if input14['core']!=r or not input14['complete'] or sha(input14['domain'])!=input14['domain_sha256']:
        raise ValueError('complete input14 binding')
    start=time.monotonic();answer=[];cache={};tested=0
    for _,rows,c,DT in input14['domain']:
        k=tuple(c[i].bit_count()-MIN[i] for i in range(6))
        if sum(z==2 for z in k)>1:continue
        if k not in cache:cache[k]=sy_options(k)
        R=tuple(w.bit_count() for w in rows)
        for sy,beta in cache[k]:
            tested+=1
            if sy[0].bit_count()>min(8-R[1],8-R[2]) or sy[1].bit_count()>min(8-R[0],8-R[1]):continue
            if any((sy[s]&rows[t]).bit_count()>2 for s,w in enumerate((6,3)) for t in range(3) if w>>t&1):continue
            red,degrees,columns=known(r,rows,sy)
            q=(0,6,0,*(3+b for b in beta),4,4,2,2,3,2,3)
            if tuple(degrees[i]-red[i].bit_count() for i in range(16))!=q:
                raise ValueError('actual variable degree/rank mismatch')
            if necessary(red,degrees,tuple(range(16)),PAIRS16,6,65535):
                answer.append((r,tuple(rows),tuple(c),sy,beta,tuple(degrees[11:])))
            if tested%256==0:guard(start)
        guard(start)
    guard(start);answer.sort()
    return {'schema':'cross-edge-only-projection16-v1','scope':SCOPE,'core':r,'complete':True,
            'input14_sha256':input14['domain_sha256'],'SY_candidates_tested':tested,'count':len(answer),
            'outside_endpoint_degree_histogram':sorted(Counter(item[5] for item in answer).items()),
            'domain_sha256':sha(answer),'elapsed_seconds':time.monotonic()-start,'domain':answer}

def main():
    p=argparse.ArgumentParser();p.add_argument('--core',type=int,choices=(0,1),required=True)
    p.add_argument('--stage',type=int,choices=(14,16),required=True)
    p.add_argument('--scratch',type=Path,required=True);a=p.parse_args();a.scratch.mkdir(parents=True,exist_ok=True)
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    if any((state/n).exists() for n in ('PAUSED','PAUSED.json')):raise RuntimeError('pause barrier')
    if a.stage==14:d=domain14(a.core)
    else:d=domain16(a.core,json.loads((a.scratch/f'projection14-r{a.core}.json').read_text()))
    path=a.scratch/f'projection{a.stage}-r{a.core}.json'
    path.write_text(canonical(d)+'\n')
    print(canonical({k:v for k,v in d.items() if k!='domain'}))

if __name__=='__main__':main()
