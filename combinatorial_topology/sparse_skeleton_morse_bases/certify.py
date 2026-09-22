"""Exact sparse-skeleton collapse certificates. Python 3.11+, standard library."""
from itertools import combinations


def normalize(n, edges, triangles, weights):
    if type(n) is not int or n < 0:
        raise ValueError('n must be a nonnegative integer')
    edges = [tuple(x) for x in edges]
    triangles = [tuple(x) for x in triangles]
    for size, faces in [(2, edges), (3, triangles)]:
        if len(set(faces)) != len(faces):
            raise ValueError('duplicate face')
        for x in faces:
            if (len(x) != size or any(type(v) is not int for v in x)
                    or x != tuple(sorted(set(x)))
                    or any(v < 0 or v >= n for v in x)):
                raise ValueError('faces must be increasing integer tuples')
    if any(e not in set(edges) for t in triangles for e in combinations(t, 2)):
        raise ValueError('missing boundary edge')
    if len(weights) != len(triangles) or any(type(w) is not int or w < 0 for w in weights):
        raise ValueError('code accepts nonnegative integer costs only')
    return sorted(edges), triangles, list(weights)


def sparse(n, edges):
    """Exponential hypothesis check, intended for small exact examples."""
    es = [sum(1 << v for v in e) for e in edges]
    for u in range(1 << n):
        if u.bit_count() >= 3 and sum(e & u == e for e in es) > 3*u.bit_count()-6:
            return False
    return True


def columns(edges, triangles):
    index = {e: i for i, e in enumerate(edges)}
    return [sum(1 << index[e] for e in combinations(t, 2)) for t in triangles]


def greedy(cols, weights):
    """F2 elimination with dependency witnesses in input triangle indices."""
    pivots, kept, rejected = {}, [], []
    for i in sorted(range(len(cols)), key=lambda j: (-weights[j], j)):
        x, support = cols[i], 1 << i
        while x:
            p = x.bit_length()-1
            if p not in pivots:
                pivots[p] = (x, support)
                kept.append(i)
                break
            y, s = pivots[p]
            x ^= y
            support ^= s
        else:
            rejected.append({'triangle': i, 'circuit': [j for j in range(len(cols))
                                                       if support >> j & 1]})
    return sorted(kept), rejected


def peel(edges, triangles, kept):
    remaining, es, pairs = set(kept), set(edges), []
    while remaining:
        incidence = {e: [] for e in es}
        for i in remaining:
            for e in combinations(triangles[i], 2):
                incidence[e].append(i)
        free = sorted(e for e, ids in incidence.items() if len(ids) == 1)
        if not free:
            break
        e = free[0]
        i = incidence[e][0]
        pairs.append([list(e), i])
        es.remove(e)
        remaining.remove(i)
    return pairs, sorted(es), sorted(remaining)


def forest(n, edges):
    adj = {v: [] for v in range(n)}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen, pairs, roots = set(), [], []
    for root in range(n):
        if root in seen:
            continue
        roots.append(root)
        seen.add(root)
        queue = [root]
        for a in queue:
            for b in sorted(adj[a]):
                if b not in seen:
                    seen.add(b)
                    queue.append(b)
                    pairs.append([b, sorted([a, b])])
    return pairs, roots


def certify(n, edges, triangles, weights):
    edges, triangles, weights = normalize(n, edges, triangles, weights)
    if not sparse(n, edges):
        raise ValueError('hereditary edge bound fails')
    kept, rejected = greedy(columns(edges, triangles), weights)
    pairs, residual, stuck = peel(edges, triangles, kept)
    if stuck:
        raise AssertionError('independent set did not collapse')
    tree, roots = forest(n, residual)
    r = len(kept)
    return {'kept': kept, 'rejected': rejected, 'collapse': pairs,
            'residual_edges': [list(e) for e in residual],
            'forest_matching': tree, 'roots': roots,
            'betti': [len(roots), len(edges)-n+len(roots)-r, len(triangles)-r],
            'deleted_cost': sum(weights[x['triangle']] for x in rejected)}


def fixtures():
    tetra = list(combinations(range(4), 3))
    glued = sorted(set(tetra + list(combinations([0, 1, 2, 4], 3))))
    octa = [tuple(sorted(t)) for t in __import__('itertools').product([0, 1], [2, 3], [4, 5])]
    cases = [('empty', 0, [], [], []), ('isolates', 3, [], [], []),
             ('graph', 4, [(0, 1), (1, 2), (0, 2), (2, 3)], [], [])]
    for name, n, ts in [('disk', 4, tetra[:-1]), ('tetrahedron', 4, tetra),
                         ('two_spheres_shared_face', 5, glued), ('octahedron', 6, octa)]:
        es = sorted({e for t in ts for e in combinations(t, 2)})
        cases.append((name, n, es, ts, [(7*i+3) % 11 for i in range(len(ts))]))
    # A nonplanar example satisfying (H): K3,3 wedged with a tetrahedral sphere.
    ts = list(combinations([0, 6, 7, 8], 3))
    es = sorted(set((a, b) for a in range(3) for b in range(3, 6)) |
                {e for t in ts for e in combinations(t, 2)})
    cases.append(('nonplanar_wedge', 9, es, ts, [0, 5, 5, 8]))
    # Two disconnected spheres and one isolated vertex.
    ts = tetra + [tuple(v+4 for v in t) for t in tetra]
    es = sorted({e for t in ts for e in combinations(t, 2)})
    cases.append(('disconnected_spheres', 9, es, ts, [0]*8))
    return [{'name': name, 'n': n, 'edges': [list(e) for e in es],
             'triangles': [list(t) for t in ts], 'weights': ws}
            for name, n, es, ts, ws in cases]


if __name__ == '__main__':
    import json
    records = []
    for case in fixtures():
        records.append({'input': case, 'certificate': certify(**{k: v for k, v in case.items()
                                                               if k != 'name'})})
    print(json.dumps(records, sort_keys=True, indent=2))
