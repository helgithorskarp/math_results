"""Static-order exhaustive reference; no forward-domain propagation."""
from itertools import combinations

def search(H,B,threshold=56,stop=False,minimum=6,maximum=8):
    n=len(H);m=len(B);full=(1<<m)-1
    eh=sum(x.bit_count() for x in H)//2;eb=sum(x.bit_count() for x in B)//2
    need=threshold-n-eh-eb
    domains=[]
    rt=[sum(1<<v for v in S) for S in combinations(range(m),3)
        if all(B[a]>>b&1 for a,b in combinations(S,2))]
    bt=[sum(1<<v for v in S) for S in combinations(range(m),3)
        if all(not(B[a]>>b&1) for a,b in combinations(S,2))]
    for h in H:
        domains.append([t for t in range(1<<m) if minimum<=1+h.bit_count()+t.bit_count()<=maximum
                        and not any(t&r==r for r in rt) and not any(not(t&r) for r in bt)])
    order=sorted(range(n),key=lambda i:(len(domains[i]),i))
    hi=[maximum-b.bit_count() for b in B];lo=[minimum-b.bit_count() for b in B]
    maxs=[max((t.bit_count() for t in domains[i]),default=-100) for i in order]
    suffix=[sum(maxs[d:]) for d in range(n+1)]
    nodes=[0]*(n+1);solutions=[]
    def visit(rows,cols,total):
        d=len(rows);nodes[d]+=1
        if total+suffix[d]<need:return False
        if d==n:
            if total>=need and all(c>=l for c,l in zip(cols,lo)):
                original=[0]*n
                for i,t in zip(order,rows):original[i]=t
                solutions.append(tuple(original))
                return stop
            return False
        i=order[d]
        for t in domains[i]:
            if total+t.bit_count()+suffix[d+1]<need:continue
            new=[cols[b]+int(t>>b&1) for b in range(m)]
            if any(new[b]>hi[b] or new[b]+n-d-1<lo[b] for b in range(m)):continue
            good=True
            for at,s in enumerate(rows):
                j=order[at];red=bool(H[i]>>j&1);common=t&s if red else full^(t|s)
                vs=[v for v in range(m) if common>>v&1]
                if any(bool(B[a]>>b&1)==red for a,b in combinations(vs,2)):
                    good=False;break
            if not good:continue
            for a,j in enumerate(order[:d]):
                if H[i]>>j&1:continue
                for b,jj in enumerate(order[:a]):
                    if (H[i]>>jj&1) or (H[j]>>jj&1):continue
                    if t|rows[a]|rows[b]!=full:good=False;break
                if not good:break
            if good and visit(rows+[t],new,total+t.bit_count()):return True
        return False
    visit([],[0]*m,0)
    return {'nodes':nodes,'solutions':sorted(solutions),'domains':list(map(len,domains)),'need':need}
