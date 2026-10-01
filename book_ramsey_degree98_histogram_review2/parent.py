"""Direct marked one-attachment row-multiset exclusion, without defect E."""
from itertools import combinations
import time
from incidence import need
from domains import marked_cubic8,matrix,gram


def search(capacity, counts, cap=200000, seconds=10):
    need(type(cap) is int and 0<=cap<=200000 and 0<seconds<=10,'invalid parent guard')
    initial=(4,4,6,5,5,5,5,5)
    need(len(capacity)==8 and all(len(r)==8 for r in capacity),'invalid parent capacity shape')
    need(all(type(capacity[i][j]) is int and capacity[i][j]>=0 and capacity[i][j]==capacity[j][i]
             for i in range(8) for j in range(8)),'invalid parent capacity entries')
    need(tuple(capacity[i][i] for i in range(8))==initial,'invalid parent column quotas')
    need(len(counts)==6 and all(type(c) is int and c>=0 for c in counts) and sum(counts)==13,'invalid parent profile')
    patterns=(7,5,6,1,2,0)
    rows=[tuple(c for c in combinations(range(8),3) if sum(1<<z for z in c if z<3)==p) for p in patterns]
    pairs=tuple(combinations(range(8),2))
    at=[tuple(tuple(i for i,p in enumerate(pairs) if set(p)<=set(c)) for c in family) for family in rows]
    caps=tuple(capacity[u][v] for u,v in pairs)
    states=0;st=time.monotonic()
    def visit(q,cc,rr,last):
        nonlocal states
        states+=1;need(states<=cap and time.monotonic()-st<=seconds,'INCOMPLETE parent search guard')
        if not any(cc):return () if not any(q) else None
        active=[]
        for f,family in enumerate(rows):
            active.append(tuple(i for i in range(last[f],len(family))
                                if all(q[z] for z in family[i]) and all(rr[p] for p in at[f][i])))
        if any(cc[f] and not active[f] for f in range(6)):return None
        if any(q[z]>sum(cc[f] for f in range(6) if any(z in rows[f][i] for i in active[f])) for z in range(8)):return None
        f=min((f for f in range(6) if cc[f]),key=lambda f:(len(active[f]),f))
        for i in active[f]:
            nq=list(q);nc=list(cc);nr=list(rr);nl=list(last)
            for z in rows[f][i]:nq[z]-=1
            for p in at[f][i]:nr[p]-=1
            nc[f]-=1;nl[f]=i
            answer=visit(tuple(nq),tuple(nc),tuple(nr),tuple(nl))
            if answer is not None:return ((f,i),)+answer
        return None
    answer=visit(initial,tuple(counts),caps,(0,)*6)
    need(time.monotonic()-st<=seconds,'INCOMPLETE parent final time guard')
    return answer,states


def audit():
    graphs=marked_cubic8();raw=len(graphs);negative=0;cases=states=maximum=0
    profiles=[]
    for t in range(3):
        for p in range(3-t):
            q=2-t-p
            profiles.append((t,4-p-t,4-q-t,p,q,5+t))
    need(len(profiles)==6,'parent profile census incomplete')
    for edges in graphs:
        a=matrix(8,edges);s=gram(a,(8,8,10,9,9,9,9,9))
        if any(s[i][j]<0 for i in range(8) for j in range(8)):
            negative+=1;continue
        for cc in profiles:
            answer,nodes=search(s,cc);need(answer is None,'positive parent incidence witness')
            cases+=1;states+=nodes;maximum=max(maximum,nodes)
    return dict(marked_cubic8=raw,negative_capacity_graphs=negative,direct_profiles=cases,states=states,max_states=maximum,root_profiles=profiles,survivors=0)
