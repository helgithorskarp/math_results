#!/usr/bin/env python3
"""Direct geometry and scope audit; no research imports."""
from collections import Counter
from itertools import product, combinations

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
        lengths=[[8],[1,6,1],[2,3,4],[1,8,3]][j%4]
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


def is_geodesic(g,d,path):
    assert len(path)==len(set(path))
    return sum(g[u][v] for u,v in zip(path,path[1:]))==d[path[0],path[-1]]


def qualifies(g,A,C,prices,word,shift,ai,cj):
    k=len(A)
    if k<5 or word[shift]!='A' or word[shift-1]!='D' or word[(shift+1)%len(word)]!='D':return False
    near=(set(g[A[(ai+2)%k]])|set(g[A[(ai+3)%k]]))&set(C)
    if near&set(g[A[(ai-1)%k]]):return False
    return min(prices[cj],prices[cj-1])>=8


def audit_word(word,total):
    g,A0,C0,arcs0,prices,states,core=build(word)
    k,m=len(A0),len(C0);r=('r',0)
    accepted=[(z,i%k,j%m) for z,(i,j) in enumerate(states)
              if qualifies(g,A0,C0,prices,word,z,i%k,j%m)]
    total['models']+=1
    if not accepted:total['models_without_anchor']+=1;return
    d=distances(g)
    for shift,ai,cj in accepted:
        A=A0[ai:]+A0[:ai];C=C0[cj:]+C0[:cj];arcs=arcs0[cj:]+arcs0[:cj]
        a0,c0=A[0],C[0];anchor={r,a0,c0};represented=set(g)-anchor
        P=(r,a0,c0);path_check(g,d,P)
        assert set(g[c0])&set(A)=={A[0],A[1]}
        assert all(set(g[a])&set(C)=={c0} for a in A[:2])
        carriers=[]
        for z,a in enumerate(A):
            if z==0:E=(c0,a0)
            elif z==1:E=(c0,A[1])
            elif z==2:E=(c0,A[1],A[2])
            elif z==k-1:E=(c0,a0,a)
            else:E=(c0,a0,r,a)
            path_check(g,d,E);carriers.append(E);total['carrier_paths']+=1
        for c in set(C)&(set(g[A[2]])|set(g[A[3]])):
            assert d[a0,c]==12;total['complement_distances']+=1
        alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
        tau=[set(arc[1:-1]) for arc in arcs];sector=[{('k',a[1])} for a in A]
        def sides(i,j):
            L=set().union(*(alpha[z]|sector[z] for z in range(i)),*(gamma[z]|tau[z] for z in range(j)))
            return L,represented-L-alpha[i%k]-gamma[j%m]
        def pair(paths,bounds):
            for path in paths:path_check(g,d,path)
            removed=set().union(*map(set,paths));assert anchor<=removed
            for K in components(g,removed):
                if K&core:assert any(K<=S for S in bounds),(word,paths,K,bounds)
                else:assert len(K)==1 and next(iter(K))[0]=='k'
            total['new_component_pairs']+=1
        i=j=0
        for letter in word[shift:]+word[:shift]:
            ni=i+int(letter in 'AD');nj=j+int(letter in 'CD')
            L,Rold=sides(i,j);Lnew,R=sides(ni,nj)
            if letter=='A' and i==2:
                pair([carriers[2],(a0,r,A[3],C[j%m])],[L,R]);total['A_repacked']+=1
            elif letter=='D' and i==1 and j==0:
                arc=arcs[0]
                # Select cut vertices from direct full-graph shortestness,
                # independently of the production threshold calculations.
                p=max(z for z in range(len(arc)) if is_geodesic(g,d,(a0,)+arc[:z+1]))
                q=min(z for z in range(len(arc)) if is_geodesic(g,d,(A[1],A[2])+tuple(reversed(arc[z:]))))
                H1=Rold-set(arc[1:p+1]);H2=set(arc[1:q])
                assert q<=p+1 and not H1&H2 and H1|H2<=represented
                pair([(a0,)+arc[:p+1],(r,A[1])],[L,H1])
                pair([P,(A[1],A[2])+tuple(reversed(arc[q:]))],[L,H2,R])
                total['D_anchor']+=1
            elif letter=='D' and i==2:
                arc=arcs[j]
                p=max(z for z in range(len(arc)) if is_geodesic(g,d,(A[2],)+arc[:z+1]))
                q=min(z for z in range(len(arc)) if is_geodesic(g,d,(a0,r,A[3])+tuple(reversed(arc[z:]))))
                H1=L|gamma[j%m]|set(arc[1:q]);H2=R|gamma[(j+1)%m]|set(arc[p+1:-1])
                assert q<=p+1 and not H1&H2 and H1|H2<=represented
                pair([carriers[2],(a0,r,A[3])+tuple(reversed(arc[q:]))],[H1,R])
                pair([carriers[3],(A[2],)+arc[:p+1]],[L,H2]);total['D_repacked']+=1
            i,j=ni,nj
        total['anchors']+=1


