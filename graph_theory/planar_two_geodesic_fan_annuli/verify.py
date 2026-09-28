#!/usr/bin/env python3
"""Exact regression checks for the written fan-annulus theorem, not a census."""
import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'subdivided', HERE.parent/'planar_two_geodesic_subdivided_annuli'/'verify.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
base, require = previous.base, previous.require


def core_graph(runs, scale, lengths):
    require(len(runs) >= 5 and all(d > 0 and e > 0 for d, e in runs), 'five positive fan pairs')
    k, m = sum(d for d, e in runs), sum(e for d, e in runs)
    require(len(lengths) == m, 'one length list per inner edge')
    A, C = list(range(1, k+1)), list(range(k+1, k+m+1))
    edges, faces = {}, []
    def edge(a, b): edges[tuple(sorted((a, b)))] = scale
    for i in range(k):
        edge(0, A[i]); edge(A[i], A[(i+1) % k])
        faces.append((0, A[i], A[(i+1) % k]))
    for j in range(m): edge(C[j], C[(j+1) % m])
    i = j = 0
    for d, e in runs:
        for _ in range(d):
            edge(A[i % k], C[j % m]); edge(A[(i+1) % k], C[j % m])
            faces.append((A[i % k], C[j % m], A[(i+1) % k])); i += 1
        for _ in range(e):
            edge(A[i % k], C[j % m]); edge(A[i % k], C[(j+1) % m])
            faces.append((A[i % k], C[j % m], C[(j+1) % m])); j += 1
    faces.append(tuple(reversed(C)))
    g = base.Graph(1+k+m, [(a, b, v) for (a, b), v in edges.items()], faces)
    arcs = []
    for j, sizes in enumerate(lengths):
        require(sizes and all(x > 0 for x in sizes), 'positive rim lengths')
        require(sum(sizes) >= scale, 'rim lower bound')
        require(len(sizes) == 1 or sum(sizes) >= 2*scale, 'subdivided rim lower bound')
        u, v = C[j], C[(j+1) % m]
        inside = sorted(previous.reroot.subdivide(g, u, v, sizes))
        arcs.append(tuple([u]+inside+[v]))
    g.sphere()
    return g, A, C, arcs


def check_decomposition(g, bags, edges):
    tree = [set() for _ in bags]
    for a, b in edges: tree[a].add(b); tree[b].add(a)
    require(len(edges) == len(bags)-1, 'tree edge count')
    def reachable(nodes):
        seen = {min(nodes)}; todo = list(seen)
        while todo:
            new = (tree[todo.pop()] & nodes)-seen
            seen |= new; todo.extend(new)
        return seen
    require(reachable(set(range(len(bags)))) == set(range(len(bags))), 'tree connected')
    for v in range(len(g.adj)):
        nodes = {i for i, bag in enumerate(bags) if v in bag}
        require(nodes and reachable(nodes) == nodes, 'running intersection')
    for u, row in enumerate(g.adj):
        for v in row: require(any({u, v} <= bag for bag in bags), 'edge covered')


def fan_decomposition(g, A, c, l, t, F, dist):
    k = len(A)
    bags = [{0, c, A[l % k], A[s % k], A[(s+1) % k]} for s in range(l, t)]
    edges = [(i, i+1) for i in range(len(bags)-1)]
    anchor = len(bags)-1
    covers = []
    for s, bag in zip(range(l, t), bags):
        path = (0, A[s % k], c)
        rest = sorted(bag-set(path))
        cover = [path]
        if rest: cover.append(g.shortest(rest[0], rest[-1], dist))
        covers.append(cover)
    for piece in g.pieces:
        if piece['internal'] <= F:
            host = next(i for i, bag in enumerate(bags[:t-l]) if piece['boundary'] <= bag)
            guest = next(i for i, bag in enumerate(piece['bags']) if piece['boundary'] <= bag)
            offset = len(bags)
            edges.extend((a+offset, b+offset) for a, b in piece['tree'])
            edges.append((host, guest+offset))
            bags.extend(piece['bags'])
            covers.extend(base.cover_bag(g, bag, dist) for bag in piece['bags'])
    require({0, c, A[l % k], A[t % k]} <= bags[anchor], 'whole fan boundary in anchor')
    edges.append((anchor, len(bags)))
    check_decomposition(g, bags+[set(range(len(g.adj)))-F], edges)
    for bag, cover in zip(bags, covers):
        require(len(cover) <= 2 and bag <= set().union(*map(set, cover)), 'two-path bag cover')
        for path in cover: g.check_path(path, dist)
    return dict(internal=F, bags=bags, covers=covers)


