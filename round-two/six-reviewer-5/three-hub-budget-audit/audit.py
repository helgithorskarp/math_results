"""Independent necessary-domain audit, written after a sealed first checker.

The first checker was run before any researcher executable was read.
Coarse59 states suffice for exclusion. Refined74 states independently
reconstruct the author's extra isolation flags for whole-record comparison.
Neither representation enumerates actual ambient codes.
"""
from collections import Counter
from itertools import combinations, permutations, product
import hashlib
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()).hexdigest()


def canonical(n, edges):
    return min(tuple(sorted(tuple(sorted((p[a], p[b]))) for a, b in edges))
               for p in permutations(range(n)))


def positive_compositions(total, length):
    if length == 1:
        if total > 0:
            yield (total,)
    elif length > 1:
        for first in range(1, total-length+2):
            for tail in positive_compositions(total-first, length-1):
                yield (first,)+tail


def unit_types(fixtures):
    require(len(fixtures) == 23, 'complete credited generic fixture input')
    records, classes, seen = [], set(), set()
    for index, quads in enumerate(fixtures):
        require(len(quads) == 20 and all(len(q) == len(set(q)) == 4 and
                all(type(p) is int and 0 <= p < 17 for p in q) for q in quads), 'literal quadruple domain')
        key = tuple(sorted(tuple(sorted(q)) for q in quads))
        require(key not in seen, 'duplicate fixture'); seen.add(key)
        pairs = Counter(p for q in quads for p in combinations(sorted(q), 2))
        degrees = Counter(p for q in quads for p in q)
        require(len(pairs) == 120 and max(pairs.values()) == 1, 'repeated fixture pair')
        high = sorted(p for p in range(17) if degrees[p] < 5)
        require(all(degrees[p] <= 5 for p in range(17)), 'fixture point cap')
        require(not any(degrees[a] == degrees[b] == 5 and (a, b) not in pairs
                        for a, b in combinations(range(17), 2)), 'low-low fixture leave')
        if sorted(5-degrees[p] for p in high) != [1]*5:
            continue
        edges = tuple((a, b) for a, b in combinations(range(5), 2)
                      if tuple(sorted((high[a], high[b]))) not in pairs)
        require(len(edges) == 4, 'unit high-leave count')
        form = canonical(5, edges); classes.add(form)
        records.append({'fixture': index, 'high': high, 'edges': edges, 'canonical': form})
    require([r['fixture'] for r in records] == [11, 15, 16, 17, 19, 20, 21, 22]
            and len(classes) == 4, 'complete eight unit fixtures/four graph classes')
    check_charge(classes)
    return classes, records


def check_charge(classes):
    for edges in classes:
        for marks in combinations(range(5), 2):
            require(sum(bool(set(e)&set(marks)) for e in edges) >= 2,
                    'unit two-hub charge below two')


def flags(delta, edges, marks):
    degree = Counter(v for e in edges for v in e)
    h = len(delta)
    return tuple(int(v >= 0 and degree[v] == 0 and
                     (h == 5 and delta[v] == 1 or h == 4 and delta[v] == 2)) for v in marks)


def derive_rows(classes):
    refined = set()
    for h in range(1, 6):
        for edges in combinations(tuple(combinations(range(h), 2)), h-1):
            if h == 5 and canonical(h, edges) not in classes:
                continue
            # All ordered positive compositions retain every deficit placement.
            for delta in positive_compositions(5, h):
                for marks in product(range(-1, h), repeat=3):
                    present = tuple(v for v in marks if v >= 0)
                    if len(set(present)) != len(present):
                        continue
                    q = sum(any(v in e for v in present) for e in edges)
                    e = 5-h
                    if e+q > 3:
                        continue
                    d = tuple(delta[v] if v >= 0 else 0 for v in marks)
                    refined.add(d+(e, q, h-len(present))+flags(delta, edges, marks))
    coarse = {r[:6] for r in refined}
    return tuple(sorted(coarse)), tuple(sorted(refined))


