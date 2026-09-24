"""Exact flow and matching routines reused verbatim from the clique extension.
Source provenance is recorded in SOURCES.md. No universal design constructor.
"""
from collections import deque
from fractions import Fraction


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Dinic:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]
        self.augmentations = 0

    def add(self, a, b, capacity):
        require(type(capacity) is int and capacity >= 0, 'invalid capacity')
        f = [b, len(self.graph[b]), capacity]
        r = [a, len(self.graph[a]), 0]
        self.graph[a].append(f)
        self.graph[b].append(r)
        return f

    def max_flow(self, source, sink):
        total = 0
        n = len(self.graph)
        while True:
            level = [-1] * n
            level[source] = 0
            queue = deque([source])
            while queue:
                a = queue.popleft()
                for b, rev, cap in self.graph[a]:
                    if cap and level[b] < 0:
                        level[b] = level[a] + 1
                        queue.append(b)
            if level[sink] < 0:
                return total
            cursor = [0] * n

            def augment(a, cap):
                if a == sink:
                    return cap
                while cursor[a] < len(self.graph[a]):
                    e = self.graph[a][cursor[a]]
                    b, rev, left = e
                    if left and level[b] == level[a] + 1:
                        sent = augment(b, min(cap, left))
                        if sent:
                            e[2] -= sent
                            self.graph[b][rev][2] += sent
                            return sent
                    cursor[a] += 1
                return 0

            while True:
                sent = augment(source, 10**30)
                if not sent:
                    break
                self.augmentations += 1
                total += sent


def allocate_spokes(available, columns, quota):
    """Integral bipartite rounding of row-normalized fractional edge weights."""
    require(type(columns) is int and columns >= 1, 'invalid column count')
    require(type(quota) is int and quota >= 0, 'invalid row quota')
    rows = len(available)
    require(rows > 0, 'empty row set')
    for neighbors in available:
        require(all(type(y) is int and 0 <= y < columns for y in neighbors), 'invalid spoke')
        require(quota <= len(neighbors), 'row quota infeasible')
    if quota == 0:
        return [set() for _ in available], {'augmentations': 0}
    fractions = [Fraction(0) for _ in range(columns)]
    for neighbors in available:
        weight = Fraction(quota, len(neighbors))
        for y in neighbors:
            fractions[y] += weight
    source, sink = rows + columns, rows + columns + 1
    super_source, super_sink = sink + 1, sink + 2
    network = Dinic(super_sink + 1)
    balance = [0] * (sink + 1)

    def bounded(a, b, low, high):
        require(0 <= low <= high, 'invalid lower bound')
        balance[a] -= low
        balance[b] += low
        return network.add(a, b, high-low)

    for x in range(rows):
        bounded(source, x, quota, quota)
    arcs = []
    for x, neighbors in enumerate(available):
        arcs.append([(y, bounded(x, rows+y, 0, 1)) for y in sorted(neighbors)])
    for y, value in enumerate(fractions):
        low = value.numerator // value.denominator
        high = -(-value.numerator // value.denominator)
        bounded(rows+y, sink, low, high)
    bounded(sink, source, 0, rows*quota)
    demand = 0
    for a, b in enumerate(balance):
        if b > 0:
            network.add(super_source, a, b)
            demand += b
        elif b < 0:
            network.add(a, super_sink, -b)
    require(network.max_flow(super_source, super_sink) == demand, 'fractional rounding flow failed')
    selected = [{y for y, arc in row if arc[2] == 0} for row in arcs]
    return selected, {'augmentations': network.augmentations}


def avoiding_matching(left, right, forbidden):
    """Exact augmenting matching; allowed pairs are the complement of forbidden."""
    left, right = sorted(left), sorted(right)
    require(len(left) == len(right) and len(set(left)) == len(left) and
            len(set(right)) == len(right) and not set(left).intersection(right), 'bad matching sides')
    n = len(left)
    position = {v: j for j, v in enumerate(right)}
    full = (1 << n)-1
    masks = []
    for u in left:
        bad = sum(1 << position[v] for v in forbidden.get(u, ()) if v in position)
        masks.append(full ^ bad)
    at_right = [-1] * n
    at_left = [-1] * n
    free = full
    repairs = 0
    for i, mask in enumerate(masks):
        choices = mask & free
        if choices:
            bit = choices & -choices
            j = bit.bit_length()-1
            free ^= bit
            at_right[j] = i
            at_left[i] = j
            continue
        repairs += 1
        queue = deque([i])
        seen_left = {i}
        seen_right = 0
        parent = {}
        end = None
        while queue and end is None:
            a = queue.popleft()
            choices = masks[a] & ~seen_right
            while choices:
                bit = choices & -choices
                choices ^= bit
                seen_right |= bit
                b = bit.bit_length()-1
                parent[b] = a
                old = at_right[b]
                if old < 0:
                    end = b
                    break
                if old not in seen_left:
                    seen_left.add(old)
                    queue.append(old)
        require(end is not None, 'no avoiding perfect matching')
        free &= ~(1 << end)
        while end >= 0:
            a = parent[end]
            old = at_left[a]
            at_left[a] = end
            at_right[end] = a
            end = old
    return [(left[i], right[j]) for i, j in enumerate(at_left)], repairs
