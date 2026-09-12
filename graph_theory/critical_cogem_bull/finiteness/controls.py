#!/usr/bin/env python3
"""Exact finite controls for proof.md; not an all-order proof or census.

CPython 3.11+, standard library only. No solver, external catalogue or input.
Run normally to compare with expected.json; --emit prints the fresh result.
"""
import argparse
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path


def graph(n, edges):
    a = [0] * n
    for u, v in edges:
        assert 0 <= u < n and 0 <= v < n and u != v
        a[u] |= 1 << v
        a[v] |= 1 << u
    return tuple(a)


def complement(a):
    full = (1 << len(a)) - 1
    return tuple(full ^ (1 << v) ^ row for v, row in enumerate(a))


def vertices(mask):
    return [v for v in range(mask.bit_length()) if mask >> v & 1]


def induced(a, vs):
    assert len(set(vs)) == len(vs)
    return graph(len(vs), ((i, j) for i, j in combinations(range(len(vs)), 2)
                          if a[vs[i]] >> vs[j] & 1))


def stable(a, vs):
    return all(not (a[u] >> v & 1) for u, v in combinations(vs, 2))


def is_p4(a):
    return len(a) == 4 and sorted(x.bit_count() for x in a) == [1, 1, 2, 2]


def is_gem(a):
    return len(a) == 5 and any(
        row.bit_count() == 4 and is_p4(induced(a, [u for u in range(5) if u != v]))
        for v, row in enumerate(a))


def cogem_free(a):
    return all(not is_gem(complement(induced(a, vs)))
               for vs in combinations(range(len(a)), 5))


def connected(a):
    seen = 1
    while True:
        new = seen
        for v in vertices(seen):
            new |= a[v]
        if new == seen:
            return seen == (1 << len(a)) - 1
        seen = new


def chromatic_data(a):
    @lru_cache(None)
    def chi(mask):
        if not mask:
            return 0
        first = mask & -mask
        # Enumerate every possible color class containing the first vertex.
        best = mask.bit_count()
        sub = mask
        while sub:
            if sub & first and stable(a, vertices(sub)):
                best = min(best, 1 + chi(mask ^ sub))
            sub = (sub - 1) & mask
        return best
    full = (1 << len(a)) - 1
    k = chi(full)
    return k, all(chi(full ^ (1 << v)) < k for v in range(len(a)))


def modules(a):
    full = (1 << len(a)) - 1
    return [m for m in range(1, full) if 2 <= m.bit_count()
            and all((a[v] & m) in (0, m) for v in vertices(full ^ m))]


def twin_quotient(a):
    bags = {}
    for v, row in enumerate(a):
        bags.setdefault(row | (1 << v), []).append(v)
    values = list(bags.values())
    return induced(a, [bag[0] for bag in values]), values


def family_controls():
    total = 0
    for t in range(3, 13):
        # Star labels: c=0, ai=i, bi=t+i, for 1<=i<=t.
        star = graph(2 * t + 1, [(0, i) for i in range(1, t + 1)]
                     + [(i, t + i) for i in range(1, t + 1)])
        assert stable(star, list(range(t + 1, 2 * t + 1)))
        assert is_gem(induced(complement(star), [t + 1, 1, 0, 2, t + 3]))
        a, b = list(range(t)), list(range(t, 2 * t))
        matching = [(i, t + i) for i in a]
        cliques = list(combinations(a, 2)) + list(combinations(b, 2))
        line = graph(2 * t, cliques + matching)
        prism = induced(line, [0, 1, 2, t, t + 1, t + 2])
        expected_prism = graph(6, [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5),
                                   (4, 5), (0, 3), (1, 4), (2, 5)])
        assert prism == expected_prism
        assert stable(complement(line), a)
        cycle = complement(prism)
        assert connected(cycle) and all(row.bit_count() == 2 for row in cycle)
        spider = graph(2 * t, list(combinations(b, 2)) + matching)
        half_edges = [(i, t + j) for i in a for j in a if i >= j]
        half = graph(2 * t, half_edges)
        assert is_gem(induced(complement(half), [0, t, 1, t + 1, t + 2]))
        half_i = graph(2 * t + 1, half_edges + list(combinations(b, 2))
                       + [(2 * t, i) for i in a])
        half_star = graph(2 * t + 1, half_edges + list(combinations(b, 2))
                          + [(2 * t, t - 1)])
        for f in (spider, half, half_i, half_star):
            assert stable(f, a)
        for f in (spider, half_i, half_star):
            assert stable(complement(f), b)
        total += 12  # Six fixed types, two orientations each.
    return {'parameters': [3, 12], 'family_orientation_checks': total,
            'complement_line_K23_is_C6': True}


