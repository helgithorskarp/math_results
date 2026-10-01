from paths import INPUTS, WORK
"""Actual involutions at a swapped saturated pair of multiplicity five.

six-code-2, researcher. Exact finite carrier, not a completion theorem.
The two generators use tail permutations and constrained point matchings.
"""
from itertools import combinations, permutations, product


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mask(vertices):
    return sum(1 << v for v in vertices)


def points(word):
    return tuple(v for v in range(18) if word >> v & 1)


def image(word, mapping):
    return mask(mapping[v] for v in points(word))


def matching(items):
    if not items:
        yield ()
        return
    first = items[0]
    for i in range(1, len(items)):
        for rest in matching(items[1:i] + items[i + 1:]):
            yield ((first, items[i]),) + rest


def common_tails(quads, mate):
    tails = tuple(sorted(tuple(v for v in q if v != mate) for q in quads if mate in q))
    require(len(tails) == 5 and all(len(t) == 3 for t in tails), 'five common tails')
    require(len({v for t in tails for v in t}) == 15, 'disjoint common tails')
    left = set(range(18)) - {17, mate} - {v for t in tails for v in t}
    require(len(left) == 1, 'one complement point')
    return tails, next(iter(left))


def check_map(g, tails, mate, left):
    require(tuple(sorted(g)) == tuple(range(18)) and all(g[g[v]] == v for v in range(18)),
            'actual involution required')
    require(g[17] == mate and g[mate] == 17, 'swapped star centers')
    fixed = {v for v in range(18) if g[v] == v}
    require(len(fixed) == 2 and left in fixed, 'two fixed points including complement')
    actual = {frozenset(t) for t in tails}
    require({frozenset(g[v] for v in t) for t in tails} == actual, 'common-tail action')


def tail_maps(quads, mate):
    tails, left = common_tails(quads, mate)
    result = []
    for i, fixed_tail in enumerate(tails):
        for fixed_vertex in fixed_tail:
            swapped = tuple(v for v in fixed_tail if v != fixed_vertex)
            for paired in matching(tuple(j for j in range(5) if j != i)):
                for targets in product(*(tuple(permutations(tails[b])) for a, b in paired)):
                    g = [-1] * 18
                    g[17], g[mate] = mate, 17
                    g[left], g[fixed_vertex] = left, fixed_vertex
                    g[swapped[0]], g[swapped[1]] = swapped[1], swapped[0]
                    for (a, b), target in zip(paired, targets):
                        for v, w in zip(tails[a], target):
                            g[v], g[w] = w, v
                    check_map(g, tails, mate, left)
                    result.append(tuple(g))
    require(len(result) == len(set(result)) == 1620, 'tail carrier count/uniqueness')
    return tuple(sorted(result))


def point_maps(quads, mate):
    """Pair smallest remaining point, propagating whole-tail image domains."""
    tails, left = common_tails(quads, mate)
    tail_of = {v: i for i, t in enumerate(tails) for v in t}
    result = []
    nodes = 0
    for fixed_vertex in sorted(tail_of):
        g = [-1] * 18
        g[17], g[mate] = mate, 17
        g[left], g[fixed_vertex] = left, fixed_vertex
        fixed_tail = tail_of[fixed_vertex]
        others = tuple(v for v in tails[fixed_tail] if v != fixed_vertex)
        g[others[0]], g[others[1]] = others[1], others[0]
        partners = {fixed_tail: fixed_tail}

        def visit():
            nonlocal nodes
            nodes += 1
            remaining = [v for v in tail_of if g[v] == -1]
            if not remaining:
                check_map(g, tails, mate, left)
                result.append(tuple(g))
                return
            # Assigned tail images give smaller domains and a distinct order.
            a = min(remaining, key=lambda v: (0 if tail_of[v] in partners else 1, v))
            ia = tail_of[a]
            for b in sorted(remaining):
                ib = tail_of[b]
                if ia == ib or (ia in partners and partners[ia] != ib) or (
                        ib in partners and partners[ib] != ia):
                    continue
                new = ia not in partners
                if new:
                    require(ib not in partners, 'tail-image propagation')
                    partners[ia], partners[ib] = ib, ia
                g[a], g[b] = b, a
                visit()
                g[a], g[b] = -1, -1
                if new:
                    del partners[ia], partners[ib]

        visit()
    require(len(result) == len(set(result)) == 1620, 'point carrier count/uniqueness')
    return tuple(sorted(result)), nodes


def check_code(words, g):
    require(len(words) == len(set(words)) and all(type(w) is int and 0 <= w < 1 << 18
            and w.bit_count() == 5 for w in words), 'five-set code domain')
    require(all((a & b).bit_count() <= 2 for a, b in combinations(words, 2)),
            'pairwise intersection')
    require({image(w, g) for w in words} == set(words), 'closed code')
    return tuple(sum(w >> v & 1 for w in words) for v in range(18))


def anchor(quads, mate, g):
    star = tuple(mask(q) | (1 << 17) for q in quads)
    private = tuple(w for w in star if not w >> mate & 1)
    moved = tuple(image(w, g) for w in private)
    if any((a & b).bit_count() > 2 for a in private for b in moved):
        return None
    words = tuple(sorted(set(star) | {image(w, g) for w in star}))
    reps = check_code(words, g)
    require(len(words) == 35 and reps[17] == reps[mate] == 20, 'complete two-star union')
    require(sum(w >> 17 & 1 and w >> mate & 1 for w in words) == 5, 'pair multiplicity5')
    return words


STANDARD_G = tuple(v ^ 1 if v < 16 else v for v in range(18))


def normalize(words, g, mate):
    pairs = tuple((v, g[v]) for v in range(18) if v < g[v] and v not in (17, mate))
    fixed = tuple(v for v in range(18) if g[v] == v)
    require(len(pairs) == 7 and len(fixed) == 2, 'normalization cycles')
    p = [-1] * 18
    p[17], p[mate] = 0, 1
    for j, (a, b) in enumerate(pairs, 1):
        p[a], p[b] = 2*j, 2*j+1
    for j, a in enumerate(fixed, 16):
        p[a] = j
    require(sorted(p) == list(range(18)) and all(p[g[v]] == STANDARD_G[p[v]] for v in range(18)),
            'literal conjugacy transport')
    normalized = tuple(sorted(image(w, p) for w in words))
    require(check_code(normalized, STANDARD_G)[:2] == (20, 20), 'normalized centers')
    return normalized, tuple(p)


def literal_residual(words, g=STANDARD_G, centers=(0, 1)):
    """Distinct-word orbits; genuinely fixed words are eligible."""
    actual = tuple(frozenset(points(w)) for w in words)
    eligible = set(range(18)) - set(centers)
    seen = set()
    output = []
    for five in combinations(sorted(eligible), 5):
        original = frozenset(five)
        conjugate = frozenset(g[v] for v in five)
        orbit = frozenset((original, conjugate))
        if orbit in seen:
            continue
        seen.add(orbit)
        if any(len(a & b) > 2 for a, b in combinations(orbit, 2)) or any(
                len(a & b) > 2 for a in orbit for b in actual):
            continue
        output.append(tuple(sorted(mask(w) for w in orbit)))
    return tuple(sorted(output))
