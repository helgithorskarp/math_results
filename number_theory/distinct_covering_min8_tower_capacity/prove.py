"""Exclude distinct minimum-at-least-eight coverings in the binary tower of 405.

Author: six-covering-3, researcher. Python >=3.10, standard library only.
Capacity and prime-tree enumeration extend six-covering-2's published work.
The infinite-tail argument and exact scope are in proof.md.
"""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from math import gcd, isqrt
from pathlib import Path
from time import monotonic
import argparse
import json
import sys


class IncompleteSearch(RuntimeError):
    """An operational cutoff supplies no exclusion."""


def divisors(n):
    if not isinstance(n, int) or n < 1:
        raise ValueError('positive integer required')
    found = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            found.update((d, n // d))
    return tuple(sorted(found))


@lru_cache(None)
def factor_levels(n):
    factors, p = [], 2
    while p * p <= n:
        if n % p == 0:
            levels, power = [], 1
            while n % p == 0:
                levels.append(power)
                power *= p
                n //= p
            factors.append((p, tuple(levels)))
        p += 1
    if n > 1:
        factors.append((n, (1,)))
    return tuple(factors)


def valuation(n, p):
    answer = 0
    while n % p == 0:
        n //= p
        answer += 1
    return answer


@lru_cache(None)
def classes(Q, m):
    if Q % m:
        raise ValueError('modulus must divide the base period')
    return tuple(sum(1 << x for x in range(a, Q, m)) for a in range(m))


def maximum_fibre(U, Q, g):
    """Exact maximum population modulo g; bit-sliced for large g."""
    if Q % g:
        raise ValueError('phase modulus must divide the base period')
    if g * g <= Q:
        return max((U & mask).bit_count() for mask in classes(Q, g))
    low, counters = (1 << g) - 1, []
    for shift in range(0, Q, g):
        carry, level = (U >> shift) & low, 0
        while carry:
            if level == len(counters):
                counters.append(carry)
                break
            counters[level], carry = counters[level] ^ carry, counters[level] & carry
            level += 1
    phases, answer = low, 0
    for level in reversed(range(len(counters))):
        candidate = phases & counters[level]
        if candidate:
            phases = candidate
            answer |= 1 << level
    return answer


def canonical_options(modulus, seen):
    """First appearance naming at every prime-digit prefix tree node."""
    for residue in range(modulus):
        updates, valid = {}, True
        for q, levels in factor_levels(modulus):
            for power in levels:
                key = q, power, residue % power
                child, count = residue // power % q, seen.get(key, 0)
                if child >= min(q, count + 1):
                    valid = False
                    break
                updates[key] = max(count, child + 1)
            if not valid:
                break
        if valid:
            following = seen.copy()
            following.update(updates)
            yield residue, following


def case_parameters(p, M, minimum, anchors):
    if p < 2 or any(p % d == 0 for d in range(2, isqrt(p) + 1)):
        raise ValueError('prime p required')
    if M < 1 or gcd(p, M) != 1 or minimum < 2:
        raise ValueError('invalid cofactor or minimum')
    anchors = tuple(anchors)
    if not anchors or len(anchors) != len(set(anchors)) or any(m < minimum for m in anchors):
        raise ValueError('distinct eligible anchors required')
    e = max(valuation(m, p) for m in anchors)
    Q = p**e * M
    if Q > 100000:
        raise IncompleteSearch('base period exceeds this implementation budget')
    if any(Q % m for m in anchors) or p**(e + 1) < minimum:
        raise ValueError('anchors or fully-admissible tail condition fail')
    head = tuple(m for m in divisors(Q) if m >= minimum)
    tail = tuple(p**e * d for d in divisors(M))
    return anchors, e, Q, head, tail


def event_bytes(tag, residues, size, head_capacity, tail_capacity, scaled):
    return (json.dumps([tag, residues, size, head_capacity, tail_capacity, scaled],
                       separators=(',', ':')) + '\n').encode('ascii')


def search(p, M, minimum, anchors, max_nodes=200000, seconds=120):
    anchors, e, Q, head, tail = case_parameters(p, M, minimum, anchors)
    weights = []
    for depth in range(len(anchors) + 1):
        weights.append(Counter(m for m in head if m not in anchors[:depth]))
    nodes, cuts = [0] * (len(anchors) + 1), [0] * (len(anchors) + 1)
    leaves, equalities, upper, least_tail = 0, 0, -1, None
    total, digest, start = 0, sha256(), monotonic()

    def visit(depth, U, seen, residues):
        nonlocal leaves, equalities, upper, least_tail, total
        total += 1
        if total > max_nodes or monotonic() - start > seconds:
            raise IncompleteSearch(f'budget reached: M={M}, nodes={total}')
        nodes[depth] += 1
        phases = {g: maximum_fibre(U, Q, g) for g in weights[depth].keys() | set(tail)}
        head_cap = sum(count * phases[g] for g, count in weights[depth].items())
        tail_cap = sum(phases[g] for g in tail)
        scaled = (p - 1) * (Q - U.bit_count() + head_cap) + tail_cap
        cut = bool(U) and scaled <= (p - 1) * Q
        if cut or depth == len(anchors):
            if cut:
                cuts[depth] += 1
                equalities += scaled == (p - 1) * Q
                if tail_cap <= 0:
                    raise RuntimeError('nonempty residual has zero tail capacity')
                least_tail = tail_cap if least_tail is None else min(least_tail, tail_cap)
            else:
                leaves += 1
            upper = max(upper, scaled)
            digest.update(event_bytes('cut' if cut else 'leaf', residues, U.bit_count(),
                                      head_cap, tail_cap, scaled))
            return
        m = anchors[depth]
        for residue, following in canonical_options(m, seen):
            visit(depth + 1, U & ~classes(Q, m)[residue], following, residues + (residue,))

    visit(0, (1 << Q) - 1, {}, ())
    return {'p': p, 'M': M, 'minimum_threshold': minimum, 'base_exponent': e,
            'Q': Q, 'anchors': list(anchors), 'head_moduli': list(head),
            'tail_phase_moduli': list(tail), 'nodes_per_depth': nodes,
            'cuts_per_depth': cuts, 'nodes': total, 'cuts': sum(cuts),
            'uncut_leaves': leaves, 'excludes_every_finite_exponent': leaves == 0,
            'max_scaled_infinite_capacity': upper, 'scaled_period': (p - 1) * Q,
            'equality_cuts': equalities, 'min_tail_capacity_at_cut': least_tail,
            'proof_events_sha256': digest.hexdigest()}


ANCHORS_135 = (8, 9, 10, 12, 15, 18, 20, 24)
ANCHORS_405 = (8, 9, 10, 12, 15, 18, 20, 24, 27, 30, 36, 40, 45,
               54, 60, 72, 81, 90, 108, 120, 135)


def prove():
    results = [search(2, 135, 8, ANCHORS_135), search(2, 405, 8, ANCHORS_405)]
    if not all(result['excludes_every_finite_exponent'] for result in results):
        raise RuntimeError('At least one case remains unresolved')
    return {'agent': 'six-covering-3', 'role': 'researcher',
            'claim': 'No finite distinct covering with all moduli >=8 in {2^j*d: d|405}',
            'arithmetic': 'exact integers; infinite tails summed mathematically',
            'cases': results}


def main():
    if sys.version_info < (3, 10):
        raise RuntimeError('Python >=3.10 required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    start, result = monotonic(), prove()
    if args.check is not None and result != json.loads(args.check.read_text()):
        raise RuntimeError('Complete output differs from expected manifest')
    if args.write is not None:
        args.write.write_text(json.dumps(result, indent=2) + '\n')
    for case in result['cases']:
        print(f'M={case["M"]}: {case["nodes"]} nodes, {case["cuts"]} cuts, '
              f'{case["uncut_leaves"]} uncut leaves, {case["equality_cuts"]} equality cuts')
    print('PROVED: minimum >=8 is impossible in every finite binary tower of 405.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
