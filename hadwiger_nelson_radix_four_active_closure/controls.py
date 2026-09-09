#!/usr/bin/env python3
"""Small, independent boundary controls; the full replay is verify.py."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations, permutations
import json
from pathlib import Path
import verify as V


def rejects(thunk):
    try:
        thunk()
    except (ValueError, IndexError, KeyError, StopIteration):
        return
    raise ValueError('invalid input was accepted')


def main():
    # Algebraic obstruction used for every K4 certificate.
    gram = [[Q(1) if i == j else Q(1, 2) for j in range(3)] for i in range(3)]
    determinant = Q(0)
    for perm in permutations(range(3)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(3) for j in range(i + 1, 3))
        value = Q(sign)
        for i, j in enumerate(perm):
            value *= gram[i][j]
        determinant += value
    V.require(determinant == Q(1, 2), 'K4 Gram determinant')

    edges = set(combinations(range(4), 2))
    V.check_clique((0, 1, 2, 3), edges)
    rejects(lambda: V.check_clique((0, 1, 2, 2), edges))
    rejects(lambda: V.check_clique((0, 1, 2, 243), edges))
    rejects(lambda: V.check_clique((False, 1, 2, 3), edges))
    for edge in edges:
        rejects(lambda edge=edge: V.check_clique((0, 1, 2, 3), edges - {edge}))
    bits = [sum(1 << v for v in range(4) if u != v) for u in range(4)]
    V.require(V.first_clique_bits(bits) == (0, 1, 2, 3), 'K4 reconstruction')
    rejects(lambda: V.first_clique_bits([6, 5, 3]))  # A triangle is not K4.

    # The independently expanded one-digit and two-digit norm identities.
    powers = V.radix_powers()
    zero, one = (0, 0), (1, 0)
    V.require(V.event((one, zero, zero, zero, zero), powers) == (), 'universal event')
    V.require(V.event((zero, one, zero, zero, zero), powers) == ((0, 0, -1), (0, 2, 3), (2, 0, 1)), 'circle event')
    V.require(V.event((one, one, zero, zero, zero), powers) == ((0, 2, 3), (1, 0, 2), (2, 0, 1)), '|1+z| squared minus one')
    V.require(all(V.times(u, (u[0] + u[1], -u[1])) == one for u in V.UNITS), 'six exact units')
    for row in [(one, one, zero, zero, zero), (zero, (0, 1), (-1, 0), zero, one)]:
        V.require(all(V.canonical(tuple(V.times(u, d) for d in row)) == V.canonical(row) for u in V.UNITS), 'unit orbit normalization')

    certificate = json.loads((Path(__file__).resolve().parent / 'certificate.json').read_text())
    for field in ['eligible_quartets', 'impossible_planar_K4', 'minimum_active_curves_for_nonfour',
                  'entrywise_witness_transcript_sha256', 'forbidden_incidence_list_sha256']:
        corrupt = deepcopy(certificate)
        corrupt[field] = 'corrupted'
        rejects(lambda corrupt=corrupt: V.require(corrupt == certificate, 'certificate mismatch'))
    print(json.dumps({'verified': True, 'K4_gram_determinant': str(determinant),
                      'rejected_invalid_cliques': 9, 'rejected_triangle_as_K4': 1,
                      'rejected_certificate_corruptions': 5,
                      'exact_norm_identity_controls': 3, 'unit_normalization_controls': 2}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
