"""Independent cost-class occupancy coverage of all exceptional multisets.

No monotone row recursion, hub-deficit pruning or inventory-engine imports.
Choose class occupancies first, Cartesian products of unordered choices
within classes second, then independently solve all zero-cost counts.
"""
from collections import defaultdict
from itertools import combinations_with_replacement, product
import time
from star_primitives import require, digest


def basic_key(record):
    return (tuple(tuple(r) for r in record['exceptional']), tuple(record['filler_counts']),
            record['E'], record['Q'], record['X'], record['tau'])


def verify(rows, cases):
    groups = defaultdict(list)
    for row in rows:
        if row[3]+row[4]:
            groups[(row[3], row[3]+row[4])].append(row)
    groups = sorted(groups.items())
    base = {row[:3]: row for row in rows if row[3]+row[4] == 0}
    populations = {tuple(c['lam'])+(c['E'],c['t']):set() for c in cases}
    patterns = []
    def occupancies(i, cost, excess, chosen):
        if i == len(groups):
            if excess <= 2:
                patterns.append((tuple(chosen), cost, excess))
            return
        (e, charge), _ = groups[i]
        for n in range((6-cost)//charge+1):
            if excess+n*e <= 2:
                occupancies(i+1, cost+n*charge, excess+n*e, chosen+[n])
    occupancies(0, 0, 0, [])
    started = time.monotonic(); multiset_count = 0
    for pattern, cost, E in patterns:
        choices = [tuple(combinations_with_replacement(group, n))
                   for (_,group),n in zip(groups,pattern)]
        for blocks in product(*choices):
            multiset_count += 1
            require(multiset_count <= 200000 and time.monotonic()-started < 20,
                    'INCOMPLETE fixed occupancy-oracle guard')
            chosen = tuple(sorted(r for block in blocks for r in block))
            cross = tuple(sum(r[i] for r in chosen) for i in range(3))
            for c in cases:
                lam = tuple(c['lam']); e, t = c['E'], c['t']
                if e != E or cost > 6-t or (6-t-cost) % 2:
                    continue
                a,b,z = lam; D = (14-z,6-b,6-a)
                filler = tuple(D[i]-cross[i] for i in range(3))
                unmarked = 15-len(chosen)-sum(filler)
                if min(filler) < 0 or unmarked < 0:
                    continue
                entire = list(chosen)+[base[(0,0,0)]]*unmarked
                for i,n in enumerate(filler):
                    entire.extend([base[tuple(int(i == j) for j in range(3))]]*n)
                # Independent degree-sum equation, rather than subtracting
                # cross excess from E in the producer's row conservation.
                ss_weight = sum(5-sum(r[:3]) for r in entire)
                ss_degree = sum(r[5] for r in entire)
                require(ss_weight == 56, 'SS double-incidence fixed profile')
                if (ss_weight-ss_degree) < 0 or (ss_weight-ss_degree) % 2:
                    continue
                key = (chosen,(unmarked,)+filler,E,cost-E,
                       (ss_weight-ss_degree)//2,(6-t-cost)//2)
                populations[lam+(E,t)].add(key)
    records = []
    for c in cases:
        key = tuple(c['lam'])+(c['E'],c['t'])
        expected = {basic_key(r) for r in c['all_records']}
        require(expected == populations[key], 'complete budget-valid multiset coverage differs')
        records.append({'multiplicities':c['lam'],'E':c['E'],'t':c['t'],
                        'budget_valid':len(expected),'actual_multisets_sha256':digest(sorted(expected))})
    return {'cost_class_patterns':len(patterns),'unordered_multisets_before_hub_filters':multiset_count,
            'all_complete_budget_valid_multiset_sets_equal':True,'domains':records}
