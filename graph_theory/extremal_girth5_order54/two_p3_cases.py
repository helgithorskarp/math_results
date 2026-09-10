"""Complete profile/center cases for the two-P3 six-edge forest."""
PATTERNS=[(D,Q) for D in ((0,0),(0,1),(1,0),(1,1)) for Q in ((0,0),(0,1),(1,0)) if all(q<=d for q,d in zip(Q,D))]

CASES=[(0,0),(1,0),(2,0)]+[(3,i) for i in range(len(PATTERNS))]+[(4,0),(5,0)]

def role_groups(profile,index=0):
    if profile==0:
        common=13;groups6=[list(range(14,18)),list(range(18,22)),list(range(22,30))]
        center_six=[{13}|set(groups6[0]),{13}|set(groups6[1])]
        center_seven=[30,31];groups7=[list(range(32,39)),list(range(39,52)),[52,53]]
    elif profile==3:
        D,Q=PATTERNS[index]
        common=13 if D==(1,1) else 14
        normals=list(range(14,29));available=[v for v in normals if v!=common]
        counts=[5-d-q-(common==14) for d,q in zip(D,Q)]
        groups6=[available[:counts[0]],available[counts[0]:sum(counts)],available[sum(counts):]]
        center_six=[set(g)|{common}|({13} if d else set())|({29} if q else set()) for g,d,q in zip(groups6,D,Q)]
        ones=list(range(30,38));twos=list(range(38,53));center_seven=[]
        for d,q in zip(D,Q):center_seven.append((twos if d-q else ones).pop(0))
        groups7=[ones,twos]
    else:raise ValueError(profile)
    return center_six,center_seven,groups6+groups7
