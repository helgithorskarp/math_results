#!/usr/bin/env python3
"""Exact regressions for the written one-anchor mixed-annulus theorem."""
import argparse
from collections import Counter
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('metric',HERE.parent/'planar_two_geodesic_metric_cd_annuli/verify.py')
metric=importlib.util.module_from_spec(spec);spec.loader.exec_module(metric)
mixed,base,fan,require=metric.mixed,metric.base,metric.fan,metric.require


def core_graph(word,scale,lengths):
    require(scale>0,'positive scale')
    g,A,C,arcs=mixed.core_graph(word,list(map(len,lengths)),scale)
    for arc,prices in zip(arcs,lengths):
        require(prices and all(x>0 for x in prices) and sum(prices)>=scale,'arc total at least scale')
        for u,v,price in zip(arc,arc[1:],prices):g.adj[u][v]=g.adj[v][u]=price
    g.sphere()
    return g,A,C,arcs


def local_anchor(g,A,C,arcs,scale,j):
    j%=len(C)
    neighbors=set(g.adj[C[j]])&set(A)
    if len(neighbors)!=1:return False
    a=next(iter(neighbors));i=A.index(a)
    near={a,A[i-1],A[(i+1)%len(A)]}
    for arc,z in [(arcs[j],C[(j+1)%len(C)]),(arcs[j-1],C[j-1])]:
        length=sum(g.adj[u][v] for u,v in zip(arc,arc[1:]))
        if length<2*scale and not (set(g.adj[z])&set(A))<=near:return False
    return True


def states(word):
    i=j=0
    for pos,letter in enumerate(word):
        yield pos,i,j
        i+=int(letter in 'AD');j+=int(letter in 'CD')


def system(g,original_A,original_C,original_arcs,original_word,core,dist,scale,result,shift):
    ai=sum(x in 'AD' for x in original_word[:shift]);cj=sum(x in 'CD' for x in original_word[:shift])
    A=original_A[ai:]+original_A[:ai];C=original_C[cj:]+original_C[:cj]
    arcs=original_arcs[cj:]+original_arcs[:cj]
    word=original_word[shift:]+original_word[:shift]
    k,m=len(A),len(C);P=(0,A[0],C[0])
    require(local_anchor(g,A,C,arcs,scale,0),'eligible anchor')
    alpha=[set()]+[{a} for a in A[1:]]
    gamma=[set()]+[{c} for c in C[1:]]
    tau=[set(arc[1:-1]) for arc in arcs]
    kappa=[set() for _ in A];discarded=set();outside=g.components(core)
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
            if K&core:require(any(K<=side for side in sides),'full component containment')
            else:require(K in outside,'whole detached attachment')
        cut=dict(paths=paths,sides=sides,parts=parts,flavor=flavor);cuts.append(cut);return cut
    carriers=[]
    for i,a in enumerate(A):
        path=(C[0],A[0]) if i==0 else ((C[0],A[0],a) if i in [1,k-1] else (C[0],A[0],0,a))
        g.check_path(path,dist);carriers.append(path)
    sequence=[prepare([P],bounds(0,0),'spoke')];transitions=[];i=j=0
    for letter in word:
        L,Rold=bounds(i,j);ni=i+int(letter in 'AD');nj=j+int(letter in 'CD')
        Lnew,R=bounds(ni,nj);a,b=A[i%k],A[ni%k]
        if letter=='A':
            ea=carriers[i%k]
            other=(b,C[j%m]) if 0 in ea else (0,b,C[j%m])
            choices=[prepare([ea,other],[L,R],'A')]
            result['A_exchanges']+=1
            result['A_root_carrier_exchanges']+=int(0 in ea)
            result['A_other_root_exchanges']+=int(0 not in ea)
        else:
            arc=arcs[j];x=[0]
            for u,v in zip(arc,arc[1:]):x.append(x[-1]+g.adj[u][v])
            ell=x[-1]
            if letter=='C':
                p=max(z for z,t in enumerate(x) if 2*t<=ell)
                q=min(z for z,t in enumerate(x) if 2*t>=ell)
                left=prepare([P,(0,a)+arc[:p+1]],[L,Rold-set(arc[1:p+1])],'C_left')
                right=prepare([P,(0,a)+tuple(reversed(arc[q:]))],[Lnew-set(arc[q:-1]),R],'C_right')
                heavy=left['sides'][1],right['sides'][0];choices=[left,right]
                result['C_exchanges']+=1
            else:
                ea,eb=carriers[i%k],carriers[ni%k]
                q=min(z for z,t in enumerate(x) if 2*t>=ell-(scale if 0 in ea else 0))
                p=max(z for z,t in enumerate(x) if 2*t<=ell+(scale if 0 in eb else 0))
                suffix=((b,) if 0 in ea else (0,b))+tuple(reversed(arc[q:]))
                prefix=((a,) if 0 in eb else (0,a))+arc[:p+1]
                left=prepare([ea,suffix],[L|atom(gamma,j)|set(arc[1:q]),R],'D_left')
                right=prepare([eb,prefix],[L,R|atom(gamma,nj)|set(arc[p+1:-1])],'D_right')
                require(q<=p+1,'overlapping threshold coverage')
                heavy=left['sides'][0],right['sides'][1];choices=[left,right]
                result['D_exchanges']+=1
            require(not heavy[0]&heavy[1] and heavy[0]|heavy[1]<=represented,'disjoint heavy supports')
        i,j=ni,nj
        sequence.append(prepare([P,(0,A[i%k],C[j%m])],(Lnew,R),'spoke'))
        transitions.append(choices)
    require((i,j)==(k,m),'full sweep')
    result['systems']+=1;result['component_cuts']+=len(cuts)
    return dict(anchor=P,mass_set=represented,discarded=discarded,outside=outside,
                sequence=sequence,transitions=transitions,cuts=cuts)


