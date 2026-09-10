"""Concrete-set coverage check independent of histogram-pair generation."""
from itertools import combinations,product
from collections import Counter
from forest_profiles import profiles
from shared_center_cases import cases,roles,BASE_PROFILES,STAR_PARENTS,RESIDUAL,proof_cases

def direct_joint(profile):
    a,b=profiles(5,2)[profile];six=[c for c,n in enumerate(a) for _ in range(n)];seven=[c for c,n in enumerate(b) for _ in range(n)];first={}
    def sig(V,c7):
        n=Counter(six[v] for v in V);return (tuple(n[c] for c in range(7)),c7)
    for A in combinations(range(17),5):
        if any(six[v]==0 for v in A):continue
        c7=16-sum(six[v] for v in A)
        if c7>=1 and c7 in seven:first.setdefault(sig(A,c7),A)
    result=set()
    for S,A in first.items():
        first7=seven.index(S[1]);other7=set(seven[:first7]+seven[first7+1:])-{0};outside=sorted(set(range(17))-set(A))
        for common in A:
            if six[common]<2:continue
            for rest in combinations(outside,4):
                B=(common,)+rest
                if any(six[v]==0 for v in B):continue
                c7=16-sum(six[v] for v in B)
                if c7 in other7:
                    U,V=sorted((S,sig(B,c7)));result.add((6,six[common],U,V))
        if S[1]>=2:
            for B in combinations(outside,5):
                if all(six[v]>=1 for v in B) and sum(six[v] for v in B)+S[1]==16:
                    U,V=sorted((S,sig(B,S[1])));result.add((7,S[1],U,V))
    return result

def check_joint():
    tallies=[];common_types={}
    for p,(a,b) in enumerate(profiles(5,2)):
        D=direct_joint(p);C=cases(p)
        if set(C)!=D or len(C)!=len(D):raise AssertionError(('cover',p,len(C),len(D)))
        cs={v:c for v,c in enumerate([c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)],13)}
        for i,(d,c,S,T) in enumerate(C):
            six,seven,common,groups=roles(p,i);I=[six[j]|{seven[j]} for j in (0,1)]
            if I[0]&I[1]!={common} or any(len(U)!=6 for U in I):raise AssertionError('unique common')
            if any(len(U)!=5 for U in six) or any(v<30 for v in seven):raise AssertionError('degree role')
            if (6 if common<30 else 7,cs[common])!=(d,c):raise AssertionError('common class')
            if any(sum(cs[v] for v in U)!=16 for U in I):raise AssertionError('center high sum')
            fixed={common}|set(seven);flat=[v for G in groups for v in G]
            if len(flat)!=len(set(flat)) or set(flat)&fixed or set(flat)|fixed!=set(range(13,54)):raise AssertionError('label partition')
            for G in groups:
                colors={(6 if v<30 else 7,cs[v],v in I[0],v in I[1]) for v in G}
                if len(colors)>1:raise AssertionError('row color')
        tallies.append(len(D));common_types[str(p)]=sorted({(d,c) for d,c,S,T in D})
    return {'profiles':15,'joint_case_counts':tallies,'total_cases':sum(tallies),'common_classes':common_types}

from functools import lru_cache
from shared_center_cases import cases,roles
from shared_star_cases import stars,star_roles
from forest_profiles import profiles

@lru_cache(None)
def partitions(n):
    if not n:return ((),)
    out=[]
    for P in partitions(n-1):
        out.append(P+((n-1,),))
        for j in range(len(P)):out.append(P[:j]+(P[j]+(n-1,),)+P[j+1:])
    return tuple(out)

def direct_star(profile,index):
    a,b=profiles(5,2)[profile];d,c,S,T=cases(profile)[index];L=d-c
    caps=Counter({(6,k):n-S[0][k]-T[0][k]+int(d==6 and k==c) for k,n in enumerate(a)})
    caps.update({(7,k):n-int(k==S[1])-int(k==T[1])+int(d==7 and k==c) for k,n in enumerate(b)})
    out=set()
    for matched in range(min(1,c-2)+1):
        q=c-2-matched;niso=5-q;R=niso+(0 if matched else 2);marked=set() if matched else {niso,niso+1}
        for P in partitions(R):
            if len(P)>L or any(len(set(B)&marked)>1 for B in P):continue
            blocks=P+((),)*(L-len(P))
            for degrees in product((6,7),repeat=L):
                types=[(dd,len(B)) for dd,B in zip(degrees,blocks)]
                if any(n>caps[t] for t,n in Counter(types).items()):continue
                M=tuple(sorted(t for t,B in zip(types,blocks) if set(B)&marked));U=tuple(sorted(t for t,B in zip(types,blocks) if not set(B)&marked));out.add((matched,M,U))
    return out

