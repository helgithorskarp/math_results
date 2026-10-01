"""Integer union-count bounds. Python standard library; no solver."""
from functools import lru_cache
from math import gcd

PERIOD = 720
LABELS = [m for m in range(8, PERIOD + 1) if PERIOD % m == 0]
FREE = [m for m in LABELS if m not in (8, 9)]
FULL = (1 << PERIOD) - 1
FIXED = sum(1 << x for x in range(PERIOD) if x % 8 == 5 or x % 9 == 6)
ODD = sum(1 << x for x in range(1, PERIOD, 2))
EVEN = FULL ^ ODD
MASKS = {m: [sum(1 << x for x in range(a, PERIOD, m)) for a in range(m)] for m in FREE}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def residual(a, c):
    require(type(a) is int and 0 <= a < 18 and type(c) is int and 0 <= c < 6,
            'target phases must be canonical integers')
    allowed = sum(1 << x for x in range(PERIOD) if x % 18 == a or x % 6 == c)
    return FULL & ~(FIXED | allowed), allowed & ~FIXED


def scalar_budget(R, groups, u, v):
    require(type(u) is int and type(v) is int and u >= 0 and v >= 0 and u + v > 0,
            'parity weights must be nonnegative nonzero integers')
    flat = [m for group in groups for m in group]
    require(sorted(flat) == FREE, 'partition repeats or omits an original resource')
    require(all(1 <= len(g) <= 2 for g in groups), 'only singleton/pair groups supported')
    O, E = R & ODD, R & EVEN
    capacities, combinations = [], 0
    for group in groups:
        if len(group) == 1:
            candidates = MASKS[group[0]]
        else:
            candidates = [p | q for p in MASKS[group[0]] for q in MASKS[group[1]]]
        combinations += len(candidates)
        capacities.append(max(u * (mask & O).bit_count() + v * (mask & E).bit_count()
                              for mask in candidates))
    return u * O.bit_count() + v * E.bit_count(), sum(capacities), capacities, combinations


def pareto(options):
    # The count bound is nonincreasing in the odd threshold. Therefore a
    # phase pair with both smaller counts never enlarges the upper bound.
    result, largest_even = [], -1
    for o, e in sorted(set(options), reverse=True):
        if e > largest_even:
            result.append((o, e))
            largest_even = e
    return result


def count_envelope(R):
    O, E = R & ODD, R & EVEN
    low, high = FREE[:14], FREE[14:]
    single = {m: pareto(((p & O).bit_count(), (p & E).bit_count()) for p in MASKS[m])
              for m in FREE}
    pairs = {(i, j): pareto((((p | q) & O).bit_count(), ((p | q) & E).bit_count())
                            for p in MASKS[low[i]] for q in MASKS[low[j]])
             for i in range(14) for j in range(i + 1, 14)}
    high_states = {0: 0}
    for m in high:
        new = {}
        for o, e in high_states.items():
            for a, b in single[m]:
                new[o + a] = max(new.get(o + a, -1), e + b)
        high_states = new
    high_max = max(high_states)
    high_bounds = [max((e for o, e in high_states.items() if o >= t), default=None)
                   for t in range(high_max + 1)]
    max_odd = [0] * (1 << 14)
    for mask in range(1, len(max_odd)):
        bit = mask & -mask
        i = bit.bit_length() - 1
        max_odd[mask] = max_odd[mask ^ bit] + max(o for o, e in single[low[i]])

    @lru_cache(None)
    def bound(mask, t):
        # None means that even the count relaxation cannot meet t odd
        # points; it is justified by the same induction, not a timeout.
        if t > max_odd[mask] + high_max:
            return None
        if not mask:
            return high_bounds[t]
        i = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << i)
        answers = []
        for j in range(i + 1, 14):
            if not rest & (1 << j):
                continue
            candidates = []
            for o, e in pairs[i, j]:
                child = bound(rest ^ (1 << j), max(0, t - o))
                if child is not None:
                    candidates.append(e + child)
            if not candidates:
                return None
            answers.append(max(candidates))
        return min(answers)

    upper = bound((1 << 14) - 1, O.bit_count())
    return {'odd_demand': O.bit_count(), 'even_demand': E.bit_count(), 'even_upper': upper}


def valid_affine(u, t):
    return (type(u) is int and type(t) is int and gcd(u, PERIOD) == 1 and
            (5 * u + t) % 8 == 5 and (6 * u + t) % 9 == 6)


def affine_maps():
    return [(u, t) for u in range(1, PERIOD) if gcd(u, PERIOD) == 1
            for t in range(72) if valid_affine(u, t)]
