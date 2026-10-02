"""Exact T2 exclusion kernels; actual six-code-1, researcher."""
from collections import Counter
import hashlib
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
import time
HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/"five_hub_pair_total36"
PAIRS=tuple(it.combinations(range(5),2))
PATTERNS=(("T1",((0,1,2),)),("T2_shared_one",((0,1,2),(0,3,4))),("T2_shared_pair",((0,1,2),(0,1,3))))
BTYPE=(1,1,0,True,4,3,0,0,0,0,2)

def need(ok, message):
    if not ok:
        raise ValueError(message)

def enc(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()

def compositions(n, k):
    if k == 1:
        yield (n,)
        return
    for a in range(n + 1):
        for rest in compositions(n - a, k - 1):
            yield (a,) + rest

def pair_carrier():
    records = []
    for name, triples in PATTERNS:
        t = tuple(sum(set(p) <= set(tri) for tri in triples) for p in PAIRS)
        Ta = tuple(sum(a in tri for tri in triples) for a in range(5))
        modes = [("all_le4", None, 3)]
        if name == "T2_shared_pair":
            modes.append(("common_pair5", PAIRS.index((0, 1)), 4))
        for mode, special, total in modes:
            roles = tuple(j for j in range(10) if j != special)
            begin = time.monotonic()
            nodes = 0
            for u in compositions(total, len(roles)):
                nodes += 1
                need(nodes <= 100000 and time.monotonic() - begin <= 10,
                     "INCOMPLETE fixed100000-state/10s pair guard")
                lam = [4] * 10
                if special is not None:
                    lam[special] = 5
                for j, deficit in zip(roles, u):
                    lam[j] -= deficit
                D = tuple(sum(lam[j] for j, p in enumerate(PAIRS) if a in p) - 11
                          for a in range(5))
                L = tuple(13 - 3 * v + t[j] for j, v in enumerate(lam))
                reason = "PAIR_FEASIBLE"
                if any(v < t[j] or v < 0 or L[j] < 0 for j, v in enumerate(lam)):
                    reason = "ACTUAL_HH_HHH_QUOTA"
                elif any(3 * D[a] < 3 + Ta[a] for a in range(5)):
                    reason = "Z_EDGES_NONNEGATIVE"
                elif any(D[a] + D[b] > 11 for a, b in PAIRS):
                    reason = "PAIR_COLUMN11"
                elif any(L[j] > D[a] + D[b] for j, (a, b) in enumerate(PAIRS)):
                    reason = "HH_HIGH_ENDPOINT_WEIGHT"
                records.append(dict(pattern=name, triples=triples, mode=mode,
                                    lam=lam, t=t, Ta=Ta, D=D, L=L, reason=reason))
    return records

def column_carrier(record):
    if record["reason"] != "PAIR_FEASIBLE":
        return []
    D, lam, t, L = (record[k] for k in ("D", "lam", "t", "L"))
    out = []
    for N in it.product(*(range((d + 1) // 2, d + 1) for d in D)):
        if any(L[j] > N[a] + N[b] for j, (a, b) in enumerate(PAIRS)):
            continue
        good = True
        for j, (a, b) in enumerate(PAIRS):
            J = set(range(5)) - {a, b}
            lost_triples = sum(t[i] for i, p in enumerate(PAIRS) if set(p) <= J)
            lost_support = 2 * sum(D[c] - N[c] for c in J)
            if 5 * (D[a] + D[b]) > 44 + 3 * lam[j] - lost_triples - lost_support:
                good = False
                break
        if good:
            out.append(dict(N=N, n=tuple(d - n for d, n in zip(D, N)), K=sum(N)))
    return out

def frozen(name):
    sha=dict(producer='2e1df2b5a12fcead9bcff37352105e57d882a683c95e698f38db247f8b34818a',
             oracle='19a2c993dd642d8bff3c518e864c105fa9f400e4607db0dc4e3753e22ff3cb2b')[name]
    path=PARENT/(name+'.py');need(hashlib.sha256(path.read_bytes()).hexdigest()==sha,'changed frozen engine')
    spec=importlib.util.spec_from_file_location('pass16_'+name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def actual_marks(p,literal):
    raw,_=p.rows_and_physical_bridge(literal);records=[];selected=[]
    for fi,words in enumerate(literal['stars']):
        mult=Counter(a for w in words for a in w)
        delta={a:5-mult[a] for a in range(17)}
        high={a for a,d in delta.items() if d};low=set(range(17))-high
        covered={frozenset(pair) for w in words for pair in it.combinations(w,2)}
        adj={a:{b for b in range(17) if a!=b and frozenset((a,b)) not in covered} for a in range(17)}
        hnames=sorted(high);lnames=sorted(low)
        for row in (r for r in raw if r['fixture']==fi):
            hs=set(row['hub_high']);slots=5-len(hs)
            req={a:max(0,1+4*delta[a]-len(adj[a]&high)-(6 if a in hs else 5)) for a in high}
            buckets={a:sorted(adj[a]&low) for a in high}
            need(all(sum(b in buckets[a] for a in high)==1 for b in low),'actual disjoint LOW buckets')
            algebra=0
            if all(delta[a]<=2 for a in high):
                factors=[1]+[0]*slots
                for a in hnames:
                    nxt=[0]*(slots+1)
                    for used,count in enumerate(factors):
                        for n in range(req[a],min(len(buckets[a]),slots-used)+1):
                            nxt[used+n]+=count*math.comb(len(buckets[a]),n)
                    factors=nxt
                algebra=factors[slots]
            direct=0
            if all(delta[a]<=2 for a in high):
                for chosen in it.combinations(lnames,slots):
                    H=hs|set(chosen)
                    # Actual friend names are LOW points assigned to S.
                    if all(delta[a]+len(adj[a]&(low-H))<=(6 if a in hs else 5) for a in high):
                        direct+=1
            need(algebra==direct,'all426 literal-name and bucket counts agree')
            r=dict(fixture=fi,hub_high=row['hub_high'],coordinates=row['coordinates'],cap6_LOW_completions=algebra)
            records.append(r)
            if algebra:selected.append(row)
    need(len(records)==426,'all raw HIGH marks retained in coverage')
    types=sorted({tuple(r['coordinates']) for r in selected})
    return records,types

def full_cases():
    out=[]
    for X in range(6):
        for tau in range((11-2*X)//4+1):
            for Q in range(12-2*X-4*tau):
                E=15-2*tau-Q;K=4+2*tau+Q+2*X
                out.append(dict(T=2,X=X,tau=tau,N5=0,Q=Q,E=E,K=K,
                                margin_budget=3*(11-2*X-4*tau-Q)))
    other=[]
    for X,tau,Q in it.product(range(8),range(4),range(16)):
        if 4+2*X+4*tau+Q<=15:
            other.append(dict(T=2,X=X,tau=tau,N5=0,Q=Q,E=15-2*tau-Q,
                              K=4+2*tau+Q+2*X,margin_budget=3*(11-2*X-4*tau-Q)))
    need(out==other and len(out)==68,'complete necessary capacity domain, no unconditional surcharge')
    return out

def slot_matching(types,vector,r,c,covered_pair=True):
    heavy=[]
    for t,count in zip(types,vector):
        for _ in range(count*(t[10]-t[1])):heavy.append((t[1],t[2]))
    capacities=[d-n for d,n in zip(r['D'],c['N'])]
    slots=[a for a,n in enumerate(capacities) for _ in range(n)]
    need(len(slots)==len(heavy),'each actual heavy hub entry has one capacity slot')
    common={a for j,pair in enumerate(PAIRS) if r['lam'][j]==5 for a in pair}
    edges=[]
    for k,q in heavy:
        options=[]
        for index,a in enumerate(slots):
            # At k1 the mate of an always-covered HH pair is LOW and
            # is unavailable as a LOW hub leave friend.
            unavailable=int(covered_pair and k==1 and a in common)
            friends=max(0,7-q-(5-k-unavailable))
            if c['N'][a]>=1+friends:options.append(index)
        edges.append(options)
    assigned=[-1]*len(slots)
    def augment(v,seen):
        for slot in edges[v]:
            if slot in seen:continue
            seen.add(slot)
            if assigned[slot]<0 or augment(assigned[slot],seen):
                assigned[slot]=v;return True
        return False
    order=sorted(range(len(heavy)),key=lambda v:(len(edges[v]),v))
    return all(augment(v,set()) for v in order)

def prior_certificate(types,vector,p):
    cert=p.certificate(types,vector)
    if cert['reason']!='OPEN':return dict(reason='FROZEN_ENDPOINT_RADIUS_OR_CLOSURE',cut=cert)
    rows=[t for t,n in zip(types,vector) for _ in range(n)]
    A=[t for t in rows if t[0]==0 and not t[3]]
    V=[t for t in rows if t[0]==0 and t[3]]
    B=[t for t in rows if t[0]>0 and t[3]]
    C=[t for t in rows if t[0]>0 and not t[3]]
    R=sum(t[0]==0 and t[1]==0 for t in rows)
    DA=sum(t[4]-t[1] for t in A);DV=sum(t[4]-t[1] for t in V)
    even=2*(sum(min(t[4]-t[1],len(A)-1) for t in A)//2)
    C1=sum(t[5] for t in C);required=DV+max(R,DA-even)
    if R and (V or B) and C1<required:
        return dict(reason='9538_ROOT_ENDPOINT_C1',R=R,D_A=DA,D_V=DV,I_even=even,C1=C1,required=required)
    b=sum(t==BTYPE for t in rows)
    if b>2:return dict(reason='9697_ACTUAL_B2_CAP',B_count=b)
    K=sum(t[1] for t in rows)
    return dict(reason='OPEN',K=K,B_count=b)

def check_vector(types,case,v):
    need(len(v)==len(types) and all(type(n) is int and n>=0 for n in v),"full nonnegative integer vector")
    totals=(sum(v),)+tuple(sum(n*t[i] for n,t in zip(v,types)) for i in (0,1,2,8,9,10))
    need(totals==(13,case["E"],case["K"],case["Q"],2*case["X"],0,19),"every exact total including hub weight")
    need(sum(n*t[7] for n,t in zip(v,types))<=case["margin_budget"],"corrected margin bound")
