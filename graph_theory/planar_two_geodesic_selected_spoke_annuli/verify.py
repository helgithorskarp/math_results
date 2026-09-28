#!/usr/bin/env python3
"""Exact regressions; the selected-spoke annulus theorem is proved in README."""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('quadrilaterals',HERE.parent/'planar_two_geodesic_quadrilateral_annuli/verify.py')
quad=importlib.util.module_from_spec(spec);spec.loader.exec_module(quad)
fan,base,require=quad.fan,quad.base,quad.require


def validate(word):
    require(word and set(word)<=set('ACD'),'staircase word')
    k,m=sum(x in 'AD' for x in word),sum(x in 'CD' for x in word)
    require(k>=3 and m>=3,'cycle orders')
    require(quad.maximum_run(word,'A')<=k-2 and quad.maximum_run(word,'C')<=m-2,'wrap bounds')
    return k,m


def bad_positions(word):
    return [s for s,x in enumerate(word) if x=='A' and word[s-1]=='D' and word[(s+1)%len(word)]=='D']


def core_graph(word,scale=1):
    k,m=validate(word)
    A=list(range(1,k+1));C=list(range(k+1,k+m+1))
    edges={};faces=[]
    def edge(a,b,length=scale):edges[tuple(sorted((a,b)))]=length
    for i in range(k):
        edge(0,A[i]);edge(A[i],A[(i+1)%k]);faces.append((0,A[i],A[(i+1)%k]))
    for j in range(m):edge(C[j],C[(j+1)%m],scale*(1+(2*j+m)%5))
    i=j=0;states=[]
    for letter in word:
        a,c=A[i%k],C[j%m];edge(a,c);states.append((a,c))
        if letter=='A':faces.append((a,c,A[(i+1)%k]));i+=1
        elif letter=='C':faces.append((a,c,C[(j+1)%m]));j+=1
        else:faces.append((a,c,C[(j+1)%m],A[(i+1)%k]));i+=1;j+=1
    require(len(set(states))==len(word),'distinct cross states')
    faces.append(tuple(reversed(C)))
    g=base.Graph(1+k+m,[(a,b,l) for (a,b),l in edges.items()],faces)
    g.sphere()
    return g,A,C


