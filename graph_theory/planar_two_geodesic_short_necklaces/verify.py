"""Exact finite controls for the written short-inner-metric necklace theorem."""
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
        require(prices and all(x>0 for x in prices) and sum(prices)<=scale,'short positive arc')
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
    require(all(0<x<=scale for x in lengths),'short arcs')
    positions=[F(0)]
    for ell in lengths:positions.append(positions[-1]+ell)
    total=positions[-1];delta=[min(x,total-x) for x in positions[:-1]]
    for j in range(m):
        for u in A[2*j:2*j+2]:require(dist[C[0]][u]==scale+min(delta[j],2*scale),'distance profile')
    result['distance_profiles']+=1
    result['branch_antipode_orientations' if total/2 in positions else 'interior_antipode_orientations']+=1
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
    for j,c in enumerate(C):
        require(dist[r][c]==2*scale,'root distance')
        require(dist[A[2*j+1]][C[(j+1)%m]]==scale+min(lengths[j],total-lengths[j]),'opposite-parent distance')
        if delta[j]<=2*scale:g.check_path(inner(j)+(A[2*j+1],),dist)
        result['opposite_arc_checks']+=1
    sequence=[pair([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in 'AD'*m:
        ni=i+1;nj=j+int(letter=='D');L,Rold=bounds(i,j);Lnew,R=bounds(ni,nj)
        heavy=None
        if letter=='A':
            if j==0:paths=[(r,A[0]),(C[0],A[1])];flavor='A_anchor'
            elif delta[j]>=2*scale:paths=[(C[0],A[0],r,A[2*j+1]),(A[2*j],C[j])];flavor='A_root'
            else:paths=[inner(j)+(A[2*j+1],),(A[0],r,A[2*j])];flavor='A_inner'
        else:
            arc=arcs[j];a,b=A[i%k],A[ni%k];x,y=delta[j],delta[nj%m];ell=lengths[j]
            turning=abs(y-x)<ell
            if j==0 and not turning:paths=[(A[1],)+arc,(A[0],r,A[2])];flavor='D_first'
            elif j==m-1 and not turning:paths=[(r,A[0]),tuple(reversed(arc))+(A[-1],)];flavor='D_last'
            elif delta[j]>=2*scale:
                paths=[(C[0],A[0],r,a),(b,)+tuple(reversed(arc))];flavor='D_root_old'
            elif y>=2*scale:
                paths=[(C[0],A[0],r,b),(a,)+arc];flavor='D_root_new'
            elif y==x+ell:
                paths=[inner(j)+arc[1:]+(b,),(A[0],r,a)];flavor='D_increasing'
            elif x==y+ell:
                paths=[inner(j+1)+tuple(reversed(arc))[1:]+(a,),(A[0],r,b)];flavor='D_decreasing'
            else:
                require(turning and max(x,y)<2*scale,'remaining antipodal step')
                coordinates=[F(0)]
                for u,v in zip(arc,arc[1:]):coordinates.append(coordinates[-1]+g.adj[u][v])
                threshold=ell+y-x
                if x<=y:
                    p=max(h for h,z in enumerate(coordinates) if 2*z<=threshold)
                    q=min(h for h,z in enumerate(coordinates) if 2*z>=ell)
                    H1=R|gamma[nj%m]|tau[j];H2=L|alpha[i%k]|kappa[i%k]
                    first=pair([inner(j)+(a,),(A[0],r,b)],[L,H1],'D_turn_left_carrier')
                    paths=[(A[0],)+inner(j)+arc[1:p+1],(r,b)+tuple(reversed(arc[q:]))]
                    second=pair(paths,[H2,R],'D_turn_left_split')
                else:
                    q=min(h for h,z in enumerate(coordinates) if 2*z>=threshold)
                    p=max(h for h,z in enumerate(coordinates) if 2*z<=ell)
                    H1=L|gamma[j]|tau[j];H2=R|alpha[ni%k]|kappa[i%k]
                    complement=(r,a) if j==m-1 else (A[0],r,a)
                    first=pair([inner(nj%m)+(b,),complement],[H1,R],'D_turn_right_carrier')
                    paths=[(A[0],)+inner(nj%m)+tuple(reversed(arc[q:]))[1:],(r,a)+arc[:p+1]]
                    second=pair(paths,[L,H2],'D_turn_right_split')
                require(q<=p+1,'antipodal coordinate overlap')
                require(not H1&H2 and H1|H2<=represented,'disjoint antipodal heavy supports')
                result['turn_disjoint_checks']+=1;heavy=H1,H2
                choices=[first,second];flavor='D_turn_split'
            require(set(arc)<=set().union(*map(set,paths)),('whole D arc',flavor))
        if heavy is None:choices=[pair(paths,[L,R],flavor)]
        transitions.append(choices)
        i,j=ni,nj;sequence.append(pair([P,(r,A[i%k],C[j%m])],[Lnew,R],'spoke'))
    result['systems']+=1;result['component_cuts']+=len(cuts)
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,sequence=sequence,
                transitions=transitions,cuts=cuts,sectors=kappa,arcs=arcs,outer=A,branches=C)


def designs():
    totals=[[F(1,2),F(1,4),F(1,4)],[F(1)]*4,[F(1,4),F(3,4)]*2,
            [F(3,4),F(1,4),F(1,4),F(1,4),F(1,2)],
            [F(3,4),F(1),F(1)]*2,[F(1),F(1,2),F(3,4),F(1,4)]*2,
            [F(1),F(1,10),F(1,10)],[F(1),F(2,3),F(1,2),F(1,4)]]
    cuts=[[F(1)],[F(1,4),F(3,4)],[F(1,2),F(1,4),F(1,4)],[F(3,7),F(4,7)]]
    for n,values in enumerate(totals):
        scale=F(1+n%3,1+n//3)
        yield len(values),scale,[[scale*x*y for y in cuts[(j+n)%len(cuts)]] for j,x in enumerate(values)]


def main():
    result=Counter();rng=random.Random(2026092921)
    for m,scale,lengths in designs():
        g,A,C,arcs=core_graph(m,scale,lengths);core=set(range(len(g.adj)));before=g.distances()
        for i,a in enumerate(A):
            if i%2==0:g.attach(2,(0,a,A[(i+1)%len(A)]),long_edges=scale)
            first=len(g.adj);fan.previous.old.ears(g,len(A),i,3)
            for u in range(first,len(g.adj)):
                for v in g.adj[u]:g.adj[u][v]=g.adj[v][u]=scale
        g.attach(2,(0,A[1]),long_edges=scale);g.sphere();dist=g.distances()
        require(all(dist[u][v]==before[u][v] for u in core for v in core),'core isometry')
        for piece in g.pieces:g.check_local_decomposition(piece);result['local_decompositions']+=1
        profiles=list(single.base.masses(g,rng))
        for shift in range(m):
            for reverse in [False,True]:
                sys=system(g,A,C,arcs,core,dist,scale,result,shift,reverse)
                for masses in profiles:
                    cut,twice_h=metric.choose(sys,masses,result)
                    if any(2*sum(masses[v] for v in K)>sum(masses) for K in sys['outside']):
                        fan.previous.old.heavy(g,dist,masses,result)
                    else:
                        require(twice_h<=sum(masses),'light half threshold')
                        require(all(2*sum(masses[v] for v in K)<=sum(masses) for K in cut['parts']),'actual half balance')
                        result['light_half_checks']+=1
                result['fixture_orientations']+=1
        result['fixtures']+=1
    for trial in range(60):
        half=2+trial%4;m=2*half;scale=F(4)
        values=[F(rng.randrange(1,17),4) for _ in range(half)]*2
        if trial%2:values[-1]/=2
        lengths=[[ell/3,2*ell/3] if (j+trial)%3 else [ell] for j,ell in enumerate(values)]
        g,A,C,arcs=core_graph(m,scale,lengths);core=set(range(len(g.adj)));dist=g.distances()
        for reverse in [False,True]:system(g,A,C,arcs,core,dist,scale,result,trial%m,reverse)
        result['additional_core_models']+=1
    for flavor in ['D_turn_left_carrier','D_turn_left_split','D_turn_right_carrier','D_turn_right_split']:
        require(result[flavor+'_choices']>0,'mass branch exercised: '+flavor)
    return dict(sorted(result.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2))
