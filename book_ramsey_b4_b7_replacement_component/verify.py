"""Check domain-tree coverage by clause scanning and graphs by vertex sets.

This module does not import the generator or use its implication-closure code.
"""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import resource
import time

if not __debug__:
    raise SystemExit('Python assertions must be enabled')


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def valid(n, red):
    vertices = set(range(n))
    adj = [set() for _ in range(n)]
    for u, v in red:
        assert 0 <= u < v < n
        adj[u].add(v)
        adj[v].add(u)
    for u, v in itertools.combinations(range(n), 2):
        if (u, v) in red:
            if len(adj[u] & adj[v]) > 3:
                return False
        elif len((vertices - {u, v}) - (adj[u] | adj[v])) > 6:
            return False
    return True


def augment(red, n, patterns, colors):
    result = set(red)
    for j, mask in enumerate(patterns):
        assert type(mask) is int and 0 <= mask < 1 << n
        for u in range(n):
            if (mask >> u) & 1:
                result.add((u, n + j))
    assert len(colors) == len(patterns) * (len(patterns) - 1) // 2
    for (i, j), color in zip(itertools.combinations(range(len(patterns)), 2), colors):
        assert type(color) is int and color in (0, 1)
        if color:
            result.add((n + i, n + j))
    return result


def distinct_rigid(graphs):
    """Joint color refinement uses color-count vectors, not generator ordering."""
    names = list(graphs)
    adjacency = {name: [{v if u == i else u for u, v in edges if i in (u, v)}
                        for i in range(21)] for name, edges in graphs.items()}
    colors = {name: [len(a) for a in adjacency[name]] for name in names}
    for iteration in range(21):
        signatures = {name: [(colors[name][u], tuple(sorted(collections.Counter(
            colors[name][v] for v in adjacency[name][u]).items()))) for u in range(21)]
                      for name in names}
        palette = {s: i for i, s in enumerate(sorted({s for ss in signatures.values() for s in ss}))}
        colors = {name: [palette[s] for s in signatures[name]] for name in names}
        profiles = [tuple(sorted(colors[name])) for name in names]
        if all(len(set(colors[name])) == 21 for name in names) and len(set(profiles)) == len(names):
            return {'rounds': iteration + 1, 'joint_colors': len(palette),
                    'distinct_classes': len(names), 'all_automorphism_groups_trivial': True}
    raise AssertionError('Distinct rigid classes not certified by this invariant')


