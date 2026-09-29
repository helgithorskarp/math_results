"""Separate named-graph audit: exact local path banks and actual components.

No imports of research implementations; finite evidence, not a universal proof.
"""
from collections import Counter
from functools import lru_cache
import json
import random


def model(patterns, scale=12):
    m=len(patterns);g={};A=[v for j in range(m) for v in (f'a{j}',f'b{j}')]
    C=[f'c{j}' for j in range(m)];arcs=[]
    def edge(u,v,w):
        assert u!=v and w>0
        g.setdefault(u,{})[v]=w;g.setdefault(v,{})[u]=w
    for i,a in enumerate(A):
        b=A[(i+1)%len(A)];edge('r',a,scale);edge(a,b,scale)
        for z in ('r',a,b):edge(f'K{i}',z,scale)
    for j,c in enumerate(C):
        for a in A[2*j:2*j+2]:edge(c,a,scale)
        arc=(c,)+tuple(f'v{j}_{h}' for h in range(1,len(patterns[j])))+(C[(j+1)%m],)
        for u,v,w in zip(arc,arc[1:],patterns[j]):edge(u,v,w)
        arcs.append(arc)
    V=sorted(g);d={u:{v:0 if u==v else g[u].get(v,10**12) for v in V} for u in V}
    for k in V:
        for i in V:
            for j in V:d[i][j]=min(d[i][j],d[i][k]+d[k][j])
    core=set(g)-{f'K{i}' for i in range(len(A))}
    @lru_cache(None)
    def paths(s,t):
        if s==t:return ((s,),)
        answer=tuple((s,)+tail for v,w in g[s].items() if v in core and w+d[v][t]==d[s][t] for tail in paths(v,t))
        assert len(answer)<10000,'path bank too large'
        return answer
    def components(removed):
        left=set(g)-set(removed);answer=[]
        while left:
            u=min(left);left.remove(u);part={u};q=[u]
            for v in q:
                for w in g[v]:
                    if w in left:left.remove(w);part.add(w);q.append(w)
            answer.append(part)
        return answer
    return g,A,C,arcs,d,paths,components


def audit(patterns,result,verbose=False):
    g,A,C,arcs,d,paths,components=model(patterns);m=len(C);k=len(A)
    anchor={'r',A[0],C[0]};represented=set(g)-anchor;atoms={f'K{i}' for i in range(k)}
    def bounds(i,j):
        left=({A[h] for h in range(i) if h}|{f'K{h}' for h in range(i)}
             |{C[h] for h in range(j) if h}|{v for h in range(j) for v in arcs[h][1:-1]})
        return left,represented-left-{A[i%k],C[j%m]}
    for j in range(m):
        for letter in 'AD':
            i=2*j+(letter=='D');ni=i+1;nj=j+(letter=='D');a,b=A[i%k],A[ni%k]
            L,_=bounds(i,j);_,R=bounds(ni,nj)
            targets=arcs[j] if letter=='D' else (C[j],)
            bank={frozenset(p):p for s in ['r',A[0],C[0],a,b] for t in list(targets)+[a,b] for p in paths(s,t)}
            bank[frozenset(anchor)]=('r',A[0],C[0]);entries=list(bank.items())
            critical={};seen=set()
            for x,(S,P) in enumerate(entries):
                for T,Q in entries[x:]:
                    U=S|T
                    if not anchor<=U or U in seen:continue
                    seen.add(U)
                    parts=components(U)
                    bad=frozenset().union(*(part for part in parts if not(part<=L or part<=R or len(part)==1 and part<=atoms)))
                    critical.setdefault(bad,(P,Q))
            result['local_steps']+=1;result['tested_pairs']+=len(seen)
            good=None
            if frozenset() in critical:good=[critical[frozenset()]];result['single']+=1
            else:
                ordered=sorted(critical,key=lambda S:(len(S),sorted(S)))
                for s in ordered:
                    for t in ordered:
                        if not s&t:good=[critical[s],critical[t]];break
                    if good:break
                if good:result['disjoint']+=1
            if not good:
                answer={'patterns':patterns,'step':[letter,j],'critical':[
                    {'support':sorted(s),'paths':critical[s]} for s in sorted(critical,key=lambda S:(len(S),sorted(S)))],
                    'L':sorted(L),'R':sorted(R),'bank':len(bank)}
                return answer
            if verbose:print(json.dumps({'step':[letter,j],'pairs':good}))
    result['models']+=1


def controls(result):
    for name,patterns,I,carrier,inner_pair,masses in [
        ('previous',[[1],[6,6,6],[6,6,6],[1]],
         ('c0','c1','v1_1','v1_2','c2'),
         [('c0','c1','b1','a2'),('a0','r','b2')],
         [('a0','c0','c1','v1_1','v1_2','c2'),('r','b2')],
         {'v1_1':3,'K6':3,'K4':4}),
        ('next',[[2],[6,6,6],[6,6,6],[1]],
         ('c0','c3','v2_2','v2_1','c2'),
         [('c0','c3','a3','b2'),('a0','r','a2')],
         [('a0','c0','c3','v2_2','v2_1','c2'),('r','a2')],
         {'v2_1':3,'K1':3,'K4':4}),
    ]:
        g,A,C,arcs,d,paths,components=model(patterns)
        length=lambda p:sum(g[u][v] for u,v in zip(p,p[1:]))
        assert length(I)==d['c0']['c2']==19
        for a in ['a2','b2']:assert length(I+(a,))>d['c0'][a]
        for pair in [carrier,inner_pair]:
            assert {'r','a0','c0'}<=set().union(*map(set,pair))
            for path in pair:assert len(set(path))==len(path) and length(path)==d[path[0]][path[-1]]
        residual=lambda pair:max((sum(masses.get(v,0) for v in part) for part in components(set().union(*map(set,pair)))),default=0)
        assert sum(masses.values())==10 and max(masses.get(f'K{i}',0) for i in range(8))==4
        assert residual(carrier)==6 and residual(inner_pair)==4
        result[name+'_carrier_residual']=6;result[name+'_inner_residual']=4
        result['naive_parent_append_failures']+=2


def main():
    rng=random.Random(2026092926);result=Counter()
    shapes=[[1],[6],[12],[1,11],[3,3,6],[1,2,1],[5,1],[1,5,5,1],
            [13],[5,5,5],[12,12],[1,6,1,6,1],[8]*7,[1,60,1]]
    for trial in range(240):
        m=3+trial%6;prices=[list(rng.choice(shapes)) for _ in range(m)]
        prices[-1]=list(rng.choice(shapes[:8]))
        answer=audit(prices,result)
        assert answer is None,answer
    controls(result)
    assert result['single']>0 and result['disjoint']>0
    return dict(sorted(result.items()))


if __name__=='__main__':print(json.dumps(main(),indent=2)+'\nPASS')
