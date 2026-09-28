"""Check the finite-core proof certificate without importing its generator.

This enumerates set partitions, whereas the generator enumerates cut sets;
it uses mutable-set elimination, explicit tree-decomposition validation and
Floyd--Warshall, rather than the generator's bitmask reachability search.
"""
import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def partitions(length):
    def visit(word):
        if len(word) == length:
            classes = max(word) + 1
            changes = sum(word[i] != word[(i + 1) % length] for i in range(length))
            if classes == 1 or changes == classes:
                yield tuple(word)
        else:
            for value in range(max(word) + 2):
                yield from visit(word + [value])
    yield from visit([0])


def edges_of_cycle(k, labels):
    ans = set()
    for a, b in zip(labels, labels[1:] + labels[:1]):
        if a != b:
            ans.add(tuple(sorted((k + 1 + a, k + 1 + b))))
    return sorted(ans)


def core(k, labels, keep):
    m = max(labels) + 1
    n = 1 + k + m
    cycle = edges_of_cycle(k, labels)
    actual = set(itertools.combinations(range(1, k + 1), 2))
    actual.update((0, y) for y in range(k + 1, n))
    for x in range(1, k + 1):
        for b in labels[2 * x - 2:2 * x]:
            actual.add((x, k + 1 + b))
    actual.update(e for index, e in enumerate(cycle) if (keep >> index) & 1)
    filled = actual | set(cycle) | {(0, x) for x in range(1, k + 1)}
    return n, actual, filled, cycle


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        adj[u].add(v)
        adj[v].add(u)
    return adj


def distances(n, edges):
    dist = [[0 if i == j else n + 1 for j in range(n)] for i in range(n)]
    for u, v in edges:
        dist[u][v] = dist[v][u] = 1
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


def decomposition(n, filled, order):
    assert sorted(order) == list(range(n)), 'order is not a permutation'
    adj = adjacency(n, filled)
    alive = set(range(n))
    bags = []
    position = {v: i for i, v in enumerate(order)}
    tree = [set() for _ in order]
    for i, v in enumerate(order):
        later = adj[v] & alive
        bags.append(later | {v})
        if later:
            parent = min(position[w] for w in later)
            assert parent > i
            tree[i].add(parent)
            tree[parent].add(i)
        for a, b in itertools.combinations(later, 2):
            adj[a].add(b)
            adj[b].add(a)
        alive.remove(v)
    # All core and expanded-patch filled graphs are connected.
    assert sum(map(len, tree)) == 2 * (n - 1)
    return bags, tree


def check_tree(n, graph_edges, bags, tree):
    assert len(bags) == len(tree) and bags
    assert sum(map(len, tree)) == 2 * (len(tree) - 1)
    reached, todo = {0}, [0]
    while todo:
        for j in tree[todo.pop()]:
            if j not in reached:
                reached.add(j)
                todo.append(j)
    assert len(reached) == len(tree)
    for u, v in graph_edges:
        assert any(u in bag and v in bag for bag in bags), 'uncovered edge'
    for v in range(n):
        nodes = {i for i, bag in enumerate(bags) if v in bag}
        assert nodes, 'uncovered vertex'
        found = {next(iter(nodes))}
        todo = list(found)
        while todo:
            for j in tree[todo.pop()] & nodes:
                if j not in found:
                    found.add(j)
                    todo.append(j)
        assert found == nodes, 'disconnected occurrence set'


def check_covers(n, actual, bags, covers):
    assert len(bags) == len(covers)
    dist = distances(n, actual)
    for bag, pair in zip(bags, covers):
        assert 1 <= len(pair) <= 2
        union = set()
        for path in pair:
            assert 1 <= len(path) <= 3
            assert len(path) == len(set(path))
            assert all(0 <= v < n for v in path)
            for u, v in zip(path, path[1:]):
                assert tuple(sorted((u, v))) in actual, 'virtual metric edge'
            assert dist[path[0]][path[-1]] == len(path) - 1, 'nongeodesic path'
            union.update(path)
        assert bag <= union, 'bag is not covered'


def check_record(rec):
    k, labels, keep = rec['k'], tuple(rec['labels']), rec['keep']
    n, actual, filled, cycle = core(k, labels, keep)
    bags, tree = decomposition(n, filled, rec['order'])
    check_tree(n, filled, bags, tree)
    check_covers(n, actual, bags, rec['covers'])
    assert max(map(len, bags)) <= 6
    for a, b in cycle:
        assert any({0, a, b} <= bag for bag in bags), 'missing interface bag'
    for y in range(k + 1, n):
        assert any({0, y} <= bag for bag in bags)
    return bags, tree