def chain(bits):
    return graph(len(bits) + 1,
                 ((j, i) for i in range(1, len(bits) + 1) for j in range(i)
                  if ((j == i - 1) != bool(bits[i - 1]))))


def chain_controls():
    words = long_run_words = 0
    for m in range(1, 13):
        for bits in product((0, 1), repeat=m):
            a = chain(bits)
            assert complement(a) == chain(tuple(1 - bit for bit in bits))
            zeros = [i for i, bit in enumerate(bits, 1) if bit == 0]
            parity_sets = [[i for i in zeros if i % 2 == p] for p in (0, 1)]
            assert all(stable(a, vs) for vs in parity_sets)
            assert max(map(len, parity_sets)) >= (len(zeros) + 1) // 2
            starts = [j for j in range(m - 4) if bits[j:j + 5] == (1,) * 5]
            for j in starts:
                # Steps j+1,...,j+5: use vj,...,v(j+3),v(j+5).
                assert is_gem(induced(a, [j, j + 1, j + 2, j + 3, j + 5]))
            if starts:
                long_run_words += 1
            else:
                assert m <= 5 * len(zeros) + 4
            words += 1
    return {'maximum_length': 12, 'binary_words_checked': words,
            'words_with_five_one_steps': long_run_words,
            'parity_independent_sets_and_all_run_witnesses_verified': True}


def cycle_expansion(weights):
    bags = []
    n = 0
    for w in weights:
        bags.append(list(range(n, n + w)))
        n += w
    edges = []
    for i, bag in enumerate(bags):
        edges.extend(combinations(bag, 2))
        edges.extend(product(bag, bags[(i + 1) % len(bags)]))
    return graph(n, edges)


def module_controls():
    cases = [('K1', graph(1, [])), ('K5', graph(5, combinations(range(5), 2))),
             ('C5', cycle_expansion([1] * 5)),
             ('C5_clique_expansion_21211', cycle_expansion([2, 1, 2, 1, 1]))]
    rows = []
    for name, a in cases:
        k, critical = chromatic_data(a)
        assert critical and cogem_free(a)
        if connected(complement(a)):
            assert all(stable(complement(a), vertices(m)) for m in modules(a))
            q, bags = twin_quotient(a)
            assert not modules(q)
            assert max(map(len, bags)) <= k and len(a) <= k * len(q)
        rows.append({'graph': name, 'order': len(a), 'chromatic_number': k,
                     'critical': critical})
    c5 = cycle_expansion([1] * 5)
    cone = graph(6, [(u, v) for u, v in combinations(range(5), 2)
                     if c5[u] >> v & 1] + [(v, 5) for v in range(5)])
    assert chromatic_data(cone) == (4, True)
    assert cogem_free(cone) and not connected(complement(cone))
    assert 31 in modules(cone) and not stable(complement(cone), list(range(5)))
    d = graph(4, [(0, 1), (1, 2)])
    assert cogem_free(d) and connected(complement(d))
    assert not chromatic_data(d)[1] and 7 in modules(d)
    assert not stable(complement(d), [0, 1, 2])
    return {'critical_examples': rows,
            'co_connectedness_hypothesis_needed': 'K1 join C5',
            'criticality_hypothesis_needed': 'P3+P1'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    result = {'status': 'PASS', 'role': 'finite controls, not the universal proof',
              'families': family_controls(), 'chains': chain_controls(),
              'modules': module_controls()}
    if not args.emit:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        if result != expected:
            raise RuntimeError('Finite controls differ from expected.json')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
