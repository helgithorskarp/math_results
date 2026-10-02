"""Independent ground-set discovery and pure J/P/D graph constructor."""
from itertools import combinations

def geometry():
    """Independent ground-set construction, including native orbit discovery."""
    sigma = {0: 1, 1: 2, 2: 0, 3: 4, 4: 5, 5: 3, 6: 6}
    unseen = {frozenset(x) for x in combinations(range(7), 2)}
    labels = []
    while unseen:
        pair = min(unseen, key=lambda s: tuple(sorted(s)))
        for _ in range(3):
            if pair not in unseen:
                raise ValueError('native vertex orbit overlaps')
            unseen.remove(pair)
            labels.append(pair)
            pair = frozenset(sigma[x] for x in pair)
    images = [labels.index(frozenset(sigma[x] for x in s)) for s in labels]
    orbits = []
    for red in (True, False):
        unseen_edges = {e for e in combinations(range(21), 2)
                        if labels[e[0]].isdisjoint(labels[e[1]]) == red}
        color = []
        while unseen_edges:
            edge = min(unseen_edges)
            orbit = []
            for _ in range(3):
                if edge not in unseen_edges:
                    raise ValueError('native edge orbit overlaps')
                unseen_edges.remove(edge)
                orbit.append(edge)
                edge = tuple(sorted(images[v] for v in edge))
            color.append(tuple(orbit))
        orbits.append(tuple(color))
    return labels, orbits


def rows(native, J, additions, deletions):
    labels, (reds, blues) = native
    removed = {e for d in deletions for e in reds[d]}
    added = {e for p in additions for e in blues[p]}
    joined = {3*i+t for i in J for t in range(3)}
    rows = [set() for _ in range(22)]
    for u, v in combinations(range(22), 2):
        red = u in joined if v == 21 else (
            (labels[u].isdisjoint(labels[v]) and (u, v) not in removed)
            or (u, v) in added)
        if red:
            rows[u].add(v)
            rows[v].add(u)
    return rows
