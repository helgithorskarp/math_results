"""Definition-level replay, rational ranks, finite exhaustive and negative checks."""
from collections import Counter, deque
from copy import deepcopy
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import certify as producer


def rational_rank(edges, ts):
    """Independent oriented d2 construction and rational row reduction."""
    matrix = []
    for e in edges:
        row = []
        for a, b, c in ts:
            row.append(Fraction(int(tuple(e) == (b, c)) - int(tuple(e) == (a, c))
                                + int(tuple(e) == (a, b))))
        matrix.append(row)
    rank = 0
    for j in range(len(ts)):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][j]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][j]
        matrix[rank] = [x/scale for x in matrix[rank]]
        for i in range(rank+1, len(matrix)):
            scale = matrix[i][j]
            if scale:
                matrix[i] = [a-scale*b for a, b in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


def dag(nodes, arcs):
    out = {x: [] for x in nodes}
    indeg = {x: 0 for x in nodes}
    for a, b in arcs:
        out[a].append(b)
        indeg[b] += 1
    todo = deque(x for x in nodes if not indeg[x])
    seen = 0
    while todo:
        a = todo.popleft()
        seen += 1
        for b in out[a]:
            indeg[b] -= 1
            if not indeg[b]:
                todo.append(b)
    return seen == len(nodes)


def sphere(ts):
    """Closed connected surface + Euler two, checked directly from vertex links."""
    vertices = {v for t in ts for v in t}
    edges = Counter(e for t in ts for e in combinations(t, 2))
    assert ts and set(edges.values()) == {2}
    assert len(vertices)-len(edges)+len(ts) == 2
    for v in vertices:
        link = [tuple(x for x in t if x != v) for t in ts if v in t]
        adj = {}
        for a, b in link:
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
        assert all(len(s) == 2 for s in adj.values())
        todo, seen = [next(iter(adj))], set()
        while todo:
            a = todo.pop()
            if a not in seen:
                seen.add(a)
                todo.extend(adj[a]-seen)
        assert len(seen) == len(adj)
    # Vertex connectivity excludes a disjoint union of surfaces.
    todo, seen = [next(iter(vertices))], set()
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v)
            todo.extend(w for e in edges if v in e for w in e if w not in seen)
    assert seen == vertices


def check(case, cert):
    n = case['n']
    es = {tuple(e) for e in case['edges']}
    ts = [tuple(t) for t in case['triangles']]
    w = case['weights']
    kept = set(cert['kept'])
    deleted = [x['triangle'] for x in cert['rejected']]
    assert len(kept) == len(cert['kept']) and len(set(deleted)) == len(deleted)
    assert not kept.intersection(deleted) and kept.union(deleted) == set(range(len(ts)))
    rank = rational_rank(sorted(es), ts)
    assert rational_rank(sorted(es), [ts[i] for i in kept]) == len(kept) == rank
    # A full circuit of no lighter basis elements certifies each rejection.
    for rec in cert['rejected']:
        i, circuit = rec['triangle'], rec['circuit']
        assert len(set(circuit)) == len(circuit) and i in circuit
        assert set(circuit)-{i} <= kept
        assert all(w[j] >= w[i] for j in circuit if j != i)
        sphere([ts[j] for j in circuit])
    remain, edges, matching = set(kept), set(es), []
    for edge, i in cert['collapse']:
        e = tuple(edge)
        assert e in edges and i in remain and set(e) <= set(ts[i])
        assert [j for j in remain if set(e) <= set(ts[j])] == [i]
        matching.append((e, ts[i]))
        remain.remove(i)
        edges.remove(e)
    assert not remain and edges == {tuple(e) for e in cert['residual_edges']}
    for v, edge in cert['forest_matching']:
        e = tuple(edge)
        assert e in edges and v in e
        matching.append(((v,), e))
    used = [s for pair in matching for s in pair]
    assert len(set(used)) == len(used)
    faces = {(v,) for v in range(n)} | es | set(ts)
    pairs = set(matching)
    arcs = []
    for b in faces:
        if len(b) > 1:
            for a in combinations(b, len(b)-1):
                arcs.append((a, b) if (a, b) in pairs else (b, a))
    assert dag(faces, arcs)
    critical = faces-set(used)
    counts = [sum(len(s) == d+1 for s in critical) for d in range(3)]
    # Graph-component count independent of the producer's forest.
    components = [{v} for v in range(n)]
    for a, b in es:
        left = next(s for s in components if a in s)
        right = next(s for s in components if b in s)
        if left is not right:
            left.update(right)
            components.remove(right)
    betti = [len(components), len(es)-n+len(components)-rank, len(ts)-rank]
    assert counts == cert['betti'] == betti
    assert {(v,) for v in cert['roots']} == {s for s in critical if len(s) == 1}
    assert cert['deleted_cost'] == sum(w[i] for i in deleted)


