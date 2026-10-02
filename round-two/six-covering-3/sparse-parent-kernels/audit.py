"""Separate literal physical-progression audit; does not import checker/search.

This is a second same-author algorithm, not an independent reviewer verdict.
"""
import argparse
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


def demand(ok, message):
    if not ok:
        raise ValueError(message)


def hash_json(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def audit(f, e=None):
    prefix = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
    demand(f['prefix'] == prefix and f['period'] == 10080 and
           f['agent'] == 'six-covering-3' and f['role'] == 'researcher', 'wrong original root')
    divisors = tuple(d for d in range(1, 316) if 315 % d == 0)
    tails = sorted(n for n in range(8, 10081) if 10080 % n == 0 and n % 16 == 0)
    base = sorted(n for n in range(8, 2521) if 2520 % n == 0 and
                  n not in dict(prefix))
    demand(len(tails) == 24 and sorted([n for n, a in prefix]+base+tails) ==
           [n for n in range(8, 10081) if 10080 % n == 0], 'wrong resource partition')
    phase = f['base_phases']
    demand(isinstance(phase, list) and len(phase) == 36 and all(
        isinstance(pair, list) and len(pair) == 2 and type(pair[0]) is int and
        type(pair[1]) is int and 0 <= pair[1] < pair[0] for pair in phase) and
        sorted(n for n, a in phase) == base, 'wrong actual BASE stage')
    hole_set = set(range(10080))
    for n, a in prefix+phase:
        hole_set.difference_update(range(a, 10080, n))
    groups = [sorted({x % 315 for x in hole_set if x % 8 == r}) for r in range(1, 8)]
    demand(len(hole_set) == 4*sum(map(len, groups)), 'residual is not fourfold product')
    demand(all(not groups[i] for i in (0, 2, 4)) and all(groups[i] for i in (1, 3, 5, 6)),
           'wrong active original parents')
    ability = f['all_q_witness']
    w = ability['classes']
    demand(type(ability['parent']) is int and ability['parent'] in (2, 4, 6, 7) and
           0 < len(w) <= 5 and all(isinstance(pair, list) and len(pair) == 2 and
           type(pair[0]) is int and type(pair[1]) is int and pair[0] in divisors[1:] and
           0 <= pair[1] < pair[0] for pair in w) and len(dict(w)) == len(w),
           'wrong distinct-label ability')
    leftover = set(groups[ability['parent']-1])
    for d, a in w:
        leftover.difference_update(range(a, 315, d))
    demand(not leftover, 'ability does not cover actual cofactor holes')
    demand(set(y % 3 for y in groups[1]) == {0} and
           set(y % 9 for y in groups[1]) == {3, 6}, 'old-test passing bridge failed')

    def physical_capacities(points):
        return [[n, max(sum(x in points for x in range(a, 10080, n))
                        for a in range(n))] for n in tails]

    summaries = {}
    for key, number, support, cap in (('three_parent_kernel', 13, 3, 51),
                                     ('two_parent_kernel', 22, 2, 87)):
        K = f[key]
        demand(isinstance(K, list) and len(K) == 7 and all(isinstance(part, list) and
               part == sorted(set(part)) and all(type(y) is int and 0 <= y < 315
               for y in part) for part in K), 'invalid literal kernel')
        demand(sum(map(len, K)) == number and sum(bool(part) for part in K) == support,
               'wrong literal kernel cardinality')
        points = {x for x in range(10080) if x % 8 != 0 and x % 315 in K[x % 8-1]}
        demand(len(points) == 4*number and all(all(x % n != a for n, a in prefix)
               for x in points), 'literal kernel hits prescribed class')
        caps = physical_capacities(points)
        demand(sum(c for n, c in caps) == cap < len(points), 'wrong strict physical budget')
        M = [[d, max(max(Counter(y % d for y in part).values(), default=0)
                     for part in K)] for d in divisors]
        demand(caps == sorted([[16*d, 2*v] for d, v in M]+[[32*d, v] for d, v in M]),
               'physical/cofactor capacity bridge disagrees')
        if support == 3:
            demand(sorted(len(part) for part in K if part) == [4, 4, 5] and
                   [v for d, v in M] == [5, 2]+[1]*10 and points.issubset(hole_set),
                   'minimal thirteen equality characterization failed')
        else:
            demand(all(len(part) == 11 for part in K if part) and
                   all(v == -(-11//d) for d, v in M),
                   'minimal twenty-two equality characterization failed')
        terms = [[n, a] for n in base for a in sorted({x % n for x in points if x < 2520})]
        summary = {'cofactor_points': number, 'nonempty_parents': support,
                   'physical_demand': len(points), 'cofactor_capacities': M,
                   'tail_capacities': caps, 'tail_capacity_budget': cap,
                   'clause_terms': len(terms), 'clause_sha256': hash_json(terms)}
        if e is not None:
            demand(summary == e[key], 'literal kernel differs from expected output')
        summaries[key] = summary
    coord = f['two_parent_coordinates']
    demand(len(coord) == 11 and all(len(row) == 4 and all(type(v) is int for v in row) and
           [y for y in range(315) if (y % 9, y % 5, y % 7) == tuple(row[:3])] == [row[3]]
           for row in coord) and sorted(row[3] for row in coord) ==
           f['two_parent_kernel'][3] == f['two_parent_kernel'][6], 'CRT table failed')
    profile_counts = []
    for parents, limit in ((2, 21), (3, 12)):
        checked = 0
        for h in product(range(limit+1), repeat=parents):
            total = sum(h)
            if not 1 <= total <= limit:
                continue
            biggest = max(h)
            lower = (3*sum(-(-biggest//d) for d in divisors) if parents == 2 else
                     3*(biggest-(-biggest//3)+10))
            demand(lower >= 4*total, 'arbitrary profile endpoint bound failed')
            checked += 1
        profile_counts.append([parents, limit, checked])
    stage_caps = physical_capacities(hole_set)
    if e is not None:
        demand(hash_json(f) == e['fixture_sha256'] and e['at_most_two_minimum_points'] == 22 and
               e['at_most_three_minimum_points'] == 13 and not e['at_most_one_unit_obstruction'] and
               not e['whole_P_exclusion'] and not e['L_min8_bound_improvement'] and
               list(map(len, groups)) == e['actual_stage']['sizes'] and
               len(hole_set) == e['actual_stage']['physical_holes'] and
               stage_caps == e['actual_stage']['tail_capacities'] and
               sum(c for n, c in stage_caps) == e['actual_stage']['tail_capacity_budget'],
               'actual stage or theorem output differs')
    return {'literal_original_phases_per_inventory': sum(tails),
            'inventories_checked': 3, 'universal_profile_controls': profile_counts,
            'actual_physical_holes': len(hole_set), 'actual_tail_budget': sum(c for n, c in stage_caps),
            'kernels': summaries}


def controls(f):
    damages = []
    for mutation in (lambda g: g.update(period=2520),
                     lambda g: g['prefix'].append([16, 1]),
                     lambda g: g['base_phases'].pop(),
                     lambda g: g['three_parent_kernel'][3].__setitem__(0, 0),
                     lambda g: g['three_parent_kernel'][5].__setitem__(2, 11),
                     lambda g: g['two_parent_kernel'][3].pop(),
                     lambda g: g['two_parent_coordinates'][0].__setitem__(0, 0),
                     lambda g: g['all_q_witness'].update(classes=[[1, 0]]),
                     lambda g: g['all_q_witness']['classes'].append([3, 2]),
                     lambda g: g['all_q_witness'].update(classes=[])):
        g = deepcopy(f)
        mutation(g)
        damages.append(g)
    for g in damages:
        try:
            audit(g)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise ValueError('literal semantic damage accepted')
    return {'rejecting_fixture_damages': len(damages)}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    fixture = json.loads(Path(__file__).with_name('fixture.json').read_text())
    expected = json.loads(args.expected.read_text()) if args.expected else None
    result = audit(fixture, expected)
    print(json.dumps(controls(fixture) if args.controls else result, sort_keys=True))
