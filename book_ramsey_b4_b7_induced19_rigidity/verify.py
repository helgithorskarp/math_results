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


def check(path, graph_path):
    data = json.loads(graph_path.read_text())
    cert = json.loads(path.read_text())
    assert data['n'] == 21
    base = set(map(tuple, data['red_edges']))
    assert len(base) == len(data['red_edges']) == 93
    assert valid(21, base)
    graph_hash = digest({'n': 21, 'red_edges': [list(e) for e in sorted(base)]})
    assert graph_hash == cert['graph_sha256'] == (
        '189afcebf499016989b196498ccb3ed6431c7599f3ee5c638784f29be0d4eda0')
    assert cert['format'] == 'book-core-domain-tree-v1' and cert['complete'] is True
    all_deleted = list(itertools.combinations(range(21), 2))
    assert [tuple(c['deleted']) for c in cert['cases']] == all_deleted
    variants = [base, base ^ {(6, 16), (10, 16)}, base ^ {(9, 16), (10, 16)}]
    assert all(valid(21, g) for g in variants)
    counts, shapes = collections.Counter(), collections.Counter()
    projection = []
    for case in cert['cases']:
        deleted = case['deleted']
        labels = [u for u in range(21) if u not in deleted]
        n = len(labels)
        core = {(i, j) for i, j in itertools.combinations(range(n), 2)
                if tuple(sorted((labels[i], labels[j]))) in base}
        assert valid(n, core)
        clauses = []
        # Derive all saturated spines from explicit color/page definitions.
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
                child = assignment.copy()
                child[u] = value
                visit(node[value + 1], child)

        visit(case['tree'], [-1] * n)
        domain.sort()
        assert len(set(domain)) == len(domain)
        assert domain == case['domain']
        pairs = [[i, j, color] for i in range(len(domain))
                 for j in range(i, len(domain)) for color in (0, 1)
                 if valid(n + 2, augment(core, n, [domain[i], domain[j]], [color]))]
        assert pairs == case['pair_colors'], 'Wrong or omitted pair-color result'
        assert all(i != j for i, j, color in pairs), 'A loop invalidates the clique bound'
        adjacency = [set() for _ in domain]
        for i, j, color in pairs:
            adjacency[i].add(j)
            adjacency[j].add(i)
        assert not any(adjacency[i] & adjacency[j] for i, j, color in pairs), (
            'A triangle invalidates the claimed order21 bound')
        shape = tuple(sorted(len(a) for a in adjacency if a))
        assert shape in ((1, 1), (1, 1, 1, 1), (1, 1, 1, 3))
        shapes[str(shape)] += 1
        predicted = set()
        for g in variants:
            if any(((u, v) in g) != ((u, v) in base)
                   for u, v in itertools.combinations(labels, 2)):
                continue
            patterns = [sum(1 << j for j, w in enumerate(labels)
                            if tuple(sorted((w, u))) in g) for u in deleted]
            i, j = sorted(domain.index(p) for p in patterns)
            predicted.add((i, j, int(tuple(deleted) in g)))
        assert predicted == set(map(tuple, pairs)), 'A completion outside H/A/B exists'
        projection.append({'deleted': deleted, 'domain': domain, 'pair_colors': pairs})
    return {'complete': True, 'cohort_size': len(projection),
            'graph_sha256': graph_hash, 'projection_sha256': digest(projection),
            'counts': dict(counts), 'domain_count': sum(len(c['domain']) for c in projection),
            'compatibility_shapes': dict(shapes),
            'maximum_host_order': 21, 'completions_outside_H_A_B': 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('h21.json'))
    args = parser.parse_args()
    start = time.perf_counter()
    result = check(args.certificate, args.input)
    expected = json.loads(Path(__file__).with_name('expected.json').read_text())
    for key in ('cohort_size', 'graph_sha256', 'projection_sha256', 'counts', 'domain_count'):
        assert result[key] == expected[key], key
    print(json.dumps(result, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    main()
