"""Exact count bounds after consuming original labels twelve and sixteen."""
from functools import lru_cache

N = 720
LABELS = tuple(m for m in range(8, N + 1) if N % m == 0)
FULL = (1 << N) - 1
ODD = sum(1 << x for x in range(1, N, 2))
EVEN = FULL ^ ODD
FIXED = sum(1 << x for x in range(N) if x % 8 == 5 or x % 9 == 6)
MASKS = {m: tuple(sum(1 << x for x in range(a, N, m)) for a in range(m))
         for m in LABELS}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pareto(options):
    result, largest_even = [], -1
    for o, e in sorted(set(options), reverse=True):
        if e > largest_even:
            result.append((o, e))
            largest_even = e
    return tuple(result)


def bound(a18, c6, consumed):
    require(type(a18) is int and 0 <= a18 < 18 and
            type(c6) is int and 0 <= c6 < 6, 'noncanonical target phase')
    require(set(consumed) in ({12}, {12, 16}) and
            all(type(a) is int and 0 <= a < m for m, a in consumed.items()),
            'wrong original consumed labels or phases')
    pool = tuple(m for m in LABELS if m not in (8, 9) and m not in consumed)
    low, high = pool[:12], pool[12:]
    require(len(pool) in (20, 21) and len(low) == 12 and len(high) in (8, 9),
            'wrong original-resource census')
    known = FIXED | sum(1 << x for x in range(N) if x % 18 == a18 or x % 6 == c6)
    for m, a in consumed.items():
        known |= MASKS[m][a]
    R = FULL & ~known
    O, E = R & ODD, R & EVEN
    single = {m: pareto(((p & O).bit_count(), (p & E).bit_count()) for p in MASKS[m])
              for m in pool}
    pairs = {(i, j): pareto((((p | q) & O).bit_count(), ((p | q) & E).bit_count())
                            for p in MASKS[low[i]] for q in MASKS[low[j]])
             for i in range(12) for j in range(i + 1, 12)}
    states = {0: 0}
    for m in high:
        new = {}
        for o, e in states.items():
            for a, b in single[m]:
                new[o + a] = max(new.get(o + a, -1), e + b)
        states = new
    high_max = max(states)
    terminal = tuple(max((e for o, e in states.items() if o >= t), default=None)
                     for t in range(high_max + 1))
    low_max = [0] * (1 << 12)
    for mask in range(1, len(low_max)):
        bit = mask & -mask
        i = bit.bit_length() - 1
        low_max[mask] = low_max[mask ^ bit] + max(o for o, e in single[low[i]])

    @lru_cache(None)
    def recurse(mask, t):
        if t > low_max[mask] + high_max:
            return None
        if not mask:
            return terminal[t]
        i = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << i)
        answers = []
        for j in range(i + 1, 12):
            if rest & (1 << j):
                candidates = []
                for o, e in pairs[i, j]:
                    child = recurse(rest ^ (1 << j), max(0, t - o))
                    if child is not None:
                        candidates.append(e + child)
                if not candidates:
                    return None
                answers.append(max(candidates))
        require(answers, 'unpaired recursive resource')
        return min(answers)

    upper = recurse((1 << 12) - 1, O.bit_count())
    return (O.bit_count(), E.bit_count(), upper), sum(low[i] * low[j] for i, j in pairs)


def strict(row):
    return row[-1] is None or row[-1] < row[-2]
