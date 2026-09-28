#!/usr/bin/env python3
"""Exact regressions for unit annular faces; universal assertions are proved in README."""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'fan_annuli', HERE.parent/'planar_two_geodesic_fan_annuli'/'verify.py')
fan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fan)
base, require = fan.base, fan.require


def maximum_run(word, letter):
    count = answer = 0
    for x in word+word:
        count = count+1 if x == letter else 0
        answer = max(answer, count)
    return answer


def validate(word):
    require(word and set(word) <= set('ACD'), 'annular word')
    k, m = sum(x in 'AD' for x in word), sum(x in 'CD' for x in word)
    require(k >= 5 and m >= 5, 'cycle orders')
    require(maximum_run(word, 'A') <= k-4 and maximum_run(word, 'C') <= m-4, 'fan wrap bounds')
    require('DAD' not in word+word[:2], 'no isolated A between two D steps')
    return k, m


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


def system(g, original_A, original_C, original_arcs, original_word, core, dist, result, shift=0):
    word = original_word[shift:]+original_word[:shift]
    require(not (word[0] == word[-1] == 'A'), 'seam does not split an A-run')
    ai = sum(x in 'AD' for x in original_word[:shift])
    cj = sum(x in 'CD' for x in original_word[:shift])
    A = original_A[ai:]+original_A[:ai]
    C = original_C[cj:]+original_C[:cj]
    arcs = original_arcs[cj:]+original_arcs[:cj]
    k, m = len(A), len(C)
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
    def prepare(path, sides):
        g.check_path(path, dist)
        parts = g.components(set(P) | set(path))
        for K in parts:
            if K & core: require(any(K <= side for side in sides), 'exact component containment')
            else: require(K in outside, 'whole detached attachment')
        cut = dict(path=path, sides=sides, parts=parts)
        cuts.append(cut)
        return cut
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
            else:
                require(word[pos-1] == 'C', 'backward C neighbor exists')
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
                mass_set=mass_set)


def quantitative(g, sys, w, result):
    def mass(K): return sum(w[v] for v in K)
    M = mass(sys['mass_set'])
    require(M == sum(w)-mass(sys['P'])-mass(sys['discarded']), 'represented mass identity')
    bound2 = max(M, 2*max(map(mass, sys['outside']), default=0),
                 2*max((mass(f['internal']) for f in sys['fans']), default=0))
    def balanced(parts): return all(2*mass(K) <= bound2 for K in parts)
    chosen = None
    for j, cut in enumerate(sys['sequence']):
        if balanced(cut['sides']): chosen = cut; break
        if j and 2*mass(sys['sequence'][j-1]['sides'][1]) > bound2 and 2*mass(cut['sides'][0]) > bound2:
            chosen = next((q for q in sys['transitions'][j-1][1] if balanced(q['sides'])), None)
            require(chosen is not None, 'quantitative transition repair')
            break
    require(chosen is not None and balanced(chosen['parts']), 'original quantitative residual bound')
    result['quantitative_checks'] += 1
    result['sharper_than_half_bounds'] += int(bound2 < sum(w))


def nonuniform_control(result):
    # The geometric cut choices still exist, but their mass identity can fail.
    g, A, C, arcs = core_graph('D'*5, [1]*5, scale=4)
    inside = sorted(fan.previous.reroot.subdivide(g, C[0], C[1], [3,2,3]))
    arc = tuple([C[0]]+inside+[C[1]])
    coordinates = fan.previous.positions(g, arc)
    require(coordinates == [0,3,5,8], 'nonuniform control coordinates')
    n, scale = coordinates[-1], 4
    p = max(i for i, x in enumerate(coordinates) if 2*x <= n)
    q = min(i for i, x in enumerate(coordinates) if 2*x >= n)
    u = max(i for i, x in enumerate(coordinates) if 2*x <= n-scale)
    v = min(i for i, x in enumerate(coordinates) if 2*x >= n+scale)
    paths = [(0,A[0])+arc[:p+1], (0,A[1])+tuple(reversed(arc[q:])),
             (A[0],A[1])+tuple(reversed(arc[v:])), (A[1],A[0])+arc[:u+1]]
    g.sphere(); dist = g.distances()
    for path in paths: g.check_path(path, dist)
    coefficients = Counter(x for part in [arc[p+1:-1],arc[1:q],arc[1:v],arc[u+1:-1]] for x in part)
    require([coefficients[x] for x in inside] == [3,3], 'unit four-side identity does not extend to these lengths')
    result['nonuniform_identity_defects'] = len(inside)


