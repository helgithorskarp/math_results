#!/usr/bin/env python3
"""Exact regressions for the written two-parent mixed-annulus theorem."""
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
metric=single.metric
mixed,base,fan,require=single.mixed,single.base,single.fan,single.require


def eligible(g,A,C,arcs,word,scale,shift):
    k=len(A);m=len(C)
    if k<5 or not (word[shift]=='A' and word[shift-1]=='D' and word[(shift+1)%len(word)]=='D'):return False
    ai=sum(x in 'AD' for x in word[:shift])%k;cj=sum(x in 'CD' for x in word[:shift])%m
    outer=A[ai:]+A[:ai]
    near=set(g.adj[outer[2]])|set(g.adj[outer[3]])
    if near&set(g.adj[outer[-1]])&set(C):return False
    for arc in [arcs[cj],arcs[cj-1]]:
        if sum(g.adj[u][v] for u,v in zip(arc,arc[1:]))<2*scale:return False
    return True


def system(g,original_A,original_C,original_arcs,original_word,core,dist,scale,result,shift):
    require(eligible(g,original_A,original_C,original_arcs,original_word,scale,shift),'eligible two-parent anchor')
    ai=sum(x in 'AD' for x in original_word[:shift]);cj=sum(x in 'CD' for x in original_word[:shift])
    A=original_A[ai:]+original_A[:ai];C=original_C[cj:]+original_C[:cj]
    arcs=original_arcs[cj:]+original_arcs[:cj];word=original_word[shift:]+original_word[:shift]
    k,m=len(A),len(C);P=(0,A[0],C[0])
    require(set(g.adj[C[0]])&set(A)=={A[0],A[1]},'two outer parents')
    require(all(set(g.adj[a])&set(C)=={C[0]} for a in A[:2]),'two single-inner parent sites')
    for c in set(C)&(set(g.adj[A[2]])|set(g.adj[A[3]])):
        require(dist[A[0]][c]==3*scale,'complement endpoint distance')
        result['complement_distances']+=1
    alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    tau=[set(arc[1:-1]) for arc in arcs];kappa=[set() for _ in A]
    discarded=set();outside=g.components(core)
    for K in outside:
        N=set().union(*(set(g.adj[v]) for v in K))&core;Y=N&set(A)
        require(N<=Y|{0} and len(Y)<=2,'root-clique boundary')
        if len(Y)==2:
            sites=[i for i in range(k) if Y=={A[i],A[(i+1)%k]}]
            require(len(sites)==1,'consecutive active boundary');kappa[sites[0]]|=K
        elif Y and A[0] not in Y:alpha[A.index(next(iter(Y))) ]|=K
        else:discarded|=K
    represented=set(range(len(g.adj)))-set(P)-discarded
    groups=alpha+gamma+tau+kappa
    require(set().union(*groups)==represented and sum(map(len,groups))==len(represented),'mass partition')
    def atom(values,i):return values[i%len(values)]
    def bounds(i,j):
        L=set().union(*(alpha[s]|kappa[s] for s in range(i)),*(gamma[t]|tau[t] for t in range(j)))
        return L,represented-L-atom(alpha,i)-atom(gamma,j)
    cuts=[]
    def prepare(paths,sides,flavor):
        require(len(paths)<=2,'two paths')
        for path in paths:g.check_path(path,dist)
        removed=set().union(*map(set,paths));require(set(P)<=removed,'anchor triple preserved')
        parts=g.components(removed)
        for K in parts:
            if K&core:require(any(K<=side for side in sides),('full component containment',word,flavor,paths,K,sides))
            else:require(K in outside,'whole detached attachment')
        cut=dict(paths=paths,sides=sides,parts=parts,flavor=flavor);cuts.append(cut);return cut
    carriers=[]
    for i,a in enumerate(A):
        if i==0:path=(C[0],A[0])
        elif i==1:path=(C[0],A[1])
        elif i==2:path=(C[0],A[1],A[2])
        elif i==k-1:path=(C[0],A[0],a)
        else:path=(C[0],A[0],0,a)
        g.check_path(path,dist);carriers.append(path)
        result['carriers']+=1
    sequence=[prepare([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in word:
        L,Rold=bounds(i,j);ni=i+int(letter in 'AD');nj=j+int(letter in 'CD')
        Lnew,R=bounds(ni,nj);a,b=A[i%k],A[ni%k]
        if letter=='A':
            ea=carriers[i%k]
            require(i%k!=1,'anchor second parent exits by D')
            if i%k==2:
                other=(A[0],0,b,C[j%m]);flavor='A_repacked';result['A_repacked_exchanges']+=1
            else:
                other=(b,C[j%m]) if 0 in ea else (0,b,C[j%m]);flavor='A';result['A_exchanges']+=1
            choices=[prepare([ea,other],[L,R],flavor)]
        else:
            arc=arcs[j];x=[0]
            for u,v in zip(arc,arc[1:]):x.append(x[-1]+g.adj[u][v])
            ell=x[-1]
            if letter=='C':
                p=max(z for z,t in enumerate(x) if 2*t<=ell);q=min(z for z,t in enumerate(x) if 2*t>=ell)
                left=prepare([P,(0,a)+arc[:p+1]],[L,Rold-set(arc[1:p+1])],'C_left')
                right=prepare([P,(0,a)+tuple(reversed(arc[q:]))],[Lnew-set(arc[q:-1]),R],'C_right')
                heavy=left['sides'][1],right['sides'][0];choices=[left,right];result['C_exchanges']+=1
            elif i==1 and j==0:
                p=max(z for z,t in enumerate(x) if 2*t<=ell+2*scale)
                q=min(z for z,t in enumerate(x) if 2*t>=ell+scale)
                left=prepare([(A[0],)+arc[:p+1],(0,A[1])],[L,Rold-set(arc[1:p+1])],'D_anchor_prefix')
                right=prepare([P,(A[1],A[2])+tuple(reversed(arc[q:]))],[L,set(arc[1:q]),R],'D_anchor_suffix')
                require(q<=p+1,'anchor threshold coverage')
                heavy=left['sides'][1],right['sides'][1];choices=[left,right]
                result['D_anchor_exchanges']+=1
            else:
                require(i%k!=1 and ni%k not in [1,2],'only exceptional D handled above')
                ea,eb=carriers[i%k],carriers[ni%k]
                if i%k==2:
                    q=min(z for z,t in enumerate(x) if 2*t>=ell)
                    suffix=(A[0],0,b)+tuple(reversed(arc[q:]))
                    result['D_repacked_exchanges']+=1;flavor='D_repacked_left'
                else:
                    q=min(z for z,t in enumerate(x) if 2*t>=ell-(scale if 0 in ea else 0))
                    suffix=((b,) if 0 in ea else (0,b))+tuple(reversed(arc[q:]));flavor='D_left'
                p=max(z for z,t in enumerate(x) if 2*t<=ell+(scale if 0 in eb else 0))
                prefix=((a,) if 0 in eb else (0,a))+arc[:p+1]
                left=prepare([ea,suffix],[L|atom(gamma,j)|set(arc[1:q]),R],flavor)
                right=prepare([eb,prefix],[L,R|atom(gamma,nj)|set(arc[p+1:-1])],'D_right')
                require(q<=p+1,'normal threshold coverage')
                heavy=left['sides'][0],right['sides'][1];choices=[left,right]
                result['D_exchanges']+=1
            require(not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented,'disjoint heavy supports')
        i,j=ni,nj
        sequence.append(prepare([P,(0,A[i%k],C[j%m])],(Lnew,R),'spoke'))
        transitions.append(choices)
    require((i,j)==(k,m),'full sweep')
    result['systems']+=1;result['component_cuts']+=len(cuts)
    dads=[s for pos,s,t in single.states(word)
          if word[pos]=='A' and word[pos-1]=='D' and word[(pos+1)%len(word)]=='D']
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,
                sequence=sequence,transitions=transitions,cuts=cuts,
                anchor_sector=kappa[0],dad_sectors=[kappa[s%k] for s in dads])


def designs():
    words=['AD'*3,'AD'*5,'ADAAADDDDD','ADCCADCDDD','ADCCDDADDD','ADDDDD','ADCCCAADCCDDDD']
    for index,word in enumerate(words):
        scale=F(1+index%3);m=sum(x in 'CD' for x in word)
        choices=[[scale],[3*scale/4,scale/2,3*scale/4],
                 [scale/4,scale/2,scale/4],[scale/3,2*scale,scale/7]]
        lengths=[choices[(j+index)%len(choices)] for j in range(m)]
        lengths[0]=[scale/5,8*scale/5,scale/5]
        lengths[-1]=[scale/3,2*scale,scale/7]
        yield word,scale,lengths


def main():
    result=Counter();rng=random.Random(2026092919)
    for word,scale,lengths in designs():
        g,A,C,arcs=single.core_graph(word,scale,lengths)
        core=set(range(len(g.adj)));d0=g.distances()
        for i in range(len(A)):
            if i%2==0:g.attach(3,(0,A[i],A[(i+1)%len(A)]),long_edges=scale)
            start=len(g.adj);fan.previous.old.ears(g,len(A),i,3)
            for u in range(start,len(g.adj)):
                for v in g.adj[u]:g.adj[u][v]=g.adj[v][u]=scale
        g.attach(2,(0,A[1]),long_edges=scale)
        g.sphere();dist=g.distances()
        require(all(dist[u][v]==d0[u][v] for u in core for v in core),'core isometry')
        for piece in g.pieces:g.check_local_decomposition(piece);result['local_decompositions']+=1
        anchors=[z for z in range(len(word)) if eligible(g,A,C,arcs,word,scale,z)]
        require(anchors,('fixture has no eligible anchor',word))
        profiles=list(base.masses(g,rng));fans=single.long_fans(word,A,C,g,core)
        for arc in arcs:profiles.append([int(v in arc[1:-1]) for v in range(len(g.adj))])
        for region in fans:profiles.append([int(v in region) for v in range(len(g.adj))])
        for shift in anchors:
            sys=system(g,A,C,arcs,word,core,dist,scale,result,shift)
            for masses in profiles:
                cut,twice_h=metric.choose(sys,masses,result)
                if any(2*sum(masses[v] for v in K)>sum(masses) for K in sys['outside']):
                    fan.previous.old.heavy(g,dist,masses,result)
                else:
                    require(twice_h<=sum(masses),'light K half bound')
                    require(all(2*sum(masses[v] for v in K)<=sum(masses) for K in cut['parts']),'all-mass half residual')
                    result['light_half_checks']+=1
                    result['heavy_fan_without_replacement']+=int(any(2*sum(masses[v] for v in R)>sum(masses) for R in fans))
                    mass=lambda S:sum(masses[v] for v in S)
                    result['nonmaximum_anchor_light_checks']+=int(mass(sys['anchor_sector'])<max(map(mass,sys['dad_sectors'])))
        result['fixtures']+=1
    for trial in range(100):
        while True:
            word='AD'+''.join(rng.choice('ACD') for _ in range(rng.randrange(3,15)))+'D'
            try:k,m=mixed.validate(word)
            except AssertionError:continue
            if k>=5:break
        scale=F(2);lengths=[[F(1,3),2*scale,F(2,3)] for _ in range(m)]
        g,A,C,arcs=single.core_graph(word,scale,lengths);core=set(range(len(g.adj)));dist=g.distances()
        anchors=[z for z in range(len(word)) if eligible(g,A,C,arcs,word,scale,z)]
        result['additional_core_models']+=1;result['models_without_anchor']+=int(not anchors)
        for shift in anchors:system(g,A,C,arcs,word,core,dist,scale,result,shift)
    for key in ['D_anchor_prefix_choices','D_anchor_suffix_choices','A_repacked_choices','D_repacked_left_choices','heavy_fan_without_replacement','nonmaximum_anchor_light_checks']:
        require(result[key]>0,'branch exercised: '+key)
    return dict(sorted(result.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2,sort_keys=True))
