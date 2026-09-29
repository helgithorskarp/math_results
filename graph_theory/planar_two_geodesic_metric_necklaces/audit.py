#!/usr/bin/env python3
"""Separate direct geometry/scope audit, with no research-code imports."""
from collections import Counter
from itertools import combinations, product


def add(g,u,v,cost):
    assert u!=v and cost>0
    assert v not in g.setdefault(u,{})
    g[u][v]=cost;g.setdefault(v,{})[u]=cost


def build(lengths):
    m=len(lengths);assert m>=3
    r=('r',0);A=[('a',i) for i in range(2*m)];C=[('c',j) for j in range(m)]
    g={};arcs=[];faces=[]
    for i,a in enumerate(A):add(g,r,a,4);add(g,a,A[(i+1)%(2*m)],4)
    for j,c in enumerate(C):
        for a in A[2*j:2*j+2]:add(g,a,c,4)
        T=[c]+[('v',j,z) for z in range(len(lengths[j])-1)]+[C[(j+1)%m]]
        for u,v,cost in zip(T,T[1:],lengths[j]):add(g,u,v,cost)
        arcs.append(tuple(T))
        faces.extend([(A[2*j],c,A[2*j+1]),(A[2*j+1],)+tuple(T)+(A[(2*j+2)%(2*m)],)])
    faces.append(tuple(v for T in arcs for v in T[:-1])[::-1]);core=set(g)
    for i,a in enumerate(A):
        b=A[(i+1)%(2*m)];z=('k',i)
        for v in [r,a,b]:add(g,z,v,4)
        faces.extend([(r,a,z),(a,b,z),(b,r,z)])
    return g,A,C,arcs,core,faces


def distances(g):
    V=sorted(g);at={v:i for i,v in enumerate(V)};n=len(V)
    D=[[10**9]*n for _ in V]
    for u in V:
        D[at[u]][at[u]]=0
        for v,cost in g[u].items():D[at[u]][at[v]]=cost
    for z in range(n):
        via=D[z]
        for x in range(n):
            row=D[x];prefix=row[z]
            for y in range(n):
                if prefix+via[y]<row[y]:row[y]=prefix+via[y]
    return {(u,v):D[at[u]][at[v]] for u in V for v in V}


def parts(g,removed):
    unseen=set(g)-set(removed);answer=[]
    while unseen:
        K={unseen.pop()};todo=list(K)
        while todo:
            for v in g[todo.pop()]:
                if v in unseen:unseen.remove(v);K.add(v);todo.append(v)
        answer.append(K)
    return answer


def geodesic(g,D,P):
    assert P and len(P)==len(set(P))
    return sum(g[u][v] for u,v in zip(P,P[1:]))==D[P[0],P[-1]]


def geometry(lengths,reverse,total):
    g,A0,C0,T0,core,_=build(lengths);D=distances(g);r=('r',0);m=len(C0);k=2*m
    if reverse:
        A=[A0[(1-i)%k] for i in range(k)];C=[C0[-j%m] for j in range(m)]
        arcs=[tuple(reversed(T0[(-j-1)%m])) for j in range(m)]
    else:A,C,arcs=A0,C0,T0
    totals=[sum(g[u][v] for u,v in zip(T,T[1:])) for T in arcs]
    assert min(totals)>=4 and m>=4
    anchor={r,A[0],C[0]};represented=set(g)-anchor;P=(r,A[0],C[0])
    alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    tau=[set(T[1:-1]) for T in arcs]
    sectors=[{('k',next(s for s in range(k) if {A[i],A[(i+1)%k]}=={A0[s],A0[(s+1)%k]}))} for i in range(k)]
    def sides(i,j):
        L=set().union(*(alpha[s]|sectors[s] for s in range(i)),*(gamma[t]|tau[t] for t in range(j)))
        return L,represented-L-alpha[i%k]-gamma[j%m]
    def pair(paths,bounds,label):
        assert all(geodesic(g,D,path) for path in paths),(lengths,reverse,label,paths)
        deleted=set().union(*map(set,paths));assert anchor<=deleted
        for K in parts(g,deleted):
            if K&core:assert any(K<=S for S in bounds),(lengths,reverse,label,K,bounds)
            else:assert len(K)==1 and next(iter(K))[0]=='k'
        total[label]+=1;total['new_component_pairs']+=1
    def disjoint(H1,H2):assert not H1&H2 and H1|H2<=represented
    E=[]
    for i,a in enumerate(A):
        if i==0:Q=(C[0],A[0])
        elif i==1:Q=(C[0],A[1])
        elif i==2:Q=(C[0],A[1],a)
        elif i==k-1:Q=(C[0],A[0],a)
        elif i==3 and totals[0]<8:Q=arcs[0]+(a,)
        elif i==k-2 and totals[-1]<8:Q=tuple(reversed(arcs[-1]))+(a,)
        else:Q=(C[0],A[0],r,a)
        assert geodesic(g,D,Q);E.append(Q);total['carriers']+=1
    assert D[A[0],C[1]]==min(12,4+totals[0]) and D[A[0],C[-1]]==8
    assert all(D[A[0],c]==12 for c in C[2:-1])
    for j in range(m):
        L,_=sides(2*j,j);_,R=sides(2*j+1,j)
        if j==0:paths=[(r,A[0]),(C[0],A[1])];label='A_anchor'
        elif j==1 and totals[0]<8:paths=[arcs[0]+(A[3],),(A[0],r,A[2])];label='A_first_short'
        elif j==m-1:paths=[(C[0],A[0],A[-1]),(r,A[-2],C[-1])];label='A_last'
        else:paths=[(C[0],A[0],r,A[2*j+1]),(A[2*j],C[j])];label='A_first_long' if j==1 else 'A_ordinary'
        pair(paths,[L,R],label)
    # Arc cuts are selected by direct shortestness, not threshold formulas.
    T=arcs[0];L,Rold=sides(1,0);_,R=sides(2,1)
    p=max(z for z in range(len(T)) if geodesic(g,D,(A[0],)+T[:z+1]))
    q=min(z for z in range(len(T)) if geodesic(g,D,(A[1],A[2])+tuple(reversed(T[z:]))))
    H1=Rold-set(T[1:p+1]);H2=set(T[1:q]);disjoint(H1,H2)
    pair([(A[0],)+T[:p+1],(r,A[1])],[L,H1],'D_anchor_prefix')
    pair([P,(A[1],A[2])+tuple(reversed(T[q:]))],[L,H2,R],'D_anchor_suffix')
    for j in [1,m-2]:
        if (j==1 and totals[0]>=8) or (j==m-2 and totals[-1]>=8):continue
        i=2*j+1;T=arcs[j];L,_=sides(i,j);_,R=sides(i+1,j+1)
        start=(A[0],r,A[i+1]) if j==1 else (A[i+1],)
        start2=(A[0],r,A[i]) if j==m-2 else (A[i],)
        q=min(z for z in range(len(T)) if geodesic(g,D,start+tuple(reversed(T[z:]))))
        p=max(z for z in range(len(T)) if geodesic(g,D,start2+T[:z+1]))
        H1=L|gamma[j]|set(T[1:q]);H2=R|gamma[j+1]|set(T[p+1:-1]);disjoint(H1,H2)
        pair([E[i],start+tuple(reversed(T[q:]))],[H1,R],'D_short_forward')
        pair([E[i+1],start2+T[:p+1]],[L,H2],'D_short_backward')
    total['oriented_systems']+=1


