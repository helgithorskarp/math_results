#!/usr/bin/env python3
"""Independent scalar-capacity and physical-spine audit of committed8871.

Standard library only. No author code, solver, degree bound on outside
points, host catalogue, or input corpus is imported by the derivation.
"""
import argparse
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def add_edge(g, a, b):
    require(a != b, 'loop')
    g[a] |= 1 << b
    g[b] |= 1 << a


def petersen():
    # Two pentagons with spokes: inner pentagon traversed in steps of two.
    g = [0] * 10
    for i in range(5):
        add_edge(g, i, (i + 1) % 5)
        add_edge(g, 5 + i, 5 + (i + 2) % 5)
        add_edge(g, i, 5 + i)
    return g


def points(word, n):
    return [i for i in range(n) if word >> i & 1]


def blue(g):
    all_points = (1 << len(g)) - 1
    return [all_points ^ (1 << i) ^ g[i] for i in range(len(g))]


def pages(g, a, b):
    color = g if g[a] >> b & 1 else blue(g)
    return (color[a] & color[b]).bit_count()


def literal_pages(g, a, b):
    red = bool(g[a] >> b & 1)
    return sum((bool(g[a] >> h & 1) == red and
                bool(g[b] >> h & 1) == red)
               for h in range(len(g)) if h != a and h != b)


def host(p, rows):
    require(len(rows) == 11 and all(0 <= z < 1024 for z in rows),
            'eleven binary ten-point rows')
    g = [0] * 22
    for i in range(10):
        add_edge(g, 0, 1 + i)
        for j in points(p[i], 10):
            if j > i:
                add_edge(g, 1 + i, 1 + j)
        for h, z in enumerate(rows):
            if not z >> i & 1:
                add_edge(g, i + 1, h + 11)
    return g


def shape_scan():
    # Every nondecreasing integer eleven-row shape summing to50, floor4,
    # maximum10. Recursion is independent of partitioning surplus6.
    out = []

    def visit(prefix, least, left):
        count = 11 - len(prefix)
        if not count:
            if left == 0:
                out.append(prefix)
            return
        for value in range(least, 11):
            rest = left - value
            if (count - 1) * value <= rest <= (count - 1) * 10:
                visit(prefix + [value], value, rest)

    visit([], 4, 50)
    large = [s for s in out if s[-1] >= 9]
    require(large == [[4] * 10 + [10], [4] * 9 + [5, 9]],
            'exhaustive large shapes')
    return out, large


def ground_map(p):
    # Find a physical point bijection to KG(5,2) instead of presuming one.
    pairs = list(combinations(range(5), 2))
    kg = [sum(1 << j for j, b in enumerate(pairs)
              if not set(a) & set(b)) for a in pairs]
    found = []

    def search(m, used):
        i = len(m)
        if i == 10:
            found.append(m[:])
            return True
        for j in range(10):
            if j not in used and all(bool(p[i] >> h & 1) ==
                                     bool(kg[j] >> m[h] & 1)
                                     for h in range(i)):
                if search(m + [j], used | {j}):
                    return True
        return False

    require(search([], set()), 'physical Petersen to Kneser bijection')
    return pairs, found[0]


def multiplicities(stars, targets):
    # Solve any five independent-four-set column system by exact elimination,
    # then verify all ten equations. This never enumerates weak compositions.
    from fractions import Fraction
    a = [[Fraction(bool(s >> i & 1)) for s in stars] + [Fraction(targets[i])]
         for i in range(10)]
    pivot = 0
    for col in range(5):
        row = next((r for r in range(pivot, 10) if a[r][col]), None)
        require(row is not None, 'rank five of star incidence')
        a[pivot], a[row] = a[row], a[pivot]
        z = a[pivot][col]
        a[pivot] = [x / z for x in a[pivot]]
        for r in range(10):
            if r != pivot:
                z = a[r][col]
                a[r] = [x - z * y for x, y in zip(a[r], a[pivot])]
        pivot += 1
    require(all(a[r][-1] == 0 for r in range(5, 10)), 'remaining column equations')
    answer = [a[i][-1] for i in range(5)]
    require(all(x.denominator == 1 and x >= 0 for x in answer),
            'nonnegative integer multiplicity')
    return [int(x) for x in answer]


