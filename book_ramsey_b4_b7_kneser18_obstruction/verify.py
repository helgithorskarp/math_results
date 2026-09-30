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

CASES = [('triangle', (0, 1, 6), 35), ('star', (0, 1, 2), 140),
         ('path', (0, 6, 11), 420), ('wedge_edge', (0, 1, 15), 630),
         ('matching', (0, 11, 18), 105)]
POSITIONS = list(itertools.combinations(range(4), 2))


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
    assert sum(map(len, orbits)) == len(set().union(*orbits)) == 1330
    assert set().union(*orbits) == set(itertools.combinations(range(21), 3))
    return actions


def check_domain(tree, declared, core):
    n = 18; vertices = set(range(n)); adj = [set() for _ in range(n)]
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
    n = 18; vertices = set(range(n)); red = [set() for _ in range(n)]
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


def candidate_joinings(pairs, size):
    allowed = set(map(tuple, pairs)); adjacency = [set() for _ in range(size)]
    assert all(i != j for i, j, c in pairs), 'A loop invalidates distinct-pattern coverage'
    for i, j, c in pairs:
        assert 0 <= i < j < size and c in (0, 1)
        adjacency[i].add(j); adjacency[j].add(i)
    cliques = []

    def extend(prefix, candidates):
        if len(prefix) == 4:
            cliques.append(tuple(prefix)); return
        remaining = set(candidates)
        for u in sorted(candidates):
            remaining.remove(u)
            extend(prefix + [u], remaining & adjacency[u])

    extend([], set(range(size)))
    assert cliques == sorted(set(cliques))
    result = set()
    for indices in cliques:
        for joining in range(64):
            if all((indices[i], indices[j], (joining >> b) & 1) in allowed
                   for b, (i, j) in enumerate(POSITIONS)):
                result.add((indices, joining))
    return result, len(cliques), sum(map(len, adjacency)) // 2


def check_obstructions(core, domain, deleted, labels, actions, candidates, reps):
    domain_lookup = {p: i for i, p in enumerate(domain)}
    label_index = {v: i for i, v in enumerate(labels)}
    mappings = []
    for action in actions:
        if {action[u] for u in deleted} != set(deleted):
            continue
        perm = [label_index[action[u]] for u in labels]
        assert sorted(perm) == list(range(18))
        assert {tuple(sorted((perm[u], perm[v]))) for u, v in core} == core
        images = []
        for p in domain:
            selected = {perm[u] for u in range(18) if (p >> u) & 1}
            images.append(domain_lookup[sum(1 << u for u in selected)])
        assert sorted(images) == list(range(len(domain)))
        mappings.append((images, perm))
    assert mappings
    covered = set(); keys = []
    for witness in reps:
        indices = witness['indices']; joining = witness['joining_mask']
        assert len(indices) == 4 and all(type(i) is int for i in indices)
        assert indices == sorted(set(indices)) and all(0 <= i < len(domain) for i in indices)
        assert type(joining) is int and 0 <= joining < 64
        key = tuple(indices), joining; keys.append(key)
        assert key in candidates, 'Obstruction is not a candidate'
        edges = augment(core, 18, [domain[i] for i in indices],
                        [(joining >> b) & 1 for b in range(6)])
        spine, pages = witness['spine'], witness['pages']
        assert len(spine) == 2 and all(type(u) is int for u in spine)
        u, v = spine; assert 0 <= u < v < 22
        c = int((u, v) in edges)
        assert len(pages) == (4 if c else 7), 'Wrong number of book pages'
        assert pages == sorted(set(pages)) and all(type(w) is int and 0 <= w < 22 for w in pages)
        assert not set(spine) & set(pages)
        assert all(int(tuple(sorted((a, w))) in edges) == c for a in spine for w in pages), 'False book witness'
        orbit = set()
        for mapping, perm in mappings:
            moved = [mapping[i] for i in indices]; ordered = tuple(sorted(moved))
            red_join = {frozenset((moved[i], moved[j])) for b, (i, j) in enumerate(POSITIONS)
                        if (joining >> b) & 1}
            bits = sum(1 << b for b, (i, j) in enumerate(POSITIONS)
                       if frozenset((ordered[i], ordered[j])) in red_join)
            full_image = perm + [18 + ordered.index(moved[i]) for i in range(4)]
            mapped = {tuple(sorted((full_image[a], full_image[b]))) for a, b in edges}
            target = augment(core, 18, [domain[i] for i in ordered],
                             [(bits >> b) & 1 for b in range(6)])
            assert mapped == target, 'Wrong transport of a colored completion'
            orbit.add((ordered, bits))
        assert min(orbit) == key and len(orbit) == witness['orbit_size'], 'Wrong orbit metadata'
        assert orbit <= candidates and not orbit & covered, 'Overlapping or invalid obstruction orbit'
        covered |= orbit
    assert keys == sorted(keys) and covered == candidates, 'Uncovered candidate22 joining'
    return len(mappings)


