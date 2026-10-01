"""Small rooted census for validation of a known classification, not a proof premise.

Actual author six-books-3, researcher. Python 3.11 standard library.
Edges on six tail points use lexicographic combinations(range(6), 2).
"""
from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, permutations

PAIRS = list(combinations(range(6), 2))
INDEX = {p: i for i, p in enumerate(PAIRS)}


def transform(mask, mapping):
    return sum(1 << mapping[i] for i in range(15) if mask >> i & 1)


def normalizations():
    maps = [tuple(INDEX[tuple(sorted((p[a], p[b])))] for a, b in PAIRS)
            for p in permutations(range(6))]
    normal = {}
    for triplet in combinations_with_replacement(range(15), 3):
        images = [tuple(sorted(m[i] for i in triplet)) for m in maps]
        best = min(images)
        normal[triplet] = (best, [k for k, image in enumerate(images) if image == best])
    return maps, normal


def graph_for(triplet, tail):
    adj = [0] * 10
    edges = [(0, i) for i in range(1, 4)]
    edges += [(v, a + 4) for v, e in enumerate(triplet, 1) for a in PAIRS[e]]
    edges += [(a + 4, b + 4) for i, (a, b) in enumerate(PAIRS) if tail >> i & 1]
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj


def rooted_key(adj, root, maps, normal):
    neighbors = [i for i in range(10) if adj[root] >> i & 1]
    rest = [i for i in range(10) if i != root and i not in neighbors]
    ri = {v: i for i, v in enumerate(rest)}
    triplet = tuple(sorted(INDEX[tuple(sorted(ri[j] for j in rest
                                             if adj[v] >> j & 1))]
                           for v in neighbors))
    tail = sum(1 << INDEX[(a, b)] for a, b in PAIRS
               if adj[rest[a]] >> rest[b] & 1)
    rep, indices = normal[triplet]
    return rep, min(transform(tail, maps[k]) for k in indices)


def enumerate_cores():
    maps, normal = normalizations()
    reps = sorted(set(rep for rep, _ in normal.values()))
    rooted = {}
    profiles = []
    for rep in reps:
        degrees = [3] * 6
        for e in rep:
            for a in PAIRS[e]:
                degrees[a] -= 1
        stabilizer = normal[rep][1]
        orbits = Counter()
        allowed = [e for e in range(15) if e not in rep]
        for chosen in combinations(allowed, 6):
            d = [0] * 6
            for e in chosen:
                a, b = PAIRS[e]
                d[a] += 1
                d[b] += 1
            if d != degrees:
                continue
            tail = sum(1 << e for e in chosen)
            adj = graph_for(rep, tail)
            if any(adj[a] & adj[b] for a in range(10) for b in range(a + 1, 10)
                   if adj[a] >> b & 1):
                continue
            canon = min(transform(tail, maps[k]) for k in stabilizer)
            orbits[canon] += 1
        for tail in sorted(orbits):
            rooted[(rep, tail)] = graph_for(rep, tail)
        assignments = 6
        for multiplicity in Counter(rep).values():
            for factor in range(2, multiplicity + 1):
                assignments //= factor
        profiles.append({'triplet': list(rep), 'stabilizer': len(stabilizer),
                         'tails': sum(orbits.values()), 'rooted_classes': len(orbits),
                         'cross_labeled_count': 720 // len(stabilizer) * assignments})
    classes = defaultdict(list)
    for key, adj in rooted.items():
        canon = min(rooted_key(adj, root, maps, normal) for root in range(10))
        classes[canon].append(key)
    cores = [{'key': [list(key[0]), key[1]], 'neighbors': graph_for(*key),
              'rooted_classes': len(roots)} for key, roots in sorted(classes.items())]
    return {'profiles': profiles, 'rooted_classes': len(rooted), 'unrooted_classes': len(cores),
            'normalized_labeled_count': sum(p['tails'] * p['cross_labeled_count']
                                            for p in profiles), 'cores': cores}
