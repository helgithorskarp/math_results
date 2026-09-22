"""Independent objects: no import of the counting formula or its parameters."""

from collections import Counter
from itertools import permutations


def avoids_123(p):
    # Literal forbidden subsequences, separate from the insertion construction.
    return not any(p[i] < p[j] < p[k]
                   for i in range(len(p)) for j in range(i+1, len(p))
                   for k in range(j+1, len(p)))


def insert_maximum(previous, n):
    # A newly inserted maximum creates 123 precisely when its prefix has an
    # increasing pair. Thus it can follow any decreasing prefix, including [].
    for p in previous:
        prefix = 1 if p else 0
        while prefix < len(p) and p[prefix-1] > p[prefix]:
            prefix += 1
        for j in range(prefix+1):
            yield p[:j] + (n,) + p[j:]


def observed(p):
    fixed = [i for i, value in enumerate(p, 1) if i == value]
    if len(fixed) != 2:
        return None
    a, b = fixed
    x = sum(a < value < b for value in p[:a-1])
    y = sum(value > b for value in p[a:b-1])
    e = sum(value > i for i, value in enumerate(p, 1))
    return b-a, x, y, a, e


def build_observations(maximum=12, literal_maximum=9):
    previous = [()]
    results = []
    for n in range(1, maximum+1):
        current = list(insert_maximum(previous, n))
        if len(set(current)) != len(current):
            raise ValueError((n, "insertion duplicates"))
        if n <= literal_maximum:
            literal = {p for p in permutations(range(1, n+1)) if avoids_123(p)}
            if set(current) != literal:
                raise ValueError((n, "literal and insertion sets differ"))
        histogram = Counter()
        for p in current:
            row = observed(p)
            if row is not None:
                histogram[row] += 1
        results.append((n, len(current), histogram))
        previous = current
    return results


def path_counts(length):
    # Count nonnegative up/down walks directly, without binomial arithmetic.
    counts = [1]
    for _ in range(length):
        nxt = [0]*(len(counts)+1)
        for height, number in enumerate(counts):
            nxt[height+1] += number
            if height:
                nxt[height-1] += number
        counts = nxt
    return counts
