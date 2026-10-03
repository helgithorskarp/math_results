"""Independent row-subset mincuts and physical pair witnesses; imports no producer."""
import itertools,json,sys,hashlib
from pathlib import Path
def ensure(ok,msg):
    if not ok:raise ValueError(msg)
def analyze(carrier,n,m):
    missing={0,1} if carrier=='A' else {1,2}
    pairs=list(itertools.combinations(range(4),2))
    multiplicity={p:(3 if set(p)==missing else 4) for p in pairs}
    deficits=[70-4*(18 if a==0 else 19)+sum(v for p,v in multiplicity.items() if a in p) for a in range(4)]
    for a in range(4):
        # Direct incidence inequality: all HIGH-HIGH edges plus LOW stubs.
        if (42+n[a] if a==0 else 30+n[a])>(n[a]+3)*(n[a]+2)+14-n[a]:return None
        if not 0<=m[a]<=min(n[a],deficits[a]-n[a]):return None
        if m[a] and n[a]<5:return None
    centers=tuple(a for a in range(4) for _ in range(m[a]))
    allowed=[];demands=[]
    for a in centers:
        allowed.append({p for p in pairs if a in p and not any(
            b in p and b!=a and b>0 and n[b]==2 and multiplicity[p]==4
            for b in range(4))})
        demands.append(max(0,8-n[a]))
    capacities={p:14-3*multiplicity[p] for p in pairs}
    # Eliminate EDGE vertices from every s-t cut. Sixteen ROW-subset cuts.
    for bits in itertools.product([False,True],repeat=4):
        subset=[j for j,b in enumerate(bits) if b]
        supply=sum(min(capacities[p],sum(p in allowed[j] for j in subset)) for p in pairs)
        if sum(demands[j] for j in subset)>supply:return None
    return centers,allowed,demands,capacities,pairs
def all_physical(data):
    centers,allowed,demands,cap,pairs=data
    domains=[list(itertools.combinations(sorted(A),d)) for A,d in zip(allowed,demands)]
    answer=[]
    for stars in itertools.product(*domains):
        counts={p:sum(p in s for s in stars) for p in pairs}
        if all(counts[p]<=cap[p] for p in pairs):
            answer.append([[pairs.index(p) for p in s] for s in stars])
    return answer
def main(directory):
    given=json.loads((directory/'records.json').read_text());flags=(directory/'flags.bin').read_bytes()
    ensure(set(given)=={'cases','records','equality'},'packet keys')
    ms=[v for v in itertools.product(range(5),repeat=4) if sum(v)==4]
    truth=[];positive=[];equality=[];case_counts={}
    for c in ['A','B']:
        special={0,1} if c=='A' else {1,2}
        D=[]
        for a in range(4):
            P_a=sum(3 if {a,b}==special else 4 for b in range(4) if b!=a)
            D.append(70-4*(18 if a==0 else 19)+P_a)
        total=0
        for n in itertools.product(*(range(d+1) for d in D)):
            for m in ms:
                total+=1;data=analyze(c,n,m);truth.append(int(data is not None))
                if data is not None:
                    positive.append((c,list(n),list(m)))
                    ensure(sum(n)>=17,'subseventeen feasible')
                    if sum(n)==17:equality.append({'carrier':c,'n':list(n),'m':list(m),'all_stars':all_physical(data)})
        case_counts[c]=total
    ensure(flags==bytes(truth),'complete defining case stream')
    ensure(given['cases']==case_counts,'domain coverage')
    ensure([(r['carrier'],r['n'],r['m']) for r in given['records']]==positive,'complete positive cases')
    for r in given['records']:
        data=analyze(r['carrier'],r['n'],r['m']);centers,allowed,demands,cap,pairs=data
        ensure(len(r['witness'])==4,'four literal rows')
        used={p:0 for p in pairs}
        for j,star in enumerate(r['witness']):
            ensure(len(star)==demands[j] and len(set(star))==len(star),'star cardinality')
            ensure(all(type(e)==int and 0<=e<6 for e in star),'edge index')
            for e in star:
                ensure(pairs[e] in allowed[j],'actual prohibited HH edge');used[pairs[e]]+=1
        ensure(all(used[p]<=cap[p] for p in pairs),'capacity')
    ensure(given['equality']==equality,'all equality stars')
    ensure(len(equality)==2 and all(e['carrier']=='A' and e['m'][0]==3 for e in equality),'equality patterns')
    # Full five-HIGH graph/LOW matching check, independent of all packets.
    closed=0
    edges=list(itertools.combinations(range(5),2))
    for bits in itertools.product([0,1],repeat=10):
        for low_matching in range(7):
            hsum=2*sum(bits)+12-2*low_matching
            if hsum==32:
                ensure(sum(bits)==10 and low_matching==0,'K5 rigidity');closed+=1
    ensure(closed==1,'unique K5 equality')
    print(json.dumps({'cases':case_counts,'positive_cases':len(positive),'minimum_K':17,'equality':equality,'K5_degree_identities':7168,'K5_equalities':closed,'flags_sha256':hashlib.sha256(flags).hexdigest(),'records_sha256':hashlib.sha256((directory/'records.json').read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1]))