def controls(total):
    # The long-arc hypothesis certifies a specific necessary path equality.
    for length,expected in [(7,False),(8,True)]:
        g,A,C,arcs,prices,states,core=build('AD'*3,{0:[3,length-3],2:[4,4]})
        d=distances(g)
        assert qualifies(g,A,C,prices,'AD'*3,0,0,0)==expected
        assert is_geodesic(g,d,(A[0],('r',0),A[3],C[1]))==expected
        assert d[A[0],C[1]]==length+4
        total['arc_threshold_controls']+=1
    # A prohibited common inner neighbor shortens the complementary path.
    g,A,C,arcs,prices,states,core=build('ADDAD',{0:[4,4],1:[4,4],2:[4,4]})
    d=distances(g)
    assert not qualifies(g,A,C,prices,'ADDAD',0,0,0)
    assert C[2] in g[A[3]] and C[2] in g[A[-1]]
    assert d[A[0],C[2]]==8
    assert not is_geodesic(g,d,(A[0],('r',0),A[3],C[2]))
    total['incidence_failure_controls']+=1


def scope_control(total):
    # All edges cost four; division by four gives a unit-edge graph.
    word='AD'*3
    g,A,C,arcs,prices,states,core=build(word,{0:[4,4],1:[4,4],2:[4,4]})
    r=('r',0);d=distances(g)
    assert len(g)==19 and sum(map(len,g.values()))//2==42
    assert all(length==4 for row in g.values() for length in row.values())
    assert qualifies(g,A,C,prices,word,0,0,0)
    assert all(len(set(g[c])&set(A))==2 for c in C)
    masses={('k',1):3,('k',2):4,('k',4):3}
    assert masses.get(('k',0),0)<max(masses.get(('k',i),0) for i in [0,2,4])
    paths=[(C[0],A[1],A[2]),(A[0],r,A[3],C[1])]
    for path in paths:path_check(g,d,path)
    removed=set().union(*map(set,paths));assert {r,A[0],C[0]}<=removed
    mass=lambda K:sum(masses.get(v,0) for v in K)
    assert sum(masses.values())==10 and max(map(mass,components(g,removed)))==4
    faces=[]
    for i,a in enumerate(A):
        b=A[(i+1)%len(A)];z=('k',i)
        faces.extend([(r,a,z),(a,b,z),(b,r,z)])
    i=j=0
    for letter in word:
        if letter=='A':faces.append((A[i%len(A)],C[j%len(C)],A[(i+1)%len(A)]))
        else:faces.append((A[i%len(A)],)+arcs[j]+(A[(i+1)%len(A)],));j+=1
        i+=1
    inner=tuple(v for arc in arcs for v in arc[:-1]);faces.append(inner[::-1])
    darts=[(u,v) for face in faces for u,v in zip(face,face[1:]+face[:1])]
    assert len(darts)==len(set(darts))==sum(map(len,g.values()))
    assert set(darts)=={(u,v) for u in g for v in g[u]}
    assert len(g)-sum(map(len,g.values()))//2+len(faces)==2
    for v in g:
        successor={face[i-1]:face[(i+1)%len(face)] for face in faces for i,x in enumerate(face) if x==v}
        assert set(successor)==set(g[v])
        seen=set();start=next(iter(successor));x=start
        while x not in seen:seen.add(x);x=successor[x]
        assert x==start and seen==set(g[v])
    smallest=min(max(map(mass,components(g,face))) for face in faces)
    assert len(faces)==25 and smallest==6
    branch={v for v in g if v[0]!='v'}
    suppressed={v:set(g[v])&branch for v in branch}
    for arc in arcs:
        suppressed[arc[0]].add(arc[-1]);suppressed[arc[-1]].add(arc[0])
    connected=0
    for size in range(3):
        for removed in combinations(suppressed,size):
            assert len(components(suppressed,removed))==1;connected+=1
    assert connected==137
    kernel={r}|set(A)|set(C)
    assert min(len(suppressed[v]&kernel) for v in kernel)==4
    total.update(scope_vertices=19,scope_edges=42,scope_faces=25,
                 scope_total_mass=10,scope_pair_residual=4,scope_min_facial_residual=6,
                 scope_connectivity_checks=connected,scope_core_minimum_degree=4,
                 nonmaximum_anchor_control=1,no_single_parent_control=1)


def main():
    total=Counter()
    for n in range(5,9):
        for letters in product('ACD',repeat=n):
            word=''.join(letters)
            if valid(word) and sum(x in 'AD' for x in word)>=5 and 'DAD' in word*2:audit_word(word,total)
    controls(total);scope_control(total)
    assert all(total[k] for k in ['A_repacked','D_repacked','D_anchor','anchors'])
    print(' '.join(f'{k}={v}' for k,v in sorted(total.items()))+' PASS')


if __name__=='__main__':main()
