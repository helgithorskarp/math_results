"""Certify the maximum valid host order of every KG(7,2) induced17 core."""
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

CASES = [('star4', [0, 1, 2, 3], 105), ('path4', [0, 6, 11, 15], 1260), ('fork', [0, 1, 2, 15], 1260), ('cycle4', [0, 2, 6, 11], 105), ('paw', [0, 1, 2, 6], 420), ('triangle_edge', [0, 1, 6, 15], 210), ('star_edge', [0, 1, 2, 18], 420), ('path_edge', [0, 6, 11, 18], 1260), ('two_wedges', [0, 1, 15, 16], 630), ('wedge_two_edges', [0, 1, 15, 20], 315)]
POSITIONS = list(itertools.combinations(range(5), 2))


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def valid(rows):
    n = len(rows); full = (1 << n) - 1
    for u, v in itertools.combinations(range(n), 2):
        c = (rows[u] >> v) & 1
        pages = rows[u] & rows[v] if c else (
            full & ~(rows[u] | rows[v] | (1 << u) | (1 << v)))
        if pages.bit_count() > (3 if c else 6):
            return False
    return True


def augment(rows, patterns, colors):
    n = len(rows)
    result = [row | sum(1 << (n + j) for j, p in enumerate(patterns)
                        if (p >> u) & 1) for u, row in enumerate(rows)]
    new = list(patterns)
    assert len(colors) == len(new) * (len(new) - 1) // 2
    for (i, j), c in zip(itertools.combinations(range(len(new)), 2), colors):
        if c:
            new[i] |= 1 << (n + j); new[j] |= 1 << (n + i)
    return result + new


