#!/usr/bin/env python3
"""Separately written physical-spine replay; does not import gram.py."""
import argparse
import hashlib
import json
import random
from itertools import combinations
from pathlib import Path

LABELS = ((0, 1), (0, 2), (0, 3), (0, 4), (1, 2),
          (1, 3), (1, 4), (2, 3), (2, 4), (3, 4))
# Fixed independent adjacency listing, rather than a matrix-square construction.
LOCAL = ({7, 8, 9}, {5, 6, 9}, {4, 6, 8}, {4, 5, 7}, {2, 3, 9},
         {1, 3, 8}, {1, 2, 7}, {0, 3, 6}, {0, 2, 5}, {0, 1, 4})


def require(condition, message):
    if not condition:
        raise ValueError(message)


def colors(red):
    universe = set(range(len(red)))
    return [universe - ns - {i} for i, ns in enumerate(red)]


def edge(red, x, y):
    require(x != y, 'no loop')
    red[x].add(y)
    red[y].add(x)


def host(rows):
    require(len(rows) == 11, 'eleven outside points')
    red = [set() for _ in range(22)]
    for i in range(10):
        edge(red, 0, i + 1)
        for j in LOCAL[i]:
            edge(red, i + 1, j + 1)
        for b in range(11):
            if i not in rows[b]:
                edge(red, i + 1, b + 11)
    return red


def star_domain(rows):
    """All 2^10 red stars at B[0], checking its actual v/A spines only."""
    base = host(rows)
    accepted = []
    for word in range(1024):
        red = [s.copy() for s in base]
        for h in range(10):
            if (word >> h) & 1:
                edge(red, 11, 12 + h)
        blue = colors(red)
        if len(red[11]) > 10:
            continue
        if any(len((red if i in red[11] else blue)[i] &
                   (red if i in red[11] else blue)[11]) >
               (3 if i in red[11] else 6) for i in range(11)):
            continue
        accepted.append(word)
    return accepted


def cap_slacks(red):
    """Unused ordinary A-A capacities, including signed invalid controls."""
    blue = colors(red)
    return {(i, j): (3 - len(red[i + 1] & red[j + 1])
                      if j in LOCAL[i]
                      else 6 - len(blue[i + 1] & blue[j + 1]))
            for i, j in combinations(range(10), 2)}


def signed_identity_control(rows, red):
    blue = colors(red)
    columns = [{b for b, row in enumerate(rows) if i in row}
               for i in range(10)]
    require(all(len(w) == 5 for w in columns), 'control column margins')
    require(len(red[0]) == 10 and all(len(red[i + 1]) == 10
                                    for i in range(10)), 'control full degrees')
    slacks = cap_slacks(red)
    for i, j in combinations(range(10), 2):
        bound = 1 if j in LOCAL[i] else 3
        require(len(columns[i] & columns[j]) + slacks[i, j] == bound,
                'literal pair-cap identity')
    for i in range(10):
        margin = sum(slacks[min(i, j), max(i, j)]
                     for j in range(10) if j != i)
        surplus = sum(len(rows[b]) - 4 for b in columns[i])
        require(margin == 6 - surplus, 'literal F margin')
    for b, row in enumerate(rows):
        delta = 10 - len(red[b + 11])
        require(len(red[b + 11] & set(range(11, 22))) == len(row) - delta,
                'actual B degree, with signed deficit')
        require(len(blue[0] & blue[b + 11]) == 10 - len(row) + delta,
                'literal blue root identity')
    return 45 + 10 + 22


