"""Owned-block/mate/point-incidence compiler; no producer import."""
from collections import Counter
import itertools as it
import math
import time

def check(ok,msg):
    if not ok: raise ValueError(msg)

def compile_fixture(words,fi):
    start=time.monotonic();universe=set(range(17));blocks=[frozenset(w) for w in words]
    check(len(blocks)==len(set(blocks))==20 and all(len(b)==4 and b<=universe for b in blocks),'literal blocks')
    rep={a:sum(a in b for b in blocks) for a in universe};defect={a:5-rep[a] for a in universe}
    incident=Counter(frozenset(p) for b in blocks for p in it.combinations(b,2))
    check(len(incident)==120 and all(n==1 for n in incident.values()),'unique pairs')
    leave={frozenset(p) for p in it.combinations(range(17),2) if frozenset(p) not in incident}
    high={a for a,d in defect.items() if d};low=universe-high
    adjacent={a:{b for b in universe if frozenset((a,b)) in leave} for a in universe}
    check(sum(defect.values())==5 and len(leave)==16,'mass and edge count')
    check(all(len(adjacent[a])==1+3*defect[a] for a in universe),'degrees')
    check(all(b&high for b in leave),'every leave edge meets HIGH')
    high_pairs=[p for p in leave if p<=high];isolated={a for a in high if not any(a in p for p in high_pairs)}
    check(len(high_pairs)==len(high)-1,'HIGH edge count')
    coords={};baseline=0;raw_marks=0
    # Independent LOW-bucket coefficient compiler covers all physical H5
    # placements before any owned-word restriction.
    for size in range(len(high)+1):
        for marked in it.combinations(sorted(high),size):
            raw_marks+=1;slots=5-size
            if slots<0 or max(defect.values())>2: continue
            poly=[1]+[0]*slots
            for a in sorted(high):
                bucket=adjacent[a]&low
                required=max(0,1+4*defect[a]-len(adjacent[a]&high)-5)
                nxt=[0]*(slots+1)
                for used,coefficient in enumerate(poly):
                    for count in range(required,min(len(bucket),slots-used)+1):
                        nxt[used+count]+=coefficient*math.comb(len(bucket),count)
                poly=nxt
            if not poly[slots]:continue
            check(all(sum(a in adjacent[b] for b in high)==1 for a in low),'partition of LOW buckets')
            hubs=set(marked);saturated=high-hubs;excess=5-len(high)
            touch=sum(bool(p&hubs) for p in high_pairs)
            eligible=bool(hubs&isolated);units=sum(defect[a]==1 for a in saturated)
            sigma=sum(defect[a]-1 for a in saturated);weight=sum(defect[a] for a in hubs)
            psi=units if excess==0 and eligible else -units if excess and not eligible else 0
            fifth=int(excess==0 and size==5)
            coord=(excess,size,touch,eligible,len(high),units,psi,psi-3*(size-excess-touch)+3*fifth,sigma,fifth,weight)
            coords[tuple(marked)]=coord;baseline+=poly[slots]
    accepted={};routes=0;cap2=max(defect.values())<=2
    # Any uniquely owned triple has one and only one (block,mate,other-H)
    # representation below; no actual-code automorphism is assumed.
    for owned_block in blocks:
        for mate in sorted(owned_block):
            A=owned_block-{mate}
            for extra in it.combinations(sorted(universe-owned_block),2):
                routes+=1
                check(routes<=100000 and time.monotonic()-start<=10,'INCOMPLETE fixed100000-state/10s oracle fixture guard')
                if not cap2:continue
                H=A|set(extra)
                if any(defect[a]+len(adjacent[a]&(low-H))>5 for a in high):continue
                sizes=[len(b&H) for b in blocks]
                if any(v==4 for v in sizes) or sizes.count(3)!=1:continue
                hs=tuple(sorted(H));check(hs not in accepted,'unique owned-block representation')
                friends=tuple(tuple(sorted(adjacent[a]&(low-H))) for a in hs)
                row=coords[tuple(sorted(H&high))]
                record=dict(fixture=fi,H=hs,A=tuple(sorted(A)),mate=mate,
                    delta=tuple(defect[a] for a in hs),friends=friends,
                    HH_leave=tuple((a,b) for a,b in it.combinations(hs,2) if frozenset((a,b)) in leave),
                    mate_leave=tuple(a for a in hs if mate in adjacent[a]),z=defect[mate],coordinates=row)
                for a in A:
                    check(all(frozenset((a,b)) in incident for b in owned_block if b!=a),'owned pairs covered')
                    if defect[a]:check(len(friends[hs.index(a)])>=max(0,4*defect[a]+len(H&high)+defect[mate]-7),'mate support lower bound')
                accepted[hs]=record
    check(routes==6240,'all owned block/mate/extra routes')
    return [accepted[h] for h in sorted(accepted)],baseline,raw_marks,[(fi,h,coords[h]) for h in sorted(coords)]

def labelled(records):
    table={}
    for r in records:
        position={a:i for i,a in enumerate(r['H'])}
        leftover=sorted(set(r['H'])-set(r['A']))
        orders=[p+q for p in it.permutations(r['A']) for q in (tuple(leftover),tuple(reversed(leftover)))]
        for roles in orders:
            d=tuple(r['delta'][position[a]] for a in roles)
            f=tuple(len(r['friends'][position[a]]) for a in roles)
            pairs=[{a,b} for a,b in r['HH_leave']]
            mask=0;j=0
            for a in range(5):
                for b in range(a+1,5):
                    if {roles[a],roles[b]} in pairs:mask+=2**j
                    j+=1
            mate=sum(2**a for a in range(5) if roles[a] in r['mate_leave'])
            key=(d,f,mask,r['z'],mate,r['coordinates'])
            witness=(r['fixture'],r['H'],r['mate'],roles)
            if key not in table:table[key]=[0,witness]
            table[key][0]+=1
            table[key][1]=min(witness,table[key][1])
    return [(key,table[key][0],table[key][1]) for key in sorted(table)]
