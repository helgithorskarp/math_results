"""Exact disjoint chain coordinates; Python standard library, no solver."""
from functools import cache
from collections import Counter


def hook(a, b, t):
    """The t-th symmetric chain of [a] x [b], with both ranks starting at 0."""
    if not (a >= 1 and b >= 1 and 0 <= t < min(a, b)):
        raise ValueError('rectangle coordinates')
    return [(i, t) for i in range(a-t)] + [(a-1-t, j) for j in range(t+1, b)]


def hook_inverse(a, b, t, h):
    if not (0 <= t < min(a, b) and 0 <= h < a+b-1-2*t):
        raise ValueError('hook position')
    return (h, t) if h < a-t else (a-1-t, t+1+h-(a-t))


def hook_address(a, b, i, j):
    if not (0 <= i < a and 0 <= j < b):
        raise ValueError('rectangle point')
    t = min(j, a-1-i)
    return t, i if j == t else a+j-2*t-1


@cache
def local(red):
    """A saturated chain partition of B4 with its forbidden endpoint removed."""
    if red not in (0, 1):
        raise ValueError('block color')
    out = [[0]]
    for bit in range(4):
        out = [[c[i] | (j << bit) for i, j in hook(len(c), 2, t)]
               for c in out for t in range(min(len(c), 2))]
    banned = 15 if red else 0
    return tuple(tuple(x for x in c if x != banned) for c in out)


@cache
def ways(remaining, a=1):
    if remaining < 0 or a < 1:
        raise ValueError('suffix dimensions')
    if remaining == 0:
        return 1
    return sum(mult * sum(ways(remaining-1, a+b-1-2*t)
                          for t in range(min(a, b)))
               for b, mult in ((1, 2), (3, 3), (4, 1)))


def distribution(m):
    d = Counter({1: 1})
    for _ in range(m):
        nxt = Counter()
        for a, v in d.items():
            for b, mult in ((1, 2), (3, 3), (4, 1)):
                for t in range(min(a, b)):
                    nxt[a+b-1-2*t] += v*mult
        d = nxt
    return d


class Product:
    """Integer chain index plus within-chain position, bijective with all states."""
    def __init__(self, colors):
        self.colors = tuple(colors)
        self.parts = tuple(local(c) for c in self.colors)
        self.m = len(colors)
        self.size = ways(self.m)

    def path(self, index):
        if type(index) is not int or not 0 <= index < self.size:
            raise ValueError('chain index')
        a, path = 1, []
        for i, parts in enumerate(self.parts):
            found = False
            for j, c in enumerate(parts):
                b = len(c)
                for t in range(min(a, b)):
                    length = a+b-1-2*t
                    count = ways(self.m-i-1, length)
                    if index >= count:
                        index -= count
                    else:
                        path.append((a, b, j, t))
                        a, found = length, True
                        break
                if found:
                    break
            if not found:
                raise ValueError('unranking gap')
        return tuple(path), a

    def state(self, index, position):
        path, length = self.path(index)
        if type(position) is not int or not 0 <= position < length:
            raise ValueError('chain position')
        out = [None]*self.m
        for i in reversed(range(self.m)):
            a, b, j, t = path[i]
            position, v = hook_inverse(a, b, t, position)
            out[i] = self.parts[i][j][v]
        if position != 0:
            raise ValueError('nonzero origin')
        return tuple(out)

    def address(self, state):
        if len(state) != self.m:
            raise ValueError('star vector length')
        a, h, index = 1, 0, 0
        for i, (value, parts) in enumerate(zip(state, self.parts)):
            candidates = [(j, c.index(value)) for j, c in enumerate(parts) if value in c]
            if len(candidates) != 1:
                raise ValueError('star outside domain')
            j, v = candidates[0]
            b = len(parts[j])
            t, h = hook_address(a, b, h, v)
            for jj, c in enumerate(parts):
                for tt in range(min(a, len(c))):
                    if (jj, tt) == (j, t):
                        break
                    index += ways(self.m-i-1, a+len(c)-1-2*tt)
                if jj == j:
                    break
            a = a+b-1-2*t
        return index, h
