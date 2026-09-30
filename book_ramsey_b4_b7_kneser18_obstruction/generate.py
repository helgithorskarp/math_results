"""Certify the maximum valid host order of every KG(7,2) induced18 core."""
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

CASES = [('triangle', [0, 1, 6], 35), ('star', [0, 1, 2], 140),
         ('path', [0, 6, 11], 420), ('wedge_edge', [0, 1, 15], 630),
         ('matching', [0, 11, 18], 105)]
POSITIONS = list(itertools.combinations(range(4), 2))


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


def four_cliques(adjacency):
    result = []
    for i in range(len(adjacency)):
        for j in sorted(adjacency[i]):
            if i < j:
                common = adjacency[i] & adjacency[j]
                for k in sorted(common):
                    if j < k:
                        result.extend((i, j, k, l) for l in sorted(common & adjacency[k]) if k < l)
    assert result == sorted(set(result))
    return result


def transform(case, mapping):
    indices, mask = case
    target = [mapping[i] for i in indices]; ordered = sorted(target)
    where = {v: j for j, v in enumerate(ordered)}
    bits = 0
    for b, (i, j) in enumerate(POSITIONS):
        if (mask >> b) & 1:
            pair = tuple(sorted((where[target[i]], where[target[j]])))
            bits |= 1 << POSITIONS.index(pair)
    return tuple(ordered), bits


def obstructions(rows, domain, joint_cases, roots, deleted, labels):
    root_deleted = {roots[u] for u in deleted}
    core_index = {roots[u]: j for j, u in enumerate(labels)}
    domain_index = {p: i for i, p in enumerate(domain)}
    maps = []
    for sigma in itertools.permutations(range(7)):
        def image(edge):
            return tuple(sorted(sigma[x] for x in edge))
        if {image(edge) for edge in root_deleted} != root_deleted:
            continue
        perm = [core_index[image(roots[u])] for u in labels]
        maps.append([domain_index[sum(1 << perm[u] for u in range(18) if (p >> u) & 1)]
                     for p in domain])
    unseen = set(joint_cases); representatives = []
    while unseen:
        case = min(unseen)
        orbit = {transform(case, mapping) for mapping in maps}
        assert orbit <= unseen and orbit <= joint_cases
        indices, joining = case
        g = augment(rows, [domain[i] for i in indices], [(joining >> b) & 1 for b in range(6)])
        assert not valid(g), 'A valid22 completion escapes the proposed obstruction'
        full = (1 << 22) - 1
        for u, v in itertools.combinations(range(22), 2):
            c = (g[u] >> v) & 1
            pages = g[u] & g[v] if c else (
                full & ~(g[u] | g[v] | (1 << u) | (1 << v)))
            cap = 3 if c else 6
            if pages.bit_count() > cap:
                representatives.append({'indices': list(indices), 'joining_mask': joining,
                    'spine': [u, v], 'pages': [w for w in range(22) if (pages >> w) & 1][:cap + 1],
                    'orbit_size': len(orbit)})
                break
        unseen -= orbit
    return representatives, len(maps)


def generate():
    roots = list(itertools.combinations(range(7), 2))
    base = [sum(1 << j for j, f in enumerate(roots) if not set(edge) & set(f)) for edge in roots]
    assert valid(base) and all(row.bit_count() == 10 for row in base)
    edges = [[u, v] for u, v in itertools.combinations(range(21), 2) if (base[u] >> v) & 1]
    assert len(edges) == 105
    assert all((base[u] & base[v]).bit_count() == 3 for u, v in edges)
    full = (1 << 21) - 1
    assert all((full & ~(base[u] | base[v] | (1 << u) | (1 << v))).bit_count() == 5
               for u, v in itertools.combinations(range(21), 2) if not (base[u] >> v) & 1)
    baseline_hash = digest({'n': 21, 'red_edges': edges})
    cases, diagnostics, projection = [], [], []
    for name, deleted, multiplicity in CASES:
        labels = [u for u in range(21) if u not in deleted]
        rows = [sum(1 << j for j, v in enumerate(labels) if (base[u] >> v) & 1) for u in labels]
        tree, domain, counts = domain_tree(rows)
        pairs = []; adjacency = [set() for _ in domain]; allowed = collections.defaultdict(list)
        for i, p in enumerate(domain):
            for j in range(i, len(domain)):
                for c in (0, 1):
                    if pair_valid(rows, p, domain[j], c):
                        pairs.append([i, j, c]); adjacency[i].add(j); adjacency[j].add(i)
                        allowed[i, j].append(c)
        assert all(i != j for i, j, c in pairs), 'A loop prevents distinct-pattern coverage'
        cliques = four_cliques(adjacency)
        joint_cases = {(indices, sum(c << b for b, c in enumerate(colors)))
                       for indices in cliques for colors in itertools.product(
                           *(allowed[i, j] for i, j in itertools.combinations(indices, 2)))}
        reps, group_size = obstructions(rows, domain, joint_cases, roots, deleted, labels)
        case = {'name': name, 'deleted': deleted, 'tree': tree, 'domain': domain,
                'pair_colors': pairs, 'obstructions': reps}
        cases.append(case)
        projection.append({k: v for k, v in case.items() if k != 'tree'})
        diagnostics.append({'name': name, 'deleted': deleted, 'labeled_core_count': multiplicity,
            'core_red_edges': sum(r.bit_count() for r in rows) // 2, 'counts': counts,
            'domain_size': len(domain), 'domain_weights': dict(sorted(collections.Counter(
                str(p.bit_count()) for p in domain).items())), 'colored_pairs': len(pairs),
            'compatibility_edges': sum(map(len, adjacency)) // 2,
            'loops': 0, 'four_cliques': len(cliques), 'allowed_joinings': len(joint_cases),
            'root_stabilizer_size': group_size, 'obstruction_orbits': len(reps),
            'orbit_sizes': [r['orbit_size'] for r in reps], 'valid22_completions': 0})
    certificate = {'format': 'kneser18-host-obstruction-v1', 'complete': True,
                   'baseline_sha256': baseline_hash, 'cases': cases}
    summary = {'complete': True, 'representative_cores': 5, 'labeled_cores': 1330,
               'baseline_sha256': baseline_hash, 'projection_sha256': digest(projection),
               'cases': diagnostics}
    compact = {'format': 'kneser18-obstructions-v1', 'cases': [
        {'name': c['name'], 'deleted': c['deleted'], 'obstructions': c['obstructions']} for c in cases]}
    return certificate, summary, compact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--summary', type=Path)
    parser.add_argument('--obstructions', type=Path)
    args = parser.parse_args(); start = time.perf_counter()
    certificate, summary, compact = generate()
    args.certificate.write_text(json.dumps(certificate, separators=(',', ':')) + '\n')
    if args.summary:
        args.summary.write_text(json.dumps(summary, indent=2) + '\n')
    if args.obstructions:
        args.obstructions.write_text(json.dumps(compact, separators=(',', ':')) + '\n')
    print(json.dumps(summary, indent=2))
    print('seconds=', time.perf_counter() - start,
          'maxrss_kib=', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
          'private_certificate_bytes=', args.certificate.stat().st_size)


if __name__ == '__main__':
    main()
