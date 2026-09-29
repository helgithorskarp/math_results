"""Full replay using literal populations and original-child relabeling.

This is a separate algorithm by the same researcher, not an external review.
No production fibre counter or production symmetry generator is called.
"""
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
from time import monotonic
import argparse
import json
import random
import prove as fast


@lru_cache(None)
def prime_powers(m):
    factors = []
    for q in range(2, m + 1):
        if m % q:
            continue
        power = 1
        while m % q == 0:
            power *= q
            m //= q
        factors.append((q, power))
        if m == 1:
            break
    return tuple(factors)


def original_names(previous):
    names = {}
    for m, a in previous:
        for q, maximal in prime_powers(m):
            power = 1
            while power < maximal:
                key = q, power, a % power
                digits = names.setdefault(key, {})
                child = a // power % q
                if child not in digits:
                    digits[child] = len(digits)
                power *= q
    return names


def normalize(previous):
    names, answer = {}, []
    for m, a in previous:
        coordinates = []
        for q, maximal in prime_powers(m):
            encoded, power = 0, 1
            while power < maximal:
                key = q, power, a % power
                digits = names.setdefault(key, {})
                child = a // power % q
                if child not in digits:
                    digits[child] = len(digits)
                encoded += power * digits[child]
                power *= q
            coordinates.append((maximal, encoded))
        image = next(r for r in range(m) if all(r % q == b for q, b in coordinates))
        answer.append((m, image))
    return tuple(answer)


def reference_options(m, previous):
    """Normalize original children, then test if the candidate already has that name."""
    names = original_names(previous)
    for a in range(m):
        canonical = True
        for q, maximal in prime_powers(m):
            encoded, power = 0, 1
            while power < maximal:
                digits = names.get((q, power, a % power), {})
                child = a // power % q
                encoded += power * digits.get(child, len(digits))
                power *= q
            if encoded != a % maximal:
                canonical = False
                break
        if canonical:
            yield a


