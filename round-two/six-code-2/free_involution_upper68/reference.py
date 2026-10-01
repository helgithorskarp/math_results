"""Literal reconstruction and a second exact cover with optional rows last.

Does not import the primary carrier, solver, point-map search or joint model.
Both programs are by six-code-2; this is validation, not independent review.
"""
from collections import Counter
from itertools import combinations, permutations, product
from math import comb
from common import Guard, require


def literal_model():
    cells = tuple((r, c) for r in range(4) for c in range(4) if r != c)
    row = {r: tuple(i for i, cell in enumerate(cells) if cell[0] == r) for r in range(4)}
    column = {c: tuple(i for i, cell in enumerate(cells) if cell[1] == c) for c in range(4)}
    anchors = tuple(sorted([(12, 13, 15, 16)] + [tuple(sorted(row[r] + (15,))) for r in range(4)] +
                           [tuple(sorted(column[c] + (16,))) for c in range(4)]))
    used = Counter(p for q in anchors for p in combinations(q, 2))
    require(len(used) == 54 and set(used.values()) == {1}, 'literal anchor packing')
    eligible = tuple(sorted(set(combinations(range(15), 2)) - set(used)))
    columns = tuple(q for q in combinations(range(15), 4) if not {12, 13} <= set(q) and
                    len({cells[v][0] for v in q if v < 12}) == len([v for v in q if v < 12]) and
                    len({cells[v][1] for v in q if v < 12}) == len([v for v in q if v < 12]))
    require(len(columns) == 225 and all(set(combinations(q, 2)) <= set(eligible) for q in columns),
            'literal candidate carrier')
    return dict(cells=cells, anchors=anchors, used=frozenset(used), eligible=eligible, columns=columns)


def literal_group(data):
    lookup = {cell: i for i, cell in enumerate(data['cells'])}
    output = set()
    for rows, columns in product(tuple(permutations(range(4))), repeat=2):
        for transpose, exchange in product((False, True), repeat=2):
            moved = tuple((rows[c], columns[r]) if transpose else (rows[r], columns[c])
                          for r, c in data['cells'])
            if set(moved) != set(data['cells']):
                continue
            p = tuple(lookup[cell] for cell in moved)
            p += ((13, 12) if exchange else (12, 13)) + (14,)
            p += (16, 15) if transpose else (15, 16)
            actual = tuple(sorted(tuple(sorted(p[v] for v in q)) for q in data['anchors']))
            require(actual == data['anchors'], 'literal anchor group action')
            output.add(p)
    require(len(output) == 96, 'literal anchor group size')
    return tuple(sorted(output))


def literal_cases(data, group):
    raw = set()
    for total in range(5):
        length = total + 13
        for bars in combinations(range(length), 13):
            separators = (-1,) + bars + (length,)
            values = tuple(separators[i + 1] - separators[i] - 1 for i in range(14))
            raw.add(values + (5 - total,))
    require(len(raw) == 3060, 'stars-and-bars carrier size')
    buckets = {}
    for deficit in sorted(raw):
        images = []
        for p in group:
            inv = [0] * 15
            for v in range(15):
                inv[p[v]] = v
            images.append(tuple(deficit[inv[v]] for v in range(15)))
        key = min(images)
        buckets.setdefault(key, set()).add(deficit)
    require(len(buckets) == 108 and set().union(*buckets.values()) == raw, 'literal orbit coverage')
    output = []
    for deficit, orbit in sorted(buckets.items()):
        high = tuple(v for v, d in enumerate(deficit) if d > 0)
        budget = comb(len(high), 2) - (len(high) - 1)
        already = comb(len(high), 2) - sum(set(p) <= set(high) for p in data['eligible'])
        quota = tuple(5 - deficit[v] - sum(v in q for q in data['anchors']) for v in range(15))
        columns = tuple(q for q in data['columns'] if comb(len(set(q) & set(high)), 2) <= budget - already)
        mandatory = tuple(p for p in data['eligible'] if all(deficit[v] == 0 for v in p))
        output.append(dict(deficit=deficit, high=high, orbit_size=len(orbit), quota=quota,
                           already_high=already, covered_high_budget=budget, columns=columns,
                           mandatory=mandatory, direct=min(quota) < 0 or already > budget))
    return output


