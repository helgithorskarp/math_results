"""Literal controls for all sixteen phases at the prescribed five-class root.

These controls verify transports and redundant classes. The separate complete
odd16 tree is required before any covering exclusion or presence conclusion.
"""
from hashlib import sha256
import json

N = 10080
P = ((8, 0), (9, 0), (10, 1), (14, 0), (12, 4))
D = tuple(m for m in range(1, N + 1) if N % m == 0)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(a):
    require(type(a) is int and 0 <= a < 16, 'Noncanonical16 phase')
    if a in (0, 8):
        return None
    if a % 2:
        return 1
    return 2 if a % 4 == 2 else 4


def transport(a):
    target = canonical(a)
    require(target is not None, 'Redundant16 phase has no transport')
    if target == 1:
        q, r = 2, 1
        k = 630 * ((3 * ((1 - a) // 2)) % 8)
    elif target == 2:
        q, r = 4, 2
        k = 1260 * ((3 * ((2 - a) // 4)) % 4)
    else:
        q, r = 8, 4
        k = 2520 * (((4 - a) // 8) % 2)
    return tuple((x + k) % N if x % q == r else x for x in range(N))


def check():
    digest = sha256()
    classes_checked = 0
    cases = []
    for a in range(16):
        target = canonical(a)
        if target is None:
            require(all(x % 8 == 0 for x in range(a, N, 16)),
                    'False redundant16 class')
            cases.append([a, 'redundant inside8:0'])
            continue
        perm = transport(a)
        require(len(set(perm)) == N, 'Transport is not a bijection')
        require(all((x % 16 == a) == (y % 16 == target)
                    for x, y in enumerate(perm)), 'Wrong16 image')
        for m, phase in P:
            require(all((x % m == phase) == (y % m == phase)
                        for x, y in enumerate(perm)), 'Prescribed class moves')
        for m in D:
            images = [-1] * m
            for x, y in enumerate(perm):
                r, s = x % m, y % m
                if images[r] == -1:
                    images[r] = s
                require(images[r] == s, 'A divisor class splits')
            require(set(images) == set(range(m)), 'Modulus labels not preserved')
            classes_checked += m
            digest.update(json.dumps([a, m, images], separators=(',', ':')).encode())
        cases.append([a, target])
    return {'root': P, 'phase_cases': cases, 'divisor_labels': len(D),
            'literal_class_images': classes_checked,
            'digest_sha256': digest.hexdigest(),
            'odd_phases': list(range(1, 16, 2)),
            'redundant_even_phases': [0, 8],
            'allowed_even_phases_if_odd16_excluded': [2, 4, 6, 10, 12, 14],
            'remaining_canonical_phases_if_odd16_excluded': [2, 4]}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
