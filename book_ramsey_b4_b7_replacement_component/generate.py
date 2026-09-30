"""Generate exact trees and isomorphism witnesses for a five-class replacement component."""
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


def valid(rows):
    n = len(rows)
    full = (1 << n) - 1
    for u, v in itertools.combinations(range(n), 2):
        color = (rows[u] >> v) & 1
        common = rows[u] & rows[v] if color else (
            full & ~(rows[u] | rows[v] | (1 << u) | (1 << v)))
        if common.bit_count() > (3 if color else 6):
            return False
    return True


def augment(rows, patterns, colors):
    n = len(rows)
    result = [row | sum(1 << (n + j) for j, p in enumerate(patterns)
                        if (p >> u) & 1) for u, row in enumerate(rows)]
    new = list(patterns)
    for (i, j), color in zip(itertools.combinations(range(len(new)), 2), colors):
        if color:
            new[i] |= 1 << (n + j)
            new[j] |= 1 << (n + i)
    return result + new


def domain_tree(rows):
    n = len(rows)
    full = (1 << n) - 1
    adj = [[] for _ in range(2 * n)]
    for u, v in itertools.combinations(range(n), 2):
        color = (rows[u] >> v) & 1
        common = rows[u] & rows[v] if color else (
            full & ~(rows[u] | rows[v] | (1 << u) | (1 << v)))
        assert common.bit_count() <= (3 if color else 6)
        if common.bit_count() == (3 if color else 6):
            a, b = 2 * u + color, 2 * v + color
            adj[a ^ 1].append(b)
            adj[b ^ 1].append(a)
    red, blue = [], []
    for literal in range(2 * n):
        todo, seen = [literal], {literal}
        while todo:
            for other in adj[todo.pop()]:
                if other not in seen:
                    seen.add(other)
                    todo.append(other)
        red.append(sum(1 << (x // 2) for x in seen if x % 2 == 0))
        blue.append(sum(1 << (x // 2) for x in seen if x % 2 == 1))
    counts = collections.Counter()
    domain = []

    def visit(p, q):
        counts['tree_nodes'] += 1
        if p & q:
            return 'C'
        missing = full & ~(p | q)
        if not missing:
            counts['kernel_models'] += 1
            if valid(augment(rows, [p], [])):
                domain.append(p)
                return ['V', p]
            return 'I'
        u = (missing & -missing).bit_length() - 1
        # Even literal = red; odd literal = blue. Both branches are kept.
        return [u, visit(p | red[2 * u + 1], q | blue[2 * u + 1]),
                visit(p | red[2 * u], q | blue[2 * u])]

    tree = visit(0, 0)
    domain.sort()
    assert len(domain) == len(set(domain))
    return tree, domain, counts


def discrete_key(rows):
    """Only used to find witnesses; nondiscrete refinement fails loudly."""
    n = len(rows)
    colors = [row.bit_count() for row in rows]
    for _ in range(n):
        signatures = [(colors[u], tuple(sorted(colors[v] for v in range(n)
                                              if (rows[u] >> v) & 1))) for u in range(n)]
        palette = {s: i for i, s in enumerate(sorted(set(signatures)))}
        new = [palette[s] for s in signatures]
        if len(set(new)) == n:
            order = sorted(range(n), key=new.__getitem__)
            key = tuple((rows[u] >> v) & 1 for u, v in itertools.combinations(order, 2))
            return key, order
        assert len(set(new)) > len(set(colors)), 'Nondiscrete graph: no closure certificate'
        colors = new
    raise AssertionError('Incomplete refinement')


def generate(directory):
    data = json.loads((directory / 'h21.json').read_text())
    assert data['n'] == 21
    base = set(map(tuple, data['red_edges']))
    assert len(base) == len(data['red_edges']) == 93
    assert all(0 <= u < v < 21 for u, v in base)
    graph_hash = digest({'n': 21, 'red_edges': [list(e) for e in sorted(base)]})
    assert graph_hash == '189afcebf499016989b196498ccb3ed6431c7599f3ee5c638784f29be0d4eda0'
    manifest = json.loads((directory / 'templates.json').read_text())
    assert [t['name'] for t in manifest] == ['H', 'A', 'B', 'D', 'E']
    graphs, keys = {}, {}
    for template in manifest:
        edits = set(map(tuple, template['toggles']))
        assert len(edits) == len(template['toggles'])
        assert all(0 <= u < v < 21 for u, v in edits)
        edges = base ^ edits
        rows = [sum(1 << v for v in range(21) if tuple(sorted((u, v))) in edges)
                for u in range(21)]
        assert valid(rows)
        key, order = discrete_key(rows)
        assert key not in keys
        name = template['name']
        graphs[name] = rows
        keys[key] = (name, order)
    reps, diagnostics, projection = [], [], []
    for name, base_rows in graphs.items():
        cases, counts = [], collections.Counter()
        transitions, shapes = collections.Counter(), collections.Counter()
        for deleted in itertools.combinations(range(21), 2):
            labels = [u for u in range(21) if u not in deleted]
            rows = [sum(1 << j for j, v in enumerate(labels) if (base_rows[u] >> v) & 1)
                    for u in labels]
            tree, domain, local = domain_tree(rows)
            counts.update(local)
            pairs, witnesses = [], []
            adjacency = [set() for _ in domain]
            for i in range(len(domain)):
                for j in range(i, len(domain)):
                    for color in (0, 1):
                        completed = augment(rows, [domain[i], domain[j]], [color])
                        if not valid(completed):
                            continue
                        key, order = discrete_key(completed)
                        assert key in keys, 'A completion escapes the proposed component'
                        target, target_order = keys[key]
                        image = [None] * 21
                        for u, v in zip(order, target_order):
                            image[u] = v
                        pairs.append([i, j, color])
                        witnesses.append({'target': target, 'image': image})
                        transitions[target] += 1
                        adjacency[i].add(j); adjacency[j].add(i)
            assert all(i != j for i, j, _ in pairs), 'Compatible loop'
            assert not any(adjacency[i] & adjacency[j] for i, j, _ in pairs), 'Compatible triangle'
            shapes[str(tuple(sorted(len(a) for a in adjacency if a)))] += 1
            cases.append({'deleted': list(deleted), 'tree': tree, 'domain': domain,
                          'pair_colors': pairs, 'isomorphisms': witnesses})
        edge_list = [[u, v] for u, v in itertools.combinations(range(21), 2)
                     if (base_rows[u] >> v) & 1]
        gh = digest({'n': 21, 'red_edges': edge_list})
        reps.append({'name': name, 'graph_sha256': gh, 'cases': cases})
        diagnostics.append({'name': name, 'graph_sha256': gh,
                            'red_edges': len(edge_list), 'cohort_size': len(cases),
                            'counts': dict(counts),
                            'domain_count': sum(len(c['domain']) for c in cases),
                            'maximum_domain_size': max(len(c['domain']) for c in cases),
                            'pair_color_count': sum(len(c['pair_colors']) for c in cases),
                            'transitions': dict(sorted(transitions.items())),
                            'compatibility_shapes': dict(sorted(shapes.items()))})
        projection.append({'name': name, 'graph_sha256': gh, 'cases': [
            {'deleted': c['deleted'], 'domain': c['domain'], 'pair_colors': c['pair_colors'],
             'targets': [w['target'] for w in c['isomorphisms']]} for c in cases]})
    cert = {'format': 'book-replacement-component-v1', 'complete': True,
            'baseline_sha256': graph_hash, 'representatives': reps}
    summary = {'complete': True, 'representative_count': len(reps),
               'cohort_size': sum(len(r['cases']) for r in reps),
               'projection_sha256': digest(projection), 'representatives': diagnostics}
    return cert, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--summary', type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    certificate, summary = generate(Path(__file__).parent)
    args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    if args.summary:
        args.summary.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'temporary_certificate_bytes=', args.certificate.stat().st_size)


if __name__ == '__main__':
    main()
