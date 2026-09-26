#!/usr/bin/env python3
"""Exact author audit; the universal proof is PROOF.md, not this census."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools as it
import json
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inertia(matrix):
    a = [[F(x) for x in row] for row in matrix]
    require(all(len(row) == len(a) for row in a), 'not square')
    require(all(a[i][j] == a[j][i] for i in range(len(a))
                for j in range(i)), 'not symmetric')
    p = z = m = 0
    while a:
        n = len(a)
        k = next((i for i in range(n) if a[i][i]), None)
        if k is not None:
            order = [k] + [i for i in range(n) if i != k]
            a = [[a[i][j] for j in order] for i in order]
            d = a[0][0]
            p += int(d > 0)
            m += int(d < 0)
            a = [[a[i][j]-a[i][0]*a[0][j]/d
                  for j in range(1, n)] for i in range(1, n)]
        else:
            ij = next(((i, j) for i in range(n) for j in range(i)
                       if a[i][j]), None)
            if ij is None:
                z += n
                break
            i, j = ij
            order = [i, j] + [k for k in range(n) if k not in ij]
            a = [[a[i][j] for j in order] for i in order]
            d = a[0][1]
            p += 1
            m += 1
            a = [[a[i][j]-(a[i][0]*a[1][j]+a[i][1]*a[0][j])/d
                  for j in range(2, n)] for i in range(2, n)]
    return p, z, m


def sig(a):
    p, _, m = inertia(a)
    return p-m


def charpoly_inertia(a):
    """Integer Faddeev-LeVerrier and Descartes, exact for real-rooted spectra."""
    n = len(a)
    require(all(len(row) == n for row in a), 'not square')
    require(all(isinstance(x, int) for row in a for x in row), 'not integer')
    require(all(a[i][j] == a[j][i] for i in range(n)
                for j in range(i)), 'not symmetric')
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    coefficients = [1]
    for k in range(1, n+1):
        b = [[sum(a[i][h]*b[h][j] for h in range(n))
              for j in range(n)] for i in range(n)]
        trace = sum(b[i][i] for i in range(n))
        require(trace % k == 0, 'characteristic polynomial divisibility')
        c = -trace//k
        coefficients.append(c)
        for i in range(n):
            b[i][i] += c
    require(not any(x for row in b for x in row), 'Cayley-Hamilton failure')
    def variations(seq):
        signs = [1 if x > 0 else -1 for x in seq if x]
        return sum(x != y for x, y in zip(signs, signs[1:]))
    z = 0
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
        z += 1
    p = variations(coefficients)
    m = variations([x*(-1)**i for i, x in enumerate(coefficients)])
    require(p+m+z == n, 'real-root count incomplete')
    return p, z, m


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for first in range(minimum, total+1):
        for rest in partitions(total-first, first):
            yield (first,)+rest


def rooted_forms(maximum):
    forms = {1: ((),)}
    for n in range(2, maximum+1):
        out = []
        for partition in partitions(n-1):
            options = [it.combinations_with_replacement(forms[k], count)
                       for k, count in sorted(Counter(partition).items())]
            for choice in it.product(*options):
                out.append(tuple(sorted(it.chain.from_iterable(choice))))
        require(len(out) == len(set(out)), 'duplicate rooted tree')
        forms[n] = tuple(sorted(out))
    return forms


@lru_cache(None)
def state(tree):
    children = [state(t) for t in tree]
    a = F(len(tree)-1)-sum((r for _, r in children), F(0))
    require(a != 0, 'tree pivot vanished')
    return sum(s for s, _ in children)+(1 if a > 0 else -1), 1/a


def forest_state(forest):
    states = [state(t) for t in forest]
    return sum(s for s, _ in states), sum((1-r for _, r in states), F(0))


def attach(n, edges, forests):
    require(len(forests) == n, 'wrong number of forests')
    out = list(edges)
    current = n
    def add(tree, parent):
        nonlocal current
        root = current
        current += 1
        out.append((min(root, parent), max(root, parent)))
        for child in tree:
            add(child, root)
    for vertex, forest in enumerate(forests):
        for tree in forest:
            add(tree, vertex)
    return current, tuple(out)


def adjacency(n, edges):
    a = [[0]*n for _ in range(n)]
    for u, v in edges:
        require(0 <= u < v < n and a[u][v] == 0, 'invalid edge')
        a[u][v] = a[v][u] = 1
    return a


def shifted(n, edges):
    a = adjacency(n, edges)
    for i in range(n):
        a[i][i] = sum(a[i])-2
    return a


def line_matrix(edges):
    return [[int(i != j and bool(set(e) & set(f)))
             for j, f in enumerate(edges)] for i, e in enumerate(edges)]


def update(a, diagonal):
    out = [row[:] for row in a]
    for i, value in enumerate(diagonal):
        out[i][i] += value
    return out


def connected(n, edges):
    a = adjacency(n, edges)
    seen = {0}
    queue = [0]
    for v in queue:
        for w in range(n):
            if a[v][w] and w not in seen:
                seen.add(w)
                queue.append(w)
    return len(seen) == n


def hosts():
    for n in range(1, 5):
        possible = tuple(it.combinations(range(n), 2))
        for bits in it.product((0, 1), repeat=len(possible)):
            edges = tuple(e for e, bit in zip(possible, bits) if bit)
            if connected(n, edges):
                yield n, edges


def main():
    counts = Counter()
    forms = rooted_forms(11)
    expected = (1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842)
    require(tuple(map(lambda n: len(forms[n]), range(1, 12))) == expected,
            'rooted-tree census counts')
    for n, trees in forms.items():
        for tree in trees:
            s, r = state(tree)
            require(r.numerator % 2 and r.denominator % 2, 'parity')
            require(s <= 0 and (s != 0 or r == 1), 'state bound')
            require(s != -1 or r >= -1, 'minus-one bound')
            counts['rooted_trees'] += 1
            if n <= 8:
                # Build C_T directly as the non-host block of a rooted attachment.
                size, edges = attach(1, (), [(tree,)])
                full = shifted(size, edges)
                c = [row[1:] for row in full[1:]]
                p, z, m = charpoly_inertia(c)
                require(z == 0 and p-m == s, 'literal rooted inertia')
                require(inertia(c) == (p, z, m), 'inertia algorithms disagree')
                counts['literal_rooted_matrices'] += 1

    # A forest is the children of a new rooted tree. All forests through 9
    # vertices therefore occur among children of forms of order at most 10.
    forests = [t for n in range(1, 11) for t in forms[n]]
    states = sorted(set(map(forest_state, forests)))
    counts['forests_through_order9'] = len(forests)
    counts['distinct_forest_states'] = len(states)
    matrices = [[[F(x, 2)]] for x in range(-8, 9)]
    matrices += [[[a, b], [b, d]] for a, b, d in it.product(range(-2, 3), repeat=3)]
    for values in it.product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = values
        matrices.append([[a, b, c], [b, d, e], [c, e, f]])
    for a in matrices:
        n = len(a)
        base = sig(a)
        leaf = sig(update(a, [2]+[0]*(n-1)))-1
        counts['singular_local_hosts'] += int(inertia(a)[1] > 0)
        for s, d in states:
            value = s+sig(update(a, [d]+[0]*(n-1)))
            require(value <= (leaf if s == -1 else base), 'local domination')
            counts['local_domination_checks'] += 1

    small_hosts = list(hosts())
    for n, edges in small_hosts:
        a = shifted(n, edges)
        c = len(edges)-n+1
        best = -10**9
        for mask in range(1 << n):
            subset = [bool(mask >> i & 1) for i in range(n)]
            predicted = sig(update(a, [2*bit for bit in subset]))-sum(subset)-c+1
            nn, ee = attach(n, edges, [((),) if bit else () for bit in subset])
            p, _, m = charpoly_inertia(line_matrix(ee))
            require(p-m == predicted, 'leaf-subset formula')
            best = max(best, predicted)
            counts['literal_leaf_subsets'] += 1
        require(best >= sig(a)-c+1, 'empty subset missing')
        counts['hosts_all_connected_through4'] += 1

    rng = random.Random(2609261)
    options = [()] + [(t,) for k in range(1, 5) for t in forms[k]] + [((), ())]
    for case in range(180):
        n, edges = small_hosts[case % len(small_hosts)]
        forests = [rng.choice(options) for _ in range(n)]
        states_here = list(map(forest_state, forests))
        chosen = [s == -1 for s, _ in states_here]
        nn, ee = attach(n, edges, forests)
        rn, re = attach(n, edges, [((),) if bit else () for bit in chosen])
        a = shifted(n, edges)
        predicted = sum(s for s, _ in states_here)+sig(update(a, [d for _, d in states_here]))
        require(predicted == sig(shifted(nn, ee)), 'forest Schur identity')
        require(predicted <= sig(shifted(rn, re)), 'simultaneous domination')
        require(rn <= min(nn, 2*n) and len(ee)-nn == len(re)-rn, 'size or cycles')
        if case < 45:
            for size, edge_set in ((nn, ee), (rn, re)):
                p, _, m = charpoly_inertia(line_matrix(edge_set))
                require(p-m == sig(shifted(size, edge_set))-len(edge_set)+size,
                        'literal line-graph identity')
                counts['literal_multivertex_line_graphs'] += 1
        counts['simultaneous_forests'] += 1

    # The published C4--path2--C5 core shows that the leaf choice is needed.
    edges = ((0, 1), (1, 2), (2, 3), (0, 3), (4, 5), (5, 6),
             (6, 7), (7, 8), (4, 8), (0, 9), (4, 9))
    n, ee = attach(10, edges, [()] * 9 + [((),)])
    before = charpoly_inertia(line_matrix(edges))
    after = charpoly_inertia(line_matrix(ee))
    require(before[0]-before[2] == 0 and after[0]-after[2] == 1,
            'known strict leaf gain')

    # Each individual update is unfavorable, but three can cooperate in
    # an abstract symmetric host. No graph realization is asserted here.
    k = [[F(8-18*int(i == j), 27) for j in range(3)] for i in range(3)]
    require(sig(k) == -1, 'interaction host')
    for i in range(3):
        require(sig(update(k, [2*int(j == i) for j in range(3)]))-1 == -2,
                'single update control')
    require(sig(update(k, [2, 2, 2]))-3 == 0, 'three-update control')

    # Both representatives are necessary for the universal matrix envelope.
    require(sig([[1]]) > sig([[3]])-1, 'empty representative necessary')
    require(sig([[-1]]) < sig([[1]])-1, 'leaf representative necessary')
    counts['focused_controls'] = 7
    result = dict(status='VERIFIED', arithmetic='exact integers and fractions',
                  counts=dict(sorted(counts.items())),
                  known_leaf_gain=dict(before=before, after=after))
    encoded = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    result['record_sha256'] = hashlib.sha256(encoded).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
