#!/usr/bin/env python3
"""Exact regressions for the metric C/D theorem; see README for the proof."""
import argparse
from collections import Counter
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'mixed', HERE.parent/'planar_two_geodesic_subdivided_mixed_annuli/verify.py')
mixed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mixed)
base, fan, require = mixed.base, mixed.fan, mixed.require


def repeated(value, n):
    return list(value) if isinstance(value, (list,tuple)) else [value]*n


def wheel(k, rho, outer):
    require(k >= 3 and len(outer) == k, 'outer cycle')
    rho = repeated(rho,k)
    require(len(rho) == k and all(x > 0 for x in rho+outer), 'positive wheel lengths')
    edges = [(0, i+1, rho[i]) for i in range(k)]
    edges += [(i+1, (i+1) % k+1, outer[i]) for i in range(k)]
    return base.Graph(k+1, edges, [])


def core_graph(word, rho, sigma, outer, arc_lengths):
    require(set(word) <= set('CD') and word.count('D') >= 3, 'C/D word')
    k = word.count('D')
    rho,sigma = repeated(rho,k),repeated(sigma,len(word))
    require(len(sigma) == len(word) and all(x > 0 for x in sigma) and len(arc_lengths) == len(word), 'cross lengths and arcs')
    w = wheel(k, rho, outer)
    wd = w.distances()
    g, A, C, arcs = mixed.core_graph(word, list(map(len, arc_lengths)))
    for a,price in zip(A,rho):
        g.adj[0][a] = g.adj[a][0] = price
    for i, a in enumerate(A):
        b = A[(i+1) % k]
        g.adj[a][b] = g.adj[b][a] = outer[i]
    parent = []
    i = 0
    for j, letter in enumerate(word):
        parent.append(A[i % k])
        g.adj[A[i % k]][C[j]] = g.adj[C[j]][A[i % k]] = sigma[j]
        prices = arc_lengths[j]
        require(prices and all(x > 0 for x in prices), 'positive arc edges')
        next_i = i+int(letter == 'D')
        require(sum(prices) >= wd[A[i % k]][A[next_i % k]]+abs(sigma[j]-sigma[(j+1) % len(word)]), 'arc projection bound')
        i = next_i
        for a, b, price in zip(arcs[j], arcs[j][1:], prices):
            g.adj[a][b] = g.adj[b][a] = price
    g.sphere()
    return g, A, C, arcs, parent, w, wd


