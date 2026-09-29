"""Exact regressions for the written all-inner-metric necklace theorem."""
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


def system(g,A0,C0,arcs0,core,dist,scale,result,shift=0,reverse=False):
    k,m=len(A0),len(C0)
    require(k==2*m and m>=4,'necklace size')
    if reverse:
        A=[A0[(2*shift+1-i)%k] for i in range(k)]
        C=[C0[(shift-j)%m] for j in range(m)]
        arcs=[tuple(reversed(arcs0[(shift-j-1)%m])) for j in range(m)]
    else:
        A=A0[2*shift:]+A0[:2*shift];C=C0[shift:]+C0[:shift]
        arcs=arcs0[shift:]+arcs0[:shift]
    coords=[]
    for arc in arcs:
        x=[F(0)]
        for u,v in zip(arc,arc[1:]):x.append(x[-1]+g.adj[u][v])
        require(x[-1]>=scale,'arc lower bound');coords.append(x)
    ell0,elllast=coords[0][-1],coords[-1][-1]
    r=0;P=(r,A[0],C[0])
    alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    tau=[set(T[1:-1]) for T in arcs];kappa=[set() for _ in A]
    discarded=set();outside=g.components(core)
    for K in outside:
        N=set().union(*(set(g.adj[v]) for v in K))&core;Y=N&set(A)
        require(N<=Y|{r} and len(Y)<=2,'root-clique boundary')
        if len(Y)==2:
            sites=[i for i in range(k) if Y=={A[i],A[(i+1)%k]}]
            require(len(sites)==1,'consecutive attachment');kappa[sites[0]]|=K
        elif Y and A[0] not in Y:alpha[A.index(next(iter(Y)))]|=K
        else:discarded|=K
    represented=set(range(len(g.adj)))-set(P)-discarded
    require(set().union(*(alpha+gamma+tau+kappa))==represented,'mass partition union')
    require(sum(map(len,alpha+gamma+tau+kappa))==len(represented),'mass partition disjoint')
    def bounds(i,j):
        L=set().union(*(alpha[s]|kappa[s] for s in range(i)),*(gamma[t]|tau[t] for t in range(j)))
        return L,represented-L-alpha[i%k]-gamma[j%m]
    cuts=[]
    def pair(paths,sides,flavor):
        for path in paths:g.check_path(path,dist)
        removed=set().union(*map(set,paths));require(set(P)<=removed,('prescribed triple',flavor,paths))
        parts=g.components(removed)
        for K in parts:
            if K&core:require(any(K<=side for side in sides),('containment',m,ell0,elllast,flavor,paths,K,sides))
            else:require(K in outside,'whole detached K')
        cut=dict(paths=paths,sides=sides,parts=parts,flavor=flavor);cuts.append(cut)
        result[flavor+'_pairs']+=1;return cut
    carriers=[]
    for i,a in enumerate(A):
        if i==0:E=(C[0],A[0]);want=scale
        elif i==1:E=(C[0],A[1]);want=scale
        elif i==2:E=(C[0],A[1],a);want=2*scale
        elif i==k-1:E=(C[0],A[0],a);want=2*scale
        elif i==3 and ell0<2*scale:E=arcs[0]+(a,);want=scale+ell0
        elif i==k-2 and elllast<2*scale:E=tuple(reversed(arcs[-1]))+(a,);want=scale+elllast
        else:E=(C[0],A[0],r,a);want=3*scale
        require(dist[C[0]][a]==want,'anchor distance profile');g.check_path(E,dist);carriers.append(E)
        result['carrier_checks']+=1
    require(dist[A[0]][C[1]]==min(3*scale,scale+ell0),'first branch distance')
    require(dist[A[0]][C[-1]]==2*scale,'last branch distance')
    require(dist[A[1]][C[-1]]==min(3*scale,scale+elllast),'reflected branch distance')
    for c in C[2:-1]:require(dist[A[0]][c]==3*scale,'far branch distance')
    sequence=[pair([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in 'AD'*m:
        ni=i+1;nj=j+int(letter=='D');L,Rold=bounds(i,j);Lnew,R=bounds(ni,nj)
        a,b=A[i%k],A[ni%k]
        if letter=='A':
            heavy=None
            if j==0:
                paths=[(r,A[0]),(C[0],A[1])];flavor='A_anchor'
            elif j==1 and ell0<2*scale:
                paths=[carriers[3],(A[0],r,A[2])];flavor='A_first_short'
            elif j==m-1:
                paths=[carriers[-1],(r,A[-2],C[-1])];flavor='A_last'
            else:
                require(r in carriers[2*j+1],'reflected A carrier contains root')
                paths=[carriers[2*j+1],(A[2*j],C[j])]
                flavor='A_first_long' if j==1 else 'A_ordinary'
            choices=[pair(paths,[L,R],flavor)]
        else:
            arc=arcs[j];x=coords[j];ell=x[-1]
            if j==0:
                p=max(z for z,t in enumerate(x) if 2*t<=ell+min(2*scale,ell))
                q=min(z for z,t in enumerate(x) if 2*t>=ell+scale)
                H1=Rold-set(arc[1:p+1]);H2=set(arc[1:q])
                first=pair([(A[0],)+arc[:p+1],(r,A[1])],[L,H1],'D_anchor_prefix')
                second=pair([P,(A[1],A[2])+tuple(reversed(arc[q:]))],[L,H2,R],'D_anchor_suffix')
                choices=[first,second];heavy=H1,H2
            else:
                Ea,Eb=carriers[i%k],carriers[ni%k]
                if j==1 and ell0<2*scale:
                    threshold=ell+2*scale-ell0;start=(A[0],r,b);forward='D_first_short'
                else:
                    threshold=ell-(scale if r in Ea else 0)
                    start=(b,) if r in Ea else (r,b);forward='D_forward'
                q=min(z for z,t in enumerate(x) if 2*t>=threshold)
                suffix=start+tuple(reversed(arc[q:]))
                if j==m-2 and elllast<2*scale:
                    threshold2=ell-scale;start2=(A[0],r,a);backward='D_last_short'
                else:
                    threshold2=ell+(scale if r in Eb else 0)
                    start2=(a,) if r in Eb else (r,a);backward='D_backward'
                p=max(z for z,t in enumerate(x) if 2*t<=threshold2)
                prefix=start2+arc[:p+1]
                H1=L|gamma[j]|set(arc[1:q]);H2=R|gamma[nj%m]|set(arc[p+1:-1])
                first=pair([Ea,suffix],[H1,R],forward);second=pair([Eb,prefix],[L,H2],backward)
                choices=[first,second];heavy=H1,H2
                require(threshold<=threshold2,'ordered D thresholds')
            require(q<=p+1,'D coordinate overlap')
        if heavy is not None:
            require(not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented,'disjoint potentially heavy supports')
            result['disjoint_checks']+=1
        transitions.append(choices);i,j=ni,nj
        sequence.append(pair([P,(r,A[i%k],C[j%m])],[Lnew,R],'spoke'))
    result['systems']+=1;result['component_cuts']+=len(cuts)
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,sequence=sequence,transitions=transitions,cuts=cuts,
                outer=A,branches=C,arcs=arcs,coords=coords,sectors=kappa)


def targeted_profiles(sys,n,scale):
    """Sector and inner-arc mass cases at the first and last A steps."""
    K=sys['sectors'];arcs=sys['arcs'];coords=sys['coords']
    def profile(entries):
        w=[0]*n
        for v,mass in entries:w[v]+=mass
        return w
    if coords[0][-1]<2*scale:
        yield profile([(min(K[1]),3),(min(K[2]),4),(min(K[4]),3)])
        late=[v for v,x in zip(arcs[0][1:-1],coords[0][1:-1]) if 2*x>coords[0][-1]]
        if late:yield profile([(late[0],4),(min(K[2]),3),(min(K[4]),3)])
    if coords[-1][-1]<2*scale:
        yield profile([(min(K[-2]),4),(min(K[-1]),3),(min(K[-4]),3)])
        early=[v for v,x in zip(arcs[-1][1:-1],coords[-1][1:-1]) if 2*x<coords[-1][-1]]
        if early:yield profile([(early[0],4),(min(K[-2]),3),(min(K[-4]),3)])


def designs():
    for index,m in enumerate([4,4,5,6,7,8]):
        scale=F(1+index%3,1+(index//3))
        patterns=[[scale],[3*scale/4,scale/4],[scale/4,3*scale/4],
                  [scale/3]*3,[scale/4,scale,scale/4],
                  [scale/3,4*scale/3,scale/3],
                  [scale/5,scale,scale],[5*scale/7,scale/7,scale/7]]
        lengths=[[scale] for _ in range(m)] if index==0 else [patterns[(j+index)%len(patterns)] for j in range(m)]
        yield m,scale,lengths


def main():
    result=Counter();rng=random.Random(2026092920)
    for m,scale,lengths in designs():
        g,A,C,arcs=single.core_graph('AD'*m,scale,lengths);core=set(range(len(g.adj)));before=g.distances()
        for i,a in enumerate(A):
            if i%2==0:g.attach(2,(0,a,A[(i+1)%len(A)]),long_edges=scale)
            first=len(g.adj);fan.previous.old.ears(g,len(A),i,3)
            for u in range(first,len(g.adj)):
                for v in g.adj[u]:g.adj[u][v]=g.adj[v][u]=scale
        g.attach(2,(0,A[1]),long_edges=scale)
        g.sphere();dist=g.distances()
        require(all(dist[u][v]==before[u][v] for u in core for v in core),'core isometry')
        for piece in g.pieces:g.check_local_decomposition(piece);result['local_decompositions']+=1
        profiles=list(single.base.masses(g,rng))
        for shift in range(m):
            for reverse in [False,True]:
                sys=system(g,A,C,arcs,core,dist,scale,result,shift,reverse)
                for masses in profiles+list(targeted_profiles(sys,len(g.adj),scale)):
                    cut,twice_h=metric.choose(sys,masses,result)
                    if any(2*sum(masses[v] for v in K)>sum(masses) for K in sys['outside']):
                        fan.previous.old.heavy(g,dist,masses,result)
                    else:
                        require(twice_h<=sum(masses),'light K half bound')
                        require(all(2*sum(masses[v] for v in K)<=sum(masses) for K in cut['parts']),'actual half balance')
                        result['light_half_checks']+=1
                        mass=lambda K:sum(masses[v] for v in K)
                        result['nonmaximum_anchor_light_checks']+=int(mass(sys['sectors'][0])<max(mass(K) for K in sys['sectors'][::2]))
                result['fixture_orientations']+=1
        result['fixtures']+=1
    # Additional geometry-only metrics exercise every short/long endpoint regime.
    for trial in range(100):
        m=4+trial%6;scale=F(4)
        shapes=[[4],[3,1],[1,3],[1,1,2],[1,3,1],[3,1,2],[1,5,1],[3,2,3],[1,4,4],[1,8,3]]
        lengths=[list(map(F,rng.choice(shapes))) for _ in range(m)]
        g,A,C,arcs=single.core_graph('AD'*m,scale,lengths);core=set(range(len(g.adj)));dist=g.distances()
        for reverse in [False,True]:system(g,A,C,arcs,core,dist,scale,result,trial%m,reverse)
        result['additional_core_models']+=1
    for flavor in ['A_first_short','A_last','D_first_short','D_last_short']:
        require(result[flavor+'_choices']>0,'mass branch exercised: '+flavor)
    return dict(sorted(result.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2,sort_keys=True))
