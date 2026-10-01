"""Primary literal-involution carrier, pair quotient and residual bit graphs."""
from itertools import combinations, permutations, product
from common import image_word, mask, require


def matchings(items):
    if not items:
        yield ()
        return
    first = items[0]
    for i in range(1, len(items)):
        second = items[i]
        for rest in matchings(items[1:i] + items[i + 1:]):
            yield ((first, second),) + rest


def maps_for_mate(quads, mate):
    tails = tuple(tuple(v for v in q if v != mate) for q in quads if mate in q)
    require(len(tails) == 4 and len({v for t in tails for v in t}) == 12, 'four disjoint common tails')
    left = tuple(sorted(set(range(18)) - {17, mate} - {v for t in tails for v in t}))
    require(len(left) == 4, 'common-tail complement')
    output = []
    for pairs in matchings(tuple(range(4))):
        for chosen in product(*(tuple(permutations(tails[j])) for i, j in pairs)):
            for remaining in matchings(left):
                g = [-1] * 18
                g[17], g[mate] = mate, 17
                for (i, j), moved in zip(pairs, chosen):
                    for v, w in zip(tails[i], moved):
                        g[v], g[w] = w, v
                for v, w in remaining:
                    g[v], g[w] = w, v
                require(sorted(g) == list(range(18)) and all(g[g[v]] == v != g[v] for v in range(18)),
                        'invalid generated involution')
                output.append(tuple(g))
    require(len(output) == len(set(output)) == 324, 'involution carrier coverage')
    return tuple(sorted(output))


def valid_pairs(quads):
    star = tuple(mask(q) | (1 << 17) for q in quads)
    output = {}
    for mate in range(17):
        if sum(mate in q for q in quads) != 4:
            continue
        private = tuple(mask(q) for q in quads if mate not in q)
        for g in maps_for_mate(quads, mate):
            moved = tuple(image_word(q, g) for q in private)
            if any((a & b).bit_count() > 2 for a in private for b in moved):
                continue
            anchor = tuple(sorted(set(star) | {image_word(b, g) for b in star}))
            require(len(anchor) == 36 and all((a & b).bit_count() <= 2 for a, b in combinations(anchor, 2)),
                    'invalid valid-pair anchor')
            output[(mate, g)] = anchor
    return output


def pair_quotient(valid, maps):
    group = tuple(tuple(p) + (17,) for p in maps)
    seen = set()
    result = []
    for key, anchor in sorted(valid.items()):
        if key in seen:
            continue
        mate, g = key
        orbit = set()
        for p in group:
            inverse = [0] * 18
            for v, w in enumerate(p):
                inverse[w] = v
            moved = (p[mate], tuple(p[g[inverse[v]]] for v in range(18)))
            require(moved in valid, 'pair orbit escape')
            orbit.add(moved)
        require(key in orbit and not orbit & seen, 'pair orbit identity or overlap')
        seen |= orbit
        result.append(dict(mate=mate, mapping=g, anchor=anchor, orbit=tuple(sorted(orbit))))
    require(seen == set(valid), 'pair quotient incomplete')
    return result


def residual(anchor, mapping, mate):
    rows = []
    for word in combinations(tuple(v for v in range(18) if v not in (17, mate)), 5):
        b = mask(word)
        c = image_word(b, mapping)
        if b > c or (b & c).bit_count() > 2:
            continue
        if all((b & a).bit_count() <= 2 and (c & a).bit_count() <= 2 for a in anchor):
            rows.append(b)
    rows = tuple(sorted(rows))
    partners = tuple(image_word(b, mapping) for b in rows)
    adjacency = tuple(sum(1 << j for j, c in enumerate(rows) if i != j and
                          (b & c).bit_count() <= 2 and (b & partners[j]).bit_count() <= 2)
                      for i, b in enumerate(rows))
    require(all(not (adjacency[i] >> i & 1) and
                all((adjacency[i] >> j & 1) == (adjacency[j] >> i & 1) for j in range(len(rows)))
                for i in range(len(rows))), 'residual graph symmetry')
    return rows, adjacency
