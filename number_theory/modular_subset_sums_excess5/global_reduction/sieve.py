#!/usr/bin/env python3
"""Exact, exhaustive one-parameter sieve justified in proof.md, Sections 3-5."""
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path


def is_prime(p):
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    return all(p % d for d in range(3, isqrt(p) + 1, 2))


def prime_divisors(value):
    divisors = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            divisors.append(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        divisors.append(value)
    return divisors


def validate_field(n, N, p, root):
    if N != 2 ** n + 5 or not is_prime(p) or (p - 1) % N:
        raise ValueError('Invalid modulus/prime certificate')
    if not 0 < root < p or pow(root, N, p) != 1:
        raise ValueError('Root does not have order dividing N')
    if any(pow(root, N // q, p) == 1 for q in prime_divisors(N)):
        raise ValueError('Root has order smaller than N')


def known_cores(N):
    result = set()
    for u, v in [(1, 2), (1, 3), (3, 4)]:
        for anchor, other in [(u, v), (v, u)]:
            if gcd(anchor, N) == 1:
                b = other * pow(anchor, -1, N) % N
                result.add(min(b, N - b))
    return sorted(result)


def evaluate(field):
    n, N, p, root = (field[k] for k in ['n', 'N', 'p', 'root'])
    validate_field(n, N, p, root)
    powers = [1]
    for _ in range(1, N):
        powers.append(powers[-1] * root % p)
    cosines = [(powers[j] + powers[-j % N]) % p for j in range(N)]
    candidates = [b for b in range(2, N // 2 + 1) if gcd(b, N) in (1, 3)]
    survivors = []
    digest = hashlib.sha256()
    for b in candidates:
        product = 1
        index = b
        for j in range(1, N // 2 + 1):
            product = product * (1 + cosines[j] + cosines[index]) % p
            index += b
            if index >= N:
                index -= N
        square = product * product % p
        target = 4 if gcd(b, N) == 3 else 1
        digest.update(f'{b}:{square}\n'.encode('ascii'))
        if square == target:
            survivors.append(b)
    known = known_cores(N)
    if survivors != known:
        raise AssertionError(f'Unresolved or lost cores at n={n}: {survivors}, expected {known}')
    phi = sum(gcd(a, N) == 1 for a in range(1, N))
    return {'n': n, 'N': N, 'p': p, 'root': root,
            'candidate_count': len(candidates),
            'excluded_count': len(candidates) - len(survivors),
            'surviving_cores': survivors,
            'ordered_residue_sha256': digest.hexdigest(),
            'equivalence_classes': 3,
            'exact_subset_count': 3 * 2 ** (n - 1) * phi}


def build():
    certificate = json.loads(Path(__file__).with_name('certificate.json').read_text())
    if [f['n'] for f in certificate['fields']] != list(range(5, 15)):
        raise ValueError('Certificate must cover every n=5,...,14 exactly once')
    return {'status': 'ALL_NORMALIZED_CORES_COVERED_N5_THROUGH_N14',
            'scope': 'Unrestricted classification for each n=5,...,14 via proof.md',
            'uniform_count_basis': 'Theorems1-2 of proof.md, not extrapolation',
            'results': [evaluate(field) for field in certificate['fields']]}


if __name__ == '__main__':
    print(json.dumps(build(), sort_keys=True, indent=2))
