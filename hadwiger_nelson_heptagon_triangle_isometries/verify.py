#!/usr/bin/env python3
"""Independent exact audit in Q(zeta_7, omega_6), without modular filtering.

No producer or solver imports. Coordinates are reconstructed with geometric
series inverses and the C3/reflection generators of each triangle's S3.
"""
import argparse
from itertools import combinations,permutations,product
import json
from math import comb
from pathlib import Path

ZERO=(0,)*12;ONE=(1,)+(0,)*11
Z=(0,1)+(0,)*10;W=(0,)*6+(1,)+(0,)*5
def require(ok,message):
    if not ok:raise ValueError(message)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def times_int(a,c):return tuple(c*x for x in a)
def divide(a,d):
    require(all(x%d==0 for x in a),'nonintegral tensor coordinates')
    return tuple(x//d for x in a)
def multiply(a,b):
    # First reduce z^7=1 and w^2=w-1 in a 7 by 2 array; then eliminate z^6.
    v=[0]*14
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            if not y:continue
            k=(i%6+j%6)%7;degree=i//6+j//6;c=x*y
            if degree==2:v[k]-=c;v[k+7]+=c
            else:v[k+7*degree]+=c
    return tuple(v[7*j+i]-v[7*j+6] for j in range(2) for i in range(6))
def power(a,n):
    out=ONE
    for _ in range(n):out=multiply(out,a)
    return out
ZPOW=[power(Z,i) for i in range(7)]
CBASIS=[multiply(ZPOW[-i%7],ONE if j==0 else minus(ONE,W)) for j in range(2) for i in range(6)]
def conjugate(a):
    out=ZERO
    for c,v in zip(a,CBASIS):out=plus(out,times_int(v,c))
    return out
def norm(a):return multiply(a,conjugate(a))
T=multiply(ZPOW[6],W)
TPOW=[power(T,i) for i in range(12)]
def convert(a):
    out=ZERO
    for c,v in zip(a,TPOW):out=plus(out,times_int(v,c))
    return out

def reconstruct_seed():
    def inv7(x):
        # x is a primitive seventh root. (x-x^-1)*x*sum k*x^(2k)=7.
        out=ZERO
        for k in range(7):out=plus(out,times_int(power(x,2*k),k))
        ans=multiply(x,out)
        require(multiply(minus(x,conjugate(x)),ans)==times_int(ONE,7),'geometric-series inverse')
        return ans
    P=inv7(ZPOW[4])
    Q=times_int(multiply(conjugate(W),inv7(Z)),-1)
    R=times_int(multiply(W,inv7(ZPOW[2])),-1)
    return [multiply(a,ZPOW[j]) for a in [P,Q,R] for j in range(7)]

def reconstruct_copies(H):
    result={}
    for j in range(7):
        tri=(j,j+7,j+14);a,b,c=[H[i] for i in tri]
        candidates=[minus(W,ONE),times_int(W,-1)]
        r=next(v for v in candidates if plus(b,multiply(v,minus(b,a)))==c)
        require(norm(r)==ONE and power(r,3)==ONE,'unit order-three rotation')
        def rotate(x):return plus(b,multiply(r,minus(x,a)))
        require(rotate(c)==a,'triangle rotation cycle')
        uv=multiply(minus(b,a),minus(c,a))
        require(norm(uv)==times_int(ONE,49**2),'unit reflection coefficient')
        def reflect(x):return plus(a,divide(multiply(uv,conjugate(minus(x,a))),49))
        require(reflect(a)==a and reflect(b)==c and reflect(c)==b,'triangle reflection')
        perms=set()
        for flip in [False,True]:
            for k in range(3):
                cp=[reflect(x) if flip else x for x in H]
                for _ in range(k):cp=[rotate(x) for x in cp]
                perm=tuple(H.index(cp[i]) for i in tri)
                perms.add(perm)
                if not flip and k==0:require(cp==H,'identity copy');continue
                result[j,perm]=cp
        require(perms==set(permutations(tri)),'complete triangle isometry coverage')
    return result

def abstract_seed_edges():
    E=set()
    for j in range(7):
        for ring,step in enumerate([1,2,3]):
            E.add(tuple(sorted((7*ring+j,7*ring+(j+step)%7))))
        E.update(combinations((j,j+7,j+14),2))
    return E

def three_colour_census(E):
    # Any three-colouring can be renamed to colour triangle zero 0,1,2.
    choices=list(permutations(range(3)));w=[-1]*21
    w[0],w[7],w[14]=0,1,2;attempts=valid=0
    for states in product(choices,repeat=6):
        for j,state in enumerate(states,1):w[j],w[j+7],w[j+14]=state
        attempts+=1
        valid+=all(w[a]!=w[b] for a,b in E)
    return attempts,valid

def audit(g,certificate):
    require(type(certificate) is dict and set(certificate)=={'version','seed_colouring'},'certificate shape')
    require(type(certificate['version']) is int and certificate['version']==1,'certificate version')
    word=certificate['seed_colouring']
    require(type(word) is list and len(word)==21 and all(type(c) is int and 0<=c<4 for c in word),'colouring shape')
    H=reconstruct_seed();E0=abstract_seed_edges()
    require(all(word[a]!=word[b] for a,b in E0),'seed colouring')
    exactE0={(a,b) for a,b in combinations(range(21),2) if norm(minus(H[a],H[b]))==times_int(ONE,49)}
    require(exactE0==E0 and len(E0)==42,'exact seed graph')
    attempts,valid=three_colour_census(sorted(E0));require(valid==0,'seed three-colour obstruction')
    require(type(g) is dict and set(g)=={'denominator','coordinates','edges','seed_indices','copies','maps','filter'},'producer shape')
    require(type(g['denominator']) is int and g['denominator']==7,'denominator')
    require(type(g['coordinates']) is list and len(g['coordinates'])==651,'complete support size')
    for z in g['coordinates']:require(type(z) is list and len(z)==12 and all(type(c) is int for c in z),'coordinate shape')
    V=[convert(a) for a in g['coordinates']];require(len(set(V))==651,'distinct producer coordinates')
    index={z:i for i,z in enumerate(V)}
    labels=g['seed_indices']
    require(type(labels) is list and len(labels)==21 and all(type(x) is int and 0<=x<651 for x in labels),'seed labels')
    require([V[x] for x in labels]==H,'seed coordinate comparison')
    copies=reconstruct_copies(H);require(len(copies)==35,'nonidentity copy count')
    allpoints=set(H).union(*(set(cp) for cp in copies.values()))
    require(allpoints==set(V),'complete support comparison')
    require(len(g['copies'])==35 and len(g['maps'])==35,'complete producer copy count')
    observed=set();private=set();expected_edges={tuple(sorted((index[H[a]],index[H[b]]))) for a,b in E0}
    colouring={index[z]:word[i] for i,z in enumerate(H)}
    base=set(H);private_counts=[];copy_edge_occurrences=0
    for info,labels in zip(g['maps'],g['copies']):
        require(type(info) is dict and set(info)=={'triangle','permutation','reflection'},'isometry label shape')
        j,perm=info['triangle'],info['permutation']
        require(type(j) is int and 0<=j<7 and type(perm) is list and len(perm)==3 and all(type(x) is int for x in perm),'isometry label range')
        require(type(info['reflection']) is bool,'orientation type')
        tri=(j,j+7,j+14);key=j,tuple(perm)
        require(key in copies and key not in observed,'complete unique isometry labels');observed.add(key)
        cp=copies[key]
        require(type(labels) is list and len(labels)==21 and all(type(x) is int and 0<=x<651 for x in labels),'copy labels')
        require([V[x] for x in labels]==cp,'copy coordinate comparison')
        invs=sum(perm[a]>perm[b] for a,b in combinations(range(3),2))
        require(info['reflection']==bool(invs%2),'orientation parity')
        C=set(cp);require(len(C)==21,'copy injective')
        require(C&base=={H[i] for i in tri},'copy-base exact intersection')
        P=C-base;require(len(P)==18 and not P&private,'private vertices disjoint');private|=P;private_counts.append(len(P))
        # Extend the base colouring by the unique four-colour permutation
        # agreeing on the shared triangle; its fourth colour is fixed.
        sigma={word[a]:word[b] for a,b in zip(tri,perm)}
        remaining=set(range(4))-set(sigma);require(len(remaining)==1,'triangle uses three colours')
        last=remaining.pop();sigma[last]=last
        require(set(sigma.values())==set(range(4)),'colour permutation')
        for i,z in enumerate(cp):
            v=index[z];colour=sigma[word[i]]
            require(v not in colouring or colouring[v]==colour,'colour agreement')
            colouring[v]=colour
        for a,b in E0:expected_edges.add(tuple(sorted((labels[a],labels[b]))));copy_edge_occurrences+=1
    require(observed==set(copies),'complete isometry set comparison')
    require(type(g['edges']) is list and all(type(e) is list and len(e)==2 and all(type(x) is int for x in e) and 0<=e[0]<e[1]<651 for e in g['edges']),'edge shape')
    require(g['edges']==[list(e) for e in sorted(set(map(tuple,g['edges'])))],'canonical edges')
    exact_edges=set();conjugates=[conjugate(z) for z in V];pairs=0
    for a,b in combinations(range(len(V)),2):
        # Full characteristic-zero computation on every pair, no filter.
        unit=multiply(minus(V[a],V[b]),minus(conjugates[a],conjugates[b]))==times_int(ONE,49)
        if unit:exact_edges.add((a,b))
        pairs+=1
    require(exact_edges==set(map(tuple,g['edges'])),'full edge comparison')
    require(exact_edges==expected_edges,'no extra unit edges between copies')
    require(all(colouring[a]!=colouring[b] for a,b in exact_edges),'full extended colouring')
    return {'verified':True,'seed_vertices':21,'seed_edges':42,'seed_chromatic_number':4,
            'normalized_three_colour_assignments':attempts,'valid_three_colourings':valid,
            'nonidentity_copies':35,'private_vertices_per_copy':18,'vertices':651,'edges':len(exact_edges),
            'all_pair_norm_checks':pairs,'maximum_target_copies':27,'maximum_target_vertices':507,
            'maximum_target_edges':1095,'target_sized_family_members':sum(comb(35,k) for k in range(28)),
            'every_base_four_colouring_extends':True,'all_family_graphs_chromatic_number':4,'record_improvement':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args()
    g=json.loads((args.work/'graph.json').read_text());c=json.loads((Path(__file__).resolve().parent/'certificate.json').read_text())
    print(json.dumps(audit(g,c),sort_keys=True))
if __name__=='__main__':main()
