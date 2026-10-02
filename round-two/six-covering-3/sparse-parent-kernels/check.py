"""Cofactor checker; no solver, producer, previous fixture, or proof corpus.

Written pigeonhole arguments provide the universal reduction. This program
checks the finite endpoint arithmetic, explicit witnesses and BASE stage.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from math import lcm
from pathlib import Path
from separate import balanced_rainbow, separate

D = (1, 3, 5, 7, 9, 15, 21, 35, 45, 63, 105, 315)
P = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
BASE = [n for n in range(8, 2521) if 2520 % n == 0 and n not in {n for n, a in P}]
TAIL = sorted([16*d for d in D] + [32*d for d in D])


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def verify_expected(result, expected):
    need(result == expected, 'expected cofactor report differs')


def validate_kernel(K, support, N):
    need(isinstance(K, list) and len(K) == 7 and all(
        isinstance(H, list) and H == sorted(set(H)) and
        all(type(y) is int and 0 <= y < 315 for y in H) for H in K), 'invalid kernel')
    need(sum(bool(H) for H in K) == support and sum(map(len, K)) == N,
         'wrong product-kernel cardinality or support')
    points = [x for x in range(2520) if x % 8 and x % 315 in K[x % 8 - 1]]
    need(len(points) == N and all(all(x % n != a for n, a in P) for x in points),
         'kernel leaves initial owned P')
    M = [[d, max(sum(y % d == a for y in H) for H in K for a in range(d))] for d in D]
    caps = sorted([[16*d, 2*m] for d, m in M]+[[32*d, m] for d, m in M])
    need(sum(c for n, c in caps) < 4*N, 'no strict original-tail unit obstruction')
    clause = [[n, a] for n in BASE for a in sorted({x % n for x in points})]
    return {'cofactor_points': N, 'nonempty_parents': support, 'physical_demand': 4*N,
            'cofactor_capacities': M, 'tail_capacities': caps,
            'tail_capacity_budget': sum(c for n, c in caps),
            'clause_terms': len(clause), 'clause_sha256': digest(clause)}


def report(f):
    need(f['agent'] == 'six-covering-3' and f['role'] == 'researcher' and
         f['period'] == 10080 and f['prefix'] == P, 'wrong author, period or original prefix')
    need(sorted([n for n, a in P]+BASE+TAIL) ==
         [n for n in range(8, 10081) if 10080 % n == 0], 'original resources fail partition')
    phases = f['base_phases']
    need(isinstance(phases, list) and len(phases) == 36 and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and 0 <= row[1] < row[0] for row in phases) and
        sorted(n for n, a in phases) == BASE, 'wrong BASE choices')
    need(lcm(*(n for n, a in P+phases)) == 2520, 'wrong partial-stage LCM')
    H = [[] for _ in range(7)]
    for x in range(2520):
        if all(x % n != a for n, a in P+phases):
            need(x % 8 != 0, 'unexpected parent0')
            H[x % 8-1].append(x % 315)
    for points in H:
        points.sort()
    need(all(not H[r-1] for r in (1, 3, 5)) and all(H[r-1] for r in (2, 4, 6, 7)),
         'wrong actual three-empty/four-nonempty stage')
    w = f['all_q_witness']
    need(w['parent'] in (2, 4, 6, 7) and 0 < len(w['classes']) <= 5 and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and row[0] in D[1:] and 0 <= row[1] < row[0]
        for row in w['classes']) and len({d for d, a in w['classes']}) == len(w['classes']),
         'wrong five-DISTINCT-label ability witness')
    need(all(any(y % d == a for d, a in w['classes']) for y in H[w['parent']-1]),
         'literal residual escapes five-class ability')
    # The two credited tests require a mixed ternary triple at every2/4/6/7,
    # or a rainbow triple at all four. The actual parent2 has neither.
    need({y % 3 for y in H[1]} == {0} and {y % 9 for y in H[1]} == {3, 6},
         'old necessary-test passing bridge failed')
    three = validate_kernel(f['three_parent_kernel'], 3, 13)
    two = validate_kernel(f['two_parent_kernel'], 2, 22)
    need(three['tail_capacity_budget'] == 51 and two['tail_capacity_budget'] == 87,
         'wrong equality capacities')
    need(all(set(K).issubset(points) for K, points in zip(f['three_parent_kernel'], H)),
         'thirteen-point kernel is not in actual BASE residual')
    coords = f['two_parent_coordinates']
    need(len(coords) == 11 and all(isinstance(row, list) and len(row) == 4 and
        all(type(v) is int for v in row) and 0 <= row[3] < 315 and
        [row[3] % 9, row[3] % 5, row[3] % 7] == row[:3] for row in coords) and
        sorted(row[3] for row in coords) == f['two_parent_kernel'][3] == f['two_parent_kernel'][6],
         'explicit two-parent CRT table differs')
    lower2 = [[N, (N+1)//2, 3*sum(((N+1)//2+d-1)//d for d in D), 4*N]
              for N in range(1, 22)]
    lower3 = [[N, (N+2)//3, 3*((N+2)//3+(((N+2)//3)+2)//3+10), 4*N]
              for N in range(1, 13)]
    need(all(L >= demand for N, M, L, demand in lower2+lower3),
         'universal endpoint pigeonhole lower bound failed')
    stage_caps = sorted([[16*d, 2*max(sum(y % d == a for y in points)
                                      for points in H for a in range(d))] for d in D]+
                        [[32*d, max(sum(y % d == a for y in points)
                                    for points in H for a in range(d))] for d in D])
    found = separate(phases)
    need(found['status'] == 'MINIMAL_THREE_PARENT13_KERNEL' and
         found['kernel'] == f['three_parent_kernel'] and
         found['clause_sha256'] == three['clause_sha256'], 'complete separator disagrees')
    return {'agent': 'six-covering-3', 'role': 'researcher', 'fixture_sha256': digest(f),
            'three_parent_kernel': three, 'two_parent_kernel': two,
            'at_most_two_lower_rows': lower2, 'at_most_three_lower_rows': lower3,
            'at_most_one_unit_obstruction': False,
            'at_most_two_minimum_points': 22, 'at_most_three_minimum_points': 13,
            'kernel_common_q_automatic_max_parents': 3,
            'actual_stage': {'sizes': list(map(len, H)), 'cofactor_holes': sum(map(len, H)),
                            'physical_holes': 4*sum(map(len, H)),
                            'tail_capacity_budget': sum(c for n, c in stage_caps),
                            'tail_capacities': stage_caps,
                            'all_common_q_passed_by_witness': True,
                            'credited12_and13_tests_passed': True,
                            'new_minimal_three_parent13_test_passed': False},
            'whole_P_exclusion': False, 'L_min8_bound_improvement': False}


def controls(f):
    damages = []
    def damaged(mutator):
        g = deepcopy(f)
        mutator(g)
        damages.append(g)
    damaged(lambda g: g.update(period=2520))
    damaged(lambda g: g['prefix'].append([16, 1]))
    damaged(lambda g: g['base_phases'].pop())
    damaged(lambda g: g['base_phases'][0].__setitem__(1, g['base_phases'][0][0]))
    damaged(lambda g: g['three_parent_kernel'][3].append(g['three_parent_kernel'][3][0]))
    damaged(lambda g: g['three_parent_kernel'][3].__setitem__(0, 0))
    damaged(lambda g: g['three_parent_kernel'][5].__setitem__(2, 11))
    damaged(lambda g: g['two_parent_kernel'][3].pop())
    damaged(lambda g: g['two_parent_coordinates'][0].__setitem__(0, 0))
    damaged(lambda g: g['all_q_witness']['classes'].append([3, 2]))
    damaged(lambda g: g['all_q_witness']['classes'].__setitem__(0, [1, 0]))
    damaged(lambda g: g['all_q_witness'].update(classes=[]))
    for g in damages:
        try:
            report(g)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise ValueError('semantic fixture damage accepted')
    points = [1, 2, 4, 6, 8, 13, 33, 35]
    cases = 0
    for mask in range(1 << len(points)):
        H = [y for i, y in enumerate(points) if mask >> i & 1]
        for k in (4, 5):
            literal = any(all(len({y % d for y in chosen}) == k for d in (5, 7, 9)) and
                          max(sum(y % 3 == a for y in chosen) for a in range(3)) <= 2
                          for chosen in combinations(H, k))
            found = balanced_rainbow(H, k)
            need((found is not None) == literal, 'complete tuple enumeration disagrees')
            if found is not None:
                need(len(found) == k and set(found).issubset(H) and all(
                     len({y % d for y in found}) == k for d in (5, 7, 9)) and
                     max(sum(y % 3 == a for y in found) for a in range(3)) <= 2,
                     'bad tuple witness')
            cases += 1
    return {'rejecting_fixture_damages': len(damages), 'literal_tuple_controls': cases}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    f = json.loads(Path(__file__).with_name('fixture.json').read_text())
    result = report(f)
    if args.expected:
        expected = json.loads(args.expected.read_text())
        verify_expected(result, expected)
        for key in ('at_most_two_minimum_points', 'at_most_three_minimum_points',
                    'fixture_sha256', 'whole_P_exclusion'):
            changed = deepcopy(expected)
            changed[key] = True if key == 'whole_P_exclusion' else 'damaged'
            try:
                verify_expected(result, changed)
            except ValueError:
                pass
            else:
                raise ValueError('damaged expected output accepted')
    if args.controls:
        print(json.dumps(controls(f), sort_keys=True))
    else:
        print(json.dumps(result, sort_keys=True, separators=(',', ':')))