def literal_solve(case, nodes=200000, seconds=10):
    columns = tuple(case['columns'])
    pairs = tuple(frozenset(combinations(q, 2)) for q in columns)
    point_rows = [frozenset(i for i, q in enumerate(columns) if v in q) for v in range(15)]
    mandatory = frozenset(case['mandatory'])
    pair_rows = {p: frozenset(i for i, used in enumerate(pairs) if p in used) for p in mandatory}
    conflicts = [frozenset(j for j, other in enumerate(pairs) if used & other) for used in pairs]
    positive = frozenset(i for i, used in enumerate(pairs) if used & mandatory)
    available = set(range(len(columns)))
    for v, n in enumerate(case['quota']):
        if n == 0:
            available -= point_rows[v]
    guard = Guard(nodes, seconds)
    covers = []

    def remaining(active, left, selected):
        after = list(left)
        active = set(active)
        for i in selected:
            active -= conflicts[i]
            for v in columns[i]:
                after[v] -= 1
        if min(after) < 0:
            return None
        for v, n in enumerate(after):
            if n == 0:
                active -= point_rows[v]
        return frozenset(active), tuple(after)

    def optional(active, left, chosen):
        guard.tick()
        require(not (set(active) & positive), 'mandatory pair omitted before optional phase')
        if not any(left):
            covers.append(tuple(sorted(chosen)))
            return
        if any(len(active & point_rows[v]) < n for v, n in enumerate(left)):
            return
        v = min((v for v, n in enumerate(left) if n),
                key=lambda v: (comb(len(active & point_rows[v]), left[v]), v))
        for selected in combinations(sorted(active & point_rows[v]), left[v]):
            guard.tick()
            if any(pairs[i] & pairs[j] for i, j in combinations(selected, 2)):
                continue
            child = remaining(active, left, selected)
            if child is not None:
                optional(child[0], child[1], chosen + selected)

    def positive_rows(active, left, need, chosen):
        guard.tick()
        if not need:
            optional(active, left, chosen)
            return
        if any(len(active & point_rows[v]) < n for v, n in enumerate(left)):
            return
        p = min(need, key=lambda p: (len(active & pair_rows[p]), p))
        for i in sorted(active & pair_rows[p]):
            child = remaining(active, left, (i,))
            require(child is not None, 'literal active row quota inconsistency')
            positive_rows(child[0], child[1], need - pairs[i], chosen + (i,))

    positive_rows(frozenset(available), tuple(case['quota']), mandatory, ())
    require(len(set(covers)) == len(covers), 'literal duplicate covers')
    return tuple(sorted(covers)), guard.nodes


def check_point_map(first, second, mapping):
    require(len(mapping) == 17 and sorted(mapping) == list(range(17)), 'point map not bijective')
    actual = {tuple(sorted(mapping[v] for v in q)) for q in first}
    require(actual == {tuple(q) for q in second}, 'point map does not transport the actual star')


def check_group(quads, maps):
    if not any(sum(v in q for q in quads) == 4 for v in range(17)):
        require(not maps, 'unused fixture group record')
        return
    maps = tuple(tuple(p) for p in maps)
    require(len(maps) == len(set(maps)) and tuple(range(17)) in maps, 'group identity or duplicate')
    for p in maps:
        check_point_map(quads, quads, p)
    require(all(tuple(a[b[v]] for v in range(17)) in maps for a in maps for b in maps), 'fixture group closure')