def audit(records):
    expected = set()
    counts = {}
    for k in range(1, 4):
        words = list(partitions(2 * k))
        counts[str(k)] = {'patterns': len(words), 'cases': 0}
        for labels in words:
            for keep in range(1 << len(edges_of_cycle(k, labels))):
                expected.add((k, labels, keep))
                counts[str(k)]['cases'] += 1
    observed = [(r['k'], tuple(r['labels']), r['keep']) for r in records]
    assert len(observed) == len(set(observed)), 'duplicate case'
    assert set(observed) == expected, 'incomplete or extraneous coverage'
    sizes = Counter()
    for rec in records:
        bags, _ = check_record(rec)
        sizes.update(map(len, bags))
    return {'cases_by_clique_order': counts, 'total_cases': len(records),
            'bag_count': sum(sizes.values()),
            'bag_size_histogram': dict(sorted(sizes.items()))}


def expanded_patch(records, lengths, transitions):
    """Three fans, all six extreme spokes distinct; optional transition edges."""
    actual = {(1, 2), (1, 3), (2, 3)}
    cycle = []
    order = []
    covers = []
    next_vertex = 10
    for i, length in enumerate(lengths):
        a, b, x = 4 + 2 * i, 5 + 2 * i, 1 + i
        middle = list(range(next_vertex, next_vertex + length))
        next_vertex += length
        fan = [a] + middle + [b]
        for v in fan:
            actual.add((0, v))
            actual.add((x, v))
        for u, v in zip(fan, fan[1:]):
            actual.add(tuple(sorted((u, v))))
            cycle.append(tuple(sorted((u, v))))
        for index, v in enumerate(middle):
            other = fan[index + 2]
            endpoint_edge = tuple(sorted((a, other)))
            # Such an edge is absent after at least one fan vertex intervenes.
            pair = [[0, v, x], [a, other] if endpoint_edge in actual else [a, 0, other]]
            order.append(v)
            covers.append(pair)
        next_a = 4 + (2 * (i + 1)) % 6
        edge = tuple(sorted((b, next_a)))
        cycle.append(edge)
        if transitions[i]:
            actual.add(edge)
    labels = (0, 1, 2, 3, 4, 5)
    small_cycle = edges_of_cycle(3, labels)
    keep = sum(1 << i for i, e in enumerate(small_cycle) if e in actual)
    rec = next(r for r in records if r['k'] == 3 and tuple(r['labels']) == labels
               and r['keep'] == keep)
    order.extend(rec['order'])
    covers.extend(copy.deepcopy(rec['covers']))
    filled = actual | set(cycle) | {(0, x) for x in (1, 2, 3)}
    bags, tree = decomposition(next_vertex, filled, order)
    check_tree(next_vertex, filled, bags, tree)
    check_covers(next_vertex, actual, bags, covers)
    return next_vertex, actual, bags, tree, covers


def glue_patches(left, right):
    """Glue facial triangles r-5-6; these edges are real in both fixtures."""
    n, edges, bags, tree, covers = copy.deepcopy(left)
    rn, re, rb, rt, rc = right
    shared = {0, 5, 6}
    assert {(0, 5), (0, 6), (5, 6)} <= edges & re
    rename = {v: v for v in shared}
    for v in range(rn):
        if v not in shared:
            rename[v] = n
            n += 1
    offset = len(bags)
    bags.extend({rename[v] for v in b} for b in rb)
    tree.extend({offset + j for j in neighbours} for neighbours in rt)
    covers.extend([[rename[v] for v in p] for p in pair] for pair in rc)
    edges.update(tuple(sorted((rename[u], rename[v]))) for u, v in re)
    a = next(i for i, b in enumerate(bags[:offset]) if shared <= b)
    b = next(offset + i for i, b in enumerate(rb) if shared <= b)
    tree[a].add(b)
    tree[b].add(a)
    # Add an inactive vertex inside the left clique triangle, making a K4.
    bag = {1, 2, 3, n}
    at = next(i for i, b in enumerate(bags) if {1, 2, 3} <= b)
    leaf = len(bags)
    bags.append(bag)
    tree.append({at})
    tree[at].add(leaf)
    covers.append([[n, 1], [2, 3]])
    edges.update((x, n) for x in (1, 2, 3))
    n += 1
    check_tree(n, edges, bags, tree)
    check_covers(n, edges, bags, covers)
    return n, edges, bags, tree, covers