def controls(total):
    r=('r',0)
    for which in ['first_sector','first_inner','last_sector','last_inner']:
        lengths=[[4] for _ in range(4)]
        if which=='first_inner':lengths[0]=[3,1]
        if which=='last_inner':lengths[-1]=[1,3]
        g,A,C,T,core,faces=build(lengths);D=distances(g)
        if which.startswith('first'):
            paths=[T[0]+(A[3],),(A[0],r,A[2])]
            w={('k',1):3,('k',2):4,('k',4):3} if which.endswith('sector') else {T[0][1]:4,('k',2):3,('k',4):3}
        else:
            paths=[(C[0],A[0],A[-1]),(r,A[-2],C[-1])]
            w={('k',6):4,('k',7):3,('k',4):3} if which.endswith('sector') else {T[-1][1]:4,('k',6):3,('k',4):3}
        assert sum(w.values())==10 and all(geodesic(g,D,P) for P in paths)
        deleted=set().union(*map(set,paths));assert {r,A[0],C[0]}<=deleted
        residual=max(sum(w.get(v,0) for v in K) for K in parts(g,deleted))
        assert residual==(3 if which=='first_inner' else 4),(which,residual)
        total[which+'_control_residual']=residual
        if which!='first_sector':continue
        assert len(g)==21 and sum(map(len,g.values()))//2==52 and len(faces)==33
        darts=[(u,v) for f in faces for u,v in zip(f,f[1:]+f[:1])]
        assert len(darts)==len(set(darts))==sum(map(len,g.values()))
        assert set(darts)=={(u,v) for u in g for v in g[u]}
        for v in g:
            rot={f[i-1]:f[(i+1)%len(f)] for f in faces for i,x in enumerate(f) if x==v}
            assert set(rot)==set(g[v]);start=next(iter(rot));x=start;seen=set()
            while x not in seen:seen.add(x);x=rot[x]
            assert x==start and seen==set(g[v])
        assert len(g)-len(darts)//2+len(faces)==2
        facial=min(max(sum(w.get(v,0) for v in K) for K in parts(g,f)) for f in faces)
        assert facial==6
        count=0
        for size in range(3):
            for deleted in combinations(g,size):assert len(parts(g,deleted))==1;count+=1
        assert count==232 and min(len(set(g[v])&core) for v in core)==4
        assert not geodesic(g,D,(A[0],r,A[3],C[1])) and D[A[0],C[1]]==8
        total.update(scope_vertices=21,scope_edges=52,scope_faces=33,scope_facial_minimum=6,scope_pair_residual=4,scope_total_mass=10,scope_connectivity_checks=count,scope_core_minimum_degree=4,old_complement_failure=1)
    # The t=3 neighboring D exceptions coincide; the current proof needs t>=4.
    g,A,C,T,_,_=build([[4],[4],[4]]);D=distances(g)
    assert D[A[0],C[2]]==8 and not geodesic(g,D,(A[0],r,A[4],C[2]))
    total['three_branch_method_boundary']=1


def main():
    total=Counter();patterns=[[4],[3,1],[1,3],[1,1,2],[1,3,1],[3,1,2],[1,5,1],[3,2,3],[1,8,3]]
    for m in range(4,9):
        for left,right in product(range(len(patterns)),repeat=2):
            lengths=[patterns[(j+left+2*right)%len(patterns)] for j in range(m)]
            lengths[0]=patterns[left];lengths[-1]=patterns[right]
            for reverse in [False,True]:geometry(lengths,reverse,total)
            total['models']+=1
    controls(total)
    print(' '.join(f'{k}={v}' for k,v in sorted(total.items()))+' PASS')


if __name__=='__main__':main()