def system(g,original_A,original_C,original_word,core,dist,shift,result):
    word=original_word[shift:]+original_word[:shift]
    require(not(word[0]==word[-1]=='A'),'seam does not split A-run')
    ai=sum(x in 'AD' for x in original_word[:shift]);cj=sum(x in 'CD' for x in original_word[:shift])
    A=original_A[ai:]+original_A[:ai];C=original_C[cj:]+original_C[:cj]
    has_bad=bool(bad_positions(word))
    require(not has_bad or 0 in bad_positions(word),'maximum-sector anchor is a DAD position')
    k,m=len(A),len(C);P=(0,A[0],C[0])
    alpha=[set()]+[{a} for a in A[1:]];gamma=[set()]+[{c} for c in C[1:]]
    kappa=[set() for _ in A];discarded=set();outside=g.components(core)
    for K in outside:
        N=set().union(*(set(g.adj[v]) for v in K))&core;Y=N&set(A)
        require(N<=Y|{0} and len(Y)<=2,'root clique boundary')
        if len(Y)==2:
            sites=[i for i in range(k) if Y=={A[i],A[(i+1)%k]}]
            require(len(sites)==1,'one sector');kappa[sites[0]]|=K
        elif Y and A[0] not in Y:alpha[A.index(next(iter(Y)))]|=K
        else:discarded|=K
    represented=set(range(len(g.adj)))-set(P)-discarded;atoms=alpha+gamma+kappa
    require(set().union(*atoms)==represented and sum(map(len,atoms))==len(represented),'mass partition')
    def atom(xs,i):return xs[i%len(xs)]
    def bounds(i,j):
        L=set().union(*(alpha[s]|kappa[s] for s in range(i)),*(gamma[q] for q in range(j)))
        return L,represented-L-atom(alpha,i)-atom(gamma,j)
    cuts=[]
    def prepare(path,sides):
        g.check_path(path,dist);parts=g.components(set(P)|set(path))
        for K in parts:
            if K&core:require(any(K<=S for S in sides),'component containment')
            else:require(K in outside,'one whole detached attachment')
        answer=dict(path=path,sides=sides,parts=parts);cuts.append(answer);return answer
    sequence=[prepare(P,bounds(0,0))];transitions=[];fans=[];i=j=pos=0
    while pos<len(word):
        letter=word[pos];L,R=bounds(i,j)
        if letter=='A':
            d=1
            while pos+d<len(word) and word[pos+d]=='A':d+=1
            l,t=i,i+d;LN,RN=bounds(t,j)
            if d>=2:
                F=set().union(*(alpha[s] for s in range(l+1,t)),*(kappa[s] for s in range(l,t)))
                require(F in g.components({0,C[j%m],A[l%k],A[t%k]}),'whole long fan')
                fans.append(fan.fan_decomposition(g,A,C[j%m],l,t,F,dist))
                choices=[prepare((A[l%k],C[j%m],A[t%k]),[L,RN,F])];label='long_fan_choices'
            elif C[j%m]==C[0]:
                choices=[prepare((A[l%k],A[t%k]),[L,RN])];label='seam_choices'
            elif word[(pos+1)%len(word)]=='C':
                choices=[prepare((A[l%k],A[t%k],C[(j+1)%m]),[L|atom(gamma,j),RN])];label='forward_C_choices'
            elif word[pos-1]=='C':
                choices=[prepare((A[t%k],A[l%k],C[(j-1)%m]),[L,RN|atom(gamma,j)])];label='backward_C_choices'
            else:
                require(pos in bad_positions(word),'only DAD remains')
                if j==1:
                    choices=[prepare((A[1],A[l%k],A[t%k]),[represented-LN])];label='forward_neighbor_choices'
                elif j==m-1:
                    choices=[prepare((A[l%k],A[t%k],A[0]),[represented-R])];label='backward_neighbor_choices'
                else:
                    choices=[prepare((A[1],0,A[t%k],C[j%m]),[LN-kappa[0],RN])];label='far_singleton_choices'
                result['bad_component_cuts']+=1
            for _ in range(d):
                i+=1;sequence.append(prepare((0,A[i%k],C[j%m]),bounds(i,j)));transitions.append((label,choices))
            pos+=d
        elif letter=='C':
            LN,RN=bounds(i,j+1)
            require(not R&LN and R|LN<=represented,'C transition cannot have two heavy sides')
            result['C_identities']+=1;j+=1;pos+=1
            new=prepare((0,A[i%k],C[j%m]),[LN,RN]);sequence.append(new);transitions.append(('C_choices',[new]))
        else:
            LN,RN=bounds(i+1,j+1)
            a,b,c,e=A[i%k],A[(i+1)%k],C[j%m],C[(j+1)%m]
            old=prepare((0,a,c),[L,R]);new=prepare((0,b,e),[LN,RN])
            plus=prepare((a,b,e),[L|atom(gamma,j),RN]);minus=prepare((b,a,c),[L,RN|atom(gamma,j+1)])
            coeff=Counter(v for S in [R,LN,plus['sides'][0],minus['sides'][1]] for v in S)
            require(all(coeff[v]==2-int(v in atom(alpha,i)|atom(alpha,i+1)) for v in represented),'D four-side identity')
            result['D_identities']+=1;i+=1;j+=1;pos+=1
            sequence.append(new);transitions.append(('D_choices',[old,new,plus,minus]))
    require(i==k and j==m,'full sweep')
    result['systems']+=1;result['component_cuts']+=len(cuts);result['fan_decompositions']+=len(fans)
    return dict(P=P,sequence=sequence,transitions=transitions,fans=fans,patches=[],covers=[],outside=outside,
                mass_set=represented,discarded=discarded,sector_groups=kappa,anchor_sector=kappa[0] if has_bad else set())


