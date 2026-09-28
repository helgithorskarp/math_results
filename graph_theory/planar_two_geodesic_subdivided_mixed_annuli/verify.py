#!/usr/bin/env python3
"""Exact regressions for the written subdivided mixed-annulus theorem."""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('quad',HERE.parent/'planar_two_geodesic_quadrilateral_annuli/verify.py')
quad=importlib.util.module_from_spec(spec);spec.loader.exec_module(quad)
fan,base,require=quad.fan,quad.base,quad.require

def validate(word):
    require(word and set(word)<=set('ACD'),'word')
    k,m=sum(x in 'AD' for x in word),sum(x in 'CD' for x in word)
    require(k>=3 and m>=3,'cycle orders')
    require(quad.maximum_run(word,'A')<=k-2 and quad.maximum_run(word,'C')<=m-2,'wrap bounds')
    return k,m

def bad_positions(word):
    return [s for s,x in enumerate(word) if x=='A' and word[s-1]=='D' and word[(s+1)%len(word)]=='D']

def core_graph(word, lengths, scale=1):
    k, m = validate(word)
    require(len(lengths) == m and all(n >= 1 for n in lengths), 'unit arc lengths')
    A, C = list(range(1, k+1)), list(range(k+1, k+m+1))
    edges, faces = {}, []
    def edge(a, b): edges[tuple(sorted((a, b)))] = scale
    for i in range(k):
        edge(0, A[i]); edge(A[i], A[(i+1) % k])
        faces.append((0, A[i], A[(i+1) % k]))
    for j in range(m): edge(C[j], C[(j+1) % m])
    i = j = 0
    states = []
    for letter in word:
        a, c = A[i % k], C[j % m]
        states.append((a, c)); edge(a, c)
        if letter == 'A':
            faces.append((a, c, A[(i+1) % k])); i += 1
        elif letter == 'C':
            faces.append((a, c, C[(j+1) % m])); j += 1
        else:
            faces.append((a, c, C[(j+1) % m], A[(i+1) % k])); i += 1; j += 1
    require(len(set(states)) == len(word), 'distinct cross edges')
    faces.append(tuple(reversed(C)))
    g = base.Graph(1+k+m, [(a, b, v) for (a, b), v in edges.items()], faces)
    arcs = []
    for j, size in enumerate(lengths):
        u, v = C[j], C[(j+1) % m]
        inside = sorted(fan.previous.reroot.subdivide(g, u, v, [scale]*size))
        arcs.append(tuple([u]+inside+[v]))
    g.sphere()
    return g, A, C, arcs


def outer_region(g,A,C,core,a):
    neighbors=set(g.adj[a])&set(C)
    require(len(neighbors)==1,'unique inner neighbor')
    c=next(iter(neighbors));i=A.index(a)
    boundary={0,c,A[i-1],A[(i+1)%len(A)]};S={a}
    for K in g.components(core):
        N=set().union(*(set(g.adj[v]) for v in K))&core
        if a in N:S|=K
    require(S in g.components(boundary),'whole single-outer-vertex region')
    return dict(internal=S,center=a)