def literal_involutions(quads, mate):
    tails = tuple(tuple(v for v in q if v != mate) for q in quads if mate in q)
    require(len(tails) == 4 and len({v for t in tails for v in t}) == 12, 'literal common tails')
    left = tuple(sorted(set(range(18)) - {17, mate} - {v for t in tails for v in t}))
    output = []
    for order in permutations(range(4)):
        if not all(order[i] != i and order[order[i]] == i for i in range(4)):
            continue
        paired = tuple((i, order[i]) for i in range(4) if i < order[i])
        for maps in product(*(tuple(permutations(tails[j])) for i, j in paired)):
            for partner in left[1:]:
                other = tuple(v for v in left if v not in (left[0], partner))
                g = [-1] * 18
                g[17], g[mate] = mate, 17
                for (i, j), moved in zip(paired, maps):
                    for v, w in zip(tails[i], moved):
                        g[v], g[w] = w, v
                for v, w in ((left[0], partner), other):
                    g[v], g[w] = w, v
                require(sorted(g) == list(range(18)) and all(g[g[v]] == v != g[v] for v in range(18)),
                        'literal free involution')
                output.append(tuple(g))
    require(len(output) == len(set(output)) == 324, 'literal involution carrier')
    return tuple(sorted(output))


def literal_valid(quads):
    star = tuple(tuple(sorted(q + (17,))) for q in quads)
    star_set = set(star)
    star_triples = {t for q in star for t in combinations(q, 3)}
    require(len(star_triples) == 200, 'literal first star triples')
    output = {}
    for mate in range(17):
        if sum(mate in q for q in quads) != 4:
            continue
        for g in literal_involutions(quads, mate):
            occupied = set(star_triples)
            restored = set(star)
            good = True
            for q in star:
                partner = tuple(sorted(g[v] for v in q))
                if partner in star_set:
                    continue
                triples = set(combinations(partner, 3))
                if triples & occupied:
                    good = False
                    break
                occupied |= triples
                restored.add(partner)
            if good:
                require(len(restored) == 36 and len(occupied) == 360, 'literal two-star anchor')
                output[(mate, g)] = tuple(sorted(sum(2 ** v for v in b) for b in restored))
    return output


def literal_residual(anchor, mapping, mate):
    words = [tuple(v for v in range(18) if b >> v & 1) for b in anchor]
    occupied = {t for b in words for t in combinations(b, 3)}
    rows = {}
    for word in combinations(range(18), 5):
        partner = tuple(sorted(mapping[v] for v in word))
        b, c = sum(2 ** v for v in word), sum(2 ** v for v in partner)
        if b > c:
            continue
        triples, conjugate = set(combinations(word, 3)), set(combinations(partner, 3))
        if triples & conjugate or occupied & (triples | conjugate):
            continue
        require(17 not in word and mate not in word, 'residual word containing an already saturated center')
        rows[b] = triples | conjugate
    candidates = tuple(sorted(rows))
    adjacency = tuple(sum(2 ** j for j, c in enumerate(candidates) if i != j and not rows[b] & rows[c])
                      for i, b in enumerate(candidates))
    return candidates, adjacency


def check_code(record, expected_size=62):
    words = tuple(tuple(w) for w in record['words'])
    mapping = tuple(record['involution'])
    center = record['center']
    require(len(words) == len(set(words)) == expected_size and
            all(len(w) == 5 and tuple(sorted(set(w))) == w and
                all(type(v) is int and 0 <= v < 18 for v in w) for w in words), 'invalid witness words')
    require(len(mapping) == 18 and sorted(mapping) == list(range(18)) and
            all(mapping[mapping[v]] == v != mapping[v] for v in range(18)), 'witness involution')
    require({tuple(sorted(mapping[v] for v in w)) for w in words} == set(words), 'witness not invariant')
    triples = Counter(t for w in words for t in combinations(w, 3))
    require(len(triples) == 10 * expected_size and set(triples.values()) == {1}, 'witness repeats a triple')
    require(type(center) is int and 0 <= center < 18 and sum(center in w for w in words) == 20 and
            sum(center in w and mapping[center] in w for w in words) == 4, 'witness local hypotheses')
