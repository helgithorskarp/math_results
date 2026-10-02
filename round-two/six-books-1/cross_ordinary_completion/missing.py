"""Graph-free integer corroboration of the written ordinary proof."""
from itertools import product

cycle=((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
P={0,2,3};S={1,4,5};own=({3,5},{2,4});W=({0,1,3,5},{0,1,2,4},{0,1})
roles={'A0':((1,0),(1,0,0)),'A1U':((1,0),(0,0,1)),'A1V':((1,0),(1,0,1)),'B':((0,1),(0,0,1)),'C':((0,0),(1,1,0)),'D':((0,0),(0,1,0))}
def classify():
    output={}
    for role,(s,t) in roles.items():
        records=[]
        for word in range(64):
            M={i for i in range(6) if word>>i&1}
            if any(i in M and j in M for i,j in cycle):continue
            h=4-sum(s)-sum(t)
            if len(M)>1+h or (5 in M and not t[0]):continue
            for p in product((0,1),repeat=2):
                if any(M&own[j] and not p[j] for j in range(2)):continue
                if s[0] and len(M&P)<1+t[1]+t[2]:continue
                if s[1] and len(M&S)<1+t[0]+t[1]:continue
                if t[0] and len(M&W[0])<1+p[1]+s[1]:continue
                if t[1] and len(M&W[1])<1+p[0]+s[0]+s[1]:continue
                if t[2] and len(M&W[2])<p[0]+p[1]+s[0]-1:continue
                if p[0] and t[1]+t[2]+max(0,h-2)>1+len(M&own[0]):continue
                if p[1] and t[0]+t[2]+max(0,h-2)>1+len(M&own[1]):continue
                if not s[0] and len(M&S)>2+sum(p)-t[1]-t[2]:continue
                if not s[1] and len(M&P)>2+sum(p)-t[0]-t[1]:continue
                failure=False
                for i in range(6):
                    neighbors={j if a==i else a for a,j in cycle if a==i or j==i}
                    common=2-len(M&neighbors)
                    common+=p[0] if i in own[0] else p[1] if i in own[1] else 0
                    common+=sum(t) if i<2 else t[0] if i in own[0] else t[1]
                    common+=s[0] if i in P else s[1]
                    q=3 if i<2 else 4
                    blue=i in M
                    lower=common+max(0,q+h-(5 if blue else 6))
                    cap=7+sum(p)-len(M) if blue else 3
                    if lower>cap:failure=True;break
                if failure:continue
                records.append({'M':sorted(M),'SX':p})
        output[role]={'records':records,'missing_sets':sorted({tuple(r['M']) for r in records}),'count':len(records)}
    return output
