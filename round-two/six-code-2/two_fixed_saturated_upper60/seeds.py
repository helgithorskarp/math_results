"""Actual two-fixed-point twenty-star seeds, then exact Y-star obligations.

The complete twenty-star fixture cover is the author's previously published
free_involution_upper68 result. This file regenerates only the new fixed-point
involution interface. Pilot counts are not global code upper bounds.
"""
from pathlib import Path
from itertools import combinations, permutations, product
import json
import model as M

HERE = Path(__file__).resolve().parent


def matchings(items):
    if not items:
        yield ()
        return
    a = items[0]
    for j in range(1, len(items)):
        for rest in matchings(items[1:j] + items[j+1:]):
            yield ((a, items[j]),) + rest


def point_image(word, mapping):
    return M.mask(mapping[v] for v in M.points(word))


def maps_for_mate(quads, mate):
    tails = tuple(tuple(v for v in q if v != mate) for q in quads if mate in q)
    M.require(len(tails) == 4 and len({v for q in tails for v in q}) == 12,
              'four disjoint common tails')
    left = tuple(sorted(set(range(17)) - {mate} - {v for q in tails for v in q}))
    M.require(len(left) == 4, 'common-tail complement')
    result = []
    for pairs in matchings(tuple(range(4))):
        for moved in product(*(tuple(permutations(tails[j])) for i, j in pairs)):
            for rest in matchings(left):
                g = [-1] * 18
                g[17], g[mate] = 17, mate
                for (i, j), moved_tail in zip(pairs, moved):
                    for v, w in zip(tails[i], moved_tail):
                        g[v], g[w] = w, v
                for v, w in rest:
                    g[v], g[w] = w, v
                M.require(sorted(g) == list(range(18)) and
                          all(g[g[v]] == v for v in range(18)) and
                          {v for v in range(18) if g[v] == v} == {17, mate},
                          'actual two-fixed involution')
                result.append(tuple(g))
    M.require(len(result) == len(set(result)) == 324, '324 literal carriers')
    return tuple(sorted(result))


def normalize(mate, g, anchor):
    pairs = tuple((v, g[v]) for v in range(18) if v < g[v])
    M.require(len(pairs) == 8, 'eight moved point pairs')
    p = [-1] * 18
    for i, (v, w) in enumerate(pairs):
        p[v], p[w] = 2*i, 2*i+1
    p[17], p[mate] = 16, 17
    M.require(sorted(p) == list(range(18)) and
              all(p[g[v]] == M.G[p[v]] for v in range(18)), 'normalizing point map')
    words = tuple(sorted(point_image(w, p) for w in anchor))
    stats = M.check_code(words)
    M.require(stats['words'] == 20 and stats['fixed_words'] == 4 and
              stats['replications'][16:] == (20, 4), 'normalized twenty-star degrees')
    return tuple(p), words


def root_cases():
    data = json.loads((HERE.parent / 'free_involution_upper68' / 'fixtures.json').read_text())
    result, table = [], []
    for i, (quads, group) in enumerate(zip(data['stars'], data['groups'])):
        quads = tuple(tuple(q) for q in quads)
        anchor = tuple(sorted(M.mask(q) | (1 << 17) for q in quads))
        valid = {}
        for mate in range(17):
            if sum(mate in q for q in quads) != 4:
                continue
            for g in maps_for_mate(quads, mate):
                if {point_image(w, g) for w in anchor} == set(anchor):
                    valid[(mate, g)] = anchor
        seen, cases = set(), []
        for key in sorted(valid):
            if key in seen:
                continue
            mate, g = key
            orbit = set()
            for raw in group:
                p = tuple(raw) + (17,)
                inverse = [0] * 18
                for v, w in enumerate(p):
                    inverse[w] = v
                M.require({point_image(w, p) for w in anchor} == set(anchor),
                          'fixture supplied map not actual')
                moved = p[mate], tuple(p[g[inverse[v]]] for v in range(18))
                M.require(moved in valid, 'rooted orbit escaped actual carrier')
                orbit.add(moved)
            M.require(key in orbit and not seen & orbit, 'rooted orbit overlap')
            seen |= orbit
            p, words = normalize(mate, g, anchor)
            record = dict(fixture=i, case=len(cases), mate=mate, mapping=g,
                          point_map=p, anchor=words, raw_anchor=anchor, orbit=tuple(sorted(orbit)))
            cases.append(record)
        M.require(seen == set(valid), 'rooted carrier quotient incomplete')
        table.append(dict(fixture=i, valid=len(valid), representatives=len(cases)))
        result.extend(cases)
    M.require(tuple(r['fixture'] for r in result) == (17, 20, 22), 'three fixed roots')
    return tuple(result), table


def y_domains(anchor, resources, all_rows):
    rows = M.residual(anchor, resources, all_rows)
    fixed = tuple(r for r in rows if r['weight'] == 1 and r['replications'][17] == 1)
    paired = tuple(r for r in rows if r['weight'] == 2 and r['replications'][17] == 2)
    M.require(all(not any(w >> 16 & 1 for w in r['words']) for r in fixed + paired),
              'saturated X cannot admit further X word')
    wanted = {r['representative']: r for r in fixed}
    configurations = []
    for matching in matchings(tuple(range(8))):
        words = tuple(sorted(M.mask((2*a, 2*a+1, 2*b, 2*b+1, 17)) for a,b in matching))
        if not set(words) <= set(wanted):
            continue
        # Fixed Y words partition all sixteen non-fixed points.
        base = tuple(sorted(anchor + words))
        M.check_code(base)
        available = M.residual(base, resources, paired)
        adjacency = tuple(sum(1 << j for j, other in enumerate(available) if i != j and
                              not set(row['resources']) & set(other['resources']))
                          for i, row in enumerate(available))
        configurations.append(dict(matching=matching, fixed_words=words, rows=available,
                                   adjacency=adjacency))
    return dict(fixed_candidates=len(fixed), paired_candidates=len(paired),
                configurations=configurations, residual_rows=len(rows))


if __name__ == '__main__':
    roots, table = root_cases()
    resources, rows = M.orbit_carrier()
    output = []
    for root in roots:
        domain = y_domains(root['anchor'], resources, rows)
        configs = domain.pop('configurations')
        output.append(dict(fixture=root['fixture'], anchor=root['anchor'], **domain,
                           matchings=len(configs), paired_counts=[len(c['rows']) for c in configs]))
    print(json.dumps(dict(status='COMPLETE literal rooted domain generation', roots=output,
                          fixtures=table), sort_keys=True))
