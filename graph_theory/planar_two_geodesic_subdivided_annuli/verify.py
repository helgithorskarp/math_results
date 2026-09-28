#!/usr/bin/env python3
"""Exact metric and component checks; the universal theorem has a written proof."""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent


def module(name, sibling):
    spec = importlib.util.spec_from_file_location(name, HERE.parent/sibling/'verify.py')
    answer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(answer)
    return answer


old = module('old_exchange', 'planar_two_geodesic_annular_exchange')
reroot = module('old_reroot', 'planar_two_geodesic_rerooted_attachments')
base = old.base
require = base.require


def positions(g, path):
    answer = [0]
    for a, b in zip(path, path[1:]):
        answer.append(answer[-1]+g.adj[a][b])
    return answer


def split_index(coords, cut4):
    return (max(i for i, x in enumerate(coords) if 4*x <= cut4),
            min(i for i, x in enumerate(coords) if 4*x >= cut4))


def cover_three_portal(g, left, right, dist):
    """left runs u to m; right runs v to m. Cuts are exact quarters."""
    require(left[-1] == right[-1] and set(left) & set(right) == {left[-1]}, 'two ears meet at m')
    require(all(len(g.adj[x]) == 2 for x in left[1:-1]+right[1:-1]), 'only three possible ports')
    u, m, v = left[0], left[-1], right[0]
    ca, cb = positions(g, left), positions(g, right)
    A, B = ca[-1], cb[-1]
    p, q, s = dist[u][m], dist[m][v], dist[u][v]
    z4, t4 = 2*A-p+q-s, 2*B+p-q-s
    require(0 <= z4 <= 4*A and 0 <= t4 <= 4*B, 'cuts inside ears')
    a, aa = split_index(ca, z4)
    b, bb = split_index(cb, t4)
    outside = tuple(reversed(left[:a+1])) + base_path(g, u, v, dist)[1:] + tuple(right[1:b+1])
    inside = tuple(left[aa:]) + tuple(reversed(right[bb:]))[1:]
    for path in (outside, inside):
        g.check_path(path, dist)
    require(set(left+right) <= set(outside+inside), 'entire three-portal path covered')
    return outside, inside


def base_path(g, a, b, d):
    return g.shortest(a, b, d)


def fixture(k, scale, lengths, sites=(), m=3, pocket_length=None, extra=False):
    require(k >= 5 and len(lengths) == k, 'annular order')
    g, _ = base.annulus(k)
    for row in g.adj:
        for v in row: row[v] *= scale
    arcs = []
    for i, sizes in enumerate(lengths):
        require(sizes and all(x > 0 for x in sizes), 'positive rim lengths')
        require(sum(sizes) >= scale, 'rim total lower bound')
        require(len(sizes) == 1 or sum(sizes) >= 2*scale, 'subdivided rim total lower bound')
        u, v = 1+k+i, 1+k+(i+1) % k
        interior = sorted(reroot.subdivide(g, u, v, sizes))
        arcs.append(tuple([u]+interior+[v]))
    core = set(range(len(g.adj)))
    d0 = g.distances()
    for i in sites:
        if m:
            g.attach(m, (0, 1+i, 1+(i+1) % k), long_edges=pocket_length or scale)
        else:
            require(scale == 1, 'octahedral fixture scale')
            old.octahedron(g, k, i)
    if extra:
        require(scale <= 2, 'ear metric preserves isometry')
        for i in range(k):
            old.ears(g, k, i, 3)
            old.ears(g, k, i, 4)
        g.attach(2, (0, 1), long_edges=pocket_length or scale)
    g.sphere()
    d = g.distances()
    require(all(d[u][v] == d0[u][v] for u in core for v in core), 'core isometry')
    return g, arcs, core, d


