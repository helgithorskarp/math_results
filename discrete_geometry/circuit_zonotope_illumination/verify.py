#!/usr/bin/env python3
"""Exact finite corroboration of circuit illumination; CPython 3.11+, stdlib."""
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, gcd, lcm
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def vadd(a, b):
    return tuple(x+y for x, y in zip(a, b))


def smul(t, v):
    return tuple(t*x for x in v)


def rref(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return a, []
    r, pivots = 0, []
    for j in range(len(a[0])):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        t = a[r][j]
        a[r] = [x/t for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                t = a[i][j]
                a[i] = [x-t*y for x, y in zip(a[i], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    return a, pivots


def rank(rows):
    return len(rref(rows)[1])


def nullspace(rows, columns=None):
    if not rows:
        require(columns is not None, 'missing empty-matrix column count')
        return [tuple(F(i == j) for i in range(columns)) for j in range(columns)]
    a, pivots = rref(rows)
    columns = len(a[0])
    out = []
    for j in range(columns):
        if j in pivots:
            continue
        v = [F(0)]*columns
        v[j] = F(1)
        for i, k in enumerate(pivots):
            v[k] = -a[i][j]
        out.append(tuple(v))
    return out


def primitive(v):
    v = tuple(map(F, v))
    multiple = lcm(*(x.denominator for x in v))
    w = tuple(int(multiple*x) for x in v)
    divisor = gcd(*w)
    require(divisor > 0, 'zero normal')
    return tuple(x//divisor for x in w)


def symmetric_chains(n):
    """Classical recursive symmetric-chain decomposition of all subsets."""
    require(isinstance(n, int) and n >= 0, 'invalid Boolean dimension')
    chains = [[0]]
    for j in range(n):
        bit = 1 << j
        new = []
        for chain in chains:
            new.append(chain + [chain[-1] | bit])
            if len(chain) > 1:
                new.append([s | bit for s in chain[:-1]])
        chains = new
    return chains


def chain_order(chain, n):
    require(chain, 'empty chain')
    order, prev = [], 0
    for mask in chain:
        require(mask & prev == prev, 'not an increasing chain')
        order.extend(i for i in range(n) if (mask & ~prev) >> i & 1)
        prev = mask
    order.extend(i for i in range(n) if not (prev >> i & 1))
    require(sorted(order) == list(range(n)), 'not a permutation')
    return order


def circuit_system(generators):
    """Return a proved-size illuminating set; permit a lower-dimensional span."""
    require(len(generators) >= 2, 'circuit must contain at least two vectors')
    d = len(generators[0])
    require(d > 0 and all(len(g) == d for g in generators), 'shape')
    require(all(any(g) for g in generators), 'zero generator')
    n = len(generators)
    kernel = nullspace([tuple(g[i] for g in generators) for i in range(d)])
    require(len(kernel) == 1 and all(kernel[0]), 'not a linear circuit')
    alpha = kernel[0]
    v = [smul(t, g) for t, g in zip(alpha, generators)]
    oriented = [smul(1 if t > 0 else -1, g) for t, g in zip(alpha, generators)]
    require(all(sum(g[j] for g in v) == 0 for j in range(d)), 'normalization')
    directions, orders = [], []
    for chain in symmetric_chains(n):
        order = chain_order(chain, n)
        coeff = [0]*n
        for j, i in enumerate(order):
            coeff[i] = j
        w = tuple(sum(coeff[i]*v[i][j] for i in range(n)) for j in range(d))
        require(any(w), 'zero illuminating direction')
        directions.append(w)
        orders.append(order)
    require(len(directions) == comb(n, n//2), 'direction count')
    return directions, orders, oriented


def facets(generators):
    """Independent geometric route: normals orthogonal to d-1 generators."""
    d = len(generators[0])
    require(rank(generators) == d, 'not full dimensional')
    normals = set()
    for inds in combinations(range(len(generators)), d-1):
        ns = nullspace([generators[i] for i in inds], columns=d)
        if len(ns) == 1:
            normal = primitive(ns[0])
            normals.add(normal)
            normals.add(tuple(-x for x in normal))
    return sorted((u, sum(max(F(0), dot(u, g)) for g in generators)) for u in normals)


def corner_points(generators):
    points = {tuple(F(0) for _ in generators[0])}
    for g in generators:
        points |= {vadd(p, g) for p in points}
    return points


def vertex_atlas(generators):
    fs = facets(generators)
    d = len(generators[0])
    atlas = {}
    for x in corner_points(generators):
        require(all(dot(u, x) <= h for u, h in fs), 'invalid support inequality')
        active = tuple(u for u, h in fs if dot(u, x) == h)
        if rank(active) == d:
            atlas[x] = active
    require(atlas, 'empty vertex atlas')
    return fs, atlas


def geometric_cover(generators, directions, lower_witnesses=None):
    fs, atlas = vertex_atlas(generators)
    # Precompute strict signs of every actual facet normal on every direction.
    inward = [{u for u, _ in fs if dot(u, w) < 0} for w in directions]
    coverage = [[i for i, signs in enumerate(inward) if set(active) <= signs]
                for x, active in sorted(atlas.items())]
    require(all(coverage), 'unilluminated vertex')
    if lower_witnesses is not None:
        require(len(set(lower_witnesses)) == len(lower_witnesses), 'repeated lower witness')
        require(all(x in atlas for x in lower_witnesses), 'lower witness not a vertex')
        # Pairwise opposite active facet normals give a direction-independent obstruction.
        for x, y in combinations(lower_witnesses, 2):
            require(any(tuple(-z for z in u) in atlas[y] for u in atlas[x]),
                    'lower witnesses lack opposing supporting facets')
        require(len(lower_witnesses) == len(directions), 'bounds do not match')
    return {'generators': len(generators), 'dimension': len(generators[0]),
            'vertices': len(atlas), 'facets': len(fs), 'directions': len(directions),
            'incidences': sum(map(len, coverage))}


def canonical_circuit(n, varied=False):
    d = n-1
    vectors = [tuple(F(i == j) for i in range(d)) for j in range(d)]
    vectors.append(tuple(F(-1) for _ in range(d)))
    if varied:
        # Invertible triangular rational map, unequal positive lengths, and reorientations.
        M = [[F(2+i) if i == j else F(1, j+1) if i < j else F(0)
              for j in range(d)] for i in range(d)]
        vectors = [smul(F((-1)**j*(j+2), j+1), tuple(dot(row, g) for row in M))
                   for j, g in enumerate(vectors)]
    return vectors


def subset_point(gens, mask):
    return tuple(sum(gens[i][j] for i in range(len(gens)) if mask >> i & 1)
                 for j in range(len(gens[0])))


def circuit_audit(n, varied=False):
    gens = canonical_circuit(n, varied)
    directions, orders, oriented = circuit_system(gens)
    lower = [subset_point(oriented, s) for s in range(1 << n) if s.bit_count() == n//2]
    report = geometric_cover(oriented, directions, lower)
    require(report['vertices'] == (1 << n)-2, 'vertex count')
    fs, atlas = vertex_atlas(oriented)
    # Exact equality of all claimed prefix patterns with the geometric signs.
    for w, order in zip(directions, orders):
        predicted, mask = set(), 0
        for i in order[:-1]:
            mask |= 1 << i
            predicted.add(subset_point(oriented, mask))
        actual = {x for x, active in atlas.items() if all(dot(u, w) < 0 for u in active)}
        require(actual == predicted, 'chain/facet mismatch')
    report.update(n=n, varied=varied)
    return report


def tied_direction_audit(n):
    gens = canonical_circuit(n)
    _, atlas = vertex_atlas(gens)
    count = 0
    for coeff in product((-1, 0, 1), repeat=n):
        w = tuple(coeff[i]-coeff[-1] for i in range(n-1))
        actual = {s for s in range(1, (1 << n)-1)
                  if all(dot(u, w) < 0 for u in atlas[subset_point(gens, s)])}
        predicted = {s for s in range(1, (1 << n)-1)
                     if max(coeff[i] for i in range(n) if s >> i & 1)
                     < min(coeff[i] for i in range(n) if not (s >> i & 1))}
        require(actual == predicted, 'tie/strictness mismatch')
        require(sum(s.bit_count() == n//2 for s in actual) <= 1, 'middle layer capacity')
        count += 1
    return count


def cactus(block_lengths, bridges):
    """Attach every cycle or bridge at a root or preceding vertex; connected cactus."""
    edges, blocks, root, next_vertex = [], [], 0, 1
    for length in block_lengths:
        require(length >= 3, 'not a simple cycle')
        vertices = [root] + list(range(next_vertex, next_vertex+length-1))
        next_vertex += length-1
        block = []
        for u, v in zip(vertices, vertices[1:] + vertices[:1]):
            block.append(len(edges)); edges.append((u, v))
        blocks.append(block)
        root = vertices[-1]
    singletons = []
    for _ in range(bridges):
        singletons.append(len(edges)); edges.append((root, next_vertex))
        root = next_vertex; next_vertex += 1
    d = next_vertex-1
    gens = [tuple(F((u == j)-(v == j)) for j in range(1, next_vertex)) for u, v in edges]
    directions = [tuple(F(0) for _ in range(d))]
    lower = [tuple(F(0) for _ in range(d))]
    independent = []
    for block in blocks:
        g = [gens[i] for i in block]
        ds, _, oriented = circuit_system(g)
        ws = [subset_point(oriented, s) for s in range(1 << len(g))
              if s.bit_count() == len(g)//2]
        # Orientations might translate the factor; build all geometry consistently below.
        for i, new_g in zip(block, oriented):
            gens[i] = new_g
        directions = [vadd(a, b) for a in directions for b in ds]
        lower = [vadd(a, b) for a in lower for b in ws]
        independent.extend(g[:-1])
    for i in singletons:
        g = gens[i]
        directions = [vadd(a, smul(sign, g)) for a in directions for sign in (-1, 1)]
        lower = [vadd(a, smul(sign, g)) for a in lower for sign in (0, 1)]
        independent.append(g)
    require(rank(independent) == d == len(independent), 'not a direct circuit decomposition')
    report = geometric_cover(gens, directions, lower)
    expected = 2**bridges
    for length in block_lengths:
        expected *= comb(length, length//2)
    require(report['directions'] == expected, 'cactus formula')
    report.update(cycles=block_lengths, bridges=bridges)
    return report


def summand_audit(n):
    # Hamiltonian cycle in K_n: full-dimensional circuit summand of its graphical zonotope.
    cycle = [(i, (i+1) % n) for i in range(n)]
    edges = cycle + [(i, j) for i in range(n) for j in range(i+1, n)
                     if (i, j) not in cycle and (j, i) not in cycle]
    gens = [tuple(F((i == k)-(j == k)) for k in range(1, n)) for i, j in edges]
    ds, _, _ = circuit_system(gens[:n])
    result = geometric_cover(gens, ds)
    result['complete_graph_order'] = n
    return result


def main():
    scd = []
    for n in range(2, 13):
        chains = symmetric_chains(n)
        flat = [s for c in chains for s in c]
        require(len(flat) == 1 << n and set(flat) == set(range(1 << n)), 'SCD partition')
        for c in chains:
            require(c[0].bit_count()+c[-1].bit_count() == n, 'not symmetric')
            require(all(a & b == a and b.bit_count() == a.bit_count()+1
                        for a, b in zip(c, c[1:])), 'not saturated')
        require(len(chains) == comb(n, n//2), 'not an optimal chain count')
        scd.append({'n': n, 'chains': len(chains), 'subsets': len(flat)})
    circuits = [circuit_audit(n) for n in range(2, 8)]
    circuits += [circuit_audit(n, varied=True) for n in range(3, 7)]
    ties = sum(tied_direction_audit(n) for n in range(2, 5))
    products = [cactus(cs, b) for cs, b in [((), 3), ((3,), 1), ((3, 3), 0),
                                          ((3, 4), 1), ((4, 4), 0)]]
    summands = [summand_audit(n) for n in (4, 5)]
    rejected = 0
    for bad in [[(0, 0), (1, 0), (0, 1)], [(1, 0), (2, 0), (0, 1)],
                [(1, 0), (0, 1)], [(1, 0), (0, 1, 0), (-1, -1)]]:
        try:
            circuit_system(bad)
        except ValueError:
            rejected += 1
    require(rejected == 4, 'invalid circuit controls')
    # Edge-disjoint cycles need not have linearly independent spans: two squares in K_2,4.
    edge_sets = [[(0, 2), (2, 1), (1, 3), (3, 0)],
                 [(0, 4), (4, 1), (1, 5), (5, 0)]]
    blocks = [[tuple(F((u == k)-(v == k)) for k in range(1, 6)) for u, v in es]
              for es in edge_sets]
    require([rank(g) for g in blocks] == [3, 3] and rank(blocks[0]+blocks[1]) == 5,
            'direct-span negative control')
    evidence = {'symmetric_chains': scd, 'circuit_geometry': circuits, 'tied_directions': ties,
                'cactus_geometry': products, 'summand_geometry': summands,
                'invalid_circuits_rejected': rejected,
                'edge_disjoint_nondirect_ranks': [3, 3, 5]}
    raw = json.dumps(evidence, sort_keys=True, separators=(',', ':')).encode()
    report = {'status': 'VERIFIED', 'payload_sha256': hashlib.sha256(raw).hexdigest(),
              'evidence': evidence}
    print(json.dumps(report, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
