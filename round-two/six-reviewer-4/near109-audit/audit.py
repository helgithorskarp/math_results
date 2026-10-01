#!/usr/bin/env python3
"""Independent reverse-column incidence and arc-consistency Book22 audit.

No author modules are imported. Integer decisions and explicit guards survive -O.
Generated incidence lists remain local; the ordinary reductions are in REVIEW.md.
"""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
START = time.monotonic()


def need(ok, why):
    if not ok:
        raise ValueError(why)


PAIRS = list(combinations(range(5), 2))
P = [sum(1 << j for j, y in enumerate(PAIRS) if not set(x) & set(y))
     for x in PAIRS]
EDGES = list(combinations(range(10), 2))
RED = [(i, j) for i, j in EDGES if P[i] >> j & 1]
BLUE = [(i, j) for i, j in EDGES if not (P[i] >> j & 1)]
STARS = [sum(1 << i for i, x in enumerate(PAIRS) if a in x) for a in range(5)]
FULL = 1023
VECTORS = [tuple((z >> i) & 1 for i in range(10)) for z in range(1024)]
RS = [sum(1 << e for e, (i, j) in enumerate(RED) if z >> i & z >> j & 1)
      for z in range(1024)]
BS = [sum(1 << e for e, (i, j) in enumerate(BLUE) if z >> i & z >> j & 1)
      for z in range(1024)]
ISOLATED = [sum(1 << i for i in range(10)
                if (FULL ^ z) >> i & 1 and not (P[i] & (FULL ^ z)))
            for z in range(1024)]


def row_domain(delta):
    result = []
    for z in range(1024):
        k = z.bit_count()
        c = FULL ^ z
        if not 4 + delta <= k <= 8:
            continue
        if any((P[i] & c).bit_count() > (1 if delta == 0 else 2)
               for i in range(10) if c >> i & 1):
            continue
        if any(k - delta > 8 - (P[i] & c).bit_count()
               for i in range(10) if c >> i & 1):
            continue
        if any((P[i] & z).bit_count() < k - 7
               for i in range(10) if z >> i & 1):
            continue
        result.append(z)
    return result


DOM = [row_domain(d) for d in range(3)]
LOW1, LOW2 = set(DOM[1]), set(DOM[2])
HIGH = [z for z in DOM[0] if z.bit_count() > 4]
need([z for z in DOM[0] if z.bit_count() == 4] == sorted(STARS),
     'all full-degree four-rows are the five stars')


def blue_add(levels, sig):
    once, twice, thrice = levels
    if thrice & sig:
        return None
    return once | sig, twice | (once & sig), thrice | (twice & sig)


def high_multisets(max_surplus):
    groups = [[] for _ in range(max_surplus + 1)]

    def visit(start, rows, surplus, used):
        groups[surplus].append(tuple(rows))
        for j in range(start, len(HIGH)):
            z = HIGH[j]
            weight = z.bit_count() - 4
            if surplus + weight <= max_surplus and not used & RS[z]:
                visit(j, rows + [z], surplus + weight, used | RS[z])

    visit(0, [], 0, 0)
    return groups


MULTS = {}
for mu in product(range(3), repeat=5):
    values = [sum(mu[a] for a in x) for x in PAIRS]
    star_words = [z for z, count in zip(STARS, mu) for _ in range(count)]
    levels = (0, 0, 0)
    for z in star_words:
        levels = blue_add(levels, BS[z])
        need(levels is not None, 'star multiplicity cap')
    MULTS.setdefault(sum(mu), []).append((mu, values, levels))


def pair_color_possible(words, delta):
    for b, c in combinations(range(11), 2):
        red_a = (FULL ^ (words[b] | words[c])).bit_count()
        blue_a = (words[b] & words[c]).bit_count()
        if red_a > 3 and (blue_a > 5 or red_a + delta[b] + delta[c] > 6):
            return False
    return True