def system(g, original, core, shift=0, reverse=False):
    k = len(original)
    A = [1+(shift+(-i if reverse else i)) % k for i in range(k)]
    C = [1+k+(shift+(1-i if reverse else i)) % k for i in range(k)]
    arcs = []
    for i in range(k):
        chain = original[(shift-i if reverse else shift+i) % k]
        arcs.append(tuple(reversed(chain)) if reverse else chain)
        require(arcs[-1][0] == C[i] and arcs[-1][-1] == C[(i+1) % k], 'oriented arc')
    P = (0, A[0], C[0])
    alpha = [set()]+[{A[i]} for i in range(1,k)]
    gamma = [set()]+[{C[i]} for i in range(1,k)]
    tau = [set(path[1:-1]) for path in arcs]
    kappa = [set() for _ in range(k)]
    discarded = set()
    outside = g.components(core)
    for K in outside:
        N = set().union(*(set(g.adj[v]) for v in K)) & core
        Y = N & set(A)
        require(N <= Y | {0} and len(Y) <= 2, 'root-clique boundary')
        if len(Y) == 2:
            at = [i for i in range(k) if Y == {A[i],A[(i+1) % k]}]
            require(len(at) == 1, 'one outer sector')
            kappa[at[0]] |= K
        elif Y and A[0] not in Y:
            alpha[A.index(next(iter(Y)))] |= K
        else:
            discarded |= K
    mass_set = set(range(len(g.adj)))-set(P)-discarded
    groups = alpha+gamma+tau+kappa
    require(set().union(*groups) == mass_set and sum(map(len,groups)) == len(mass_set), 'mass partition')

    def atom(values, i): return values[i % k]
    def bounds(i):
        left = set().union(*(alpha[j] | gamma[j] | tau[j] | kappa[j] for j in range(i)))
        return left, mass_set-left-atom(alpha,i)-atom(gamma,i)
    def prepare(Q, sides):
        pieces = g.components(set(P) | set(Q))
        for K in pieces:
            if K & core:
                require(any(K <= side for side in sides), 'exact component containment')
            else:
                require(K in outside, 'one whole detached attachment')
        return dict(path=Q,sides=sides,pieces=pieces)

    seq, middles, exchanges, patches = [], [], [], []
    for i in range(k):
        L, R = bounds(i)
        LV, RV = L | gamma[i] | tau[i], R-atom(gamma,i+1)-tau[i]
        seq.append(prepare((0,A[i],C[i]), [L,R]))
        seq.append(prepare((0,A[i],C[(i+1)%k]), [LV,RV]))
        coords = positions(g,arcs[i])
        a, b = split_index(coords,2*coords[-1])
        removed_left, removed_right = set(arcs[i][1:a+1]),set(arcs[i][b:-1])
        mu = prepare(tuple([0,A[i]])+arcs[i][:a+1], [L,R-removed_left])
        mv = prepare(tuple([0,A[i]])+tuple(reversed(arcs[i][b:])),
                     [L | gamma[i] | (tau[i]-removed_right),RV])
        require(not mu['sides'][1] & mv['sides'][0], 'midpoint heavy sides disjoint')
        require(mu['sides'][1] | mv['sides'][0] <= mass_set, 'midpoint sides in represented mass')
        middles.append((mu,mv))
        LN, RN = bounds(i+1)
        patch = tau[i] | {C[(i+1)%k]} | atom(tau,i+1)
        patches.append(patch)
        if tau[i] or atom(tau,i+1):
            Q = (C[i],A[i],A[(i+1)%k],C[(i+2)%k])
            exchanges.append([prepare(Q,[LV,RN,patch])])
        else:
            plus = prepare((A[i],A[(i+1)%k],C[(i+2)%k]),[LV | atom(gamma,i+1),RN])
            minus = prepare((A[(i+1)%k],A[i],C[i]),[LV,RN | atom(gamma,i+1)])
            coeff = Counter(x for side in [RV,LN,plus['sides'][0],minus['sides'][1]] for x in side)
            require(all(coeff[x] == 2-int(x in alpha[i] | atom(alpha,i+1)) for x in mass_set), 'unsubdivided exchange identity')
            exchanges.append([plus,minus])
    LK,RK = bounds(k)
    seq.append(prepare(P,[LK,RK]))
    return dict(P=P,sequence=seq,middles=middles,exchanges=exchanges,patches=patches,
                outside=outside,discarded=discarded,mass_set=mass_set)


