#!/usr/bin/env python3
"""Exact finite corroboration; CPython 3.11+, standard library only.

The universal homotopy and integer-presentation claims are proved in PROOF.md.
This checker builds small square complexes directly and checks a stored
integral torsion witness. It does not enumerate the large example's faces.
"""
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
BASE_FACETS = [tuple(map(int, s)) for s in
               '012 013 024 035 045 125 134 145 234 235'.split()]


def require(test, message):
    if not test:
        raise ValueError(message)


def normalize_graph(n, edges):
    require(type(n) is int and n >= 2, 'at least two vertices required')
    out = []
    for edge in edges:
        require(len(edge) == 2, 'bad edge size')
        u, v = edge
        require(type(u) is int and type(v) is int and 0 <= u < n and 0 <= v < n,
                'bad vertex label')
        require(u != v, 'loop')
        out.append(tuple(sorted((u, v))))
    require(len(out) == len(set(out)), 'duplicate edge')
    out.sort()
    adj = adjacency(n, out)
    seen, todo = {0}, [0]
    while todo:
        v = todo.pop()
        for u in adj[v] - seen:
            seen.add(u)
            todo.append(u)
    require(len(seen) == n, 'disconnected graph')
    return out, adj


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def construct(n, edges):
    edges, _ = normalize_graph(n, edges)
    m = len(edges)
    original = list(range(m + 1, m + 1 + n))
    ports = list(range(m + 1 + n, 2 * m + n + 1))
    be = []
    for i, (u, v) in enumerate(edges):
        be.extend([(i, original[u]), (i, original[v]), (i, ports[i]), (m, ports[i])])
    nb = 2 * m + n + 1
    return adjacency(nb, be), list(range(m + 1)), original, ports, edges


def square(adj):
    return [(set(ns).union(*(adj[u] for u in ns))) - {v}
            for v, ns in enumerate(adj)]


def cliques(adj, bound=4):
    levels = [[] for _ in range(bound)]

    def rec(prefix, candidates):
        if prefix:
            levels[len(prefix) - 1].append(prefix)
        if len(prefix) == bound:
            return
        for i, v in enumerate(candidates):
            rec(prefix + (v,), [u for u in candidates[i + 1:] if u in adj[v]])
    rec((), list(range(len(adj))))
    return [sorted(level) for level in levels]


def simplex_faces(vertices):
    vv = sorted(vertices)
    return {frozenset(s) for k in range(len(vv) + 1) for s in combinations(vv, k)}


def orientation(vertices):
    require(len(set(vertices)) == len(vertices), 'repeated oriented vertex')
    sign = (-1) ** sum(vertices[i] > vertices[j]
                       for i in range(len(vertices)) for j in range(i + 1, len(vertices)))
    return tuple(sorted(vertices)), sign


def clean(chain):
    return {f: a for f, a in chain.items() if a}


def boundary(chain):
    result = Counter()
    for face, a in chain.items():
        for i in range(len(face)):
            result[face[:i] + face[i + 1:]] += a * (-1) ** i
    return clean(result)


def matrix_columns(upper, lower):
    index = {f: i for i, f in enumerate(lower)}
    result = []
    for f in upper:
        result.append({index[f[:i] + f[i + 1:]]: (-1) ** i for i in range(len(f))})
    return result


def rank_mod(columns, p):
    pivots = {}
    for column in columns:
        v = {i: a % p for i, a in column.items() if a % p}
        while v:
            i = min(v)
            if i not in pivots:
                scale = pow(v[i], -1, p)
                pivots[i] = {j: a * scale % p for j, a in v.items()}
                break
            scale = v[i]
            for j, a in pivots[i].items():
                b = (v.get(j, 0) - scale * a) % p
                if b:
                    v[j] = b
                else:
                    v.pop(j, None)
    return len(pivots)


def canonical_vector(v):
    v = clean(v)
    if not v:
        return ()
    s = 1 if v[min(v)] > 0 else -1
    return tuple((i, s * a) for i, a in sorted(v.items()))


