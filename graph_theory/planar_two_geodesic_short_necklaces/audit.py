"""Separate named-graph/Floyd audit; no imports of research implementations.

Search the displayed local path bank by direct shortestness. A step is
certified from its actual components, using either no potentially heavy
support or two disjoint such supports. No coordinate threshold is used.
"""
from collections import Counter
import json
import random


def model(patterns,scale=12):
    m=len(patterns);g={};outer=[v for j in range(m) for v in (f'a{j}',f'b{j}')]
    branches=[f'c{j}' for j in range(m)];arcs=[]
    def edge(u,v,w):
        assert u!=v and w>0
        g.setdefault(u,{})[v]=w;g.setdefault(v,{})[u]=w
    for i,u in enumerate(outer):
        v=outer[(i+1)%len(outer)];edge('r',u,scale);edge(u,v,scale)
        for x in ('r',u,v):edge(f'K{i}',x,scale)
    for j,c in enumerate(branches):
        for a in outer[2*j:2*j+2]:edge(c,a,scale)
        prices=patterns[j];assert prices and all(w>0 for w in prices) and sum(prices)<=scale
        arc=(c,)+tuple(f'v{j}_{h}' for h in range(1,len(prices)))+(branches[(j+1)%m],)
        for u,v,w in zip(arc,arc[1:],prices):edge(u,v,w)
        arcs.append(arc)
    vertices=sorted(g);index={v:i for i,v in enumerate(vertices)};n=len(vertices)
    distances=[[10**12]*n for _ in range(n)]
    for u in vertices:
        i=index[u];distances[i][i]=0
        for v,w in g[u].items():distances[i][index[v]]=w
    for k in range(n):
        row=distances[k]
        for i in range(n):
            d=distances[i];base=d[k]
            for j in range(n):
                if base+row[j]<d[j]:d[j]=base+row[j]
    def shortest(path):
        return (len(set(path))==len(path) and all(v in g[u] for u,v in zip(path,path[1:]))
                and sum(g[u][v] for u,v in zip(path,path[1:]))==distances[index[path[0]]][index[path[-1]]])
    def components(removed):
        remaining=set(g)-set(removed);answer=[]
        while remaining:
            start=min(remaining);remaining.remove(start);part={start};queue=[start]
            for u in queue:
                for v in g[u]:
                    if v in remaining:remaining.remove(v);part.add(v);queue.append(v)
            answer.append(part)
        return answer
    return g,outer,branches,arcs,shortest,components


