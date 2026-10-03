"""Fresh independent exact column DP and common physical-row bounds.
Written from graph mathematics before target9884 executable/certificate access.
Supplied catalogue frequencies never constrain multiplicities.
"""
import collections,functools,itertools as it,json,sys,time
from independent import P,PAIRS,enc,need

def carriers():
    # All labelled nonnegative slack compositions of2; no code symmetry.
    labelled=[]
    for i in range(6):
        for j in range(i,6):
            s=[0]*6;s[i]+=1;s[j]+=1
            lam=tuple(4-x for x in s)
            D=tuple(sum(l for pair,l in zip(PAIRS,lam) if a in pair)-(2 if a==0 else 6) for a in range(4))
            L=tuple(14-3*l for l in lam)
            labelled.append((lam,D,L))
    def transport(lam,p):
        out=[0]*6
        for pair,l in zip(PAIRS,lam):out[PAIRS.index(tuple(sorted(p[a] for a in pair)))]=l
        return tuple(out)
    ps=[(0,)+p for p in it.permutations((1,2,3))]
    keys={c[0] for c in labelled}
    need(all(transport(c[0],p) in keys for c in labelled for p in ps),'all six light transports covered')
    chosen=sorted({min(transport(c[0],p) for p in ps) for c in labelled})
    canonical=[c for lam in chosen for c in labelled if c[0]==lam]
    need(len(labelled)==21 and len(canonical)==6,'complete labelled carrier/light relabelling domain')
    return labelled,canonical

def physical():
    rows=json.loads((P/'physical22.json').read_text())['physical_rows']
    bytype=collections.defaultdict(list)
    for r in rows:
        i,d,hh,hhh,wc,iso,L=r['signature']
        if hhh==0:
            need(wc[3]==wc[4]==0,'no HHH has no three/four-hub local words')
            bytype[i].append((tuple(d),hh,tuple(L)))
    return {i:sorted(set(v)) for i,v in bytype.items()}

def option_tables(physical):
    return [{i:sorted({(d[a],L[a]+1 if d[a] else 0,L[a]%2) for d,hh,L in rows})
             for i,rows in physical.items()} for a in range(4)]

def column(counts,options,D):
    # For each (total deficit,number positive,friend parity), keep the least
    # maximum support requirement. max is monotone, so larger dominated
    # values cannot produce a new actual feasible N after another factor.
    order=sorted([i for i,n in enumerate(counts) if n],key=lambda i:(len(options.get(i,[])),i))
    if any(not options.get(i) for i in order):return []
    state={(0,0,0):0}
    for i in order:
        available=[v for v in options[i] if v[0]<=D and v[1]<=D]
        if not available:return []
        for repeat in range(counts[i]):
            nxt={}
            for (d,n,p),required in state.items():
                for weight,r,parity in available:
                    nd=d+weight;nn=n+int(weight>0)
                    if nd>D or nn>D:continue
                    key=(nd,nn,p^parity);nr=max(required,r)
                    if nr<nxt.get(key,100):nxt[key]=nr
            state=nxt
            if not state:return []
    return sorted(n for (d,n,p),r in state.items() if d==D and p==0 and r<=n)

@functools.lru_cache(maxsize=4096)
def extrema(N,immutable):
    bytype=dict(immutable);result={}
    for i,rows in bytype.items():
        allowed=[(d,hh,L) for d,hh,L in rows if all(not d[a] or L[a]<N[a] for a in range(4))]
        if not allowed:result[i]=None;continue
        scores=[]
        for d,hh,L in allowed:
            ds=[sum(d[a] for a in range(4) if mask>>a&1) for mask in range(1,16)]
            zs=[sum(max(0,d[a]-1) for a in range(4) if mask>>a&1) for mask in range(1,16)]
            ls=[hh>>j&1 for j in range(6)]
            scores.append(ds+zs+ls)
        result[i]=(tuple(min(r[j] for r in scores) for j in range(36)),
                   tuple(max(r[j] for r in scores) for j in range(36)),len(allowed))
    return result

def row_check(counts,N,D,L,immutable):
    bounds=extrema(tuple(N),immutable);used=[i for i,n in enumerate(counts) if n]
    absent=[i for i in used if bounds.get(i) is None]
    if absent:return dict(reason='empty_common_physical_domain',type=absent[0])
    targets=[sum(D[a] for a in range(4) if mask>>a&1) for mask in range(1,16)]
    targets += [sum(D[a]-N[a] for a in range(4) if mask>>a&1) for mask in range(1,16)]
    targets += list(L)
    # Independent ordering: all36 common-domain scores, then two orientations.
    checks=[]
    for j,target in enumerate(targets):
        lo=sum(counts[i]*bounds[i][0][j] for i in used)
        hi=sum(counts[i]*bounds[i][1][j] for i in used)
        if target<lo or target>hi:
            return dict(reason='common_row_integer_bound',score=j,target=target,lower=lo,upper=hi)
        checks.append((target,lo,hi))
    return dict(reason='UNEXCLUDED',complete_bounds=checks)

def run(start,stop):
    began=time.monotonic();populations=json.loads((P/'census22.json').read_text())['survivors']
    physical_rows=physical();tables=option_tables(physical_rows)
    need(tables[1]==tables[2]==tables[3],'joint role transports make all light coordinate relaxations equal')
    immutable=tuple((i,tuple(rows)) for i,rows in sorted(physical_rows.items()))
    labelled,canonical=carriers();records=[];choices=[];summary=collections.Counter()
    for ordinal in range(start,min(stop,len(populations))):
        pop=populations[ordinal];counts=pop['counts'];K=pop['branch']['K'];cache={}
        per=[]
        for ci,(lam,D,L) in enumerate(canonical):
            nsets=[]
            for a in range(4):
                key=(a==0,D[a])
                if key not in cache:cache[key]=column(counts,tables[0 if a==0 else 1],D[a])
                nsets.append(cache[key])
            good=[]
            for N in it.product(*nsets):
                if sum(N)!=K or any(N[a]+N[b]<l for (a,b),l in zip(PAIRS,L)):continue
                capacity=sum(min(N[a],D[a]-N[a]) for a in range(4) if N[a]>=5)
                if counts[18]>capacity:proof=dict(reason='weighted_C_capacity',demand=counts[18],capacity=capacity)
                else:proof=row_check(counts,N,D,L,immutable)
                need(proof['reason']!='UNEXCLUDED','actual necessary choice not excluded; no absence conclusion')
                summary[proof['reason']]+=1
                item=dict(ordinal=ordinal,carrier=ci,N=N,proof=proof)
                good.append(item);choices.append(item)
            per.append(dict(carrier=ci,coordinate_support_sets=nsets,complete_choices=good))
            summary['carrier_population_records']+=1
        if any(r['complete_choices'] for r in per):summary['positive_populations']+=1
        records.append(dict(ordinal=ordinal,branch=pop['branch'],counts=counts,carriers=per))
        if time.monotonic()-began>45:raise RuntimeError('INCOMPLETE fixed45-second64-population column phase guard')
    result=dict(start=start,stop=min(stop,len(populations)),labelled_carriers=labelled,canonical_carriers=canonical,
                records=records,summary=summary)
    out=P/'column-phases';out.mkdir(exist_ok=True)
    (out/('%05d.json'%start)).write_bytes(enc(result))
    print(json.dumps(dict(start=start,stop=result['stop'],seconds=time.monotonic()-began,summary=summary),sort_keys=True),flush=True)

if __name__=='__main__':run(int(sys.argv[1]),int(sys.argv[2]))