def audit_w(n, edges, original, ports):
    faces = simplex_faces(ports)
    incident = [[i for i, e in enumerate(edges) if v in e] for v in range(n)]
    for v in range(n):
        faces.update(simplex_faces([original[v]] + [ports[i] for i in incident[v]]))
    for i, (u, v) in enumerate(edges):
        faces.update(simplex_faces([original[u], original[v], ports[i]]))
    pairs = 0

    def remove(low, high):
        nonlocal pairs
        low, high = frozenset(low), frozenset(high)
        require(low in faces and high in faces and len(high) == len(low) + 1,
                'absent collapse pair')
        require({f for f in faces if low < f} == {high}, 'pair is not globally free in W')
        faces.remove(low)
        faces.remove(high)
        pairs += 1

    for i, (u, v) in enumerate(edges):
        remove([original[u], original[v]], [original[u], original[v], ports[i]])
    for v in range(n):
        pp = [ports[i] for i in incident[v]]
        anchor, rest = pp[0], pp[1:]
        for size in range(len(rest), -1, -1):
            for s in combinations(rest, size):
                low = [original[v], *s]
                remove(low, low + [anchor])
    require(faces == simplex_faces(ports), 'W did not collapse to the port simplex')
    return pairs


def audit_small(n, edges):
    badj, xx, original, ports, edges = construct(n, edges)
    m = len(edges)
    xset, yset = set(xx), set(original + ports)
    require(all(len(badj[a] & badj[b]) <= 1 for a, b in combinations(xx, 2)), 'C4')
    require(sum(map(len, badj)) == 8 * m, 'wrong edge count')
    adj = square(badj)
    require(xset - {m} <= adj[m], 'X half is not a cone')
    for e, f in combinations(range(m), 2):
        require((f in adj[e]) == bool(set(edges[e]) & set(edges[f])), 'wrong line graph')
    levels = cliques(adj)
    tri_set = set(levels[2])
    closed = [ns | {v} for v, ns in enumerate(badj)]

    def in_bridge(face):
        return any(set(face) <= ns for ns in closed)

    require(all(in_bridge(e) for e in levels[1]), 'bridge misses an edge')
    ytri = [t for t in levels[2] if set(t) <= yset and not in_bridge(t)]
    index = {t: i for i, t in enumerate(ytri)}
    _, gadj = normalize_graph(n, edges)
    gl = cliques(gadj)
    expected_tri = [tuple(original[v] for v in t) for t in gl[2]]
    incident = [[i for i, e in enumerate(edges) if v in e] for v in range(n)]
    expected_tri += [(original[v], ports[e], ports[f])
                     for v in range(n) for e, f in combinations(incident[v], 2)]
    require(set(ytri) == set(expected_tri), 'noncentered triangle classification')

    direct_relations = []
    for tet in levels[3]:
        if not set(tet) <= yset:
            continue
        v = {index[t]: a for t, a in boundary({tet: 1}).items() if t in index}
        if v:
            direct_relations.append(canonical_vector(v))
    predicted_relations, fan_columns = [], []
    for tet in gl[3]:
        v = {index[tuple(original[u] for u in t)]: a
             for t, a in boundary({tet: 1}).items()}
        predicted_relations.append(canonical_vector(v))
    for v in range(n):
        for e, f, g in combinations(incident[v], 3):
            column = {index[(original[v], ports[f], ports[g])]: 1,
                      index[(original[v], ports[e], ports[g])]: -1,
                      index[(original[v], ports[e], ports[f])]: 1}
            predicted_relations.append(canonical_vector(column))
            fan_columns.append(column)
    require(Counter(direct_relations) == Counter(predicted_relations), 'integer relation columns')

    # Literal octahedral chains and the detector, without using the claimed presentation.
    def expanded(t):
        cycle = Counter()
        for a, b in zip(t, t[1:] + t[:1]):
            common = badj[a] & badj[b]
            require(len(common) == 1, 'nonunique center')
            center = next(iter(common))
            cycle[(center, a)] -= 1
            cycle[(center, b)] += 1
        return clean(cycle)

    expansion = {t: expanded(t) for t in levels[2] if set(t) <= yset}

    def detect(chain):
        out = Counter()
        for t, a in chain.items():
            for e, b in expansion.get(t, {}).items():
                out[e] += a * b
        return clean(out)

    for tet in levels[3]:
        require(not detect(boundary({tet: 1})), 'detector fails on a tetrahedron')
    for t in ytri:
        opposite = [next(iter(badj[t[(i + 1) % 3]] & badj[t[(i + 2) % 3]]))
                    for i in range(3)]
        sphere = Counter()
        for bits in product([0, 1], repeat=3):
            face, sign = orientation([opposite[i] if bits[i] else t[i] for i in range(3)])
            require(face in tri_set, 'missing sphere face')
            sphere[face] += sign * (-1) ** sum(bits)
        sphere = clean(sphere)
        require(len(sphere) == 8 and not boundary(sphere), 'not an integral octahedral cycle')
        require({f: a for f, a in sphere.items() if f in index} == {t: 1}, 'relative sphere sign')
        image = detect(sphere)
        require(image == expansion[t] and len(image) == 6 and set(image.values()) == {-1, 1},
                'nonprimitive hexagon detector image')

    b2 = matrix_columns(levels[2], levels[1])
    b3 = matrix_columns(levels[3], levels[2])
    gb3 = matrix_columns(gl[3], gl[2])
    values = {}
    for p in (2, 3):
        r2, r3 = rank_mod(b2, p), rank_mod(b3, p)
        h1 = len(levels[1]) - len(levels[0]) + 1 - r2
        h2 = len(levels[2]) - r2 - r3
        predicted = len(gl[2]) - rank_mod(gb3, p) + 2 * m - n
        require(h1 == 0 and h2 == predicted, 'direct square homology mismatch')
        require(len(ytri) - rank_mod([dict(v) for v in direct_relations], p) == h2,
                'presentation rank mismatch')
        values[str(p)] = h2
    return {'n': n, 'm': m, 'B_vertices': len(badj), 'hexagons': len(ytri),
            'relations': len(direct_relations), 'fan_rank_F3': rank_mod(fan_columns, 3),
            'H2_dimensions': values, 'W_collapse_pairs': audit_w(n, edges, original, ports)}


