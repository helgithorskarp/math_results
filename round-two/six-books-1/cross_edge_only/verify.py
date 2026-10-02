"""Independent column and literal-colored-set exploratory checker."""
from itertools import combinations, product
from pathlib import Path
import argparse, hashlib, json, time

V14=tuple(i for i in range(16) if i not in (11,12))
LOCAL={0:(1,8,9),1:(0,),2:(6,7),3:(4,5),4:(3,7,9),5:(3,6,8),6:(2,5,9),7:(2,4,8),8:(0,5,7),9:(0,4,6)}
LABEL={0:2,1:1,2:3,3:4,4:5,5:6,6:7,7:8,8:9,9:10}

def canonical(x):return json.dumps(x,separators=(',',':'))
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def guard(t):
    if time.monotonic()-t>30:raise RuntimeError('30s phase guard: incomplete verification')

def graph(r,columns,sy=(0,0)):
    red=[set() for i in range(16)]
    def edge(i,j):red[i].add(j);red[j].add(i)
    for i in LABEL.values():edge(0,i)
    for i,neighbors in LOCAL.items():
        for j in neighbors:edge(LABEL[i],LABEL[j])
    for j in (11,12):edge(1,j);edge(2,j)
    for j in (13,14,15):edge(2,j)
    omissions=(0,1) if r==0 else (1,0)
    for s in range(2):
        for t in range(3):
            if t!=omissions[s]:edge(s+9,t+13)
    for s,omission in enumerate((0,2)):
        for t in range(3):
            if t!=omission:edge(s+11,t+13)
    for i,c in enumerate(columns):
        for t in range(3):
            if c>>t&1:edge(i+3,t+13)
        for s in range(2):
            if sy[s]>>i&1:edge(i+3,s+11)
    return red

def necessary(red,degrees,vertices,outside):
    universe=set(vertices)
    nr={i:red[i]&universe for i in vertices}
    nb={i:universe-nr[i]-{i} for i in vertices}
    q={i:degrees[i]-len(nr[i]) for i in vertices}
    if any(z<0 or z>outside for z in q.values()):raise ValueError('outside rank')
    for i,j in combinations(vertices,2):
        if j in nr[i]:
            if len(nr[i]&nr[j])+max(0,q[i]+q[j]-outside)>3:return False
        elif len(nb[i]&nb[j])+max(0,outside-q[i]-q[j])>6:return False
    return True

def domain14(r):
    start=time.monotonic();answer=[];words=0
    for c in product((3,5,6,7),(3,5,6,7),range(1,8),range(1,8),range(1,8),range(1,8)):
        words+=1;red=graph(r,c)
        DT=tuple(len(red[t]&set(V14))+4 for t in (13,14,15))
        # T1>11 contradicts SY rank sum>=5 and each rank<=8-R1.
        if DT[1]>11:continue
        degrees=(10,10,9,*([10]*8),6,6,*DT)
        # Dissect the eight omitted vertices into two blue-to-SX specials
        # and six ordinary-Y vertices. This is a necessary Q intersection.
        if any(len(red[s]&red[t]&set(V14))+max(0,4+(3,2,3)[t-13]-6)>3
               for s in (9,10) for t in (13,14,15) if t in red[s]):continue
        if not necessary(red,degrees,V14,8):continue
        rows=tuple(sum(int(t+13 in red[i+3])<<i for i in range(6)) for t in range(3))
        answer.append((r,rows,c,DT))
        if words%256==0:guard(start)
    guard(start);answer.sort()
    return answer,time.monotonic()-start

