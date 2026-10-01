"""Carry-aware exact binary fibers for seven-AP avoidance in Z/621Z."""
from collections import Counter
from math import gcd

M = 207
N = 621
K = 7


def validate_skeleton(tau):
    if len(tau) != M or any(type(t) is not int or t not in (0, 1, 2) for t in tau):
        raise ValueError("skeleton must contain exactly 207 ternary integers")


def local_patterns(t):
    if len(t) != K or any(type(z) is not int or z not in (0, 1, 2) for z in t):
        raise ValueError("local vector must have seven ternary entries")
    counts = Counter()
    for b in range(3):
        for s in range(3):
            mask = sum(int((b + j * s - t[j]) % 3 == 0) << j for j in range(K))
            counts[min(mask, mask ^ 127)] += 1
    return counts


def canonical_key(xs, mask):
    ordered = sorted(zip(xs, ((mask >> j) & 1 for j in range(K))))
    support = tuple(x for x, bit in ordered)
    if len(set(support)) != K:
        raise ValueError("non-distinct support")
    word = sum(bit << i for i, (x, bit) in enumerate(ordered))
    return support, min(word, word ^ 127)


def projected_progressions():
    # Reversal chooses r in 1,...,103; r=69 has projected order three.
    for r in range(1, 104):
        if r == 69:
            continue
        for a in range(M):
            xs = tuple((a + j * r) % M for j in range(K))
            yield a, r, xs


def edges(tau):
    validate_skeleton(tau)
    result = Counter()
    for a, r, xs in projected_progressions():
        t = tuple((tau[x] - (a + j * r) // M) % 3 for j, x in enumerate(xs))
        for mask, weight in local_patterns(t).items():
            result[canonical_key(xs, mask)] += weight
    return result


def clauses(weighted_edges, normalize=True):
    for support, mask in weighted_edges:
        row = tuple(-(x + 1) if (mask >> j) & 1 else x + 1
                    for j, x in enumerate(support))
        yield row
        yield tuple(-literal for literal in row)
    if normalize:
        yield (-1,)


def decode(tau, u):
    validate_skeleton(tau)
    if len(u) != M or any(type(bit) is not int or bit not in (0, 1) for bit in u):
        raise ValueError("orientation must contain exactly 207 binary integers")
    return [u[x] ^ int(y == tau[x]) for y in range(3) for x in range(M)]


def weighted_cost(weighted_edges, u):
    total = 0
    for (support, mask), weight in weighted_edges.items():
        word = sum(u[x] << j for j, x in enumerate(support))
        if min(word, word ^ 127) == mask:
            total += weight
    return total


def carry_bad_starts(tau, r):
    validate_skeleton(tau)
    if not 1 <= r < M or M // gcd(r, M) < K:
        raise ValueError("projected step must have order at least seven")
    defect = {x for x in range(M)
              if (tau[(x + 3 * r) % M] - tau[x] - (x + 3 * r) // M) % 3}
    bad = {(x - j * r) % M for x in defect for j in range(4)}
    return defect, bad


def skeletons():
    yield "constant", [0] * M
    yield "thirds", [x // 69 for x in range(M)]
    yield "digit3", [(x // 3) % 3 for x in range(M)]
    yield "digit9", [(x // 9) % 3 for x in range(M)]
    yield "digit23", [(x // 23) % 3 for x in range(M)]
    yield "residue3", [x % 3 for x in range(M)]