def mass_checks(fixture):
    n, edges, bags, tree, covers = fixture
    masses = [[0] * n, [1] * n, [(v * v + 3 * v + 1) % 17 for v in range(n)]]
    masses += [[int(v == at) for v in range(n)] for at in range(n)]
    assignment = [next(i for i, bag in enumerate(bags) if v in bag) for v in range(n)]
    for mass in masses:
        total = sum(mass)
        node_mass = [0] * len(bags)
        for v, value in enumerate(mass):
            node_mass[assignment[v]] += value
        for candidate in range(len(bags)):
            good = True
            for first in tree[candidate]:
                seen, todo = {candidate, first}, [first]
                value = 0
                while todo:
                    at = todo.pop()
                    value += node_mass[at]
                    for nxt in tree[at] - seen:
                        seen.add(nxt)
                        todo.append(nxt)
                if 2 * value > total:
                    good = False
                    break
            if good:
                break
        assert good, 'weighted tree has no centroid'
        removed = set().union(*map(set, covers[candidate]))
        parent = list(range(n))
        def find(v):
            while parent[v] != v:
                parent[v] = parent[parent[v]]
                v = parent[v]
            return v
        for u, v in edges:
            if u not in removed and v not in removed:
                parent[find(u)] = find(v)
        residual = Counter()
        for v in range(n):
            if v not in removed:
                residual[find(v)] += mass[v]
        assert 2 * max(residual.values(), default=0) <= total
    return len(masses)


def width_four_obstruction():
    """Exact order-13 example: all width-four elimination prefixes are found."""
    n = 13
    edges = {(0, v) for v in range(1, 10)}
    edges.update(tuple(sorted((v, v % 9 + 1))) for v in range(1, 10))
    edges.update({(10, 11), (10, 12), (11, 12)})
    for x, boundary in [(10, (9, 1, 2, 3)), (11, (3, 4, 5, 6)),
                        (12, (6, 7, 8, 9))]:
        edges.update(tuple(sorted((x, b))) for b in boundary)
    original = adjacency(n, edges)
    seen = {frozenset()}
    todo = [frozenset()]
    while todo:
        eliminated = todo.pop()
        adj = [set(a) for a in original]
        alive = set(range(n))
        # Fill after eliminating a set is independent of its internal order.
        for v in sorted(eliminated):
            neighbours = adj[v] & alive
            for a, b in itertools.combinations(neighbours, 2):
                adj[a].add(b)
                adj[b].add(a)
            alive.remove(v)
        for v in alive:
            if len(adj[v] & alive) <= 4:
                nxt = eliminated | {v}
                if nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
    fan = {1, 2, 4, 5, 7, 8}
    expected = {frozenset(s) for k in range(7) for s in itertools.combinations(fan, k)}
    assert seen == expected
    assert frozenset(range(n)) not in seen
    return {'vertices': n, 'edges': len(edges), 'width_four_prefix_sets': len(seen),
            'treewidth_at_least': 5}


def invalid_controls(records):
    count = 0
    def reject(action):
        nonlocal count
        try:
            action()
        except (AssertionError, IndexError):
            count += 1
        else:
            raise AssertionError('invalid control was accepted')
    reject(lambda: audit(records[:-1]))
    reject(lambda: audit(records + records[:1]))
    bad = copy.deepcopy(records[0])
    bad['order'][0] = bad['order'][1]
    reject(lambda: check_record(bad))
    bad = copy.deepcopy(records[0])
    bad['covers'][0][0] = [0, 1]
    reject(lambda: check_record(bad))
    bad = copy.deepcopy(records[0])
    bad['covers'][0] = [[0], [0]]
    reject(lambda: check_record(bad))
    bad = copy.deepcopy(records[0])
    bad['covers'][0][0] = [0, 2, 0]
    reject(lambda: check_record(bad))
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = (HERE / 'certificate.jsonl').read_bytes()
    records = [json.loads(line) for line in data.splitlines()]
    result = audit(records)
    fixtures = [expanded_patch(records, lengths, transitions)
                for lengths, transitions in [((1, 2, 3), (1, 1, 1)),
                                              ((7, 8, 9), (0, 0, 0)),
                                              ((0, 5, 11), (1, 0, 1)),
                                              ((2, 4, 6), (1, 1, 0))]]
    fixtures.append(glue_patches(fixtures[0], fixtures[3]))
    result['expanded_fixtures'] = len(fixtures)
    result['expanded_bag_covers'] = sum(len(x[2]) for x in fixtures)
    result['mass_assignments'] = sum(mass_checks(f) for f in fixtures)
    result['width_four_obstruction'] = width_four_obstruction()
    result['invalid_controls_rejected'] = invalid_controls(records)
    result['certificate_sha256'] = hashlib.sha256(data).hexdigest()
    result['status'] = 'PASS'
    # JSON round-trip also makes histogram keys agree with the saved JSON file.
    result = json.loads(json.dumps(result))
    if args.check:
        assert result == json.loads((HERE / 'expected.json').read_text())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
