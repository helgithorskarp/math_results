"""Unit actions and signed-translation parameter orbits for split columns.

No SAT imports. Parameter orbits need not be disjoint sets of colourings:
one word may satisfy more than one relation when its state map is periodic.
"""
import argparse
import collections
import itertools
import json
import math
from pathlib import Path


def transform_word(word, u):
    n = len(word)+1
    assert n % 5 == 0 and math.gcd(u, n) == 1
    swap = u % 5 in (2, 3)
    image = [None]*n
    for x, c in enumerate(word, 1):
        image[u*x % n] = 1-c if swap and c in (0, 1) else c
    assert all(c is not None for c in image[1:])
    return image[1:]


def normalize_axis_word(data):
    a = data['axis_factor']
    assert data.get('colours', 6) == 6 and a > 45
    assert all(a % d for d in range(2, math.isqrt(a)+1))
    row = [None, *data['word']]
    q = next(q for q in range(1, a) if row[5*q] in (0, 1))
    short_residue = 1 if row[5*q] == 0 else 2
    u = next(u for u in range(short_residue, 5*a, 5) if u*q % a == 1)
    result = dict(axis_factor=a, short_factor=5, colours=6,
                  word=transform_word(data['word'], u), source_axis=q, multiplier=u)
    assert result['word'][4] == 0
    return result


def columns(word):
    a = (len(word)+1)//5
    return [[word[5*q+b-1] if word[5*q+b-1] >= 2 else 0 for q in range(a)] for b in (1, 2)]


def signed_relations(word):
    q1, q2 = columns(word)
    a = len(q1)
    return [(sign, delta) for sign in (1, -1) for delta in range(a)
            if all(q2[q] == q1[(sign*q+delta) % a] for q in range(a))]


def invariant(a, sign, delta):
    assert sign in (1, -1)
    return math.gcd(5*delta + (-1 if sign == 1 else 3), a)


def action(a, sign, delta, u):
    """Dilation action on the specified relation Q2(q)=Q1(sign*q+delta)."""
    n = 5*a
    assert math.gcd(u, n) == 1
    # Multipliers u and -u give the same image of a reflected word.
    v = u if u % 5 in (1, 2) else -u
    if v % 5 == 1:
        return sign, (v*delta+(1-2*sign)*((v-1)//5)) % a
    assert v % 5 == 2
    return -sign, (sign*v*delta+sign*((v-2)//5)-(2*v+1)//5) % a


def reduce_to_positive(a, sign, delta):
    if sign == 1:
        return 1, delta, 1
    # Dilation by two, and exchange of the two special colours.
    return 1, (-2*delta-1) % a, 2


def reduce_primitive(a, sign, delta):
    """Return a unit taking a primitive parameter to (sign,delta)=(1,0)."""
    assert invariant(a, sign, delta) == 1
    _, positive_delta, first = reduce_to_positive(a, sign, delta)
    n = 5*a
    gamma = (5*positive_delta-1) % n
    second = (-pow(gamma, -1, n)) % n
    assert second % 5 == 1
    u = first*second % n
    assert action(a, sign, delta, u) == (1, 0)
    return u


def pointer(a, sign, delta, x):
    """Independent word rule: state index and special colour at a point."""
    n = 5*a
    x %= n
    q, b = divmod(x, 5)
    assert b
    if b > 2:
        q, b = divmod(n-x, 5)
    return ((q if b == 1 else sign*q+delta) % a, b-1)


def audit_parameter_orbits(a):
    n = 5*a
    units = [u for u in range(1, n) if math.gcd(u, n) == 1]
    parameters = [(s, d) for s in (1, -1) for d in range(a)]
    by_invariant = collections.defaultdict(set)
    for parameter in parameters:
        by_invariant[invariant(a, *parameter)].add(parameter)
    point_checks = 0
    for sign, delta in parameters:
        orbit = set()
        for u in units:
            new_sign, new_delta = action(a, sign, delta, u)
            assert invariant(a, new_sign, new_delta) == invariant(a, sign, delta)
            orbit.add((new_sign, new_delta))
            inv = pow(u, -1, n)
            swap = u % 5 in (2, 3)
            # Literal preimages of every lower second-column point must use
            # the same old state as the related new first-column point.
            # This checks arbitrary state maps symbolically, not chosen words.
            for q in range(a):
                left = pointer(a, sign, delta, inv*(5*q+2))
                right = pointer(a, sign, delta, inv*(5*((new_sign*q+new_delta) % a)+1))
                assert left[0] == right[0]
                assert (1-left[1] if swap else left[1]) == 1
                assert (1-right[1] if swap else right[1]) == 0
                point_checks += 1
        assert orbit == by_invariant[invariant(a, sign, delta)]
        if invariant(a, sign, delta) == 1:
            assert action(a, sign, delta, reduce_primitive(a, sign, delta)) == (1, 0)
    assert set(by_invariant) == {d for d in range(1, a+1) if a % d == 0 and d % 5}
    return dict(axis_factor=a, units=len(units), signed_parameters=len(parameters),
                orbit_sizes={str(d): len(parameters) for d, parameters in sorted(by_invariant.items())},
                symbolic_point_checks=point_checks, status='PARAMETER_ORBITS_VERIFIED')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    results = []
    for a in (1, 5, 7, 13, 25, 47, 77, 105, 109):
        record = audit_parameter_orbits(a)
        results.append(record)
        print(json.dumps(record), flush=True)
    Path(args.output).write_text(json.dumps(results, indent=2)+'\n')


if __name__ == '__main__':
    main()