def long_fans(word,A,C,g,core):
    answer=[]
    for pos,i,j in states(word):
        if word[pos]!='A' or word[pos-1]=='A':continue
        length=0
        while word[(pos+length)%len(word)]=='A':length+=1
        if length<2:continue
        internal={A[(i+z)%len(A)] for z in range(1,length)}
        edges=[{A[(i+z)%len(A)],A[(i+z+1)%len(A)]} for z in range(length)]
        for K in g.components(core):
            Y=set().union(*(set(g.adj[v]) for v in K))&set(A)
            if len(Y)==1 and Y<=internal or len(Y)==2 and Y in edges:internal|=K
        answer.append(internal)
    return answer


def designs():
    words=['ADDDDD','AAAAADDDDD','DADDDD','AAADCCAACDDAACCCD','CCDAADCCDD','D'*3]
    for index,word in enumerate(words):
        scale=F(1+index%3);m=sum(x in 'CD' for x in word)
        choices=[[scale],[3*scale/4,scale/2,3*scale/4],
                 [scale/4,scale/2,scale/4],[scale/3,2*scale,scale/7]]
        yield word,scale,[choices[(j+index)%len(choices)] for j in range(m)]


def main():
    result=Counter();rng=random.Random(2026092918)
    for word,scale,lengths in designs():
        g,A,C,arcs=core_graph(word,scale,lengths)
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
        eligible=[]
        for shift,i,j in states(word):
            local=local_anchor(g,A,C,arcs,scale,j)
            gate=all(dist[C[j%len(C)]][a]==scale+(0 if a==A[i%len(A)] else scale if a in [A[(i-1)%len(A)],A[(i+1)%len(A)]] else 2*scale) for a in A)
            require(local==gate,'exact local anchor criterion')
            result['anchor_criteria']+=1
            result['rejected_anchors']+=int(not local)
            if local:eligible.append(shift)
        require(eligible,'fixture has an anchor')
        profiles=list(base.masses(g,rng));fans=long_fans(word,A,C,g,core)
        for arc in arcs:profiles.append([int(v in arc[1:-1]) for v in range(len(g.adj))])
        for region in fans:profiles.append([int(v in region) for v in range(len(g.adj))])
        for shift in eligible:
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
        result['fixtures']+=1
    accepted=0
    for trial in range(80):
        while True:
            word=''.join(rng.choice('ACD') for _ in range(rng.randrange(6,19)))
            try:k,m=mixed.validate(word)
            except AssertionError:continue
            break
        scale=F(2)
        lengths=[[scale] if rng.randrange(2) else [F(1,3),2*scale,F(2,3)] for _ in range(m)]
        g,A,C,arcs=core_graph(word,scale,lengths);core=set(range(len(g.adj)));dist=g.distances()
        for shift,i,j in states(word):
            local=local_anchor(g,A,C,arcs,scale,j)
            expected=all(dist[C[j%m]][a]==scale+(0 if a==A[i%k] else scale if a in [A[(i-1)%k],A[(i+1)%k]] else 2*scale) for a in A)
            require(local==expected,'random exact criterion')
            result['anchor_criteria']+=1
            if local:
                system(g,A,C,arcs,word,core,dist,scale,result,shift);accepted+=1
        result['additional_core_models']+=1
    require(accepted,'additional anchored systems')
    for word in ['AD'*5,'AC'*5]:
        g,A,C,arcs=core_graph(word,F(1),[[F(2)]]*5)
        require(not any(local_anchor(g,A,C,arcs,F(1),j) for j in range(5)),'no anchor in double-parent cycle')
        result['no_anchor_controls']+=1
    for key in ['A_choices','A_root_carrier_exchanges','A_other_root_exchanges','C_left_choices','C_right_choices',
                'D_left_choices','D_right_choices','heavy_fan_without_replacement','heavy_checks']:
        require(result[key]>0,'branch exercised: '+key)
    return dict(sorted(result.items()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2,sort_keys=True))
