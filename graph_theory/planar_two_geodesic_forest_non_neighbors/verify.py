"""Exact regression checks for the written forest-patch theorem.

Python standard library; no finite sample is used as an all-order proof.
Port words encode planar tree-in-polygon fixtures. Fill edges are kept
separate from metric edges. The construction is checked against an
independent elimination-prefix computation and all TD axioms.
"""
import argparse
import itertools
import json
import random
from collections import deque
from pathlib import Path


def edge(a, b):
    return tuple(sorted((a, b)))


def adjacency(n, edges):
    out = [set() for _ in range(n)]
    for a, b in edges:
        assert a != b and 0 <= a < n and 0 <= b < n
        out[a].add(b)
        out[b].add(a)
    return out


def tree_word(tree):
    if len(tree) == 1:
        return [1]
    word = []
    def walk(u, parent):
        for v in sorted(tree[u] - {parent}):
            word.append(u)
            walk(v, u)
        if parent is not None:
            word.append(u)
    walk(1, None)
    return word


def make_patch(tree_edges, sources, labels, keep):
    k = max((max(e) for e in tree_edges), default=1)
    assert len(sources) == len(labels) and labels
    m = 1 + max(labels)
    assert set(labels) == set(range(m))
    n = 1 + k + m
    ports = [(x, k + 1 + y) for x, y in zip(sources, labels)]
    boundary = list(range(k + 1, n))
    cycle = sorted({edge(a, b) for a, b in
                    zip(boundary, boundary[1:] + boundary[:1]) if a != b})
    actual = set(map(lambda e: edge(*e), tree_edges))
    actual.update((0, y) for y in boundary)
    actual.update(edge(x, y) for x, y in ports)
    actual.update(e for j, e in enumerate(cycle) if keep >> j & 1)
    fill = actual | set(cycle) | {(0, x) for x in range(1, k + 1)}
    return dict(n=n, k=k, actual=actual, fill=fill, ports=ports,
                boundary=boundary, tree_edges=set(map(lambda e: edge(*e), tree_edges)))


def shortest(adj, start, finish):
    parent = {start: None}
    todo = deque([start])
    while finish not in parent:
        assert todo, 'disconnected pair'
        u = todo.popleft()
        for v in sorted(adj[u]):
            if v not in parent:
                parent[v] = u
                todo.append(v)
    path = [finish]
    while path[-1] != start:
        path.append(parent[path[-1]])
    return path[::-1]


def cover(adj, bag, kind, info, patch, counters):
    bag = set(bag)
    if len(bag) <= 4:
        vs = sorted(bag)
        return [shortest(adj, vs[i], vs[min(i + 1, len(vs)-1)])
                for i in range(0, len(vs), 2)]
    assert len(bag) == 5 and 0 in bag
    if kind == 'fan':
        x = info['source']
        bs = sorted(bag - {0, x})
        nonedge = next(((a, b) for a, b in itertools.combinations(bs, 2)
                        if b not in adj[a]), None)
        if nonedge is not None:
            a, b = nonedge
            first = [a, 0, b]
            counters['fan_nonedge'] += 1
        else:
            assert set(bs) == set(patch['boundary']), 'actual boundary chord'
            first = shortest(adj, 0, x)
            assert set(first) & set(bs)
            counters['fan_triangle'] += 1
    else:
        assert kind == 'leaf'
        u, v, w, z = info['u'], info['v'], info['w'], info['z']
        assert v in adj[u] and w != z
        if z not in adj[w]:
            counters['leaf_nonedge'] += 1
            return [[w, 0, z], [u, v]]
        # Independently test the original-tree cut used in the proof.
        original_tree = adjacency(patch['k'] + 1, patch['tree_edges'])
        possible = []
        for x, y in ((u, v), (v, u)):
            reached = {x}; todo = [x]
            while todo:
                a = todo.pop()
                for b in original_tree[a]:
                    if edge(a, b) != edge(x, y) and b not in reached:
                        reached.add(b); todo.append(b)
            neighbors = set().union(*(adj[a] for a in reached)) & set(patch['boundary'])
            if neighbors <= {w, z}:
                possible.append((x, y))
        assert possible, 'cut endpoints do not bound an empty original arc'
        x, y = possible[0]
        first = shortest(adj, 0, x)
        assert set(first) & {y, w, z}
        counters['leaf_adjacent'] += 1
    remaining = sorted(bag - set(first))
    assert len(remaining) <= 2
    second = [] if not remaining else [shortest(adj, remaining[0], remaining[-1])]
    return [first] + second


