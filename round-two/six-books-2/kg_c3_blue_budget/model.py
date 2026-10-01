"""Explicit KG(7,2), cyclic edge orbits, graph predicates and checked symmetry."""
from itertools import combinations, product
from collections import Counter

FULL = (1 << 22)-1
PAIRS = tuple(combinations(range(22), 2))


def need(condition, message):
    if not condition:
        raise ValueError(message)


def geometry():
    ground = (1, 2, 0, 4, 5, 3, 6)
    labels, seen = [], set()
    for pair in combinations(range(7), 2):
        if pair in seen:
            continue
        p = pair
        for _ in range(3):
            need(p not in seen, 'vertex orbit overlap')
            seen.add(p)
            labels.append(p)
            p = tuple(sorted(ground[x] for x in p))
        need(p == pair, 'vertex orbit closure')
    need(len(labels) == 21 and len(seen) == 21, 'vertex coverage')
    action = tuple(3*(i//3)+(i+1) % 3 for i in range(21))
    colors = [set(), set()]
    base = [0]*21
    for u, v in combinations(range(21), 2):
        red = set(labels[u]).isdisjoint(labels[v])
        colors[0 if red else 1].add((u, v))
        if red:
            base[u] |= 1 << v
            base[v] |= 1 << u
    orbits = []
    for edges in colors:
        seen, collection = set(), []
        for edge in sorted(edges):
            if edge in seen:
                continue
            p, orbit = edge, []
            for _ in range(3):
                need(p not in seen and p in edges, 'edge orbit coverage')
                seen.add(p)
                orbit.append(p)
                p = tuple(sorted(action[x] for x in p))
            need(p == edge, 'edge orbit closure')
            collection.append(tuple(orbit))
        need(seen == edges and len(edges) == 105 and len(collection) == 35, 'color orbit count')
        orbits.append(tuple(collection))
    need(all(r.bit_count() == 10 for r in base), 'KG degree')
    need(all((base[u] & base[v]).bit_count() == 3 for u, v in colors[0]), 'KG red pages')
    need(all((((1 << 21)-1) & ~(base[u] | base[v] | (1 << u) | (1 << v))).bit_count() == 5
             for u, v in colors[1]), 'KG blue pages')
    return labels, base, *orbits


def toggle(rows, orbit):
    for u, v in orbit:
        rows[u] ^= 1 << v
        rows[v] ^= 1 << u


def graph(g, J, P, D=()):
    labels, base, reds, blues = g
    need(len(J) == 3 and len(set(J)) == 3 and all(type(x) is int and 0 <= x < 7 for x in J), 'join domain')
    need(len(set(P)) == len(P) and all(type(x) is int and 0 <= x < 35 for x in P), 'promotion domain')
    need(len(set(D)) == len(D) and all(type(x) is int and 0 <= x < 35 for x in D), 'deletion domain')
    rows = base[:] + [0]
    for p in P:
        toggle(rows, blues[p])
    for d in D:
        toggle(rows, reds[d])
    for i in J:
        for u in range(3*i, 3*i+3):
            rows[u] |= 1 << 21
            rows[21] |= 1 << u
    return rows


def blue_bad(rows):
    for u, v in PAIRS:
        if not rows[u] >> v & 1:
            pages = FULL & ~(rows[u] | rows[v] | (1 << u) | (1 << v))
            if pages.bit_count() > 6:
                return [u, v, [w for w in range(22) if pages >> w & 1]]
    return None


def literal(g, J, P, D=()):
    """Ground disjointness/explicit sets; never decode the producer's rows."""
    labels, base, reds, blues = g
    added = {e for p in P for e in blues[p]}
    removed = {e for d in D for e in reds[d]}
    joined = {3*i+t for i in J for t in range(3)}
    rows = [set() for _ in range(22)]
    for u, v in PAIRS:
        red = u in joined if v == 21 else ((set(labels[u]).isdisjoint(labels[v]) and (u, v) not in removed) or (u, v) in added)
        if red:
            rows[u].add(v)
            rows[v].add(u)
    return rows


def literal_summary(rows):
    n = len(rows)
    universe = set(range(n))
    for u, row in enumerate(rows):
        need(u not in row and row <= universe and all(u in rows[v] for v in row), 'simple symmetric graph')
    hist = [Counter(), Counter()]
    violations = []
    for u, v in combinations(range(n), 2):
        red = v in rows[u]
        pages = sorted(w for w in range(n) if w != u and w != v and
                       ((w in rows[u] and w in rows[v]) if red else (w not in rows[u] and w not in rows[v])))
        hist[0 if red else 1][len(pages)] += 1
        if len(pages) > (3 if red else 6):
            violations.append([u, v, 'red' if red else 'blue', pages])
    return dict(vertices=n, edges=sum(map(len, rows))//2, degrees=list(map(len, rows)),
                red_pages=dict(sorted(hist[0].items())), blue_pages=dict(sorted(hist[1].items())),
                violations=violations)


def centralizer(g):
    labels, base, reds, blues = g
    keys = [{tuple(sorted(orb)): i for i, orb in enumerate(color)} for color in (reds, blues)]
    ground_action = (1, 2, 0, 4, 5, 3, 6)
    maps, vertices = [], []
    for swap, a, b in product(range(2), range(3), range(3)):
        perm = tuple(3*swap+(i+a) % 3 if i < 3 else
                     3*(1-swap)+(i-3+b) % 3 if i < 6 else 6 for i in range(7))
        need(set(perm) == set(range(7)) and all(perm[ground_action[i]] == ground_action[perm[i]] for i in range(7)), 'commuting ground permutation')
        vertex = tuple(labels.index(tuple(sorted(perm[x] for x in p))) for p in labels)
        orbit = tuple(vertex[3*i]//3 for i in range(7))
        need(all(vertex[3*i+t]//3 == orbit[i] for i in range(7) for t in range(3)), 'vertex orbit image')
        color_maps = [tuple(k[tuple(sorted(tuple(sorted(vertex[x] for x in e)) for e in orb))] for orb in source)
                      for source, k in zip((reds, blues), keys)]
        maps.append((orbit, *color_maps))
        vertices.append(vertex)
    need(len(set(vertices)) == 18 and all(tuple(v[w[i]] for i in range(21)) in vertices
                                        for v in vertices for w in vertices), 'centralizer18 closure')
    need(sum(all(m[i] == i for i in range(len(m))) for _, m, _ in maps) == 3, 'cyclic kernel')
    return maps


def choices(g, p):
    need(p in (1, 2), 'one/two-promotion scope')
    all_cases = [(J, P) for J in combinations(range(7), 3) for P in combinations(range(35), p)]
    if p == 1:
        return [(J, P, 1) for J, P in all_cases]
    maps = centralizer(g)
    counts = Counter(min((tuple(sorted(v[i] for i in J)), tuple(sorted(blue[i] for i in P)))
                         for v, red, blue in maps) for J, P in all_cases)
    need(sum(counts.values()) == 20825 and all(18 % w == 0 for w in counts.values()), 'complete case partition')
    return [(J, P, w) for (J, P), w in sorted(counts.items())]
