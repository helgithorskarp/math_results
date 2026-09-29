#!/usr/bin/env python3
"""six-reviewer-1: independent exact replay of the 135/405 binary towers.

No target module is imported. Literal congruence masks count capacities;
pairwise prime-power agreements give stabilizer orbits. Child renaming is
used only for comparing terminal records, never for choosing search branches.
The infinite-exponent bridge is proved in README.md.
"""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from math import gcd
from pathlib import Path
from time import monotonic


class IncompleteSearch(RuntimeError):
    pass


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def divisors(n):
    return tuple(d for d in range(1, n+1) if n % d == 0)


@lru_cache(None)
def factors(n):
    answer = []
    for p in range(2, n+1):
        if n % p:
            continue
        power = 1
        while n % p == 0:
            n //= p
            power *= p
        answer.append((p, power))
        if n == 1:
            break
    return tuple(answer)


def signature(m, a, previous):
    return tuple(gcd(a-b, q) for n, b in previous
                 for _, q in factors(gcd(m, n)))


def representatives(m, previous):
    seen = set()
    for a in range(m):
        s = signature(m, a, previous)
        if s not in seen:
            seen.add(s)
            yield a


def renamed_residues(previous):
    """Canonical record key only; this function cannot prune a branch."""
    children, output = {}, []
    for m, a in previous:
        coordinates = []
        for p, maximal in factors(m):
            original_prefix, encoded, power = (), 0, 1
            while power < maximal:
                digit = (a//power) % p
                ranks = children.setdefault((p, original_prefix), {})
                if digit not in ranks:
                    ranks[digit] = len(ranks)
                encoded += power*ranks[digit]
                original_prefix += (digit,)
                power *= p
            coordinates.append((maximal, encoded))
        # CRT reconstruction, independent of the author's residue scan.
        image = sum(b*(m//q)*pow(m//q, -1, q) for q, b in coordinates) % m
        output.append(image)
    return output


def masks(Q, moduli):
    answer = {}
    for m in moduli:
        require(Q % m == 0, 'phase modulus does not divide the period')
        classes = [0]*m
        for x in range(Q):
            classes[x % m] |= 1 << x
        answer[m] = tuple(classes)
    return answer


def maxima(Q, U, phases):
    answer = {}
    for g, classes in phases.items():
        largest = 0
        for C in classes:
            largest = max(largest, (U & C).bit_count())
            if largest == Q//g:
                break
        answer[g] = largest
    return answer


def minimum_frontier(pairs):
    frontier, least_T = [], None
    for gap, T in sorted(set(pairs)):
        if least_T is None or T < least_T:
            frontier.append([gap, T])
            least_T = T
    return frontier


ANCHORS = {
    135: (8, 9, 10, 12, 15, 18, 20, 24),
    405: (8, 9, 10, 12, 15, 18, 20, 24, 27, 30, 36, 40, 45,
          54, 60, 72, 81, 90, 108, 120, 135),
}


def search(M, max_nodes=200000, seconds=120):
    require(M in ANCHORS, 'unsupported proof case')
    Q, anchors = 8*M, ANCHORS[M]
    head = tuple(m for m in divisors(Q) if m >= 8)
    tail = tuple(8*d for d in divisors(M))
    require(len(set(anchors)) == len(anchors) and all(m in head for m in anchors),
            'invalid anchors')
    phase_masks = masks(Q, sorted(set(head) | set(tail)))
    remaining = [tuple(m for m in head if m not in anchors[:k])
                 for k in range(len(anchors)+1)]
    nodes, cuts = [0]*(len(anchors)+1), [0]*(len(anchors)+1)
    events, cut_pairs = [], []
    leaves = equalities = 0
    start = monotonic()
    ordered_digest = sha256()

    def visit(depth, U, previous):
        nonlocal leaves, equalities
        nodes[depth] += 1
        if sum(nodes) > max_nodes or monotonic()-start > seconds:
            raise IncompleteSearch('bounded independent replay incomplete')
        counts = maxima(Q, U, phase_masks)
        size = U.bit_count()
        H = sum(counts[g] for g in remaining[depth])
        T = sum(counts[g] for g in tail)
        gap = size-H-T
        cut = size > 0 and gap >= 0
        if cut or depth == len(anchors):
            if cut:
                require(T > 0, 'invalid zero-tail cut')
                cuts[depth] += 1
                equalities += gap == 0
                cut_pairs.append((gap, T))
            else:
                leaves += 1
            tag = 'cut' if cut else 'leaf'
            original = [tag, [a for _, a in previous], size, H, T, Q-gap]
            ordered_digest.update((json.dumps(original, separators=(',', ':'))+'\n').encode())
            normalized = [tag, renamed_residues(previous), size, H, T, Q-gap]
            events.append(json.dumps(normalized, separators=(',', ':')))
            return
        m = anchors[depth]
        for a in representatives(m, previous):
            visit(depth+1, U & ~phase_masks[m][a], previous+((m, a),))

    visit(0, (1 << Q)-1, ())
    require(cut_pairs, 'no completed terminal cuts')
    events.sort()
    frontier = minimum_frontier(cut_pairs)
    # Exact minima for selected finite horizons, with dominance checked on
    # every terminal pair. The displayed formula works for every horizon.
    finite_minima = []
    for h in range(9):
        direct = min((1 << h)*gap+T for gap, T in cut_pairs)
        compressed = min((1 << h)*gap+T for gap, T in frontier)
        require(direct == compressed, 'incorrect finite-horizon compression')
        finite_minima.append(direct)
    result = {
        'M': M, 'Q': Q, 'anchors': list(anchors),
        'head_moduli': list(head), 'tail_phase_moduli': list(tail),
        'nodes_per_depth': nodes, 'cuts_per_depth': cuts,
        'nodes': sum(nodes), 'cuts': sum(cuts), 'uncut_leaves': leaves,
        'equality_cuts': equalities,
        'max_infinite_capacity_at_cut': Q-min(gap for gap, _ in cut_pairs),
        'min_tail_capacity_at_cut': min(T for _, T in cut_pairs),
        'pareto_minimum_pairs_gap_and_T': frontier,
        'uncovered_lower_bounds_for_A_equals_3_through_11': finite_minima,
        'uncovered_lower_bound_for_every_A_ge_3': 'min(2**(A-3)*gap+T over frontier)',
        'sorted_normalized_terminal_sha256': sha256(('\n'.join(events)+'\n').encode()).hexdigest(),
        'ordered_independent_terminal_sha256': ordered_digest.hexdigest(),
    }
    return result, events


def tree_group(p, depth):
    if depth == 0:
        return [(0,)]
    sub = tree_group(p, depth-1)
    return [tuple(root[x % p]+p*child[x % p][x//p] for x in range(p**depth))
            for root in permutations(range(p)) for child in product(sub, repeat=p)]


def literal_finite_bound(p, M, e, minimum, assigned, U, h):
    Q, L = p**e*M, p**(e+h)*M
    residual = [x for x in range(L) if x % Q in U]
    capacities = []
    for n in divisors(L):
        if n < minimum or n in assigned:
            continue
        capacities.append(max(sum(x % n == a for x in residual) for a in range(n)))
    return L-len(residual)+sum(capacities)


def series_finite_bound(p, M, e, minimum, assigned, U, h):
    Q = p**e*M
    cap = lambda n: max(sum(x % n == a for x in U) for a in range(n))
    H = sum(cap(n) for n in divisors(Q) if n >= minimum and n not in assigned)
    T = sum(cap(p**e*d) for d in divisors(M))
    return p**h*(Q-len(U)+H)+sum(p**j for j in range(h))*T


def controls():
    orbit_checks = 0
    for p, depth, moduli in [(2, 3, (2, 4)), (2, 3, (4, 8)), (3, 2, (3, 9))]:
        group, m = tree_group(p, depth), p**depth
        for residues in product(*(range(n) for n in moduli)):
            previous = tuple(zip(moduli, residues))
            stabilizer = [f for f in group if all(f[a] % n == a for n, a in previous)]
            blocks = {}
            for a in range(m):
                blocks.setdefault(signature(m, a, previous), set()).add(a)
            actual = {frozenset(f[a] for f in stabilizer) for a in range(m)}
            require({frozenset(B) for B in blocks.values()} == actual, 'stabilizer orbit failure')
            orbit_checks += 1
    finite_checks = 0
    for p, M, e, minimum in [(2, 3, 0, 2), (2, 3, 1, 2), (3, 2, 1, 2)]:
        Q = p**e*M
        require(p**(e+1) >= minimum, 'test tail eligibility')
        for bits in range(1 << Q):
            U = {x for x in range(Q) if bits >> x & 1}
            for h in range(4):
                require(literal_finite_bound(p, M, e, minimum, (), U, h) ==
                        series_finite_bound(p, M, e, minimum, (), U, h),
                        'finite CRT/geometric-tail identity failure')
                finite_checks += 1
    # A zero infinite-capacity gap can genuinely leave exactly one point at
    # every finite depth. This is a positive equality-boundary control.
    for h in range(7):
        L = 1 << h
        classes = [(1 << j, (1 << (j-1))-1) for j in range(1, h+1)]
        missing = [x for x in range(L) if not any(x % n == a for n, a in classes)]
        require(missing == [L-1], 'sharp finite-tail equality control')
    # A known complete period-12 cover must survive all its prefix cuts.
    cover = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    require(all(any(x % n == a for n, a in cover) for x in range(12)), 'positive cover fixture')
    for k in range(6):
        U = {x for x in range(12) if not any(x % n == a for n, a in cover[:k])}
        assigned = tuple(n for n, _ in cover[:k])
        infinite = series_finite_bound(2, 3, 2, 2, assigned, U, 1)
        # The finite h=1 upper bound must allow the repeated genuine cover.
        require(infinite >= 24, 'a genuine covering prefix was excluded')
    try:
        search(135, max_nodes=0)
    except IncompleteSearch:
        pass
    else:
        raise RuntimeError('node-budget exhaustion was accepted')
    return {'full_tree_stabilizer_checks': orbit_checks,
            'full_period_finite_capacity_checks': finite_checks,
            'sharp_equality_horizons': 7, 'genuine_period12_prefixes': 6,
            'budget_exhaustion_rejected': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--events', type=Path, help='optional scratch-only terminal records')
    args = parser.parse_args()
    checked_controls, results, events = controls(), [], {}
    for M in (135, 405):
        result, rows = search(M)
        require(result['uncut_leaves'] == 0, 'an unresolved leaf remains')
        results.append(result)
        events[str(M)] = rows
    if args.events is not None:
        args.events.write_text(json.dumps(events)+'\n')
    print(json.dumps({'agent': 'six-reviewer-1', 'role': 'independent reviewer',
                      'controls': checked_controls, 'cases': results}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