def main():
    result = dict(fixtures=0, systems=0, component_cuts=0, fan_decompositions=0,
                  local_decompositions=0, heavy_checks=0, heavy_fan_checks=0,
                  heavy_fan_five_bag_choices=0, heavy_fan_multiple_pockets=0,
                  light_checks=0, spoke_choices=0, C_choices=0, D_choices=0,
                  long_fan_choices=0, forward_A_choices=0, backward_A_choices=0,
                  seam_choices=0, quadrilateral_identities=0, one_sided_identities=0,
                  rejected_DAD=0, additional_core_models=0, quantitative_checks=0,
                  sharper_than_half_bounds=0, nonuniform_identity_defects=0)
    rng = random.Random(2026092814)
    words = ['D'*5, 'DCC'*5, 'DAC'*5, 'CAD'*5,
             'AAADCCAACDDAACCCD', 'AC'*6]
    for index, word in enumerate(words):
        k, m = validate(word)
        scale = 2 if index == 3 else 1
        lengths = [1+(2*j+index) % 6 for j in range(m)]
        g, A, C, arcs = core_graph(word, lengths, scale)
        core = set(range(len(g.adj))); d0 = g.distances()
        for i in range(k):
            if i % 2 == 0: g.attach(3, (0,A[i],A[(i+1) % k]), long_edges=1)
            fan.previous.old.ears(g, k, i, 3)
            fan.previous.old.ears(g, k, i, 4)
        g.attach(2, (0,A[1]), long_edges=1)
        g.sphere(); dist = g.distances()
        require(all(dist[u][v] == d0[u][v] for u in core for v in core), 'core isometry')
        for piece in g.pieces:
            g.check_local_decomposition(piece); result['local_decompositions'] += 1
        profiles = list(base.masses(g, rng))
        for arc in arcs:
            profiles.append([int(v in set(arc[1:-1])) for v in range(len(g.adj))])
        shifts = [s for s in range(len(word)) if not (word[s] == word[s-1] == 'A')]
        for shift in shifts:
            sys = system(g, A, C, arcs, word, core, dist, result, shift)
            result['systems'] += 1; result['component_cuts'] += len(sys['cuts'])
            result['fan_decompositions'] += len(sys['fans'])
            weights = list(profiles)
            for part in sys['fans']:
                weights.append([int(v in part['internal']) for v in range(len(g.adj))])
            for w in weights:
                quantitative(g, sys, w, result)
                fan.finish(g, sys, w, dist, result)
        result['fixtures'] += 1
    # Random words and reflections check component sets, not sampled masses.
    for trial in range(40):
        while True:
            word = ''.join(rng.choice('ACD') for _ in range(rng.randrange(12, 25)))
            try: validate(word)
            except AssertionError: continue
            break
        if trial % 2: word = word[::-1]
        k, m = validate(word)
        shift = next(s for s in range(len(word)) if not (word[s] == word[s-1] == 'A'))
        g, A, C, arcs = core_graph(word, [rng.randrange(1, 9) for _ in range(m)])
        core = set(range(len(g.adj)))
        sys = system(g, A, C, arcs, word, core, g.distances(), result, shift)
        result['component_cuts'] += len(sys['cuts'])
        result['additional_core_models'] += 1
    try: validate('DAD'+'D'*5)
    except AssertionError as error:
        require(str(error) == 'no isolated A between two D steps', 'expected DAD exclusion')
        result['rejected_DAD'] = 1
    nonuniform_control(result)
    require(all(result[x] > 0 for x in result), 'all claimed branches exercised')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    answer = main()
    if args.check: require(answer == json.loads((HERE/'expected.json').read_text()), 'expected evidence')
    print(json.dumps(answer, indent=2, sort_keys=True))