def system(g, original_A, original_C, original_arcs, original_runs, core, dist, shift=0):
    ai = sum(d for d, e in original_runs[:shift])
    cj = sum(e for d, e in original_runs[:shift])
    A = original_A[ai:]+original_A[:ai]
    C = original_C[cj:]+original_C[:cj]
    arcs = original_arcs[cj:]+original_arcs[:cj]
    runs = original_runs[shift:]+original_runs[:shift]
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
        require(N <= Y | {0} and len(Y) <= 2, 'root-clique boundary')
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
        left = set().union(*(alpha[x] | kappa[x] for x in range(i)),
                           *(gamma[x] | tau[x] for x in range(j)))
        return left, mass_set-left-atom(alpha, i)-atom(gamma, j)
    cuts = []
    def prepare(Q, sides):
        g.check_path(Q, dist)
        parts = g.components(set(P) | set(Q))
        for K in parts:
            if K & core: require(any(K <= side for side in sides), 'component containment')
            else: require(K in outside, 'whole outside component')
        cut = dict(path=Q, sides=sides, parts=parts)
        cuts.append(cut)
        return cut
    sequence, transitions, fans = [], [], []
    i = j = 0
    sequence.append(prepare(P, bounds(0, 0)))
    for d, e in runs:
        l, t = i, i+d
        L_start, _ = bounds(l, j)
        _, R_end = bounds(t, j)
        if d >= 2:
            F = set().union(*(alpha[s] for s in range(l+1, t)), *(kappa[s] for s in range(l, t)))
            boundary = {0, C[j % m], A[l % k], A[t % k]}
            require(F in g.components(boundary), 'fan is a whole component')
            require(A[t % k] not in g.adj[A[l % k]], 'nonadjacent fan endpoints')
            fan = fan_decomposition(g, A, C[j % m], l, t, F, dist)
            fans.append(fan)
            choices = [prepare((A[l % k], C[j % m], A[t % k]), [L_start, R_end, F])]
            label = 'long_fan_choices'
        else:
            patch = tau[(j-1) % m] | {C[j % m]} | tau[j % m]
            if tau[(j-1) % m] or tau[j % m]:
                choices = [prepare((C[(j-1) % m], A[l % k], A[t % k], C[(j+1) % m]), [L_start, R_end, patch])]
                label = 'outer_detours'
            else:
                plus = prepare((A[l % k], A[t % k], C[(j+1) % m]), [L_start | gamma[j % m], R_end])
                minus = prepare((A[t % k], A[l % k], C[(j-1) % m]), [L_start, R_end | gamma[j % m]])
                choices = [plus, minus]; label = 'old_exchange_choices'
                _, R_start = bounds(l, j)
                L_end, _ = bounds(t, j)
                count = Counter(v for side in [R_start, L_end, plus['sides'][0], minus['sides'][1]] for v in side)
                require(all(count[v] == 2-int(v in atom(alpha, l) | atom(alpha, t)) for v in mass_set), 'four-side identity')
        for _ in range(d):
            i += 1
            sequence.append(prepare((0, A[i % k], C[j % m]), bounds(i, j)))
            transitions.append((label, choices))
        for _ in range(e):
            L, R = bounds(i, j)
            LN, RN = bounds(i, j+1)
            coords = previous.positions(g, arcs[j])
            a, b = previous.split_index(coords, 2*coords[-1])
            remove_left, remove_right = set(arcs[j][1:a+1]), set(arcs[j][b:-1])
            mu = prepare((0, A[i % k])+arcs[j][:a+1], [L, R-remove_left])
            mv = prepare((0, A[i % k])+tuple(reversed(arcs[j][b:])),
                         [L | atom(gamma, j) | (tau[j]-remove_right), RN])
            require(not mu['sides'][1] & mv['sides'][0], 'midpoint heavy supports disjoint')
            require(mu['sides'][1] | mv['sides'][0] <= mass_set, 'midpoint supports accounted')
            j += 1
            sequence.append(prepare((0, A[i % k], C[j % m]), (LN, RN)))
            transitions.append(('midpoint_choices', [mu, mv]))
    require(i == k and j == m, 'one full annular sweep')
    patches = [tau[(j-1) % m] | {C[j]} | tau[j] for j in range(m)]
    covers = [previous.cover_three_portal(g, arcs[(j-1) % m], tuple(reversed(arcs[j])), dist) for j in range(m)]
    return dict(P=P, sequence=sequence, transitions=transitions, fans=fans, patches=patches,
                covers=covers, outside=outside, cuts=cuts, discarded=discarded)


