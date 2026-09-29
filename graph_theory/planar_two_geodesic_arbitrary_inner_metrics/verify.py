"""Exact finite controls for the arbitrary-inner-metric necklace proof."""
import argparse
from collections import Counter
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('single',ROOT/'planar_two_geodesic_anchor_mixed_annuli/verify.py')
single=importlib.util.module_from_spec(spec);spec.loader.exec_module(single)
metric,fan,require=single.metric,single.fan,single.require


def core_graph(m,scale,lengths):
    g,A,C,arcs=single.mixed.core_graph('AD'*m,list(map(len,lengths)),scale)
    for arc,prices in zip(arcs,lengths):
        require(prices and all(x>0 for x in prices) ,'positive arc')
        for u,v,price in zip(arc,arc[1:],prices):g.adj[u][v]=g.adj[v][u]=price
    g.sphere()
    return g,A,C,arcs


def system(g,A0,C0,arcs0,core,dist,scale,result,shift=0,reverse=False):
    k,m=len(A0),len(C0);require(k==2*m and m>=3,'necklace size')
    if reverse:
        A=[A0[(2*shift+1-i)%k] for i in range(k)]
        C=[C0[(shift-j)%m] for j in range(m)]
        arcs=[tuple(reversed(arcs0[(shift-j-1)%m])) for j in range(m)]
    else:
        A=A0[2*shift:]+A0[:2*shift];C=C0[shift:]+C0[:shift]
        arcs=arcs0[shift:]+arcs0[:shift]
    lengths=[sum(g.adj[u][v] for u,v in zip(arc,arc[1:])) for arc in arcs]
    require(all(x>0 for x in lengths) and lengths[-1]<=scale,'positive arcs and short preceding arc')
    positions=[F(0)]
    for ell in lengths:positions.append(positions[-1]+ell)
    total=positions[-1];delta=[min(x,total-x) for x in positions[:-1]]
    for j in range(m):
        require(dist[C[0]][A[2*j]]==scale+min(delta[j],scale+delta[(j-1)%m],2*scale),'left parent profile')
        require(dist[C[0]][A[2*j+1]]==scale+min(delta[j],scale+delta[(j+1)%m],2*scale),'right parent profile')
        require(dist[A[0]][C[j]]==scale+min(delta[j],2*scale),'anchor parent profile')
    result['distance_profiles']+=1
    def inner(j):
        if positions[j]<=total/2:
            return (C[0],)+tuple(v for arc in arcs[:j] for v in arc[1:])
        return (C[0],)+tuple(v for arc in reversed(arcs[j:]) for v in tuple(reversed(arc))[1:])
    r=0;P=(r,A[0],C[0]);alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    tau=[set(T[1:-1]) for T in arcs];kappa=[set() for _ in A];discarded=set();outside=g.components(core)
    for K in outside:
        N=set().union(*(set(g.adj[v]) for v in K))&core;Y=N&set(A)
        require(N<=Y|{r} and len(Y)<=2,'root-clique boundary')
        if len(Y)==2:
            sites=[i for i in range(k) if Y=={A[i],A[(i+1)%k]}]
            require(len(sites)==1,'consecutive boundary');kappa[sites[0]]|=K
        elif Y and A[0] not in Y:alpha[A.index(next(iter(Y)))]|=K
        else:discarded|=K
    represented=set(range(len(g.adj)))-set(P)-discarded
    require(set().union(*(alpha+gamma+tau+kappa))==represented,'mass partition union')
    require(sum(map(len,alpha+gamma+tau+kappa))==len(represented),'mass partition disjoint')
    def bounds(i,j):
        L=set().union(*(alpha[h]|kappa[h] for h in range(i)),*(gamma[h]|tau[h] for h in range(j)))
        return L,represented-L-alpha[i%k]-gamma[j%m]
    cuts=[]
    def pair(paths,sides,flavor):
        for path in paths:g.check_path(path,dist)
        removed=set().union(*map(set,paths));require(set(P)<=removed,('anchor',flavor,paths))
        parts=g.components(removed)
        for K in parts:
            if K&core:require(any(K<=side for side in sides),('component',flavor,K,sides,paths))
            else:require(K in outside,'whole detached K')
        cut=dict(paths=paths,sides=sides,parts=parts,flavor=flavor);cuts.append(cut)
        result[flavor+'_pairs']+=1;return cut
    def carrier(j,side):
        a=A[2*j+side];neighbor=(j+(-1 if side==0 else 1))%m
        options=[inner(j)+(a,), (C[0],A[0],r,a)]
        parent=A[(2*j-1)%k] if side==0 else A[(2*j+2)%k]
        options.append(inner(neighbor)+(parent,a))
        for path in options:
            if len(set(path))==len(path) and all(v in g.adj[u] for u,v in zip(path,path[1:])):
                if sum(g.adj[u][v] for u,v in zip(path,path[1:]))==dist[path[0]][path[-1]]:return path
        raise AssertionError(('no carrier',j,side))
    for j,c in enumerate(C):
        require(dist[r][c]==2*scale,'root distance')
        s=min(lengths[j],total-lengths[j],scale)
        require(dist[A[2*j+1]][C[(j+1)%m]]==scale+s,'opposite parent distance')
    sequence=[pair([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in 'AD'*m:
        ni=i+1;nj=j+int(letter=='D');L,Rold=bounds(i,j);Lnew,R=bounds(ni,nj)
        a,b=A[i%k],A[ni%k];heavy=None
        if letter=='A':
            if j==0:
                paths=[(r,A[0]),(C[0],A[1])];flavor='A_anchor'
            elif delta[j]>=2*scale:
                paths=[(A[0],r,a,C[j]),carrier(j,1)];flavor='A_root'
            elif dist[C[0]][b]==scale+delta[j]:
                paths=[inner(j)+(b,),(A[0],r,a)];flavor='A_right'
            elif dist[C[0]][a]==scale+delta[j]:
                paths=[inner(j)+(a,),(A[0],r,b)];flavor='A_left'
            else:
                walk=inner(j)
                if positions[j]<=total/2:
                    previous=(j-1)%m;T=arcs[previous]
                    require(walk[-len(T):]==T,'previous inner arrival')
                    H1=R|gamma[j]|tau[previous];H2=(L-tau[previous])|alpha[i%k]|kappa[i%k]
                    first=pair([inner(previous)+(A[(i-1)%k],a),(A[0],r,b)],[L,H1],'A_previous_carrier')
                    second=pair([(A[0],)+walk,(r,b)],[H2,R],'A_previous_inner')
                else:
                    after=(j+1)%m;T=tuple(reversed(arcs[j]))
                    require(walk[-len(T):]==T,'next inner arrival')
                    H1=L|gamma[j]|tau[j];H2=(R-tau[j])|alpha[ni%k]|kappa[i%k]
                    first=pair([inner(after)+(A[(ni+1)%k],b),(A[0],r,a)],[H1,R],'A_next_carrier')
                    second=pair([(A[0],)+walk,(r,a)],[L,H2],'A_next_inner')
                choices=[first,second];heavy=H1,H2
        else:
            arc=arcs[j];ell=lengths[j];x,y=delta[j],delta[nj%m]
            coordinates=[F(0)]
            for u,v in zip(arc,arc[1:]):coordinates.append(coordinates[-1]+g.adj[u][v])
            if min(x,y)>=2*scale:
                radius=min(scale,ell,total-ell)
                q=min(h for h,z in enumerate(coordinates) if 2*z>=ell-radius)
                p=max(h for h,z in enumerate(coordinates) if 2*z<=ell+radius)
                H1=L|gamma[j]|set(arc[1:q]);H2=R|gamma[nj%m]|set(arc[p+1:-1])
                first=pair([(C[0],A[0],r,a),(b,)+tuple(reversed(arc[q:]))],[H1,R],'D_far_suffix')
                second=pair([(C[0],A[0],r,b),(a,)+arc[:p+1]],[L,H2],'D_far_prefix')
            elif x<=y:
                theta=ell+min(y,2*scale)-x
                p=max(h for h,z in enumerate(coordinates) if 2*z<=theta)
                q=min(h for h,z in enumerate(coordinates) if 2*z>=ell)
                H1=R|gamma[nj%m]|tau[j];H2=L|alpha[i%k]|kappa[i%k]
                first=pair([inner(j)+(a,),(A[0],r,b)],[L,H1],'D_near_left_carrier')
                second=pair([(A[0],)+inner(j)+arc[1:p+1],(r,b)+tuple(reversed(arc[q:]))],[H2,R],'D_near_left_split')
            else:
                theta=ell+y-min(x,2*scale)
                q=min(h for h,z in enumerate(coordinates) if 2*z>=theta)
                p=max(h for h,z in enumerate(coordinates) if 2*z<=ell)
                H1=L|gamma[j]|tau[j];H2=R|alpha[ni%k]|kappa[i%k]
                complement=(r,a) if j==m-1 else (A[0],r,a)
                first=pair([inner(nj%m)+(b,),complement],[H1,R],'D_near_right_carrier')
                second=pair([(A[0],)+inner(nj%m)+tuple(reversed(arc[q:]))[1:],(r,a)+arc[:p+1]],[L,H2],'D_near_right_split')
            require(q<=p+1,'ordered D cuts');choices=[first,second];heavy=H1,H2
        if heavy is None:choices=[pair(paths,[L,R],flavor)]
        else:
            require(not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented,'disjoint critical supports')
            result[letter+'_disjoint_checks']+=1
        transitions.append(choices);i,j=ni,nj
        sequence.append(pair([P,(r,A[i%k],C[j%m])],[Lnew,R],'spoke'))
    result['systems']+=1;result['component_cuts']+=len(cuts)
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,sequence=sequence,
                transitions=transitions,cuts=cuts,sectors=kappa,arcs=arcs,outer=A,branches=C)


def designs():
    patterns=[[[1],[18],[18],[1]],[[2],[18],[18],[1]],
              [[1],[18],[19],[2]],[[1],[6,6,6],[6,6,6],[1]],
              [[1,11],[1,2,1],[8,8,8]],
              [[24],[3],[1,30,1],[3,9],[48]],
              [[1],[48],[1],[18],[1,11],[1,1,40]],
              [[12],[1,1,50],[3],[1,11],[24],[6],[9,9],[1]]]
    for n,prices in enumerate(patterns):
        scale=F(1+n%3,1+n//3)
        yield scale,[[scale*x/12 for x in arc] for arc in prices]


def main():
    result=Counter();rng=random.Random(2026092925)
    for scale,lengths in designs():
        m=len(lengths);g,A,C,arcs=core_graph(m,scale,lengths);core=set(range(len(g.adj)));before=g.distances()
        for i,a in enumerate(A):
            if i%2==0:g.attach(2,(0,a,A[(i+1)%len(A)]),long_edges=scale)
            first=len(g.adj);fan.previous.old.ears(g,len(A),i,3)
            for u in range(first,len(g.adj)):
                for v in g.adj[u]:g.adj[u][v]=g.adj[v][u]=scale
        g.attach(2,(0,A[1]),long_edges=scale);g.sphere();dist=g.distances()
        require(all(dist[u][v]==before[u][v] for u in core for v in core),'ambient core isometry')
        for piece in g.pieces:g.check_local_decomposition(piece);result['local_decompositions']+=1
        profiles=list(single.base.masses(g,rng))
        for shift in range(m):
            for reverse in [False,True]:
                if sum(lengths[shift if reverse else (shift-1)%m])>scale:continue
                sys=system(g,A,C,arcs,core,dist,scale,result,shift,reverse)
                for masses in profiles:
                    cut,twice_h=metric.choose(sys,masses,result)
                    if any(2*sum(masses[v] for v in K)>sum(masses) for K in sys['outside']):
                        fan.previous.old.heavy(g,dist,masses,result)
                    else:
                        require(twice_h<=sum(masses),'half threshold')
                        require(all(2*sum(masses[v] for v in K)<=sum(masses) for K in cut['parts']),'actual half balance')
                        result['light_half_checks']+=1
                result['fixture_orientations']+=1
        result['fixtures']+=1
    shapes=[[1],[6],[12],[1,11],[3,3,6],[13],[5,5,5],[12,12],[1,6,1,6,1],[8]*7]
    for trial in range(100):
        m=3+trial%6;lengths=[list(map(F,rng.choice(shapes))) for _ in range(m)]
        lengths[-1]=list(map(F,rng.choice(shapes[:5])));scale=F(12)
        g,A,C,arcs=core_graph(m,scale,lengths);core=set(range(len(g.adj)));dist=g.distances()
        system(g,A,C,arcs,core,dist,scale,result)
        result['additional_core_models']+=1
    for flavor in ['A_previous_carrier','A_previous_inner','A_next_carrier','A_next_inner',
                   'D_far_prefix','D_far_suffix','D_near_left_split','D_near_right_split']:
        require(result[flavor+'_pairs']>0,'proof branch exercised: '+flavor)
    return dict(sorted(result.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2))
