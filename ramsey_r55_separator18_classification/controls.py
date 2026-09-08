#!/usr/bin/env python3
"""Definition-level controls and physical certificates, including both new routes."""
import copy
import json
import random
from collections import Counter
from itertools import combinations
from pathlib import Path
import derive
import extract
import verify_five

HERE=Path(__file__).resolve().parent

def packed(adj,separator,color='red'):
    code=sum((adj[u]>>v&1)<<k for k,(u,v) in enumerate(combinations(range(43),2)))
    return {'n':43,'red_hex':f'{code:0226x}','separator':sorted(separator),'cut_color':color}

def edge(adj,u,v):
    adj[u]|=1<<v
    adj[v]|=1<<u

def boundary_fixture(red_separator_edge):
    # Attributed exact graph6 catalog records; these fixtures are NOT good43.
    fa=derive.graph6((HERE/'r35_12.g6').read_text().splitlines()[2])
    fb=derive.graph6('Ls`?XGRQR@B`Kc')
    red_a=[((1<<12)-1)^(1<<v)^fa[v] for v in range(12)]
    red_b=[((1<<13)-1)^(1<<v)^fb[v] for v in range(13)]
    special=[q for q in combinations(range(12),4) if derive.independent(fa,q) and not any(derive.independent(fa,t) for t in combinations(set(range(12))-set(q),4))]
    if special!=[(0,1,2,3)]:
        raise ValueError('physical special-four control changed')
    # Find an actual K4-free red contact set on the 13-side.
    nb=None
    for size in range(8,-1,-1):
        for q in combinations(range(13),size):
            mask=sum(1<<v for v in q)
            if extract.clique(red_b,mask,4) is None:
                nb=q
                break
        if nb is not None:
            break
    adj=[0]*43
    for u,v in combinations(range(12),2):
        if red_a[u]>>v&1:
            edge(adj,u,v)
    for u,v in combinations(range(13),2):
        if red_b[u]>>v&1:
            edge(adj,12+u,12+v)
    for s in range(25,43):
        for a in range(4,12):
            edge(adj,s,a)
        for b in nb:
            edge(adj,s,12+b)
    if red_separator_edge:
        edge(adj,25,26)
    return packed(adj,list(range(25,43)))

def transform(obj,p,complement):
    old=int(obj['red_hex'],16)
    adj=[0]*43
    for i,(u,v) in enumerate(combinations(range(43),2)):
        if bool(old>>i&1)!=complement:
            edge(adj,p[u],p[v])
    return packed(adj,[p[v] for v in obj['separator']],'blue' if complement else 'red')

def check_controls():
    rng=random.Random(202609080328)
    routes=Counter()
    fixtures=[]
    for red in (False,True):
        original=boundary_fixture(red)
        cert=extract.extract(original)
        expected='unique_attachment_red_pair' if red else 'unique_attachment_blue_separator'
        if cert['route']!=expected:
            raise ValueError('new proof route not exercised')
        fixtures.append({'graph':original,'certificate':cert})
        for trial in range(12):
            p=list(range(43));rng.shuffle(p)
            obj=transform(original,p,bool(trial%2))
            c=extract.extract(obj)
            verify_five.check(obj,c)
            routes[c['route']]+=1
    for trial in range(72):
        total=25+trial%2
        a=2+trial%(total-3)
        adj=[0]*43
        for u,v in combinations(range(43),2):
            if u<a<=v<total:
                continue
            if rng.randrange(2):
                edge(adj,u,v)
        obj=packed(adj,list(range(total,43)))
        p=list(range(43));rng.shuffle(p)
        obj=transform(obj,p,bool(trial%2))
        c=extract.extract(obj)
        verify_five.check(obj,c)
        routes[c['route']]+=1
    comparisons=0
    for n in range(1,6):
        pairs=list(combinations(range(n),2))
        for word in range(1<<len(pairs)):
            adj=[0]*n
            for i,(u,v) in enumerate(pairs):
                if word>>i&1:
                    edge(adj,u,v)
            for color in (0,1):
                mat=adj if color else [((1<<n)-1)^(1<<v)^adj[v] for v in range(n)]
                for k in range(1,n+1):
                    expected=any(all(mat[u]>>v&1 for u,v in combinations(q,2)) for q in combinations(range(n),k))
                    found=extract.clique(mat,(1<<n)-1,k)
                    if (found is not None)!=expected:
                        raise ValueError('clique existence mismatch')
                    if found is not None and (len(found)!=k or any(not(mat[u]>>v&1) for u,v in combinations(found,2))):
                        raise ValueError('incorrect clique labels')
                    comparisons+=1
    bad=[]
    original=fixtures[0]['graph']
    for key,value in (('n',42),('separator',[25,25]),('separator',list(range(24,43))),('red_hex','f'*226),('cut_color','green'),('separator',[])):
        x=copy.deepcopy(original);x[key]=value;bad.append(x)
    # Deliberately defective K24 control, still outside the proved excluded family.
    adj=[0]*43
    for u,v in combinations(range(1,25),2):edge(adj,u,v)
    bad.append(packed(adj,list(range(25,43))))
    for x in bad:
        try:extract.extract(x)
        except ValueError:continue
        raise ValueError('invalid or unsupported extractor input accepted')
    rejected_certificates=0
    cert=fixtures[0]['certificate']
    for key,value in (('vertices',cert['vertices'][:4]),('vertices',[25]*5),('color','red'),('vertices',[25,26,27,28,43])):
        x=copy.deepcopy(cert);x[key]=value
        try:verify_five.check(original,x)
        except ValueError:rejected_certificates+=1;continue
        raise ValueError('corrupt literal certificate accepted')
    pairs=extract.cut_clauses(list(range(2)),list(range(2,25)))
    if len(pairs['at_least_one_red'])!=46 or pairs['at_least_one_red']!=pairs['at_least_one_blue']:
        raise ValueError('global cut-clause map')
    rejected_cuts=0
    for a,b in (([0],list(range(1,25))),([0,1],list(range(1,25))),([0,1],list(range(2,24)))):
        try:extract.cut_clauses(a,b)
        except ValueError:rejected_cuts+=1;continue
        raise ValueError('outside cut scope accepted')
    return {'status':'VERIFIED_PHYSICAL_SEPARATOR_CONTROLS','physical_fixtures':sum(routes.values()),'extractor_routes':dict(sorted(routes.items())),'small_graph_clique_comparisons':comparisons,'rejected_extractor_inputs':len(bad),'rejected_literal_certificates':rejected_certificates,'rejected_cut_requests':rejected_cuts,'cut_clause_minimum_width':46,'fixtures':fixtures}

if __name__=='__main__':
    print(json.dumps(check_controls(),indent=2,sort_keys=True))