def quantitative(g,sys,w,result):
    def mass(K):return sum(w[v] for v in K)
    M=mass(sys['mass_set']);require(M==sum(w)-mass(sys['P'])-mass(sys['discarded']),'represented mass')
    bound2=max(M,2*max(map(mass,sys['outside']),default=0),2*max((mass(F['internal']) for F in sys['fans']),default=0))
    def valid(parts):return all(2*mass(K)<=bound2 for K in parts)
    chosen=None
    for j,cut in enumerate(sys['sequence']):
        if valid(cut['sides']):chosen=cut;break
        if j and 2*mass(sys['sequence'][j-1]['sides'][1])>bound2 and 2*mass(cut['sides'][0])>bound2:
            label,options=sys['transitions'][j-1]
            chosen=next((q for q in options if valid(q['sides'])),None)
            require(chosen is not None,'maximum-sector exchange')
            result['quant_'+label]=result.get('quant_'+label,0)+1
            break
    require(chosen is not None and valid(chosen['parts']),'quantitative full-graph balance')
    result['quantitative_checks']+=1;result['sharper_than_half']+=int(bound2<sum(w))


CONTROL=json.loads((HERE/'control.json').read_text())
STACK_FACES=CONTROL['stack_faces']
OBSTRUCTION_WEIGHTS=CONTROL['positive_weights']


def stacked_control(result):
    word='AD'*5;g,A,C=core_graph(word)
    # For this obstruction every core edge, including every rim edge, is unit.
    for a,b in zip(C,C[1:]+C[:1]):g.adj[a][b]=g.adj[b][a]=1
    core=set(range(len(g.adj)));original=g.distances()
    for group in range(3):
        bags=[];tree=[];inside=set();boundary=set(STACK_FACES[12*group])
        for triple in STACK_FACES[12*group:12*(group+1)]:
            face=next(f for f in g.faces if len(f)==3 and set(f)==set(triple))
            g.faces.remove(face);x=len(g.adj);g.adj.append({});inside.add(x)
            for a in face:g.edge(a,x,1)
            g.faces.extend((face[i],face[(i+1)%3],x) for i in range(3))
            if bags:tree.append((next(i for i,B in enumerate(bags) if set(triple)<=B),len(bags)))
            bags.append(set(triple)|{x})
        g.pieces.append(dict(internal=inside,boundary=boundary,bags=bags,tree=tree))
    g.sphere();dist=g.distances()
    require(all(dist[a][b]==original[a][b] for a in core for b in core),'control core isometry')
    for piece in g.pieces:g.check_local_decomposition(piece)
    w=[0]*len(g.adj)
    for v,value in OBSTRUCTION_WEIGHTS:w[v]=value
    P=(0,A[0],C[0]);paths={}
    for s in range(len(g.adj)):
        for Q in g.paths(s,range(s,len(g.adj)),dist):paths.setdefault(frozenset(Q),Q)
    optimum=min(max((sum(w[v] for v in K) for K in g.components(set(P)|set(Q))),default=0) for Q in paths.values())
    require(len(g.adj)==52 and sum(w)==37 and optimum==19,'arbitrary-spoke obstruction')
    require(sorted(sum(w[v] for v in K) for K in g.components(core))==[9,14,14],'all three attachments light')
    systems=[system(g,A,C,word,core,dist,j,result) for j in bad_positions(word)]
    maximum=max(sum(w[v] for v in s['anchor_sector']) for s in systems)
    for sys in systems:
        if sum(w[v] for v in sys['anchor_sector'])==maximum:
            quantitative(g,sys,w,result);fan.finish(g,sys,w,dist,result)
    result.update(obstruction_vertices=52,obstruction_geodesics=len(paths),obstruction_mass=37,obstruction_fixed_optimum=optimum,obstruction_max_sector=maximum)