def finish(g, sys, w, dist, result):
    W = sum(w)
    def mass(K): return sum(w[v] for v in K)
    def valid(parts): return all(2*mass(K) <= W for K in parts)
    if any(2*mass(K) > W for K in sys['outside']):
        previous.old.heavy(g, dist, w, result)
        return
    for fan in sys['fans']:
        if 2*mass(fan['internal']) > W:
            choice = next((i for i, bag in enumerate(fan['bags']) if valid(g.components(bag))), None)
            require(choice is not None, 'heavy fan has a local centroid')
            removed = set().union(*map(set, fan['covers'][choice]))
            require(valid(g.components(removed)), 'heavy fan gives original full-graph balance')
            result['heavy_fan_checks'] += 1
            result['heavy_fan_five_bag_choices'] += int(len(fan['bags'][choice]) == 5)
            result['heavy_fan_multiple_pockets'] += int(sum(K <= fan['internal'] and mass(K) > 0 for K in sys['outside']) >= 2)
            return
    for patch, cover in zip(sys['patches'], sys['covers']):
        if 2*mass(patch) > W:
            removed = set().union(*map(set, cover))
            require(patch <= removed and valid(g.components(removed)), 'whole heavy patch deleted')
            result['heavy_patch_checks'] += 1
            return
    chosen = None
    for j, cut in enumerate(sys['sequence']):
        if valid(cut['sides']):
            chosen = cut; result['spoke_choices'] += 1; break
        if j and 2*mass(sys['sequence'][j-1]['sides'][1]) > W and 2*mass(cut['sides'][0]) > W:
            label, choices = sys['transitions'][j-1]
            chosen = next((q for q in choices if valid(q['sides'])), None)
            require(chosen is not None, 'heavy-side transition repaired')
            result[label] += 1
            break
    require(chosen is not None and valid(chosen['parts']), 'full-graph half balance')
    result['light_checks'] += 1


