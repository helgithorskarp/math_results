"""Cofactor engine and analytical finite/infinite threshold certificate."""
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from model import BASE, D, PREFIX, capacities, collapse, hitting_clause, mono_minimality, need
from separate import rainbow, separate


def cut_minima(fibers):
    singles = []; pairs = []
    for H in fibers:
        singles.append([1 << i for i, d in enumerate(D) if not H or
                        all(y % d == H[0] % d for y in H)])
        two = []
        for i, j in combinations(range(len(D)), 2):
            d, e = D[i], D[j]
            for a in range(d):
                rest = [y for y in H if y % d != a]
                if not rest or all(y % e == rest[0] % e for y in rest):
                    two.append((1 << i) | (1 << j))
                    break
        pairs.append(two)
    low2 = low3 = 10**9
    for B in range(1 << len(D)):
        Q1 = sum(not H or any(s & B == 0 for s in S) for H, S in zip(fibers, singles))
        Q2 = sum(not H or any(s & B == 0 for s in S) or any(t & B == 0 for t in T)
                 for H, S, T in zip(fibers, singles, pairs))
        low2 = min(low2, 8*Q1 + 3*B.bit_count())
        low3 = min(low3, 24*Q2 + 10*B.bit_count())
    need(low2 >= 20 and low3 >= 72, 'full q2/q3 families fail')
    return [low2, low3]


def run(fixture):
    need(fixture['agent'] == 'six-covering-3' and fixture['role'] == 'researcher' and
         fixture['schema'] == 1 and fixture['prefix'] == list(map(list, PREFIX)) and
         fixture['tail_pools'] == [list(D), list(D)], "wrong free original-resource scope")
    phases = fixture['base_phases']
    need(isinstance(phases, list) and len(phases) == 36 and all(
        isinstance(row, list) and len(row) == 2 and type(row[0]) is int and
        type(row[1]) is int and 0 <= row[1] < row[0] for row in phases) and
        sorted(n for n, a in phases) == list(BASE), "invalid original phase inventory")
    initial = [set() for _ in range(7)]; H = [set() for _ in range(7)]
    for x in range(2520):
        if all(x % n != a for n, a in PREFIX):
            need(x % 8 != 0, "unexpected eighth parent")
            initial[x % 8 - 1].add(x % 315)
            if all(x % n != a for n, a in phases):
                H[x % 8 - 1].add(x % 315)
    H = [sorted(h) for h in H]
    need([r for r, h in enumerate(H, 1) if not h] == [1, 3, 5], "wrong empty parents")
    witness = fixture['five_class_ability_witness']
    need(set(witness) == {'parent', 'classes'} and type(witness['parent']) is int and
         witness['parent'] in (2, 4, 6, 7), "wrong labeled erasure witness")
    classes = witness['classes']
    need(isinstance(classes, list) and 1 <= len(classes) <= 5 and all(
        isinstance(v, list) and len(v) == 2 and type(v[0]) is int and type(v[1]) is int and
        v[0] in D and v[0] != 1 and 0 <= v[1] < v[0] for v in classes) and
        len({d for d, a in classes}) == len(classes), "wrong DISTINCT erasure labels")
    need(all(any(y % d == a for d, a in classes) for y in H[witness['parent']-1]),
         "five-class erasure witness misses a point")
    K = fixture['kernel']
    need(isinstance(K, list) and len(K) == 7 and all(isinstance(k, list) and
        k == sorted(set(k)) and all(type(y) is int and 0 <= y < 315 for y in k) for k in K),
        "invalid labeled kernel")
    need([r for r, k in enumerate(K, 1) if k] == [2, 4, 6, 7] and
         sorted(len(k) for k in K if k) == [3, 3, 3, 4] and
         all(set(k) <= set(h) for k, h in zip(K, H)), "kernel leaves actual residual")
    need(all(len({y % d for y in k}) == len(k) for k in K for d in (5, 7, 9)),
         "kernel is not rainbow at each coordinate")
    need(all(y % 3 == 2 for r in (2, 6) for y in H[r-1]), "wrong actual mono parents")
    # Original18:6 and36:30 imply this mono property already before the other
    # BASE choices; the sharp cardinality lower bound uses only that domain.
    partial = PREFIX + ((18, 6), (36, 30))
    need([18, 6] in phases and [36, 30] in phases and all(x % 3 == 2 for x in range(2520)
        if x % 8 in (2, 6) and all(x % n != a for n, a in partial)),
        "partial-stage monochromatic bridge failed")
    stage_caps = capacities(H); kernel_caps = capacities(K)
    terms = hitting_clause(K)
    need(not any(row in terms for row in phases), "stage meets the kernel hitting clause")
    no_old_kernel = rainbow(H[1], 3, mixed3=True) is None
    need(no_old_kernel, "fixture is not a false negative of the credited12 test")
    separation = separate(phases)
    need(separation['status'] == 'THIRTEEN_POINT_KERNEL' and separation['kernel'] == K,
         "complete separator reconstructed a different kernel")
    five_best = sorted((315//d for d in D if d != 1), reverse=True)[:5]
    need(sum(five_best) == 269 < 315, "abstract q6 negative calibration failed")
    return {'agent': 'six-covering-3', 'role': 'researcher', 'collapse': collapse(),
            'stage_sizes': list(map(len, H)), 'stage_physical_points': 4*sum(map(len, H)),
            'stage_capacities': stage_caps, 'stage_capacity_budget': sum(c for n, c in stage_caps),
            'single_ability_witness': witness, 'stage_all_integer_q_at_least2_passed': True,
            'stage_all4096_each_q2_q3_minima': cut_minima(H),
            'kernel_sizes': list(map(len, K)), 'kernel_physical_points': 4*sum(map(len, K)),
            'kernel_capacities': kernel_caps, 'kernel_capacity_budget': sum(c for n, c in kernel_caps),
            'kernel_all_integer_q_at_least2_passed': True,
            'kernel_clause_terms': len(terms),
            'kernel_clause_sha256': sha256(json.dumps(terms, separators=(",", ":")).encode()).hexdigest(),
            'prior12_test_passed': no_old_kernel, 'minimality_vectors_through12': mono_minimality(),
            'abstract_full315_five_class_capacity': sum(five_best),
            'abstract_q6_B1_left_right': [83, 84]}


def verify(fixture, expected):
    observed = run(fixture)
    need(observed == expected, "frozen evidence differs")
    need(expected['kernel_physical_points'] == 52 and expected['kernel_capacity_budget'] == 51 and
         expected['stage_capacity_budget'] < expected['stage_physical_points'],
         "no strict physical capacity deficit")
    return observed


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    print(json.dumps(verify(json.loads((here/'fixture.json').read_text()),
                            json.loads((here/'expected.json').read_text())), sort_keys=True))