def system(g, original_A, original_C, original_arcs, original_word, core, dist, result, shift=0):
    word = original_word[shift:]+original_word[:shift]
    require(not (word[0] == word[-1] == 'A'), 'seam does not split an A-run')
    ai = sum(x in 'AD' for x in original_word[:shift])
    cj = sum(x in 'CD' for x in original_word[:shift])
    A = original_A[ai:]+original_A[:ai]
    C = original_C[cj:]+original_C[:cj]
    arcs = original_arcs[cj:]+original_arcs[:cj]
    k, m = len(A), len(C)
    has_bad=bool(bad_positions(word))
    require(not has_bad or 0 in bad_positions(word),'DAD anchor')
    stars=[outer_region(g,A,C,core,a) for a in A if len(set(g.adj[a])&set(C))==1]
    star_by_center={S['center']:S['internal'] for S in stars}
    P = (0, A[0], C[0])
    alpha = [set()]+[{a} for a in A[1:]]
    gamma = [set()]+[{c} for c in C[1:]]
    tau = [set(arc[1:-1]) for arc in arcs]
    kappa = [set() for _ in A]
    discarded = set()
    outside = g.components(core)
    for K in outside:
        N = set().union(*(set(g.adj[v]) for v in K)) & core
        Y = N & set(A)
        require(N <= Y | {0} and len(Y) <= 2, 'root-clique attachment')
        if len(Y) == 2:
            sites = [i for i in range(k) if Y == {A[i], A[(i+1) % k]}]
            require(len(sites) == 1, 'consecutive active boundary')
            kappa[sites[0]] |= K
        elif Y and A[0] not in Y: alpha[A.index(next(iter(Y)))] |= K
        else: discarded |= K
    mass_set = set(range(len(g.adj)))-set(P)-discarded
    groups = alpha+gamma+tau+kappa
    require(set().union(*groups) == mass_set and sum(map(len, groups)) == len(mass_set), 'mass partition')
    def atom(values, i): return values[i % len(values)]
    def bounds(i, j):
        L = set().union(*(alpha[x] | kappa[x] for x in range(i)),
                        *(gamma[x] | tau[x] for x in range(j)))
        return L, mass_set-L-atom(alpha, i)-atom(gamma, j)
    cuts = []
    def prepare_pair(paths,sides,flavor="ordinary"):
        for path in paths:g.check_path(path,dist)
        removed=set().union(*map(set,paths))
        require(set(P)<=removed,'original spoke vertices retained')
        parts=g.components(removed)
        for K in parts:
            if K & core: require(any(K <= side for side in sides), 'exact component containment')
            else: require(K in outside, 'whole detached attachment')
        cut = dict(paths=paths, sides=sides, parts=parts,flavor=flavor)
        cuts.append(cut)
        return cut
    def prepare(path,sides):return prepare_pair([P,path],sides)
    sequence, transitions, fans = [], [], []
    i = j = pos = 0
    sequence.append(prepare(P, bounds(0, 0)))
    while pos < len(word):
        letter = word[pos]
        L, R = bounds(i, j)
        if letter == 'A':
            d = 1
            while pos+d < len(word) and word[pos+d] == 'A': d += 1
            l, t = i, i+d
            LN, RN = bounds(t, j)
            if d >= 2:
                F = set().union(*(alpha[s] for s in range(l+1, t)), *(kappa[s] for s in range(l, t)))
                boundary = {0, C[j % m], A[l % k], A[t % k]}
                require(F in g.components(boundary), 'whole long fan component')
                fans.append(fan.fan_decomposition(g, A, C[j % m], l, t, F, dist))
                choices = [prepare((A[l % k], C[j % m], A[t % k]), [L, RN, F])]
                label = 'long_fan_choices'
            elif C[j % m] == C[0]:
                choices = [prepare((A[l % k], A[t % k]), [L, RN])]
                label = 'seam_choices'
            elif word[(pos+1) % len(word)] == 'C':
                arc = arcs[j % m]; n = len(arc)-1
                p, q = n//2, (n+2)//2
                prefix = set(arc[1:p+1])
                root = prepare((0, A[l % k])+arc[:p+1], [L, R-prefix])
                detour = prepare((A[l % k], A[t % k])+tuple(reversed(arc[q:])),
                                 [L | atom(gamma, j) | set(arc[1:q]), RN])
                require(not root['sides'][1] & detour['sides'][0], 'forward heavy sides disjoint')
                require(root['sides'][1] | detour['sides'][0] <= mass_set, 'forward accounted mass')
                choices = [root, detour]; label = 'forward_A_choices'
                result['one_sided_identities'] += 1
            elif word[pos-1] == 'C':
                arc = arcs[(j-1) % m]; n = len(arc)-1
                p, q = (n+1)//2, (n-1)//2
                suffix = set(arc[p:-1])
                root = prepare((0, A[t % k])+tuple(reversed(arc[p:])), [LN-suffix, RN])
                detour = prepare((A[t % k], A[l % k])+arc[:q+1],
                                 [L, RN | atom(gamma, j) | set(arc[q+1:-1])])
                require(not root['sides'][0] & detour['sides'][1], 'backward heavy sides disjoint')
                require(root['sides'][0] | detour['sides'][1] <= mass_set, 'backward accounted mass')
                choices = [root, detour]; label = 'backward_A_choices'
                result['one_sided_identities'] += 1
            else:
                require(pos in bad_positions(word),'only DAD remains')
                if j==1:
                    arc=arcs[0];n=len(arc)-1
                    if n==1:
                        choices=[prepare((A[1],A[l],A[t]),[mass_set-LN])]
                        label='next_unsubdivided_choices'
                        result['next_unsubdivided_geometries']+=1
                    else:
                        p,q=(n+1)//2,(n+3)//2
                        U=(A[0],0,A[t])+tuple(reversed(arc[q:]))
                        V=(A[1],)+arc[:p+1]
                        require(set(arc)<=set(U)|set(V),'whole adjacent arc covered')
                        S=star_by_center[A[l]]
                        require(R&S==kappa[l],'old-heavy overlap is the new sector')
                        require(mass_set-(R|S)==kappa[0]|alpha[1]|tau[0]|gamma[1],
                                'complement contains the anchor sector')
                        choices=[prepare_pair([U,V],[S,RN],'arc_pair')]
                        result['next_neighbor_mass_identities']+=1
                        label='repartition_choices'
                        result['repartition_geometries']+=1
                elif j==m-1 and len(arcs[-1])==2:
                    choices=[prepare((A[l],A[t%k],A[0]),[mass_set-R])]
                    label='previous_unsubdivided_choices'
                    result['previous_unsubdivided_geometries']+=1
                else:
                    choices=[prepare((A[1],0,A[t%k],C[j%m]),[LN-kappa[0],RN])]
                    label='root_sector_choices'
                    result['root_sector_geometries']+=1
            for _ in range(d):
                i += 1
                sequence.append(prepare((0, A[i % k], C[j % m]), bounds(i, j)))
                transitions.append((label, choices))
            pos += d
        elif letter == 'C':
            LN, RN = bounds(i, j+1)
            arc = arcs[j]; n = len(arc)-1
            p, q = n//2, (n+1)//2
            left_removed, right_removed = set(arc[1:p+1]), set(arc[q:-1])
            old = prepare((0, A[i % k])+arc[:p+1], [L, R-left_removed])
            new = prepare((0, A[i % k])+tuple(reversed(arc[q:])),
                          [L | atom(gamma, j) | (tau[j]-right_removed), RN])
            require(not old['sides'][1] & new['sides'][0], 'C-step disjoint heavy supports')
            j += 1; pos += 1
            sequence.append(prepare((0, A[i % k], C[j % m]), (LN, RN)))
            transitions.append(('C_choices', [old, new]))
        else:
            LN, RN = bounds(i+1, j+1)
            arc = arcs[j]; n = len(arc)-1
            p, q, u, v = n//2, (n+1)//2, (n-1)//2, (n+2)//2
            old = prepare((0, A[i % k])+arc[:p+1], [L, R-set(arc[1:p+1])])
            new = prepare((0, A[(i+1) % k])+tuple(reversed(arc[q:])), [LN-set(arc[q:-1]), RN])
            plus = prepare((A[i % k], A[(i+1) % k])+tuple(reversed(arc[v:])),
                           [L | atom(gamma, j) | set(arc[1:v]), RN])
            minus = prepare((A[(i+1) % k], A[i % k])+arc[:u+1],
                            [L, RN | atom(gamma, j+1) | set(arc[u+1:-1])])
            count = Counter(x for side in [old['sides'][1], new['sides'][0], plus['sides'][0], minus['sides'][1]] for x in side)
            require(all(count[x] == 2-int(x in atom(alpha, i) | atom(alpha, i+1)) for x in mass_set), 'quadrilateral four-side identity')
            result['quadrilateral_identities'] += 1
            i += 1; j += 1; pos += 1
            sequence.append(prepare((0, A[i % k], C[j % m]), (LN, RN)))
            transitions.append(('D_choices', [old, new, plus, minus]))
    require(i == k and j == m, 'full word swept')
    return dict(P=P, sequence=sequence, transitions=transitions, fans=fans,
                patches=[], covers=[], outside=outside, cuts=cuts, discarded=discarded,
                mass_set=mass_set,stars=stars,anchor_sector=kappa[0] if has_bad else set())