def check(path, directory, compare_compact=True):
    cert = json.loads(path.read_text())
    assert cert['format'] == 'kneser18-host-obstruction-v1' and cert['complete'] is True
    roots = [frozenset((a, b)) for a in range(7) for b in range(a + 1, 7)]
    base = {(i, j) for i, j in itertools.combinations(range(21), 2) if roots[i].isdisjoint(roots[j])}
    assert len(base) == 105 and valid(21, base)
    baseline_hash = digest({'n': 21, 'red_edges': [list(e) for e in sorted(base)]})
    assert baseline_hash == cert['baseline_sha256']
    actions = root_actions(roots)
    assert [(c['name'], tuple(c['deleted'])) for c in cert['cases']] == [(n, s) for n, s, m in CASES], 'Core cohort mismatch'
    diagnostics, projection = [], []
    for case, (name, deleted, multiplicity) in zip(cert['cases'], CASES):
        labels = [u for u in range(21) if u not in deleted]
        core = {(i, j) for i, j in itertools.combinations(range(18), 2) if (labels[i], labels[j]) in base}
        assert valid(18, core)
        domain, counts = check_domain(case['tree'], case['domain'], core)
        pairs = compatible_pairs(core, domain)
        assert pairs == case['pair_colors'], 'Wrong or omitted colored pair'
        candidates, cliques, graph_edges = candidate_joinings(pairs, len(domain))
        group_size = check_obstructions(core, domain, deleted, labels, actions, candidates, case['obstructions'])
        projection.append({'name': name, 'deleted': list(deleted), 'domain': domain,
                           'pair_colors': pairs, 'obstructions': case['obstructions']})
        diagnostics.append({'name': name, 'deleted': list(deleted), 'labeled_core_count': multiplicity,
            'core_red_edges': len(core), 'counts': counts, 'domain_size': len(domain),
            'domain_weights': dict(sorted(collections.Counter(str(p.bit_count()) for p in domain).items())),
            'colored_pairs': len(pairs), 'compatibility_edges': graph_edges, 'loops': 0,
            'four_cliques': cliques, 'allowed_joinings': len(candidates), 'root_stabilizer_size': group_size,
            'obstruction_orbits': len(case['obstructions']), 'orbit_sizes': [w['orbit_size'] for w in case['obstructions']],
            'valid22_completions': 0})
    compact = {'format': 'kneser18-obstructions-v1', 'cases': [
        {'name': c['name'], 'deleted': c['deleted'], 'obstructions': c['obstructions']} for c in cert['cases']]}
    if compare_compact:
        assert compact == json.loads((directory / 'obstructions.json').read_text()), 'Public book-witness mismatch'
    return {'complete': True, 'representative_cores': 5, 'labeled_cores': 1330,
            'baseline_sha256': baseline_hash, 'projection_sha256': digest(projection), 'cases': diagnostics}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    args = parser.parse_args(); start = time.perf_counter()
    result = check(args.certificate, Path(__file__).parent)
    assert result == json.loads((Path(__file__).parent / 'expected.json').read_text()), 'Compact signature mismatch'
    print(json.dumps({'checked': result}, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


if __name__ == '__main__':
    main()
