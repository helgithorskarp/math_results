"""All-five-hub-set/bit-leave owner compiler. six-code-1, researcher."""
from collections import Counter
import itertools as it
import time

PAIRS=tuple(it.combinations(range(5),2))
ALL=(1<<17)-1

def need(ok,msg):
    if not ok: raise ValueError(msg)

def bits(mask): return tuple(a for a in range(17) if mask>>a&1)

def compile_fixture(words,fi):
    begin=time.monotonic();blocks=[sum(1<<p for p in w) for w in words]
    need(len(blocks)==len(set(blocks))==20,'twenty distinct blocks')
    covered=[0]*17;rep=[0]*17
    for w,mask in zip(words,blocks):
        need(len(w)==len(set(w))==4 and all(type(p)is int and 0<=p<17 for p in w),'literal points')
        for a in w:
            rep[a]+=1
            need(not(covered[a]&(mask^(1<<a))),'simple pairs')
            covered[a]|=mask^(1<<a)
    delta=[5-r for r in rep];high=sum(1<<a for a,d in enumerate(delta) if d)
    low=ALL^high;adj=[ALL^covered[a]^(1<<a) for a in range(17)]
    need(min(delta)>=0 and sum(delta)==5,'deficit mass')
    need(sum(v.bit_count() for v in adj)==32,'sixteen leave edges')
    need(all(v.bit_count()==1+3*delta[a] for a,v in enumerate(adj)),'leave degrees')
    need(all(not(adj[a]&low) for a in bits(low)),'no LOW-LOW')
    hh=[(a,b) for a,b in it.combinations(bits(high),2) if adj[a]>>b&1]
    isolated=sum(1<<a for a in bits(high) if not(adj[a]&high))
    need(len(hh)==high.bit_count()-1,'HIGH forest edge count')
    records=[];positive_marks={};cap_count=0;counts=Counter()
    for index,H in enumerate(it.combinations(range(17),5),1):
        need(index<=100000 and time.monotonic()-begin<=10,'INCOMPLETE fixed100000-state/10s fixture guard')
        counts['all_H5']+=1;mask=sum(1<<a for a in H)
        if max(delta)>2:
            counts['deficit_cap_reject']+=1;continue
        low_sat=low&~mask
        if any(delta[a]+(adj[a]&low_sat).bit_count()>5 for a in bits(high)):
            counts['propagation_reject']+=1;continue
        cap_count+=1;hm=mask&high;k=hm.bit_count();e=5-high.bit_count()
        q=sum(bool(hm&((1<<a)|(1<<b))) for a,b in hh)
        eligible=bool(hm&isolated);sat_high=high&~mask
        g1=sum(delta[a]==1 for a in bits(sat_high));sigma=sum(delta[a]-1 for a in bits(sat_high))
        weight=sum(delta[a] for a in H);psi=g1 if e==0 and eligible else -g1 if e and not eligible else 0
        I5=int(e==0 and k==5)
        coords=(e,k,q,eligible,high.bit_count(),g1,psi,psi-3*(k-e-q)+3*I5,sigma,I5,weight)
        positive_marks[hm]=coords
        hub_sizes=[(b&mask).bit_count() for b in blocks]
        if 4 in hub_sizes:
            counts['four_hub_block']+=1;continue
        owned=[i for i,v in enumerate(hub_sizes) if v==3]
        if len(owned)!=1:
            counts['owner_count_'+str(len(owned))]+=1;continue
        ow=blocks[owned[0]];A=bits(ow&mask);mate=bits(ow&~mask)[0]
        fs=tuple(bits(adj[a]&low_sat) for a in H)
        leaves=tuple((a,b) for a,b in it.combinations(H,2) if adj[a]>>b&1)
        mleave=tuple(a for a in H if adj[a]>>mate&1)
        for a in A:
            need(mate not in fs[H.index(a)] and not(adj[a]&(ow^(1<<a))),'actual owned word covers mates')
            if delta[a]:
                need(len(fs[H.index(a)])>=max(0,4*delta[a]+k+delta[mate]-7),'new mate-aware support bridge')
        record=dict(fixture=fi,H=H,A=A,mate=mate,delta=tuple(delta[a] for a in H),
                    friends=fs,HH_leave=leaves,mate_leave=mleave,z=delta[mate],coordinates=coords)
        records.append(record);counts['owned_retained']+=1
    return records,dict(counts),cap_count,[(fi,bits(hm),c) for hm,c in sorted(positive_marks.items())]

def labelled(records):
    frequencies=Counter();minimum={}
    for r in records:
        H=r['H'];A=r['A'];B=tuple(a for a in H if a not in A)
        positions={a:j for j,a in enumerate(H)}
        for left in it.permutations(A):
            for right in it.permutations(B):
                roles=left+right
                d=tuple(r['delta'][positions[a]] for a in roles)
                f=tuple(len(r['friends'][positions[a]]) for a in roles)
                edge_set=set(r['HH_leave'])
                hh=sum(1<<j for j,(a,b) in enumerate(PAIRS) if tuple(sorted((roles[a],roles[b]))) in edge_set)
                ml=sum(1<<a for a,p in enumerate(roles) if p in r['mate_leave'])
                key=(d,f,hh,r['z'],ml,r['coordinates'])
                witness=(r['fixture'],H,r['mate'],roles)
                frequencies[key]+=1
                if key not in minimum or witness<minimum[key]: minimum[key]=witness
    return [(key,frequencies[key],minimum[key]) for key in sorted(frequencies)]