def domain16(r,domain):
    start=time.monotonic();answer=[];cache={};tested=0
    # Start with all4096 ordered pairs of arbitrary six-point SY subsets.
    # A literal SY-pair blue minimum is11-|S0 union S1|.
    sy_pairs=tuple((a,b) for a,b in product(range(64),repeat=2) if 11-(a|b).bit_count()<=6)
    for _,rows,c,DT in domain:
        fixed=graph(r,c)
        counts=tuple(w.bit_count() for w in c)
        # Xi-known-degree:3+SX incidence+T incidence. Blue a--Xi
        # requires that its total K degree be<=7.
        sx_inc=tuple(sum(i+3 in fixed[s] for s in (9,10)) for i in range(6))
        capacity=tuple(4-sx_inc[i]-counts[i] for i in range(6))
        if capacity not in cache:
            cache[capacity]=tuple(sy for sy in sy_pairs if all(((sy[0]>>i)&1)+((sy[1]>>i)&1)<=capacity[i] for i in range(6)))
        # A vertex's K-neighborhood depends only on its own SY incidence.
        # Cache these exact literal neighborhoods; the whole colored predicate
        # and all120 pair comparisons below remain unchanged.
        universe=frozenset(range(16))
        degree_fixed=(10,10,9,*([10]*8),6,6,*DT)
        def entry(i,n,degree):
            nr=frozenset(n)
            return nr,universe-nr-{i},degree-len(nr)
        static=tuple(entry(i,fixed[i],degree_fixed[i]) for i in range(16))
        x_tables=tuple(tuple(entry(i+3,fixed[i+3]|{11+s for s in range(2) if word>>s&1},10)
                             for word in range(4)) for i in range(6))
        sy_tables=tuple(tuple(entry(s+11,fixed[s+11]|{i+3 for i in range(6) if word>>i&1},6+word.bit_count())
                              for word in range(64)) for s in range(2))
        for sy in cache[capacity]:
            tested+=1
            # Direct red SY--T pages contain a and their common X subset.
            # No rank normalization for SY is assumed.
            if any(1+(sy[s]&rows[t]).bit_count()>3 for s,omit in enumerate((0,2)) for t in range(3) if t!=omit):continue
            neighborhoods=list(static)
            for i in range(6):neighborhoods[i+3]=x_tables[i][((sy[0]>>i)&1)+2*((sy[1]>>i)&1)]
            neighborhoods[11]=sy_tables[0][sy[0]];neighborhoods[12]=sy_tables[1][sy[1]]
            okay=True
            for i,j in combinations(range(16),2):
                ni,nj=neighborhoods[i],neighborhoods[j]
                if j in ni[0]:
                    if len(ni[0]&nj[0])+max(0,ni[2]+nj[2]-6)>3:okay=False;break
                elif len(ni[1]&nj[1])+max(0,6-ni[2]-nj[2])>6:okay=False;break
            if not okay:continue
            beta=tuple(neighborhoods[i+3][2]-3 for i in range(6))
            if any(z<0 for z in beta):raise ValueError('ordinary blue mark cut')
            degrees=(10,10,9,*([10]*8),6+sy[0].bit_count(),6+sy[1].bit_count(),*DT)
            answer.append((r,tuple(rows),tuple(c),sy,beta,tuple(degrees[11:])))
            if tested%128==0:guard(start)
        guard(start)
    guard(start);answer.sort()
    return answer,time.monotonic()-start,tested

def main():
    p=argparse.ArgumentParser();p.add_argument('--core',type=int,choices=(0,1),required=True)
    p.add_argument('--stage',type=int,choices=(14,16),required=True);p.add_argument('--scratch',type=Path,required=True)
    a=p.parse_args();state=Path('/scratch/research-team-sol61-six-20260929/state')
    if any((state/n).exists() for n in ('PAUSED','PAUSED.json')):raise RuntimeError('pause barrier')
    domain,elapsed14=domain14(a.core)
    target14=json.loads((a.scratch/f'projection14-r{a.core}.json').read_text())
    if canonical(domain)!=canonical(target14['domain']):raise ValueError('complete independent14 domain mismatch')
    data={'agent':'six-books-1','role':'researcher','core':a.core,'stage':a.stage,
          'complete14':True,'count14':len(domain),'digest14':sha(domain),'elapsed14':elapsed14}
    if a.stage==16:
        d16,elapsed16,tested=domain16(a.core,domain)
        target16=json.loads((a.scratch/f'projection16-r{a.core}.json').read_text())
        if canonical(d16)!=canonical(target16['domain']):raise ValueError('complete independent16 domain mismatch')
        data.update({'complete16':True,'count16':len(d16),'digest16':sha(d16),'elapsed16':elapsed16,'SY_candidates_tested':tested})
    (a.scratch/f'independent{a.stage}-r{a.core}.json').write_text(canonical(data)+'\n')
    print(canonical(data))

if __name__=='__main__':main()