def construct(patch, counters):
    n, k = patch['n'], patch['k']
    metric = adjacency(n, patch['actual'])
    fill = adjacency(n, patch['fill'])
    tree = {x: set() for x in range(1, k + 1)}
    for u, v in patch['tree_edges']:
        tree[u].add(v); tree[v].add(u)
    assert len(patch['tree_edges']) == k - 1
    # Verify connectedness before interpreting the boundary word.
    reached = {1}; todo = [1]
    while todo:
        u = todo.pop()
        for v in tree[u] - reached:
            reached.add(v); todo.append(v)
    assert len(reached) == k
    ports = list(patch['ports'])
    boundary = list(patch['boundary'])
    alive = set(range(n))
    rows = []

    def eliminate(v, kind, info):
        neighbors = fill[v] & alive
        bag = neighbors | {v}
        paths = cover(metric, bag, kind, info, patch, counters)
        rows.append(dict(v=v, bag=sorted(bag), paths=paths, kind=kind))
        for a, b in itertools.combinations(neighbors, 2):
            fill[a].add(b); fill[b].add(a)
        alive.remove(v)

    while tree:
        u = min(x for x in tree if len(tree[x]) <= 1)
        v = next(iter(tree[u]), None)
        positions = [i for i, (x, _) in enumerate(ports) if x == u]
        if not positions:
            block = []
        elif len(positions) == len(ports):
            block = list(ports)
        else:
            starts = [i for i in positions if ports[(i-1) % len(ports)][0] != u]
            assert len(starts) == 1, 'current leaf does not have one port interval'
            block = []
            i = starts[0]
            while ports[i][0] == u:
                block.append(ports[i]); i = (i+1) % len(ports)
        ends = set() if not block else {block[0][1], block[-1][1]}
        interior = list(dict.fromkeys(y for _, y in block if y not in ends))
        for t in interior:
            assert {x for x, y in ports if y == t} == {u}
            i = boundary.index(t)
            a, b = boundary[(i-1) % len(boundary)], boundary[(i+1) % len(boundary)]
            assert (fill[t] & alive) <= {0, u, a, b}
            eliminate(t, 'fan', {'source': u})
            boundary.remove(t)
            ports = [(x, y) for x, y in ports if y != t]
        allowed = {0, u} | ends | ({v} if v is not None else set())
        assert (fill[u] & alive) | {u} <= allowed
        if v is not None and len(ends) == 2:
            w, z = sorted(ends)
            info = dict(u=u, v=v, w=w, z=z)
            kind = 'leaf'
        else:
            info = {}; kind = 'small'
        eliminate(u, kind, info)
        if v is not None:
            tree[v].remove(u)
            ports = [(v if x == u else x, y) for x, y in ports]
        else:
            ports = []
        del tree[u]
    for b in list(boundary):
        eliminate(b, 'small', {})
    eliminate(0, 'small', {})
    return rows


