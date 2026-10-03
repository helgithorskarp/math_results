"""Fresh reviewer field definitions; no target executable or certificate imports."""
Q = 103
ROOTS = (1, 2, 4)
FREE = frozenset((0, *ROOTS))

def require(condition, message):
    if not condition:
        raise ValueError(message)

def gauss(x):
    x %= Q
    require(x != 0, 'undefined character')
    return sum((k*x) % Q > Q//2 for k in range(1, Q//2+1)) % 2

def label(x):
    require(x not in FREE, 'free column')
    return 4*gauss(x-1) + 2*gauss(x-2) + gauss(x-4)

def candidates():
    labels = {x:label(x) for x in range(Q) if x not in FREE}
    records = []
    for d in range(1, 52):
        for a in range(Q):
            points = tuple((a+j*d) % Q for j in range(7))
            if FREE.intersection(points):
                continue
            support = frozenset(points)
            require(len(support) == 7, 'repeated point')
            pattern = frozenset(labels[x] for x in points)
            records.append((a, d, support, pattern))
    return records
