"""Independent root-edge coefficient census and complete actual affine orbits."""
from collections import Counter
from itertools import combinations, product
from hashlib import sha256
from exact import insist, bits, mask, pairs, mul, plane, encoded
from degrees import edge_degree_graphs

PAIRS = tuple(combinations(range(16), 2))
INDEX = {p: i for i, p in enumerate(PAIRS)}


def edge_mask(edges):
    return sum(1 << INDEX[tuple(sorted(p))] for p in edges)


def pmask(w):
    return edge_mask(pairs(w))


def root_degree_graphs(n, degree):
    # Normalize only the first vertex's neighborhood; enumerate every residual edge.
    rest = tuple(range(1, n))
    neighbors = tuple(range(1, degree + 1))
    degrees = {z: degree - (z in neighbors) for z in rest}
    residual, states = edge_degree_graphs(rest, degrees, tuple(combinations(rest, 2)))
    seed = [tuple(sorted(tuple((0, z) for z in neighbors) + g)) for g in residual]
    answer = set()
    for selected in combinations(rest, degree):
        other = tuple(z for z in rest if z not in selected)
        p = (0,) + tuple(selected) + other
        for g in seed:
            answer.add(tuple(sorted(tuple(sorted((p[x], p[y]))) for x, y in g)))
    insist(len(answer) == len(seed) * len(tuple(combinations(rest, degree))), 'root neighborhood partition differs')
    insist(all(all(sum(z in e for e in g) == degree for z in range(n)) for g in answer), 'false regular graph')
    return tuple(sorted(answer)), {'root_graphs': len(seed), 'root_states': states, 'all_graphs': len(answer)}


def group():
    p = set(plane())
    out = set()
    for r, s, t, v in product(range(4), repeat=4):
        if mul(r, v) == mul(s, t):
            continue
        for conjugate in (False, True):
            f = lambda z: mul(z, z) if conjugate else z
            for h, k in product(range(4), repeat=2):
                g = tuple(4 * (mul(r, f(x)) ^ mul(s, f(y)) ^ h) +
                          (mul(t, f(x)) ^ mul(v, f(y)) ^ k)
                          for x in range(4) for y in range(4))
                insist(len(set(g)) == 16 and {mask(g[z] for z in bits(w)) for w in p} == p, 'bad affine action')
                out.add(g)
    insist(len(out) == 5760, 'affine group differs')
    # The formula defines the semilinear affine group; check closure under a spanning set too.
    generators = [tuple(z ^ h for z in range(16)) for h in (1, 2, 4, 8)]
    generators += [tuple(4 * (z % 4) + z // 4 for z in range(16)),
                   tuple(4 * (z // 4) + ((z % 4) ^ (z // 4)) for z in range(16)),
                   tuple(4 * mul(2, z // 4) + z % 4 for z in range(16)),
                   tuple(4 * (z // 4) + mul(2, z % 4) for z in range(16)),
                   tuple(4 * mul(z // 4, z // 4) + mul(z % 4, z % 4) for z in range(16))]
    insist(all(g in out for g in generators), 'generator absent')
    insist(all(tuple(g[h[z]] for z in range(16)) in out for g in out for h in generators), 'generator closure differs')
    return tuple(sorted(out))


def image_word(w, g):
    return mask(g[z] for z in bits(w))


def orbits(values, permutations, action):
    remaining = set(values)
    while remaining:
        r = min(remaining)
        orbit = {action(r, g) for g in permutations}
        insist(orbit <= remaining, 'invalid or overlapping orbit')
        remaining -= orbit
        yield r, len(orbit)


def holes(leave, hub):
    # Recognize a K4 component via one closed neighborhood, rather than enumerate cliques.
    adjacency = {}
    for i in bits(leave):
        x, y = PAIRS[i]
        if x == hub or y == hub:
            continue
        adjacency.setdefault(x, set()).add(y)
        adjacency.setdefault(y, set()).add(x)
    if not adjacency:
        return []
    z = min(adjacency)
    first = {z} | adjacency[z]
    expected_size = 4 if hub is None else 3
    if len(first) != expected_size or not all(adjacency[x] == first - {x} for x in first):
        return []
    second = set(adjacency) - first
    if len(second) != expected_size or not all(adjacency[x] == second - {x} for x in second):
        return []
    additions = (set() if hub is None else {hub})
    result = sorted((mask(first | additions), mask(second | additions)))
    insist(pmask(result[0]) & pmask(result[1]) == 0 and pmask(result[0]) | pmask(result[1]) == leave, 'false completion')
    return result


def build():
    cubic, c = root_degree_graphs(8, 3)
    cycles, d = root_degree_graphs(6, 2)
    insist(len(cubic) == 19355 and len(cycles) == 70, 'abstract graph count differs')
    p, symmetries = plane(), group()
    collinear = tuple(pmask(mask(q)) for w in p for q in combinations(tuple(bits(w)), 3))
    insist(len(set(collinear)) == 80, 'collinear triangles differ')
    groups, leaves = [], []
    for profile, abstract in enumerate((cubic, cycles)):
        supports = ({mask(s) for s in combinations(range(16), 8)} if profile == 0 else
                    {(mask(s), z) for s in combinations(range(16), 7) for z in s})
        action = image_word if profile == 0 else lambda v, g: (image_word(v[0], g), g[v[1]])
        support_cover = list(orbits(supports, symmetries, action))
        insist(len(support_cover) == (10 if profile == 0 else 25), 'support cover differs')
        for si, (r, orbit_size) in enumerate(support_cover):
            support, hub = (r, None) if profile == 0 else r
            order = tuple(bits(support if hub is None else support ^ 1 << hub))
            stabilizer = [g for g in symmetries if image_word(support, g) == support and (hub is None or g[hub] == hub)]
            insist(len(stabilizer) * orbit_size == 5760, 'support stabilizer differs')
            candidates = {edge_mask([(order[x], order[y]) for x, y in g] +
                                    ([] if hub is None else [(hub, z) for z in order])) for g in abstract}
            maps = [tuple(INDEX[tuple(sorted((g[x], g[y])))] for x, y in PAIRS) for g in stabilizer]
            local = list(orbits(candidates, maps, lambda w, g: sum(1 << g[j] for j in bits(w))))
            counts = Counter()
            for leave, size in local:
                kind = 0 if any(leave & q == q for q in collinear) else 1 if holes(leave, hub) else 2
                counts[kind] += 1
                leaves.append([len(leaves), profile, si, leave, size, kind])
            groups.append([profile, si, support, hub, orbit_size, len(stabilizer), len(candidates), len(local), [counts[k] for k in range(3)]])
    allowed = [mask(q) for q in combinations(range(16), 4) if all((mask(q) & line).bit_count() <= 2 for line in p)]
    domain = {'plane': list(p), 'groups': groups, 'leaves': leaves, 'allowed': allowed}
    raw = encoded(domain)
    insist(len(leaves) == 45100 and len(allowed) == 840 and sum(g[4] * g[6] for g in groups) == 254704450, 'complete domain totals differ')
    insist(sha256(raw).hexdigest() == 'b50acb019ad4c1244c5e37f19aebb7d2281b58874a06f1c72b3a404d47e9943f', 'entrywise domain hash differs')
    return domain, {'cubic': c, 'cycles': d, 'domain_sha256': sha256(raw).hexdigest(), 'domain_bytes': len(raw)}