def verify_rows(patch, rows, counters):
    n = patch['n']; adj = adjacency(n, patch['actual'])
    filled = adjacency(n, patch['fill'])
    assert sorted(row['v'] for row in rows) == list(range(n))
    order = {row['v']: i for i, row in enumerate(rows)}
    bags = [set(row['bag']) for row in rows]
    td = [set() for _ in rows]
    prefix = set()
    for i, row in enumerate(rows):
        v = row['v']; reached = {v}; todo = [v]; boundary = set()
        # Reachability through the original filled graph and the eliminated
        # prefix gives the elimination bag without replaying mutable fill.
        while todo:
            a = todo.pop()
            boundary |= filled[a]
            for b in filled[a] & prefix - reached:
                reached.add(b); todo.append(b)
        expected = (boundary - prefix) | {v}
        assert bags[i] == expected and len(bags[i]) <= 5
        later = bags[i] - {v}
        if later:
            parent = min(later, key=order.get)
            j = order[parent]
            assert j > i and later <= bags[j]
            td[i].add(j); td[j].add(i)
        covered = set()
        assert 1 <= len(row['paths']) <= 2
        for path in row['paths']:
            assert len(path) == len(set(path))
            assert all(b in adj[a] for a, b in zip(path, path[1:]))
            # Distance only, separately from the witness's chosen BFS parent.
            reached2 = {path[0]}; frontier = {path[0]}; distance = 0
            while path[-1] not in reached2:
                frontier = set().union(*(adj[a] for a in frontier)) - reached2
                assert frontier
                reached2 |= frontier; distance += 1
            assert distance == len(path)-1
            counters['longest_path_edges'] = max(counters['longest_path_edges'], distance)
            covered.update(path)
        assert bags[i] <= covered
        counters['bags'] += 1
        counters['five_vertex_bags'] += len(bags[i]) == 5
        prefix.add(v)
    assert sum(map(len, td)) == 2 * (n - 1)
    for v in range(n):
        indices = {i for i, bag in enumerate(bags) if v in bag}
        reached = {min(indices)}; todo = list(reached)
        while todo:
            i = todo.pop()
            for j in td[i] & indices - reached:
                reached.add(j); todo.append(j)
        assert reached == indices
    for a, b in patch['fill']:
        assert any({a, b} <= bag for bag in bags)
    bs = patch['boundary']
    for a, b in zip(bs, bs[1:] + bs[:1]):
        assert any({0, a, b} <= bag for bag in bags)
    counters['cases'] += 1
    return td


def mass_checks(patch, rows, td, counters):
    n = patch['n']; adj = adjacency(n, patch['actual'])
    bags = [set(row['bag']) for row in rows]
    weights = [[1]*n, [0]*n]
    weights.extend([[int(i == v) for i in range(n)] for v in (0, 1, n-1)])
    weights.append([(i*i + 7*i + 3) % 11 for i in range(n)])
    assigned = [next(i for i, bag in enumerate(bags) if v in bag) for v in range(n)]
    for weight in weights:
        total = sum(weight)
        tree_mass = [0]*len(rows)
        for v, w in enumerate(weight):tree_mass[assigned[v]] += w
        centroid = None
        for i in range(len(rows)):
            good = True
            for neighbor in td[i]:
                reached = {i, neighbor}; todo = [neighbor]; mass = 0
                while todo:
                    a = todo.pop(); mass += tree_mass[a]
                    for b in td[a] - reached:
                        reached.add(b); todo.append(b)
                if 2*mass > total:good = False; break
            if good:centroid = i; break
        assert centroid is not None
        deleted = set().union(*map(set, rows[centroid]['paths']))
        left = set(range(n)) - deleted
        while left:
            a = min(left); left.remove(a); todo = [a]; mass = 0
            while todo:
                u = todo.pop(); mass += weight[u]
                for v in adj[u] & left:
                    left.remove(v); todo.append(v)
            assert 2*mass <= total
        counters['mass_checks'] += 1


def cyclic_patterns(size):
    yield (0,) * size
    for count in range(2, size+1):
        for cuts in itertools.combinations(range(size), count):
            labels = [None]*size; label = 0
            for step in range(size):
                i = (cuts[0]+1+step) % size
                labels[i] = label
                if i in cuts:label += 1
            rename = {}
            yield tuple(rename.setdefault(x, len(rename)) for x in labels)


