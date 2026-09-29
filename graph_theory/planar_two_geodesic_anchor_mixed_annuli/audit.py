#!/usr/bin/env python3
"""Direct audit of the new anchor criterion and A-step; no research imports."""
from collections import Counter
from itertools import product


def run_bound(word,letter):
    best=now=0
    for x in word*2:
        now=now+1 if x==letter else 0;best=max(best,now)
    return best


def valid(word):
    k=sum(x in 'AD' for x in word);m=sum(x in 'CD' for x in word)
    return k>=3 and m>=3 and run_bound(word,'A')<=k-2 and run_bound(word,'C')<=m-2


def edge(g,u,v,length):
    assert u!=v and length>0
    if v in g.setdefault(u,{}):assert g[u][v]==length
    g[u][v]=length;g.setdefault(v,{})[u]=length


def build(word,override=None):
    assert valid(word)
    k=sum(x in 'AD' for x in word);m=sum(x in 'CD' for x in word)
    r=('r',0);A=[('a',i) for i in range(k)];C=[('c',j) for j in range(m)]
    g={};states=[];i=j=0
    for z,a in enumerate(A):edge(g,r,a,4);edge(g,a,A[(z+1)%k],4)
    for letter in word:
        states.append((i,j));edge(g,A[i%k],C[j%m],4)
        i+=int(letter in 'AD');j+=int(letter in 'CD')
    arcs=[];prices=[]
    for j,c in enumerate(C):
        lengths=[[4],[3,5],[1,2,1],[1,8,2]][j%4]
        if override is not None and j in override:lengths=override[j]
        arc=[c]+[('v',j,t) for t in range(len(lengths)-1)]+[C[(j+1)%m]]
        for u,v,length in zip(arc,arc[1:],lengths):edge(g,u,v,length)
        arcs.append(tuple(arc));prices.append(sum(lengths))
    core=set(g)
    for i,a in enumerate(A):
        for v in [r,a,A[(i+1)%k]]:edge(g,('k',i),v,4)
    return g,A,C,arcs,prices,states,core


def distances(g):
    vertices=sorted(g);ix={v:i for i,v in enumerate(vertices)};n=len(vertices)
    d=[[10**9]*n for _ in vertices]
    for u in g:
        d[ix[u]][ix[u]]=0
        for v,length in g[u].items():d[ix[u]][ix[v]]=length
    for z in range(n):
        via=d[z]
        for x in range(n):
            row=d[x];prefix=row[z]
            for y in range(n):
                if prefix+via[y]<row[y]:row[y]=prefix+via[y]
    return {(u,v):d[ix[u]][ix[v]] for u in vertices for v in vertices}


def components(g,removed):
    unseen=set(g)-set(removed);answer=[]
    while unseen:
        part={unseen.pop()};todo=list(part)
        while todo:
            for v in g[todo.pop()]:
                if v in unseen:unseen.remove(v);part.add(v);todo.append(v)
        answer.append(part)
    return answer


def path_check(g,d,path):
    assert len(path)==len(set(path))
    assert sum(g[u][v] for u,v in zip(path,path[1:]))==d[path[0],path[-1]]


def local(g,A,C,prices,j):
    outer=set(A);neighbors=set(g[C[j]])&outer
    if len(neighbors)!=1:return False
    a=next(iter(neighbors));i=A.index(a);near={a,A[i-1],A[(i+1)%len(A)]}
    return all(prices[t]>=8 or (set(g[C[z]])&outer)<=near
               for t,z in [(j,(j+1)%len(C)),((j-1)%len(C),(j-1)%len(C))])


def audit_word(word,total):
    g,A0,C0,arcs0,prices,states,core=build(word);d=distances(g)
    k,m=len(A0),len(C0);r=('r',0)
    for shift,(ai,cj) in enumerate(states):
        ai%=k;cj%=m;a0,c0=A0[ai],C0[cj]
        by_distance=all(d[c0,a]==4+(0 if a==a0 else 4 if a in [A0[ai-1],A0[(ai+1)%k]] else 8) for a in A0)
        by_local=local(g,A0,C0,prices,cj)
        assert by_distance==by_local
        total['criterion_states']+=1;total['eligible_states']+=int(by_local)
        if not by_local:continue
        A=A0[ai:]+A0[:ai];C=C0[cj:]+C0[:cj];arcs=arcs0[cj:]+arcs0[:cj]
        anchor={r,a0,c0};represented=set(g)-anchor
        alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
        tau=[set(arc[1:-1]) for arc in arcs];sector=[{('k',a[1])} for a in A]
        def left(i,j):return set().union(*(alpha[z]|sector[z] for z in range(i)),*(gamma[z]|tau[z] for z in range(j)))
        i=j=0
        for letter in word[shift:]+word[:shift]:
            if letter=='A':
                a,b,c=A[i%k],A[(i+1)%k],C[j%m]
                location=i%k
                carrier=(c0,a0) if location==0 else ((c0,a0,a) if location in [1,k-1] else (c0,a0,r,a))
                other=(b,c) if r in carrier else (r,b,c)
                path_check(g,d,carrier);path_check(g,d,other)
                removed=set(carrier)|set(other);assert anchor<=removed
                L=left(i,j);R=represented-left(i+1,j)-alpha[(i+1)%k]-gamma[j%m]
                for K in components(g,removed):
                    if K&core:assert K<=L or K<=R
                    else:assert len(K)==1 and next(iter(K))[0]=='k'
                total['A_component_pairs']+=1
                total['A_root_carrier' if r in carrier else 'A_other_root']+=1
            i+=int(letter in 'AD');j+=int(letter in 'CD')
    total['models']+=1


def controls(total):
    # The strict threshold 2 lambda in the criterion is exact.
    for length,expect in [(7,False),(8,True)]:
        g,A,C,arcs,prices,states,core=build('AADDDD',{0:[3,length-3]})
        d=distances(g)
        assert local(g,A,C,prices,1)==expect
        assert d[C[1],A[0]]==length+4
        total['anchor_threshold_controls']+=1
    # A whole long fan is heavy, each attached K is light, and no centroid
    # replacement is used: one carrier pair gives the sharper bound directly.
    g,A,C,arcs,prices,states,core=build('AAAAADDDDD',{0:[3,2,3]})
    d=distances(g);r=('r',0)
    assert local(g,A,C,prices,2)
    masses={A[i]:1 for i in range(1,5)}
    masses.update({('k',i):1 for i in range(5)})
    paths=[(C[2],A[7],r,A[2]),(A[3],C[0])]
    for path in paths:path_check(g,d,path)
    removed=set().union(*map(set,paths));assert {r,A[7],C[2]}<=removed
    largest=max(sum(masses.get(v,0) for v in K) for K in components(g,removed))
    assert sum(masses.values())==9 and largest==3
    total['heavy_fan_control_mass']=9;total['heavy_fan_control_residual']=3
    for word in ['AD'*5,'AC'*5]:
        g,A,C,arcs,prices,states,core=build(word)
        assert not any(local(g,A,C,prices,j) for j in range(len(C)))
        total['no_anchor_controls']+=1


def main():
    total=Counter()
    for n in range(3,8):
        for letters in product('ACD',repeat=n):
            word=''.join(letters)
            if 'A' in word and valid(word):audit_word(word,total)
    controls(total)
    print(' '.join(f'{k}={v}' for k,v in sorted(total.items()))+' PASS')


if __name__=='__main__':main()