def domain_tree(rows):
    n = len(rows); full = (1 << n) - 1
    adj = [[] for _ in range(2 * n)]
    for u, v in itertools.combinations(range(n), 2):
        c = (rows[u] >> v) & 1
        pages = rows[u] & rows[v] if c else (
            full & ~(rows[u] | rows[v] | (1 << u) | (1 << v)))
        assert pages.bit_count() <= (3 if c else 6)
        if pages.bit_count() == (3 if c else 6):
            a, b = 2 * u + c, 2 * v + c
            adj[a ^ 1].append(b); adj[b ^ 1].append(a)
    red, blue = [], []
    for literal in range(2 * n):
        todo, seen = [literal], {literal}
        while todo:
            for other in adj[todo.pop()]:
                if other not in seen:
                    seen.add(other); todo.append(other)
        red.append(sum(1 << (x // 2) for x in seen if x % 2 == 0))
        blue.append(sum(1 << (x // 2) for x in seen if x % 2 == 1))
    counts = collections.Counter(); domain = []

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
        # Even literal means red; odd literal means blue. Keep both branches.
        return [u, visit(p | red[2 * u + 1], q | blue[2 * u + 1]),
                visit(p | red[2 * u], q | blue[2 * u])]

    tree = visit(0, 0); domain.sort()
    assert len(domain) == len(set(domain))
    return tree, domain, dict(counts)


def pair_valid(rows, p, q, c):
    """Check the new spine, all cross spines, and then every old spine."""
    n = len(rows); full = (1 << n) - 1
    if (p & q if c else full & ~(p | q)).bit_count() > (3 if c else 6):
        return False
    for u in range(n):
        a, b = (p >> u) & 1, (q >> u) & 1
        for pat, other, color in ((p, b, a), (q, a, b)):
            pages = (pat & rows[u] if color else (
                full & ~(pat | rows[u] | (1 << u)))).bit_count()
            if pages + int(color == c == other) > (3 if color else 6):
                return False
    for u, v in itertools.combinations(range(n), 2):
        color = (rows[u] >> v) & 1
        pages = (rows[u] & rows[v] if color else (
            full & ~(rows[u] | rows[v] | (1 << u) | (1 << v)))).bit_count()
        pages += int(((p >> u) & 1) == ((p >> v) & 1) == color)
        pages += int(((q >> u) & 1) == ((q >> v) & 1) == color)
        if pages > (3 if color else 6):
            return False
    return True


def saturated_spines(rows):
    n = len(rows); full = (1 << n) - 1
    red = [0] * n; blue = [0] * n
    for u, v in itertools.combinations(range(n), 2):
        c = (rows[u] >> v) & 1
        pages = rows[u] & rows[v] if c else full & ~(rows[u] | rows[v] | (1 << u) | (1 << v))
        assert pages.bit_count() <= (3 if c else 6)
        if pages.bit_count() == (3 if c else 6):
            target = red if c else blue
            target[u] |= 1 << v; target[v] |= 1 << u
    return red, blue


def addition_valid(rows, p, saturated):
    """All old spines keep their cap; then check every new incident spine."""
    full = (1 << len(rows)) - 1; q = full ^ p
    sat_red, sat_blue = saturated
    for u, row in enumerate(rows):
        if (p >> u) & 1:
            if sat_red[u] & p or (row & p).bit_count() > 3:
                return False
        else:
            if sat_blue[u] & q or (full & ~(row | p | (1 << u))).bit_count() > 6:
                return False
    return True


def prefix_graph(rows, domain, indices, mask):
    colors = [(mask >> POSITIONS.index(pair)) & 1
              for pair in itertools.combinations(range(len(indices)), 2)]
    return augment(rows, [domain[i] for i in indices], colors)


def save_case(cert, path):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(cert, separators=(',', ':')) + '\n')
    temporary.replace(path)


def run_case(name, deleted, base, path, resume):
    labels = [u for u in range(21) if u not in deleted]
    rows = [sum(1 << j for j, v in enumerate(labels) if (base[u] >> v) & 1) for u in labels]
    if resume and path.exists():
        cert = json.loads(path.read_text())
        assert cert['name'] == name and cert['deleted'] == deleted and cert['rows'] == rows
        assert 2 <= cert['complete_through_outside_vertices'] <= 5
        domain = cert['domain']; pairs = cert['pair_colors']
        levels = cert['levels']; counts = cert['counts']
        assert len(levels) == cert['complete_through_outside_vertices'] - 1
        assert len(counts) == cert['complete_through_outside_vertices'] - 2
    else:
        tree, domain, kernel_counts = domain_tree(rows)
        pairs = [[i, j, c] for i, p in enumerate(domain)
                 for j in range(i, len(domain)) for c in (0, 1)
                 if pair_valid(rows, p, domain[j], c)]
        assert all(i != j for i, j, c in pairs), 'Repeated pattern needs separate coverage'
        levels = [[(tuple([i, j]), c) for i, j, c in pairs]]; counts = []
        cert = {'format': 'kneser17-prefix-case-v1', 'complete_through_outside_vertices': 2,
                'name': name, 'deleted': deleted, 'rows': rows, 'tree': tree,
                'domain': domain, 'kernel_counts': kernel_counts, 'pair_colors': pairs,
                'levels': levels, 'counts': counts}
        save_case(cert, path)
        print('pairs_complete', name, 'domain', len(domain), 'pairs', len(pairs), flush=True)
    adjacency = [set() for _ in domain]; allowed = collections.defaultdict(list)
    for i, j, color in pairs:
        assert i != j
        adjacency[i].add(j); adjacency[j].add(i); allowed[i, j].append(color)
    for k in range(cert['complete_through_outside_vertices'], 5):
        next_level = []; tested = 0; candidate_indices = 0
        for indices, mask in levels[-1]:
            candidates = set.intersection(*(adjacency[i] for i in indices))
            partial = prefix_graph(rows, domain, indices, mask)
            saturated = saturated_spines(partial)
            for j in sorted(candidates):
                if j <= indices[-1]:
                    continue
                candidate_indices += 1
                for colors in itertools.product(*(allowed[i, j] for i in indices)):
                    tested += 1
                    p = domain[j] | sum(c << (17 + i) for i, c in enumerate(colors))
                    if addition_valid(partial, p, saturated):
                        next_mask = mask | sum(c << POSITIONS.index((i, k))
                                               for i, c in enumerate(colors))
                        next_level.append((tuple(indices) + (j,), next_mask))
        next_level.sort(); assert len(next_level) == len(set(next_level))
        levels.append(next_level)
        diagnostic = {'outside_vertices': k + 1,
                      'candidate_index_extensions': candidate_indices,
                      'joining_tests': tested, 'valid_prefixes': len(next_level)}
        counts.append(diagnostic)
        cert['complete_through_outside_vertices'] = k + 1
        save_case(cert, path)
        print('level_complete', name, diagnostic, flush=True)
    assert not levels[-1], 'A valid22 completion requires exact witness analysis'
    return cert


def summarize(cert, multiplicity):
    levels = cert['levels']
    return {'name': cert['name'], 'deleted': cert['deleted'],
        'labeled_core_count': multiplicity,
        'core_red_edges': sum(row.bit_count() for row in cert['rows']) // 2,
        'domain_size': len(cert['domain']), 'kernel_counts': cert['kernel_counts'],
        'domain_weights': dict(sorted(collections.Counter(str(p.bit_count()) for p in cert['domain']).items())),
        'colored_pairs': len(cert['pair_colors']), 'loops': 0, 'counts': cert['counts'],
        'domain_sha256': digest(cert['domain']), 'pairs_sha256': digest(cert['pair_colors']),
        'level_sha256': [digest(level) for level in levels]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--summary', type=Path)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args(); start = time.perf_counter()
    args.scratch.mkdir(parents=True, exist_ok=True)
    roots = list(itertools.combinations(range(7), 2))
    base = [sum(1 << j for j, f in enumerate(roots) if not set(e) & set(f)) for e in roots]
    assert valid(base) and all(row.bit_count() == 10 for row in base)
    red = [[u, v] for u, v in itertools.combinations(range(21), 2) if (base[u] >> v) & 1]
    baseline_hash = digest({'n': 21, 'red_edges': red})
    diagnostics = []
    for name, deleted, multiplicity in CASES:
        cert = run_case(name, deleted, base, args.scratch / ('case-' + name + '.json'), args.resume)
        diagnostic = summarize(cert, multiplicity); diagnostics.append(diagnostic)
        print('case_complete', name, 'seconds', time.perf_counter() - start, flush=True)
    summary = {'complete': True, 'representative_cores': 10, 'labeled_cores': 5985,
               'baseline_sha256': baseline_hash, 'cases': diagnostics}
    if args.summary:
        args.summary.write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    main()
