"""Independent9665 audit; owned literal/row/DP inputs credited in CREDIT.
New full mark masks, focused cases, disjoint supports and degree-radius bridge.
No author9665 program or certificate is imported.
"""
import collections,hashlib,itertools as it,json,pathlib,time
import prior_dp as old
P=pathlib.Path(__file__).resolve().parent
old.P=P
need=old.need;enc=old.enc;sha=old.sha

def placements(stars,raw,types):
    rid={(r['star'],tuple(r['hubs'])):r for r in raw};ids={t:i for i,t in enumerate(types)}
    packed=bytearray(27370);used=collections.Counter();index=0;start=time.monotonic()
    for si,star in enumerate(stars):
        words=[set(w) for w in star];degree=[sum(a in w for w in words) for a in range(17)]
        delta=[5-d for d in degree];high={a for a in range(17) if delta[a]};low=set(range(17))-high
        pairs={tuple(ab) for w in words for ab in it.combinations(sorted(w),2)}
        adj=[{b for b in range(17) if b!=a and tuple(sorted((a,b))) not in pairs} for a in range(17)]
        friend={t:next(iter(adj[t])) for t in low}
        need(all(len(adj[t])==1 and friend[t] in high for t in low),'literal LOW unique HIGH friend')
        for Ht in it.combinations(range(17),4):
            H=set(Ht);sat=set(range(17))-H
            # First algorithm queries HIGH leave neighborhoods. The second
            # aggregates the unique friends of individual LOW SAT points.
            direct={a:len(adj[a]&low&sat) for a in high}
            inverse=collections.Counter(friend[t] for t in low&sat)
            need(all(direct[a]==inverse[a] for a in high),'every LOW-SAT friend count')
            r=rid[si,tuple(sorted(H&high))];tid=ids[tuple(r[f] for f in old.F)]
            for heavy in Ht:
                ok=all(delta[a]+direct[a]<=5+4*(2 if a==heavy else int(a in H)) for a in high)
                mask_ok=all(delta[a]+inverse[a]<=(13 if a==heavy else 9 if a in H else 5) for a in high)
                need(ok==mask_ok,'every full four-hub/heavy membership decision')
                if ok:packed[index//8]|=1<<(index%8);used[tid]+=1
                index+=1
            old.guard(start,index,218960,30)
    need(index==218960,'entire literal mark domain')
    result=dict(order='fixture; lexicographic 4-subset; heavy in subset order; bit i is byte i//8 bit i%8',marks=index,accepted=sum(used.values()),type_frequencies=dict(sorted(used.items())),membership_hex=packed.hex())
    (P/'PHYSICAL.json').write_bytes(enc(result))
    return result,set(used)

def cases():
    out=[]
    for T in (3,4):
        for Q,X,tau in it.product(range(13),range(7),range(4)):
            cost=Q+2*T+2*X+4*tau
            if cost<=12:
                E=18-Q-T-2*tau
                out.append(dict(T=T,Q=Q,X=X,tau=tau,E=E,K=24-E+2*X,budget=3*(12-cost)))
    return out

def description(t,hist):
    return dict(zip(old.F,t),w=5-sum((j+1)*c for j,c in enumerate(hist)),histogram=list(hist))

def final_cut(V):
    U,A,C,B,D,I,C1,R=old.metric(V)
    if D>I+C1:return dict(stage='unit_capacity',demand=D,internal_upper=I,cross_upper=C1)
    if U and not C:
        degrees=[sum(V[a][2]) for a in U]
        if sum(degrees)%2:return dict(stage='closed_unit_parity',degrees=degrees)
    # New ordinary lemma: disjoint positive hub columns and max degree Delta
    # imply m*(n-Delta^2)<=n, proved in REVIEW.md without classification.
    ds=[sum(v[2]) for v in V]
    if all(v[1][1]<=1 for v in V) and max(ds)<=3:
        return dict(stage='new_disjoint_radius',n=len(V),hubs=4,max_degree=max(ds),column_minimum=len(V)-max(ds)**2,required=4*(len(V)-max(ds)**2))
    count=collections.Counter()
    for _,t,h in V:
        w=5-sum((j+1)*c for j,c in enumerate(h))
        if t[0]==1 and t[1]==0:count['A']+=1
        elif t[0]==1 and t[1]==1 and w==2 and t[2] in (0,1):count['C' if t[2]==0 else 'J']+=1
        else:raise ValueError('unhandled necessary population')
    need(count['A']==2 and (count['C'],count['J']) in ((12,0),(11,1)),'complete residual support populations')
    return dict(stage='support',population=dict(count))

def compositions(n,k=4):
    if k==1:yield (n,);return
    for i in range(n+1):
        for tail in compositions(n-i,k-1):yield (i,)+tail

def support_check():
    targets=[(a,b,c,d) for a in range(5,14) for b,c,d in it.product(range(1,10),repeat=3) if a+b+c+d==24]
    records=[];traversed=0
    for Bt,Ct,Jt in ((0,12,0),(4,10,0),(0,11,1),(4,9,1)):
        prior=[];good=[];weak=[];start=time.monotonic();local=0
        for B,C,J in it.product(compositions(Bt),compositions(Ct),compositions(Jt)):
            local+=1;traversed+=1;old.guard(start,local,500000,20)
            D=tuple(b+2*c+2*j for b,c,j in zip(B,C,J));N=tuple(b+c+j for b,c,j in zip(B,C,J))
            if not (5<=D[0]<=13 and all(1<=d<=9 for d in D[1:])):continue
            record=dict(B=B,C=C,J=J,D=D,N=N)
            prior.append(record)
            if all((not b or n>=2) and (not c or n>=5) and (not j or n>=4) for b,c,j,n in zip(B,C,J,N)):good.append(record)
            if all((not b or n>=2) and (not c or n>=4) and (not j or n>=4) for b,c,j,n in zip(B,C,J,N)):weak.append(record)
        need(not good,'whole support allocation absence')
        records.append(dict(B=Bt,C=Ct,J=Jt,compositions=local,before_support=len(prior),degree_allocations=prior,after_support=good,weakened_C4=weak))
    need(len(targets)==489 and traversed==42721,'complete ordered targets and typed compositions')
    return dict(ordered_targets=targets,typed_compositions=traversed,populations=records)

def radius_controls():
    # Complete small simple graphs independently check the exact ball bound.
    checked=0;strict=0
    for n in range(1,6):
        edges=list(it.combinations(range(n),2))
        for mask in range(1<<len(edges)):
            adj=[set() for _ in range(n)]
            for i,(a,b) in enumerate(edges):
                if mask>>i&1:adj[a].add(b);adj[b].add(a)
            Delta=max(map(len,adj))
            for s in range(n):
                ball={s}|adj[s]|{v for u in adj[s] for v in adj[u]}
                neighbor_sum=sum(len(adj[u]) for u in adj[s])
                need(len(ball)<=1+neighbor_sum<=1+Delta**2,'exact two-step and uniform Moore upper bounds')
                checked+=1;strict+=int(len(ball)<1+neighbor_sum)
    # Petersen is a positive graph control saturating cubic radius10.
    adj=[set() for _ in range(10)]
    for i in range(5):
        for a,b in ((i,(i+1)%5),(i,i+5),(i+5,(i+2)%5+5)):
            adj[a].add(b);adj[b].add(a)
    balls=[]
    for s in range(10):
        ball={s}|adj[s]|{v for u in adj[s] for v in adj[u]};balls.append(len(ball))
    need(balls==[10]*10,'Petersen positive equality graph, not a packing')
    return dict(small_graph_root_checks=checked,strict_neighbor_sum= strict,petersen_balls=balls)

def build():
    stars,raw,types,hist=old.local();physical,accepted=placements(stars,raw,types)
    all_cases=[];stages=collections.Counter();surv=[]
    for case in cases():
        vectors,states=old.census(types,case,accepted);records=[]
        for v in vectors:
            V=old.expand_vertices(types,hist,v);bad=old.old_failures(V,old.potential(V))
            cut=dict(stage='prior',failures=bad) if bad else final_cut(V)
            stages[cut['stage']]+=1
            records.append(dict(counts=v,cut=cut))
            if not bad:surv.append(dict(case=case,counts=v,cut=cut))
        all_cases.append(dict(case=case,states=states,records=records))
    support=support_check()
    result=dict(types=[description(t,h) for t,h in zip(types,hist)],raw_rows=len(raw),raw_rows_sha=sha(raw),physical_sha=sha(physical),cases=all_cases,final_populations=surv,stages=dict(stages),radius_controls=radius_controls(),support_summary=[{k:r[k] for k in ('B','C','J','compositions','before_support')}|dict(feasible=len(r['after_support']),weak_C4=len(r['weakened_C4'])) for r in support['populations']])
    (P/'SUPPORT.json').write_bytes(enc(support));(P/'EVIDENCE.json').write_bytes(enc(result))
    print(json.dumps(dict(types=len(types),accepted_types=len(accepted),marks=physical['marks'],accepted=physical['accepted'],branches=len(all_cases),vectors=sum(len(c['records']) for c in all_cases),stages=dict(stages),support=result['support_summary'],sha256=sha(result),support_sha256=sha(support),physical_sha256=sha(physical)),indent=2))
    return result

if __name__=='__main__':build()