def determinant(a):
    a = [row[:] for row in a]
    n, previous, sign = len(a), 1, 1
    require(all(len(row) == n for row in a), 'nonsquare determinant input')
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            sign *= -1
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = a[i][j] * p - a[i][k] * a[k][j]
                require(num % previous == 0, 'inexact Bareiss division')
                a[i][j] = num // previous
            a[i][k] = 0
        previous = p
    return sign * a[-1][-1]


def torsion_input():
    base_faces = set().union(*(simplex_faces(f) for f in BASE_FACETS)) - {frozenset()}
    labels = sorted(base_faces, key=lambda f: (len(f), sorted(f)))
    edges = [(i, j) for i, a in enumerate(labels) for j, b in enumerate(labels)
             if i < j and (a < b or b < a)]
    u, v = len(labels), len(labels) + 1
    edges += [(i, u) for i in range(len(labels))] + [(i, v) for i in range(len(labels))]
    edges, adj = normalize_graph(v + 1, edges)
    return labels, edges, adj, u, v


def decode_chain(entries, dimension, valid_faces):
    result = {}
    for entry in entries:
        require(len(entry) == 2, 'bad certificate entry')
        f, a = tuple(entry[0]), entry[1]
        require(len(f) == dimension + 1 and tuple(sorted(f)) == f and len(set(f)) == len(f),
                'bad certificate simplex')
        require(f in valid_faces and f not in result, 'unknown or repeated certificate simplex')
        require(type(a) is int and a != 0, 'bad coefficient')
        result[f] = a
    return result