def literal_case(p, M, minimum, anchors, max_nodes=200000, seconds=120):
    # Determine the period and every divisor without production helpers.
    e = 0
    for m in anchors:
        exponent, quotient = 0, m
        while quotient % p == 0:
            exponent += 1
            quotient //= p
        e = max(e, exponent)
    Q = p**e * M
    head = tuple(m for m in range(minimum, Q + 1) if Q % m == 0)
    tail = tuple(p**e * d for d in range(1, M + 1) if M % d == 0)
    remaining = [tuple(m for m in head if m not in anchors[:depth])
                 for depth in range(len(anchors) + 1)]
    phase_moduli = sorted(set(head) | set(tail))
    # Literal populations, updated by actual x % g for every removed point.
    counts = {g: [Q // g] * g for g in phase_moduli}
    active = bytearray([1]) * Q
    size = Q
    nodes, cuts = [0] * (len(anchors) + 1), [0] * (len(anchors) + 1)
    total, leaves, equalities, upper, least_tail = 0, 0, 0, -1, None
    digest, start = sha256(), monotonic()

    def visit(depth, residues):
        nonlocal total, leaves, equalities, upper, least_tail, size
        total += 1
        if total > max_nodes or monotonic() - start > seconds:
            raise fast.IncompleteSearch('literal audit budget reached')
        nodes[depth] += 1
        maxima = {g: max(populations) for g, populations in counts.items()}
        head_cap = sum(maxima[g] for g in remaining[depth])
        tail_cap = sum(maxima[g] for g in tail)
        scaled = (p - 1) * (Q - size + head_cap) + tail_cap
        cut = size > 0 and scaled <= (p - 1) * Q
        if cut or depth == len(anchors):
            if cut:
                cuts[depth] += 1
                equalities += scaled == (p - 1) * Q
                if tail_cap <= 0:
                    raise RuntimeError('invalid zero-tail equality cut')
                least_tail = tail_cap if least_tail is None else min(least_tail, tail_cap)
            else:
                leaves += 1
            upper = max(upper, scaled)
            event = ['cut' if cut else 'leaf', residues, size, head_cap, tail_cap, scaled]
            digest.update((json.dumps(event, separators=(',', ':')) + '\n').encode('ascii'))
            return
        m = anchors[depth]
        previous = tuple(zip(anchors[:depth], residues))
        for a in reference_options(m, previous):
            # Definition-level removal, with no bitsets or phase projection.
            removed = [x for x in range(Q) if active[x] and x % m == a]
            for x in removed:
                active[x] = 0
                for g, populations in counts.items():
                    populations[x % g] -= 1
            size -= len(removed)
            visit(depth + 1, residues + (a,))
            size += len(removed)
            for x in removed:
                active[x] = 1
                for g, populations in counts.items():
                    populations[x % g] += 1

    visit(0, ())
    if size != Q or any(not x for x in active):
        raise RuntimeError('literal replay failed to restore the base state')
    return {'p': p, 'M': M, 'minimum_threshold': minimum, 'base_exponent': e,
            'Q': Q, 'anchors': list(anchors), 'head_moduli': list(head),
            'tail_phase_moduli': list(tail), 'nodes_per_depth': nodes,
            'cuts_per_depth': cuts, 'nodes': total, 'cuts': sum(cuts),
            'uncut_leaves': leaves, 'excludes_every_finite_exponent': leaves == 0,
            'max_scaled_infinite_capacity': upper, 'scaled_period': (p - 1) * Q,
            'equality_cuts': equalities, 'min_tail_capacity_at_cut': least_tail,
            'proof_events_sha256': digest.hexdigest()}


def literal_finite_capacity(p, M, e, minimum, anchors, U, h):
    Q, L = p**e * M, p**(e + h) * M
    points = [x for x in range(L) if U >> (x % Q) & 1]
    covered = L - len(points)
    for m in range(minimum, L + 1):
        if L % m or m in anchors:
            continue
        populations = [0] * m
        for x in points:
            populations[x % m] += 1
        covered += max(populations)
    return covered


def finite_formula(p, M, e, minimum, anchors, U, h):
    Q = p**e * M
    head_cap = sum(fast.maximum_fibre(U, Q, m) for m in fast.divisors(Q)
                   if m >= minimum and m not in anchors)
    tail_cap = sum(fast.maximum_fibre(U, Q, p**e * d) for d in fast.divisors(M))
    return p**h * (Q - U.bit_count() + head_cap) + (p**h - 1) // (p - 1) * tail_cap


def controls():
    symmetry = []
    for moduli in ((2, 3, 4), (8, 9, 10), (8, 10, 12), (3, 4, 6, 9)):
        literal = {normalize(tuple(zip(moduli, residues)))
                   for residues in product(*(range(m) for m in moduli))}
        produced, replayed = set(), set()
        def generate(depth, seen, residues):
            if depth == len(moduli):
                produced.add(tuple(zip(moduli, residues)))
                return
            for a, following in fast.canonical_options(moduli[depth], seen):
                generate(depth + 1, following, residues + (a,))
        def replay(depth, previous):
            if depth == len(moduli):
                replayed.add(previous)
                return
            m = moduli[depth]
            for a in reference_options(m, previous):
                replay(depth + 1, previous + ((m, a),))
        generate(0, {}, ())
        replay(0, ())
        if literal != produced or literal != replayed:
            raise RuntimeError('complete symmetry-control sets differ')
        symmetry.append({'moduli': list(moduli), 'literal_tuples': len(list(product(*(range(m) for m in moduli)))),
                         'canonical_tuples': len(literal)})
    finite_checks = 0
    for p, M, e, minimum in ((2, 3, 0, 2), (2, 3, 1, 2), (3, 2, 1, 2)):
        Q = p**e * M
        for U in range(1 << Q):
            for h in (1, 2, 3):
                actual = literal_finite_capacity(p, M, e, minimum, (), U, h)
                formula = finite_formula(p, M, e, minimum, (), U, h)
                if actual != formula:
                    raise RuntimeError('literal finite-horizon capacity differs')
                finite_checks += 1
    rng = random.Random(20260929)
    for M, anchors in ((135, fast.ANCHORS_135), (405, fast.ANCHORS_405)):
        Q = 8 * M
        for U in (0, (1 << Q) - 1, rng.getrandbits(Q), 1 | (1 << (Q - 1))):
            for h in (1, 2):
                if literal_finite_capacity(2, M, 3, 8, anchors[:5], U, h) != finite_formula(2, M, 3, 8, anchors[:5], U, h):
                    raise RuntimeError('large literal capacity control differs')
                finite_checks += 1
    # A real positive cover: no nonempty prefix may be excluded.
    witness, Q, U = ((2, 0), (3, 0), (4, 1), (6, 1), (12, 11)), 12, (1 << 12) - 1
    used = []
    for m, a in witness:
        U &= ~sum(1 << x for x in range(Q) if x % m == a)
        used.append(m)
        head = sum(fast.maximum_fibre(U, Q, d) for d in (2, 3, 4, 6, 12) if d not in used)
        tail = sum(fast.maximum_fibre(U, Q, d) for d in (4, 12))
        if U and Q - U.bit_count() + head + tail <= Q:
            raise RuntimeError('a prefix of a known cover was excluded')
    if U:
        raise RuntimeError('known covering fixture does not cover')
    for runner in (fast.search, literal_case):
        try:
            runner(2, 405, 8, fast.ANCHORS_405, max_nodes=1)
        except fast.IncompleteSearch:
            pass
        else:
            raise RuntimeError('a budget cutoff was accepted as complete')
    return {'symmetry_controls': symmetry, 'literal_finite_capacity_checks': finite_checks,
            'positive_cover_prefixes_checked': 5, 'incomplete_search_rejections': 2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    start = monotonic()
    print(json.dumps(controls(), indent=2), flush=True)
    expected = json.loads(args.expected.read_text())
    for case in expected['cases']:
        actual = literal_case(case['p'], case['M'], case['minimum_threshold'], tuple(case['anchors']))
        if actual != case:
            raise RuntimeError(f'complete literal replay differs for M={case["M"]}')
        print(f'M={case["M"]}: identical full proof-event digest and all manifest fields', flush=True)
    print('FULL AUDIT PASSED: literal populations, separate normalization, finite-horizon controls.')
    print(f'Elapsed seconds: {monotonic() - start:.3f}')


if __name__ == '__main__':
    main()
