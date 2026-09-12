#!/usr/bin/env python3
"""Exact finite controls for proof.md; no inference from finite n to all n."""
import hashlib
import json
from math import gcd
from pathlib import Path


def signed_classes(values, modulus):
    return tuple(sorted(min(x % modulus, (-x) % modulus) for x in values))


def representative(n, kind):
    m = 1 << (n - 2)
    return tuple(1 << i for i in range(n - 2)) + (
        m + (kind == 2), 2 * m + (kind != 0))


def rotate(bits, shift, modulus):
    return ((bits << shift) | (bits >> (modulus - shift))) & ((1 << modulus) - 1)


def sum_distinct(values, modulus):
    bits = 1
    for value in values:
        shifted = rotate(bits, value, modulus)
        if bits & shifted:
            return False
        bits |= shifted
    return True


def edges(values, modulus):
    vertices = set(values)
    return [(a, b) for a in values
            if (b := min(2 * a % modulus, -2 * a % modulus)) in vertices]


def census(n):
    """Every increasing positive signed-class representative, with safe pruning.

    A collision in a prefix persists in all extensions, so pruning is complete.
    Choosing signs covers every actual subset; zero/opposite pairs are invalid.
    """
    modulus = (1 << n) + 5
    found = []

    def visit(values, bits, lower):
        if len(values) == n:
            found.append(values)
            return
        upper = modulus // 2 - (n - len(values)) + 1
        for a in range(lower, upper + 1):
            shifted = rotate(bits, a, modulus)
            if not bits & shifted:
                visit(values + (a,), bits | shifted, a + 1)

    visit((), 1, 1)
    return found


def build():
    rows = json.loads(Path(__file__).with_name('normal_forms.json').read_text())['rows']
    assert {(r['a'], r['b']) for r in rows} == {
        (a, b) for b in range(3) for a in range(b + 1)}
    controls = []
    for n in range(5, 11):
        m = 1 << (n - 2)
        modulus = 4 * m + 5
        chain = tuple(1 << i for i in range(n - 2))
        pairs = []
        for x in range(1, modulus // 2 + 1):
            if x in chain or not sum_distinct(chain + (x,), modulus):
                continue
            for y in range(x + 1, modulus // 2 + 1):
                if y not in chain and sum_distinct(chain + (x, y), modulus):
                    pairs.append((x - m, y - 2 * m))
        assert pairs == sorted((r['a'], r['b']) for r in rows)
        for r in rows:
            values = chain + (m + r['a'], 2 * m + r['b'])
            image = signed_classes((r['multiplier'] * a for a in values), modulus)
            assert image == representative(n, r['class'])
        units = [u for u in range(1, modulus) if gcd(u, modulus) == 1]
        graphs, stabilizers = [], []
        for kind in range(3):
            values = representative(n, kind)
            assert sum_distinct(values, modulus)
            graph = edges(values, modulus)
            assert len(graph) == n - 1 - kind
            graphs.append(graph)
            stabilizer = [u for u in units
                          if signed_classes((u * a for a in values), modulus) == values]
            assert stabilizer == [1, modulus - 1]
            stabilizers.append(stabilizer)
        controls.append({'n': n, 'N': modulus, 'normalized_pairs': pairs,
                         'graphs': graphs, 'stabilizers': stabilizers,
                         'phi': len(units),
                         'chain_family_subsets': 3 * (1 << (n - 1)) * len(units)})

    censuses = []
    for n in [5, 6]:
        modulus = (1 << n) + 5
        found = census(n)
        orbit_sets = []
        for kind in range(3):
            base = representative(n, kind)
            orbit_sets.append({signed_classes((u * a for a in base), modulus)
                               for u in range(1, modulus) if gcd(u, modulus) == 1})
        assert all(not orbit_sets[i] & orbit_sets[j]
                   for i in range(3) for j in range(i))
        assert set(found) == set.union(*orbit_sets)
        censuses.append({'n': n, 'N': modulus, 'signed_class_sets': found,
                         'class_sizes_in_signed_quotient': list(map(len, orbit_sets)),
                         'all_actual_subsets': len(found) * (1 << n),
                         'unclassified_signed_class_sets': []})
    return {'status': 'UNIFORM_CHAIN_THEOREM_FINITE_CONTROLS_VERIFIED',
            'uniformity_basis': 'Written proof.md, not these finite controls',
            'normal_forms_sha256': hashlib.sha256(
                Path(__file__).with_name('normal_forms.json').read_bytes()).hexdigest(),
            'controls': controls, 'complete_small_censuses': censuses}


if __name__ == '__main__':
    print(json.dumps(build(), sort_keys=True, indent=2))
