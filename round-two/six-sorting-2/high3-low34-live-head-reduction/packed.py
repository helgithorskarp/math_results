"""Four verbatim packed primitives credited in SOURCE-CREDITS.md."""
from functools import lru_cache

LOW, HIGH = "L", "H"


@lru_cache(None)
def truth_columns(m):
    return tuple(sum(1 << x for x in range(1 << m) if (x >> j) & 1)
                 for j in range(m))



def mask(indices):
    return sum(1 << i for i in indices)



def marked_ports(values):
    return (mask(i for i, x in enumerate(values) if x == LOW),
            mask(i for i, x in enumerate(values) if x == HIGH))



def transition(values, a, b):
    x, y = values[a], values[b]
    if isinstance(x, str) or isinstance(y, str):
        def order(z):
            return -1 if z == LOW else 1 if z == HIGH else 0
        if order(x) > order(y):
            values[a], values[b] = y, x
        return 1, 0
    redundant = int((x & ~y) == 0)
    values[a], values[b] = x & y, x | y
    return 0, redundant