def finish(g, sys, w, d, covers, result, allow_heavy):
    W=sum(w)
    def mass(K): return sum(w[v] for v in K)
    heavy = [K for K in sys['outside'] if 2*mass(K)>W]
    if heavy:
        if allow_heavy: old.heavy(g,d,w,result)
        return
    for patch, paths in zip(sys['patches'],covers):
        if 2*mass(patch)>W:
            removed=set().union(*map(set,paths))
            require(patch <= removed, 'whole heavy patch deleted')
            require(all(2*mass(K)<=W for K in g.components(removed)), 'heavy replacement restores P safely')
            result['heavy_patch_checks']+=1
            return
    def balanced(cut): return all(2*mass(K)<=W for K in cut['sides'])
    chosen=None
    for j,cut in enumerate(sys['sequence']):
        if balanced(cut):
            chosen=cut; result['spoke_choices']+=1; break
        if j and 2*mass(sys['sequence'][j-1]['sides'][1])>W and 2*mass(cut['sides'][0])>W:
            if j%2:
                choices=sys['middles'][j//2]; label='midpoint_choices'
            else:
                choices=sys['exchanges'][j//2-1]
                label='outer_detours' if len(choices)==1 else 'old_exchange_choices'
            chosen=next((q for q in choices if balanced(q)),None)
            require(chosen is not None,'local transition has a valid completion')
            result[label]+=1
            break
    require(chosen is not None,'sweep terminates')
    require(all(2*mass(K)<=W for K in chosen['pieces']),'original full-graph half balance')
    result['light_patch_checks']+=1


def main():
    result=dict(portal_cover_checks=0,portal_models=0,fixtures=0,systems=0,
                component_cuts=0,ambient_path_checks=0,spoke_choices=0,
                midpoint_choices=0,outer_detours=0,old_exchange_choices=0,
                heavy_patch_checks=0,heavy_checks=0,light_patch_checks=0,
                local_decompositions=0,rejected_short_subdivision=0)
    rng=random.Random(2026092812)
    # General metric cover lemma: three terminal edges plus two arbitrary ears.
    for trial in range(240):
        g=base.Graph(3,[(0,1,rng.randrange(1,20)),(1,2,rng.randrange(1,20)),(0,2,rng.randrange(1,20))],[])
        paths=[]
        for u in (0,2):
            chain=[u]
            for _ in range(rng.randrange(1,8)):
                chain.append(len(g.adj));g.adj.append({})
            chain.append(1)
            for a,b in zip(chain,chain[1:]):g.edge(a,b,rng.randrange(1,10))
            paths.append(tuple(chain))
        cover_three_portal(g,*paths,g.distances())
        result['portal_models']+=1
    specs=[(5,1,[[1]*x for x in [1,2,3,4,6]],range(5),3,None,False),
           (6,1,[[1,1]]*6,[0,2,4],3,None,False),
           (7,2,[[2],[1,1,1,1],[2],[1,1,4],[2],[3,2],[2]],range(7),3,1,True),
           (9,4,[[1,3,2,5] if i%2 else [4] for i in range(9)],range(9),2,2,False),
           (5,1,[[1]*x for x in [2,7,2,7,2]],range(5),0,None,False),
           (8,1,[[1]*x for x in [1,1,7,1,1,1,4,1]],[],3,None,False)]
    for k,scale,lengths,sites,m,pl,extra in specs:
        g,arcs,core,d=fixture(k,scale,lengths,sites,m,pl,extra)
        if m:
            for piece in g.pieces:
                g.check_local_decomposition(piece);result['local_decompositions']+=1
        result['fixtures']+=1
        weights=list(base.masses(g,rng))
        # Explicit mass profiles force rim-heavy and sector-heavy decisions.
        for i in range(k):
            w=[0]*len(g.adj)
            patch=set(arcs[i][1:]) | set(arcs[(i+1)%k][1:-1])
            for v in patch:w[v]=1
            weights.append(w)
        for shift in range(k):
            for reverse in (False,True):
                sys=system(g,arcs,core,shift,reverse)
                paths=[q for pair in sys['middles']+sys['exchanges'] for q in pair]+sys['sequence']
                for cut in paths:g.check_path(cut['path'],d)
                result['ambient_path_checks']+=len(paths)
                result['component_cuts']+=len(paths)
                result['systems']+=1
                ordered=[]
                for i in range(k):
                    j=(shift-i if reverse else shift+i)%k
                    chain=tuple(reversed(arcs[j])) if reverse else arcs[j]
                    ordered.append(chain)
                covers=[cover_three_portal(g,ordered[i],tuple(reversed(ordered[(i+1)%k])),d) for i in range(k)]
                result['portal_cover_checks']+=k
                for w in weights:finish(g,sys,w,d,covers,result,bool(m))
    try:fixture(5,2,[[1,2]]+[[2]]*4)
    except AssertionError as error:
        require(str(error)=='subdivided rim total lower bound','expected rejection')
        result['rejected_short_subdivision']=1
    require(result['rejected_short_subdivision']==1,'short subdivision rejected')
    require(all(result[x]>0 for x in ['midpoint_choices','outer_detours','old_exchange_choices','heavy_patch_checks','heavy_checks']), 'all proof branches exercised')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    answer=main()
    if args.check:require(answer==json.loads((HERE/'expected.json').read_text()),'expected evidence')
    print(json.dumps(answer,indent=2,sort_keys=True))
