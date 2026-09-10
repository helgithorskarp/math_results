"""Complete center and endpoint incidence cases for H=P4+2P2+5K1."""
from forest_profiles import profiles
from itertools import product

def rows(a,b):
    result=[]
    for counts in product(*(range(min(n,5)+1) for n in a)):
        if sum(counts)!=5 or counts[0]:continue
        c7=15-sum(c*n for c,n in enumerate(counts))
        if 1<=c7<len(b) and b[c7]:result.append((counts,c7))
    return result

def cases(profile):
    a,b=profiles(5,2)[profile];R=rows(a,b)
    return [(S,T) for S in R for T in R if S<=T and all(x+y<=n for x,y,n in zip(S[0],T[0],a)) and (S[1]!=T[1] or b[S[1]]>=2)]

def roles(profile,index):
    a,b=profiles(5,2)[profile];S,T=cases(profile)[index]
    six=[set(),set()];seven=[];groups=[];start=13
    for c,n in enumerate(a):
        counts=(S[0][c],T[0][c],n-S[0][c]-T[0][c])
        for j,k in enumerate(counts):
            group=list(range(start,start+k));start+=k
            if j<2:six[j].update(group)
            groups.append(group)
    if start!=30:raise AssertionError('six labels')
    seven=[None,None]
    for c,n in enumerate(b):
        for j,U in enumerate((S,T)):
            if U[1]==c:seven[j]=start;start+=1;n-=1
        groups.append(list(range(start,start+n)));start+=n
    if start!=54:raise AssertionError('seven labels')
    return six,seven,groups

def endpoint_roles(end_case):
    endpoint6=[{23,24,25,26},{23,27,28,29}]
    patterns=[((2,0,1),(2,0,1)),((2,0,1),(1,2,0)),((1,2,0),(1,2,0))]
    U,V=patterns[end_case];endpoint7=[set(),set()]
    groups=[list(range(15,19)),list(range(19,23)),list(range(24,27)),list(range(27,30))]
    for c,available in enumerate((list(range(32,36)),list(range(36,51)),list(range(51,54)))):
        for j,P in enumerate((U,V)):
            group=available[:P[c]];del available[:P[c]];endpoint7[j].update(group);groups.append(group)
        groups.append(available)
    return endpoint6,endpoint7,groups

CASES=[(p,i,e) for p in range(15) for i in range(len(cases(p))) for e in (range(3) if p==1 else [-1])]