def system(g, original_A, original_C, original_arcs, original_word,
           core, dist, w, wd, sigma, result, shift):
    word = original_word[shift:]+original_word[:shift]
    ai = original_word[:shift].count('D')
    A = original_A[ai:]+original_A[:ai]
    C = original_C[shift:]+original_C[:shift]
    arcs = original_arcs[shift:]+original_arcs[:shift]
    k, m = len(A), len(C)
    sigma = repeated(sigma,len(original_word))
    sigma = sigma[shift:]+sigma[:shift]
    S0 = (0,A[0],C[0])
    P = w.shortest(0,A[0],wd)+(C[0],)
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
        elif Y and A[0] not in Y:
            alpha[A.index(next(iter(Y)))] |= K
        else:
            discarded |= K
    mass_set = set(range(len(g.adj)))-set(S0)-discarded
    groups = alpha+gamma+tau+kappa
    require(set().union(*groups) == mass_set and sum(map(len, groups)) == len(mass_set),
            'disjoint mass partition')
    def atom(values, i): return values[i % len(values)]
    def bounds(i, j):
        L = set().union(*(alpha[x] | kappa[x] for x in range(i)),
                        *(gamma[x] | tau[x] for x in range(j)))
        return L, mass_set-L-atom(alpha, i)-atom(gamma, j)
    cuts = []
    def prepare(paths, sides, flavor):
        require(len(paths) <= 2, 'two paths')
        for path in paths:
            g.check_path(path, dist)
        deleted = set().union(*map(set, paths))
        require(set(S0) <= deleted, 'distinguished triple retained')
        parts = g.components(deleted)
        for K in parts:
            if K & core:
                require(any(K <= side for side in sides), 'full component containment')
            else:
                require(K in outside, 'whole individual detached attachment')
        cut = dict(paths=paths, sides=sides, parts=parts, flavor=flavor)
        cuts.append(cut)
        return cut
    carriers = {}
    for a in A:
        carrier = (C[0],)+w.shortest(A[0], a, wd)
        g.check_path(carrier, dist)
        require(dist[C[0]][a] == sigma[0]+wd[A[0]][a], 'projection with cross cost')
        carriers[a] = carrier
        result['carriers_with_root' if 0 in carrier else 'carriers_without_root'] += 1
        result['long_outer_carriers'] += int(0 not in carrier and len(carrier) >= 4)
    sequence = [prepare([P], bounds(0, 0), 'spoke')]
    transitions = []
    i = j = 0
    for letter in word:
        L, Rold = bounds(i, j)
        ni, nj = i+int(letter == 'D'), j+1
        Lnew, R = bounds(ni, nj)
        arc = arcs[j]
        coordinates = [0]
        for u, v in zip(arc, arc[1:]):
            coordinates.append(coordinates[-1]+g.adj[u][v])
        length = coordinates[-1]
        a, b = A[i % k], A[ni % k]
        if letter == 'C':
            threshold = length+sigma[(j+1) % m]-sigma[j]
            p = max(t for t, x in enumerate(coordinates) if 2*x <= threshold)
            q = min(t for t, x in enumerate(coordinates) if 2*x >= threshold)
            old = prepare([P, w.shortest(0,a,wd)+arc[:p+1]],
                          [L, Rold-set(arc[1:p+1])], 'C_left')
            new = prepare([P, w.shortest(0,a,wd)+tuple(reversed(arc[q:]))],
                          [Lnew-set(arc[q:-1]), R], 'C_right')
            heavy = old['sides'][1], new['sides'][0]
            choices = [old, new]
            result['C_exchanges'] += 1
        else:
            ea, eb = carriers[a], carriers[b]
            delta = wd[a][b]
            offset = sigma[(j+1) % m]-sigma[j]
            central = length+offset+wd[0][b]-wd[0][a]
            q = min(t for t, x in enumerate(coordinates)
                    if 2*x >= (length+offset-delta if 0 in ea else central))
            p = max(t for t, x in enumerate(coordinates)
                    if 2*x <= (length+offset+delta if 0 in eb else central))
            suffix = ((b,) if 0 in ea else w.shortest(0,b,wd))+tuple(reversed(arc[q:]))
            prefix = ((a,) if 0 in eb else w.shortest(0,a,wd))+arc[:p+1]
            left = prepare([ea, suffix],
                           [L | atom(gamma,j) | set(arc[1:q]), R], 'D_left')
            right = prepare([eb, prefix],
                            [L, R | atom(gamma,j+1) | set(arc[p+1:-1])], 'D_right')
            require(q <= p+1, 'no gap between threshold cuts')
            heavy = left['sides'][0], right['sides'][1]
            choices = [left, right]
            result['D_exchanges'] += 1
            result['both_carriers_omit_root'] += int(0 not in ea and 0 not in eb)
        require(not heavy[0] & heavy[1] and heavy[0] | heavy[1] <= mass_set,
                'disjoint potentially heavy supports')
        i, j = ni, nj
        sequence.append(prepare([P, w.shortest(0,A[i % k],wd)+(C[j % m],)], (Lnew,R), 'spoke'))
        transitions.append(choices)
    require((i,j) == (k,m), 'full cyclic sweep')
    result['systems'] += 1
    result['component_cuts'] += len(cuts)
    return dict(anchor=S0, mass_set=mass_set, discarded=discarded, outside=outside,
                sequence=sequence, transitions=transitions, cuts=cuts)


def choose(sys, masses, result):
    mass = lambda S: sum(masses[v] for v in S)
    M = mass(sys['mass_set'])
    require(M == sum(masses)-mass(sys['anchor'])-mass(sys['discarded']), 'M identity')
    twice_h = max(M, 2*max(map(mass, sys['outside']), default=0))
    good = lambda sets: all(2*mass(S) <= twice_h for S in sets)
    chosen = None
    for j, cut in enumerate(sys['sequence']):
        if good(cut['sides']):
            chosen = cut
            break
        if j and 2*mass(sys['sequence'][j-1]['sides'][1]) > twice_h and 2*mass(cut['sides'][0]) > twice_h:
            chosen = next((x for x in sys['transitions'][j-1] if good(x['sides'])), None)
            require(chosen is not None, 'failed transition repaired')
            break
    require(chosen is not None and good(chosen['parts']), 'quantitative residual bound')
    result['quantitative_checks'] += 1
    result[chosen['flavor']+'_choices'] += 1
    result['sharper_than_half'] += int(twice_h < sum(masses))
    return chosen, twice_h