def quantitative(g,sys,w,result):
    def mass(K):return sum(w[v] for v in K)
    M=mass(sys['mass_set'])
    require(M==sum(w)-mass(sys['P'])-mass(sys['discarded']),'represented mass')
    bound2=max(M,2*max(map(mass,sys['outside']),default=0),
               2*max((mass(F['internal']) for F in sys['fans']),default=0))
    def valid(parts):return all(2*mass(K)<=bound2 for K in parts)
    chosen=None
    for j,cut in enumerate(sys['sequence']):
        if valid(cut['sides']):chosen=cut;break
        if j and 2*mass(sys['sequence'][j-1]['sides'][1])>bound2 and 2*mass(cut['sides'][0])>bound2:
            label,options=sys['transitions'][j-1]
            chosen=next((cut for cut in options if valid(cut['sides'])),None)
            require(chosen is not None,'quantitative transition')
            result['quant_'+label]+=1
            if chosen['flavor']!='ordinary':result['quant_'+chosen['flavor']]+=1
            break
    require(chosen is not None and valid(chosen['parts']),'quantitative original components')
    result['quantitative_checks']+=1
    result['sharper_than_half']+=int(bound2<sum(w))

def finish(g,sys,w,dist,result):
    # The earlier centroid reductions for heavy K and long F are unchanged.
    before=result['repartition_choices']
    fan.finish(g,sys,w,dist,result)
    if result['repartition_choices']>before:
        for j,cut in enumerate(sys['sequence']):
            if j and 2*sum(w[v] for v in sys['sequence'][j-1]['sides'][1])>sum(w) and 2*sum(w[v] for v in cut['sides'][0])>sum(w):
                label,options=sys['transitions'][j-1]
                require(label=='repartition_choices','identified repartition transition')
                chosen=next(q for q in options if all(2*sum(w[v] for v in S)<=sum(w) for S in q['sides']))
                result[chosen['flavor']+'_choices']+=1
                break


