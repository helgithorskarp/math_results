"""Definition-based checks; no target imports, external fixtures or hash gate.

These are semantic/release checks, not a third independent mathematical proof.
The two primary kernels and this checker share the written model's definitions.
"""
import itertools, math

F=tuple(t for t in range(180) if t%9!=3)
D=tuple(d for d in range(1,721)if 720%d==0 and d not in(1,2,4))
E={d:d//math.gcd(d,4)for d in D}

def need(ok,why):
    if not ok:raise ValueError(why)

def native(d,s,b,points):
    need(d in D and s in range(5)and b in range(d),'original native coordinates')
    want=tuple(t for t in F if (4*t+3-b)%d==0)
    need(tuple(points)==want,'original phase footprint, including inactive phases')

def inventory(q,removed,pool):
    need(len(q)==4 and q[0]in(3,6,12)and q[1]in(9,18,36)and q[2:]==[24,720],'entire Q labels')
    want=[d for d in D if d not in set(q)|set(removed)]
    need(pool==want,'distinct original labels and exact remaining inventory')

def assignment(rows):
    spent=set()
    for d,s,b in rows:
        need(d in D and s in range(5)and(b is None or b in range(d)),'original owner/phase')
        need(d not in spent,'one globally assigned owner per original')
        spent.add(d)

def qsize(state,one,size):
    need(len(state)==3 and all(r in range(-1,e)for r,e in zip(state,(3,9,6))),'Q phases and omission')
    need(one is None or one in range(180),'singleton phase')
    points={t for t in F if any(r>=0 and t%e==r for r,e in zip(state,(3,9,6)))}
    if one in F:points.add(one)
    need(size==len(points),'Q actual union, including omission and inactive singleton')

def gap(v,h,p,points):
    need(p in(0,1)and h in range(4)and h%2!=p,'opposite binary arm')
    want=tuple(t for t in F if t%9==v and t%4==(h+2)%4)
    need(tuple(points)==want and len(want)==5 and len({t%5 for t in want})==5,'mandatory five-point transversal')

def supplemental(W,T,budget=23):
    need(set(W)<=set(F)and set(T)<=set(F),'supplemental domain')
    need(len(set(W)&set(T))<=budget,'supplemental intersection budget')

def verify(record):
    domain=record['domain'];need(domain['F']==list(F)and domain['originals']==list(D),'complete domain/original aliases')
    need({int(k):v for k,v in domain['projected'].items()}==E,'all original projections')
    maps=record['native_maps'];need([(d,s)for d,s,_ in maps]==list(itertools.product(D,range(5))),'all original owners')
    for d,s,phases in maps:
        need(len(phases)==d,'all original native phases')
        for b,points in enumerate(phases):native(d,s,b,points)
    states=list(itertools.product(range(-1,3),range(-1,9),range(-1,6)))
    need(record['Q_states']==[list(s)for s in states]and len(record['Q_sizes'])==len(states),'all Q states')
    for state,row in zip(states,record['Q_sizes']):
        need(len(row)==181,'all singleton phases with omission')
        for j,value in enumerate(row):qsize(state,None if j==0 else j-1,value)
    large=record['large_Q_size_histogram'];need({int(k):v for k,v in large.items()}=={110:8,111:400}and record['Q_small_max']==101,'Q large classification')
    pools=record['pools'];need([p['Q']for p in pools]==[[x,y,24,720]for x,y in itertools.product((3,6,12),(9,18,36))],'all nine Q original inventories')
    for pool in pools:
        for key,remove in [('four',[8,16,48,144]),('triple',[8,16,48]),('alternate',[8,16,48,72])]:inventory(pool['Q'],remove,pool[key])
    bs=list(itertools.product(range(-1,2),range(-1,4),range(-1,12)));need(record['binary_states']==[list(s)for s in bs],'all binary states including omissions')
    phase={d:[frozenset(t for t in F if t%E[d]==r)for r in range(E[d])]for d in D}
    catalogue={}
    for a,u,p in itertools.product((1,2),(0,6),(0,1)):
        base={t for t in F if t%3==a or t%9==u or(t%3==3-a and t%2==p)}
        need(len(base)==110,'ordinary large-Q shape')
        for z in set(F)-base:catalogue[(a,u,p,z)]=frozenset(base|{z})
    rr=record['records'];need([tuple(r['parameters'])for r in rr]==sorted(catalogue),'complete target parameter catalogue')
    capacity_entries=gap_entries=binary_entries=0;forced=0;bad=structural=0;affordable=set()
    for r in rr:
        a,u,p,z=r['parameters'];T=catalogue[(a,u,p,z)];need(r['points']==sorted(T),'entire target')
        cap={int(d):xs for d,xs in r['phase_capacities'].items()};need(set(cap)==set(D),'all original capacity vectors')
        for d in D:
            need(cap[d]==[len(T&c)for c in phase[d]],'entire original capacity vector')
            capacity_entries+=len(cap[d])
        credit={d:max(cap[d])for d in D}
        want_sums=[[sum(credit[d]for d in pool[k])for k in('four','triple','alternate')]for pool in pools]
        need(r['pool_sums']==want_sums,'all nine resource pool sums')
        parity=0 if z%2!=p else 1
        need(all(s==([319,324,314]if parity==0 else[321,326,316])for s in want_sums),'ordinary phase-capacity totals')
        sizes=[];local_bad=local_structural=0
        for r2,r4,r12 in bs:
            k=sum((r2>=0 and t%2==r2)or(r4>=0 and t%4==r4)or(r12>=0 and t%12==r12)for t in T);sizes.append(k)
            good=r2==p and r4>=0 and r4%2!=p and r12>=0 and r12%4==(r4+2)%4
            strong=good and r12%3==a
            if not good:local_structural=max(local_structural,k)
            if not strong:local_bad=max(local_bad,k)
            else:forced+=1
        binary_entries+=len(sizes);need(r['binary_sizes']==sizes and r['bad_binary_max']==local_bad and r['structural_bad_max']==local_structural,'complete binary union cardinalities')
        bad=max(bad,local_bad);structural=max(structural,local_structural)
        gr=r['repair_rows'];want_keys=[(h,v)for h in range(4)if h%2!=p for v in(u,a)]
        need([(g['h'],g['v'])for g in gr]==want_keys,'both repair rows and arms')
        for g in gr:
            gap(g['v'],g['h'],p,g['points']);G=frozenset(g['points']);counts={int(d):xs for d,xs in g['phase_intersections'].items()};need(set(counts)==set(D),'every gap original')
            for d in D:
                need(counts[d]==[len(G&c)for c in phase[d]],'entire gap phase intersections');gap_entries+=len(counts[d])
        affordable.update(d for d in pools[0]['triple']if credit[d]<=16 and E[d]%5)
        cheap=sorted((credit[d],d)for d in pools[0]['triple']if E[d]%5==0)[:5]
        need(sum(v for v,d in cheap)==17,'five distinct affordable repair resources cost17')
        A={t for t in T if t%3==a}
        for d in pools[0]['four']:
            if E[d]==15:need(max(len(T&c)for c in phase[d]if len(A&c)==0)<=(7 if parity==0 else 6),'non-A e15 loss')
            if E[d]==5:need(all(len(A&c)==12 for c in phase[d]),'five columns each meet full colour in12')
            if E[d]==10:need(all(len(A&c)==6 for c in phase[d]),'e10 unavoidable six-point overlap')
    summary=record['summary']
    need(summary=={'native_original_phase_owner_maps':sum(d*5 for d in D),'Q_states_with_omission':len(states)*181,'targets':len(catalogue),'opposite_extra_targets':320,'binary_states_with_omission':binary_entries,'forced_active_binary_states':forced,'bad_binary_max':bad,'structural_bad_max':structural,'all_original_G_phase_entries':gap_entries,'affordable_nonfive':sorted(affordable)},'all aggregate summaries')
    need(capacity_entries==279600 and gap_entries==1118400 and binary_entries==78000,'full checked populations')
    return {'status':'COMPLETE_DEFINITION_BASED_CHECKS','native_maps':12055,'Q_states':50680,'targets':400,'capacity_entries':capacity_entries,'binary_entries':binary_entries,'gap_entries':gap_entries,'shared_model_definitions':True}
