#!/usr/bin/env python3
"""Run exact finite corroboration; PROOF.md supplies the asymptotic theorem."""
from fractions import Fraction
from itertools import product
import json
import game_checks
import templates


def require(condition, message):
    if not condition:
        raise ValueError(message)


def probabilities():
    p, q = Fraction(1, 3), Fraction(2, 3)
    directions = vectors = codes = couplings = 0
    for a, b, h in product(range(3), range(3), range(2)):
        n = a + b + h
        A = set(range(a + h))
        B = set(range(a, n))
        diff = Fraction(0)
        for mask in range(1 << n):
            hit_A = any(mask >> i & 1 for i in A)
            hit_B = any(mask >> i & 1 for i in B)
            if hit_A != hit_B:
                ones = mask.bit_count()
                diff += p ** ones * q ** (n - ones)
        formula = q ** len(A) * (1 - q ** len(B - A))
        formula += q ** len(B) * (1 - q ** len(A - B))
        require(diff == formula, 'direction separation formula')
        directions += 1
        equal_vectors = Fraction(0)
        for mask in range(1 << (2 * n)):
            equal = all(any(mask >> (j * n + i) & 1 for i in A)
                        == any(mask >> (j * n + i) & 1 for i in B) for j in (0, 1))
            if equal:
                ones = mask.bit_count()
                equal_vectors += p ** ones * q ** (2 * n - ones)
        require(equal_vectors == (1 - formula) ** 2, 'independent direction vectors')
        vectors += 1
    for d in range(1, 6):
        match = Fraction(0)
        for mask in range(1 << (2 * d)):
            if all((mask >> i & 1) == (mask >> (i + d) & 1) for i in range(d)):
                ones = mask.bit_count()
                match += p ** ones * q ** (2 * d - ones)
        require(match == (p * p + q * q) ** d, 'NN code-equality probability')
        codes += 1
    for denominator in range(3, 12):
        for lo in range(1, denominator):
            for hi in range(lo + 1, denominator):
                low, high = Fraction(lo, denominator), Fraction(hi, denominator)
                rho = (high - low) / (1 - low)
                require(0 < rho < 1 and low + (1 - low) * rho == high, 'edge-addition marginal')
                couplings += 1
    coefficient = Fraction(31, 64)
    K = 23
    require(Fraction(1, 2) + K * (Fraction(15, 8) - 4 * coefficient) < 0,
            'concrete star exponent')
    require(2 + K * (Fraction(7, 8) - 2 * coefficient) < 0, 'concrete pair exponent')
    for M in range(3, 101):
        c_plus = Fraction(1, 2) + Fraction(1, 2 * M - 1)
        require(1 / (2 * c_plus - 1) == Fraction(2 * M - 1, 2), 'slowdown coefficient')
        require(coefficient < c_plus, 'edge probabilities not ordered')
    return {'direction_identities': directions, 'two_direction_vector_identities': vectors,
            'NN_code_identities': codes, 'rational_edge_couplings': couplings,
            'slowdown_coefficients': 98, 'concrete_coefficient': '31/64',
            'concrete_alternative_probes': K}


def main():
    result = {'status': 'VERIFIED',
              'scope': 'finite exact corroboration; asymptotic proof is PROOF.md',
              'templates': templates.run(), 'game': game_checks.run(),
              'probabilities': probabilities()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