def main():
    result=Counter()
    rng=random.Random(2026092816)
    words=['AD'*5,'AD'*3,'AD'*4,'ADADD','ADCD','ADACDADCCD','ADCADADC',
           'AAADCCAACDDAACCCD','AC'*3,'AACC'*3,'AADADAAADAD','D'*3]
    for index,word in enumerate(words):
        k,m=validate(word);scale=2 if index%3==1 else 1
        lengths=[1+(j+index)%6 for j in range(m)]
        g,A,C,arcs=core_graph(word,lengths,scale);core=set(range(len(g.adj)));original=g.distances()
        for i in range(k):
            if i%2==0:g.attach(3,(0,A[i],A[(i+1)%k]),long_edges=1)
            fan.previous.old.ears(g,k,i,3);fan.previous.old.ears(g,k,i,4)
        g.attach(2,(0,A[1]),long_edges=1);g.sphere();dist=g.distances()
        require(all(dist[a][b]==original[a][b] for a in core for b in core),'core isometry')
        for piece in g.pieces:g.check_local_decomposition(piece);result['local_decompositions']+=1
        anchors=bad_positions(word) or [next(s for s in range(len(word)) if not(word[s]==word[s-1]=='A'))]
        systems=[system(g,A,C,arcs,word,core,dist,result,s) for s in anchors]
        profiles=list(base.masses(g,rng))
        for arc in arcs:profiles.append([int(v in arc[1:-1]) for v in range(len(g.adj))])
        for S in systems[0]['stars']+systems[0]['fans']:
            profiles.append([int(v in S['internal']) for v in range(len(g.adj))])
        for w in profiles:
            maximum=max(sum(w[v] for v in sys['anchor_sector']) for sys in systems)
            for sys in systems:
                if sum(w[v] for v in sys['anchor_sector'])==maximum:
                    quantitative(g,sys,w,result);finish(g,sys,w,dist,result)
        result['fixtures']+=1;result['systems']+=len(systems)
        result['component_cuts']+=sum(len(sys['cuts']) for sys in systems)
        result['outer_regions']+=sum(len(sys['stars']) for sys in systems)
        result['fan_decompositions']+=sum(len(sys['fans']) for sys in systems)
    for trial in range(60):
        while True:
            word=''.join(rng.choice('ACD') for _ in range(rng.randrange(5,25)))
            try:k,m=validate(word)
            except AssertionError:continue
            break
        g,A,C,arcs=core_graph(word,[rng.randrange(1,10) for _ in range(m)])
        anchor=(bad_positions(word) or [next(s for s in range(len(word)) if not(word[s]==word[s-1]=='A'))])[0]
        sys=system(g,A,C,arcs,word,set(range(len(g.adj))),g.distances(),result,anchor)
        result['component_cuts']+=len(sys['cuts']);result['systems']+=1
    result['additional_core_models']=60
    require(all(result[k]>0 for k in ['repartition_choices','repartition_geometries','root_sector_choices','arc_pair_choices','next_neighbor_mass_identities','next_unsubdivided_geometries','previous_unsubdivided_geometries']),'new cases exercised')
    return dict(sorted(result.items()))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected exact counts')
    print(json.dumps(answer,indent=2))