def own_rows(p):
    require(all(z.bit_count() == 3 for z in p), 'cubic')
    for i, j in combinations(range(10), 2):
        require((p[i] & p[j]).bit_count() == (0 if p[i] >> j & 1 else 1),
                'Petersen red/blue local common counts')
    pairs, mapping = ground_map(p)
    four_words = [sum(1 << i for i in s) for s in combinations(range(10), 4)]
    stars = [z for z in four_words
             if all(not (p[i] & z) for i in points(z, 10))]
    require(len(stars) == 5, 'all210 four-subsets, five independent ones')
    star_type = {}
    for z in stars:
        common = set(range(5))
        for i in points(z, 10):
            common &= set(pairs[mapping[i]])
        require(len(common) == 1, 'unique ground center of every independent set')
        star_type[z] = common.pop()
    stars.sort(key=star_type.get)
    caps = {(i, j): 1 if p[i] >> j & 1 else 3
            for i, j in combinations(range(10), 2)}
    require(sum(caps.values()) == 105, 'total pair capacity')
    require(all(sum(c for ij, c in caps.items() if i in ij) == 21
                for i in range(10)), 'off-diagonal column capacities')
    records = []
    margin_rejects = support_rejects = 0
    checks = 0
    for a in range(10):
        big = 1023 ^ (1 << a)
        for qt in combinations(range(10), 5):
            q = sum(1 << i for i in qt)
            # Total slack =105-[C(9,2)+C(5,2)+9*C(4,2)]=5.
            # Slack incident to a =21-[4*q_a+3*(5-q_a)]=6-q_a.
            incident = 6 - bool(q >> a & 1)
            if incident > 5:
                margin_rejects += 1
                continue
            virtual = q ^ (1 << a)
            if any(p[i] & virtual for i in points(virtual, 10)):
                support_rejects += 1
                continue
            require(virtual in stars, 'virtual row covered by independent-set census')
            slack = {(i, j): int((i == a and not q >> j & 1) or
                                 (j == a and not q >> i & 1))
                     for i, j in caps}
            remaining = {(i, j): c - bool(big >> i & 1 and big >> j & 1)
                          - bool(q >> i & 1 and q >> j & 1) - slack[i, j]
                         for (i, j), c in caps.items()}
            require(all(z >= 0 for z in remaining.values()), 'residual pair capacities')
            allowed = [z for z in four_words if all(remaining[i, j] > 0
                       for i, j in combinations(points(z, 10), 2))]
            require(set(allowed) == set(stars), 'literal residual four-row support')
            targets = [5 - bool(big >> i & 1) - bool(q >> i & 1)
                       for i in range(10)]
            mu = multiplicities(stars, targets)
            require(sum(mu) == 9 and sorted(mu) == [1, 2, 2, 2, 2],
                    'unique nine-row column solution')
            small = [z for z, n in zip(stars, mu) for _ in range(n)]
            rows = [big, q] + small
            require(all(sum(bool(z >> i & 1) for z in rows) == 5
                        for i in range(10)), 'all actual column margins')
            for (i, j), c in caps.items():
                observed = sum(bool(z >> i & 1 and z >> j & 1) for z in rows)
                require(observed + slack[i, j] == c, 'all45 actual pair capacities')
                checks += 1
            records.append({'omitted': a, 'star': star_type[virtual],
                            'rows': rows, 'multiplicities': mu,
                            'slack_pairs': [list(ij) for ij, s in slack.items() if s]})
    mu10 = multiplicities(stars, [4] * 10)
    require(mu10 == [2] * 5, 'unique ten-row column solution')
    rows10 = [1023] + [z for z in stars for _ in range(2)]
    for (i, j), c in caps.items():
        require(sum(bool(z >> i & 1 and z >> j & 1) for z in rows10) == c,
                'tight ten-row capacity')
    require((margin_rejects, support_rejects, len(records)) == (1260, 1230, 30),
            'complete2520 nine-row choices')
    return records, rows10, mapping, stars, checks


def star_scan(p, rows):
    base = host(p, rows)
    domains = []
    for word in range(1024):
        g = base[:]
        for j in points(word, 10):
            add_edge(g, 11, 12 + j)
        if all(pages(g, 11, i) <= (3 if g[11] >> i & 1 else 6)
               for i in range(11)):
            domains.append(word)
    return domains


