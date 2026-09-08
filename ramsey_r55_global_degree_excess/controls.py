#!/usr/bin/env python3
"""Check the new identities against whole physical graphs, not profile formulas."""
import itertools
import json
import random


def require(condition, message):
    if not condition:
        raise ValueError(message)


def controls():
    rng = random.Random(394390513)
    n = 43
    overlap_cases = 0
    overlap_edges = 0
    for c in range(5, 14):
        for trial in range(8):
            common = set(range(2, 2 + c))
            left = set(range(2 + c, 25))
            right = set(range(25, 48 - c))
            tail = set(range(48 - c, n))
            a = [set() for _ in range(n)]
            for u, v in itertools.combinations(range(n), 2):
                if u == 0:
                    bit = v == 1 or v in common or v in left
                elif u == 1:
                    bit = v in common or v in right
                elif u in common and v in common:
                    bit = (u % 2 != v % 2) and bool(rng.getrandbits(1))
                else:
                    bit = bool(rng.getrandbits(1))
                if bit:
                    a[u].add(v)
                    a[v].add(u)
            require(len(a[0]) == len(a[1]) == 24 and a[0] & a[1] == common,
                    'root controls')
            require(set(range(n)) - (a[0] | a[1]) == tail, 'tail controls')
            delta = [24 - len(x) for x in a]
            d = {w: len(a[w] & common) for w in common}
            d0 = {w: len(a[w] & a[0]) for w in common}
            d1 = {w: len(a[w] & a[1]) for w in common}
            for w in common:
                require(len(a[w] & tail) == 24 - delta[w] - d0[w] - d1[w] + d[w],
                        'individual overlap identity')
            edges = [(w, z) for w, z in itertools.combinations(common, 2) if z in a[w]]
            p = sum(d0.values()) + sum(d1.values())
            first = c * (29 - c) + 2 * len(edges)
            require(p - first + sum(delta[w] for w in common)
                    == sum(z not in a[w] for w in common for z in tail),
                    'summed degree overlap identity')
            q = sum(d[w] * (d0[w] + d1[w]) for w in common)
            q -= sum(len(a[w] & a[z] & a[0]) + len(a[w] & a[z] & a[1])
                     for w, z in edges)
            second = sum(x * x for x in d.values()) + (40 - c) * len(edges)
            residual = sum(13 - len(a[w] & a[z]) + len(tail - (a[w] | a[z]))
                           for w, z in edges)
            require(q - second + sum(d[w] * delta[w] for w in common) == residual,
                    'summed edge overlap identity')
            overlap_cases += 1
            overlap_edges += len(edges)

    split_cases = 0
    for trial in range(96):
        a = [set() for _ in range(n)]
        for u, v in itertools.combinations(range(n), 2):
            bit = v <= 18 if u == 0 else bool(rng.getrandbits(1))
            if bit:
                a[u].add(v)
                a[v].add(u)
        small = a[0]
        large = set(range(1, n)) - small
        excess = [len(x) - 18 for x in a]
        small_edges = sum(v in a[u] for u, v in itertools.combinations(small, 2))
        opposite_large_edges = sum(v not in a[u] for u, v in itertools.combinations(large, 2))
        total = sum(excess)
        weighted = sum(excess[w] for w in small)
        require(total % 2 == 0 and excess[0] == 0, 'split parity')
        require(small_edges + opposite_large_edges == 213 + weighted - total // 2,
                'irregular neighborhood density identity')
        split_cases += 1
    return {'status': 'VERIFIED_PHYSICAL_DEGREE_EXCESS_IDENTITIES',
            'seed': 394390513, 'overlap_graphs': overlap_cases,
            'common_edges_checked': overlap_edges, 'degree_split_graphs': split_cases,
            'fixtures_are_ramsey_graphs': False,
            'signed_deficits_allowed_in_identity_controls': True}


if __name__ == '__main__':
    print(json.dumps(controls(), sort_keys=True))