def fixtures():
    # All endpoint identifications and boundary-edge subsets for the
    # nonempty corner words of a P3. Duplicates are intentionally removed.
    for groups in ((1, 3), (1, 2, 3), (1, 2, 3, 2)):
        sources = [x for x in groups for _ in range(2)]
        for labels in sorted(set(cyclic_patterns(len(sources)))):
            m = max(labels)+1
            cycle_size = m if m >= 3 else max(0, m-1)
            for keep in range(1 << cycle_size):
                yield make_patch({(1, 2), (2, 3)}, sources, labels, keep), False
    # Long inactive tree interiors, forks, and long fans. All have a port
    # embedding by construction; no planar-enumerator assumption is used.
    for k in (1, 2, 3, 4, 8, 16, 32):
        for kind in ('path', 'star', 'binary'):
            edges = {(i-1, i) for i in range(2, k+1)} if kind == 'path' else (
                {(1, i) for i in range(2, k+1)} if kind == 'star' else
                {(i//2, i) for i in range(2, k+1)})
            tree = {i:set() for i in range(1, k+1)}
            for a,b in edges:tree[a].add(b);tree[b].add(a)
            word = tree_word(tree)
            for mode in ('all', 'leaves', 'one'):
                selected = word if mode == 'all' else ([x for x in word if len(tree[x]) <= 1]
                    if mode == 'leaves' else [word[-1]])
                sources = [x for x in selected for _ in range(3)]
                # Shared ports at every third gap, and ordinary long fans.
                for merged in (False, True):
                    labels = list(range(len(sources))) if not merged else [i//2 for i in range(len(sources))]
                    m = max(labels)+1
                    for keep in (0, (1<<m)-1):
                        yield make_patch(edges, sources, labels, keep), True
    rng = random.Random(2026092805)
    for _ in range(600):
        k = rng.randrange(2, 13)
        edges = {(rng.randrange(1, i), i) for i in range(2, k+1)}
        tree = {i:set() for i in range(1, k+1)}
        for a,b in edges:tree[a].add(b);tree[b].add(a)
        sources = [x for x in tree_word(tree) for _ in range(rng.randrange(5))]
        if not sources:sources = [1]
        size = len(sources); cuts = [i for i in range(size) if rng.randrange(2)]
        if len(cuts) < 2:labels = [0]*size
        else:
            labels = [None]*size; label = 0
            for step in range(size):
                i = (cuts[0]+1+step) % size
                labels[i] = label
                if i in cuts:label += 1
            rename = {}; labels = [rename.setdefault(x, len(rename)) for x in labels]
        m = max(labels)+1
        yield make_patch(edges, sources, labels, rng.randrange(1<<m)), False


def extra_checks(counters):
    blank = lambda: dict(cases=0, bags=0, five_vertex_bags=0, fan_nonedge=0,
                         fan_triangle=0, leaf_nonedge=0, leaf_adjacent=0,
                         longest_path_edges=0, mass_checks=0)
    # Two patches glued along an actual triangle {r,a,b}. The clique
    # interface makes both induced patches isometric in their union.
    p = make_patch({(1,2),(2,3)}, [1,1,2,2,3,3,2,2], list(range(8)), 255)
    q = make_patch({(1,2),(1,3),(1,4)}, [1,2,1,3,1,4], list(range(6)), 63)
    p_rows = construct(p, blank()); q_rows = construct(q, blank())
    p_td = verify_rows(p, p_rows, blank()); q_td = verify_rows(q, q_rows, blank())
    shared = [0] + p['boundary'][:2]
    rename = {0:0, q['boundary'][0]:shared[1], q['boundary'][1]:shared[2]}
    next_id = p['n']
    for v in range(q['n']):
        if v not in rename:rename[v] = next_id; next_id += 1
    es = p['actual'] | {edge(rename[a], rename[b]) for a,b in q['actual']}
    rows = list(p_rows) + [dict(v=rename[row['v']],
        bag=[rename[x] for x in row['bag']],
        paths=[[rename[x] for x in path] for path in row['paths']]) for row in q_rows]
    td = [set(x) for x in p_td] + [{len(p_rows)+j for j in x} for x in q_td]
    i = next(i for i,row in enumerate(rows[:len(p_rows)]) if set(shared) <= set(row['bag']))
    j = next(j for j,row in enumerate(rows[len(p_rows):],len(p_rows)) if set(shared) <= set(row['bag']))
    td[i].add(j);td[j].add(i)
    adj = adjacency(next_id,es);bags=[set(row['bag']) for row in rows]
    assert sum(map(len,td)) == 2*(len(rows)-1)
    for v in range(next_id):
        indices={i for i,b in enumerate(bags) if v in b}
        reached={min(indices)};todo=list(reached)
        while todo:
            a=todo.pop()
            for b in td[a]&indices-reached:reached.add(b);todo.append(b)
        assert reached == indices
    for a,b in es:assert any({a,b} <= bag for bag in bags)
    for row,bag in zip(rows,bags):
        assert bag <= set().union(*map(set,row['paths']))
        for path in row['paths']:
            assert len(shortest(adj,path[0],path[-1])) == len(path)
    mass_checks(dict(n=next_id,actual=es),rows,td,counters)
    counters['glued_fixtures'] = 1

    # A concrete 16-vertex member outside the earlier clique-nonneighbor
    # and dominating-edge sufficient classes, with minimum degree four.
    sources=[x for x in (1,2,3,2) for _ in range(3)]
    strict=make_patch({(1,2),(2,3)},sources,list(range(12)),4095)
    adj=adjacency(strict['n'],strict['actual'])
    assert strict['n'] == 16 and min(map(len,adj)) == 4
    for r in range(len(adj)):
        left=set(range(len(adj)))-{r}-adj[r];all_cliques=True
        while left:
            a=min(left);left.remove(a);comp={a};todo=[a]
            while todo:
                u=todo.pop()
                for v in adj[u]&left:left.remove(v);comp.add(v);todo.append(v)
            if any(len(adj[u]&comp) != len(comp)-1 for u in comp):all_cliques=False
        assert not all_cliques
    assert not any({a,b}|adj[a]|adj[b] == set(range(len(adj))) for a,b in strict['actual'])
    counters['strict_extension_order'] = 16

    # Negative controls: reject a cycle, alternating leaf ports, a boundary
    # chord, a fake metric edge, and an altered decomposition bag.
    invalid=[]
    invalid.append(make_patch({(1,2),(2,3),(1,3)},[1,2,3],[0,1,2],7))
    invalid.append(make_patch({(1,2)},[1,2,1,2],[0,1,2,3],15))
    chord=make_patch({(1,2)},[1,1,1,2,2,2],list(range(6)),63)
    a,b=chord['boundary'][0],chord['boundary'][2]
    chord['actual'].add(edge(a,b));chord['fill'].add(edge(a,b));invalid.append(chord)
    rejected=0
    for bad in invalid:
        try:construct(bad,blank())
        except AssertionError:rejected+=1
        else:raise AssertionError('invalid port fixture accepted')
    for corrupt in ('path','bag'):
        rows=construct(p,blank())
        if corrupt=='path':rows[0]['paths']=[[0,1]]
        else:rows[0]['bag']=rows[0]['bag'][:-1]
        try:verify_rows(p,rows,blank())
        except AssertionError:rejected+=1
        else:raise AssertionError('corrupted witness accepted')
    counters['rejected_invalid_controls']=rejected

    # The general five-bag claim is false without the cut structure:
    # K4 on r,w,z,a and a triangle a,u,v. S={r,w,z,u,v} is in general
    # position, so two geodesics cannot cover it. This graph has small
    # separators; it is not a counterexample to Problem 31.
    bad_edges={edge(a,b) for a,b in itertools.combinations(range(4),2)}|{(3,4),(3,5),(4,5)}
    adj=adjacency(6,bad_edges);s=(0,1,2,4,5)
    d=[[len(shortest(adj,a,b))-1 for b in range(6)] for a in range(6)]
    assert all(d[a][b]+d[b][c] != d[a][c] for a,b,c in itertools.permutations(s,3))
    counters['unstructured_bag_control']=1


def main():
    if not __debug__:
        raise SystemExit('Run without -O: the verifier uses assertions.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    counters = dict(cases=0, bags=0, five_vertex_bags=0, fan_nonedge=0,
                    fan_triangle=0, leaf_nonedge=0, leaf_adjacent=0,
                    longest_path_edges=0, mass_checks=0)
    for patch, check_mass in fixtures():
        rows = construct(patch, counters)
        td = verify_rows(patch, rows, counters)
        if check_mass:mass_checks(patch, rows, td, counters)
    extra_checks(counters)
    if args.check:
        assert counters == json.loads(Path(__file__).with_name('expected.json').read_text())
    print(json.dumps(counters, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