def check(path, directory):
    data = json.loads((directory / 'h21.json').read_text())
    cert = json.loads(path.read_text())
    assert data['n'] == 21
    base = set(map(tuple, data['red_edges']))
    assert len(base) == len(data['red_edges']) == 93 and valid(21, base)
    gh = digest({'n': 21, 'red_edges': [list(e) for e in sorted(base)]})
    assert gh == cert['baseline_sha256'] == '189afcebf499016989b196498ccb3ed6431c7599f3ee5c638784f29be0d4eda0'
    assert cert['format'] == 'book-replacement-component-v1' and cert['complete'] is True
    manifest = json.loads((directory / 'templates.json').read_text())
    names = [t['name'] for t in manifest]
    assert names == ['H', 'A', 'B', 'D', 'E']
    graphs = {}
    for t in manifest:
        edits = set(map(tuple, t['toggles']))
        assert len(edits) == len(t['toggles'])
        assert all(0 <= u < v < 21 for u, v in edits)
        graphs[t['name']] = base ^ edits
        assert valid(21, graphs[t['name']])
    invariant = distinct_rigid(graphs)
    assert [r['name'] for r in cert['representatives']] == names
    projection, diagnostics = [], []
    all_deleted = list(itertools.combinations(range(21), 2))
    for representative in cert['representatives']:
        name = representative['name']
        graph = graphs[name]
        graph_hash = digest({'n': 21, 'red_edges': [list(e) for e in sorted(graph)]})
        assert representative['graph_sha256'] == graph_hash
        assert [tuple(c['deleted']) for c in representative['cases']] == all_deleted
        counts, shapes, transitions = collections.Counter(), collections.Counter(), collections.Counter()
        local_projection = []
        for case in representative['cases']:
            deleted = case['deleted']
            labels = [u for u in range(21) if u not in deleted]
            n = len(labels)
            core = {(i, j) for i, j in itertools.combinations(range(n), 2)
                    if (labels[i], labels[j]) in graph}
            assert valid(n, core)
            clauses = []
            for u, v in itertools.combinations(range(n), 2):
                color = int((u, v) in core)
                pages = [w for w in range(n) if w not in (u, v)
                         and int(tuple(sorted((u, w))) in core) == color
                         and int(tuple(sorted((v, w))) in core) == color]
                if len(pages) == (3 if color else 6):
                    clauses.append((u, v, color))

            def propagate(assignment):
                while True:
                    changed = False
                    for u, v, color in clauses:
                        if assignment[u] == color and assignment[v] == color:
                            return None
                        for a, b in ((u, v), (v, u)):
                            if assignment[a] == color and assignment[b] == -1:
                                assignment[b] = 1 - color
                                changed = True
                    if not changed:
                        return assignment

            domain = []

            def visit(node, assignment):
                counts['tree_nodes'] += 1
                assignment = propagate(assignment)
                if assignment is None:
                    assert node == 'C', 'Unjustified conflict or wrong tree state'
                    return
                if -1 not in assignment:
                    counts['kernel_models'] += 1
                    mask = sum(1 << u for u, c in enumerate(assignment) if c == 1)
                    good = valid(n + 1, augment(core, n, [mask], []))
                    if good:
                        assert node == ['V', mask], 'Missing or wrong valid pattern'
                        domain.append(mask)
                    else:
                        assert node == 'I', 'Invalid pattern was accepted'
                    return
                assert type(node) is list and len(node) == 3
                u = node[0]
                assert type(u) is int and 0 <= u < n and assignment[u] == -1
                for value in (0, 1):
                    child = assignment.copy(); child[u] = value
                    visit(node[value + 1], child)

            visit(case['tree'], [-1] * n)
            domain.sort()
            assert len(set(domain)) == len(domain) and domain == case['domain']
            pairs = [[i, j, c] for i in range(len(domain))
                     for j in range(i, len(domain)) for c in (0, 1)
                     if valid(n + 2, augment(core, n, [domain[i], domain[j]], [c]))]
            assert pairs == case['pair_colors'], 'Wrong or omitted pair-color result'
            assert all(i != j for i, j, c in pairs), 'A loop invalidates the host bound'
            adjacency = [set() for _ in domain]
            for i, j, _ in pairs:
                adjacency[i].add(j); adjacency[j].add(i)
            assert not any(adjacency[i] & adjacency[j] for i, j, _ in pairs), 'A triangle invalidates the host bound'
            shapes[str(tuple(sorted(len(a) for a in adjacency if a)))] += 1
            witnesses = case['isomorphisms']
            assert len(witnesses) == len(pairs)
            for (i, j, color), witness in zip(pairs, witnesses):
                target, image = witness['target'], witness['image']
                assert target in graphs
                assert len(image) == 21 and all(type(u) is int for u in image)
                assert sorted(image) == list(range(21)), 'Nonbijective isomorphism'
                completed = augment(core, n, [domain[i], domain[j]], [color])
                mapped = {tuple(sorted((image[u], image[v]))) for u, v in completed}
                assert mapped == graphs[target], 'False isomorphism witness'
                transitions[target] += 1
            local_projection.append({'deleted': deleted, 'domain': domain, 'pair_colors': pairs,
                                     'targets': [w['target'] for w in witnesses]})
        projection.append({'name': name, 'graph_sha256': graph_hash, 'cases': local_projection})
        diagnostics.append({'name': name, 'graph_sha256': graph_hash, 'red_edges': len(graph),
                            'cohort_size': len(local_projection), 'counts': dict(counts),
                            'domain_count': sum(len(c['domain']) for c in local_projection),
                            'maximum_domain_size': max(len(c['domain']) for c in local_projection),
                            'pair_color_count': sum(len(c['pair_colors']) for c in local_projection),
                            'transitions': dict(sorted(transitions.items())),
                            'compatibility_shapes': dict(sorted(shapes.items()))})
    for a, b, cover in [('H', 'A', {16}), ('H', 'B', {16}),
                         ('B', 'D', {3, 19}), ('D', 'E', {0})]:
        assert all(cover & set(e) for e in graphs[a] ^ graphs[b])
    result = {'complete': True, 'representative_count': len(graphs),
              'cohort_size': sum(x['cohort_size'] for x in diagnostics),
              'projection_sha256': digest(projection), 'representatives': diagnostics}
    return result, invariant


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args()
    directory = Path(__file__).parent
    start = time.perf_counter()
    result, invariant = check(args.certificate, directory)
    expected = json.loads((directory / 'expected.json').read_text())
    assert result == expected, 'Compact signature mismatch'
    print(json.dumps({'checked': result, 'invariant': invariant}, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    main()
