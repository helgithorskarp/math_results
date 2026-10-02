"""Literal unit-capacity and ordinary common-q audit; Python standard library.

No proposal program, LP data, solver status, peer BASE fixture, or private
search tree is imported. The lower bound and all-q conclusions also require
the written elementary arguments in proof.md.
"""
import argparse
import copy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':'), sort_keys=True).encode()).hexdigest()


def audit(data):
    require((data['period'], data['minimum'], data['cofactor'], data['base_period'])
            == (10080, 8, 315, 2520), 'Wrong original ambient domain')
    N = data['period']
    roots = data['roots']
    require(roots == [[[8, 0], [9, 0], [10, 1], [14, a], [12, 10], [16, 1]]
                      for a in (0, 1)], 'Wrong H/P marked roots')
    require(data['stage'] == {'p': 2, 'm': 5, 's': 0, 'T': 10, 'k1': 11, 'k2': 12},
            'Wrong two-layer original resource parameters')
    rows = data['kernel']
    require([r for r, _ in rows] == [2, 3, 4, 5, 6], 'Wrong nonempty binary parents')
    for r, points in rows:
        require(type(r) is int and points and sorted(set(points)) == points
                and all(type(z) is int and 0 <= z < 315 for z in points),
                'Invalid original cofactor points')
    K = dict(rows)
    require([len(h) for h in K.values()] == [2, 2, 2, 2, 1]
            and sum(map(len, K.values())) == 9, 'Wrong nine-point pattern')
    W = {x for x in range(N) if x % 8 in K and x % 315 in K[x % 8]}
    require(len(W) == data['physical_demand'] == 36, 'Wrong physical demand')
    require(all(all(x % m != a for m, a in A) for A in roots for x in W),
            'Kernel hits a prescribed ORIGINAL class')
    require(all(x % 15 != 2 for x in W), 'Kernel hits original15:2')

    D = tuple(d for d in range(1, 316) if 315 % d == 0)
    E = D[1:]
    tail = tuple(16 * d for d in E) + tuple(32 * d for d in D)
    known = {m for m, _ in roots[0]}
    base = tuple(m for m in range(8, 2521) if 2520 % m == 0 and m not in known)
    original = {m for m in range(8, N + 1) if N % m == 0}
    require(len(E) == 11 and len(D) == 12 and len(base) == 36
            and len(set(tail)) == 23 and len(set(tail) | set(base) | known) == 65
            and set(tail).isdisjoint(base) and set(tail).isdisjoint(known)
            and set(base).isdisjoint(known)
            and set(tail) | set(base) | known == original,
            'Wrong partition of ORIGINAL moduli')
    maxima = []
    raw_tail_phases = 0
    for m in tail:
        # Every physical progression is scanned, including zero-gain phases.
        counts = [sum(x in W for x in range(a, N, m)) for a in range(m)]
        raw_tail_phases += m
        maxima.append([m, max(counts)])
    require(sum(c for _, c in maxima) == data['remaining_tail_capacity'] == 35
            and len(W) > sum(c for _, c in maxima), 'No strict tail obstruction')

    K0 = sorted({x % 2520 for x in W})
    clause = [[m, a] for m in base for a in sorted({x % m for x in K0})]
    clause15 = [pair for pair in clause if pair[0] != 15]
    require(len(K0) == 9 and len(clause) == data['base_clause_terms'] == 225
            and len(clause15) == data['base_clause_terms_after_15_two'] == 223,
            'Wrong BASE phase clauses')

    # Reconstruct actual single/two-class erasers in EACH original pool.
    # D2 contains1 (original32) although D1 omits1 (original16 is spent).
    # Combining E and D does not allow an original modulus at two prefixes.
    families = []
    raw_cofactor_phases = 0
    for r, h in rows:
        full = (1 << len(h)) - 1
        by_pool = []
        for pool in (E, D):
            masks = {}
            singles = []
            pairs = []
            for d in pool:
                actual = [sum((1 << i) for i, z in enumerate(h) if z % d == a)
                          for a in range(d)]
                raw_cofactor_phases += d
                masks[d] = sorted(set(actual))
                if full in actual:
                    singles.append((d,))
            for d, e in combinations(pool, 2):
                if any(a | b == full for a in masks[d] for b in masks[e]):
                    pairs.append((d, e))
            by_pool.append({1: singles, 2: pairs})
        families.append(by_pool)

    minimum = {2: 10 ** 9, 3: 10 ** 9}
    all_q_affine = []
    for mask in range(1 << len(D)):
        B = {d for j, d in enumerate(D) if mask >> j & 1}
        eps = int(1 in B)
        R, L = len(B), len(set(E) - B)
        for q in (2, 3):
            forced = sum(any(not (set(S) & B) for pool in f
                             for k in range(1, q) for S in pool[k])
                         for f in families)
            predicted = (5 if not eps else (int(L > 0) if q == 2
                         else 5 if L >= 2 else int(L == 1)))
            require(forced == predicted, 'False original eraser classification')
            lhs = 4 * q * forced + (2 * q - 1) * R
            rhs = 8 * q - 10 + 2 * (q - 1) * eps
            require(lhs >= rhs, 'Ordinary common-q cut rejects kernel')
            minimum[q] = min(minimum[q], lhs - rhs)
        # Each original kernel has at most2 points. Thus for EVERY q>=3
        # the same forced count applies, not merely for the tested q=3.
        forced = 5 if not eps or L >= 2 else int(L == 1)
        slope = 4 * forced + 2 * R - 8 - 2 * eps
        intercept = 10 - R + 2 * eps
        require(slope >= 0 and 3 * slope + intercept > 0,
                'Invalid all-q affine proof')
        # Written closed minimum: min(12q+10,14q), q>=3.
        # Verify each affine case dominates one of these two lower lines.
        require((slope >= 12 and 3 * (slope - 12) + intercept - 10 >= 0)
                or (slope >= 14 and 3 * (slope - 14) + intercept >= 0),
                'False closed common-q minimum bound')
        all_q_affine.append([R, eps, L, forced, slope, intercept])
    require({str(k): v for k, v in minimum.items()} == data['common_q_minimum_slack']
            == {'2': 3, '3': 42}, 'Wrong exact ordinary minima')

    # Finite arithmetic for the written universal product-kernel lower bound.
    # For nonempty kernels all11 remaining16d labels have capacity>=2;
    # all11 nontrivial32d labels have capacity>=1; original32 has capacity>=M.
    lower_rows = [[k, 4 * k, 33 + (k + 5) // 6] for k in range(1, 9)]
    require(all(demand <= cap for k, demand, cap in lower_rows)
            and data['minimum_product_kernel_points'] == 9,
            'Invalid limited nine-point lower bound')
    return {
        'agent': 'six-covering-2', 'role': 'researcher', 'period': N,
        'certificate_sha256': digest(data), 'cofactor_kernel_points': len(K0),
        'physical_demand': len(W), 'remaining_original_tail_capacity': 35,
        'strict_gap': 1, 'tail_maxima': maxima,
        'raw_original_tail_phases': raw_tail_phases,
        'raw_cofactor_phase_masks': raw_cofactor_phases,
        'right_subsets': len(all_q_affine),
        'common_q_minimum_slack': {str(k): v for k, v in minimum.items()},
        'common_q_ge3_minimum': 'min(12*q+10,14*q)',
        'all_q_affine_sha256': digest(all_q_affine),
        'product_kernel_lower_rows': lower_rows,
        'minimum_product_kernel_points': 9,
        'BASE_clause_terms': len(clause), 'BASE_clause_sha256': digest(clause),
        'BASE_after_15_two_clause_terms': len(clause15),
        'BASE_after_15_two_clause_sha256': digest(clause15),
        'covering_excluded': False, 'complete_BASE_realization_claimed': False,
        'independent_reviewer': False,
    }


def controls(data):
    mutations = []
    for key, value in (('period', 15120), ('minimum', 7), ('cofactor', 105),
                       ('base_period', 1260), ('physical_demand', 35),
                       ('remaining_tail_capacity', 36),
                       ('minimum_product_kernel_points', 8),
                       ('base_clause_terms', 224),
                       ('base_clause_terms_after_15_two', 222)):
        damaged = copy.deepcopy(data)
        damaged[key] = value
        mutations.append((key, damaged))
    damaged = copy.deepcopy(data); damaged['roots'][0][-1][1] = 3
    mutations.append(('wrong_original16_phase', damaged))
    damaged = copy.deepcopy(data); damaged['kernel'][0][1][0] = 2
    mutations.append(('kernel_hits15_two', damaged))
    damaged = copy.deepcopy(data); damaged['kernel'][1][1] = [3, 3]
    mutations.append(('duplicate_kernel_point', damaged))
    damaged = copy.deepcopy(data); damaged['stage']['k1'] = 12
    mutations.append(('spent_original16_reintroduced', damaged))
    damaged = copy.deepcopy(data); damaged['common_q_minimum_slack']['2'] = 2
    mutations.append(('first_only_support_cost_used_as_true_minimum', damaged))
    names = []
    for name, damaged in mutations:
        try:
            audit(damaged)
        except ValueError:
            names.append(name)
            continue
        raise ValueError('Damaged certificate accepted: ' + name)
    return {'rejected': len(names), 'names': names}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--certificate', type=Path,
                    default=Path(__file__).with_name('certificate.json'))
    ap.add_argument('--expected', type=Path)
    ap.add_argument('--controls', action='store_true')
    args = ap.parse_args()
    data = json.loads(args.certificate.read_text())
    result = controls(data) if args.controls else audit(data)
    if args.expected:
        require(result == json.loads(args.expected.read_text()), 'Expected audit differs')
    print(json.dumps(result, sort_keys=True, indent=2))