def prices(word, rho, sigma, outer, pattern):
    wd = wheel(word.count('D'), rho, outer).distances()
    sigma = repeated(sigma,len(word))
    answer = []
    i = 0
    for j, letter in enumerate(word):
        d = (wd[i+1][(i+1) % len(outer)+1] if letter == 'D' else 0)+abs(sigma[j]-sigma[(j+1) % len(word)])
        d = max(d,F(1,7))
        vectors = [[d], [3*d/4,d/2,3*d/4], [d/7,2*d/7,4*d/7],
                   [2*d,d/9,d/3], [d/10]*10]
        answer.append(vectors[(j+pattern) % len(vectors)])
        i += int(letter == 'D')
        i %= len(outer)
    return answer


def main():
    result = Counter()
    rng = random.Random(2026092917)
    designs = [
        ('DDD', F(2), F(3), [F(1),F(9),F(2)]),
        ('DDDD', [F(1),F(9),F(3),F(7)], [F(1,3),F(4),F(2),F(1)], [F(7),F(1),F(8),F(1,5)]),
        ('DDDDD', F(4), F(4), [F(4)]*5),
        ('DCDCCDDCC', [F(3),F(1),F(8),F(2)], [F(1+j % 3,2) for j in range(9)], [F(7),F(1,3),F(2),F(11)]),
        ('CCCDDCCDCCCD', F(2,3), F(5,4), [F(4),F(1),F(3),F(9)]),
        ('DCCDCDCDCD', F(20), F(2), [F(1)]*5),
    ]
    for index, (word,rho,sigma,outer) in enumerate(designs):
        g,A,C,arcs,parents,w,wd = core_graph(word,rho,sigma,outer,prices(word,rho,sigma,outer,index))
        core = set(range(len(g.adj)))
        d0 = g.distances()
        # A deliberately generous length avoids creating a boundary shortcut.
        outside_length = max(repeated(rho,len(A))+outer+repeated(sigma,len(C)))
        for i in range(len(A)):
            if i % 2 == 0:
                g.attach(3,(0,A[i],A[(i+1) % len(A)]),long_edges=outside_length)
            start = len(g.adj)
            fan.previous.old.ears(g,len(A),i,3)
            for u in range(start,len(g.adj)):
                for v in g.adj[u]:
                    g.adj[u][v] = g.adj[v][u] = outside_length
        g.attach(2,(0,A[1]),long_edges=outside_length)
        g.sphere()
        dist = g.distances()
        require(all(dist[u][v] == d0[u][v] for u in core for v in core), 'core isometry')
        for c,a,cross_length in zip(C,parents,repeated(sigma,len(C))):
            for b in A:
                require(dist[c][b] == cross_length+wd[a][b], 'all parent projection distances')
                result['projection_distances'] += 1
        for piece in g.pieces:
            g.check_local_decomposition(piece)
            result['local_decompositions'] += 1
        profiles = list(base.masses(g,rng))
        for arc in arcs:
            profiles.append([int(v in arc[1:-1]) for v in range(len(g.adj))])
        for shift in range(len(word)):
            sys = system(g,A,C,arcs,word,core,dist,w,wd,sigma,result,shift)
            for masses in profiles:
                cut,twice_h = choose(sys,masses,result)
                if any(2*sum(masses[v] for v in K) > sum(masses) for K in sys['outside']):
                    fan.previous.old.heavy(g,dist,masses,result)
                else:
                    require(twice_h <= sum(masses), 'light attachment half bound')
                    require(all(2*sum(masses[v] for v in K) <= sum(masses) for K in cut['parts']), 'half corollary')
                    result['light_half_checks'] += 1
        result['fixtures'] += 1
    for trial in range(30):
        k = rng.randrange(3,9)
        word = ''.join('D'+'C'*rng.randrange(4) for _ in range(k))
        rho = [F(rng.randrange(1,9),rng.randrange(1,5)) for _ in range(k)]
        sigma = [F(rng.randrange(1,9),rng.randrange(1,5)) for _ in word]
        outer = [F(rng.randrange(1,16),rng.randrange(1,6)) for _ in range(k)]
        g,A,C,arcs,parents,w,wd = core_graph(word,rho,sigma,outer,prices(word,rho,sigma,outer,trial))
        core = set(range(len(g.adj)))
        system(g,A,C,arcs,word,core,g.distances(),w,wd,sigma,result,trial % len(word))
        result['additional_metric_models'] += 1
    for key in ['C_left_choices','C_right_choices','D_left_choices','D_right_choices',
                'heavy_checks','long_outer_carriers','both_carriers_omit_root']:
        require(result[key] > 0, 'branch exercised: '+key)
    return dict(sorted(result.items()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    answer = main()
    if args.check:
        require(answer == json.loads((HERE/'expected.json').read_text()), 'expected exact evidence')
    print(json.dumps(answer,indent=2,sort_keys=True))