def audit_model(patterns,result):
    g,A,C,arcs,shortest,components=model(patterns);m=len(C);k=len(A)
    anchor={'r',A[0],C[0]};represented=set(g)-anchor;atoms={f'K{i}' for i in range(k)}
    forward=[(C[0],)];backward=[None]*m;backward[0]=(C[0],)
    for j in range(1,m):forward.append(forward[-1]+arcs[j-1][1:])
    tail=(C[0],)
    for j in reversed(range(1,m)):
        tail=tail+tuple(reversed(arcs[j]))[1:];backward[j]=tail
    def bounds(i,j):
        left=({A[h] for h in range(i) if h} | {f'K{h}' for h in range(i)}
              | {C[h] for h in range(j) if h}
              | {v for h in range(j) for v in arcs[h][1:-1]})
        return left,represented-left-{A[i%k],C[j%m]}
    def certify(bank,L,R):
        critical=[];seen=set()
        for paths in bank:
            if not all(shortest(path) for path in paths):continue
            deleted=frozenset(v for path in paths for v in path)
            if not anchor<=deleted or deleted in seen:continue
            seen.add(deleted);result['valid_path_pairs']+=1
            parts=components(deleted)
            bad=set().union(*(part for part in parts if not(part<=L or part<=R or len(part)==1 and part<=atoms)))
            assert bad<=represented
            critical.append(bad)
        assert critical,'empty local geodesic bank'
        if any(not bad for bad in critical):result['single_pair_steps']+=1
        else:
            assert any(not a&b for a in critical for b in critical),'no disjoint-support certificate'
            result['two_pair_steps']+=1
    for j in range(m):
        i=2*j;L,_=bounds(i,j);_,R=bounds(i+1,j)
        bank=[]
        if j==0:bank.append([('r',A[0]),(C[0],A[1])])
        for walk in [forward[j],backward[j]]:bank.append([walk+(A[i+1],),(A[0],'r',A[i])])
        bank.append([(C[0],A[0],'r',A[i+1]),(A[i],C[j])])
        certify(bank,L,R);result['A_steps']+=1
        i+=1;nj=(j+1)%m;L,_=bounds(i,j);_,R=bounds(i+1,j+1)
        a,b=A[i],A[(i+1)%k];arc=arcs[j];rev=tuple(reversed(arc))
        wheel_right=('r',a) if j==m-1 else (A[0],'r',a)
        bank=[
            [(C[0],A[0],'r',a),(b,)+rev],
            [(C[0],A[0],'r',b),(a,)+arc],
            [forward[j]+arc[1:]+(b,),(A[0],'r',a)],
            [backward[nj]+rev[1:]+(a,),(A[0],'r',b)],
            [forward[j]+(a,),(A[0],'r',b)],
            [backward[nj]+(b,),wheel_right],
        ]
        if j==0:bank.append([(A[1],)+arc,(A[0],'r',A[2])])
        if j==m-1:bank.append([('r',A[0]),rev+(A[-1],)])
        # Exhaust endpoints, then filter by Floyd distances and whole-arc coverage.
        for p in range(len(arc)):
            for q in range(p+2):
                if q>=len(arc):continue
                bank.append([(A[0],)+forward[j]+arc[1:p+1],('r',b)+tuple(reversed(arc[q:]))])
                bank.append([(A[0],)+backward[nj]+tuple(reversed(arc[q:]))[1:],('r',a)+arc[:p+1]])
        certify(bank,L,R);result['D_steps']+=1
    result['models']+=1


def controls(result):
    # A genuine interior antipode. The old carrier pair leaves seven;
    # the split pair removes the mass-four interior vertex and leaves three.
    for name,patterns,paths,old in [
        ('left',[[2],[1,1],[2]],
         [('a0','c0','c1','v1_1'),('r','a2','c2','v1_1')],
         [('c0','c1','b1'),('a0','r','a2')]),
        ('right',[[3],[1,1,1],[2]],
         [('a0','c0','c2','v1_2','v1_1'),('r','b1','c1','v1_1')],
         [('c0','c2','a2'),('a0','r','b1')]),
    ]:
        g,A,C,arcs,shortest,components=model(patterns,4)
        weights={'v1_1':4,'K1':3,'K5':3}
        residual=lambda pair:max((sum(weights.get(v,0) for v in part) for part in components(set().union(*map(set,pair)))),default=0)
        assert all(shortest(path) for path in paths+old)
        assert residual(old)==7 and residual(paths)==3
        assert {'r','a0','c0'}<=set().union(*map(set,paths))
        result[name+'_control_old_residual']=residual(old)
        result[name+'_control_split_residual']=residual(paths)
    g,A,C,arcs,shortest,components=model([[1,1,1],[1],[1]],4)
    assert not shortest(('b0',)+arcs[0])
    assert shortest(('b0','c0','c2','c1'))
    result['dominant_arc_old_path_failure']=1
    assert not shortest(('a0','r','b2'))
    result['closing_wheel_detour_failure']=1


def main():
    result=Counter();rng=random.Random(2026092922)
    patterns=[[1],[6],[12],[1,11],[11,1],[3,3,6],[1,2,1],[5,1],[1,5,5,1]]
    for m in range(3,9):
        for case in range(20):
            prices=[list(rng.choice(patterns)) for _ in range(m)]
            if case==0:prices=[[3,3,6] for _ in range(m)]
            if case in [1,2]:
                prices=[[1] for _ in range(m)];prices[case-1]=[1,5,5,1]
            for reflected in [False,True]:
                oriented=[list(reversed(x)) for x in reversed(prices)] if reflected else prices
                audit_model(oriented,result)
    controls(result)
    assert result['two_pair_steps']>0 and result['single_pair_steps']>0
    return dict(sorted(result.items()))


if __name__=='__main__':print(json.dumps(main(),indent=2)+'\nPASS')