def forced_argument(p, rows, star):
    g = host(p, rows)
    a = next(i for i in range(10) if not rows[0] >> i & 1)
    bblue = blue(g)
    # Find saturated blue spines from literal counts, no prescribed ground labels.
    all_sat = [i for i in points(rows[0], 10)
               if (bblue[11] & bblue[1 + i] & 2046).bit_count() == 6]
    chosen = [i for i in all_sat if star >> i & 1]
    require(len(all_sat) == 3 and len(chosen) == 2, 'saturated spine coverage')
    forced = sorted({h for i in chosen for h in range(1, 11)
                     if rows[h] >> i & 1})
    for h in forced:
        add_edge(g, 11, 11 + h)
    red_pages = points(g[11] & g[1 + a], 22)
    require(len(forced) == 6 and len(red_pages) == 5,
            'six forced edges and five actual red pages')
    controls = 0
    for h in forced:
        damaged = g[:]
        damaged[11] ^= 1 << (11 + h)
        damaged[11 + h] ^= 1 << 11
        require(any(pages(damaged, 11, i + 1) == 7 for i in chosen),
                'deleted forced edge has literal seventh blue page')
        controls += 1
    return {'omitted': a, 'chosen': chosen, 'all_saturated': all_sat,
            'forced': forced, 'red_pages': red_pages}, controls


def ten_degree_free(p, rows):
    g = host(p, rows)
    for h in range(1, 11):
        add_edge(g, 11, 11 + h)
    pair_hist = {}
    for x, y in combinations(range(12, 22), 2):
        known = (g[x] & g[y]).bit_count()
        require(known >= 4, 'all45 small-pair red edges have forbidden known pages')
        # Any other outside edges only add common red pages to this lower bound.
        damaged = g[:]
        add_edge(damaged, x, y)
        require(pages(damaged, x, y) == known == literal_pages(damaged, x, y),
                'physical forced-blue pair')
        pair_hist[known] = pair_hist.get(known, 0) + 1
    require(pair_hist == {4: 40, 7: 5}, 'all small-pair lower bounds')
    # All45 small pairs are forced blue, so this is the only possible B graph.
    require(all(pages(g, 0, x) == 9 == literal_pages(g, 0, x)
                for x in range(12, 22)), 'ten root-blue spines have nine pages')
    require(g[11].bit_count() == 10 and
            all(g[x].bit_count() == 7 for x in range(12, 22)),
            'deliberately invalid forced-star graph, no outside degree premise')
    return {'red_pair_lower_bound_histogram': pair_hist,
            'forced_blue_small_pairs': 45, 'root_blue_page_counts': [9] * 10,
            'outside_degrees_of_invalid_control': [10] + [7] * 10}


def arbitrary_controls(p):
    rng = random.Random(8871)
    pair_checks = identity_checks = negative = 0
    for _ in range(64):
        rows = [0] * 11
        for i in range(10):
            for b in rng.sample(range(11), 5):
                rows[b] |= 1 << i
        g = host(p, rows)
        for x, y in combinations(range(11, 22), 2):
            if rng.getrandbits(1):
                add_edge(g, x, y)
        for i, j in combinations(range(22), 2):
            require(pages(g, i, j) == literal_pages(g, i, j),
                    'bit oracle versus physical third-point oracle')
            pair_checks += 1
        slacks = {}
        for i, j in combinations(range(10), 2):
            red = bool(p[i] >> j & 1)
            s = (3 if red else 6) - literal_pages(g, 1 + i, 1 + j)
            observed = sum(bool(z >> i & 1 and z >> j & 1) for z in rows)
            require(observed + s == (1 if red else 3), 'signed pair identities')
            slacks[i, j] = s
            identity_checks += 1
        negative += any(s < 0 for s in slacks.values())
        for i in range(10):
            observed = sum(s for ij, s in slacks.items() if i in ij)
            surplus = sum(z.bit_count() - 4 for z in rows if z >> i & 1)
            require(observed == 6 - surplus, 'signed scalar slack margin')
            identity_checks += 1
        for b, z in enumerate(rows):
            d = g[11 + b].bit_count()
            require(literal_pages(g, 0, 11 + b) == 20 - d - z.bit_count(),
                    'blue root identity without outside max or min')
            require(d == 10 - z.bit_count() +
                    (g[11 + b] & (((1 << 22) - 1) ^ 2047)).bit_count(),
                    'literal outside degree')
            identity_checks += 2
    for n, red, expected in [(5, True, 3), (6, True, 4),
                             (8, False, 6), (9, False, 7)]:
        g = [((1 << n) - 1) ^ (1 << i) if red else 0 for i in range(n)]
        require(pages(g, 0, 1) == literal_pages(g, 0, 1) == expected,
                'ordinary cap threshold')
    return {'arbitrary_graphs': 64, 'literal_spine_comparisons': pair_checks,
            'signed_identities': identity_checks, 'negative_capacity_controls': negative,
            'ordinary_threshold_controls': 4}


