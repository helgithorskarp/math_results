"""Complete small Ramsey(3,4) census by labeled vertex augmentation.

The augmentation and full permutation quotient follow the earlier
ramsey_r55_ten_edge_cell_obstruction artifact. No catalog is read.
"""
from itertools import combinations, permutations


def require(ok, detail):
    if not ok:
        raise ValueError(detail)


def graph(n, mask):
    adj = [0] * n
    for bit, (a, b) in enumerate(combinations(range(n), 2)):
        if mask >> bit & 1:
            adj[a] |= 1 << b
            adj[b] |= 1 << a
    return tuple(adj)


def code(adj):
    return sum(1 << bit for bit, (a, b) in enumerate(combinations(range(len(adj)), 2))
               if adj[a] >> b & 1)


def complement(adj):
    return tuple(((1 << len(adj)) - 1) ^ (1 << i) ^ s for i, s in enumerate(adj))


def valid(adj, red=3, blue=4):
    return all(not all(bool(adj[a] >> b & 1) == color for a, b in combinations(S, 2))
               for size, color in ((red, True), (blue, False))
               for S in combinations(range(len(adj)), size))


def augment(n):
    if n == 0:
        yield ()
        return
    for old in augment(n - 1):
        blue_triples = [sum(1 << v for v in S) for S in combinations(range(n - 1), 3)
                        if all(not (old[a] >> b & 1) for a, b in combinations(S, 2))]
        for size in range(min(3, n - 1) + 1):
            for S in combinations(range(n - 1), size):
                mask = sum(1 << v for v in S)
                if any(old[v] & mask for v in S):
                    continue
                if any(not (mask & T) for T in blue_triples):
                    continue
                yield tuple(old[v] | (((mask >> v) & 1) << (n - 1))
                            for v in range(n - 1)) + (mask,)


def classes(n, labeled):
    left = set(labeled)
    ranks = {e: bit for bit, e in enumerate(combinations(range(n), 2))}
    result = []
    while left:
        key = min(left)
        adj = graph(n, key)
        edges = [e for e in ranks if adj[e[0]] >> e[1] & 1]
        images = {sum(1 << ranks[tuple(sorted((p[a], p[b])))] for a, b in edges)
                  for p in permutations(range(n))}
        require(images <= left, 'full disjoint permutation orbit')
        left -= images
        result.append({'mask': key, 'edges': len(edges), 'orbit_size': len(images)})
    return result


def run():
    generated = {}
    for n in range(9):
        values = [code(adj) for adj in augment(n)]
        require(len(values) == len(set(values)), 'augmentation label uniqueness')
        generated[n] = set(values)
    brute_checks = 0
    for n in range(7):
        direct = set()
        for mask in range(1 << (n * (n - 1) // 2)):
            brute_checks += 1
            if valid(graph(n, mask)):
                direct.add(mask)
        require(direct == generated[n], 'entry-level direct/augmentation agreement')
    counts = [len(generated[n]) for n in range(9)]
    require(counts == [1, 1, 2, 7, 40, 322, 2812, 13842, 17640], 'labeled counts')
    six = classes(6, generated[6])
    eight = classes(8, generated[8])
    require(len(six) == 15 and len(eight) == 3, 'complete small types')
    return {'labeled_counts': counts, 'brute_edge_assignments': brute_checks,
            'six_classes': six, 'eight_classes': eight}
