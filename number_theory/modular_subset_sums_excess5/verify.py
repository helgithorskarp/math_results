#!/usr/bin/env python3
"""Independent semantic controls: literal subset sums and unit/sign actions.

Does not import the bit-mask generator or infer uniform truth from examples.
"""
import json
from itertools import combinations
from math import gcd
from pathlib import Path


def literal_sums(values, modulus):
    # A list, so collisions are retained until the final uniqueness comparison.
    sums = [0]
    for a in values:
        sums = sums + [(s + a) % modulus for s in sums]
    return sums


def canonical(values, modulus):
    return tuple(sorted(min(a % modulus, (-a) % modulus) for a in values))


def classes(n):
    powers = [2 ** i for i in range(n)]
    return [powers, powers[:-1] + [powers[-1] + 1],
            powers[:-2] + [powers[-2] + 1, powers[-1] + 1]]


def check(result, normal_forms):
    checked_literal_sets = 0
    for control in result['controls']:
        n, modulus = control['n'], control['N']
        assert modulus == 2 ** n + 5 and 5 <= n <= 10
        chain = [2 ** i for i in range(n - 2)]
        m = 2 ** (n - 2)
        expected_pairs = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]
        assert list(map(tuple, control['normalized_pairs'])) == expected_pairs
        assert sorted((r['a'], r['b']) for r in normal_forms['rows']) == expected_pairs
        for row in normal_forms['rows']:
            values = chain + [m + row['a'], 2 * m + row['b']]
            sums = literal_sums(values, modulus)
            assert len(sums) == len(set(sums)) == 2 ** n
            assert gcd(row['multiplier'], modulus) == 1
            assert canonical([row['multiplier'] * a for a in values], modulus) == tuple(
                classes(n)[row['class']])
            checked_literal_sets += 1
        unit_count = sum(gcd(u, modulus) == 1 for u in range(1, modulus))
        assert unit_count == control['phi']
        assert control['chain_family_subsets'] == 3 * 2 ** (n - 1) * unit_count

    # Unpruned, definition-level census at n=5, independent of prefix search.
    brute_five = []
    for values in combinations(range(1, 19), 5):
        sums = literal_sums(values, 37)
        if len(set(sums)) == 32:
            brute_five.append(values)
    for census in result['complete_small_censuses']:
        n, modulus = census['n'], census['N']
        assert n in (5, 6) and modulus == 2 ** n + 5
        listed = list(map(tuple, census['signed_class_sets']))
        assert listed == sorted(set(listed))
        if n == 5:
            assert listed == brute_five
        orbits = []
        for base in classes(n):
            orbit = set()
            for u in range(1, modulus):
                if gcd(u, modulus) == 1:
                    orbit.add(canonical([u * a for a in base], modulus))
            orbits.append(orbit)
        assert set(listed) == set.union(*orbits)
        assert [len(o) for o in orbits] == census['class_sizes_in_signed_quotient']
        assert census['all_actual_subsets'] == 2 ** n * len(listed)
        for values in listed:
            assert len(values) == n and len(set(values)) == n
            assert all(0 < a <= modulus // 2 for a in values)
            sums = literal_sums(values, modulus)
            assert len(set(sums)) == 2 ** n
            nonunits = [a for a in values if gcd(a, modulus) > 1]
            assert len(nonunits) <= 1
            assert all(gcd(a, modulus) == 3 for a in nonunits)
            if nonunits:
                missing = set(range(modulus)) - set(sums)
                assert sorted(sum(s % 3 == j for s in missing) for j in range(3)) == [1, 1, 3]
            checked_literal_sets += 1
    assert [x['n'] for x in result['controls']] == list(range(5, 11))
    assert [x['n'] for x in result['complete_small_censuses']] == [5, 6]
    return {'literal_sets_checked': checked_literal_sets,
            'unpruned_n5_candidates': 8568, 'unpruned_n5_admissible': len(brute_five),
            'status': 'INDEPENDENT_FINITE_CONTROLS_VERIFIED'}


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    print(json.dumps(check(json.loads((here / 'expected.json').read_text()),
                           json.loads((here / 'normal_forms.json').read_text())),
                     sort_keys=True, indent=2))
