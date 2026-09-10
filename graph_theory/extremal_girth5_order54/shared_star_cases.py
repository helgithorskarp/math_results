"""Complete common-vertex stars, with the remaining high pairs partitioned."""
from collections import Counter,defaultdict
from itertools import product
from shared_center_cases import cases,roles
from forest_profiles import profiles

def available(profile,index):
    a,b=profiles(5,2)[profile];six,seven,r,groups=roles(profile,index);I=six[0]|six[1]|set(seven)
    cs=[c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)]
    out=defaultdict(list)
    for v,c in enumerate(cs,13):
        if v not in I:out[(6 if v<30 else 7,c)].append(v)
    return dict(out)

def stars(profile,index):
    d,c,S,T=cases(profile)[index];A=available(profile,index);types=sorted(A);L=d-c;out=[]
    for matched in range(min(1,c-2)+1):
        total=9-c-matched
        def rec(i,left,weight,blocks):
            if i==len(types):
                if left or weight:return
                if matched:out.append((matched,(),tuple(blocks)));return
                counts=Counter(blocks);choices=[(t,min(n,2)) for t,n in sorted(counts.items()) if t[1]>=1]
                for marks in product(*(range(n+1) for t,n in choices)):
                    if sum(marks)!=2:continue
                    M=[];U=list(blocks)
                    for (t,n),k in zip(choices,marks):
                        for _ in range(k):M.append(t);U.remove(t)
                    out.append((matched,tuple(M),tuple(U)))
                return
            t=types[i];cc=t[1]
            for n in range(min(len(A[t]),left)+1):
                if cc*n>weight:break
                rec(i+1,left-n,weight-cc*n,blocks+[t]*n)
        rec(0,L,total,[])
    return sorted(set(out))

def star_roles(profile,index,star_index):
    matched,M,U=stars(profile,index)[star_index];d,c,S,T=cases(profile)[index];q=c-2-matched
    A={k:list(v) for k,v in available(profile,index).items()};blocks=[];iso=q;iso_groups=[list(range(q))]
    for i,t in enumerate(M+U):
        mark=(11+i) if i<len(M) else None;v=A[t].pop(0);count=t[1]-(mark is not None);G=list(range(iso,iso+count));iso+=count
        blocks.append((v,tuple(G+([mark] if mark is not None else []))));iso_groups.append(G)
    if iso!=5:raise AssertionError('high partition')
    high={6,9}|set(range(q))|({11} if matched else set())
    six,seven,r,groups=roles(profile,index);selected={v for v,H in blocks};groups=[[v for v in G if v not in selected] for G in groups]
    return high,blocks,groups,iso_groups