def incidences(groups, mode):
    low_count = 1 if mode == 'one8' else 2
    records = set()
    for surplus, group in enumerate(groups):
        if mode == 'one8' and surplus < 2:
            continue
        for high in group:
            hv = [sum(VECTORS[z][i] for z in high) for i in range(10)]
            used_red = 0
            for z in high:
                used_red |= RS[z]
            for mu, sv, star_levels in MULTS.get(11 - low_count - len(high), []):
                residual = [5 - hv[i] - sv[i] for i in range(10)]
                if any(x < 0 or x > low_count for x in residual):
                    continue
                levels = star_levels
                for z in high:
                    levels = blue_add(levels, BS[z])
                    if levels is None:
                        break
                if levels is None:
                    continue
                fixed = sum(1 << i for i, x in enumerate(residual) if x == low_count)
                if any(ISOLATED[z] & fixed for z in high):
                    continue
                if low_count == 1:
                    possibilities = [(fixed,)] if fixed in LOW2 else []
                else:
                    if RS[fixed]:
                        continue  # a red column pair would already have two misses
                    varying = sum(1 << i for i, x in enumerate(residual) if x == 1)
                    possibilities = []
                    sub = varying
                    while True:
                        a, b = fixed | sub, fixed | (varying ^ sub)
                        if a <= b and a in LOW1 and b in LOW1:
                            possibilities.append((a, b))
                        if not sub:
                            break
                        sub = (sub - 1) & varying
                for low in possibilities:
                    red, lev = used_red, levels
                    for z in low:
                        if red & RS[z]:
                            lev = None
                            break
                        red |= RS[z]
                        lev = blue_add(lev, BS[z])
                        if lev is None:
                            break
                    if lev is None:
                        continue
                    words = list(low) + list(high) + [z for z, n in zip(STARS, mu) for _ in range(n)]
                    delta = ([2] if low_count == 1 else [1, 1]) + [0] * (11 - low_count)
                    if pair_color_possible(words, delta):
                        key = (low, high, mu)
                        need(key not in records, 'reverse-column incidence is unique')
                        records.add(key)
    return sorted(records)


def literal_stars(words, delta, b, local=P, target_degrees=None):
    outside = list(range(len(words)))
    cols = [{c for c in outside if words[c] >> i & 1} for i in range(10)]
    k = words[b].bit_count()
    red_degree_b = k - delta[b] if target_degrees is None else target_degrees[b]
    result = []
    for red_points in combinations([c for c in outside if c != b], red_degree_b):
        red_set = set(red_points)
        blue_set = set(outside) - red_set - {b}
        good = True
        for i in range(10):
            if words[b] >> i & 1:
                # Actual blue neighbors: root, Z_b, E_b. Root is red to i.
                common = sum(1 for j in range(10) if j != i and words[b] >> j & 1
                             and not local[i] >> j & 1) + len(blue_set & (cols[i] - {b}))
                if common > 6:
                    good = False
                    break
            else:
                common = sum(1 for j in range(10) if not words[b] >> j & 1
                             and local[i] >> j & 1) + len(red_set - cols[i])
                if common > 3:
                    good = False
                    break
        if good:
            result.append(sum(1 << c for c in red_points))
    return result


def pair_stars(words, b, sb, c, sc):
    red = (sb >> c) & 1
    if red != ((sc >> b) & 1):
        return False
    if red:
        a = FULL ^ (words[b] | words[c])
        return a.bit_count() + (sb & sc).bit_count() <= 3
    a = words[b] & words[c]
    all_outside = (1 << len(words)) - 1
    eb = all_outside ^ (sb | (1 << b))
    ec = all_outside ^ (sc | (1 << c))
    return 1 + a.bit_count() + (eb & ec).bit_count() <= 6


