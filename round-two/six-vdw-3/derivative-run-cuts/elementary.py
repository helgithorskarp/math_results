#!/usr/bin/env python3
"""Finite symbolic and boundary checks for the written combinatorial proof."""
import itertools
import json
import math


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run_checks():
    periodic = 0
    for pattern in itertools.product((0, 1), repeat=4):
        parities = [sum(pattern[(4*j+3*l) % 4] for l in range(4)) % 2 for j in range(4)]
        need(len(set(parities)) == 1, 'four-periodic telescoping parity')
        periodic += 1
    telescopes = 0
    for q in (7, 13, 23, 103):
        for a in range(q):
            for k in range(1, 5):
                support = set()
                for l in range(k):
                    for x in ((a+3*l) % q, (a+3*(l+1)) % q):
                        support.symmetric_difference_update({x})
                expected = set()
                for x in (a, (a+3*k) % q):
                    expected.symmetric_difference_update({x})
                need(support == expected, 'cyclic telescoping identity')
                telescopes += 1

    macro_cases, admissible = 0, 0
    for R in range(1, 6):
        for blocks in itertools.product(tuple(itertools.product((1, 2, 3), repeat=2)), repeat=R):
            macro_cases += 1
            regular = [a == 1 and b == 3 for a, b in blocks]
            D = regular.count(False)
            if not D or any(all(regular[(j+l) % R] for l in range(5)) for j in range(R)):
                continue
            m = sum(a for a, b in blocks)
            q = m+sum(b for a, b in blocks)
            need(R <= 5*D, 'cyclic regular gap bound')
            need(D <= 2*R-q+2*m, 'defect budget')
            need(5*q <= 9*R+10*m <= 19*m, 'packing density')
            admissible += 1
    # The two extra boundary positions work for either minority bit.
    boundary_cases = 0
    for minority in (0, 1):
        for before in (1, 2, 3):
            for after in (1, 2, 3):
                word = [1-minority]*before+([minority]+[1-minority]*3)*5+[minority]*after
                segment = word[before-1:before+21]
                need(len(segment) == 22 and all(segment[j] == segment[j % 4] for j in range(22)),
                     'five regular blocks boundary extension')
                boundary_cases += 1

    for M in range(32, 73, 2):
        need(2*math.ceil(max(M, 103-M)/3) >= 80-M, 'linear transition floor')
    for n in range(104):
        if 2*n*(103-n) >= 102*32:
            need(20 <= n <= 83, 'orientation weight consequence')
    local_parities = 0
    for bits in itertools.product((0, 1), repeat=4):
        polynomial = sum(bits)-2*sum(bits[i]*bits[j] for i in range(4) for j in range(i+1, 4))
        polynomial += 4*sum(bits[i]*bits[j]*bits[k] for i in range(4) for j in range(i+1, 4) for k in range(j+1, 4))
        polynomial -= 8*math.prod(bits)
        need(polynomial == sum(bits) % 2, 'four-point parity polynomial')
        local_parities += 1
    moment_cases = 0
    for q in (7, 11):
        for mask in range(1 << q):
            S = {x for x in range(q) if mask >> x & 1}
            n = len(S)
            A = B = Q = T = 0
            for a in range(q):
                for r in range(1, q):
                    z = [(a+j*r) % q in S for j in (0, 1, 3, 4)]
                    T += sum(z) % 2
                    A += z[0] and z[1] and z[2]
                    B += z[0] and z[1] and z[3]
                    Q += all(z)
            need(T == 4*n*(q-1)-12*n*(n-1)+8*(A+B-Q), 'global transition moment')
            moment_cases += 1
    # A compact obstruction to strengthening by only steps 1..5.
    word = tuple(map(int, '001000100010010'))
    bad_counts = []
    for k in range(1, 7):
        bad_counts.append(sum(len({sum(word[(a+j*k+3*l) % 15] for l in range(k)) % 2
                                  for j in range(4)}) == 1 for a in range(15)))
    need(bad_counts == [0, 0, 0, 0, 0, 2], 'relaxation counterexample changed')
    need(4*11 < 3*15, 'relaxation does not prove density3/11')
    return {'four_periodic_patterns': periodic, 'cyclic_symbolic_telescopes': telescopes,
            'run_macro_cases': macro_cases, 'admissible_macro_cases': admissible,
            'boundary_extensions': boundary_cases, 'four_point_truth_cases': local_parities,
            'complete_small_transition_moments': moment_cases,
            'relaxation_cycle': '001000100010010', 'relaxation_bad_counts_steps1_to6': bad_counts,
            'status': 'COMBINATORIAL_IDENTITIES_AND_BOUNDARIES_CHECKED'}


if __name__ == '__main__':
    print(json.dumps(run_checks(), sort_keys=True))
