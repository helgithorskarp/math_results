"""Independent9535 audit. Prior9422 row engines disclosed; new census/graph/role code.
Defining graph mathematics read; author programs and EXPECTED still unread.
"""
import collections,functools,hashlib,itertools as it,json,pathlib,time
import prior_rows,prior_bit_rows
P=pathlib.Path(__file__).resolve().parent
F=('e','k','q','eligible','h','g1','sigma','psi','margin')
PAIRS=list(it.combinations(range(4),2));TRIPLES=list(it.combinations(range(4),3))
def need(x,m):
    if not x:raise ValueError(m)
def enc(x):return (json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()
def sha(x):return hashlib.sha256(enc(x)).hexdigest()
def start_guard():return time.monotonic()
def guard(start,states,limit=500000,seconds=20):
    need(states<=limit and time.monotonic()-start<seconds,'INCOMPLETE fixed state/time guard')
def local():
    stars=json.loads((P/'fixtures.json').read_text())['stars']
    raw=prior_rows.marks(stars)
    need(raw==prior_bit_rows.literal_rows(stars),'whole prior426 set/bit reconstruction')
    rows=[r for r in raw if r['k']<=4]
    types=sorted({tuple(r[f] for f in F) for r in rows})
    hist={tuple(r[f] for f in F):tuple(sum(r['delta'][p]==j for p in r['high'] if p not in r['hubs']) for j in range(1,6)) for r in rows}
    need(all(sum(hist[tuple(r[f] for f in F)])==r['h']-r['k'] for r in rows),'whole color histogram')
    return stars,raw,types,[hist[t] for t in types]
def cases():
    out=[]
    for Q,T,X,tau in it.product(range(9),range(5),range(5),range(3)):
        cost=Q+2*T+2*X+4*tau
        if cost<=8:out.append({'Q':Q,'T':T,'X':X,'tau':tau,'E':15-Q-T-2*tau,'K':22-(15-Q-T-2*tau)+2*X,'budget':3*(8-cost)})
    return out

def census(types,case,admissible=None):
    charges=[(1,t[0],t[1],t[2],t[6],t[8]) for t in types]
    target=(14,case['E'],case['K'],case['Q'],2*case['X'],case['budget'])
    active=[i for i,a in enumerate(charges) if i not in (0,1) and (admissible is None or i in admissible) and all(a[j]<=target[j] for j in range(6))]
    active.sort(key=lambda i:(charges[i][3]+charges[i][4]>0,charges[i][3],charges[i][4],charges[i][1],charges[i][2]),reverse=True)
    cols=[charges[i] for i in active];suffix=[]
    need(charges[0]==(1,0,0,0,0,0) and charges[1]==(1,0,1,0,0,1),'exact two unit completion factors')
    for pos in range(len(cols)+1):
        rest=cols[pos:]+[charges[0],charges[1]];suffix.append([(min(a[j] for a in rest),max(a[j] for a in rest)) for j in range(1,6)] if rest else [])
    states=0;st=start_guard()
    @functools.cache
    def count(pos,s):
        nonlocal states
        states+=1;guard(st,states,100000,10)
        if pos==len(cols):return int(s[1]==s[3]==s[4]==0 and 0<=s[2]<=min(s[0],s[5]))
        for j,(lo,hi) in enumerate(suffix[pos],1):
            if s[j]<s[0]*lo or (j<5 and s[j]>s[0]*hi):return 0
        a=cols[pos];M=min([s[0]]+[s[j]//a[j] for j in range(1,6) if a[j]])
        return sum(count(pos+1,tuple(s[j]-m*a[j] for j in range(6))) for m in range(M+1))
    total=count(0,target);out=[]
    def expand(pos,s,path):
        if pos==len(cols):
            v=[0]*len(types);v[1]=s[2];v[0]=s[0]-s[2]
            for i,n in zip(active,path):v[i]=n
            out.append(tuple(v));return
        a=cols[pos];M=min([s[0]]+[s[j]//a[j] for j in range(1,6) if a[j]])
        for m in range(M+1):
            child=tuple(s[j]-m*a[j] for j in range(6))
            if count(pos+1,child):expand(pos+1,child,path+[m])
    if total:expand(0,target,[])
    need(len(out)==len(set(out))==total,'count DAG equals all positive paths')
    for v in out:
        q=tuple(sum(n*a[j] for n,a in zip(v,charges)) for j in range(6))
        need(q[:5]==target[:5] and q[5]<=target[5],'whole fullvector target totals')
    return sorted(out),states

def expand_vertices(types,hist,v):return [(i,types[i],hist[i]) for i,n in enumerate(v) for _ in range(n)]
def potential(V):
    out={}
    for a,b in it.combinations(range(len(V)),2):
        A,B=V[a][1],V[b][1]
        if (A[0]==0 and B[3]) or (B[0]==0 and A[3]):continue
        colors={j for j,(x,y) in enumerate(zip(V[a][2],V[b][2])) if x and y}
        if colors:out[a,b]=colors
    return out

def old_failures(V,pot):
    bad=[]
    if any(sum(v[2][j] for v in V)%2 for j in range(5)):bad.append('color_parity')
    if any(sum(j in col and a in pair for pair,col in pot.items())<V[a][2][j] for a in range(len(V)) for j in range(5)):bad.append('distinct_partners')
    if any(sum(sorted([sum(V[b][2]) for b in range(len(V)) if b!=a and tuple(sorted((a,b))) in pot],reverse=True)[:sum(V[a][2])])<13 for a in range(len(V)) if V[a][1][1]==0):bad.append('relaxed_radius13')
    return bad

def metric(V):
    U=[a for a,v in enumerate(V) if v[1][0]==0];A=[a for a in U if not V[a][1][3]]
    C=[a for a,v in enumerate(V) if v[1][0]>0 and not v[1][3]];B=[a for a,v in enumerate(V) if v[1][0]>0 and v[1][3]]
    D=sum(sum(V[a][2]) for a in U);I=sum(min(sum(V[a][2]),len(A)-1) for a in A);C1=sum(V[a][2][0] for a in C)
    R=sum(V[a][1][1]==0 for a in U)
    return U,A,C,B,D,I,C1,R

def connected(pot,n,root):
    seen={root}
    while True:
        new=seen|{b for a,b in pot if a in seen}|{a for a,b in pot if b in seen}
        if new==seen:return seen
        seen=new

def graph_cut(V,case):
    n=len(V);pot=potential(V);old=old_failures(V,pot)
    if old:return {'stage':'prior','all_prior_failures':old}
    U,A,C,B,D,I,C1,R=metric(V)
    if D>I+C1:return {'stage':'unit_endpoint','D':D,'I':I,'C1':C1}
    if D==I+C1:
        for pair,col in list(pot.items()):
            a,b=pair
            if (a in C and b not in U) or (b in C and a not in U):
                col.discard(0)
                if not col:del pot[pair]
    for r in range(n):
        if V[r][1][1]==0:
            seen=connected(pot,n,r)
            if len(seen)<n:return {'stage':'closed_all_color','root':r,'side':sorted(seen)}
    if R and B and sum(sum(V[a][2]) for a in C)<max(R,D-I)+len(B):return {'stage':'joint_crossing','R':R,'B':len(B),'Ctotal':sum(sum(V[a][2]) for a in C),'need':max(R,D-I)+len(B)}
    forced={};passes=0
    while True:
        changed=False;passes+=1;need(passes<=100,'monotone propagation termination')
        for a in range(n):
            for j in range(5):
                f=sum(a in pair and c==j for pair,c in forced.items());todo=[pair for pair,col in pot.items() if a in pair and j in col and pair not in forced]
                rem=V[a][2][j]-f
                if rem<0 or rem>len(todo):return {'stage':'forced_degree','vertex':a,'color':j+1,'remaining':rem,'possible':len(todo)}
                if rem==0:
                    for pair in todo:
                        pot[pair].discard(j);changed=True
                        if not pot[pair]:del pot[pair]
                elif rem==len(todo):
                    for pair in todo:
                        forced[pair]=j;pot[pair]={j};changed=True
        if not changed:break
    for j in range(5):
        layer={pair for pair,col in pot.items() if j in col};unseen=set(range(n))
        while unseen:
            root=min(unseen);side=connected(layer,n,root);unseen-=side
            if sum(V[a][2][j] for a in side)%2:return {'stage':'closed_color_parity','color':j+1,'side':sorted(side)}
    Fset=set(forced)
    # Every exact root-neighbor subset is overapproximated. Forced internal
    # triangles and outward repeats lower bound the exact walk losses.
    for r in range(n):
        if V[r][1][1]!=0:continue
        poss=[a for a in range(n) if a!=r and tuple(sorted((r,a))) in pot];req={a for a in poss if tuple(sorted((r,a))) in forced}
        d=sum(V[r][2]);accept=0;tested=0;largest=-1
        for Nt in it.combinations(poss,d):
            N=set(Nt)
            if not req<=N:continue
            tested+=1
            tri=sum(tuple(sorted(pair)) in Fset for pair in it.combinations(Nt,2))
            out=set(range(n))-{r}-N
            if any(not any(tuple(sorted((a,t))) in pot for a in N) for t in out):continue
            loss=sum(max(0,sum(tuple(sorted((a,t))) in Fset for a in N)-1) for t in out)
            bound=sum(sum(V[a][2]) for a in N)-2*tri-loss;largest=max(largest,bound)
            if bound>=13:accept+=1
        if not accept:return {'stage':'radius_subset_loss','root':r,'subsets':tested,'largest_upper_walks':largest}
    if case['tau']==0:
        for r in range(n):
            Ns=[a for a in range(n) if a!=r and tuple(sorted((r,a))) in Fset]
            tri=sum(tuple(sorted(pair)) in Fset for pair in it.combinations(Ns,2))
            d=sum(V[r][2]);maximum=d*(d-1)//2-(V[r][1][4]-1-V[r][1][2])
            if tri>maximum:return {'stage':'forced_uncovered_triangles','vertex':r,'forced_triangles':tri,'maximum':maximum}
    return {'stage':'survives','potential':[[a,b,sorted(col)] for (a,b),col in sorted(pot.items())],'forced':[[a,b,j] for (a,b),j in sorted(forced.items())]}

def build_census():
    stars,raw,types,hist=local();case_records=[];totals=collections.Counter();surv=[]
    physical=P/'independent-physical.json';admissible=set(map(int,json.loads(physical.read_text())['accepted_types'])) if physical.exists() else None
    for case in cases():
        vectors,states=census(types,case,admissible);records=[]
        for v in vectors:
            check=graph_cut(expand_vertices(types,hist,v),case);totals[check['stage']]+=1
            records.append({'counts':v,'graph':check})
            if check['stage']=='survives':surv.append({'case':case,'counts':v,'graph':check})
        case_records.append({'case':case,'count_states':states,'records':records})
    result={'physically_admissible_types':sorted(admissible) if admissible is not None else None,'fields':F,'types':types,'histograms':hist,'raw426_sha':sha(raw),'cases':case_records,'stage_totals':dict(totals),'survivors':surv}
    (P/'independent-census.json').write_bytes(enc(result));print(json.dumps({'types':len(types),'cases':len(case_records),'vectors':sum(len(c['records']) for c in case_records),'stages':dict(totals),'survivors':len(surv),'sha256':sha(result)}),flush=True)
    return result

if __name__=='__main__':build_census()