def edge_completion(words, domains):
    # Arc consistency followed by an edge-color split, not vertex-star branching.
    supports = {}
    size = len(words)
    need(len(domains) == size and all(domains), 'complete nonempty outside domains')
    for b, c in combinations(range(size), 2):
        supports[b, c] = [sum(1 << j for j, sc in enumerate(domains[c])
                             if pair_stars(words, b, sb, c, sc)) for sb in domains[b]]
        supports[c, b] = [sum(1 << j for j, sb in enumerate(domains[b])
                             if pair_stars(words, b, sb, c, sc)) for sc in domains[c]]
    nodes = 0

    def visit(active):
        nonlocal nodes
        nodes += 1
        changed = True
        while changed:
            changed = False
            for b in range(size):
                for c in range(size):
                    if b == c:
                        continue
                    keep = 0
                    bits = active[b]
                    while bits:
                        bit = bits & -bits
                        j = bit.bit_length() - 1
                        if supports[b, c][j] & active[c]:
                            keep |= bit
                        bits ^= bit
                    if not keep:
                        return 0
                    if keep != active[b]:
                        active[b] = keep
                        changed = True
        for b, c in combinations(range(size), 2):
            colors = {((s >> c) & 1) for j, s in enumerate(domains[b]) if active[b] >> j & 1}
            if len(colors) == 2:
                answers = 0
                for color in (0, 1):
                    child = active[:]
                    for x, y in ((b, c), (c, b)):
                        child[x] &= sum(1 << j for j, s in enumerate(domains[x]) if ((s >> y) & 1) == color)
                    if child[b] and child[c]:
                        answers += visit(child)
                return answers
        need(all(x.bit_count() == 1 for x in active), 'all fixed edge colors uniquely determine stars')
        return 1

    solutions = visit([(1 << len(xs)) - 1 for xs in domains])
    return solutions, nodes


def digest(records):
    return hashlib.sha256(''.join(json.dumps(x, separators=(',', ':')) + '\n'
                                  for x in sorted(records)).encode()).hexdigest()


def run(max_surplus=4, export_dir=None):
    groups = high_multisets(max_surplus)
    result = {'actual_reviewer': 'six-reviewer-4', 'role': 'independent mathematical reviewer',
              'complete_surplus_range': max_surplus == 4,
              'row_domains': {str(d): {'count': len(xs), 'by_size': dict(sorted(Counter(z.bit_count() for z in xs).items()))}
                              for d, xs in enumerate(DOM)},
              'red_capped_high_multisets': list(map(len, groups)), 'cases': {}}
    for mode in ('one8', 'two9'):
        records = incidences(groups, mode)
        if export_dir:
            dest = Path(export_dir)
            dest.mkdir(parents=True, exist_ok=True)
            (dest / (mode + '.json')).write_text(json.dumps(records) + '\n')
        print(json.dumps({'phase': 'incidences', 'mode': mode, 'count': len(records),
                          'elapsed_seconds': time.monotonic() - START}), flush=True)
        empty = solutions = nodes = 0
        nonempty = []
        export_stars = []
        for key in records:
            low, high, mu = key
            words = list(low) + list(high) + [z for z, n in zip(STARS, mu) for _ in range(n)]
            delta = ([2] if mode == 'one8' else [1, 1]) + [0] * (11 - len(low))
            domains = []
            for b in range(11):
                xs = literal_stars(words, delta, b)
                if not xs:
                    empty += 1
                    break
                domains.append(xs)
            else:
                nonempty.append((key, tuple(map(len, domains))))
                if export_dir:
                    export_stars.append((key, domains))
                count, visited = edge_completion(words, domains)
                solutions += count
                nodes += visited
        if export_dir:
            (Path(export_dir) / (mode + '-stars.json')).write_text(json.dumps(export_stars) + '\n')
        result['cases'][mode] = {'incidence_records': len(records), 'incidence_sha256': digest(records),
                                'empty_star_cases': empty, 'all_stars_nonempty': len(nonempty),
                                'nonempty_domain_sizes_sha256': digest(nonempty),
                                'completions': solutions, 'arc_edge_search_nodes': nodes}
        print(json.dumps({'phase': 'complete', 'mode': mode, 'result': result['cases'][mode],
                          'elapsed_seconds': time.monotonic() - START}), flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', action='store_true')
    parser.add_argument('--max-surplus', type=int, default=4, choices=range(5))
    parser.add_argument('--export-dir')
    args = parser.parse_args()
    result = run(args.max_surplus, args.export_dir)
    canonical = json.loads(json.dumps(result))
    if args.emit:
        print(json.dumps(canonical, indent=2, sort_keys=True))
    else:
        need(args.max_surplus == 4, 'partial run supplies no complete theorem')
        need(canonical == json.loads((HERE / 'expected.json').read_text()), 'full independently expected record')
        print('PASS')
