"""Exact complete necessary original-label cover. six-tammes-1 researcher."""
from itertools import combinations,permutations,product
from collections import Counter
import json

FANS=((0,1,2,3,4,5),(7,6,8,9,10,11));EARS=(1,5,6,11);OUT=(12,13,14)
TS=((0,1,2),(0,2,3),(0,3,4),(0,4,5),(7,6,8),(7,8,9),(7,9,10),(7,10,11))
TRIS=tuple(combinations(EARS+OUT,3))
def need(x,m):
    if not x:raise ValueError(m)
def edges(faces):return {tuple(sorted((t[k],t[(k+1)%len(t)]))) for t in faces for k in range(len(t))}
def maps():
    group=[]
    for a,b,swap in product((False,True),repeat=3):
        for order in permutations(OUT):
            m={i:i for i in range(15)}
            if a:m.update({1:5,5:1,2:4,4:2})
            if b:m.update({6:11,11:6,8:10,10:8})
            if swap:
                s={x:y for u,v in zip(FANS[0],FANS[1]) for x,y in ((u,v),(v,u))}
                m={x:s.get(y,y) for x,y in m.items()}
            m.update(dict(zip(OUT,order)));group.append(m)
    need(len({tuple(m[i] for i in range(15)) for m in group})==48,'48 actual label automorphisms')
    fixed={tuple(sorted(t)) for t in TS}
    for m in group:need({tuple(sorted(m[i] for i in t)) for t in TS}==fixed,'fan-face automorphism')
    return group
GROUP=maps()
def canonical(case):
    result=[];types=case['types'];opp={0:case['QA'],7:case['QB']}
    for m in GROUP:
        roles=['']*15
        for i,t in enumerate(types):roles[m[i]]=t
        q={m[f]:m[a] for f,a in opp.items()}
        free=tuple(sorted(tuple(sorted(m[i] for i in t)) for t in case['free_Ts']))
        result.append((case['p'],tuple(roles),(q[0],q[7]),free))
    return min(result)
def reject(case,stage):
    qa,qb=case['QA'],case['QB'];types=case['types'];free=case['free_Ts'];faces=list(TS)+list(free)+[(0,1,qa,5),(7,6,qb,11)]
    E=edges(faces);nb={i:{v for e in E if i in e for v in e if v!=i} for i in range(15)}
    if stage>=1 and (types[qa] not in ('D','U') or types[qb] not in ('D','U')):return 'opposite_x_cannot_R'
    if stage>=2 and any(len(nb[i])>(5 if i in (0,7) else 4) for i in nb):return 'prescribed_contact_degree'
    if stage>=3 and any(tuple(sorted(e)) in E for e in ((1,5),(6,11))):return 'same_fan_ears_noncontact'
    return None
def run():
    allcases=[];rolecounts=Counter();paircounts=Counter()
    for p in (0,1,2):
        for k in range(5):
            d=k-2*p;u=p;r=3-k+p
            if min(d,u,r)<0:continue
            for promoted in combinations(EARS,k):
                for Ds in combinations(OUT,d):
                    for Us in combinations(tuple(v for v in OUT if v not in Ds),u):
                        types=['R']*15
                        for f in (0,7):types[f]='F'
                        for e in EARS:types[e]='R' if e in promoted else 'D'
                        for v in OUT:types[v]='D' if v in Ds else 'U' if v in Us else 'R'
                        need(Counter(types)==Counter({'F':2,'D':4-2*p,'U':p,'R':9+p}),'complete degree4 T-role budget')
                        target={v:(1 if v in promoted else 0) for v in EARS}
                        target.update({v:(0 if types[v]=='U' else 1 if types[v]=='D' else 2) for v in OUT})
                        rolecounts[(p,k)]+=1
                        for free in combinations(TRIS,2):
                            count=Counter(v for tri in free for v in tri)
                            if any(count[v]!=target[v] for v in target):continue
                            paircounts[(p,k)]+=1
                            for qa,qb in product((6,11,12,13,14),(1,5,12,13,14)):
                                allcases.append({'p':p,'k':k,'types':types[:],'QA':qa,'QB':qb,'free_Ts':free})
    stages=[];survive=allcases
    for stage in range(1,4):
        counts=Counter();kept=[]
        for case in survive:
            reason=reject(case,stage)
            if reason:counts[reason]+=1
            else:kept.append(case)
        stages.append({'stage':stage,'before':len(survive),'after':len(kept),'rejections':dict(counts)})
        survive=kept
    canon={canonical(c) for c in survive}
    out={'agent':'six-tammes-1','role':'researcher','status':'Complete necessary original-label cover, NOT full contact-graph enumeration',
         'rolecounts':{str(k):v for k,v in sorted(rolecounts.items())},'free_T_pair_counts':{str(k):v for k,v in sorted(paircounts.items())},
         'raw_cases':len(allcases),'stages':stages,'surviving_labelled_cases':len(survive),
         'survivor_counts':{str(k):v for k,v in Counter((c['p'],c['k']) for c in survive).items()},
         'canonical_case_count':len(canon),'canonical_cases':sorted(canon),
         'survivors':survive}
    need(len(allcases)==5875 and len(survive)==24 and len(canon)==1,'finite cover counts')
    need(Counter((c['p'],c['k']) for c in survive)=={(0,2):24},'one p/k incidence case')
    return out
if __name__=='__main__':
    print(json.dumps({k:v for k,v in run().items() if k not in ('survivors','seconds')},indent=2,sort_keys=True))