def main():
    result = dict(fixtures=0, systems=0, component_cuts=0, local_decompositions=0,
                  fan_decompositions=0, five_vertex_bags=0, heavy_checks=0,
                  heavy_fan_checks=0, heavy_fan_five_bag_choices=0,
                  heavy_fan_multiple_pockets=0, heavy_patch_checks=0, light_checks=0,
                  spoke_choices=0, midpoint_choices=0, outer_detours=0,
                  old_exchange_choices=0, long_fan_choices=0, rejected_few_runs=0,
                  irregular_core_models=0, strict_fixture_vertices=0)
    rng = random.Random(2026092813)
    designs = [([(1,1)]*5, 1, False),
               ([(3,1),(1,3),(2,2),(1,1),(4,2)], 1, False),
               ([(3,1),(1,3),(2,2),(1,1),(4,2)], 1, True),
               ([(1,4),(2,1),(1,2),(5,3),(1,1),(2,2)], 2, True),
               ([(2,2)]*5, 4, True),
               ([(5,1),(1,5),(1,1),(1,1),(1,1)], 1, True)]
    for runs, scale, divided in designs:
        m = sum(e for d, e in runs)
        sizes = [[scale] if not divided or j % 3 == 1 else [1, scale, 2*scale] for j in range(m)]
        g, A, C, arcs = core_graph(runs, scale, sizes)
        core = set(range(len(g.adj))); d0 = g.distances()
        for i in range(len(A)):
            if i % 2 == 0: g.attach(3, (0, A[i], A[(i+1) % len(A)]), long_edges=max(1, scale//2))
        for i in range(len(A)):
            previous.old.ears(g, len(A), i, max(3, scale))
            previous.old.ears(g, len(A), i, max(4, scale))
        g.attach(2, (0, A[1]), long_edges=max(1, scale//2))
        g.sphere(); dist = g.distances()
        require(all(dist[u][v] == d0[u][v] for u in core for v in core), 'core isometry')
        for piece in g.pieces:
            g.check_local_decomposition(piece); result['local_decompositions'] += 1
        profiles = list(base.masses(g, rng))
        # Sparse masses make whole fans heavy while every outside piece stays light.
        for i in range(len(A)):
            w = [0]*len(g.adj)
            for j in range(4): w[A[(i+j) % len(A)]] = 1
            profiles.append(w)
        for shift in range(len(runs)):
            sys = system(g, A, C, arcs, runs, core, dist, shift)
            result['systems'] += 1; result['component_cuts'] += len(sys['cuts'])
            result['fan_decompositions'] += len(sys['fans'])
            result['five_vertex_bags'] += sum(len(bag) == 5 for fan in sys['fans'] for bag in fan['bags'])
            weights = list(profiles)
            for fan in sys['fans']:
                weights.append([int(v in fan['internal']) for v in range(len(g.adj))])
            for patch in sys['patches']:
                weights.append([int(v in patch) for v in range(len(g.adj))])
            for w in weights: finish(g, sys, w, dist, result)
        result['fixtures'] += 1
    # Varied incidence regression, additional to the six mass fixtures.
    for trial in range(30):
        runs = [(rng.randrange(1, 5), rng.randrange(1, 5)) for _ in range(5+trial % 3)]
        m = sum(e for d, e in runs)
        lengths = [[1]*(1+rng.randrange(4)) for _ in range(m)]
        g, A, C, arcs = core_graph(runs, 1, lengths)
        core = set(range(len(g.adj)))
        sys = system(g, A, C, arcs, runs, core, g.distances(), trial % len(runs))
        result['irregular_core_models'] += 1
        result['component_cuts'] += len(sys['cuts'])
    # Same number of A and C vertices, but their cross-incidences are irregular.
    runs = [(2,1),(1,2),(1,1),(1,1),(1,1)]
    g, A, C, arcs = core_graph(runs, 1, [[1,1]]*6)
    core = set(range(len(g.adj)))
    for i in (0,2,4): g.attach(3, (0,A[i],A[(i+1) % len(A)]))
    g.sphere(); dist = g.distances()
    require(any(len(set(g.adj[a]) & set(C)) != 2 for a in A), 'displayed incidence is not the regular core')
    sys = system(g, A, C, arcs, runs, core, dist)
    finish(g, sys, [1]*len(g.adj), dist, result)
    require(len(g.adj) == 49, 'strict displayed-hypothesis fixture order')
    result['strict_fixture_vertices'] = len(g.adj)
    try: core_graph([(1,1)]*4, 1, [[1]]*4)
    except AssertionError as error:
        require(str(error) == 'five positive fan pairs', 'expected rejection')
        result['rejected_few_runs'] = 1
    require(all(result[key] > 0 for key in result), 'every reported branch exercised')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    answer = main()
    if args.check: require(answer == json.loads((HERE/'expected.json').read_text()), 'compact expected evidence')
    print(json.dumps(answer, indent=2, sort_keys=True))
