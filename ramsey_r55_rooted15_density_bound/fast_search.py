"""Forward-domain propagation for the exact density-15 rooted CSP."""
from itertools import combinations

def search(H,B,threshold=56,stop=False,minimum=6,maximum=8):
    n=len(H);m=len(B);full=(1<<m)-1
    weights=[s.bit_count() for s in range(1<<m)]
    need=threshold-n-sum(a.bit_count() for a in H)//2-sum(a.bit_count() for a in B)//2
    triples=[[],[]]
    for S in combinations(range(m),3):
        colors={bool(B[a]>>b&1) for a,b in combinations(S,2)}
        if len(colors)==1:triples[int(colors.pop())].append(sum(1<<v for v in S))
    domains=[]
    for h in H:
        domains.append([s for s in range(1<<m)
                        if minimum<=1+h.bit_count()+weights[s]<=maximum
                        and not any(s&t==t for t in triples[1])
                        and not any(not(s&t) for t in triples[0])])
    # Pair compatibility is shared for every pair of H vertices of each color.
    compatible=[[[False]*(1<<m) for _ in range(1<<m)] for _ in range(2)]
    for red in (0,1):
        edges=[(1<<a)|(1<<b) for a,b in combinations(range(m),2) if bool(B[a]>>b&1)==bool(red)]
        for s in range(1<<m):
            for t in range(1<<m):
                common=s&t if red else full^(s|t)
                compatible[red][s][t]=not any(common&e==e for e in edges)
    lo=[minimum-a.bit_count() for a in B];hi=[maximum-a.bit_count() for a in B]
    nodes=[0]*(n+1);solutions=[];rows={}
    def visit(ds,columns,total):
        depth=len(rows);nodes[depth]+=1
        if not ds:
            if total>=need and all(lo[b]<=columns[b]<=hi[b] for b in range(m)):
                solutions.append(tuple(rows[i] for i in range(n)))
                return stop
            return False
        if any(not d for d in ds.values()):return False
        if total+sum(max(weights[t] for t in d) for d in ds.values())<need:return False
        for b in range(m):
            low=columns[b]+sum(all(t>>b&1 for t in d) for d in ds.values())
            high=columns[b]+sum(any(t>>b&1 for t in d) for d in ds.values())
            if low>hi[b] or high<lo[b]:return False
        i=min(ds,key=lambda j:(len(ds[j]),j))
        for t in ds[i]:
            newcols=[columns[b]+int(t>>b&1) for b in range(m)]
            if any(newcols[b]>hi[b] for b in range(m)):continue
            newds={}
            for j,domain in ds.items():
                if j==i:continue
                color=int(bool(H[i]>>j&1))
                old=[k for k in rows if not(H[i]>>j&1 or H[i]>>k&1 or H[j]>>k&1)]
                newds[j]=[s for s in domain if compatible[color][t][s]
                          and all(t|s|rows[k]==full for k in old)]
            rows[i]=t
            finished=visit(newds,newcols,total+weights[t])
            del rows[i]
            if finished:return True
        return False
    visit(dict(enumerate(domains)),[0]*m,0)
    return {'nodes':nodes,'solutions':sorted(solutions),'domains':list(map(len,domains)),'need':need}