def inventory(rows, multiplicities, profile, t):
    started = time.monotonic()
    a, b, c = multiplicities
    P = a+b+c
    D = tuple(75-4*profile[i]+P-(c, b, a)[i] for i in range(3))
    budget = 3*P-15-t
    require(P in (5, 6) and t in (0, 1), 'bounded boundary domain')
    bases = {r[:3]: r for r in rows if r[3]+r[4] == 0}
    require(set(bases) == {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}, 'complete four zero-cost fillers')
    positive = tuple(r for r in rows if r[3]+r[4] > 0)
    records, counts = [], Counter()

    def visit(chosen, start, cost, accumulated):
        require(time.monotonic()-started < 20, 'INCOMPLETE inventory guard')
        remaining = tuple(D[i]-accumulated[i] for i in range(3))
        unmarked = 15-len(chosen)-sum(remaining)
        if min(remaining) >= 0 and unmarked >= 0:
            total = list(chosen)+[bases[(0, 0, 0)]]*unmarked
            for i, amount in enumerate(remaining):
                key = tuple(int(i == j) for j in range(3))
                total.extend([bases[key]]*amount)
            require(len(total) == 15, 'whole saturated row count')
            E = sum(r[3] for r in total); Q = sum(r[4] for r in total)
            cross_excess = sum(sum(max(v-1, 0) for v in r[:3]) for r in total)
            ss_excess = sum(5-sum(r[:3])-r[5] for r in total)
            require(ss_excess == E-cross_excess and ss_excess >= 0, 'literal row excess conservation')
            if ss_excess % 2 or (budget-cost) % 2:
                counts['parity'] += 1
            else:
                X = ss_excess//2
                low = tuple(sum(r[i] == r[j] == 0 for r in total) for i, j in ((0, 1), (0, 2), (1, 2)))
                if len(rows[0]) == 9:
                    good = tuple(sum(r[5] for r in total if r[6+i]) for i in range(3))
                else:
                    good = tuple(sum(r[5] for r in total if r[i] > 0 and
                                     sum(v > 0 for v in r[:3]) == 1 and r[4] == 0) for i in range(3))
                # First independently prove X=0 at budget<=3. The shared-hub
                # lemmas apply to unit SS edges, so no X>0 cohort is used.
                require(X == 0, 'SS excess survives: no cohort exclusion licensed')
                require(all((r[3] == 0 and max(r[:3]) == 1 or
                             r[3] == 1 and max(r[:3]) == 2)
                            for r in total if sum(v > 0 for v in r[:3]) == 1 and r[4] == 0),
                        'coarse isolated cohort outside exact shared-hub scopes')
                counts['budget_valid'] += 1
                reason = ('low_pair_cut' if any(L > 3*m-t for L, m in zip(low, (a, b, c))) else
                          'independent_cohort_cut' if max(good) > 35-P else 'survivor')
                counts[reason] += 1
                records.append({'exceptional_rows': chosen, 'base_counts': (unmarked,)+remaining,
                                'E': E, 'Q': Q, 'X': X, 'low_pair_counts': low,
                                'good_cohort_degrees': good, 'reason': reason})
        if cost >= budget:
            return
        for index in range(start, len(positive)):
            r = positive[index]; new_cost = cost+r[3]+r[4]
            if new_cost > budget:
                continue
            new_accumulated = tuple(accumulated[i]+r[i] for i in range(3))
            if any(new_accumulated[i] > D[i] for i in range(3)):
                continue
            visit(chosen+[r], index, new_cost, new_accumulated)

    if budget >= 0 and min(D) >= 0:
        visit([], 0, 0, (0, 0, 0))
    records.sort(key=lambda r: (len(r['exceptional_rows']), r['exceptional_rows']))
    summary = {'pair_multiplicities': multiplicities, 't': t, 'cross_weights': D,
               'counts': dict(counts), 'inventory_sha256': digest(records)}
    return summary, records


def audit(work):
    classes, unit = unit_types(json.loads((HERE/'fixtures.json').read_text())['stars'])
    coarse, refined = derive_rows(classes)
    require((len(coarse), len(refined)) == (59, 74), 'whole coarse/refined row cover')
    require({r[:6] for r in refined} == set(coarse), 'full refined-to-coarse projection')
    work = Path(work); work.mkdir(parents=True, exist_ok=True)
    boundary, second = [], []
    for P in (5, 6):
        for multiplicities in product(range(6), repeat=3):
            if sum(multiplicities) != P:
                continue
            for t in (0, 1):
                summary, records = inventory(coarse, multiplicities, (17, 19, 19), t)
                require(not summary['counts'].get('survivor', 0), 'main boundary survives; no theorem verdict')
                boundary.append(summary)
                other, other_records = inventory(coarse, multiplicities, (18, 18, 19), t)
                surviving = [r for r in other_records if r['reason'] == 'survivor']
                second.append({'summary': other, 'survivors': len(surviving),
                               'survivors_sha256': digest(surviving)})
                if surviving:
                    (work/('other-%s-%d.json'%(''.join(map(str, multiplicities)), t))).write_text(json.dumps(surviving, indent=2)+'\n')
    fine_cases, fine_records = [], []
    for multiplicities in ((1, 1, 4), (1, 2, 3)):
        for t in (0, 1):
            summary, records = inventory(refined, multiplicities, (17, 19, 19), t)
            fine_cases.append(summary); fine_records.append({'pair_multiplicities': multiplicities, 't': t, 'records': records})
    original = json.loads((HERE/'AUTHOR_EXPECTED.json').read_text())
    compared = {'unit_graphs': sorted(classes), 'necessary_row_types': len(refined),
                'row_statistics_sha256': digest(refined), 'zero_cost_row_types': 4,
                'exceptional_row_types': len(refined)-4, 'cases': fine_cases,
                'all_inventories_sha256': digest(fine_records),
                'budget_valid_inventories': sum(c['counts']['budget_valid'] for c in fine_cases)}
    compared = json.loads(json.dumps(compared))
    require(all(compared[k] == original[k] for k in compared), 'whole author mathematical record differs')
    (work/'refined-inventories.json').write_text(json.dumps(fine_records)+'\n')
    return {'status': 'PASS_INDEPENDENT_THREE_HUB_BOUNDARY', 'unit_records': unit,
            'coarse_rows': coarse, 'refined_rows': refined, 'refined_projection': 'complete74-to59',
            'all_ordered_main_cases': boundary, 'main_survivors': 0, 'author_mathematical_readout': compared,
            'other_profile_cases': second,
            'other_profile_survivors': sum(v['survivors'] for v in second)}