def run(primary):
    require(all((j in LOCAL[i]) == (not set(LABELS[i]) & set(LABELS[j]))
                for i in range(10) for j in range(10)),
            'fixed adjacency listing matches its ground-pair labels')
    stars = [{i for i, pair in enumerate(LABELS) if t in pair}
             for t in range(5)]
    records = []
    literal_star_words = 0
    forced_union_counts = []
    forbidden_red_pages = []
    for t in range(5):
        for a in range(10):
            if a in stars[t]:
                continue
            rows = [set(range(10)) - {a}, stars[t] | {a}]
            rows += [stars[s].copy() for s in range(5)
                     for _ in range(1 if s == t else 2)]
            base = host(rows)
            blue = colors(base)
            all_saturated = [i + 1 for i in rows[0]
                             if len(blue[11] & blue[i + 1] & set(range(1, 11))) == 6]
            require(len(all_saturated) == 3, 'all saturated physical blue spines')
            saturated = [i for i in all_saturated if t in LABELS[i - 1]]
            require(len(saturated) == 2, 'two ground-star saturated spines suffice')
            forced = set().union(*[blue[11] & blue[i] & set(range(12, 22))
                                   for i in saturated])
            require(len(forced) == 6, 'six forced neighbors')
            forced_host = [s.copy() for s in base]
            for h in forced:
                edge(forced_host, 11, h)
            pages = forced_host[11] & forced_host[a + 1]
            require(len(pages) == 5, 'five forced red pages')
            require(11 in forced_host[a + 1], 'red spine to omitted point')
            # Removing any forced edge leaves an ordinary seventh blue page.
            for h in forced:
                damaged = [s.copy() for s in forced_host]
                damaged[11].remove(h)
                damaged[h].remove(11)
                db = colors(damaged)
                require(any(len(db[11] & db[i]) >= 7 for i in saturated),
                        'a missing forced edge creates a blue book')
            domains = star_domain(rows)
            require(domains == [], 'nine-row star exclusion')
            literal_star_words += 1024
            forced_union_counts.append(len(forced))
            forbidden_red_pages.append(len(pages))
            records.append({'star': t, 'omitted': a,
                            'saturated_A_points': sorted(i - 1 for i in saturated),
                            'forced_B_points': sorted(h - 11 for h in forced),
                            'red_pages_B': sorted(h - 11 for h in pages),
                            'star_domain': domains})
    rows10 = [set(range(10))] + [stars[t].copy() for _ in range(2)
                                                    for t in range(5)]
    require(star_domain(rows10) == [1023], 'ten-row forced complete star')
    literal_star_words += 1024
    ten = host(rows10)
    for h in range(12, 22):
        edge(ten, 11, h)
    # A concrete invalid, degree-ten control. The ten four-row points have a
    # 3-regular bipartite graph, avoiding their same-star pairs.
    for t in range(5):
        for offset in (1, 2, 3):
            edge(ten, 12 + t, 17 + (t + offset) % 5)
    require(all(len(ns) == 10 for ns in ten), 'ten-row regular identity control')
    tb = colors(ten)
    duplicate_blue_pages = []
    for t in range(5):
        x, y = 12 + t, 17 + t
        require(y in tb[x], 'same-star physical pair blue')
        require(len(ten[x] & ten[y]) == 7 and len(tb[x] & tb[y]) == 7,
                'same-star literal seven pages in both colors')
        duplicate_blue_pages.append(len(tb[x] & tb[y]))

    # Arbitrary signed controls do not satisfy the book bounds or row floors.
    # Every column is sampled separately, always with exactly five misses.
    rng = random.Random(20261001)
    identity_checks = signed_identity_control(rows10, ten)
    signed_negative_capacity_controls = 0
    for _ in range(32):
        rows = [set() for _ in range(11)]
        for i in range(10):
            for b in rng.sample(range(11), 5):
                rows[b].add(i)
        red = host(rows)
        for x, y in combinations(range(11, 22), 2):
            if rng.getrandbits(1):
                edge(red, x, y)
        identity_checks += signed_identity_control(rows, red)
        signed_negative_capacity_controls += any(s < 0 for s in cap_slacks(red).values())

    fixture_bytes = primary.read_bytes()
    require(hashlib.sha256(fixture_bytes).hexdigest() ==
            '3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
            'unchanged primary21 fixture')
    array = json.loads(fixture_bytes.decode().split('\n\n', 1)[0])
    require(len(array) == 21 and all(len(row) == 21 for row in array),
            'primary21 shape')
    require(all(array[i][j] in (0, 1) and array[i][j] == array[j][i]
                for i in range(21) for j in range(21)), 'primary21 binary symmetry')
    pr = [{j for j in range(21) if i != j and array[i][j] == 0}
          for i in range(21)]
    pb = colors(pr)
    re = [(i, j) for i, j in combinations(range(21), 2) if j in pr[i]]
    be = [(i, j) for i, j in combinations(range(21), 2) if j in pb[i]]
    baseline = {'order': 21, 'red_edges': len(re), 'blue_edges': len(be),
                'max_red_pages': max(len(pr[i] & pr[j]) for i, j in re),
                'max_blue_pages': max(len(pb[i] & pb[j]) for i, j in be)}
    require(baseline == {'order': 21, 'red_edges': 93, 'blue_edges': 117,
                         'max_red_pages': 3, 'max_blue_pages': 6}, 'primary baseline')
    # Positive controls for ordinary, noninduced book predicates.
    red_k5 = [set(range(5)) - {i} for i in range(5)]
    red_k6 = [set(range(6)) - {i} for i in range(6)]
    require(len(red_k5[0] & red_k5[1]) == 3 and
            len(red_k6[0] & red_k6[1]) == 4, 'ordinary red cap boundary')
    blue_k8 = colors([set() for _ in range(8)])
    blue_k9 = colors([set() for _ in range(9)])
    require(len(blue_k8[0] & blue_k8[1]) == 6 and
            len(blue_k9[0] & blue_k9[1]) == 7, 'ordinary blue cap boundary')
    digest = hashlib.sha256(json.dumps(records, sort_keys=True,
                                       separators=(',', ':')).encode()).hexdigest()
    return {'nine_row_configurations': len(records),
            'literal_large_star_words': literal_star_words,
            'nine_row_star_domain_sizes': sorted(set(len(x['star_domain']) for x in records)),
            'forced_blue_spines': 2,
            'all_saturated_blue_spines_per_nine_row': 3,
            'forced_red_neighbor_counts': sorted(set(forced_union_counts)),
            'forced_red_page_counts': sorted(set(forbidden_red_pages)),
            'missing_forced_edge_blue_controls': 6 * len(records),
            'ten_row_star_domain': [1023],
            'ten_row_duplicate_blue_pages': duplicate_blue_pages,
            'signed_identity_controls': 33,
            'signed_identity_checks': identity_checks,
            'signed_negative_capacity_controls': signed_negative_capacity_controls,
            'ordinary_cap_boundary_controls': 4,
            'primary21': baseline,
            'physical_records_sha256': digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--primary', type=Path,
                        default=Path(__file__).with_name('primary21.txt'))
    parser.add_argument('--derive', action='store_true')
    args = parser.parse_args()
    result = run(args.primary)
    if not args.derive:
        expected = json.loads(args.expected.read_text())['literal']
        require(json.dumps(result, sort_keys=True) ==
                json.dumps(expected, sort_keys=True), 'exact expected literal result')
    print(json.dumps({'literal': result}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