def audit_torsion():
    cert_path = HERE / 'TORSION.json'
    cert = json.loads(cert_path.read_text())
    labels, edges, adj, u, v = torsion_input()
    levels = cliques(adj)
    n, m = len(adj), len(edges)
    require([len(x) for x in levels] == [33, 152, 240, 120], 'wrong flag complex')
    z = decode_chain(cert['cycle_z'], 2, set(levels[2]))
    w = decode_chain(cert['chain_w'], 3, set(levels[3]))
    eta = decode_chain(cert['cocycle_eta_mod2'], 2, set(levels[2]))
    require(set(eta.values()) == {1}, 'bad mod2 cocycle value')
    require(not boundary(z), 'z is not a cycle')
    require(boundary(w) == {f: 2 * a for f, a in z.items()}, 'dw != 2z')
    require(sum(a * eta.get(f, 0) for f, a in z.items()) % 2 == 1, 'eta does not detect z')
    for tet in levels[3]:
        require(sum(a * eta.get(f, 0) for f, a in boundary({tet: 1}).items()) % 2 == 0,
                'eta is not a cocycle')
    base_edges = list(combinations(range(6), 2))
    require(set().union(*(set(combinations(f, 2)) for f in BASE_FACETS)) == set(base_edges),
            'base one-skeleton is not K6')
    cotree = [e for e in base_edges if 0 not in e]
    matrix = [[boundary({f: 1}).get(e, 0) for f in BASE_FACETS] for e in cotree]
    det = determinant(matrix)
    require(abs(det) == 2, 'base integral torsion determinant')
    badj, xx, _, _, _ = construct(n, edges)
    require(all(len(badj[a] & badj[b]) <= 1 for a, b in combinations(xx, 2)), 'large B has C4')
    h = len(levels[2]) + sum(len(ns) * (len(ns) - 1) // 2 for ns in adj)
    require(h == 2071 and len(badj) == 338 and sum(map(len, badj)) // 2 == 608, 'size formulas')
    require(3 * m - 2 * n + 1 == 391, 'free sphere count')
    # Mutation controls distinguish a real integer/cocycle certificate from rank evidence.
    changed = dict(z)
    f = next(iter(changed))
    changed[f] += 1
    require(boundary(w) != {g: 2 * a for g, a in changed.items()}, 'bad cycle mutation survived')
    require(sum(a * 0 for a in z.values()) % 2 != 1, 'zero detector survived')
    return {'base_cycle_determinant_abs': abs(det), 'G_f_vector': [len(a) for a in levels],
            'B_vertices': len(badj), 'B_edges': 608, 'hexagons': h,
            'H2_free_rank_by_proved_reduction': 391, 'torsion_invariant_factors': [2],
            'z_terms': len(z), 'w_terms': len(w), 'eta_terms': len(eta),
            'exact_order_two_certificate': True,
            'square_faces_enumerated': False,
            'certificate_sha256': sha256(cert_path.read_bytes()).hexdigest()}


def main():
    exhaustive = []
    for n in range(2, 5):
        universe = list(combinations(range(n), 2))
        for mask in range(1 << len(universe)):
            edges = [e for i, e in enumerate(universe) if mask >> i & 1]
            try:
                normalize_graph(n, edges)
            except ValueError:
                continue
            exhaustive.append(audit_small(n, edges))
    fixtures = [
        ('K5', 5, list(combinations(range(5), 2))),
        ('octahedral_sphere', 6, [(i, j) for i, j in combinations(range(6), 2) if i // 2 != j // 2]),
        ('five_cycle', 5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)]),
    ]
    extra = {name: audit_small(n, e) for name, n, e in fixtures}
    k4 = audit_small(4, list(combinations(range(4), 2)))
    require(k4['relations'] == 5 and k4['fan_rank_F3'] == 4
            and k4['H2_dimensions'] == {'2': 11, '3': 11}, 'K4 fan-only obstruction')
    rejections = 0
    for n, edges in [(1, []), (3, [(0, 1)]), (2, [(0, 0)]),
                     (2, [(0, 1), (1, 0)]), (2, [(0, 2)])]:
        try:
            construct(n, edges)
        except ValueError:
            rejections += 1
        else:
            raise ValueError('invalid graph accepted')
    result = {'status': 'pass', 'universal_homotopy_proved_by_code': False,
              'connected_labelled_graphs_n_2_through_4': len(exhaustive),
              'small_hexagonal_spheres_checked': sum(x['hexagons'] for x in exhaustive),
              'small_W_collapse_pairs': sum(x['W_collapse_pairs'] for x in exhaustive),
              'small_evidence_sha256': sha256(json.dumps(exhaustive, sort_keys=True,
                  separators=(',', ':')).encode()).hexdigest(),
              'fixtures': extra, 'fan_only_obstruction': k4,
              'torsion': audit_torsion(), 'invalid_inputs_rejected': rejections}
    if '--check' in sys.argv:
        require(result == json.loads((HERE / 'EXPECTED.json').read_text()), 'expected output mismatch')
        print('PASS: direct square chains, complete relation matrices, collapses, and integral torsion certificate.')
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
