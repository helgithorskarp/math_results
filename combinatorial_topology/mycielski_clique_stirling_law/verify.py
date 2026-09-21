#!/usr/bin/env python3
"""Definition-level chain and collapse audits; not a universal proof.

No solver or external dataset. All checks survive Python optimization.
"""
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json
import sys
import construct as producer


def require(ok, message):
    if not ok:
        raise ValueError(message)


def cliques(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    by_size = {}
    def extend(face, possible):
        for v in sorted(possible):
            f = face + (v,)
            by_size.setdefault(len(f), []).append(f)
            extend(f, {w for w in possible & adj[v] if w > v})
    extend((), set(range(n)))
    return by_size


def rank(columns, prime):
    pivots = {}
    for column in columns:
        a = {i: x % prime for i, x in column.items() if x % prime}
        while a:
            j = max(a)
            if j not in pivots:
                inverse = pow(a[j], -1, prime)
                pivots[j] = {i: x*inverse % prime for i, x in a.items()}
                break
            factor = a[j]
            for i, x in pivots[j].items():
                value = (a.get(i, 0)-factor*x) % prime
                if value:
                    a[i] = value
                else:
                    a.pop(i, None)
    return len(pivots)


def homology(n, edges, prime=2):
    cells = cliques(n, edges)
    maximum = max(cells)
    ranks = {0: 0, maximum: 0}
    for dimension in range(1, maximum):
        rows = {f: i for i, f in enumerate(cells[dimension])}
        columns = []
        for face in cells[dimension+1]:
            columns.append({rows[face[:i]+face[i+1:]]: (-1)**i
                            for i in range(dimension+1)})
        ranks[dimension] = rank(columns, prime)
    answer = [len(cells[d+1])-ranks[d]-ranks[d+1] for d in range(maximum)]
    return (answer+[0]*3)[:max(3, len(answer))]


def component_count(vertices, edges):
    parent = {v: v for v in vertices}
    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for a, b in edges:
        parent[root(a)] = root(b)
    return len({root(v) for v in vertices})


def direct_stats(n, edges):
    cells = cliques(n, edges)
    require(4 not in cells, 'fixture outside dimension two')
    tris = cells.get(3, [])
    multiplicities = {e: sum(set(e) <= set(t) for t in tris) for e in edges}
    links = []
    d = 0
    for v in range(n):
        vertices = {w for w in range(n) if tuple(sorted((v, w))) in edges}
        link_edges = {tuple(w for w in t if w != v) for t in tris if v in t}
        c = component_count(vertices, link_edges)
        d += len(link_edges)-len(vertices)+c
        links.append(c)
    e0 = sum(x == 0 for x in multiplicities.values())
    return {'n': n, 'm': len(edges), 't': len(tris), 'e0': e0, 'C': sum(links),
            'D': d, 'Y': sum(max(0, x-1) for x in multiplicities.values()),
            'link_components': links}


def direct_mycielski(n, edges):
    """All-pairs adjacency predicate, separate from edge lifting."""
    def adjacent(a, b):
        if b == 2*n:
            return n <= a < 2*n
        if a >= n:
            return False
        if b < n:
            return (a, b) in edges
        return tuple(sorted((a, b-n))) in edges
    return 2*n+1, {e for e in combinations(range(2*n+1), 2) if adjacent(*e)}


def check_trace(n, edges, trace, selected=None):
    require(trace is not None, 'missing collapse trace')
    triangles = set(cliques(n, edges).get(3, []))
    if selected is not None:
        triangles &= set(selected)
    remaining_edges = set(edges)
    removed = 0
    for edge, face in trace:
        edge, face = tuple(edge), tuple(face)
        if selected is not None and face not in triangles:
            continue
        require(face in triangles and edge in remaining_edges, 'absent collapse face')
        require(set(edge) < set(face), 'edge is not a triangle face')
        require(sum(set(edge) <= set(t) for t in triangles) == 1, 'edge is not free')
        triangles.remove(face)
        remaining_edges.remove(edge)
        removed += 1
    require(not triangles, 'unremoved triangles')
    return removed


def barycentric_graph(facets):
    faces = sorted({f for t in facets for k in (1, 2, 3) for f in combinations(t, k)},
                   key=lambda f: (len(f), f))
    edges = {(a, b) for a, b in combinations(range(len(faces)), 2)
             if set(faces[a]) < set(faces[b]) or set(faces[b]) < set(faces[a])}
    return len(faces), edges


def run():
    counts = {'labelled_bases': 0, 'connected_k4_free': 0, 'one_step_checks': 0,
              'collapse_traces': 0, 'collapse_pairs': 0, 'restricted_traces': 0,
              'fixture_iterates': 0, 'field_checks': 0, 'rejections': 0}
    signatures = []
    categories = {'1': 0, '2': 0, '3': 0, 'never': 0}
    for n in range(2, 6):
        all_edges = list(combinations(range(n), 2))
        for mask in range(1 << len(all_edges)):
            counts['labelled_bases'] += 1
            edges = {e for i, e in enumerate(all_edges) if mask >> i & 1}
            cells = cliques(n, edges)
            if component_count(range(n), edges) != 1 or 4 in cells:
                continue
            counts['connected_k4_free'] += 1
            s = producer.statistics(n, edges)
            require(s == direct_stats(n, edges), 'entry-level statistics')
            nn, ee = direct_mycielski(n, edges)
            require((nn, ee) == producer.mycielski(n, edges), 'all-pairs lift')
            h, hh = homology(n, edges), homology(nn, ee)
            w = producer.wedge_counts(s, 1)
            require(hh == [1, h[1]+w['circles'], h[2]+w['two_spheres']],
                    'one-step chain ranks')
            ss = direct_stats(nn, ee)
            require([ss[x] for x in ('n', 'm', 't', 'e0', 'C')] ==
                    [2*n+1, 3*s['m']+n, 4*s['t'], 3*s['e0']+n,
                     2*s['C']+2*s['e0']+2*n], 'all statistic recurrences')
            counts['one_step_checks'] += 1
            failure = producer.first_failure(s)
            categories[str(failure) if failure else 'never'] += 1
            if not s['D']:
                trace = producer.collapse_trace(nn, ee)
                counts['collapse_pairs'] += check_trace(nn, ee, trace)
                counts['collapse_traces'] += 1
            signatures.append([n, mask, s, hh, failure])

    fixtures = [
        ('edge', 2, {(0, 1)}),
        ('triangle', 3, {(0, 1), (0, 2), (1, 2)}),
        ('diamond', 4, {(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)}),
        ('wheel4', 5, {(0, 1), (1, 2), (2, 3), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)}),
        ('bowtie', 5, {(0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4)}),
        ('octahedron', 6, {e for e in combinations(range(6), 2) if e[0]//2 != e[1]//2}),
    ]
    records = []
    for name, n, edges in fixtures:
        s = direct_stats(n, edges)
        initial = {p: homology(n, edges, p) for p in (2, 3)}
        rows = []
        r, q = 0, 0
        for k in range(4):
            w = producer.wedge_counts(s, k)
            require(w == {'circles': r, 'two_spheres': q}, 'closed versus iterated counts')
            fields = {}
            for prime in (2, 3):
                h = homology(n, edges, prime)
                require(h == [1, initial[prime][1]+r, initial[prime][2]+q], 'iterate homology')
                fields[str(prime)] = h
                counts['field_checks'] += 1
            if k and q == 0:
                trace = producer.collapse_trace(n, edges)
                counts['collapse_pairs'] += check_trace(n, edges, trace)
                counts['collapse_traces'] += 1
            rows.append({'k': k, 'vertices': n, 'edges': len(edges), **w, 'betti': fields})
            counts['fixture_iterates'] += 1
            if k < 3:
                current = direct_stats(n, edges)
                r += current['C']-1
                q += current['D']
                n, edges = direct_mycielski(n, edges)
        records.append({'name': name, 'statistics': s, 'iterates': rows})

    # Restrict legal triangle/edge collapses to every triangle subfamily of
    # two positive fixtures. Arbitrary extra graph edges are harmless.
    for name, n, edges in fixtures[1:3]:
        n, edges = direct_mycielski(n, edges)
        ts = cliques(n, edges)[3]
        trace = producer.collapse_trace(n, edges)
        for mask in range(1 << len(ts)):
            selected = [t for i, t in enumerate(ts) if mask >> i & 1]
            check_trace(n, edges, trace, selected)
            counts['restricted_traces'] += 1

    # Flag subdivision of the six-vertex projective-plane triangulation.
    facets = [(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),
              (1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
    n, edges = barycentric_graph(facets)
    s = producer.statistics(n, edges)
    nn, ee = direct_mycielski(n, edges)
    torsion = {}
    for prime in (2, 3):
        before, after = homology(n, edges, prime), homology(nn, ee, prime)
        require(before == ([1,1,1] if prime == 2 else [1,0,0]), 'torsion control input')
        require(after == [1, before[1]+s['C']-1, before[2]+s['D']], 'torsion control lift')
        torsion[str(prime)] = {'before': before, 'after': after}
        counts['field_checks'] += 2

    # K4 is excluded for a reason: its filled links must not be treated as graphs.
    n, edges = 4, set(combinations(range(4), 2))
    nn, ee = direct_mycielski(n, edges)
    outside = homology(nn, ee)
    require(outside == [1,3,0,0], 'K4 outside-domain control')
    def reject(fn):
        try:
            fn()
        except ValueError:
            counts['rejections'] += 1
        else:
            raise ValueError('bad control accepted')
    reject(lambda: producer.statistics(n, edges))
    for n0, es in [(1, []), (4, [(0,1),(2,3)]), (2, [(0,0)]),
                   (2, [(1,0)]), (2, [(0,1),(0,1)]), (2, [(0,2)]), (2, [(0,1.0)])]:
        reject(lambda n0=n0, es=es: producer.statistics(n0, es))
    reject(lambda: producer.wedge_counts(records[0]['statistics'], -1))
    reject(lambda: check_trace(3, {(0,1),(0,2),(1,2)}, [[[0,2],[0,1,2]], [[0,2],[0,1,2]]]))
    reject(lambda: check_trace(3, {(0,1),(0,2),(1,2)}, [[[0,3],[0,1,2]]]))

    # Independent exponential expressions audit the Stirling convention.
    for k in range(13):
        require(producer.stirling(k+1,2) == 2**k-1, 'Stirling index two')
        require(2*producer.stirling(k+1,3) == 3**k-2*2**k+1, 'Stirling index three')
        require(6*producer.stirling(k+1,4) == 4**k-3*3**k+3*2**k-1, 'Stirling index four')
    digest = sha256(json.dumps(signatures, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'status': 'pass', 'counts': counts, 'first_failure_categories': categories,
            'labelled_audit_sha256': digest, 'fixtures': records,
            'torsion_control': torsion, 'outside_K4_betti': outside}


if __name__ == '__main__':
    result = run()
    if '--emit' not in sys.argv[1:]:
        require(result == json.loads(Path(__file__).with_name('expected.json').read_text()),
                'expected output mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))