def main():
    result=dict(fixtures=0,systems=0,component_cuts=0,D_identities=0,bad_component_cuts=0,C_identities=0,
                fan_decompositions=0,local_decompositions=0,quantitative_checks=0,sharper_than_half=0,
                heavy_checks=0,heavy_fan_checks=0,heavy_fan_five_bag_choices=0,heavy_fan_multiple_pockets=0,
                light_checks=0,spoke_choices=0,C_choices=0,D_choices=0,long_fan_choices=0,seam_choices=0,forward_C_choices=0,backward_C_choices=0,
                forward_neighbor_choices=0,backward_neighbor_choices=0,far_singleton_choices=0)
    rng=random.Random(2026092815)
    blocks=[[2]*5,[2]*3,[2]*4,[1]*3,[3,1,2,4,1],[1,2,1,1,2,1],[4,3,1],[2,1,2,1,3,1,2],[1]*6]
    designs=[''.join('A'*(n-1)+'D' for n in sizes) for sizes in blocks]
    designs+=['ADCD','ADACDADCCD','ADCADADC','AAADCCAACDDAACCCD','AC'*3,'AACC'*3]
    for index,word in enumerate(designs):
        scale=2 if index%3==1 else 1
        g,A,C=core_graph(word,scale);core=set(range(len(g.adj)));original=g.distances();k=len(A)
        for i in range(k):
            if i%2==0:g.attach(3,(0,A[i],A[(i+1)%k]),long_edges=1)
            fan.previous.old.ears(g,k,i,3);fan.previous.old.ears(g,k,i,4)
        g.attach(2,(0,A[1]),long_edges=1)
        g.sphere();dist=g.distances()
        require(all(dist[a][b]==original[a][b] for a in core for b in core),'core isometry')
        for piece in g.pieces:g.check_local_decomposition(piece);result['local_decompositions']+=1
        anchors=bad_positions(word) or [next(s for s in range(len(word)) if not(word[s]==word[s-1]=='A'))]
        systems=[system(g,A,C,word,core,dist,j,result) for j in anchors]
        profiles=list(base.masses(g,rng))
        if index==0:
            w=[0]*len(g.adj)
            w[min(systems[0]['sector_groups'][0])]=2
            w[min(systems[0]['sector_groups'][-2])]=2
            w[A[-1]]=3
            profiles.append(w)
        for F in systems[0]['fans']:profiles.append([int(v in F['internal']) for v in range(len(g.adj))])
        for w in profiles:
            maximum=max(sum(w[v] for v in s['anchor_sector']) for s in systems)
            for sys in systems:
                if sum(w[v] for v in sys['anchor_sector'])==maximum:
                    quantitative(g,sys,w,result);fan.finish(g,sys,w,dist,result)
        result['fixtures']+=1
    for trial in range(50):
        while True:
            word=''.join(rng.choice('ACD') for _ in range(rng.randrange(5,25)))
            try:validate(word)
            except AssertionError:continue
            break
        g,A,C=core_graph(word);core=set(range(len(g.adj)))
        anchor=(bad_positions(word) or [next(s for s in range(len(word)) if not(word[s]==word[s-1]=='A'))])[0]
        system(g,A,C,word,core,g.distances(),anchor,result)
    result['additional_core_models']=50
    stacked_control(result)
    branches=['D_choices','long_fan_choices','far_singleton_choices','forward_neighbor_choices','backward_neighbor_choices','forward_C_choices','backward_C_choices']
    require(all(result[x]>0 for x in branches),'exchange branches exercised: '+str({x:result[x] for x in branches})+'; quantitative '+str({x:v for x,v in result.items() if x.startswith('quant_')}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected regression counts')
    print(json.dumps(answer,indent=2,sort_keys=True))