def canonical_author_records(records, mapping, stars):
    # Data-only comparison formats; author algorithms are never imported.
    def normal(z):
        return sorted(mapping[i] for i in points(z, 10))
    out = []
    physical = []
    for rec in records:
        out.append({'omitted': mapping[rec['omitted']], 'star': rec['star'],
                    'rows': [normal(z) for z in rec['rows']],
                    'multiplicities': rec['multiplicities']})
        # Need the author's literal ordering, not Gram ordering: nine small
        # rows stay in ground-star order in both.
        force, _ = forced_argument(petersen(), rec['rows'], stars[rec['star']])
        physical.append({'star': rec['star'], 'omitted': mapping[rec['omitted']],
                         'saturated_A_points': sorted(mapping[i] for i in force['chosen']),
                         'forced_B_points': force['forced'],
                         'red_pages_B': sorted(x - 11 for x in force['red_pages']),
                         'star_domain': []})
    out.sort(key=lambda r: (r['omitted'], r['rows'][1]))
    physical.sort(key=lambda r: (r['star'], r['omitted']))
    return out, physical


def primary_control(path):
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
            'unchanged primary21 bytes')
    import ast
    matrix = ast.literal_eval(raw.decode().split(']]', 1)[0] + ']]')
    require(len(matrix) == 21 and all(len(row) == 21 for row in matrix),
            'primary21 shape')
    require(all(matrix[i][j] in (0, 1) and matrix[i][j] == matrix[j][i]
                for i in range(21) for j in range(21)), 'primary21 binary symmetry')
    g = [sum(1 << j for j in range(21) if i != j and matrix[i][j] == 0)
         for i in range(21)]
    red_counts, blue_counts = [], []
    for i, j in combinations(range(21), 2):
        count = literal_pages(g, i, j)
        require(count == pages(g, i, j), 'primary21 independent oracle agreement')
        (red_counts if g[i] >> j & 1 else blue_counts).append(count)
    answer = {'order': 21, 'red_edges': len(red_counts), 'blue_edges': len(blue_counts),
              'max_red_pages': max(red_counts), 'max_blue_pages': max(blue_counts)}
    require(answer == {'order': 21, 'red_edges': 93, 'blue_edges': 117,
                       'max_red_pages': 3, 'max_blue_pages': 6}, 'known positive control')
    return answer


def run():
    p = petersen()
    shapes, large = shape_scan()
    records, rows10, mapping, stars, pair_checks = own_rows(p)
    physical = []
    controls = 0
    for rec in records:
        require(star_scan(p, rec['rows']) == [], 'degree-free nine-row star domain empty')
        force, n = forced_argument(p, rec['rows'], stars[rec['star']])
        physical.append(force)
        controls += n
    require(star_scan(p, rows10) == [1023], 'no-degree-bound ten-row star domain')
    degree_free = ten_degree_free(p, rows10)
    author, author_physical = canonical_author_records(records, mapping, stars)
    summary = {'physical_to_KG_point_map': mapping,
               'all_row_size_shapes': len(shapes), 'large_row_shapes': large,
               'independent_four_sets': 5, 'four_subsets_checked': 210,
               'nine_initial_choices': 2520, 'nine_margin_rejects': 1260,
               'nine_red_support_rejects': 1230, 'nine_incidence_records': 30,
               'physical_small_pair_capacity_checks': pair_checks,
               'large_point_star_words': 31 * 1024,
               'nine_star_domains': [0] * 30, 'ten_star_domain': [1023],
               'missing_forced_edge_controls': controls,
               'degree_free_ten': degree_free,
               'ordinary_and_signed_controls': arbitrary_controls(p),
               'known_primary21': primary_control(Path(__file__).with_name('primary21.txt')),
               'own_incidence_records_sha256': digest(records),
               'own_forcing_records_sha256': digest(physical),
               'author_gram_format_sha256': digest(author),
               'author_literal_format_sha256': digest(author_physical)}
    return summary, {'incidences': records, 'forcing': physical,
                     'author_gram_format': author,
                     'author_literal_format': author_physical}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--derive', action='store_true')
    ap.add_argument('--expected', type=Path,
                    default=Path(__file__).with_name('EXPECTED.json'))
    ap.add_argument('--records', type=Path)
    args = ap.parse_args()
    summary, records = run()
    if not args.derive:
        require(json.dumps(summary, sort_keys=True) ==
                json.dumps(json.loads(args.expected.read_text()), sort_keys=True),
                'complete expected result equality')
    if args.records:
        args.records.write_text(json.dumps(records, sort_keys=True, indent=2) + '\n')
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