def check_stars():
    counts=[]
    for p,(a,b) in enumerate(profiles(5,2)):
        cs={v:c for v,c in enumerate([c for c,n in enumerate(a) for _ in range(n)]+[c for c,n in enumerate(b) for _ in range(n)],13)};n=0
        for i,(d,c,S,T) in enumerate(cases(p)):
            if (p,i) not in STAR_PARENTS:continue
            D=direct_star(p,i);C=stars(p,i)
            if set(C)!=D or len(C)!=len(D):raise AssertionError(('star cover',p,i,len(C),len(D)))
            for j,star in enumerate(C):
                high,blocks,groups,isog=star_roles(p,i,j);six,seven,r,old=roles(p,i);I=six[0]|six[1]|set(seven);selected={v for v,H in blocks}
                if len(high)!=c or len(blocks)!=d-c or selected&I:raise AssertionError('star degree or exclusion')
                if any(len(H)!=cs[v] for v,H in blocks):raise AssertionError('star high counts')
                hs=[t for v,H in blocks for t in H];matched=star[0];q=c-2-matched;R=set(range(q,5))|(set() if matched else {11,12})
                if len(hs)!=len(set(hs)) or set(hs)!=R:raise AssertionError('high partition')
                fixed={r}|set(seven)|selected;flat=[v for G in groups for v in G]
                if len(flat)!=len(set(flat)) or set(flat)&fixed or set(flat)|fixed!=set(range(13,54)):raise AssertionError('remaining row partition')
                if sorted(t for G in isog for t in G)!=list(range(5)):raise AssertionError('isolate partition')
                for G in isog:
                    colors={(t in high,tuple(t in H for v,H in blocks)) for t in G}
                    if len(colors)>1:raise AssertionError('column role colors')
            n+=len(C)
        counts.append(n)
    return {'refined_joint_cases':len(STAR_PARENTS),'star_cases_by_profile':counts,'total_stars':sum(counts)}

from itertools import combinations
from verify import graph,hoffman_singleton_edges,check_girth_and_identities

def control():
    G=graph(50,hoffman_singleton_edges());m=check_girth_and_identities(G);count=0;uncovered=0;classes=set()
    for a,b in combinations(range(50),2):
        if b in G[a]:continue
        shared=G[a]&G[b]
        if len(shared)!=1:raise AssertionError('unique common neighbor')
        r=next(iter(shared));order=[(a+b+7*j)%50 for j in range(50)];H={a,b}
        for v in order:
            if len(H)==13:break
            if v!=r:H.add(v)
        A=G[a]-H;B=G[b]-H;L=G[r]-H;T=G[r]&H
        if A&B!={r} or L&(A|B):raise AssertionError('center exclusion')
        reached=T|set().union(*(G[t]&H for t in T));R=H-reached
        parts=[G[v]&H for v in L];flat=[t for P in parts for t in P]
        if len(flat)!=len(set(flat)) or set(flat)!=R:raise AssertionError('individual star partition')
        count+=1;uncovered+=len(R);classes.add((len(T),len(R)))
    if count!=1050:raise AssertionError('pair count')
    return {'graph':'Hoffman-Singleton','n':50,'edges':m,'nonadjacent_center_pairs':count,'high_subset_order':13,'partition_entries_checked':uncovered,'high_degree_uncovered_classes':sorted(classes)}


def histogram_check():
    from verify_forest_reduction import independent_rows
    expected={(a,b) for q,a in independent_rows(6,17,49,5) for r,b in independent_rows(7,24,45,5) if q+r==5}
    actual={(tuple(a),tuple(b)) for a,b in profiles(5,2)}
    if expected!=actual or len(actual)!=15:raise AssertionError('histograms')
    return 15

def plan_check():
    plan=proof_cases();counts=Counter(k for k,p,i,j in plan)
    if len(plan)!=len(set(plan)) or counts!={'base':9,'joint':91,'star':24}:raise AssertionError('proof plan')
    residual={(p,i) for p,inds in RESIDUAL.items() for i in inds}
    if len(residual)!=33 or set(RESIDUAL)!={1,2,4,6}:raise AssertionError('residual cover')
    for p in range(15):
        if p in BASE_PROFILES:
            if ('base',p,-1,-1) not in plan:raise AssertionError('base missing')
            continue
        for i,(d,c,S,T) in enumerate(cases(p)):
            if (p,i) in residual:
                if d!=6 or c not in (2,3):raise AssertionError('common-neighbor theorem')
                if (p,i) in STAR_PARENTS or ('joint',p,i,-1) in plan:raise AssertionError('case overlap')
            elif (p,i) in STAR_PARENTS:
                if any(('star',p,i,j) not in plan for j in range(len(stars(p,i)))):raise AssertionError('star missing')
            elif ('joint',p,i,-1) not in plan:raise AssertionError('joint missing')
    return {'proof_cases':dict(counts),'total_refutations':len(plan),'residual_center_states':len(residual),'residual_profiles':sorted(RESIDUAL),'common_degree':6,'common_high_counts':[2,3]}

def main():
    import json
    result={'histograms':histogram_check(),'joint_cover':check_joint(),'star_cover':check_stars(),'plan':plan_check(),'positive_control':control()}
    print(json.dumps(result,sort_keys=True));return result

if __name__=='__main__':main()