def main():
    stored = json.loads(Path(__file__).with_name('certificates.json').read_text())
    assert [r['input'] for r in stored] == producer.fixtures()
    subsets = 0
    for row in stored:
        case, cert = row['input'], row['certificate']
        assert cert == producer.certify(**{k: v for k, v in case.items() if k != 'name'})
        check(case, cert)
        ts, es = case['triangles'], case['edges']
        optimum = sum(case['weights'])
        for mask in range(1 << len(ts)):
            keep = [i for i in range(len(ts)) if mask >> i & 1]
            if rational_rank(es, [ts[i] for i in keep]) == len(keep):
                optimum = min(optimum, sum(w for i, w in enumerate(case['weights']) if i not in keep))
            subsets += 1
        assert optimum == cert['deleted_cost']
    # All abstract complexes on five fixed vertices with any graph satisfying H.
    # All simple graphs except K5 satisfy H on five vertices.
    all_edges = list(combinations(range(5), 2))
    complexes = circuits = 0
    for mask in range((1 << len(all_edges))-1):
        es = [e for i, e in enumerate(all_edges) if mask >> i & 1]
        assert producer.sparse(5, es)
        ts = [t for t in combinations(range(5), 3) if all(e in es for e in combinations(t, 2))]
        for tmask in range(1 << len(ts)):
            faces = [t for i, t in enumerate(ts) if tmask >> i & 1]
            rank = rational_rank(es, faces)
            pairs, residual, stuck = producer.peel(es, faces, range(len(faces)))
            assert bool(stuck) == (rank != len(faces))
            kept, rejected = producer.greedy(producer.columns(es, faces), [1]*len(faces))
            assert len(kept) == rank
            for rec in rejected:
                sphere([faces[i] for i in rec['circuit']])
                circuits += 1
            complexes += 1
    # RP2 plus an isolated vertex passes the total bound but violates H.
    rp = [(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),
          (1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
    es = list(combinations(range(6), 2))
    assert len(es) == 3*7-6 and not producer.sparse(7, es)
    assert rational_rank(es, rp) == 10
    assert len(producer.greedy(producer.columns(es, rp), [1]*10)[0]) == 9
    assert len(producer.peel(es, rp, range(10))[2]) == 10
    bad_inputs = [(-1, [], [], []), (3, [(0,1)], [(0,1,2)], [1]),
                  (3, [(1,0)], [], []), (3, [], [], [-1]),
                  (7, es, rp, [1]*10), (2, [(0,1),(0,1)], [], [])]
    for args in bad_inputs:
        try:
            producer.certify(*args)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    # Reject independent corruption of a collapse, rank, cost, circuit, or matching.
    row = next(x for x in stored if x['input']['name'] == 'tetrahedron')
    mutations = []
    for field in ['collapse', 'kept', 'deleted_cost', 'rejected', 'forest_matching']:
        c = deepcopy(row['certificate'])
        if field == 'collapse': c[field] = c[field][1:]
        elif field == 'kept': c[field] = []
        elif field == 'deleted_cost': c[field] += 1
        elif field == 'rejected': c[field][0]['circuit'] = [c[field][0]['triangle']]
        else: c[field] += c[field][:1]
        mutations.append(c)
    for c in mutations:
        try:
            check(row['input'], c)
        except AssertionError:
            pass
        else:
            raise AssertionError('corrupt certificate accepted')
    output = {'fixtures': len(stored), 'weighted_subsets': subsets,
              'five_vertex_complexes': complexes, 'sphere_circuit_checks': circuits,
              'invalid_inputs_rejected': len(bad_inputs), 'corrupt_certificates_rejected': len(mutations),
              'global_count_counterexample': 'RP2 plus one isolated vertex'}
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        assert output == json.loads(expected.read_text())
    print(json.dumps(output, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
