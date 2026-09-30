"""Generate exact domain decision trees for all 210 primary induced19 cores."""
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


def generate(path):
    data = json.loads(path.read_text())
    assert data['n'] == 21
    base = set(map(tuple, data['red_edges']))
    assert len(base) == len(data['red_edges']) == 93
    assert all(0 <= u < v < 21 for u, v in base)
    base_rows = [sum(1 << v for v in range(21) if tuple(sorted((u, v))) in base)
                 for u in range(21)]
    assert valid(base_rows)
    cases, counts = [], collections.Counter()
    for deleted in itertools.combinations(range(21), 2):
        labels = [u for u in range(21) if u not in deleted]
        rows = [sum(1 << j for j, v in enumerate(labels)
                    if tuple(sorted((u, v))) in base) for u in labels]
        tree, domain, local = domain_tree(rows)
        counts.update(local)
        pairs = [[i, j, c] for i in range(len(domain))
                 for j in range(i, len(domain)) for c in (0, 1)
                 if valid(augment(rows, [domain[i], domain[j]], [c]))]
        cases.append({'deleted': list(deleted), 'tree': tree,
                      'domain': domain, 'pair_colors': pairs})
    projection = [{'deleted': c['deleted'], 'domain': c['domain'],
                   'pair_colors': c['pair_colors']} for c in cases]
    graph_hash = digest({'n': 21, 'red_edges': [list(e) for e in sorted(base)]})
    certificate = {'format': 'book-core-domain-tree-v1', 'complete': True,
                   'graph_sha256': graph_hash, 'cases': cases}
    summary = {'complete': True, 'cohort_size': len(cases),
               'graph_sha256': graph_hash, 'projection_sha256': digest(projection),
               'counts': dict(counts),
               'domain_count': sum(len(c['domain']) for c in cases),
               'domain_size_histogram': dict(sorted(collections.Counter(
                   len(c['domain']) for c in cases).items())),
               'pair_color_histogram': dict(sorted(collections.Counter(
                   len(c['pair_colors']) for c in cases).items()))}
    return certificate, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).with_name('h21.json'))
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--summary', type=Path)
    args = parser.parse_args()
    start = time.perf_counter()
    certificate, summary = generate(args.input)
    args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    if args.summary:
        args.summary.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'temporary_certificate_bytes=', args.certificate.stat().st_size)


if __name__ == '__main__':
    main()
