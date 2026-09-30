"""Independent set-based domain, compatibility, symmetry and book checker.

No generator import, implication-reachability routine, or generator pair test.
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

CASES = [('star4', (0, 1, 2, 3), 105), ('path4', (0, 6, 11, 15), 1260), ('fork', (0, 1, 2, 15), 1260), ('cycle4', (0, 2, 6, 11), 105), ('paw', (0, 1, 2, 6), 420), ('triangle_edge', (0, 1, 6, 15), 210), ('star_edge', (0, 1, 2, 18), 420), ('path_edge', (0, 6, 11, 18), 1260), ('two_wedges', (0, 1, 15, 16), 630), ('wedge_two_edges', (0, 1, 15, 20), 315)]
POSITIONS = list(itertools.combinations(range(5), 2))


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def valid(n, red):
    vertices = set(range(n)); adj = [set() for _ in range(n)]
    for u, v in red:
        assert 0 <= u < v < n
        adj[u].add(v); adj[v].add(u)
    for u, v in itertools.combinations(range(n), 2):
        if (u, v) in red:
            if len(adj[u] & adj[v]) > 3:
                return False
        elif len((vertices - {u, v}) - (adj[u] | adj[v])) > 6:
            return False
    return True


def augment(core, n, patterns, colors):
    red = set(core)
    for j, p in enumerate(patterns):
        assert type(p) is int and 0 <= p < 1 << n
        red.update((u, n + j) for u in range(n) if (p >> u) & 1)
    assert len(colors) == len(patterns) * (len(patterns) - 1) // 2
    for (i, j), c in zip(itertools.combinations(range(len(patterns)), 2), colors):
        assert type(c) is int and c in (0, 1)
        if c:
            red.add((n + i, n + j))
    return red


def root_actions(roots):
    """Enumerate all5040 explicit actions, check seed colors, and all core orbits."""
    index = {edge: i for i, edge in enumerate(roots)}
    actions = []; orbits = [set() for _ in CASES]
    for sigma in itertools.permutations(range(7)):
        image = [index[frozenset(sigma[x] for x in edge)] for edge in roots]
        assert sorted(image) == list(range(21))
        # Disjointness is preserved directly because sigma is a point bijection.
        actions.append(image)
        for cohort, (_, deleted, _) in zip(orbits, CASES):
            cohort.add(tuple(sorted(image[u] for u in deleted)))
    assert len(actions) == 5040 and len({tuple(a) for a in actions}) == 5040
    assert [len(o) for o in orbits] == [c[2] for c in CASES]
    assert sum(map(len, orbits)) == len(set().union(*orbits)) == 5985
    assert set().union(*orbits) == set(itertools.combinations(range(21), 4))
    return actions


def check_domain(tree, declared, core):
    n = 17; vertices = set(range(n)); adj = [set() for _ in range(n)]
    for u, v in core:
        adj[u].add(v); adj[v].add(u)
    clauses = []
    for u, v in itertools.combinations(range(n), 2):
        c = int((u, v) in core)
        pages = adj[u] & adj[v] if c else (vertices - {u, v}) - (adj[u] | adj[v])
        assert len(pages) <= (3 if c else 6)
        if len(pages) == (3 if c else 6):
            clauses.append((u, v, c))
    domain = []; counts = collections.Counter()

    def visit(node, assignment):
        counts['tree_nodes'] += 1
        while True:
            changed = False
            for u, v, c in clauses:
                if assignment[u] == c == assignment[v]:
                    assert node == 'C', 'Unjustified conflict or wrong tree state'
                    return
                for a, b in ((u, v), (v, u)):
                    if assignment[a] == c and assignment[b] == -1:
                        assignment[b] = 1 - c; changed = True
            if not changed:
                break
        if -1 not in assignment:
            counts['kernel_models'] += 1
            p = sum(1 << u for u, c in enumerate(assignment) if c == 1)
            if valid(n + 1, augment(core, n, [p], [])):
                assert node == ['V', p], 'Wrong valid pattern'
                domain.append(p)
            else:
                assert node == 'I', 'Invalid pattern was accepted'
            return
        assert type(node) is list and len(node) == 3, 'Unjustified conflict or split'
        u = node[0]
        assert type(u) is int and 0 <= u < n and assignment[u] == -1
        for c in (0, 1):
            child = assignment.copy(); child[u] = c
            visit(node[c + 1], child)

    visit(tree, [-1] * n); domain.sort()
    assert all(type(p) is int for p in declared)
    assert len(domain) == len(set(domain)) and domain == declared, 'Domain mismatch'
    return domain, dict(counts)


def compatible_pairs(core, domain):
    """Use intersections of sets of dangerous spines, rather than full bit graphs."""
    n = 17; vertices = set(range(n)); red = [set() for _ in range(n)]
    for u, v in core:
        red[u].add(v); red[v].add(u)
    blue = [vertices - {u} - red[u] for u in range(n)]
    almost_full = []
    for u, v in itertools.combinations(range(n), 2):
        c = int((u, v) in core)
        pages = len(red[u] & red[v]) if c else len(blue[u] & blue[v])
        if pages == (2 if c else 5):
            almost_full.append((u, v, c))
    reds = [{u for u in range(n) if (p >> u) & 1} for p in domain]
    blues = [vertices - r for r in reds]
    danger = [{(u, v) for u, v, c in almost_full if {u, v} <= (r if c else b)}
              for r, b in zip(reds, blues)]
    sat_red = [{u for u in r if len(red[u] & r) == 3} for r in reds]
    sat_blue = [{u for u in b if len(blue[u] & b) == 6} for b in blues]
    result = []
    for i in range(len(domain)):
        for j in range(i, len(domain)):
            if danger[i] & danger[j]:
                continue
            if (len(blues[i] & blues[j]) <= 6 and
                    not sat_blue[i] & blues[j] and not sat_blue[j] & blues[i]):
                result.append([i, j, 0])
            if (len(reds[i] & reds[j]) <= 3 and
                    not sat_red[i] & reds[j] and not sat_red[j] & reds[i]):
                result.append([i, j, 1])
    return result


def check_case(path, expected_name, expected_deleted):
    start = time.perf_counter()
    cert = json.loads(path.read_text())
    assert cert['complete_through_outside_vertices'] == 5
    assert cert['format'] == 'kneser17-prefix-case-v1'
    assert cert['name'] == expected_name and cert['deleted'] == list(expected_deleted)
    roots = [frozenset(p) for p in itertools.combinations(range(7), 2)]
    labels = [u for u in range(21) if u not in cert['deleted']]
    core = {(u, v) for u, v in itertools.combinations(range(17), 2)
            if roots[labels[u]].isdisjoint(roots[labels[v]])}
    rows = [sum(1 << v for v in range(17) if tuple(sorted((u, v))) in core)
            for u in range(17)]
    assert cert['rows'] == rows
    domain, counts = check_domain(cert['tree'], cert['domain'], core)
    pairs = compatible_pairs(core, domain)
    assert counts == cert['kernel_counts']
    assert pairs == cert['pair_colors'] and all(i != j for i, j, c in pairs)
    allowed = collections.defaultdict(set)
    neighborhoods = [set() for _ in domain]
    for i, j, c in pairs:
        allowed[i, j].add(c); neighborhoods[i].add(j); neighborhoods[j].add(i)
    previous = [(tuple([i, j]), c) for i, j, c in pairs]
    assert [[list(indices), mask] for indices, mask in previous] == cert['levels'][0]
    for k in range(2, 5):
        following = []; tests = 0; candidate_indices = 0
        for indices, mask in previous:
            choices = set(range(indices[-1] + 1, len(domain)))
            for i in indices:
                choices.intersection_update(neighborhoods[i])
            for j in sorted(choices):
                candidate_indices += 1
                new_indices = indices + (j,)
                for colors in itertools.product(*(sorted(allowed[i, j]) for i in indices)):
                    tests += 1
                    new_mask = mask + sum(c << POSITIONS.index((i, k))
                                          for i, c in enumerate(colors))
                    full_colors = [(new_mask >> POSITIONS.index(pair)) & 1
                                   for pair in itertools.combinations(range(k + 1), 2)]
                    graph = augment(core, 17, [domain[i] for i in new_indices], full_colors)
                    if valid(18 + k, graph):
                        following.append((new_indices, new_mask))
        following.sort()
        assert len(following) == len(set(following))
        diagnostic = {'outside_vertices': k + 1,
            'candidate_index_extensions': candidate_indices,
            'joining_tests': tests, 'valid_prefixes': len(following)}
        assert diagnostic == cert['counts'][k - 2]
        assert [[list(indices), mask] for indices, mask in following] == cert['levels'][k - 1]
        print(cert['name'], 'checked', diagnostic, 'seconds', time.perf_counter()-start, flush=True)
        previous = following
    assert not previous, 'Nonempty valid22 completion list'
    return summarize(cert)


def summarize(cert):
    levels = cert['levels']
    multiplicity = next(m for name, deleted, m in CASES if name == cert['name'])
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
    parser.add_argument('scratch', type=Path)
    parser.add_argument('--resume', action='store_true', help='Reuse checked receipts only for identical source and case bytes')
    args = parser.parse_args(); start = time.perf_counter()
    roots = [frozenset(p) for p in itertools.combinations(range(7), 2)]
    base = {(u, v) for u, v in itertools.combinations(range(21), 2) if roots[u].isdisjoint(roots[v])}
    assert len(base) == 105 and valid(21, base)
    vertices = set(range(21))
    red = [{v for v in vertices if tuple(sorted((u, v))) in base} for u in vertices]
    assert all(len(row) == 10 for row in red)
    for u, v in itertools.combinations(range(21), 2):
        if (u, v) in base:
            assert len(red[u] & red[v]) == 3
        else:
            assert len((vertices - {u, v}) - (red[u] | red[v])) == 5
    baseline_hash = digest({'n': 21, 'red_edges': [list(e) for e in sorted(base)]})
    root_actions(roots)
    expected = json.loads((Path(__file__).parent / 'expected.json').read_text())
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    diagnostics = []
    for position, (name, deleted, multiplicity) in enumerate(CASES):
        path = args.scratch / ('case-' + name + '.json')
        receipt_path = args.scratch / ('verified-' + name + '.json')
        case_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if args.resume and receipt_path.exists():
            receipt = json.loads(receipt_path.read_text())
            assert receipt['checked'] is True
            assert receipt['checker_sha256'] == source_hash and receipt['case_sha256'] == case_hash
            diagnostic = receipt['diagnostic']
        else:
            diagnostic = check_case(path, name, deleted)
        assert diagnostic == expected['cases'][position], 'Per-case compact signature mismatch'
        receipt = {'checked': True, 'checker_sha256': source_hash,
                   'case_sha256': case_hash, 'diagnostic': diagnostic}
        temporary = receipt_path.with_suffix('.tmp')
        temporary.write_text(json.dumps(receipt, indent=2) + '\n')
        temporary.replace(receipt_path)
        diagnostics.append(diagnostic)
        print('case_verified', name, 'seconds', time.perf_counter()-start, flush=True)
    result = {'complete': True, 'representative_cores': 10, 'labeled_cores': 5985,
              'baseline_sha256': baseline_hash, 'cases': diagnostics}
    assert result == expected, 'Compact signature mismatch'
    print(json.dumps({'checked': result}, indent=2))
    print('seconds=', time.perf_counter()-start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    main()
