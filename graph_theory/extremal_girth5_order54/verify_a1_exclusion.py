#!/usr/bin/env python3
"""Exact census and incidence controls for z12,A1 exclusion.

CPython 3.11+, standard library. This is not a 54-vertex graph search.
The accompanying written proof explains all mathematical reductions.
"""
import hashlib
import json
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from math import comb

from verify_a2_exclusion import colored_edge_packing, require


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def charged_profiles(dx):
    """Enumerate charged multiplicities, then solve four linear handshakes."""
    costs = (3, 1, 1, 3, 6, 1, 1, 3, 6)
    rows = []
    for m in range(7):
        for k in range(max(1, m)):
            if m+k > (4 if dx == 6 else 6):
                continue
            budget = 7-m-k
            for a in product(*(range(budget//c+1) for c in costs)):
                if a[0 if dx == 6 else 5] < 1 or sum(x*c for x, c in zip(a, costs)) != budget:
                    continue
                n60, n61, n64, n65, n66, n70, n73, n74, n75 = a
                rem6 = 16-sum(a[:5])
                n63 = 37+2*m-(n61+4*n64+5*n65+6*n66)-2*rem6
                n62 = rem6-n63
                rem7 = 26-sum(a[5:])
                n72 = 59-4*m-(3*n73+4*n74+5*n75)-rem7
                n71 = rem7-n72
                if min(n62, n63, n71, n72) < 0:
                    continue
                rows.append((m, k, (n60, n61, n62, n63, n64, n65, n66),
                             (n70, n71, n72, n73, n74, n75, 0, 0)))
    return sorted(rows)


@lru_cache(None)
def histograms(d, total, weight, budget):
    """Independent census: recurse over EVERY c=0,...,d, with three totals.

    No charged-type list or solved zero-cost handshake is used here.
    """
    offset = 3 if d == 6 else 1
    costs = tuple((c-offset)*(c-2)//2 for c in range(d+1))

    @lru_cache(None)
    def visit(c, n, w, b):
        if min(n, w, b) < 0 or w < c*n or w > d*n:
            return ()
        if c == d+1:
            return ((),) if n == w == b == 0 else ()
        ans = []
        for count in range(n+1):
            if count*costs[c] > b:
                break
            for rest in visit(c+1, n-count, w-c*count, b-costs[c]*count):
                ans.append((count,)+rest)
        return tuple(ans)
    return visit(0, total, weight, budget)


def direct_profiles(dx):
    rows = []
    for m in range(7):
        for k in range(max(1, m)):
            if m+k > (4 if dx == 6 else 6):
                continue
            budget = 7-m-k
            for b6 in range(budget+1):
                for six in histograms(6, 16, 37+2*m, b6):
                    for seven in histograms(7, 26, 59-4*m, budget-b6):
                        if (six if dx == 6 else seven)[0]:
                            rows.append((m, k, six, seven))
    return sorted(rows)


def profile_bounds(dx, row):
    m, k, six, seven = row
    hmax = 2 if k else (1 if m else 0)
    positive = sum(n*((c-3)*(c-2) if c < 2 else
                     (c-3)*(2*c-8) if c >= 4 else 0)
                   for c, n in enumerate(six))
    positive += sum(n*(c-3)*(2*c-7) for c, n in enumerate(seven) if c >= 4)
    lower = 15+(dx == 7)-2*m-hmax+positive
    b1 = seven[1]
    large = [(d, c) for d, counts in ((6, six), (7, seven))
             for c, n in enumerate(counts) if c >= 5 and n]
    quads = six[4]+seven[4]
    if large:
        capacities = [17-2*c if d == 6 else 11-2*c for d, c in large]
        upper = min(min(2*f, f+b1) for f in capacities)
    else:
        if quads < 2:
            b1 = 0
        upper = 9*six[4]+3*seven[4]
        if quads == 1:
            upper = min(upper, 4)
        if quads == 2:
            upper = min(upper, 9)
    upper = min(upper, (24 if dx == 7 else 28)+b1, 2*b1+seven[2])
    return lower, upper


def census():
    result = {}
    survivors = []
    for dx in (6, 7):
        rows = charged_profiles(dx)
        independent = direct_profiles(dx)
        require(rows == independent, 'entrywise comparison of independent profile censuses')
        checked = []
        for row in rows:
            m, k, six, seven = row
            sizes = sorted([c for ns in (six, seven) for c, n in enumerate(ns)
                            for _ in range(n)], reverse=True)
            require(sum(sizes[:2]) < 10, 'b22 far-size obstruction in EVERY profile')
            lower, upper = profile_bounds(dx, row)
            keep = lower <= upper
            checked.append([*row, lower, upper, keep])
            if keep:
                require(dx == 7, 'all degree-six endpoints excluded')
                survivors.append(row)
        result[str(dx)] = {
            'profiles': len(rows), 'arithmetic_excluded': sum(not r[-1] for r in checked),
            'surviving': sum(r[-1] for r in checked), 'entry_sha256': digest(rows),
            'complete_profile_table': checked
        }
    expected = sorted([
        (2, 0, (0, 0, 10, 3, 3, 0, 0), (1, 0, 24, 1, 0, 0, 0, 0)),
        (3, 0, (0, 0, 7, 7, 2, 0, 0), (1, 4, 20, 1, 0, 0, 0, 0)),
        (3, 0, (0, 0, 7, 7, 2, 0, 0), (2, 1, 23, 0, 0, 0, 0, 0)),
        (3, 0, (0, 0, 8, 5, 3, 0, 0), (1, 3, 22, 0, 0, 0, 0, 0)),
        (3, 1, (0, 0, 7, 7, 2, 0, 0), (1, 3, 22, 0, 0, 0, 0, 0)),
        (4, 0, (0, 0, 5, 9, 2, 0, 0), (1, 7, 18, 0, 0, 0, 0, 0))])
    require(sorted(survivors) == expected, 'complete six-profile terminal inventory')
    require([result[str(d)]['profiles'] for d in (6, 7)] == [17, 74], 'profile totals')
    return result, survivors


def local_signs():
    negative = set()
    records = 0
    for d in (6, 7):
        for c in range(d+1):
            for a in range(d-c+1):
                b = d-a-c
                eps = b+2*c-(8 if d == 6 else 7)
                if (d == 6 and eps > c-2) or (d == 7 and eps > c):
                    continue
                term = (c-3)*eps
                if term < 0:
                    negative.add((d, c, eps))
                if d == 6:
                    lower = (c-3)*(c-2) if c < 2 else (c-3)*(2*c-8) if c >= 4 else 0
                    require(term >= lower, 'six positive lower term')
                if d == 7 and c >= 4:
                    require(term >= (c-3)*(2*c-7), 'seven positive lower term')
                qterm = eps**2 if d == 6 else eps*(eps-1)
                require(max(-eps, 0) <= qterm, 'negative epsilon is bounded by Q')
                records += 1
    require(sorted(negative) == [(7, 1, 1), (7, 2, 1), (7, 2, 2)], 'all negative charge types')
    return {'neighbor_count_types_checked': records, 'negative_types': sorted(negative)}


def triple_bound():
    # Independent integer minimization of the convexity step for each r.
    minima = {}
    for ds in product(range(4), repeat=8):
        s = sum(ds)
        if s % 3:
            continue
        r = s//3
        value = sum(comb(d, 2) for d in ds)
        minima[r] = min(minima.get(r, value), value)
    rows = []
    for r in range(9):
        q, rem = divmod(3*r, 8)
        analytic = (8-rem)*comb(q, 2)+rem*comb(q+1, 2)
        require(minima[r] == analytic, 'convexity equals direct integer minimization')
        rows.append([r, analytic, comb(r, 2)-analytic])
    require([x[2] for x in rows] == [0, 0, 1, 2, 2, 3, 3, 3, 4], 'all-size triple bound')
    return {'integer_degree_words_checked': 4**8, 'table_r_min_intersections_max_disjoint': rows}


def bitsets(size):
    return [sum(1 << x for x in c) for c in combinations(range(12), size)]


def quad_templates():
    """Every third quad, after normalizing the first two by intersection.

    Helpers are all actual candidate high sets of sizes 2 and 3. We do not
    fix the nonsink point: every cover may repeat at most one point.
    """
    universe = (1 << 12)-1
    small = {n: bitsets(n) for n in (2, 3, 4)}
    totals = Counter()
    patterns = Counter()
    template_hist = Counter()
    transcript = []
    for second in (sum(1 << x for x in (4, 5, 6, 7)),
                   sum(1 << x for x in (0, 4, 5, 6))):
        for third in small[4]:
            qs = (15, second, third)
            if any((a & b).bit_count() > 1 for a, b in combinations(qs, 2)):
                continue
            totals['quad_configurations'] += 1
            edges = [(i, j) for i, j in combinations(range(3), 2) if qs[i] & qs[j]]
            degrees = [sum(i in e for e in edges) for i in range(3)]
            edge_count = len(edges)
            patterns[edge_count] += 1
            helpers = {n: [s for s in small[n] if all((s & q).bit_count() <= 1 for q in qs)]
                       for n in (2, 3)}
            singleton_pairs = []
            double_bad = []
            single_bad_indices = set()
            local = Counter()
            # b1 uses all three quads, or exactly two and one triple.
            if (qs[0] | qs[1] | qs[2]).bit_count() == 11:
                require(edge_count == 1, 'three-quad singleton forces single-edge pattern')
                local['b1_three_quads'] += 1
            for i, j in combinations(range(3), 2):
                for z in helpers[3]:
                    covered = qs[i] | qs[j] | z
                    if covered.bit_count() == 11:  # size sum 11: a partition
                        require(edge_count == 2 and degrees[i] == degrees[j] == 1,
                                'two-quad singleton forces leaves of path')
                        p = universe ^ covered
                        singleton_pairs.append((i, j, p, z))
                        local['b1_two_quads'] += 1
                # b2 with two selected quads and a helper of size 2 or 3.
                for size in (2, 3):
                    for u in helpers[size]:
                        covered = qs[i] | qs[j] | u
                        y = universe ^ covered
                        if y.bit_count() != 2 or any((y & q).bit_count() > 1 for q in qs):
                            continue
                        # Total far size is 10 or 11; all points of y are far-disjoint.
                        if qs[i] & qs[j]:
                            require(edge_count == 3 and not(qs[0] & qs[1] & qs[2]),
                                    'intersecting double cover forces distinct triangle')
                            require(size == 3 and not(u & (qs[i] | qs[j])),
                                    'intersecting cover has outside triple')
                            repeated = qs[i] & qs[j]
                            require(repeated.bit_count() == 1, 'unique correction point')
                            local['b2_intersecting_pair'] += 1
                        else:
                            require(edge_count == 2 and degrees[i] == degrees[j] == 1,
                                    'disjoint double cover forces path leaves')
                            other = next(t for t in range(3) if t not in (i, j))
                            outside = universe ^ (qs[i] | qs[j])
                            require((qs[other] & outside).bit_count() == 2 and
                                    (y & qs[other]).bit_count() == 1,
                                    'two-set transversal of third quad outside leaves')
                            local['b2_disjoint_pair'] += 1
                        double_bad.append((i, j, y, u))
            # b2 with a single selected quad and two triple helpers.
            for i in range(3):
                for u, v in combinations(helpers[3], 2):
                    if u & v or (u | v) & qs[i]:
                        continue
                    y = universe ^ (qs[i] | u | v)
                    if any((y & q).bit_count() > 1 for q in qs):
                        continue
                    require(y.bit_count() == 2 and degrees[i] == 2,
                            'single-quad cover needs intersections with both other quads')
                    single_bad_indices.add(i)
                    local['b2_single_quad'] += 1
            for i, j, p, z in singleton_pairs:
                for ii, jj, y, u in double_bad:
                    if (i, j) != (ii, jj):
                        continue
                    # Same triple may denote the same vertex. Distinct actual
                    # vertices with high triples must intersect at most once.
                    compatible = (y & z).bit_count() <= 1 and (u == z or (u & z).bit_count() <= 1)
                    require(not compatible, 'singleton and double-leaf bad cannot coexist')
            for pair in combinations(range(3), 2):
                ys = {y for i, j, y, u in double_bad if (i, j) == pair}
                if not (qs[pair[0]] & qs[pair[1]]):
                    require(len(ys) <= 4, 'at most four disjoint-pair bad two-sets')
            if edge_count == 3 and not(qs[0] & qs[1] & qs[2]):
                points = [qs[i] & qs[j] for i, j in edges]
                require(len(set(points)) == 3, 'fixed nonsink supports at most one triangle pair')
            if edge_count < 2:
                require(not single_bad_indices and not double_bad, 'no b2 in sparse quad pattern')
            template_hist.update(local)
            transcript.append([list(qs), edge_count, sorted(local.items())])
    require(totals['quad_configurations'] == 294, 'complete normalized quad family')
    return {'configurations': totals['quad_configurations'],
            'intersection_edge_counts': sorted(patterns.items()),
            'templates': dict(sorted(template_hist.items())), 'entry_sha256': digest(transcript)}


def terminal_arithmetic(survivors):
    records = []
    for m, k, six, seven in survivors:
        hmax = 2 if k else 1
        quads = six[4]
        base_min = 16-2*m-hmax
        if quads == 2:
            require(base_min >= 7, 'two-quad singleton exclusion')
            require(base_min+3 > 9, 'two-quad a>=1 impossible')
            if k == 0:
                require(hmax+4+3+3 < 12, 'partition requires both quads')
                require(3 < base_min, 'matching two-quad transversal contradiction')
                branch = 'matching_two_quads'
            else:
                require((m, k) == (3, 1), 'only nonmatching terminal profile')
                require(9-base_min <= 1, 'some quad has epsilon zero')
                require(8-(16-2*m-2) == 0, 'intersecting equality forces both quad epsilons zero')
                require(max(h*(4-h) for h in (1, 2)) < base_min, 'disjoint transversal contradiction')
                branch = 'path_two_quads'
        else:
            require(quads == 3 and k == 0 and m in (2, 3) and seven[1] <= 3,
                    'three-quad terminal hypotheses')
            require(base_min >= 9 and base_min+3 > 11, 'three-quad a>=1 impossible')
            require(hmax+4+3+3 < 12, 'partition needs two disjoint quads')
            require(max(0, 6, 7) < base_min, 'nontriangle at a0 contradicts charge')
            branch = 'matching_three_quads'
        records.append({'m': m, 'k': k, 'six': six, 'seven': seven,
                        'branch': branch, 'minimum_charge': base_min})
    return records


def main():
    profiles, survivors = census()
    result = {
        'claim': 'Every z12,A1 graph is impossible; combined with A<=1, all twelve high vertices are sinks',
        'proof_role': 'complete exact inventory census plus finite controls of a written incidence proof; no new solver certificate',
        'local_signs': local_signs(), 'profile_census': profiles,
        'eight_point_triple_bound': triple_bound(),
        'five_point_colored_packing': colored_edge_packing(),
        'three_quad_cover': quad_templates(),
        'terminal_profiles': terminal_arithmetic(survivors)
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
