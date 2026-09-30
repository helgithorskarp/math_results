"""Bounded exact arithmetic audits of the written coefficient reduction.

The polynomial identities and quantified proof are in PROOF.md. These audits
are supporting checks, not an exhaustive enumeration of all polynomial seeds.
Run the two modes sequentially; each uses fewer than 200000 arithmetic cases.
"""
import argparse
from math import comb, gcd
import json

P = 311


def require(condition):
    if not condition:
        raise ArithmeticError('Reduction arithmetic check failed')


def character(x):
    x %= P
    if x == 0:
        return 0
    return 1 if pow(x, 155, P) == 1 else -1


def field_audit():
    require(all(P % d for d in range(2, 18)))
    squares = {x*x % P for x in range(1, P)}
    require(len(squares) == 155 and 11 not in squares)
    require(all((character(x) == 1) == (x in squares) for x in range(1, P)))
    multiplication_cases = 0
    for x in range(P):
        for y in range(P):
            require(character(x*y) == character(x)*character(y))
            multiplication_cases += 1
    square_roots = {u*u % P: u for u in range(1, P)}
    for d in range(P):
        representative = 0 if d == 0 else (1 if d in squares else 11)
        u = 1 if d == 0 else square_roots[d*pow(representative, -1, P) % P]
        require(d == representative*u*u % P)
    require(gcd(3, P-1) == 1 and 3*207 % (P-1) == 1)
    require(len({u**3 % P for u in range(1, P)}) == 310)
    for b in range(1, P):
        require(pow(pow(b, 207, P), 3, P) == b)
    for u in range(1, P):
        lift = u if u % 2 else u+P
        require(lift % 2 == 1 and lift % P == u and gcd(lift, 622) == 1)
    for v in range(P):
        lift = v if v % 2 == 0 else v+P
        require(lift % 2 == 0 and lift % P == v)
    # Raw parameter/root-choice counts, derived in PROOF.md, not distinct words.
    monic_cubic_by_roots = {3: comb(P, 3), 2: P*(P-1),
                           1: P + P*(P*(P-1)//2)}
    monic_cubic_by_roots[0] = P**3 - sum(monic_cubic_by_roots.values())
    quadratic_weight = (P-1)*P*(2 + ((P-1)//2)*4 + (P-1)//2)
    linear_weight = (P-1)*P*2
    constant_weight = P-1
    cubic_weight = (P-1)*sum((2**r)*count for r, count in monic_cubic_by_roots.items())
    total_weight = quadratic_weight + linear_weight + constant_weight + cubic_weight
    require(total_weight == 24911476620)
    counts = {'primality_divisibility_cases': 16, 'square_table_cases': 310,
              'square_character_cases': 310, 'square_root_table_cases': 310,
              'character_multiplication_cases': multiplication_cases,
              'square_class_cases': 311, 'cube_bijection_cases': 310,
              'cube_exponent_case': 1, 'cube_inverse_cases': 310,
              'CRT_multiplier_cases': 310, 'CRT_translation_cases': 311}
    require(sum(counts.values()) < 200000)
    return {'status': 'FIELD_AND_PARAMETER_COUNT_AUDIT_PASSED', **counts,
            'total_arithmetic_cases': sum(counts.values()),
            'nonzero_degree_le3_raw_coefficient_root_assignments': total_weight,
            'monic_cubic_counts_by_distinct_roots': monic_cubic_by_roots,
            'no_distinct_word_or_orbit_count_claim': True}


def shift_audit():
    cases = 0
    for a in range(1, P):
        for b in range(P):
            v2 = -b*pow(2*a, -1, P) % P
            require((2*a*v2+b) % P == 0)
            cases += 1
            v3 = -b*pow(3*a, -1, P) % P
            require((3*a*v3+b) % P == 0)
            cases += 1
    require(cases == 192820)
    return {'status': 'ALL_QUADRATIC_AND_CUBIC_LEADING_SHIFT_CASES_PASSED',
            'leading_shift_cases': cases, 'child_case_cap': 200000,
            'remaining_coefficients': 'covered by symbolic identities in PROOF.md'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=('field', 'shifts'), required=True)
    args = parser.parse_args()
    print(json.dumps(field_audit() if args.mode == 'field' else shift_audit(), sort_keys=True))


if __name__ == '__main__':
    main()
