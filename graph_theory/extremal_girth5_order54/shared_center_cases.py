"""Joint center-incidence cover for H=2P3+P2+5K1."""
from itertools import product
from forest_profiles import profiles

def rows(a,b):
    out=[]
    for counts in product(*(range(min(n,5)+1) for n in a)):
        if sum(counts)!=5 or counts[0]:continue
        c7=16-sum(c*n for c,n in enumerate(counts))
        if 1<=c7<len(b) and b[c7]:out.append((counts,c7))
    return out

def cases(profile):
    a,b=profiles(5,2)[profile];R=rows(a,b);out=[]
    for S in R:
        for T in R:
            if S>T:continue
            for c in range(2,len(a)):
                if not S[0][c] or not T[0][c]:continue
                if any(x+y-(i==c)>n for i,(x,y,n) in enumerate(zip(S[0],T[0],a))):continue
                if S[1]==T[1] and b[S[1]]<2:continue
                out.append((6,c,S,T))
            if S[1]==T[1] and S[1]>=2 and all(x+y<=n for x,y,n in zip(S[0],T[0],a)):
                out.append((7,S[1],S,T))
    return out

def roles(profile,index):
    a,b=profiles(5,2)[profile];degree,c0,S,T=cases(profile)[index]
    six=[set(),set()];seven=[None,None];groups=[];start=13;common=None
    for c,n in enumerate(a):
        shared=int(degree==6 and c==c0)
        if shared:common=start;six[0].add(start);six[1].add(start);start+=1
        counts=(S[0][c]-shared,T[0][c]-shared,n-S[0][c]-T[0][c]+shared)
        for j,k in enumerate(counts):
            G=list(range(start,start+k));start+=k;groups.append(G)
            if j<2:six[j].update(G)
    if start!=30:raise AssertionError('six labels')
    for c,n in enumerate(b):
        if degree==7 and c==c0:common=start;seven=[start,start];start+=1;n-=1
        elif degree==6:
            for j,U in enumerate((S,T)):
                if U[1]==c:seven[j]=start;start+=1;n-=1
        G=list(range(start,start+n));start+=n;groups.append(G)
    if start!=54 or common is None or None in seven:raise AssertionError('all labels')
    return six,seven,common,groups

CASES=[(p,i) for p in range(15) for i in range(len(cases(p)))]

BASE_PROFILES=(0, 3, 5, 7, 8, 11, 12, 13, 14)
STAR_PARENTS=((4, 6), (4, 9), (4, 14))
RESIDUAL={1: [0, 1, 2, 3, 4, 6], 2: [0, 1, 3, 4], 4: [0, 1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 20, 21], 6: [10, 13, 14, 27, 28, 39]}

def proof_cases():
    from shared_star_cases import stars
    out=[]
    for p in range(15):
        if p in BASE_PROFILES:out.append(('base',p,-1,-1));continue
        for i in range(len(cases(p))):
            if (p,i) in STAR_PARENTS:out.extend(('star',p,i,j) for j in range(len(stars(p,i))))
            elif i not in RESIDUAL.get(p,[]):out.append(('joint',p,i,-1))
    return out
