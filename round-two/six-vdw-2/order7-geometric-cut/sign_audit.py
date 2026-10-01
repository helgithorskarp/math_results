"""Independent signed-clause audit using explicit coset multiplication.

No generator, Euler-coordinate auditor, or solver import.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def orientations():
    p = 617
    require(all(p % d for d in range(2, 25)), "not prime")
    subgroup = {pow(3, 88*j, p) for j in range(7)}
    require(len(subgroup) == 7 and 616 not in subgroup, "bad signed subgroup")
    slots = {}
    for i in range(44):
        for h in subgroup:
            x = pow(3, i, p)*h % p
            require(x not in slots and -x % p not in slots, "overlapping signed cosets")
            slots[x] = (i, 0)
            slots[-x % p] = (i, 1)
    require(set(slots) == set(range(1, p)), "incomplete signed coset cover")
    return slots


def phase_for(case):
    if case == 'anti':
        return tuple(1 for _ in range(44))
    if case == 'one-opposed-pair':
        return tuple(int(i == 0) for i in range(44))
    if case == 'one-agreed-pair':
        return tuple(int(i != 0) for i in range(44))
    if case == 'even-control':
        return (0,)*44
    raise ValueError('unknown signed profile')


def direct_clause_sets():
    slots = orientations()
    names = ('anti', 'one-opposed-pair', 'one-agreed-pair', 'even-control')
    phases = {name: phase_for(name) for name in names}
    clauses = {name: set() for name in names}
    retained = removed = 0
    for a in range(617):
        for d in range(1, 617):
            positions = [(a+j*d) % 617 for j in range(7)]
            if 0 in positions:
                removed += 1
                continue
            retained += 1
            positions = [slots[x] for x in positions]
            for name, phase in phases.items():
                signed = {(i+1)*(-1 if side and phase[i] else 1) for i, side in positions}
                if not any(-v in signed for v in signed):
                    clauses[name].add(tuple(sorted(signed)))
                    clauses[name].add(tuple(sorted(-v for v in signed)))
    require((retained, removed) == (375760, 4312), "incomplete signed AP coverage")
    # Positive controls retain the actual known QR orientations at phase zero.
    for complement in (0, 1):
        values = {i+1: (i % 2)^complement for i in range(44)}
        require(all(any(values[abs(v)] == int(v > 0) for v in clause)
                    for clause in clauses['even-control']), "QR control rejected")
    return clauses


def read_cnf(path):
    rows = path.read_text().splitlines()
    require(bool(rows), 'empty CNF')
    header = rows[0].split()
    require(len(header) == 4 and header[:3] == ['p', 'cnf', '44'], 'bad signed header')
    count = int(header[3])
    require(count >= 0 and len(rows) == count+1, 'wrong signed clause count')
    clauses = []
    for row in rows[1:]:
        values = list(map(int, row.split()))
        require(values and values[-1] == 0 and all(1 <= abs(x) <= 44 for x in values[:-1]),
                'invalid signed clause')
        clauses.append(tuple(sorted(values[:-1])))
    return clauses


def audit(path, case, expected=None):
    if expected is None:
        expected = direct_clause_sets()
    actual = read_cnf(path)
    require(Counter(actual) == Counter(list(expected[case])+[(-1,)]),
            'signed CNF differs from direct coset/field constraints')
    return {'case': case, 'phase_weight': sum(phase_for(case)), 'variables': 44,
            'clauses': len(actual), 'cnf_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def normalization_controls():
    checked = 0
    for half in range(2, 7):
        for bits in itertools.product((0, 1), repeat=2*half):
            phase = [bits[i]^bits[i+half] for i in range(half)]
            for kind in ('anti', 'one-opposed-pair', 'one-agreed-pair'):
                weight = sum(phase)
                if kind == 'anti':
                    if weight != half:
                        continue
                    shift = 0
                    expected = [1]*half
                elif kind == 'one-opposed-pair':
                    if weight != 1:
                        continue
                    shift = phase.index(1)
                    expected = [1]+[0]*(half-1)
                else:
                    if weight != half-1:
                        continue
                    shift = phase.index(0)
                    expected = [0]+[1]*(half-1)
                rotated = [bits[(i+shift) % (2*half)]^bits[shift] for i in range(2*half)]
                require(rotated[0] == 0, 'color normalization failed')
                require([rotated[i]^rotated[i+half] for i in range(half)] == expected,
                        'minority-phase rotation failed')
                checked += 1
    return {'exhaustive_signed_normalizations_checked': checked, 'QR_positive_controls': 2}


def audit_all(work):
    expected = direct_clause_sets()
    cases = [audit(work/(case+'.cnf'), case, expected)
             for case in ('anti', 'one-opposed-pair', 'one-agreed-pair')]
    return {'status': 'EXACT_ORDER7_SIGN_PHASE_ENCODINGS_AUDITED', 'cases': cases,
            'controls': normalization_controls()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('work', type=Path)
    args = ap.parse_args()
    print(json.dumps(audit_all(args.work), sort_keys=True))


if __name__ == '__main__':
    main()
